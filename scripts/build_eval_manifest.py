"""Write data/eval_manifest.json (or, with --suites-b, data/eval_manifest_B.json): evaluation seeds, suite specifications and a SHA256 of
the scenarios each suite generates. Re-run ONLY when a scenario change is intended and
recorded in docs/DECISIONS.md; the smoke test fails if the manifest and code disagree."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from uavaoi.scenarios import build_manifest, build_manifest_b
from uavaoi.runrecord import REPO_ROOT, now_iso

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--suites-b", action="store_true",
                    help="write data/eval_manifest_B.json (EXP-08 suites, seeds 300000-300099) instead")
    args = ap.parse_args()
    m = build_manifest_b(100) if args.suites_b else build_manifest(100)
    m["generated_at"] = now_iso()
    out = os.path.join(REPO_ROOT, "data", "eval_manifest_B.json" if args.suites_b else "eval_manifest.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(m, f, indent=2)
    print("wrote", out)
