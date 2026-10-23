"""Figure F6: TSP vs a learned policy on the same OOD-cluster scenario (docs/06 sec. 1, W6-FAO-02).

Scenario choice is fixed before any model is evaluated, never picked for a nice picture:
the default is the first evaluation seed of the suite (100000). Other seeds may be drawn as
extra panels for the thesis, but the paper figure uses the default unless DECISIONS.md says
otherwise. Writes the figure (.pdf/.png/.svg from --out) and an alt-text file next to it
(<out>.alt.txt), which EAI/Springer require for every figure (docs/06 sec. 1).

  python scripts/plot_f6.py --model runs/EXP-03/<run-id>/model.zip --label "DR-PPO (seed 0)"
  python scripts/plot_f6.py --right-method greedy_aoi        # pipeline check without a model
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uavaoi import HEURISTICS, SUITES, EnvConfig, UAVAoIEnv
from uavaoi.runrecord import REPO_ROOT
from plot_trajectory import degeneracy_flags, draw, rollout


def alt_text(suite: str, seed: int, env: UAVAoIEnv, panels: list) -> str:
    parts = [f"Two maps of the same {suite} scenario (evaluation seed {seed}): {env.N} sensors in a "
             f"{env.L:.0f} m by {env.L:.0f} m area, side by side."]
    for name, m in panels:
        parts.append(f"{name}: mean AoI {m['mean_aoi']:.1f} slots, {m['collections']} collections, "
                     f"coverage {m['coverage']:.2f}, action shares hover/slow/fast "
                     f"{m['hover_frac']:.2f}/{m['slow_frac']:.2f}/{m['fast_frac']:.2f}, "
                     f"battery empty before the horizon: {'yes' if m['early_termination'] else 'no'}.")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--left-method", choices=list(HEURISTICS), default="tsp")
    ap.add_argument("--model", default=None, help="SB3 model .zip for the right panel")
    ap.add_argument("--right-method", choices=list(HEURISTICS), default=None,
                    help="heuristic for the right panel instead of a model (pipeline check)")
    ap.add_argument("--label", default=None, help="right panel name, e.g. 'DR-PPO (seed 0)'")
    ap.add_argument("--suite", choices=list(SUITES), default="ood_cluster")
    ap.add_argument("--seed", type=int, default=100_000, help="episode seed; fixed before seeing results")
    ap.add_argument("--config", default=None, help="JSON with EnvConfig overrides (same for both panels)")
    ap.add_argument("--out", default=None, help="default figures/F6_<suite>_<seed>.pdf")
    args = ap.parse_args()
    if bool(args.model) == bool(args.right_method):
        ap.error("give exactly one of --model or --right-method")
    if args.config and not os.path.isfile(args.config):
        ap.error(f"config file not found: {args.config}")

    cfg = EnvConfig(**(json.load(open(args.config)) if args.config else {}))
    if args.model:
        from evaluate import SB3Policy
        right, right_name = SB3Policy(args.model), args.label or "model"
    else:
        right, right_name = HEURISTICS[args.right_method](), args.label or args.right_method
    left, left_name = HEURISTICS[args.left_method](), args.left_method.upper()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.8))
    panels, envs = [], []
    for ax, pol, name, show in ((axes[0], left, left_name, False), (axes[1], right, right_name, True)):
        env = UAVAoIEnv(scenario=SUITES[args.suite], cfg=cfg)   # same seed -> same scenario
        ep = rollout(env, pol, args.seed)
        flags = degeneracy_flags(ep["metrics"], masked=getattr(pol, "masked", True))
        draw(ax, env, ep, name, flags, show_legend=show)
        panels.append((name, ep["metrics"]))
        envs.append(env)
    if not (envs[0].N == envs[1].N and (envs[0].sensors == envs[1].sensors).all()):
        raise RuntimeError("the two panels did not get the same scenario")
    if axes[1].get_legend() is not None:     # one shared legend under both panels
        leg = axes[1].get_legend()
        axes[1].legend_ = None
        fig.legend(leg.legend_handles, [t.get_text() for t in leg.get_texts()], loc="lower center",
                   ncol=7, fontsize=7.5, frameon=False)
    fig.suptitle(f"{args.suite} · evaluation seed {args.seed} · N={envs[0].N}, L={envs[0].L:.0f} m", fontsize=10)
    fig.tight_layout(rect=(0, 0.05, 1, 0.97))

    out = args.out or os.path.join(REPO_ROOT, "figures", f"F6_{args.suite}_{args.seed}.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    text = alt_text(args.suite, args.seed, envs[0], panels)
    with open(out + ".alt.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    for name, m in panels:
        print(f"{name}: mean AoI {m['mean_aoi']:.2f}, coverage {m['coverage']:.2f}, "
              f"hover/slow/fast {m['hover_frac']:.2f}/{m['slow_frac']:.2f}/{m['fast_frac']:.2f}")
    print("saved", out, "and", out + ".alt.txt")


if __name__ == "__main__":
    main()
