"""Train PPO (or MaskablePPO / DQN) on the UAV-AoI environment.

Requires: torch, gymnasium, stable-baselines3 (and sb3-contrib for --masked).
NOT executed in the workspace where this starter kit was built (no PyPI access);
run it on the team's machine; compute plan in docs/03 section 8.

Examples
  # proposed method: domain-randomised training
  python scripts/train_ppo.py --experiment-id EXP-02 --train dr --seed 0 --timesteps 2000000 --masked
  # key baseline: one fixed layout
  python scripts/train_ppo.py --experiment-id EXP-02 --train fixed --seed 0 --timesteps 2000000 --masked
  # algorithm baseline
  python scripts/train_ppo.py --experiment-id EXP-04 --algo dqn --train dr --seed 0 --timesteps 2000000
  # DQN pipeline check (small buffer, updates start early)
  python scripts/train_ppo.py --experiment-id EXP-04 --algo dqn --train dr --seed 0 --timesteps 10000 \
         --dqn-buffer-size 20000 --dqn-learning-starts 1000
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import numpy as np
import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor

from uavaoi import TRAIN_DR, TRAIN_FIXED, EnvConfig, UAVAoIEnv
from uavaoi.runrecord import REPO_ROOT, RunRecord, new_run_dir, sha256_file


class SmallCNN(BaseFeaturesExtractor):
    """Feature extractor for the 5 x 31 x 31 centred map (NatureCNN needs >= 36 x 36)."""

    def __init__(self, observation_space, features_dim: int = 256):
        super().__init__(observation_space, features_dim)
        c = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(c, 32, 3, stride=1, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=2, padding=1), nn.ReLU(),
            nn.Flatten(),
        )
        with torch.no_grad():
            n = self.cnn(torch.zeros(1, *observation_space.shape)).shape[1]
        self.head = nn.Sequential(nn.Linear(n, features_dim), nn.ReLU())

    def forward(self, x):
        return self.head(self.cnn(x))


def make_env(train: str, cfg: EnvConfig, seed: int, rank: int, masked: bool):
    def _thunk():
        scenario = TRAIN_DR if train == "dr" else TRAIN_FIXED
        env = UAVAoIEnv(scenario=scenario, cfg=cfg)
        if masked:
            from sb3_contrib.common.wrappers import ActionMasker
            env = ActionMasker(env, lambda e: e.action_masks())
        env.reset(seed=seed * 1000 + rank)
        return env
    return _thunk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment-id", required=True, help="experiment card id, e.g. EXP-02")
    ap.add_argument("--algo", choices=["ppo", "dqn"], default="ppo")
    ap.add_argument("--train", choices=["dr", "fixed"], default="dr")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--timesteps", type=int, default=2_000_000)
    ap.add_argument("--n-envs", type=int, default=8)
    ap.add_argument("--masked", action="store_true", help="MaskablePPO (ppo only)")
    ap.add_argument("--lam", type=float, default=None, help="override energy weight")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--models-dir", default=os.path.join(REPO_ROOT, "runs"),
                    help="where model files go (gitignored; record SHA256 in data/checkpoint_manifest.md)")
    ap.add_argument("--subproc", action="store_true")
    ap.add_argument("--dqn-buffer-size", type=int, default=200_000,
                    help="DQN replay buffer (transitions); memory ~ 2 x size x obs bytes")
    ap.add_argument("--dqn-learning-starts", type=int, default=20_000,
                    help="DQN steps before the first gradient update")
    args = ap.parse_args()

    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")
    if args.algo == "dqn" and args.dqn_learning_starts >= args.timesteps:
        ap.error(f"--dqn-learning-starts ({args.dqn_learning_starts}) >= --timesteps ({args.timesteps}): "
                 "DQN would never update; lower --dqn-learning-starts")
    over = json.load(open(args.config)) if args.config else {}
    if args.lam is not None:
        over["lam"] = args.lam
    cfg = EnvConfig(**over)
    tag = f"{args.train}_{args.algo}{'_mask' if args.masked else ''}_lam{cfg.lam}_s{args.seed}"
    run_id, raw_dir = new_run_dir(args.experiment_id, f"{tag}_{__import__('time').strftime('%Y%m%d-%H%M%S')}")
    run_dir = os.path.join(args.models_dir, args.experiment_id, run_id)
    os.makedirs(run_dir, exist_ok=True)
    rr = RunRecord(args.experiment_id, raw_dir, run_id,
                   config={"args": vars(args), "env_cfg": cfg.to_dict(),
                           "scenario": (TRAIN_DR if args.train == "dr" else TRAIN_FIXED).to_dict()},
                   seeds={"train_seed": args.seed, "env_reset_seeds": f"seed*1000 + rank, rank < n_envs"})

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    masked = args.masked and args.algo == "ppo"
    n_envs = 1 if args.algo == "dqn" else args.n_envs
    fns = [make_env(args.train, cfg, args.seed, i, masked) for i in range(n_envs)]
    venv = SubprocVecEnv(fns) if (args.subproc and n_envs > 1) else DummyVecEnv(fns)
    venv = VecMonitor(venv)

    policy_kwargs = dict(features_extractor_class=SmallCNN,
                         features_extractor_kwargs=dict(features_dim=256),
                         normalize_images=False)
    if args.algo == "ppo":
        if masked:
            from sb3_contrib import MaskablePPO as Algo
        else:
            from stable_baselines3 import PPO as Algo
        # Starting hyper-parameters (tune with an equal Optuna budget for every learner).
        model = Algo("CnnPolicy", venv, n_steps=1024, batch_size=256, n_epochs=10,
                     gamma=0.99, gae_lambda=0.95, clip_range=0.2, ent_coef=0.01,
                     learning_rate=3e-4, policy_kwargs=policy_kwargs, seed=args.seed,
                     verbose=1, tensorboard_log=os.path.join(run_dir, "tb"))
    else:
        from stable_baselines3 import DQN
        # obs and next_obs are both stored, as float32
        buf_gb = 2 * args.dqn_buffer_size * int(np.prod(venv.observation_space.shape)) * 4 / 1e9
        print(f"DQN replay buffer: {args.dqn_buffer_size} transitions ~ {buf_gb:.1f} GB RAM")
        model = DQN("CnnPolicy", venv, buffer_size=args.dqn_buffer_size,
                    learning_starts=args.dqn_learning_starts,
                    batch_size=128, gamma=0.99, train_freq=4, target_update_interval=10_000,
                    exploration_fraction=0.2, exploration_final_eps=0.02, learning_rate=1e-4,
                    policy_kwargs=policy_kwargs, seed=args.seed, verbose=1,
                    tensorboard_log=os.path.join(run_dir, "tb"))

    import time as _t
    t0 = _t.time()
    try:
        model.learn(total_timesteps=args.timesteps, progress_bar=False)
    except Exception as e:  # record failures, never hide them
        rr.finish("failed", failure_reason=repr(e))
        raise
    model_path = os.path.join(run_dir, "model.zip")
    model.save(model_path)
    rr.data["checkpoint_digest"] = "sha256:" + sha256_file(model_path)
    rr.data["metrics"] = {"wall_time_s": round(_t.time() - t0, 1),
                          "steps_per_s": round(args.timesteps / max(_t.time() - t0, 1e-9), 1)}
    rr.data["counts"] = {"timesteps": args.timesteps, "n_envs": n_envs}
    rr.data["model_path"] = os.path.relpath(model_path, REPO_ROOT)
    rr.finish("completed")
    print("saved", model_path)
    print("run record", os.path.join(raw_dir, "run_record.json"))


if __name__ == "__main__":
    main()
