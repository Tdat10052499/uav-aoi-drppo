"""Unit tests. Run with `pytest -q` or, without pytest, `python tests/test_core.py`."""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

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


def test_single_speed_masks_fast_moves():
    env = _env(single_speed=True)
    env.reset(seed=0)
    for _ in range(20):
        m = env.action_masks()
        assert not m[9:].any() and m[1:9].any()
        env.step(int(np.flatnonzero(m)[-1]))
    try:
        env.step(9)
        raise AssertionError("fast move accepted with single_speed=True")
    except ValueError:
        pass
    run_episode(env, HEURISTICS["tsp"](), seed=100000)   # heuristics follow the mask


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


# ---------------------------------------------------------------- EXP-08 (PG-TG-PPO)
def test_grounded_obs_equals_legacy_map_at_1000m():
    """At L = G * cell_m (1000 m) the grounded map channels equal the legacy ones; only the
    energy channel differs (design note section 2)."""
    a, b = _env(), _env(obs_mode="grounded")
    rng = np.random.default_rng(0)
    for s in range(10):
        oa, _ = a.reset(seed=s)
        ob, _ = b.reset(seed=s)
        for _ in range(30):
            act = int(rng.choice(np.flatnonzero(a.action_masks())))
            oa, *_ = a.step(act)
            ob, *_ = b.step(act)
            assert np.array_equal(oa[[0, 1, 2, 4]], ob[[0, 1, 2, 4]])


def test_grounded_energy_channel_sees_absolute_budget():
    """Same state, different E_max: legacy obs differ only through E/E_max at equal absolute
    energy; grounded obs are identical (the proposition of design note section 2). At t = 0
    with different E_max, legacy shows 1.0 for both while grounded differs."""
    sens = np.array([[200.0, 300.0], [700.0, 800.0]])
    scn = lambda E: {"L": 1000.0, "sensors": sens, "E_max": E, "start": np.array([500.0, 500.0])}
    for mode, same_at_t0 in (("legacy", True), ("grounded", False)):
        e1, e2 = _env(obs_mode=mode), _env(obs_mode=mode)
        o1, _ = e1.reset(seed=0, options={"scenario": scn(0.5e6)})
        o2, _ = e2.reset(seed=0, options={"scenario": scn(1.0e6)})
        assert np.array_equal(o1, o2) == same_at_t0, mode
    g1, g2 = _env(obs_mode="grounded"), _env(obs_mode="grounded")
    g1.reset(seed=0, options={"scenario": scn(0.5e6)})
    g2.reset(seed=0, options={"scenario": scn(1.0e6)})
    g2.energy = g1.energy                       # same absolute energy left, same everything else
    assert np.array_equal(g1._obs(), g2._obs())


def test_grounded_obs_shows_larger_area():
    from uavaoi import ScenarioSpec
    e = UAVAoIEnv(scenario=ScenarioSpec(L=2000.0), cfg=EnvConfig(obs_mode="grounded"))
    o, _ = e.reset(seed=3)
    assert o.shape == e.observation_space.shape
    assert abs(o[1].sum() * e.cfg.count_norm - e.N) < 1e-4      # every sensor still on the map
    inside = (o[2] == 0).sum()
    assert inside > 16 * 16                                      # more in-area cells than at 1000 m


def test_tsp_variants_respect_speed_rule():
    env = UAVAoIEnv()
    eco = HEURISTICS["tsp_eco"]()
    obs, _ = env.reset(seed=5)
    eco.reset(env)
    for _ in range(60):
        a = eco.act(env)
        m = env.action_masks()
        assert a == 0 or a <= 8 or not m[1:9].any(), "tsp_eco used V_mr while a V_me move was allowed"
        env.step(a)
    ad = HEURISTICS["tsp_adaptive"]()
    env.reset(seed=5, options={"scenario": {**env._scn, "E_max": 0.3e6}})
    ad.reset(env)
    assert env.rho_E() < 1.0 and ad._speed(env) == "slow"


def test_tour_guided_wrapper_runs_and_masks():
    from uavaoi.options import TourGuidedEnv, HighLevelGreedy, run_option_episode
    for mode in ("grounded", "legacy"):
        w = TourGuidedEnv(scenario=SUITES["ood_energy"], cfg=EnvConfig(obs_mode=mode))
        rng = np.random.default_rng(1)
        o, _ = w.reset(seed=11)
        assert o["map"].shape == (5, 31, 31) and o["cand"].shape == (w.K * 4,)
        done, slots = False, 0
        while not done:
            m = w.action_masks()
            assert m[w.WAIT] and m.shape == (2 * w.K + 1,)
            for i, c in enumerate(w.cand):          # empty candidate slots are never allowed
                if c < 0:
                    assert not m[i] and not m[w.K + i]
            o, r, te, tr, info = w.step(int(rng.choice(np.flatnonzero(m))))
            slots += info["macro_slots"]
            done = te or tr
        em = info["episode_metrics"]
        assert 1.0 <= em["mean_aoi"] <= 151.5 + 1e-9 and em["decisions"] >= 1
        assert slots <= w.cfg.T
        mg = run_option_episode(w, HighLevelGreedy(), seed=11)
        assert mg["decisions"] >= 1


