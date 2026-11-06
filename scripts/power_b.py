"""Power analysis for PREREG appendix B (EXP-08: H5, H6, H7), by Monte Carlo simulation.

Task W4-LDN-04. Draft prepared 06/11/2026, before the raw EXP-03 data are on main. The numbers it
prints with the default --cv grid are ILLUSTRATIVE ONLY. Run it again with the per-seed spread
measured on raw EXP-03 (see `--from-exp03`) before the thresholds are locked.

Decision rules simulated (notes/2026-11-06_dat_PREREG-phu-luc-B_nhap.md sec. 4, with the test
choices proposed in notes/2026-11-06_ldn_phuong-phap-H5-H7.md):

  H5  per suite s in {ood_energy_low, ood_combo}: d_i = (A_TSPa - A_M1,i) / A_TSPa, i = 1..n seeds.
      TSP-adaptive is deterministic on the fixed scenario set, so it is a constant. Exact one-sided
      sign-flip test on d (all 2^n sign vectors). Pass s if p_Holm < alpha AND mean(d) >= delta5.
      H5 holds if both suites pass.
  H6  r_i = A_M1,i / A_TSPa on id2. Non-inferiority: the upper end of the two-sided 95% percentile
      bootstrap CI of mean(r) (resampling seeds) must be < 1 + delta6.
  H7  per suite s in {ood_energy_low, ood_area_2000}: S = (A_Random - A)/(A_Random - A_TSPa), per seed,
      for M1 and M3 (independent seeds). One-sided two-sample permutation test on mean(S_M1) -
      mean(S_M3). Pass s if p_Holm < alpha AND the mean difference >= delta7. H7 holds if both pass.

Model of the data: per-seed means are normal around the true value with a standard deviation set
by the coefficient of variation (CV) of per-seed mean AoI. Suites are simulated independently.
This ignores scenario-level noise (the scenario set is fixed and shared, so the inference is
conditional on it) and between-suite correlation (which would make "both suites pass" more likely
than simulated, so the H5/H7 power here is a slight under-estimate).

Key property, independent of any data: a rule "significant AND point estimate >= delta" has about
50% power when the true effect equals delta, however many seeds are used. Power must therefore be
read at a true effect above delta (the "target effect"), and the report says which.

  python scripts/power_b.py                         # illustrative grid, n = 10
  python scripts/power_b.py --cv 0.08 --n 10 15 20  # after measuring CV on raw EXP-03
  python scripts/power_b.py --from-exp03 'results/raw/EXP-03/*/events.csv'
"""
from __future__ import annotations

import argparse
import csv
import glob
import itertools
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from uavaoi.stats import holm  # noqa: E402

ALPHA = 0.05


# ------------------------------------------------------------------------------------- tests
EXACT_MAX_N = 12


def signflip_matrix(n: int, n_random: int = 4096, seed: int = 0) -> np.ndarray:
    """All 2^n sign vectors for n <= 12 (exact test). For larger n, the identity plus n_random - 1
    random sign vectors (Monte Carlo test; the identity keeps p >= 1/n_random)."""
    if n <= EXACT_MAX_N:
        return np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    rnd = np.random.default_rng(seed).choice((-1.0, 1.0), (n_random - 1, n))
    return np.vstack([np.ones((1, n)), rnd])


def signflip_p(d: np.ndarray, signs: np.ndarray) -> np.ndarray:
    """Exact one-sided p of H0: E[d] <= 0 vs mean(d) > 0, for each row of d (shape (m, n))."""
    obs = d.mean(axis=1)                                  # (m,)
    null = d @ signs.T / d.shape[1]                       # (m, 2^n)
    return (null >= obs[:, None] - 1e-12).mean(axis=1)


