"""Evaluate heuristics or a trained SB3 model on the ID/OOD suites.

Writes an append-only run directory  results/raw/<experiment-id>/<run-id>/  containing
  events.csv        one row per (method, train_seed, suite, episode_seed)
  run_record.json   Form E (notes/workbook_forms.md)
  config.json, environment.json

Examples
  python scripts/evaluate.py --experiment-id EXP-01 --method tsp greedy_aoi random --episodes 100
  python scripts/evaluate.py --experiment-id EXP-02 --model runs/dr_ppo_mask_lam0.1_s0/model.zip \
         --label dr_ppo --train-seed 0
  # EXP-08: strong tour heuristics and the high-level greedy ablation (old suites, test seeds)
  python scripts/evaluate.py --experiment-id EXP-08p --method tsp tsp_eco tsp_adaptive hl_greedy \
         --config configs/env_grounded.json
  # EXP-08 tour-guided model (Dict observation is detected from the checkpoint)
  python scripts/evaluate.py --experiment-id EXP-08p --model runs/EXP-08p/<run-id>/model.zip \
         --label m1 --train-seed 0 --config configs/env_grounded.json
  # reference heuristics on the Optuna validation seeds of tune_ppo.py (200000-200019), id only
  python scripts/evaluate.py --experiment-id TUNE --method random tsp --suites id --episodes 20 \
         --seed-base 200000
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

from uavaoi import HEURISTICS, SUITES, EnvConfig, UAVAoIEnv, run_episode
from uavaoi.options import OPTION_HEURISTICS, TourGuidedEnv, run_option_episode
from uavaoi.scenarios import EVAL_SEED_BASE, EVAL_SEED_BASE_B, SUITES_B

ALL_SUITES = {**SUITES, **SUITES_B}
LOCK_TAG = "prereg-B-lock"
PROTECTED = range(EVAL_SEED_BASE_B, EVAL_SEED_BASE_B + 100)   # EXP-08 confirmatory episode seeds
from uavaoi.runrecord import REPO_ROOT, RunRecord, new_run_dir, sha256_file

# "decisions" (number of high-level decisions) is filled only for option-level policies
# (TourGuidedEnv: hl_greedy and --policy options models); empty for flat policies.
FIELDS = ["method", "train_seed", "suite", "episode_seed", "mean_aoi", "peak_aoi", "energy_used_J",
          "energy_frac", "collections", "coverage", "hover_frac", "slow_frac", "fast_frac",
          "boundary_hits", "early_termination", "N", "L", "E_max", "return", "decisions"]


def lock_tag_exists() -> bool:
    import subprocess
    try:
        out = subprocess.run(["git", "tag", "-l", LOCK_TAG], cwd=REPO_ROOT, capture_output=True,
                             text=True, check=True).stdout
    except Exception:  # noqa: BLE001
        return False
    return out.strip() == LOCK_TAG


def check_confirmatory(seeds: list, suites: list, confirmatory: bool, tag_ok: bool,
                       probe_b: bool = False, has_model: bool = False) -> list:
    """Guards for the EXP-08 confirmatory evaluation (PREREG appendix B section 1):
    - episode seeds 300000-300099 need --confirmatory and the tag prereg-B-lock;
    - the EXP-08 suites (SUITES_B) on ANY seed need the tag, because running them reveals how
      hard the new distributions are. Before the lock, --probe-b allows heuristics only
      (e.g. the T = 300 feasibility check for L = 2000 m); it is recorded in the run record."""
    touches = any(s in PROTECTED for s in seeds)
    uses_b = [s for s in suites if s in SUITES_B]
    errs = []
    if uses_b and not tag_ok:
        if not probe_b:
            errs.append(f"suites {uses_b} are the EXP-08 suites; before the tag {LOCK_TAG} they can only be "
                        "probed with heuristics via --probe-b (recorded in run_record)")
        elif has_model:
            errs.append(f"--probe-b is for heuristics only; no learned policy on {uses_b} before {LOCK_TAG}")
    if touches and not confirmatory:
        errs.append(f"episode seeds overlap {PROTECTED.start}-{PROTECTED.stop - 1} (EXP-08 confirmatory set); "
                    "pass --confirmatory, only after the PREREG appendix B lock")
    if touches and confirmatory and not tag_ok:
        errs.append(f"--confirmatory needs the git tag {LOCK_TAG} (PREREG appendix B not locked yet)")
    if confirmatory and not touches:
        errs.append("--confirmatory given but the episode seeds are not the confirmatory set")
    return errs


def _patch_torch_load_buffered() -> None:
    """Make torch.load read zip-member streams into memory first.

    SB3 passes a ZipExtFile (stream inside model.zip) to torch.load. With torch 2.14.1+cpu on
    Windows this fails with "PytorchStreamReader failed reading file .data/serialization_id"
    although the checkpoint is intact (SHA256 matches run_record; see notes 2026-11-03).
    Reading the member into a BytesIO first gives the same tensors and avoids the bug.
    """
    import io
    import torch

    if getattr(torch.load, "_uavaoi_buffered", False):
        return
    _orig = torch.load

    def _load(f, *args, **kwargs):
        if hasattr(f, "read") and not isinstance(f, io.BytesIO):
            f = io.BytesIO(f.read())
        return _orig(f, *args, **kwargs)

    _load._uavaoi_buffered = True
    torch.load = _load


class SB3Policy:
    """Wrap a trained (Maskable)PPO / DQN model; deterministic actions."""

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"model file not found: {path} (no silent fallback)")
        self.masked = False
        _patch_torch_load_buffered()
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

        from gymnasium import spaces as _sp
        self.options = isinstance(self.model.observation_space, _sp.Dict)
        self.K = int(self.model.observation_space["cand"].shape[0] // 4) if self.options else None

    def reset(self, env):
        pass

    def act(self, env) -> int:
        obs = env._obs()   # UAVAoIEnv (flat) or TourGuidedEnv (options): both expose _obs/action_masks
        if self.masked:
            a, _ = self.model.predict(obs, deterministic=True, action_masks=env.action_masks())
        else:
            a, _ = self.model.predict(obs, deterministic=True)
        return int(a)


def check_model_cfg(model_path: str, cfg: EnvConfig, raw_base: str | None = None) -> tuple[list[str], list[str]]:
    """Compare the evaluation EnvConfig with the one the model was trained with.

    train_ppo.py / tune_ppo.py save the model at runs/<exp>/<run_id>/model.zip and the training
    config at results/raw/<exp>/<run_id>/config.json, so both places are tried.
    Returns (errors, warnings). `single_speed` changes the action mask, so a mismatch is an
    error: an A5 model evaluated without its config could pick V_mr, whose logits were never
    trained. Other differing fields are only warnings (they may be intentional).
    """
    errors, warnings = [], []
    model_dir = os.path.dirname(os.path.abspath(model_path))
    run_id, exp = os.path.basename(model_dir), os.path.basename(os.path.dirname(model_dir))
    raw_base = raw_base or os.path.join(REPO_ROOT, "results", "raw")
    candidates = [os.path.join(model_dir, "config.json"), os.path.join(raw_base, exp, run_id, "config.json")]
    train_cfg_path = next((c for c in candidates if os.path.isfile(c)), None)
    if train_cfg_path:
        with open(train_cfg_path) as f:
            train_cfg = json.load(f).get("env_cfg", {})
        if bool(train_cfg.get("single_speed", False)) != cfg.single_speed:
            errors.append(f"single_speed: trained {train_cfg.get('single_speed', False)}, "
                          f"evaluating {cfg.single_speed} ({train_cfg_path}); pass the training --config")
        if train_cfg.get("obs_mode", "legacy") != cfg.obs_mode:
            errors.append(f"obs_mode: trained {train_cfg.get('obs_mode', 'legacy')!r}, evaluating "
                          f"{cfg.obs_mode!r} ({train_cfg_path}); pass the training --config")
        for k, v in cfg.to_dict().items():
            if k not in ("single_speed", "obs_mode") and k in train_cfg and train_cfg[k] != v:
                warnings.append(f"env_cfg.{k}: trained {train_cfg[k]!r}, evaluating {v!r}")
    else:
        warnings.append(f"no training config.json found for {model_path} (tried {candidates}); env_cfg not checked")
        if "_1spd" in model_path.replace("\\", "/") and not cfg.single_speed:
            errors.append("model path contains '_1spd' but single_speed is False; "
                          "pass --config configs/a5_single_speed.json")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment-id", required=True, help="experiment card id, e.g. EXP-02")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--method", nargs="*", default=[],
                    help=f"heuristics: {list(HEURISTICS)} + option-level {list(OPTION_HEURISTICS)}")
    ap.add_argument("--model", default=None, help="path to SB3 model .zip")
    ap.add_argument("--label", default="model")
    ap.add_argument("--train-seed", type=int, default=-1)
    ap.add_argument("--suites", nargs="*", default=list(SUITES), choices=list(ALL_SUITES),
                    help=f"default: the EXP-01..03 suites; EXP-08 suites: {list(SUITES_B)}")
    ap.add_argument("--confirmatory", action="store_true",
                    help=f"allow episode seeds {PROTECTED.start}-{PROTECTED.stop - 1}; needs tag {LOCK_TAG}")
    ap.add_argument("--probe-b", action="store_true",
                    help="before the lock: allow heuristics (no --model) on the EXP-08 suites, off the "
                         "confirmatory seeds; written to run_record warnings")
    ap.add_argument("--K", type=int, default=5, help="candidates for option-level heuristics")
    ap.add_argument("--episodes", type=int, default=100)
    ap.add_argument("--seed-base", type=int, default=EVAL_SEED_BASE,
                    help="first episode seed; default = test seeds. 200000 = validation seeds of tune_ppo.py")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    args = ap.parse_args()

    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")
    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    bad = [m for m in args.method if m not in HEURISTICS and m not in OPTION_HEURISTICS]
    if bad:
        ap.error(f"unknown --method {bad}")
    # (name, policy, kind): kind "flat" runs on UAVAoIEnv, "options" on TourGuidedEnv
    policies = [(m, HEURISTICS[m](), "flat") if m in HEURISTICS else (m, OPTION_HEURISTICS[m](), "options")
                for m in args.method]
    cfg_warnings = []
    if args.model:
        cfg_errors, cfg_warnings = check_model_cfg(args.model, cfg)
        if cfg_errors:
            ap.error("; ".join(cfg_errors))
        for msg in cfg_warnings:
            print("WARNING:", msg, flush=True)
        pol = SB3Policy(args.model)
        policies.append((args.label, pol, "options" if pol.options else "flat"))
        if pol.options and pol.K != args.K:
            print(f"NOTE: model has K = {pol.K}; option heuristics also use K = {pol.K}", flush=True)
            args.K = pol.K
    if not policies:
        ap.error("give --method and/or --model")

    seeds = [args.seed_base + i for i in range(args.episodes)]
    needs_tag = args.confirmatory or any(s in SUITES_B for s in args.suites)
    conf_errors = check_confirmatory(seeds, args.suites, args.confirmatory,
                                     lock_tag_exists() if needs_tag else False,
                                     probe_b=args.probe_b, has_model=bool(args.model))
    if conf_errors:
        ap.error("; ".join(conf_errors))
    if args.seed_base != EVAL_SEED_BASE:
        print(f"NOTE: episode seeds {seeds[0]}-{seeds[-1]}, not the test seeds", flush=True)
    run_id, run_dir = new_run_dir(args.experiment_id, args.run_id)
    rr = RunRecord(args.experiment_id, run_dir, run_id,
                   config={"args": vars(args), "env_cfg": cfg.to_dict(),
                           "suites": {s: ALL_SUITES[s].to_dict() for s in args.suites}},
                   seeds={"eval_episode_seeds": [seeds[0], seeds[-1]], "train_seed": args.train_seed})
    rr.data["warnings"] += cfg_warnings
    if args.probe_b and any(s in SUITES_B for s in args.suites):
        rr.data["warnings"].append(f"--probe-b: heuristics run on EXP-08 suites before {LOCK_TAG} "
                                   f"(seeds {seeds[0]}-{seeds[-1]}); declare in PREREG appendix B section 1")
    if any(s in SUITES_B for s in args.suites):
        rr.data["data_manifest_path"] = "data/eval_manifest_B.json" if all(s in SUITES_B for s in args.suites) \
            else "data/eval_manifest.json + data/eval_manifest_B.json"
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
                env = UAVAoIEnv(scenario=ALL_SUITES[suite_name], cfg=cfg)
                wenv = TourGuidedEnv(scenario=ALL_SUITES[suite_name], cfg=cfg, K=args.K)
                for name, pol, kind in policies:
                    vals = []
                    for s in seeds:
                        m = (run_option_episode(wenv, pol, seed=s) if kind == "options"
                             else run_episode(env, pol, seed=s))
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