def test_tour_guided_flight_estimate_is_an_upper_bound():
    """The energy mask uses _flight_slots + 1; the low level must never need more slots than
    that, otherwise the mask would allow targets the UAV cannot reach."""
    from uavaoi.options import TourGuidedEnv
    w = TourGuidedEnv(cfg=EnvConfig(obs_mode="grounded"))
    rng = np.random.default_rng(3)
    for trial in range(40):
        w.reset(seed=1000 + trial)
        b = w.base
        b.energy = 1e9                                   # isolate geometry from energy
        c = int(rng.integers(b.N))
        for a, V in ((c, b.V_slow), (w.K + c, b.V_fast)):
            w.reset(seed=1000 + trial)
            w.base.energy = 1e9
            w.cand = np.array([c] + [-1] * (w.K - 1))
            est = w._flight_slots(c, V)
            _, _, te, tr, info = w.step(0 if a == c else w.K)
            assert info["macro_slots"] - 1 <= est + 1, (trial, info["macro_slots"], est)   # +1 = margin in _energy_need


def test_tour_advances_only_when_target_served():
    from uavaoi.options import TourGuidedEnv
    w = TourGuidedEnv(cfg=EnvConfig(obs_mode="grounded"))
    # three sensors close together; a staler one that is neither c_1 nor c_2 gets served instead
    scn = {"L": 1000.0, "sensors": np.array([[500.0, 500.0], [520.0, 500.0], [540.0, 500.0], [900.0, 900.0]]),
           "E_max": 1e6, "start": np.array([520.0, 500.0])}
    w.reset(seed=0, options={"scenario": scn})
    c1, c2 = int(w.cand[0]), int(w.cand[1])
    other = next(i for i in range(3) if i not in (c1, c2))
    w.base.aoi[:] = 1.0
    w.base.aoi[other] = 50.0                          # the other close sensor is staler
    k0 = w.k
    w.step(0)                                         # fly to c1 (already in range): one collect slot
    assert w.base.n_served[other] == 1 and w.base.n_served[c1] == 0 and w.base.n_served[c2] == 0
    assert w.k == k0, "tour advanced although its target was not served"
    # the served sensor is c_2: the tour moves past c_2 (c_1 skipped), as TSPPolicy would not
    w2 = TourGuidedEnv(cfg=EnvConfig(obs_mode="grounded"))
    scn2 = {"L": 1000.0, "sensors": np.array([[500.0, 500.0], [520.0, 500.0], [540.0, 500.0]]),
            "E_max": 1e6, "start": np.array([520.0, 500.0])}
    w2.reset(seed=0, options={"scenario": scn2})
    c1, c2 = int(w2.cand[0]), int(w2.cand[1])
    w2.base.aoi[:] = 1.0
    w2.base.aoi[c2] = 50.0
    k0 = w2.k
    w2.step(0)
    assert w2.base.n_served[c2] == 1 and w2.k == (k0 + 2) % 3


def test_option_episodes_are_deterministic():
    from uavaoi.options import TourGuidedEnv, HighLevelGreedy, run_option_episode
    w = TourGuidedEnv(scenario=SUITES["ood_cluster"], cfg=EnvConfig(obs_mode="grounded"))
    a = run_option_episode(w, HighLevelGreedy(), seed=100003)
    b = run_option_episode(w, HighLevelGreedy(), seed=100003)
    assert a == b


def test_eval_guards_confirmatory_seeds():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from evaluate import check_confirmatory
    new, old, other = list(range(300000, 300100)), list(range(100000, 100100)), list(range(900000, 900030))
    assert check_confirmatory(new, ["id2"], False, False)                 # needs --confirmatory
    assert check_confirmatory(new, ["id2"], True, False)                  # needs the lock tag
    assert not check_confirmatory(new, ["id2"], True, True)
    assert check_confirmatory(new, ["id"], False, True)                   # protected seeds on any suite
    assert check_confirmatory(old, ["id"], True, True)                    # --confirmatory on wrong seeds
    assert not check_confirmatory(old, ["id"], False, False)              # EXP-01..03 use: untouched
    # EXP-08 suites on any seed before the lock: refused, except heuristics with --probe-b
    assert check_confirmatory(other, ["ood_area_2000"], False, False)
    assert not check_confirmatory(other, ["ood_area_2000"], False, False, probe_b=True)
    assert check_confirmatory(other, ["ood_area_2000"], False, False, probe_b=True, has_model=True)
    assert not check_confirmatory(other, ["ood_area_2000"], False, True, has_model=True)   # after lock
    assert check_confirmatory(new, ["ood_combo"], False, False, probe_b=True)              # still not 300000+