def perm2_p(x: np.ndarray, y: np.ndarray, n_perm: int, rng) -> np.ndarray:
    """One-sided two-sample permutation p of mean(x) - mean(y) > 0, per row. x, y: (m, n)."""
    m, n = x.shape
    z = np.concatenate([x, y], axis=1)                    # (m, 2n)
    obs = x.mean(axis=1) - y.mean(axis=1)
    idx = np.argsort(rng.random((n_perm, 2 * n)), axis=1)  # same permutations for every row
    zp = z[:, idx]                                        # (m, n_perm, 2n)
    null = zp[:, :, :n].mean(axis=2) - zp[:, :, n:].mean(axis=2)
    return (1 + (null >= obs[:, None] - 1e-12).sum(axis=1)) / (n_perm + 1)


def holm2(p1: np.ndarray, p2: np.ndarray):
    a = np.array([holm([u, v]) for u, v in zip(p1, p2)])
    return a[:, 0], a[:, 1]


# --------------------------------------------------------------------------------- power runs
def power_h5(rho: float, cv: float, n: int, delta: float, sims: int, rng) -> float:
    """True relative reduction rho on both suites; per-seed CV of A_M1."""
    signs = signflip_matrix(n)
    sd = cv * (1 - rho)                                   # sd of d = sd(A_M1)/A_TSPa
    passes = []
    p = []
    for _ in range(2):
        d = rng.normal(rho, sd, (sims, n))
        p.append(signflip_p(d, signs))
        passes.append(d.mean(axis=1) >= delta)
    a1, a2 = holm2(*p)
    ok = (a1 < ALPHA) & passes[0] & (a2 < ALPHA) & passes[1]
    return float(ok.mean())


def power_h6(ratio: float, cv: float, n: int, delta: float, sims: int, rng, n_boot: int = 2000) -> float:
    """True ratio A_M1/A_TSPa on id2; pass if the 97.5% bootstrap quantile of mean(r) < 1 + delta."""
    r = rng.normal(ratio, cv * ratio, (sims, n))
    ub = np.empty(sims)
    for k in range(sims):
        b = rng.choice(r[k], (n_boot, n), replace=True).mean(axis=1)
        ub[k] = np.quantile(b, 0.975)
    return float((ub < 1 + delta).mean())


def power_h7(diff: float, sd_s: float, n: int, delta: float, sims: int, rng, n_perm: int = 2000) -> float:
    """True difference S_M1 - S_M3 = diff on both suites; per-seed SD of S = sd_s (both arms)."""
    passes, p = [], []
    for _ in range(2):
        x = rng.normal(diff, sd_s, (sims, n))
        y = rng.normal(0.0, sd_s, (sims, n))
        p.append(perm2_p(x, y, n_perm, rng))
        passes.append(x.mean(axis=1) - y.mean(axis=1) >= delta)
    a1, a2 = holm2(*p)
    return float(((a1 < ALPHA) & passes[0] & (a2 < ALPHA) & passes[1]).mean())


# ---------------------------------------------------------------------------- EXP-03 spread
def cv_from_exp03(pattern: str) -> dict:
    """Per (method, suite): CV of per-seed mean AoI over training seeds (completed runs only)."""
    import json
    acc = defaultdict(lambda: defaultdict(list))
    for p in sorted(glob.glob(pattern)):
        rec = os.path.join(os.path.dirname(p), "run_record.json")
        if not os.path.exists(rec) or json.load(open(rec)).get("status") != "completed":
            continue
        with open(p) as f:
            for row in csv.DictReader(f):
                if int(row["train_seed"]) >= 0:
                    acc[(row["method"], row["suite"])][row["train_seed"]].append(float(row["mean_aoi"]))
    out = {}
    for key, by_seed in acc.items():
        m = np.array([np.mean(v) for v in by_seed.values()])
        if len(m) >= 2:
            out[key] = (len(m), float(m.mean()), float(m.std(ddof=1) / m.mean()))
    return out


