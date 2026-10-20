"""Plot the trajectory of one episode as an SVG map (no plotting library needed).

Used for figure F6 and for the weekly degenerate-behaviour check (docs/05 G1 #5):
every model gets >= 3 trajectories looked at before its numbers are trusted.

The map shows the area, sensors (filled = served at least once, number = times served),
the UAV path coloured by speed (V_me slow / V_mr fast), hover slots (collect or idle),
start and end. The title line repeats the episode metrics; degenerate-behaviour flags
(one action class >= 90 %, boundary hits with masking on) are printed and drawn.

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
    """Run one episode, recording position, action class and served sensor per slot."""
    env.reset(seed=seed)
    policy.reset(env)
    path = [env.pos.copy()]
    kinds, served_at = [], []
    done = False
    while not done:
        a = policy.act(env)
        before = env.n_served.copy()
        _, _, term, trunc, info = env.step(a)
        hit = np.flatnonzero(env.n_served > before)
        path.append(env.pos.copy())
        if a == 0:
            kinds.append("collect" if hit.size else "idle")
        else:
            kinds.append("slow" if a <= 8 else "fast")
        served_at.append(int(hit[0]) if hit.size else -1)
        done = term or trunc
    return {"path": np.array(path), "kinds": kinds, "served_at": served_at,
            "metrics": info["episode_metrics"]}


def degeneracy_flags(m: dict, masked: bool) -> list:
    flags = []
    for k in ("hover_frac", "slow_frac", "fast_frac"):
        if m[k] >= 0.9:
            flags.append(f"{k} = {m[k]:.2f} >= 0.90")
    if masked and m["boundary_hits"] > 0:
        flags.append(f"boundary_hits = {m['boundary_hits']} with action mask on")
    return flags


def to_svg(env: UAVAoIEnv, ep: dict, title: str, flags: list, size: int = 640) -> str:
    pad, top = 40, 90
    s = size / env.L                                   # metres -> pixels
    X = lambda x: pad + x * s                          # noqa: E731
    Y = lambda y: top + (env.L - y) * s                # noqa: E731  (y axis up)
    W, H = size + 2 * pad, size + top + pad + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'font-family="Helvetica, Arial, sans-serif" font-size="12">',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<text x="{pad}" y="22" font-size="14" font-weight="bold">{title}</text>']
    m = ep["metrics"]
    out.append(f'<text x="{pad}" y="40">mean AoI {m["mean_aoi"]:.2f} slots · peak {m["peak_aoi"]:.0f} · '
               f'coverage {m["coverage"]:.2f} · collections {m["collections"]} · '
               f'boundary hits {m["boundary_hits"]}</text>')
    out.append(f'<text x="{pad}" y="56">hover/slow/fast {m["hover_frac"]:.2f}/{m["slow_frac"]:.2f}/'
               f'{m["fast_frac"]:.2f} · energy used {m["energy_frac"]:.2f} E_max · '
               f'battery empty before T: {m["early_termination"]}</text>')
    if flags:
        out.append(f'<text x="{pad}" y="72" fill="#c53030">DEGENERATE? {"; ".join(flags)}</text>')
    out.append(f'<clipPath id="area"><rect x="{X(0)}" y="{Y(env.L)}" width="{size}" height="{size}"/></clipPath>')
    out.append(f'<rect x="{X(0)}" y="{Y(env.L)}" width="{size}" height="{size}" fill="#f7fafc" '
               f'stroke="#4a5568"/>')
    # collection radius around each sensor (clipped to the area), then the path, then sensors
    out.append('<g clip-path="url(#area)">')
    for w in env.sensors:
        out.append(f'<circle cx="{X(w[0]):.1f}" cy="{Y(w[1]):.1f}" r="{env.r_eff * s:.1f}" '
                   f'fill="none" stroke="#e2e8f0" stroke-dasharray="3,3"/>')
    out.append('</g>')
    p = ep["path"]
    for t, k in enumerate(ep["kinds"]):
        if k in ("slow", "fast"):
            out.append(f'<line x1="{X(p[t, 0]):.1f}" y1="{Y(p[t, 1]):.1f}" x2="{X(p[t + 1, 0]):.1f}" '
                       f'y2="{Y(p[t + 1, 1]):.1f}" stroke="{SLOW if k == "slow" else FAST}" '
                       f'stroke-width="2" stroke-opacity="0.8"/>')
    for t, k in enumerate(ep["kinds"]):
        if k in ("collect", "idle"):
            out.append(f'<circle cx="{X(p[t, 0]):.1f}" cy="{Y(p[t, 1]):.1f}" r="3.5" '
                       f'fill="{COLLECT if k == "collect" else IDLE}"/>')
    for n, w in enumerate(env.sensors):
        cnt = int(env.n_served[n])
        out.append(f'<rect x="{X(w[0]) - 4:.1f}" y="{Y(w[1]) - 4:.1f}" width="8" height="8" '
                   f'fill="{"#1a202c" if cnt else "white"}" stroke="#1a202c"/>')
        out.append(f'<text x="{X(w[0]) + 6:.1f}" y="{Y(w[1]) - 6:.1f}" font-size="10">{cnt}</text>')
    out.append(f'<circle cx="{X(p[0, 0]):.1f}" cy="{Y(p[0, 1]):.1f}" r="7" fill="none" stroke="#000" '
               f'stroke-width="2"/>')
    out.append(f'<path d="M{X(p[-1, 0]) - 6:.1f},{Y(p[-1, 1]) - 6:.1f} l12,12 m0,-12 l-12,12" '
               f'stroke="#c53030" stroke-width="2.5"/>')
    # legend
    ly = top + size + 22
    items = [("line", SLOW, f"fly V_me ({env.V_slow:.1f} m/s)"), ("line", FAST, f"fly V_mr ({env.V_fast:.1f} m/s)"),
             ("dot", COLLECT, "hover + collect"), ("dot", IDLE, "hover, nothing in range"),
             ("sq", "#1a202c", "sensor (n = times served)"), ("ring", "#000", "start"), ("x", "#c53030", "end")]
    x = pad
    for i, (kind, col, label) in enumerate(items):
        if i == 4:                                     # second legend row
            x, ly = pad, ly + 20
        if kind == "line":
            out.append(f'<line x1="{x}" y1="{ly - 4}" x2="{x + 16}" y2="{ly - 4}" stroke="{col}" stroke-width="3"/>')
        elif kind == "dot":
            out.append(f'<circle cx="{x + 8}" cy="{ly - 4}" r="4" fill="{col}"/>')
        elif kind == "sq":
            out.append(f'<rect x="{x + 4}" y="{ly - 8}" width="8" height="8" fill="{col}"/>')
        elif kind == "ring":
            out.append(f'<circle cx="{x + 8}" cy="{ly - 4}" r="5" fill="none" stroke="{col}" stroke-width="2"/>')
        else:
            out.append(f'<path d="M{x + 3},{ly - 9} l10,10 m0,-10 l-10,10" stroke="{col}" stroke-width="2"/>')
        out.append(f'<text x="{x + 20}" y="{ly}">{label}</text>')
        x += 24 + 6.2 * len(label)
    out.append("</svg>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", choices=list(HEURISTICS), help="heuristic policy")
    ap.add_argument("--model", default=None, help="path to SB3 model .zip")
    ap.add_argument("--label", default=None, help="name used in the title and file name")
    ap.add_argument("--suite", choices=list(SUITES), default="id")
    ap.add_argument("--seed", type=int, default=100_000, help="episode seed (eval seeds: 100000-100099)")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides")
    ap.add_argument("--out", default=None, help="output .svg (default figures/traj_<label>_<suite>_<seed>.svg)")
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
    flags = degeneracy_flags(ep["metrics"], masked=cfg.use_action_mask_clip)

    out = args.out or os.path.join(REPO_ROOT, "figures", f"traj_{label}_{args.suite}_{args.seed}.svg")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    title = f"{label} · {args.suite} · seed {args.seed} · N={env.N}, L={env.L:.0f} m"
    with open(out, "w", encoding="utf-8") as f:
        f.write(to_svg(env, ep, title, flags))
    m = ep["metrics"]
    print(f"{label} {args.suite} seed {args.seed}: mean AoI {m['mean_aoi']:.2f}, coverage {m['coverage']:.2f}, "
          f"hover/slow/fast {m['hover_frac']:.2f}/{m['slow_frac']:.2f}/{m['fast_frac']:.2f}, "
          f"boundary hits {m['boundary_hits']}, early end {m['early_termination']}")
    print("degenerate: " + ("; ".join(flags) if flags else "no flags"))
    print("saved", out)


if __name__ == "__main__":
    main()
