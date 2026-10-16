"""Run records (Form E of notes/workbook_forms.md) and provenance helpers.

Every run writes into its own directory  results/raw/<experiment_id>/<run_id>/ ,
which must not already exist: results/raw/ is append-only. Fixing an analysis means
re-deriving from the same raw files, never editing them.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import platform
import subprocess
import sys
from typing import Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VN_TZ = _dt.timezone(_dt.timedelta(hours=7))


def now_iso() -> str:
    return _dt.datetime.now(VN_TZ).isoformat(timespec="seconds")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _git(*args) -> Optional[str]:
    try:
        return subprocess.run(["git", "-C", REPO_ROOT, *args], capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:  # noqa: BLE001 - not a git checkout, or git missing
        return None


def code_revision() -> dict:
    rev = _git("rev-parse", "HEAD")
    dirty = _git("status", "--porcelain", "--untracked-files=no")
    return {"commit": rev, "dirty": bool(dirty)}


def environment_info() -> dict:
    info = {"python": sys.version.split()[0], "platform": platform.platform(),
            "machine": platform.machine(), "node": platform.node()}
    for mod in ("numpy", "torch", "gymnasium", "stable_baselines3", "sb3_contrib", "scipy"):
        try:
            info[mod] = __import__(mod).__version__
        except Exception:  # noqa: BLE001
            info[mod] = None
    return info


def new_run_dir(experiment_id: str, run_id: Optional[str] = None, base: Optional[str] = None) -> tuple:
    """Create results/raw/<experiment_id>/<run_id>/ ; refuse to reuse an existing one."""
    if not experiment_id or "/" in experiment_id:
        raise ValueError("experiment_id must be a non-empty name without '/' (e.g. EXP-02)")
    run_id = run_id or _dt.datetime.now(VN_TZ).strftime("%Y%m%d-%H%M%S")
    base = base or os.path.join(REPO_ROOT, "results", "raw")
    path = os.path.join(base, experiment_id, run_id)
    if os.path.exists(path):
        raise FileExistsError(f"{path} already exists — results/raw is append-only; pick a new run_id")
    os.makedirs(path)
    return run_id, path


class RunRecord:
    """Collects Form E fields; `save()` writes run_record.json into the run directory."""

    def __init__(self, experiment_id: str, run_dir: str, run_id: str, config: dict, seeds: dict):
        self.run_dir = run_dir
        rev = code_revision()
        self.data = {
            "run_id": run_id,
            "experiment_id": experiment_id,
            "status": "running",
            "code_revision": rev["commit"],
            "uncommitted_patch_path": None,
            "config_path": "config.json",
            "environment_path": "environment.json",
            "data_manifest_path": os.path.relpath(os.path.join(REPO_ROOT, "data", "eval_manifest.json"), REPO_ROOT),
            "checkpoint_digest": "not-applicable",
            "seeds": seeds,
            "started_at": now_iso(),
            "finished_at": None,
            "counts": {},
            "metrics": {},
            "raw_events_path": None,
            "warnings": [],
            "failure_reason": None,
        }
        if rev["dirty"]:
            patch = _git("diff", "HEAD")
            p = os.path.join(run_dir, "uncommitted.patch")
            with open(p, "w") as f:
                f.write(patch or "")
            self.data["uncommitted_patch_path"] = "uncommitted.patch"
            self.data["warnings"].append("working tree had uncommitted changes; patch saved")
        with open(os.path.join(run_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2, default=str)
        with open(os.path.join(run_dir, "environment.json"), "w") as f:
            json.dump(environment_info(), f, indent=2)
        self.save()

    def save(self):
        with open(os.path.join(self.run_dir, "run_record.json"), "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def finish(self, status: str = "completed", failure_reason: Optional[str] = None):
        if status not in ("completed", "failed", "timed_out"):
            raise ValueError(status)
        self.data["status"] = status
        self.data["failure_reason"] = failure_reason
        self.data["finished_at"] = now_iso()
        self.save()
