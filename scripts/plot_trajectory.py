"""Plot the trajectory of one episode (figure F6 and the degenerate-behaviour check).

docs/05 G1 #5: FAO looks at >= 3 trajectories per model before its numbers are trusted.
The map shows the area, the sensors (filled = served at least once, number = times
served, dashed circle = collection radius), the UAV path coloured by speed (V_me slow,
V_mr fast), hover slots (collect or idle), start and end. Episode metrics go in the
title; degenerate-behaviour flags (one action class >= 90 %, boundary hits with the
action mask on) are printed and drawn in red. The file type follows --out (.png, .pdf
or .svg). Requires matplotlib.

Examples
  python scripts/plot_trajectory.py --method tsp --suite ood_cluster --seed 100000
  python scripts/plot_trajectory.py --model runs/EXP-02/<run-id>/model.zip --label dr_ppo \
         --suite ood_cluster --seed 100000
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import numpy as np

from uavaoi import HEURISTICS, SUITES, EnvConfig, UAVAoIEnv
from uavaoi.runrecord import REPO_ROOT

SLOW, FAST, COLLECT, IDLE = "#2b6cb0", "#dd6b20", "#2f855a", "#a0aec0"


def rollout(env: UAVAoIEnv, policy, seed: int) -> dict:
    """Run one episode, recording position and action class per slot."""
    env.reset(seed=seed)
    policy.reset(env)
    path = [env.pos.copy()]
    kinds = []
    done = False
    while not done:
        a = policy.act(env)
        before = int(env.n_served.sum())
        _, _, term, trunc, info = env.step(a)
        path.append(env.pos.copy())
        if a == 0:
            kinds.append("collect" if env.n_served.sum() > before else "idle")
        else:
            kinds.append("slow" if a <= 8 else "fast")
        done = term or trunc
    return {"path": np.array(path), "kinds": kinds, "metrics": info["episode_metrics"]}


def degeneracy_flags(m: dict, masked: bool) -> list:
    flags = [f"{k} = {m[k]:.2f} >= 0.90" for k in ("hover_frac", "slow_frac", "fast_frac") if m[k] >= 0.9]
    if masked and m["boundary_hits"] > 0:
        flags.append(f"boundary_hits = {m['boundary_hits']} with action mask on")
    return flags


def plot(env: UAVAoIEnv, ep: dict, title: str, flags: list, out: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    m, p = ep["metrics"], ep["path"]
    fig, ax = plt.subplots(figsize=(6.4, 7.2))
    ax.add_patch(plt.Rectangle((0, 0), env.L, env.L, facecolor="#f7fafc", edgecolor="#4a5568"))
    for w in env.sensors:
        ax.add_patch(plt.Circle(w, env.r_eff, fill=False, ls="--", lw=0.6, ec="#cbd5e0", clip_on=True))
    for t, k in enumerate(ep["kinds"]):
        if k in ("slow", "fast"):
            ax.plot(p[t:t + 2, 0], p[t:t + 2, 1], color=SLOW if k == "slow" else FAST, lw=1.6, alpha=0.8)
    for k, col in (("collect", COLLECT), ("idle", IDLE)):
        idx = [t for t, kk in enumerate(ep["kinds"]) if kk == k]
        if idx:
            ax.scatter(p[idx, 0], p[idx, 1], s=18, color=col, zorder=3)
    served = env.n_served
    ax.scatter(env.sensors[:, 0], env.sensors[:, 1], s=36, marker="s", zorder=4, edgecolors="#1a202c",
               facecolors=np.where(served[:, None] > 0, [[0.1, 0.13, 0.17]], [[1, 1, 1]]))
    for w, c in zip(env.sensors, served):
        ax.annotate(str(int(c)), w, xytext=(4, 4), textcoords="offset points", fontsize=7)
    ax.scatter(*p[0], s=90, facecolors="none", edgecolors="black", lw=1.8, zorder=5)
    ax.scatter(*p[-1], s=80, marker="x", color="#c53030", lw=2.2, zorder=5)
    ax.set_xlim(-0.02 * env.L, 1.02 * env.L)
    ax.set_ylim(-0.02 * env.L, 1.02 * env.L)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    sub = (f"mean AoI {m['mean_aoi']:.2f} slots · peak {m['peak_aoi']:.0f} · coverage {m['coverage']:.2f} · "
           f"collections {m['collections']}\nhover/slow/fast {m['hover_frac']:.2f}/{m['slow_frac']:.2f}/"
           f"{m['fast_frac']:.2f} · energy {m['energy_frac']:.2f} E_max · boundary hits {m['boundary_hits']}\n"
           f"battery empty before T: {m['early_termination']}")
    ax.set_title(f"{title}\n{sub}", fontsize=8.5, loc="left")
    if flags:
        ax.text(0.01, 0.99, "DEGENERATE? " + "; ".join(flags), transform=ax.transAxes, va="top",
                fontsize=8, color="#c53030")
    legend = [Line2D([], [], color=SLOW, lw=2, label=f"fly V_me ({env.V_slow:.1f} m/s)"),
              Line2D([], [], color=FAST, lw=2, label=f"fly V_mr ({env.V_fast:.1f} m/s)"),
              Line2D([], [], color=COLLECT, marker="o", ls="", label="hover + collect"),
              Line2D([], [], color=IDLE, marker="o", ls="", label="hover, nothing in range"),
              Line2D([], [], color="#1a202c", marker="s", ls="", label="sensor (n = times served)"),
              Line2D([], [], color="black", marker="o", mfc="none", ls="", label="start"),
              Line2D([], [], color="#c53030", marker="x", ls="", label="end")]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=7.5, frameon=False)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", choices=list(HEURISTICS), help="heuristic policy")
    ap.add_argument("--model", default=None, help="path to SB3 model .zip")
    ap.add_argument("--label", default=None, help="name used in the title and file name")
    ap.add_argument("--suite", choices=list(SUITES), default="id")
    ap.add_argument("--seed", type=int, default=100_000, help="episode seed (eval seeds: 100000-100099)")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--out", default=None,
                    help="output .png/.pdf/.svg (default figures/traj_<label>_<suite>_<seed>.png)")
    args = ap.parse_args()
    if bool(args.method) == bool(args.model):
        ap.error("give exactly one of --method or --model")
    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")

    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    if args.model:
        from evaluate import SB3Policy  # scripts/ is on sys.path when run as a script
        policy, label = SB3Policy(args.model), args.label or "model"
    else:
        policy, label = HEURISTICS[args.method](), args.label or args.method
    env = UAVAoIEnv(scenario=SUITES[args.suite], cfg=cfg)
    ep = rollout(env, policy, args.seed)
    # heuristics always respect the mask; DQN / plain PPO models do not see it
    flags = degeneracy_flags(ep["metrics"], masked=getattr(policy, "masked", True))

    out = args.out or os.path.join(REPO_ROOT, "figures", f"traj_{label}_{args.suite}_{args.seed}.png")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    plot(env, ep, f"{label} · {args.suite} · seed {args.seed} · N={env.N}, L={env.L:.0f} m", flags, out)
    m = ep["metrics"]
    print(f"{label} {args.suite} seed {args.seed}: mean AoI {m['mean_aoi']:.2f}, coverage {m['coverage']:.2f}, "
          f"hover/slow/fast {m['hover_frac']:.2f}/{m['slow_frac']:.2f}/{m['fast_frac']:.2f}, "
          f"boundary hits {m['boundary_hits']}, early end {m['early_termination']}")
    print("degenerate: " + ("; ".join(flags) if flags else "no flags"))
    print("saved", out)


if __name__ == "__main__":
    main()
