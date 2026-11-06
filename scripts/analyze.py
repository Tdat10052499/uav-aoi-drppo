"""Aggregate evaluation CSVs and test the pre-registered hypotheses (docs/03 section 6).

  python scripts/analyze.py results/raw/EXP-0*/*/events.csv --out results/processed/summary.md

Per-seed aggregation: each (method, train_seed, suite) -> mean over evaluation episodes.
Heuristics have no training seed; each evaluation episode is then treated as a replicate
for the descriptive table only (they are deterministic given the scenario).

Additions after the PREREG lock (docs/PREREG.md sec. 1 allows reporting-only additions; the
summary table, the H1 table and the H2 line above are produced by the locked code unchanged):
  - run filter: only CSVs whose run_record.json says status = completed (PREREG sec. 9);
    excluded files are listed in the output.
  - duplicate guard: the same (method, train_seed, suite, episode_seed) in two CSVs stops the
    run, because per_seed() would otherwise silently average, e.g., EXP-02b seed 0 with
    EXP-03 seed 0.
  - H1 decision table per PREREG sec. 8: Delta_s = mean deg_Fixed - mean deg_DR with a
    two-sample bootstrap 95% CI, IQM of deg per arm, "pass" = p_Holm < 0.05 and
    Delta_s >= 0.10, and the >= 3/4 verdict. p-values are taken from the locked H1 block.
  - per-seed table of A_id and deg (issue #14), secondary metrics (descriptive only,
    PREREG sec. 7), and figure F4 (--fig) with an alt-text file next to it.

  python scripts/analyze.py results/raw/EXP-03/*/events.csv \\
      --out results/processed/EXP-03_summary.md --fig figures/F4_deg.pdf
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import numpy as np

from uavaoi.stats import bootstrap_ci, cliffs_delta, holm, iqm, ood_degradation, permutation_test

OOD = ["ood_cluster", "ood_density", "ood_area", "ood_energy"]


def load(paths):
    rows = []
    for p in paths:
        with open(p) as f:
            rows += list(csv.DictReader(f))
    return rows


def per_seed(rows, metric="mean_aoi"):
    """{method: {suite: {train_seed: mean over episodes}}}"""
    acc = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in rows:
        acc[r["method"]][r["suite"]][int(r["train_seed"])].append(float(r[metric]))
    return {m: {s: {k: float(np.mean(v)) for k, v in d2.items()} for s, d2 in d1.items()}
            for m, d1 in acc.items()}


# ---------------------------------------------------------------------- additions after the lock
DELTA_H1 = 0.10        # PREREG sec. 8 (LDN, 03/11/2026)
N_SEEDS_PREREG = 10    # PREREG sec. 5/7
N_BOOT, BOOT_SEED = 10_000, 0
SECONDARY = ["peak_aoi", "energy_frac", "early_termination", "coverage", "collections",
             "hover_frac", "slow_frac", "fast_frac", "boundary_hits"]
LABEL = {"ood_cluster": "cluster", "ood_density": "density", "ood_area": "area", "ood_energy": "energy"}


def select_runs(paths, include_incomplete=False):
    """Keep CSVs whose sibling run_record.json has status 'completed' (PREREG sec. 9, rules 1 and 5)."""
    keep, excluded = [], []
    for p in paths:
        rec = os.path.join(os.path.dirname(os.path.abspath(p)), "run_record.json")
        if not os.path.exists(rec):
            status, run_id = "no run_record.json", os.path.basename(os.path.dirname(p))
        else:
            with open(rec) as f:
                r = json.load(f)
            status, run_id = r.get("status", "missing status"), r.get("run_id", os.path.basename(os.path.dirname(p)))
        if status == "completed" or include_incomplete:
            keep.append(p)
        else:
            excluded.append((p, run_id, status))
    if not keep:
        sys.exit("analyze.py: no completed run among the given CSVs")
    return keep, excluded


def check_duplicates(paths):
    """Stop if one (method, train_seed, suite, episode_seed) appears in more than one CSV."""
    seen, clashes = {}, defaultdict(set)
    for p in paths:
        with open(p) as f:
            for r in csv.DictReader(f):
                k = (r["method"], r["train_seed"], r["suite"], r["episode_seed"])
                if k in seen and seen[k] != p:
                    clashes[k[:2]].update({seen[k], p})
                seen.setdefault(k, p)
    if clashes:
        msg = ["analyze.py: the same method/train_seed/suite/episode_seed occurs in several CSVs.",
               "per_seed() would average them silently. Pass only one evaluation per (method, seed):"]
        for (m, s), files in sorted(clashes.items()):
            msg.append(f"  {m} seed {s}: " + ", ".join(sorted(files)))
        sys.exit("\n".join(msg))


def boot_diff_ci(x, y, n_boot=N_BOOT, alpha=0.05, seed=BOOT_SEED):
    """Percentile bootstrap CI of mean(x) - mean(y), x and y resampled independently."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rng = np.random.default_rng(seed)
    bx = rng.choice(x, (n_boot, len(x)), replace=True).mean(axis=1)
    by = rng.choice(y, (n_boot, len(y)), replace=True).mean(axis=1)
    d = bx - by
    return float(x.mean() - y.mean()), float(np.quantile(d, alpha / 2)), float(np.quantile(d, 1 - alpha / 2))


