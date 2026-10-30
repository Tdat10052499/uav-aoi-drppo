"""Build data/checkpoint_manifest.md rows from training run records.

Reads  results/raw/<experiment-id>/<run-id>/run_record.json  (+ config.json, environment.json)
written by train_ppo.py and prints one manifest row per run. With --verify the model file is
re-hashed and must match checkpoint_digest; with --append the rows are added to the manifest
(run IDs already listed are skipped, never rewritten).

Examples
  python scripts/manifest_row.py results/raw/EXP-02/dr_ppo_mask_lam0.1_s0_20261102-101500
  python scripts/manifest_row.py results/raw/EXP-02/* --verify --append
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from uavaoi.runrecord import REPO_ROOT, sha256_file

MANIFEST = os.path.join(REPO_ROOT, "data", "checkpoint_manifest.md")


def _load(run_dir: str, name: str) -> dict:
    path = os.path.join(run_dir, name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _learner(args: dict) -> str:
    if args.get("algo") == "dqn":
        return "DQN"
    return "MaskablePPO" if args.get("masked") else "PPO"


def manifest_row(run_dir: str, verify: bool = False, location: str | None = None,
                 machine: str | None = None) -> tuple:
    """Return (run_id, markdown row). Refuses runs that cannot back a number in the paper."""
    rr = _load(run_dir, "run_record.json")
    if rr.get("status") != "completed":
        raise ValueError(f"{rr.get('run_id')}: status={rr.get('status')!r}, only completed runs go in the manifest")
    digest = rr.get("checkpoint_digest") or ""
    if not digest.startswith("sha256:"):
        raise ValueError(f"{rr.get('run_id')}: no checkpoint_digest (not a training run?)")
    sha = digest.split(":", 1)[1]
    model_path = (rr.get("model_path") or "").replace("\\", "/")
    if verify:
        full = model_path if os.path.isabs(model_path) else os.path.join(REPO_ROOT, model_path)
        if not os.path.isfile(full):
            raise FileNotFoundError(f"{rr['run_id']}: model file {full} not found, cannot verify")
        actual = sha256_file(full)
        if actual != sha:
            raise ValueError(f"{rr['run_id']}: SHA256 mismatch, run_record {sha} vs file {actual}")
    args = _load(run_dir, "config.json").get("args", {})
    env = _load(run_dir, "environment.json")
    cells = [rr["experiment_id"], rr["run_id"], _learner(args), args.get("train", "?"),
             str(rr.get("seeds", {}).get("train_seed", args.get("seed", "?"))),
             str(rr.get("counts", {}).get("timesteps", args.get("timesteps", "?"))),
             sha, location or model_path, machine or env.get("node") or "?"]
    return rr["run_id"], "| " + " | ".join(cells) + " |"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dirs", nargs="+", help="results/raw/<EXP>/<run-id> directories (globs allowed)")
    ap.add_argument("--verify", action="store_true", help="re-hash model.zip and require it to match")
    ap.add_argument("--append", action="store_true", help=f"append new rows to {os.path.relpath(MANIFEST, REPO_ROOT)}")
    ap.add_argument("--location", default=None, help="override 'Vị trí lưu' (e.g. a GitHub Release asset URL)")
    ap.add_argument("--machine", default=None, help="override 'Máy' (default: node name in environment.json)")
    args = ap.parse_args()

    run_dirs = [d for pat in args.run_dirs for d in (sorted(glob.glob(pat)) or [pat])]
    rows = [manifest_row(d, args.verify, args.location, args.machine) for d in run_dirs]
    for _, row in rows:
        print(row)
    if not args.append:
        return
    with open(MANIFEST, encoding="utf-8") as f:
        text = f.read()
    new = [row for run_id, row in rows if f"| {run_id} |" not in text]
    if not new:
        print("manifest: nothing new to append")
        return
    lines = text.splitlines()
    last_row = max(i for i, line in enumerate(lines) if line.startswith("|"))
    lines[last_row + 1:last_row + 1] = new
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"manifest: appended {len(new)} row(s), skipped {len(rows) - len(new)} already listed")


if __name__ == "__main__":
    main()
