"""Tests for the reporting additions in scripts/analyze.py (issue #14, PREREG sec. 1 and 8).

  python tests/test_analyze.py

Synthetic evaluation CSVs in a temporary directory; no real result is read or written.
"""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import analyze  # noqa: E402
from uavaoi.stats import holm, ood_degradation, permutation_test  # noqa: E402

SUITES = ["id", "ood_cluster", "ood_density", "ood_area", "ood_energy"]
FIELDS = ["method", "train_seed", "suite", "episode_seed", "mean_aoi", "peak_aoi", "early_termination"]


def write_run(root, name, method, seed, aoi_by_suite, status="completed", n_ep=5):
    d = os.path.join(root, name)
    os.makedirs(d)
    with open(os.path.join(d, "events.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        for s in SUITES:
            for e in range(n_ep):
                w.writerow({"method": method, "train_seed": seed, "suite": s, "episode_seed": 100000 + e,
                            "mean_aoi": aoi_by_suite[s] + 0.01 * e, "peak_aoi": 300.0,
                            "early_termination": "True" if e % 2 else "False"})
    with open(os.path.join(d, "run_record.json"), "w") as f:
        json.dump({"run_id": name, "status": status}, f)
    return os.path.join(d, "events.csv")


def make_experiment(root, dr_deg, fx_deg, n_seeds=10):
    """DR and Fixed runs with A_id = 50 (DR) / 100 (Fixed) and the given per-suite degradation."""
    rng = np.random.default_rng(1)
    paths = []
    for k in range(n_seeds):
        for m, base, deg in (("dr_ppo", 50.0, dr_deg), ("fixed_ppo", 100.0, fx_deg)):
            a = {"id": base * (1 + 0.01 * rng.standard_normal())}
            for s, g in zip(SUITES[1:], deg):
                a[s] = a["id"] * (1 + g + 0.01 * rng.standard_normal())
            paths.append(write_run(root, f"eval_{m}_s{k}", m, k, a))
    return paths


def run(paths, *extra):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "analyze.py"), *paths, *extra],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def table(text, header):
    """Rows of the markdown table that follows a line starting with `header`."""
    lines = text.splitlines()
    i = next(j for j, l in enumerate(lines) if l.startswith(header))
    rows = []
    for l in lines[i + 1:]:
        if l.startswith("| ---"):
            continue
        if not l.startswith("|"):
            if rows:
                break
            continue
        rows.append([c.strip() for c in l.strip("|").split("|")])
    return rows


def test_decision_uses_locked_p_values():
    with tempfile.TemporaryDirectory() as root:
        paths = make_experiment(root, dr_deg=[0.05, 0.10, 0.20, 0.30], fx_deg=[0.30, 0.40, 0.50, 0.12])
        code, out, err = run(paths)
        assert code == 0, err
        locked = {r[0]: r[4] for r in table(out, "| Suite | deg DR (mean)")}
        new = {r[0]: r[7] for r in table(out, "| Suite | n DR / n Fixed")}
        assert len(locked) == 4 and locked == new, (locked, new)


def test_pass_rule_and_verdict():
    with tempfile.TemporaryDirectory() as root:
        # Delta = 0.25, 0.30, 0.30 (pass) and 0.02 (significant but below 0.10 -> no)
        paths = make_experiment(root, dr_deg=[0.05, 0.10, 0.20, 0.30], fx_deg=[0.30, 0.40, 0.50, 0.32])
        code, out, err = run(paths)
        assert code == 0, err
        rows = {r[0]: r for r in table(out, "| Suite | n DR / n Fixed")}
        assert [rows[s][8] for s in SUITES[1:]] == ["yes", "yes", "yes", "no"], rows
        assert "**H1: 3/4 suites pass -> SUPPORTED**" in out
        # the same data with delta = 0.30 leaves at most 2 suites -> not supported
        code, out, err = run(paths, "--delta", "0.30")
        assert "NOT supported" in out, out


def test_delta_matches_direct_computation():
    with tempfile.TemporaryDirectory() as root:
        paths = make_experiment(root, dr_deg=[0.05, 0.10, 0.20, 0.30], fx_deg=[0.30, 0.40, 0.50, 0.32])
        rows = analyze.load(paths)
        ps = analyze.per_seed(rows)
        code, out, _ = run(paths)
        got = {r[0]: float(re.match(r"([+-][\d.]+)", r[6]).group(1)) for r in table(out, "| Suite | n DR / n Fixed")}
        pvals = []
        for s in SUITES[1:]:
            ks = sorted(ps["dr_ppo"][s])
            dr = ood_degradation([ps["dr_ppo"][s][k] for k in ks], [ps["dr_ppo"]["id"][k] for k in ks])
            fx = ood_degradation([ps["fixed_ppo"][s][k] for k in ks], [ps["fixed_ppo"]["id"][k] for k in ks])
            assert abs(got[s] - (fx.mean() - dr.mean())) < 5e-4, (s, got[s], fx.mean() - dr.mean())
            pvals.append(permutation_test(dr, fx, "less"))
        assert all(0 <= p <= 1 for p in holm(pvals))


def test_duplicate_seed_stops():
    with tempfile.TemporaryDirectory() as root:
        paths = make_experiment(root, [0.1] * 4, [0.2] * 4, n_seeds=2)
        a = {s: 60.0 for s in SUITES}
        paths.append(write_run(root, "eval_dr_again_s0", "dr_ppo", 0, a))
        code, _, err = run(paths)
        assert code != 0 and "dr_ppo seed 0" in err, (code, err)


def test_incomplete_run_is_excluded_and_listed():
    with tempfile.TemporaryDirectory() as root:
        paths = make_experiment(root, [0.1] * 4, [0.2] * 4, n_seeds=3)
        paths.append(write_run(root, "eval_fixed_s9", "fixed_ppo", 9, {s: 1.0 for s in SUITES}, status="running"))
        code, out, err = run(paths)
        assert code == 0, err
        assert "eval_fixed_s9" in out and ": running" in out
        assert "fixed_ppo/9" not in out.split("## Runs")[1].split("\n")[2]
        assert "**Warning:** 3 DR seed(s)" in out


def test_figure_and_alt_text():
    with tempfile.TemporaryDirectory() as root:
        paths = make_experiment(root, [0.1] * 4, [0.2] * 4, n_seeds=3)
        fig = os.path.join(root, "fig", "F4.png")
        code, out, err = run(paths, "--fig", fig)
        assert code == 0, err
        assert os.path.getsize(fig) > 1000
        with open(fig + ".alt.txt") as f:
            assert "DR-PPO mean deg" in f.read()


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for f in fns:
        try:
            f()
            print(f"PASS {f.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {f.__name__}: {e!r}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
