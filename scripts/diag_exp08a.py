"""EXP-08a (exploratory, descriptive only): why does PPO lose on ood_energy / ood_area in EXP-03?

  python scripts/diag_exp08a.py results/raw/EXP-03/eval_*/events.csv \\
      results/raw/EXP-03/heuristics_lock/events.csv --out results/processed/EXP-08a_diag.md

Card: notes/EXP-08_PG-TG-PPO_card.md, section "EXP-08a". Reads only existing raw files; no
environment rollouts, no policy loading. Only CSVs whose run_record.json says
status = completed are used (PREREG sec. 9).

Stop slot t_end. events.csv has no column for it, but env.py counts one action per executed slot
(action_counts: hover, V_me, V_mr), so t_end = hover + slow + fast counts. The fractions alone fix
t_end only up to a common factor, so each candidate d <= T is also checked against the energy
balance of env.py:
    energy_used = c * E_hover_tx + (n_hover - c) * P_hover * dt + n_slow * E(V_me) + n_fast * E(V_mr)
with c = collections. An episode with zero or several consistent candidates is reported as
unresolved and left out of the t_end column (the count is printed).

Aggregation: learned arms (DR, Fixed) -> mean over episodes per training seed, then mean over
seeds, with the min-max range of the seed means; heuristics -> mean over the 100 episodes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import numpy as np

from uavaoi.env import UAVAoIEnv
from uavaoi.scenarios import SUITES

ARM = {"dr_ppo": "DR", "fixed_ppo": "Fixed", "tsp": "TSP", "greedy_aoi": "Greedy", "random": "Random"}
ARMS = ["DR", "Fixed", "TSP", "Greedy", "Random"]
SUITE_ORDER = ["id", "ood_cluster", "ood_density", "ood_area", "ood_energy"]
KEYS = ["early", "t_end", "hover", "slow", "fast", "coverage", "collections", "A"]


def slot_energies():
    """Per-slot energies of env.py; they depend on the rotor preset and dt, not on the suite."""
    env = UAVAoIEnv(SUITES["id"])
    env.reset(seed=100000)
    return {"tx": float(env.E_hover_tx), "hover": float(env.P_hover * env.cfg.dt),
            "slow": float(env.E_move[0]), "fast": float(env.E_move[8]), "T": int(env.cfg.T)}


def t_end(row, E, rtol=1e-3):
    h, s, f = (float(row[k]) for k in ("hover_frac", "slow_frac", "fast_frac"))
    c, used = int(row["collections"]), float(row["energy_used_J"])
    found = []
    for d in range(1, E["T"] + 1):
        n = [round(x * d) for x in (h, s, f)]
        if sum(n) != d or n[0] < c or any(abs(x * d - y) > 1e-6 for x, y in zip((h, s, f), n)):
            continue
        model = c * E["tx"] + (n[0] - c) * E["hover"] + n[1] * E["slow"] + n[2] * E["fast"]
        if abs(model - used) <= rtol * max(used, 1.0):
            found.append(d)
    return found[0] if len(found) == 1 else None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    E = slot_energies()
    per_seed = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    used_files, n_ep, unresolved = [], 0, 0
    for p in sorted(args.csv):
        rr = os.path.join(os.path.dirname(p), "run_record.json")
        with open(rr) as fh:
            if json.load(fh).get("status") != "completed":
                print(f"skip (not completed): {p}", file=sys.stderr)
                continue
        used_files.append(p)
        with open(p, newline="") as fh:
            for r in csv.DictReader(fh):
                if r["method"] not in ARM:
                    continue
                n_ep += 1
                te = t_end(r, E)
                unresolved += te is None
                m = {"early": float(r["early_termination"] == "True"), "t_end": te,
                     "hover": float(r["hover_frac"]), "slow": float(r["slow_frac"]),
                     "fast": float(r["fast_frac"]), "coverage": float(r["coverage"]),
                     "collections": float(r["collections"]), "A": float(r["mean_aoi"])}
                for k, v in m.items():
                    if v is not None:
                        per_seed[(ARM[r["method"]], r["suite"])][r["train_seed"]][k].append(v)

    def agg(arm, suite, k, early_only=False):
        seeds = per_seed[(arm, suite)]
        if early_only:
            v = [t for sd in seeds.values() for t, e in zip(sd["t_end"], sd["early"]) if e]
            return (float(np.mean(v)), None, None, len(v)) if v else (float("nan"), None, None, 0)
        if arm in ("DR", "Fixed"):
            v = np.array([np.mean(sd[k]) for sd in seeds.values()])
            return float(v.mean()), float(v.min()), float(v.max()), len(v)
        v = np.array(seeds["-1"][k])
        return float(v.mean()), None, None, len(v)

    try:
        rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:  # noqa: BLE001 - provenance line only
        rev = "unknown"
    L = ["# EXP-08a: chẩn đoán từ raw EXP-03 (thăm dò, chỉ mô tả)\n",
         f"Sinh bởi `scripts/diag_exp08a.py` tại commit `{rev}`. {n_ep} episode; "
         f"t_end không suy ra được (0 hoặc nhiều nghiệm): {unresolved}.",
         f"Năng lượng mỗi khe (env.py): truyền {E['tx']:.1f} J, treo không truyền {E['hover']:.1f} J, "
         f"V_me {E['slow']:.1f} J, V_mr {E['fast']:.1f} J; T = {E['T']}.",
         "DR, Fixed: trung bình của 10 trung bình theo seed, [min–max] các trung bình seed. "
         "Heuristic: trung bình 100 episode.\n",
         "| Bộ | Nhánh | n | early_termination | t_end (khe) | hover | slow (V_me) | fast (V_mr) | coverage | collections | Ā |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for s in SUITE_ORDER:
        for a in ARMS:
            if (a, s) not in per_seed:
                continue
            cells, nn = [], 0
            for k in KEYS:
                mu, lo, hi, nn = agg(a, s, k)
                fmt = "{:.0f}" if k == "t_end" else ("{:.1f}" if k in ("collections", "A") else "{:.2f}")
                rng = f" [{fmt.format(lo)}–{fmt.format(hi)}]" if lo is not None and k in ("early", "t_end", "fast", "coverage") else ""
                cells.append(fmt.format(mu) + rng)
            L.append(f"| {s} | {a} | {nn} | " + " | ".join(cells) + " |")
    L += ["\n## t_end chỉ trên các episode kết thúc sớm (gộp mọi seed)\n",
          "| Bộ | " + " | ".join(ARMS) + " |", "| --- |" + " --- |" * len(ARMS)]
    for s in SUITE_ORDER:
        row = []
        for a in ARMS:
            mu, _, _, nn = agg(a, s, "t_end", early_only=True)
            row.append(f"{mu:.0f} (n = {nn})" if nn else "–")
        L.append(f"| {s} | " + " | ".join(row) + " |")
    L += ["\n## Tệp đầu vào (SHA256)\n"] + [f"- `{p}` `{sha256(p)[:16]}`" for p in used_files]
    text = "\n".join(L) + "\n"
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)


if __name__ == "__main__":
    main()
