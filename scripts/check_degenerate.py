"""Flag degenerate policies from evaluation events (G1 criterion 5, W3-FAO-01).

  python scripts/check_degenerate.py results/raw/EXP-02/*/events.csv --masked dr_ppo fixed_ppo \
         --out results/processed/EXP-02_degenerate.md

Per (method, train_seed), over all evaluation episodes in the given CSVs:
  - action-type shares (hover / slow / fast): a type whose mean share is >= --threshold
    (default 0.9) is flagged, which also covers "hovers forever";
  - boundary hits: must be 0 for methods listed in --masked (FAIL), reported otherwise;
  - episodes with zero coverage (no sensor ever served) and early-termination rate (info).
Heuristics (train_seed = -1) are listed like any method. Exit code 1 if any FAIL.
The trajectory plots (scripts/plot_trajectory.py, >= 3 per model) are still required;
this table does not replace looking at them.
"""
from __future__ import annotations

import argparse
import csv
import glob
import sys
from collections import defaultdict

import numpy as np

TYPES = ["hover_frac", "slow_frac", "fast_frac"]


def load(patterns):
    rows = []
    for pat in patterns:
        for p in sorted(glob.glob(pat)) or [pat]:
            with open(p, newline="") as f:
                rows += list(csv.DictReader(f))
    return rows


def check(rows, masked, threshold):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["method"], int(r["train_seed"]))].append(r)
    out = []
    for (method, seed), rs in sorted(groups.items()):
        shares = {t: float(np.mean([float(r[t]) for r in rs])) for t in TYPES}
        top = max(shares, key=shares.get)
        hits = int(sum(int(r["boundary_hits"]) for r in rs))
        zero_cov = int(sum(float(r["coverage"]) == 0.0 for r in rs))
        early = float(np.mean([r["early_termination"] == "True" for r in rs]))
        flags = []
        if shares[top] >= threshold:
            flags.append(f"FAIL {top.split('_')[0]} share {shares[top]:.2f} >= {threshold}")
        if hits and method in masked:
            flags.append(f"FAIL {hits} boundary hits with action mask")
        out.append(dict(method=method, seed=seed, n=len(rs), **shares, hits=hits,
                        zero_cov=zero_cov, early=early, flags=flags))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+", help="events.csv files (globs allowed)")
    ap.add_argument("--masked", nargs="*", default=[],
                    help="method labels trained/evaluated with an action mask (boundary hits must be 0)")
    ap.add_argument("--threshold", type=float, default=0.9)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    res = check(load(args.csv), set(args.masked), args.threshold)
    lines = ["# Degeneracy check (G1 criterion 5)\n",
             f"Threshold for one action type: {args.threshold}. Masked methods: "
             f"{', '.join(args.masked) or 'none'}.\n",
             "| Method | Train seed | Episodes | Hover | Slow | Fast | Boundary hits | "
             "Episodes with 0 coverage | Early termination | Flags |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in res:
        lines.append(f"| {r['method']} | {r['seed']} | {r['n']} | {r['hover_frac']:.2f} | "
                     f"{r['slow_frac']:.2f} | {r['fast_frac']:.2f} | {r['hits']} | {r['zero_cov']} | "
                     f"{r['early']:.2f} | {'; '.join(r['flags']) or 'OK'} |")
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    sys.exit(1 if any(r["flags"] for r in res) else 0)


if __name__ == "__main__":
    main()