# ----------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[10], help="seeds per arm")
    ap.add_argument("--cv", type=float, nargs="+", default=[0.05, 0.10, 0.20],
                    help="coefficient of variation of per-seed mean AoI (illustrative default)")
    ap.add_argument("--delta", type=float, default=0.10, help="delta5 = delta6 = delta7 (draft)")
    ap.add_argument("--gap", type=float, default=1.0,
                    help="(A_Random - A_TSPa) / A_M1 for converting CV of A into SD of S (H7). Old suites with "
                         "TSP in place of TSPa and A_M1 = A_TSP give 1.2 (ood_energy) to 4.9 (ood_cluster); "
                         "the new low-battery suite may be smaller, so 1.0 is a cautious default")
    ap.add_argument("--sims", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--from-exp03", default=None, help="glob of EXP-03 events.csv to print measured CVs")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    d = args.delta
    lines = ["# Power for PREREG appendix B (simulation; scripts/power_b.py)\n",
             f"alpha = {ALPHA}, Holm over 2 suites for H5 and H7, delta = {d:.2f}, {args.sims} simulations, "
             f"RNG seed {args.seed}. Per-seed means ~ normal; see the docstring for the model and its limits.\n"]
    if args.from_exp03:
        cvs = cv_from_exp03(args.from_exp03)
        lines += ["## Measured spread on EXP-03 (per-seed mean AoI)\n",
                  "Seeds of the DR arm shared 7/8 scenario streams (DECISIONS 2026-11-06), so the DR CV is "
                  "likely an under-estimate. Use the larger of DR and Fixed, or inflate.\n",
                  "| Method | Suite | n seeds | mean A | CV |", "| --- | --- | --- | --- | --- |"]
        lines += [f"| {m} | {s} | {n} | {mu:.2f} | {cv:.3f} |" for (m, s), (n, mu, cv) in sorted(cvs.items())]
        lines.append("")
    effects = [d, 1.5 * d, 2 * d, 3 * d]
    lines += ["## H5: power vs true relative reduction (both suites must pass)\n",
              "| n | CV | " + " | ".join(f"rho = {e:.2f}" for e in effects) + " |",
              "| --- | --- | " + " | ".join("---" for _ in effects) + " |"]
    for n in args.n:
        for cv in args.cv:
            lines.append(f"| {n} | {cv:.2f} | " + " | ".join(
                f"{power_h5(e, cv, n, d, args.sims, rng):.2f}" for e in effects) + " |")
    ratios = [1 - d, 1 - d / 2, 1.0, 1 + d / 2]
    lines += ["\n## H6: power vs true ratio A_M1 / A_TSPa on id2 (non-inferiority margin 1 + delta)\n",
              "| n | CV | " + " | ".join(f"ratio = {r:.2f}" for r in ratios) + " |",
              "| --- | --- | " + " | ".join("---" for _ in ratios) + " |"]
    for n in args.n:
        for cv in args.cv:
            lines.append(f"| {n} | {cv:.2f} | " + " | ".join(
                f"{power_h6(r, cv, n, d, max(args.sims // 4, 200), rng):.2f}" for r in ratios) + " |")
    lines += [f"\n## H7: power vs true difference S_M1 - S_M3 (both suites must pass; SD of S = CV / gap, "
              f"gap = {args.gap})\n",
              "| n | CV | SD of S | " + " | ".join(f"diff = {e:.2f}" for e in effects) + " |",
              "| --- | --- | --- | " + " | ".join("---" for _ in effects) + " |"]
    for n in args.n:
        for cv in args.cv:
            sd_s = cv / args.gap
            lines.append(f"| {n} | {cv:.2f} | {sd_s:.2f} | " + " | ".join(
                f"{power_h7(e, sd_s, n, d, max(args.sims // 2, 200), rng):.2f}" for e in effects) + " |")
    lines.append("\nRead: the column where the true effect equals delta stays near or below 0.5 by construction "
                 "(the point estimate must also reach delta). Power is judged at the target effect the team "
                 "writes down before the lock.")
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
