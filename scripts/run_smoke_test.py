"""Smallest end-to-end check. Must FAIL VISIBLY if anything required is missing or drifted.

  python scripts/run_smoke_test.py

Checks, in order:
  1. required files exist (env config, eval manifest, reference heuristic results)
  2. the scenario samplers still generate exactly the manifest's scenarios (SHA256)
  3. the TSP heuristic reproduces the reference per-episode AoI exactly on 5 episodes
     per suite (deterministic environment -> any difference is a behaviour change)
Writes a run record under results/raw/SMOKE/<run-id>/.
"""
from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from uavaoi import SUITES, EnvConfig, UAVAoIEnv, eval_seeds, run_episode
from uavaoi.baselines import TSPPolicy
from uavaoi.runrecord import REPO_ROOT, RunRecord, new_run_dir
from uavaoi.scenarios import suite_digest

CONFIG = os.path.join(REPO_ROOT, "configs", "env_default.json")
MANIFEST = os.path.join(REPO_ROOT, "data", "eval_manifest.json")
REFERENCE = os.path.join(REPO_ROOT, "results", "raw", "heuristics", "heuristics_100ep_2026-10-16.csv")
N_CHECK = 5


def fail(msg: str):
    print(f"SMOKE TEST FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    for p in (CONFIG, MANIFEST, REFERENCE):
        if not os.path.isfile(p):
            fail(f"required file missing: {os.path.relpath(p, REPO_ROOT)}")
    cfg = EnvConfig(**json.load(open(CONFIG)))
    manifest = json.load(open(MANIFEST))
    seeds = eval_seeds(manifest["n_episodes"])

    run_id, run_dir = new_run_dir("SMOKE")
    rr = RunRecord("SMOKE", run_dir, run_id, config={"env_cfg": cfg.to_dict()},
                   seeds={"eval_episode_seeds": [seeds[0], seeds[N_CHECK - 1]]})
    problems = []
    for name, spec in SUITES.items():
        if suite_digest(spec, seeds) != manifest["suites"][name]["sha256"]:
            problems.append(f"scenario digest mismatch for suite '{name}'")

    ref = {}
    with open(REFERENCE) as f:
        for r in csv.DictReader(f):
            if r["method"] == "tsp":
                ref[(r["suite"], int(r["episode_seed"]))] = float(r["mean_aoi"])
    for name, spec in SUITES.items():
        env = UAVAoIEnv(scenario=spec, cfg=cfg)
        for s in seeds[:N_CHECK]:
            got = run_episode(env, TSPPolicy(), seed=s)["mean_aoi"]
            want = ref.get((name, s))
            if want is None or abs(got - want) > 1e-9:
                problems.append(f"TSP {name} seed {s}: got {got:.6f}, reference {want}")
        rr.data["counts"][name] = N_CHECK

    if problems:
        rr.data["warnings"] = problems
        rr.finish("failed", failure_reason=f"{len(problems)} check(s) failed")
        fail("\n  " + "\n  ".join(problems))
    rr.finish("completed")
    print(f"SMOKE TEST PASSED: manifest digests match for {len(SUITES)} suites; "
          f"TSP reproduces reference on {N_CHECK} episodes x {len(SUITES)} suites. Record: {run_dir}")


if __name__ == "__main__":
    main()