def fmt_ci(pt, lo, hi, nd=3):
    return f"{pt:+.{nd}f} [{lo:+.{nd}f}; {hi:+.{nd}f}]"


def report_additions(rows, ps, args, res, adj, excluded):
    out = ["\n## Runs\n"]
    used = sorted({(r["method"], r["train_seed"]) for r in rows})
    out.append("Evaluated (method, train_seed): " + ", ".join(f"{m}/{s}" for m, s in used) + ".")
    if excluded:
        out.append("\nExcluded (PREREG sec. 9; not completed):\n")
        out += [f"- `{p}` (run `{rid}`): {st}" for p, rid, st in excluded]
    else:
        out.append("No CSV excluded.")

    if res:
        dr_seeds = sorted(ps[args.proposed][res[0][0]])
        fx_seeds = sorted(ps[args.fixed][res[0][0]])
        out += [f"\n## H1 — decision per PREREG sec. 8 (delta = {args.delta:.2f})\n",
                f"p and p_Holm are copied from the H1 table above (locked code). Delta_s = mean deg_Fixed "
                f"- mean deg_DR; 95% CI by two-sample bootstrap ({N_BOOT} resamples, seed {BOOT_SEED}). "
                f"A suite passes when p_Holm < 0.05 and Delta_s >= {args.delta:.2f}.\n"]
        if min(len(dr_seeds), len(fx_seeds)) < N_SEEDS_PREREG:
            out.append(f"**Warning:** {len(dr_seeds)} DR seed(s) and {len(fx_seeds)} Fixed seed(s), fewer than the "
                       f"{N_SEEDS_PREREG} in PREREG. This is not the registered test; read it as description only "
                       f"(CLAUDE.md rule 5: a 2-seed pilot gets no p-value).\n")
        out += ["| Suite | n DR / n Fixed | deg DR mean [95% CI] | IQM | deg Fixed mean [95% CI] | IQM | "
                "Delta_s [95% CI] | p_Holm | Pass |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        n_pass = 0
        for (s, dr, fx, _p), pa in zip(res, adj):
            d_pt, d_lo, d_hi = boot_diff_ci(fx, dr)
            ok = pa < 0.05 and d_pt >= args.delta
            n_pass += ok
            out.append(f"| {s} | {len(dr)} / {len(fx)} | {fmt_ci(*bootstrap_ci(dr))} | {iqm(dr):+.3f} | "
                       f"{fmt_ci(*bootstrap_ci(fx))} | {iqm(fx):+.3f} | {fmt_ci(d_pt, d_lo, d_hi)} | "
                       f"{pa:.4f} | {'yes' if ok else 'no'} |")
        verdict = "SUPPORTED" if n_pass >= 3 else "NOT supported"
        out.append(f"\n**H1: {n_pass}/{len(res)} suites pass -> {verdict}** (rule: >= 3/4 suites).")

        out += ["\n## Per-seed A_id and deg (issue #14)\n",
                "| Method | Seed | A_id | " + " | ".join(f"deg {LABEL[s]}" for s, *_ in res) + " |",
                "| --- | --- | --- | " + " | ".join("---" for _ in res) + " |"]
        for m in (args.proposed, args.fixed):
            for k in sorted(ps[m]["id"]):
                cells = []
                for s, *_ in res:
                    v = ps[m].get(s, {}).get(k)
                    cells.append(f"{(v - ps[m]['id'][k]) / ps[m]['id'][k]:+.3f}" if v is not None else "—")
                out.append(f"| {m} | {k} | {ps[m]['id'][k]:.2f} | " + " | ".join(cells) + " |")

    present = [c for c in SECONDARY if rows and c in rows[0]]
    if present:
        out += ["\n## Secondary metrics (descriptive only, PREREG sec. 7; mean over all episodes and seeds)\n",
                "| Method | Suite | n episodes | " + " | ".join(present) + " |",
                "| --- | --- | --- | " + " | ".join("---" for _ in present) + " |"]
        groups = defaultdict(list)
        for r in rows:
            groups[(r["method"], r["suite"])].append(r)
        for (m, s), rs in sorted(groups.items()):
            vals = []
            for c in present:
                v = [1.0 if r[c] == "True" else 0.0 if r[c] == "False" else float(r[c]) for r in rs]
                vals.append(f"{np.mean(v):.3f}")
            out.append(f"| {m} | {s} | {len(rs)} | " + " | ".join(vals) + " |")
    return out


def plot_f4(res, args):
    """F4: mean deg per OOD suite, DR vs Fixed, 95% bootstrap CI, per-seed dots. Returns a report line."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    suites = [LABEL[s] for s, *_ in res]
    x = np.arange(len(res))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    rng = np.random.default_rng(0)                    # jitter only; does not touch any statistic
    alt = []
    for j, (name, color, idx) in enumerate([("DR-PPO", "#1f5fa8", 1), ("Fixed-PPO", "#c2571a", 2)]):
        means, lo, hi = [], [], []
        for r in res:
            pt, l, h = bootstrap_ci(r[idx])
            means.append(pt), lo.append(pt - l), hi.append(h - pt)
        pos = x + (j - 0.5) * w
        ax.bar(pos, means, w, yerr=[lo, hi], capsize=3, color=color, alpha=0.85, label=name,
               error_kw={"elinewidth": 1})
        for p, r in zip(pos, res):
            ax.scatter(p + rng.uniform(-w / 4, w / 4, len(r[idx])), r[idx], s=8, color="black", zorder=3,
                       linewidths=0)
        alt.append(f"{name} mean deg: " + ", ".join(f"{s} {m:+.2f}" for s, m in zip(suites, means)) + ".")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(x, suites)
    ax.set_ylabel("deg = (Ā_ood − Ā_id) / Ā_id")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(args.fig)), exist_ok=True)
    fig.savefig(args.fig, dpi=300)
    plt.close(fig)
    n = min(len(r[1]) for r in res)
    alt_text = (f"Grouped bar chart of relative OOD degradation of mean AoI (lower is better) for DR-PPO and "
                f"Fixed-PPO on four OOD suites ({', '.join(suites)}). Bars are means over {n} training seeds "
                f"with 95% bootstrap confidence intervals; dots are individual seeds. " + " ".join(alt))
    with open(args.fig + ".alt.txt", "w") as f:
        f.write(alt_text + "\n")
    return f"\nFigure F4 written to `{args.fig}` (alt text: `{args.fig}.alt.txt`)."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--metric", default="mean_aoi")
    ap.add_argument("--proposed", default="dr_ppo")
    ap.add_argument("--fixed", default="fixed_ppo")
    ap.add_argument("--heuristic", default="tsp")
    ap.add_argument("--out", default=None)
    ap.add_argument("--fig", default=None, help="figure F4 path (.pdf/.png/.svg); alt text at <fig>.alt.txt")
    ap.add_argument("--delta", type=float, default=DELTA_H1, help="PREREG sec. 8 threshold (locked: 0.10)")
    ap.add_argument("--include-incomplete", action="store_true",
                    help="do not drop CSVs whose run_record.json is missing or not completed")
    args = ap.parse_args()

    paths, excluded = select_runs(args.csv, args.include_incomplete)
    check_duplicates(paths)
    rows = load(paths)
    ps = per_seed(rows, args.metric)
    lines = [f"# Summary ({args.metric}, lower is better)\n",
             "| Method | Suite | n | Mean [95% CI] | IQM |", "| --- | --- | --- | --- | --- |"]
    for m in sorted(ps):
        for s in sorted(ps[m]):
            seeds = ps[m][s]
            if len(seeds) == 1 and -1 in seeds:      # heuristic: use episodes
                vals = [float(r[args.metric]) for r in rows if r["method"] == m and r["suite"] == s]
            else:
                vals = list(seeds.values())
            pt, lo, hi = bootstrap_ci(vals)
            lines.append(f"| {m} | {s} | {len(vals)} | {pt:.2f} [{lo:.2f}, {hi:.2f}] | {iqm(vals):.2f} |")

    # H1: OOD degradation of DR-PPO < PPO-fixed, per OOD suite, Holm-corrected
    if args.proposed in ps and args.fixed in ps:
        lines += ["\n## H1 — OOD degradation (DR vs fixed), one-sided permutation test, Holm\n",
                  "| Suite | deg DR (mean) | deg fixed (mean) | p | p_Holm | Cliff's δ |",
                  "| --- | --- | --- | --- | --- | --- |"]
        res = []
        for s in OOD:
            try:
                dr = ood_degradation([ps[args.proposed][s][k] for k in sorted(ps[args.proposed][s])],
                                     [ps[args.proposed]["id"][k] for k in sorted(ps[args.proposed][s])])
                fx = ood_degradation([ps[args.fixed][s][k] for k in sorted(ps[args.fixed][s])],
                                     [ps[args.fixed]["id"][k] for k in sorted(ps[args.fixed][s])])
            except KeyError:
                continue
            res.append((s, dr, fx, permutation_test(dr, fx, "less")))
        adj = holm([r[3] for r in res]) if res else []
        for (s, dr, fx, p), pa in zip(res, adj):
            lines.append(f"| {s} | {dr.mean():.3f} | {fx.mean():.3f} | {p:.4f} | {pa:.4f} | "
                         f"{cliffs_delta(dr, fx):.2f} |")

    # H2: DR-PPO vs TSP on ood_cluster (seed means vs episode values, descriptive + test)
    if args.proposed in ps and args.heuristic in ps and "ood_cluster" in ps[args.proposed]:
        a = list(ps[args.proposed]["ood_cluster"].values())
        b = [float(r[args.metric]) for r in rows if r["method"] == args.heuristic and r["suite"] == "ood_cluster"]
        lines += ["\n## H2 — DR-PPO vs heuristic on ood_cluster\n",
                  f"permutation p (one-sided, DR < {args.heuristic}) = {permutation_test(a, b, 'less'):.4f}; "
                  f"Cliff's δ = {cliffs_delta(a, b):.2f}. Note: compare at equal energy budget (same suite)."]

    # ------------------------------------------------------------------ additions (see docstring)
    lines += report_additions(rows, ps, args, res if args.proposed in ps and args.fixed in ps else [],
                              adj if args.proposed in ps and args.fixed in ps else [], excluded)
    if args.fig and args.proposed in ps and args.fixed in ps and res:
        lines.append(plot_f4(res, args))

    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