def test_training_seeds_never_reset_onto_eval_scenarios():
    """LDN review of PR #45 (L1): with the spaced scheme, training seed 100 / 200 / 300 would
    reset its envs on evaluation scenarios 100000+ / 200000+ / 300000+ (TRAIN_DR = id spec)."""
    from uavaoi.scenarios import reserved_overlap, train_reset_seeds, TRAIN_DR
    assert np.allclose(TRAIN_DR.sample(np.random.default_rng(100000))["sensors"],
                       SUITES["id"].sample(np.random.default_rng(100000))["sensors"])   # the leak is real
    for bad in (100, 200, 300):
        assert reserved_overlap(train_reset_seeds(bad, 8, "spaced")), bad
    for ok in list(range(0, 20)) + list(range(110, 120)) + [101, 201]:
        assert not reserved_overlap(train_reset_seeds(ok, 8, "spaced")), ok
    assert reserved_overlap(train_reset_seeds(99_999, 8, "sb3"))          # sb3 scheme checked too
    assert not reserved_overlap(train_reset_seeds(10, 8, "sb3"))


def test_eval_manifest_b_matches_samplers():
    import json
    from uavaoi.scenarios import SUITES_B, EVAL_SEED_BASE_B, suite_digest
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "eval_manifest_B.json")
    m = json.load(open(path))
    seeds = [EVAL_SEED_BASE_B + i for i in range(m["n_episodes"])]
    assert m["eval_seed_range"] == [300000, 300099]
    for name, spec in SUITES_B.items():
        assert suite_digest(spec, seeds) == m["suites"][name]["sha256"], name


# ---------------------------------------------------------------- provenance
def test_raw_dirs_are_append_only():
    import tempfile
    from uavaoi.runrecord import new_run_dir
    with tempfile.TemporaryDirectory() as base:
        new_run_dir("EXP-T", "r1", base=base)
        try:
            new_run_dir("EXP-T", "r1", base=base)
            raise AssertionError("re-using a raw run directory must fail")
        except FileExistsError:
            pass


def test_eval_refuses_single_speed_mismatch():
    import json
    import tempfile
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from evaluate import check_model_cfg
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw", "EXP-T", "r_1")          # results/raw/<exp>/<run_id>/config.json
        os.makedirs(raw)
        with open(os.path.join(raw, "config.json"), "w") as f:
            json.dump({"env_cfg": {**EnvConfig().to_dict(), "single_speed": True}}, f)
        model = os.path.join(tmp, "runs", "EXP-T", "r_1", "model.zip")   # runs/<exp>/<run_id>/model.zip
        errors, _ = check_model_cfg(model, EnvConfig(), raw_base=os.path.join(tmp, "raw"))
        assert errors and "single_speed" in errors[0]
        errors, warnings = check_model_cfg(model, EnvConfig(single_speed=True), raw_base=os.path.join(tmp, "raw"))
        assert not errors and not warnings


def test_eval_obs_mode_mismatch_is_an_error():
    import json
    import tempfile
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from evaluate import check_model_cfg
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw", "EXP-T", "r_2")
        os.makedirs(raw)
        old = {k: v for k, v in EnvConfig().to_dict().items() if k not in ("obs_mode", "cell_m", "rho_clip")}
        with open(os.path.join(raw, "config.json"), "w") as f:      # an EXP-03 config: no obs_mode key
            json.dump({"env_cfg": old}, f)
        model = os.path.join(tmp, "runs", "EXP-T", "r_2", "model.zip")
        errors, _ = check_model_cfg(model, EnvConfig(), raw_base=os.path.join(tmp, "raw"))
        assert not errors                                           # legacy model, legacy eval: fine
        errors, _ = check_model_cfg(model, EnvConfig(obs_mode="grounded"), raw_base=os.path.join(tmp, "raw"))
        assert errors and "obs_mode" in errors[0]


def test_eval_manifest_matches_samplers():
    import json
    from uavaoi.scenarios import suite_digest, eval_seeds
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "eval_manifest.json")
    m = json.load(open(path))
    seeds = eval_seeds(m["n_episodes"])
    for name, spec in SUITES.items():
        assert suite_digest(spec, seeds) == m["suites"][name]["sha256"], name


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


def test_trajectory_behaviour_notes():
    """plot_trajectory.behaviour_notes: camping on one sensor and long idle hovering are noted;
    a well-spread episode gets no note (descriptive aid, not the G1 #4 criterion)."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from plot_trajectory import behaviour_notes, rollout
    assert behaviour_notes([179, 1, 0, 0], ["collect"] * 180, coverage=0.5 - 1e-9)[0].startswith("camping")
    assert behaviour_notes([179, 1, 0, 0], ["collect"] * 180, coverage=0.5) == []
    assert behaviour_notes([5, 4, 0], ["collect"] * 9, coverage=0.1) == []          # < 10 collections
    assert behaviour_notes([1, 1], ["idle"] * 3 + ["slow"] * 7, coverage=1.0) == ["idle hover 0.30 of slots"]
    env = UAVAoIEnv(scenario=SUITES["id"])
    ep = rollout(env, HEURISTICS["tsp"](), seed=100000)
    assert behaviour_notes(env.n_served, ep["kinds"], ep["metrics"]["coverage"]) == []

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
