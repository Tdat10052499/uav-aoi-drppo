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
  # EXP-08 (PG-TG-PPO): tour-guided semi-MDP + grounded observation; --timesteps counts DECISIONS
  python scripts/train_ppo.py --experiment-id EXP-08p --policy options --masked --train dr --seed 0 \
         --config configs/env_grounded.json --timesteps <decisions>
  # EXP-08 arm M4: grounded observation, flat 17 actions
  python scripts/train_ppo.py --experiment-id EXP-08p --masked --train dr --seed 0 \
         --config configs/env_grounded.json --timesteps 2000000
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
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor

from uavaoi import TRAIN_DR, TRAIN_FIXED, EnvConfig, UAVAoIEnv
from uavaoi.options import TourGuidedEnv
from uavaoi.nets import MapCandExtractor, SmallCNN  # noqa: F401  (re-exported for tune_ppo.py)
from uavaoi.runrecord import REPO_ROOT, RunRecord, new_run_dir, sha256_file


def make_env(train: str, cfg: EnvConfig, seed: int, rank: int, masked: bool,
             policy: str = "flat", K: int = 5):
    def _thunk():
        scenario = TRAIN_DR if train == "dr" else TRAIN_FIXED
        if policy == "options":
            env = TourGuidedEnv(scenario=scenario, cfg=cfg, K=K)
        else:
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
    ap.add_argument("--policy", choices=["flat", "options"], default="flat",
                    help="flat = 17 primitive actions (EXP-01..03, arm M4); options = tour-guided "
                         "semi-MDP of src/uavaoi/options.py (arms M1-M3; --timesteps counts decisions)")
    ap.add_argument("--K", type=int, default=5, help="candidates per decision (--policy options)")
    ap.add_argument("--reset-seed-scheme", choices=["spaced", "sb3"], default="spaced",
                    help="spaced: env rank r resets with seed*1000 + r (independent scenario streams per "
                         "training seed). sb3: seed + r, what SB3 does when the model gets seed=seed; "
                         "this is what EXP-01..03 actually used (adjacent training seeds share 7 of 8 "
                         "scenario streams). Found 06/11/2026, see notes/EXP-08_PG-TG-PPO_card.md")
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
    if args.policy == "options" and not (args.algo == "ppo" and args.masked):
        ap.error("--policy options needs --algo ppo --masked (candidate slots can be empty)")
    from uavaoi.scenarios import reserved_overlap, train_reset_seeds
    n_envs_planned = 1 if args.algo == "dqn" else args.n_envs
    planned = train_reset_seeds(args.seed, n_envs_planned, args.reset_seed_scheme)
    hit = reserved_overlap(planned)
    if hit:
        ap.error(f"training seed {args.seed} resets envs with seeds {planned[0]}-{planned[-1]}, which are "
                 f"evaluation scenarios ({'; '.join(hit)}); pick another seed (PREREG section 9 "
                 "replacement seed + 100 must also avoid this)")
    over = json.load(open(args.config)) if args.config else {}
    if args.lam is not None:
        over["lam"] = args.lam
    cfg = EnvConfig(**over)
    tag = (f"{args.train}_{args.algo}{'_mask' if args.masked else ''}"
           f"{'_opt' if args.policy == 'options' else ''}{'_grd' if cfg.obs_mode == 'grounded' else ''}"
           f"{'_1spd' if cfg.single_speed else ''}_lam{cfg.lam}_s{args.seed}")
    run_id, raw_dir = new_run_dir(args.experiment_id, f"{tag}_{__import__('time').strftime('%Y%m%d-%H%M%S')}")
    run_dir = os.path.join(args.models_dir, args.experiment_id, run_id)
    os.makedirs(run_dir, exist_ok=True)
    rr = RunRecord(args.experiment_id, raw_dir, run_id,
                   config={"args": vars(args), "env_cfg": cfg.to_dict(),
                           "scenario": (TRAIN_DR if args.train == "dr" else TRAIN_FIXED).to_dict()},
                   seeds={"train_seed": args.seed,
                          "env_reset_seeds": ("seed*1000 + rank" if args.reset_seed_scheme == "spaced"
                                              else "seed + rank (SB3 VecEnv.seed)") + ", rank < n_envs",
                          "reset_seed_scheme": args.reset_seed_scheme})

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    masked = args.masked and args.algo == "ppo"
    n_envs = 1 if args.algo == "dqn" else args.n_envs
    fns = [make_env(args.train, cfg, args.seed, i, masked, args.policy, args.K) for i in range(n_envs)]
    venv = SubprocVecEnv(fns) if (args.subproc and n_envs > 1) else DummyVecEnv(fns)
    venv = VecMonitor(venv)

    policy_kwargs = dict(features_extractor_class=MapCandExtractor if args.policy == "options" else SmallCNN,
                         features_extractor_kwargs=dict(features_dim=256),
                         normalize_images=False)
    policy_name = "MultiInputPolicy" if args.policy == "options" else "CnnPolicy"
    if args.algo == "ppo":
        if masked:
            from sb3_contrib import MaskablePPO as Algo
        else:
            from stable_baselines3 import PPO as Algo
        # Starting hyper-parameters (tune with an equal Optuna budget for every learner).
        model = Algo(policy_name, venv, n_steps=1024, batch_size=256, n_epochs=10,
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

    # SB3 calls venv.seed(seed) inside the model constructor, which makes the next reset use
    # seed + rank and overrides the reset in make_env. Re-seed explicitly so the record is true.
    if args.reset_seed_scheme == "spaced":
        venv.seed(args.seed * 1000)
    rr.data["seeds"]["env_reset_seed_list"] = [int(x) for x in venv.venv._seeds] if hasattr(venv.venv, "_seeds") else None
    if rr.data["seeds"]["env_reset_seed_list"] != planned:   # never train on an unchecked seed list
        rr.finish("failed", failure_reason=f"env reset seeds {rr.data['seeds']['env_reset_seed_list']} != planned {planned}")
        raise RuntimeError("env reset seeds differ from the checked plan")

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
    rr.data["counts"] = {"timesteps": args.timesteps, "n_envs": n_envs,
                         "timestep_unit": "decision" if args.policy == "options" else "slot"}
    if args.policy == "options":
        rr.data["counts"]["base_env_slots"] = int(sum(venv.get_attr("total_slots")))
    rr.data["model_path"] = os.path.relpath(model_path, REPO_ROOT)
    rr.finish("completed")
    print("saved", model_path)
    print("run record", os.path.join(raw_dir, "run_record.json"))


if __name__ == "__main__":
    main()
