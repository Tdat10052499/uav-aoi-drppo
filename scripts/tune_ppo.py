"""Optuna hyper-parameter search for (Maskable)PPO, with an equal budget per learner.

Protocol (docs/03 section 3):
  * DR-PPO and Fixed-PPO get the same number of trials, the same steps per trial and the
    same sampler seed, so neither learner is tuned harder than the other.
  * The objective is the mean AoI on the `id` suite only, never on an OOD suite.
  * Validation episodes use seeds VAL_SEED_BASE + i, disjoint from the test seeds
    100000-100099 (scenarios.eval_seeds), so the reported ID numbers are not tuned on.
  * Trials use a training seed outside 0-9 (the seeds of the main results).
  * No pruning: every trial trains for exactly --timesteps steps.

Writes (results/raw is append-only):
  results/raw/<experiment-id>/<study-id>/            run_record.json of the study,
                                                     trials.csv, best_params.json
  results/raw/<experiment-id>/<study-id>_t<NNN>/     run_record.json of each trial
  runs/<experiment-id>/<study-id>_t<NNN>/model.zip   checkpoint (gitignored; SHA256 in record)

Examples
  python scripts/tune_ppo.py --experiment-id TUNE --train dr --n-trials 20 --masked
  python scripts/tune_ppo.py --experiment-id TUNE --train fixed --n-trials 20 --masked
  # quick check of the script itself (results/raw/SMOKE is gitignored)
  python scripts/tune_ppo.py --experiment-id SMOKE --train dr --n-trials 2 --timesteps 2048 \
         --n-envs 2 --val-episodes 2 --masked
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import optuna
import torch
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor

from uavaoi import SUITES, TRAIN_DR, TRAIN_FIXED, EnvConfig, UAVAoIEnv, run_episode
from uavaoi.runrecord import REPO_ROOT, RunRecord, new_run_dir, sha256_file
from evaluate import SB3Policy
from train_ppo import SmallCNN, make_env

VAL_SEED_BASE = 200_000
TRIAL_FIELDS = ["trial", "state", "val_mean_aoi", "val_mean_energy_frac", "learning_rate", "n_steps",
                "batch_size", "ent_coef", "gamma", "clip_range", "wall_time_s", "run_id"]


def val_seeds(n: int) -> list:
    return [VAL_SEED_BASE + i for i in range(n)]


def sample_params(trial: optuna.Trial, n_envs: int) -> dict:
    """Search space of W2-DAT-02. batch_size must divide the rollout size n_steps * n_envs."""
    n_steps = trial.suggest_categorical("n_steps", [256, 512, 1024, 2048])
    batch_size = trial.suggest_categorical("batch_size", [64, 128, 256, 512])
    if (n_steps * n_envs) % batch_size:
        raise optuna.TrialPruned(f"batch_size {batch_size} does not divide {n_steps} x {n_envs}")
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-3, log=True),
        "n_steps": n_steps,
        "batch_size": batch_size,
        "ent_coef": trial.suggest_float("ent_coef", 1e-4, 5e-2, log=True),
        "gamma": trial.suggest_categorical("gamma", [0.95, 0.98, 0.99, 0.995]),
        "clip_range": trial.suggest_categorical("clip_range", [0.1, 0.2, 0.3]),
    }


def build_model(params: dict, venv, masked: bool, seed: int, tb_dir: str):
    if masked:
        from sb3_contrib import MaskablePPO as Algo
    else:
        from stable_baselines3 import PPO as Algo
    policy_kwargs = dict(features_extractor_class=SmallCNN,
                         features_extractor_kwargs=dict(features_dim=256),
                         normalize_images=False)
    try:
        import tensorboard  # noqa: F401  (optional dependency, environment/requirements.txt)
    except ImportError:
        tb_dir = None
    # n_epochs and gae_lambda stay at the train_ppo.py values; they are not searched.
    return Algo("CnnPolicy", venv, n_epochs=10, gae_lambda=0.95, policy_kwargs=policy_kwargs,
                seed=seed, verbose=0, tensorboard_log=tb_dir, **params)


def validate(model_path: str, cfg: EnvConfig, n_episodes: int) -> dict:
    """Deterministic rollouts on the `id` suite with validation seeds (not the test seeds)."""
    env = UAVAoIEnv(scenario=SUITES["id"], cfg=cfg)
    pol = SB3Policy(model_path)
    ms = [run_episode(env, pol, seed=s) for s in val_seeds(n_episodes)]
    return {"val_mean_aoi": float(np.mean([m["mean_aoi"] for m in ms])),
            "val_mean_energy_frac": float(np.mean([m["energy_frac"] for m in ms])),
            "n_episodes": len(ms)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment-id", required=True, help="experiment card id, e.g. TUNE")
    ap.add_argument("--train", choices=["dr", "fixed"], required=True)
    ap.add_argument("--n-trials", type=int, default=20)
    ap.add_argument("--timesteps", type=int, default=200_000, help="training steps per trial")
    ap.add_argument("--n-envs", type=int, default=8)
    ap.add_argument("--masked", action="store_true", help="MaskablePPO (as in EXP-02)")
    ap.add_argument("--seed", type=int, default=1000,
                    help="training seed of every trial (keep outside 0-9, the main-result seeds)")
    ap.add_argument("--sampler-seed", type=int, default=0,
                    help="TPE sampler seed; use the same value for dr and fixed")
    ap.add_argument("--val-episodes", type=int, default=20)
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--models-dir", default=os.path.join(REPO_ROOT, "runs"))
    ap.add_argument("--subproc", action="store_true")
    args = ap.parse_args()

    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")
    if 0 <= args.seed <= 9:
        ap.error("--seed 0-9 is reserved for the main results; tune with another seed")
    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    scenario = TRAIN_DR if args.train == "dr" else TRAIN_FIXED

    study_id, study_dir = new_run_dir(
        args.experiment_id, f"tune_{args.train}{'_mask' if args.masked else ''}_{time.strftime('%Y%m%d-%H%M%S')}")
    study_rr = RunRecord(args.experiment_id, study_dir, study_id,
                         config={"args": vars(args), "env_cfg": cfg.to_dict(), "scenario": scenario.to_dict(),
                                 "objective": "minimise mean AoI on suite 'id', validation seeds",
                                 "val_seed_range": [VAL_SEED_BASE, VAL_SEED_BASE + args.val_episodes - 1]},
                         seeds={"train_seed": args.seed, "sampler_seed": args.sampler_seed})
    trials_csv = os.path.join(study_dir, "trials.csv")
    with open(trials_csv, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=TRIAL_FIELDS).writeheader()

    def log_trial(row: dict):
        with open(trials_csv, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=TRIAL_FIELDS).writerow({k: row.get(k) for k in TRIAL_FIELDS})

    def objective(trial: optuna.Trial) -> float:
        try:
            params = sample_params(trial, args.n_envs)
        except optuna.TrialPruned:
            log_trial({"trial": trial.number, "state": "invalid_params", **trial.params})
            raise
        run_id, raw_dir = new_run_dir(args.experiment_id, f"{study_id}_t{trial.number:03d}")
        model_dir = os.path.join(args.models_dir, args.experiment_id, run_id)
        os.makedirs(model_dir, exist_ok=True)
        rr = RunRecord(args.experiment_id, raw_dir, run_id,
                       config={"study_id": study_id, "trial": trial.number, "params": params,
                               "args": vars(args), "env_cfg": cfg.to_dict(), "scenario": scenario.to_dict()},
                       seeds={"train_seed": args.seed, "env_reset_seeds": "seed*1000 + rank, rank < n_envs"})
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)
        fns = [make_env(args.train, cfg, args.seed, i, args.masked) for i in range(args.n_envs)]
        venv = VecMonitor(SubprocVecEnv(fns) if (args.subproc and args.n_envs > 1) else DummyVecEnv(fns))
        t0 = time.time()
        try:
            model = build_model(params, venv, args.masked, args.seed, os.path.join(model_dir, "tb"))
            model.learn(total_timesteps=args.timesteps, progress_bar=False)
            model_path = os.path.join(model_dir, "model.zip")
            model.save(model_path)
            wall = time.time() - t0
            val = validate(model_path, cfg, args.val_episodes)
        except Exception as e:  # record failures, never hide them
            rr.finish("failed", failure_reason=repr(e))
            log_trial({"trial": trial.number, "state": "failed", "run_id": run_id, **params})
            raise
        finally:
            venv.close()
        rr.data["checkpoint_digest"] = "sha256:" + sha256_file(model_path)
        rr.data["model_path"] = os.path.relpath(model_path, REPO_ROOT)
        rr.data["metrics"] = {**val, "wall_time_s": round(wall, 1),
                              "steps_per_s": round(args.timesteps / max(wall, 1e-9), 1)}
        rr.data["counts"] = {"timesteps": args.timesteps, "n_envs": args.n_envs}
        rr.finish("completed")
        log_trial({"trial": trial.number, "state": "completed", "run_id": run_id,
                   "wall_time_s": round(wall, 1), **val, **params})
        print(f"trial {trial.number:3d}  val mean AoI {val['val_mean_aoi']:7.2f}  {params}", flush=True)
        return val["val_mean_aoi"]

    study = optuna.create_study(direction="minimize", study_name=study_id,
                                sampler=optuna.samplers.TPESampler(seed=args.sampler_seed))
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    try:
        # Invalid (batch, n_steps) pairs are pruned before training and do not use budget,
        # so stop on the number of *completed* trials.
        while sum(t.state == optuna.trial.TrialState.COMPLETE for t in study.trials) < args.n_trials:
            study.optimize(objective, n_trials=1, catch=(Exception,))
            if sum(t.state == optuna.trial.TrialState.FAIL for t in study.trials) > args.n_trials:
                raise RuntimeError("more failed trials than --n-trials; see trials.csv")
    except Exception as e:
        study_rr.finish("failed", failure_reason=repr(e))
        raise

    states = [t.state.name for t in study.trials]
    best = {"trial": study.best_trial.number, "val_mean_aoi": study.best_value,
            "params": study.best_params, "run_id": f"{study_id}_t{study.best_trial.number:03d}"}
    with open(os.path.join(study_dir, "best_params.json"), "w") as f:
        json.dump(best, f, indent=2)
    study_rr.data["metrics"] = {"best": best}
    study_rr.data["counts"] = {s: states.count(s) for s in sorted(set(states))}
    study_rr.finish("completed")
    print("best", json.dumps(best))
    print("study record", os.path.join(study_dir, "run_record.json"))


if __name__ == "__main__":
    main()
