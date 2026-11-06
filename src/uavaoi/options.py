"""Tour-guided semi-MDP on top of UAVAoIEnv (EXP-08, component B).

Design: notes/2026-11-06_dat_thiet-ke_PG-TG-PPO.md section 3. One decision = one
macro-action spanning several slots of the base environment:

  actions 0..K-1   fly to candidate c_i at V_me, collect once when in range, stop
  actions K..2K-1  same at V_mr
  action  2K       wait: hover one slot (the base env collects if a sensor is in range)

Candidates (re-computed at every decision point):
  c_1  next stop on the TSP tour (tour built at reset, as in TSPPolicy)
  c_2  the stop after c_1
  c_3..c_K  sensors with the highest AoI / flight-slots ratio, excluding c_1 and c_2

The low level is deterministic (baselines._move_towards with the chosen speed forced).
The decision reward is the sum of the base-env slot rewards of the macro-action
(no discounting inside; option (b) of the design note ✱ to be fixed in the EXP-08 card).
The optional "end early on purpose" action of the design note is left out: the base env
charges the worst-case cost for every slot lost to an early end, so it can never pay.
"""
from __future__ import annotations

from typing import Optional

import numpy as np

from ._compat import HAS_GYM, gym, spaces
from .baselines import _move_towards, tsp_tour
from .env import EnvConfig, UAVAoIEnv
from .scenarios import ScenarioSpec

N_FEAT = 4  # per candidate: flight slots at V_me / T, AoI / Delta_max, energy need / energy left, on-tour flag


class TourGuidedEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, scenario: Optional[ScenarioSpec] = None, cfg: Optional[EnvConfig] = None,
                 K: int = 5, max_macro_slots: int = 100):
        self.base = UAVAoIEnv(scenario=scenario, cfg=cfg)
        self.cfg = self.base.cfg
        self.K = int(K)
        self.max_macro_slots = int(max_macro_slots)
        self.n_actions = 2 * self.K + 1
        self.WAIT = 2 * self.K
        self.action_space = spaces.Discrete(self.n_actions)
        if HAS_GYM:
            self.observation_space = spaces.Dict({
                "map": self.base.observation_space,
                "cand": spaces.Box(low=0.0, high=np.inf, shape=(self.K * N_FEAT,), dtype=np.float32),
            })
        else:  # numpy-only shim: shapes are enough for the tests
            self.observation_space = {"map": self.base.observation_space,
                                      "cand": spaces.Box(0.0, np.inf, (self.K * N_FEAT,))}
        self.decisions = 0

    # ------------------------------------------------------------------ API
    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        _, info = self.base.reset(seed=seed, options=options)
        self.order = tsp_tour(self.base.sensors, self.base.pos)
        self.k = 0
        self.decisions = 0
        self._done = False
        self._last_info = info
        self._compute_candidates()
        return self._obs(), info

    def action_masks(self) -> np.ndarray:
        b = self.base
        mask = np.zeros(self.n_actions, dtype=bool)
        for i, c in enumerate(self.cand):
            if c < 0:
                continue
            for j, (speed_E, V) in enumerate(((b.P_slow, b.V_slow), (b.P_fast, b.V_fast))):
                if self._energy_need(c, speed_E, V) <= b.energy:
                    mask[j * self.K + i] = True
        # wait is always allowed: if even hovering is unaffordable the base env ends the episode
        mask[self.WAIT] = True
        return mask

    def step(self, action: int):
        a = int(action)
        b = self.base
        if self._done:
            raise RuntimeError("step() after the episode ended; call reset()")
        total_r, slots = 0.0, 0
        term = trunc = False
        info = self._last_info
        if a == self.WAIT:
            _, r, term, trunc, info = b.step(0)
            total_r, slots = r, 1
        else:
            i, speed = a % self.K, ("slow" if a < self.K else "fast")
            c = int(self.cand[i])
            if c < 0:
                raise ValueError(f"action {a} points at an empty candidate slot; respect action_masks()")
            target = b.sensors[c]
            while slots < self.max_macro_slots:
                m = b.action_masks()
                if np.linalg.norm(target - b.pos) <= b.r_eff and m[0]:
                    _, r, term, trunc, info = b.step(0)      # collect (env serves max-AoI sensor in range)
                    total_r += r
                    slots += 1
                    self._advance_tour(c)
                    break
                _, r, term, trunc, info = b.step(_move_towards(b, target, m, speed))
                total_r += r
                slots += 1
                if term or trunc:
                    break
        self.decisions += 1
        self._done = bool(term or trunc)
        self._last_info = info
        if self._done and "episode_metrics" in info:
            info = dict(info)
            info["episode_metrics"] = {**info["episode_metrics"], "decisions": self.decisions}
        else:
            self._compute_candidates()
        info = {**info, "macro_slots": slots}
        return self._obs(), float(total_r), bool(term), bool(trunc), info

    # ------------------------------------------------------------ helpers
    def _flight_slots(self, c: int, V: float) -> float:
        b = self.base
        d = max(float(np.linalg.norm(b.sensors[c] - b.pos)) - b.r_eff, 0.0)
        return float(np.ceil(d / (V * b.cfg.dt) - 1e-9))

    def _energy_need(self, c: int, P_move: float, V: float) -> float:
        b = self.base
        return self._flight_slots(c, V) * P_move * b.cfg.dt + b.E_hover_tx

    def _advance_tour(self, served: int):
        n = len(self.order)
        nxt = [self.order[(self.k + j) % n] for j in range(min(2, n))]
        if served in nxt:   # c_1 served, or c_2 served (c_1 skipped)
            self.k = (self.k + nxt.index(served) + 1) % n

    def _compute_candidates(self):
        b = self.base
        n = len(self.order)
        cand = []
        for j in range(min(2, n)):
            s = self.order[(self.k + j) % n]
            if s not in cand:
                cand.append(s)
        slots = np.array([self._flight_slots(s, b.V_slow) for s in range(b.N)])
        score = b.aoi / (slots + 1.0)
        for s in np.argsort(-score, kind="stable"):
            if len(cand) >= self.K:
                break
            if int(s) not in cand:
                cand.append(int(s))
        self.cand = np.array(cand + [-1] * (self.K - len(cand)), dtype=int)
        self.on_tour = np.array([1.0 if i < min(2, n) else 0.0 for i in range(self.K)], dtype=np.float32)

    def _obs(self) -> dict:
        b = self.base
        feat = np.zeros((self.K, N_FEAT), dtype=np.float32)
        for i, c in enumerate(self.cand):
            if c < 0:
                continue
            need = self._energy_need(c, b.P_slow, b.V_slow)
            if self.cfg.obs_mode == "grounded":
                feat[i, 0] = self._flight_slots(c, b.V_slow) / b.cfg.T
                feat[i, 2] = min(need / max(b.energy, 1e-9), self.cfg.rho_clip)
            else:  # legacy normalisation (arm M3): relative to the area and to E_max
                feat[i, 0] = float(np.linalg.norm(b.sensors[c] - b.pos)) / (b.L * np.sqrt(2.0))
                feat[i, 2] = need / b.E_max
            feat[i, 1] = b.aoi[c] / b.Delta_max
            feat[i, 3] = self.on_tour[i]
        return {"map": b._obs(), "cand": feat.reshape(-1)}


class HighLevelGreedy:
    """Ablation: same candidates and low level, hand rule on top. Candidate with the highest
    AoI / flight-slots ratio; speed by the TSP-adaptive rule (V_mr if rho_E > 1)."""
    name = "hl_greedy"

    def reset(self, wenv: TourGuidedEnv):
        pass

    def act(self, wenv: TourGuidedEnv) -> int:
        b = wenv.base
        mask = wenv.action_masks()
        fast = b.rho_E() > 1.0
        best, best_score = wenv.WAIT, -np.inf
        for i, c in enumerate(wenv.cand):
            if c < 0:
                continue
            for j in ((1, 0) if fast else (0, 1)):   # preferred speed first
                a = j * wenv.K + i
                if mask[a]:
                    sc = b.aoi[c] / (wenv._flight_slots(c, b.V_slow) + 1.0)
                    if sc > best_score:
                        best, best_score = a, sc
                    break
        return int(best)


OPTION_HEURISTICS = {"hl_greedy": HighLevelGreedy}


def run_option_episode(wenv: TourGuidedEnv, policy, seed: int) -> dict:
    wenv.reset(seed=seed)
    policy.reset(wenv)
    done, total_r, info = False, 0.0, {}
    while not done:
        _, r, term, trunc, info = wenv.step(policy.act(wenv))
        total_r += r
        done = term or trunc
    m = dict(info["episode_metrics"])
    m["return"] = total_r
    return m
