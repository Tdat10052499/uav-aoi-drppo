"""Evaluate heuristics or a trained SB3 model on the ID/OOD suites.

Writes an append-only run directory  results/raw/<experiment-id>/<run-id>/  containing
  events.csv        one row per (method, train_seed, suite, episode_seed)
  run_record.json   Form E (notes/workbook_forms.md)
  config.json, environment.json

Examples
  python scripts/evaluate.py --experiment-id EXP-01 --method tsp greedy_aoi random --episodes 100
  python scripts/evaluate.py --experiment-id EXP-02 --model runs/dr_ppo_mask_lam0.1_s0/model.zip \
         --label dr_ppo --train-seed 0
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import numpy as np

from uavaoi import HEURISTICS, SUITES, EnvConfig, UAVAoIEnv, eval_seeds, run_episode
from uavaoi.runrecord import RunRecord, new_run_dir, sha256_file

FIELDS = ["method", "train_seed", "suite", "episode_seed", "mean_aoi", "peak_aoi", "energy_used_J",
          "energy_frac", "collections", "coverage", "hover_frac", "slow_frac", "fast_frac",
          "boundary_hits", "early_termination", "N", "L", "E_max", "return"]


class SB3Policy:
    """Wrap a trained (Maskable)PPO / DQN model; deterministic actions."""

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"model file not found: {path} (no silent fallback)")
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


def check_model_cfg(model_path: str, cfg: EnvConfig) -> tuple[list[str], list[str]]:
    """Compare the evaluation EnvConfig with the one the model was trained with.

    Returns (errors, warnings). `single_speed` changes the action mask, so a mismatch is an
    error: an A5 model evaluated without its config could pick V_mr, whose logits were never
    trained. Other differing fields are only warnings (they may be intentional).
    """
    errors, warnings = [], []
    train_cfg_path = os.path.join(os.path.dirname(os.path.abspath(model_path)), "config.json")
    if os.path.isfile(train_cfg_path):
        with open(train_cfg_path) as f:
            train_cfg = json.load(f).get("env_cfg", {})
        if bool(train_cfg.get("single_speed", False)) != cfg.single_speed:
            errors.append(f"single_speed: trained {train_cfg.get('single_speed', False)}, "
                          f"evaluating {cfg.single_speed} ({train_cfg_path}); pass the training --config")
        for k, v in cfg.to_dict().items():
            if k != "single_speed" and k in train_cfg and train_cfg[k] != v:
                warnings.append(f"env_cfg.{k}: trained {train_cfg[k]!r}, evaluating {v!r}")
    else:
        warnings.append(f"no training config.json next to {model_path}; env_cfg not checked")
        if "_1spd" in model_path.replace("\\", "/") and not cfg.single_speed:
            errors.append("model path contains '_1spd' but single_speed is False; "
                          "pass --config configs/a5_single_speed.json")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment-id", required=True, help="experiment card id, e.g. EXP-02")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--method", nargs="*", default=[], help=f"heuristics: {list(HEURISTICS)}")
    ap.add_argument("--model", default=None, help="path to SB3 model .zip")
    ap.add_argument("--label", default="model")
    ap.add_argument("--train-seed", type=int, default=-1)
    ap.add_argument("--suites", nargs="*", default=list(SUITES))
    ap.add_argument("--episodes", type=int, default=100)
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    args = ap.parse_args()

    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")
    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    policies = [(m, HEURISTICS[m]()) for m in args.method]
    cfg_warnings = []
    if args.model:
        cfg_errors, cfg_warnings = check_model_cfg(args.model, cfg)
        if cfg_errors:
            ap.error("; ".join(cfg_errors))
        for msg in cfg_warnings:
            print("WARNING:", msg, flush=True)
        policies.append((args.label, SB3Policy(args.model)))
    if not policies:
        ap.error("give --method and/or --model")

    seeds = eval_seeds(args.episodes)
    run_id, run_dir = new_run_dir(args.experiment_id, args.run_id)
    rr = RunRecord(args.experiment_id, run_dir, run_id,
                   config={"args": vars(args), "env_cfg": cfg.to_dict(),
                           "suites": {s: SUITES[s].to_dict() for s in args.suites}},
                   seeds={"eval_episode_seeds": [seeds[0], seeds[-1]], "train_seed": args.train_seed})
    rr.data["warnings"] += cfg_warnings
    if args.model:
        rr.data["checkpoint_digest"] = "sha256:" + sha256_file(args.model)
    events = os.path.join(run_dir, "events.csv")
    rr.data["raw_events_path"] = "events.csv"
    t0 = time.time()
    try:
        with open(events, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for suite_name in args.suites:
                env = UAVAoIEnv(scenario=SUITES[suite_name], cfg=cfg)
                for name, pol in policies:
                    vals = []
                    for s in seeds:
                        m = run_episode(env, pol, seed=s)
                        w.writerow({"method": name, "train_seed": args.train_seed, "suite": suite_name,
                                    "episode_seed": s, **{k: m[k] for k in FIELDS if k in m}})
                        vals.append(m["mean_aoi"])
                    key = f"{suite_name}/{name}"
                    rr.data["counts"][key] = len(vals)
                    rr.data["metrics"][key] = {"mean_aoi_mean": float(np.mean(vals))}
                    print(f"{suite_name:12s} {name:12s} mean AoI {np.mean(vals):7.2f} slots (n={len(vals)})",
                          flush=True)
        rr.data["metrics"]["wall_time_s"] = round(time.time() - t0, 1)
        rr.finish("completed")
    except Exception as e:  # record the failure, never hide it
        rr.finish("failed", failure_reason=repr(e))
        raise
    print(f"run {run_id} -> {run_dir}")


if __name__ == "__main__":
    main()
