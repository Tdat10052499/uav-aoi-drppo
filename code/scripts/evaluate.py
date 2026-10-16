"""Evaluate heuristics or trained SB3 models on the ID/OOD suites.

Examples
  python scripts/evaluate.py --method tsp greedy_aoi random --episodes 100 --out results/heuristics.csv
  python scripts/evaluate.py --model runs/dr_ppo_s0/model.zip --label dr_ppo --train-seed 0 \
         --out results/dr_ppo_s0.csv

Output: one CSV row per (method, train_seed, suite, episode_seed).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from uavaoi import HEURISTICS, SUITES, EnvConfig, UAVAoIEnv, eval_seeds, run_episode

FIELDS = ["method", "train_seed", "suite", "episode_seed", "mean_aoi", "peak_aoi", "energy_used_J",
          "energy_frac", "collections", "coverage", "hover_frac", "slow_frac", "fast_frac",
          "boundary_hits", "early_termination", "N", "L", "E_max", "return"]


class SB3Policy:
    """Wrap a trained (Maskable)PPO / DQN model; deterministic actions."""

    def __init__(self, path: str):
        self.masked = False
        try:
            from sb3_contrib import MaskablePPO
            self.model = MaskablePPO.load(path, device="cpu")
            self.masked = True
        except Exception:  # noqa: BLE001
            from stable_baselines3 import PPO, DQN
            try:
                self.model = PPO.load(path, device="cpu")
            except Exception:  # noqa: BLE001
                self.model = DQN.load(path, device="cpu")

    def reset(self, env):
        pass

    def act(self, env) -> int:
        obs = env._obs()
        if self.masked:
            a, _ = self.model.predict(obs, deterministic=True, action_masks=env.action_masks())
        else:
            a, _ = self.model.predict(obs, deterministic=True)
        return int(a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", nargs="*", default=[], help=f"heuristics: {list(HEURISTICS)}")
    ap.add_argument("--model", default=None, help="path to SB3 model .zip")
    ap.add_argument("--label", default="model")
    ap.add_argument("--train-seed", type=int, default=-1)
    ap.add_argument("--suites", nargs="*", default=list(SUITES))
    ap.add_argument("--episodes", type=int, default=100)
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    policies = [(m, HEURISTICS[m]()) for m in args.method]
    if args.model:
        policies.append((args.label, SB3Policy(args.model)))
    if not policies:
        ap.error("give --method and/or --model")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    seeds = eval_seeds(args.episodes)
    t0 = time.time()
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for suite_name in args.suites:
            env = UAVAoIEnv(scenario=SUITES[suite_name], cfg=cfg)
            for name, pol in policies:
                vals = []
                for s in seeds:
                    m = run_episode(env, pol, seed=s)
                    row = {"method": name, "train_seed": args.train_seed, "suite": suite_name,
                           "episode_seed": s, **{k: m[k] for k in FIELDS if k in m}}
                    w.writerow(row)
                    vals.append(m["mean_aoi"])
                print(f"{suite_name:12s} {name:12s} mean AoI {np.mean(vals):7.2f} slots "
                      f"(n={len(vals)})", flush=True)
    print(f"done in {time.time() - t0:.1f}s -> {args.out}")


if __name__ == "__main__":
    main()
