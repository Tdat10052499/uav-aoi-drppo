"""Compare two evaluation event files row by row (second reader / G2 reproduction).

  python scripts/compare_events.py results/raw/EXP-03/<original-run>/events.csv \
         results/raw/EXP-03/<rerun>/events.csv --out notes/review_rows.md

Rows are matched on (method, train_seed, suite, episode_seed). Numeric fields must agree
within --atol + --rtol * |reference| (defaults 1e-9 and 0, as in the EXP-01 check); other
fields must be equal. Reports rows missing on either side and every mismatch, and exits 1
if anything differs. Used by W7-FAO-02, W8-FAO-01 and W9-FAO-01 (docs/05 G2 criterion 2).
--methods restricts the comparison to some labels (e.g. the re-evaluated models only).
"""
from __future__ import annotations

import argparse
import csv
import math
import sys

KEY = ("method", "train_seed", "suite", "episode_seed")


def load(path, methods=None):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if methods:
        rows = [r for r in rows if r["method"] in methods]
    out = {}
    for r in rows:
        k = tuple(r[c] for c in KEY)
        if k in out:
            raise ValueError(f"{path}: duplicate row for {dict(zip(KEY, k))}")
        out[k] = r
    return out


def same(a: str, b: str, atol: float, rtol: float) -> bool:
    try:
        x, y = float(a), float(b)
    except ValueError:
        return a == b
    if math.isnan(x) or math.isnan(y):
        return math.isnan(x) and math.isnan(y)
    return abs(x - y) <= atol + rtol * abs(x)


def compare(ref, new, atol, rtol):
    missing = sorted(set(ref) - set(new))
    extra = sorted(set(new) - set(ref))
    diffs = []
    for k in sorted(set(ref) & set(new)):
        for col in ref[k]:
            if col in KEY:
                continue
            if col not in new[k]:
                diffs.append((k, col, ref[k][col], "<missing column>"))
            elif not same(ref[k][col], new[k][col], atol, rtol):
                diffs.append((k, col, ref[k][col], new[k][col]))
    return missing, extra, diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference", help="original events.csv (never modified)")
    ap.add_argument("rerun", help="events.csv from the re-run")
    ap.add_argument("--methods", nargs="*", default=None, help="only compare these method labels")
    ap.add_argument("--atol", type=float, default=1e-9)
    ap.add_argument("--rtol", type=float, default=0.0)
    ap.add_argument("--max-show", type=int, default=20, help="mismatches listed in the report")
    ap.add_argument("--out", default=None, help="write the report as Markdown")
    args = ap.parse_args()

    ref, new = load(args.reference, args.methods), load(args.rerun, args.methods)
    missing, extra, diffs = compare(ref, new, args.atol, args.rtol)
    bad_rows = len({d[0] for d in diffs})
    lines = ["# events.csv comparison\n",
             f"- reference: `{args.reference}` ({len(ref)} rows)",
             f"- re-run: `{args.rerun}` ({len(new)} rows)",
             f"- methods: {', '.join(args.methods) if args.methods else 'all'}; "
             f"tolerance: atol {args.atol:g}, rtol {args.rtol:g}",
             f"- rows compared: {len(set(ref) & set(new))}; rows with a mismatch: {bad_rows}; "
             f"missing in re-run: {len(missing)}; only in re-run: {len(extra)}"]
    if diffs:
        lines += ["", "| method | train_seed | suite | episode_seed | field | reference | re-run |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {' | '.join(k)} | {c} | {a} | {b} |" for k, c, a, b in diffs[:args.max_show]]
        if len(diffs) > args.max_show:
            lines.append(f"\n... {len(diffs) - args.max_show} more mismatching fields not shown")
    for name, ks in (("Missing in re-run", missing), ("Only in re-run", extra)):
        if ks:
            lines += ["", f"{name} (first {min(len(ks), args.max_show)}):"]
            lines += [f"- {dict(zip(KEY, k))}" for k in ks[:args.max_show]]
    ok = not (missing or extra or diffs)
    lines += ["", "RESULT: " + ("MATCH" if ok else "DIFFERENT")]
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
