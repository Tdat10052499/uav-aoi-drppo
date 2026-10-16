"""Train PPO (or MaskablePPO / DQN) on the UAV-AoI environment.

Requires: torch, gymnasium, stable-baselines3 (and sb3-contrib for --masked).
NOT executed in the workspace where this starter kit was built (no PyPI access);
run it on the team's machine and check `docs/03` section 7 for the compute plan.

Examples
  # proposed method: domain-randomised training
  python scripts/train_ppo.py --train dr --seed 0 --timesteps 2000000 --masked
  # key baseline: one fixed layout
  python scripts/train_ppo.py --train fixed --seed 0 --timesteps 2000000 --masked
  # algorithm baseline
  python scripts/train_ppo.py --algo dqn --train dr --seed 0 --timesteps 2000000
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor

from uavaoi import TRAIN_DR, TRAIN_FIXED, EnvConfig, UAVAoIEnv


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
    ap.add_argument("--algo", choices=["ppo", "dqn"], default="ppo")
    ap.add_argument("--train", choices=["dr", "fixed"], default="dr")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--timesteps", type=int, default=2_000_000)
    ap.add_argument("--n-envs", type=int, default=8)
    ap.add_argument("--masked", action="store_true", help="MaskablePPO (ppo only)")
    ap.add_argument("--lam", type=float, default=None, help="override energy weight")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--out", default="runs")
    ap.add_argument("--subproc", action="store_true")
    args = ap.parse_args()

    over = json.load(open(args.config)) if args.config else {}
    if args.lam is not None:
        over["lam"] = args.lam
    cfg = EnvConfig(**over)
    tag = f"{args.train}_{args.algo}{'_mask' if args.masked else ''}_lam{cfg.lam}_s{args.seed}"
    run_dir = os.path.join(args.out, tag)
    os.makedirs(run_dir, exist_ok=True)

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
        model = DQN("CnnPolicy", venv, buffer_size=200_000, learning_starts=20_000,
                    batch_size=128, gamma=0.99, train_freq=4, target_update_interval=10_000,
                    exploration_fraction=0.2, exploration_final_eps=0.02, learning_rate=1e-4,
                    policy_kwargs=policy_kwargs, seed=args.seed, verbose=1,
                    tensorboard_log=os.path.join(run_dir, "tb"))

    with open(os.path.join(run_dir, "run_config.json"), "w") as f:
        json.dump({"args": vars(args), "env_cfg": cfg.to_dict(),
                   "scenario": (TRAIN_DR if args.train == "dr" else TRAIN_FIXED).to_dict()},
                  f, indent=2, default=str)
    model.learn(total_timesteps=args.timesteps, progress_bar=False)
    model.save(os.path.join(run_dir, "model"))
    print("saved", os.path.join(run_dir, "model.zip"))


if __name__ == "__main__":
    main()
