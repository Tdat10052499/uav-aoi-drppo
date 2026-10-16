"""Aggregate evaluation CSVs and test the pre-registered hypotheses (docs/03 section 6).

  python scripts/analyze.py results/*.csv --out results/summary.md

Per-seed aggregation: each (method, train_seed, suite) -> mean over evaluation episodes.
Heuristics have no training seed; each evaluation episode is then treated as a replicate
for the descriptive table only (they are deterministic given the scenario).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--metric", default="mean_aoi")
    ap.add_argument("--proposed", default="dr_ppo")
    ap.add_argument("--fixed", default="fixed_ppo")
    ap.add_argument("--heuristic", default="tsp")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    rows = load(args.csv)
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

    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
