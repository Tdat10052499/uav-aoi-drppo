"""Unit tests. Run with `pytest -q` or, without pytest, `python tests/test_core.py`."""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from uavaoi import (EnvConfig, HEURISTICS, PRESETS, SUITES, TRAIN_FIXED, UAVAoIEnv,
                    characteristic_speeds, effective_radius, hover_power, propulsion_power,
                    run_episode)
from uavaoi.stats import bootstrap_ci, cliffs_delta, holm, iqm, permutation_test


# ---------------------------------------------------------------- energy model
def test_energy_matches_zeng_table_I():
    p = PRESETS["zeng2019_arxiv_v1"]
    assert abs(p.U_tip - 200.0) < 1e-9
    assert abs(p.v0 - 7.2) < 0.05            # Table I lists v0 = 7.2
    assert abs(propulsion_power(0.0, p) - hover_power(p)) < 1e-6   # P(0) = P0 + Pi


def test_light_preset_reproduces_commonly_cited_values():
    p = PRESETS["light"]
    assert abs(p.P0 - 79.86) < 0.05 and abs(p.Pi - 88.63) < 0.05


def test_characteristic_speeds_ordering():
    sp = characteristic_speeds()
    assert 0 < sp["V_me"] < sp["V_mr"]        # Zeng et al.: V_me <= V_mr
    assert sp["P_me"] < sp["P_hover"]         # hovering is not the most power-saving state


# ---------------------------------------------------------------- channel
def test_effective_radius_default():
    r = effective_radius(15e6, 3.0)
    assert 140 < r < 160                      # docs/02 section 4: ~149 m


# ---------------------------------------------------------------- environment
def _env(**kw):
    return UAVAoIEnv(cfg=EnvConfig(**kw))


def test_reset_shapes_and_determinism():
    env = _env()
    o1, _ = env.reset(seed=123)
    s1 = env.sensors.copy()
    o2, _ = env.reset(seed=123)
    assert o1.shape == env.observation_space.shape
    assert np.allclose(s1, env.sensors) and np.allclose(o1, o2)


def test_aoi_update_rule():
    env = _env()
    scn = {"L": 1000.0, "sensors": np.array([[500.0, 500.0], [900.0, 900.0]]),
           "E_max": 1e6, "start": np.array([500.0, 500.0])}
    env.reset(seed=0, options={"scenario": scn})
    env.step(1)                              # move: everyone ages by 1
    assert np.allclose(env.aoi, [2.0, 2.0])
    env.step(5)                              # move back toward sensor 0 (west at V_me)
    env.pos = np.array([500.0, 500.0])       # place exactly above sensor 0
    env.step(0)                              # collect
    assert env.aoi[0] == 1.0 and env.aoi[1] == 4.0


def test_collect_out_of_range_serves_nobody():
    env = _env()
    scn = {"L": 1000.0, "sensors": np.array([[900.0, 900.0]]), "E_max": 1e6,
           "start": np.array([100.0, 100.0])}
    env.reset(seed=0, options={"scenario": scn})
    env.step(0)
    assert env.aoi[0] == 2.0 and env.n_served.sum() == 0


def test_masks_block_leaving_area():
    env = _env()
    scn = {"L": 1000.0, "sensors": np.array([[500.0, 500.0]]), "E_max": 1e6,
           "start": np.array([0.0, 0.0])}
    env.reset(seed=0, options={"scenario": scn})
    m = env.action_masks()
    # West (dir 4) and South (dir 6) at both speeds must be invalid at the corner
    for d in (4, 6):
        assert not m[1 + d] and not m[9 + d]
    assert m[1 + 0] and m[1 + 2]             # East and North allowed


def test_early_battery_death_never_pays():
    """Return of an agent that drains the battery must be lower than one that survives
    doing nothing useful (anti reward-hacking check, docs/02 section 6)."""
    scn = {"L": 1000.0, "sensors": np.array([[100.0, 100.0], [900.0, 900.0]]),
           "E_max": 0.3e6, "start": np.array([500.0, 500.0])}
    env = _env()
    env.reset(seed=0, options={"scenario": scn})
    rewards, done = [], False
    while not done:
        t_before = env.t
        _, r, term, trunc, info = env.step(0)   # hover (most expensive) until battery dies
        rewards.append((t_before, r))
        done = term or trunc
    assert info["episode_metrics"]["early_termination"]
    worst = env.worst_step_cost
    # (a) every ordinary step costs no more than the worst-case bound
    assert all(r >= -worst - 1e-9 for _, r in rewards[:-1])
    # (b) the terminal step carries at least (remaining slots) x worst-case penalty
    t_last, r_last = rewards[-1]
    remaining = env.cfg.T - (t_last + 1)
    assert r_last <= -remaining * worst + 1e-9
    # (c) the AoI metric covers the full horizon even after early termination
    assert info["episode_metrics"]["mean_aoi"] > 0


def test_episode_runs_for_all_heuristics_and_suites():
    for suite in SUITES.values():
        env = UAVAoIEnv(scenario=suite)
        for name, cls in HEURISTICS.items():
            m = run_episode(env, cls(), seed=7)
            assert 1.0 <= m["mean_aoi"] <= env.cfg.T
            assert 0.0 <= m["energy_frac"] <= 1.0 + 1e-9


def test_fixed_scenario_is_fixed():
    env = UAVAoIEnv(scenario=TRAIN_FIXED)
    env.reset(seed=1); a = env.sensors.copy()
    env.reset(seed=2); b = env.sensors.copy()
    assert np.allclose(a, b) and len(a) == 20


# ---------------------------------------------------------------- statistics
def test_stats_helpers():
    x = np.arange(10.0)
    assert abs(iqm(x) - 4.5) < 1e-9
    pt, lo, hi = bootstrap_ci(x, n_boot=2000)
    assert lo <= pt <= hi
    rng = np.random.default_rng(0)
    a, b = rng.normal(0, 1, 15), rng.normal(1.5, 1, 15)
    assert permutation_test(a, b, "less", n_perm=5000) < 0.01
    assert cliffs_delta(a, b) < -0.5
    adj = holm([0.01, 0.04, 0.03])
    assert abs(adj[0] - 0.03) < 1e-9 and all(0 <= p <= 1 for p in adj)


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
