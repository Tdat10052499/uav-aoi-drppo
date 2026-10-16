"""Heuristic baselines. They read the true environment state (sensor positions and
AoI), i.e. the same information that the map observation encodes, at full resolution."""
from __future__ import annotations

import numpy as np

from .env import DIRECTIONS, UAVAoIEnv


def _move_towards(env: UAVAoIEnv, target: np.ndarray, mask: np.ndarray) -> int:
    """Pick the feasible move whose direction is closest to the target bearing.
    Fast speed when far away, slow speed when close (avoid overshooting)."""
    vec = target - env.pos
    dist = float(np.linalg.norm(vec))
    if dist < 1e-9:
        return 0
    cos = DIRECTIONS @ (vec / dist)
    fast = dist > env.V_fast * env.cfg.dt
    order = np.argsort(-cos)
    for k in order:
        a = int(k) + (9 if fast else 1)
        if mask[a]:
            return a
        alt = int(k) + (1 if fast else 9)
        if mask[alt]:
            return alt
    return 0


def _in_range(env: UAVAoIEnv) -> np.ndarray:
    return np.linalg.norm(env.sensors - env.pos, axis=1) <= env.r_eff


class RandomPolicy:
    name = "random"

    def __init__(self, seed: int = 0):
        self.rng = np.random.default_rng(seed)

    def reset(self, env):
        pass

    def act(self, env: UAVAoIEnv) -> int:
        mask = env.action_masks()
        return int(self.rng.choice(np.flatnonzero(mask)))


class GreedyAoIPolicy:
    """Collect if a sensor in range is 'stale' (AoI >= rel_threshold x current max AoI and
    >= 2); otherwise fly to the out-of-range sensor maximising AoI / (distance + d0).
    The relative threshold prevents the policy from hovering forever over sensors it has
    just refreshed (an absolute threshold of 2 does exactly that)."""
    name = "greedy_aoi"

    def __init__(self, rel_threshold: float = 0.5, d0: float = 100.0):
        self.rel, self.d0 = rel_threshold, d0

    def reset(self, env):
        pass

    def act(self, env: UAVAoIEnv) -> int:
        mask = env.action_masks()
        inr = _in_range(env)
        th = max(2.0, self.rel * float(env.aoi.max()))
        if mask[0] and inr.any() and env.aoi[inr].max() >= th:
            return 0
        d = np.linalg.norm(env.sensors - env.pos, axis=1)
        score = env.aoi / (d + self.d0)
        score[inr] = -np.inf if (~inr).any() else score[inr]
        target = env.sensors[int(np.argmax(score))]
        return _move_towards(env, target, mask)


def _tour_length(pts: np.ndarray, order: list) -> float:
    p = pts[order]
    return float(np.linalg.norm(np.diff(np.vstack([p, p[:1]]), axis=0), axis=1).sum())


def tsp_tour(points: np.ndarray, start: np.ndarray, two_opt_iters: int = 50) -> list:
    """Nearest-neighbour tour from the sensor closest to `start`, improved by 2-opt
    (closed cycle, since collection repeats)."""
    n = len(points)
    if n <= 2:
        return list(range(n))
    cur = int(np.argmin(np.linalg.norm(points - start, axis=1)))
    unvisited = set(range(n)) - {cur}
    order = [cur]
    while unvisited:
        rest = np.array(sorted(unvisited))
        nxt = int(rest[np.argmin(np.linalg.norm(points[rest] - points[order[-1]], axis=1))])
        order.append(nxt)
        unvisited.remove(nxt)
    best = _tour_length(points, order)
    for _ in range(two_opt_iters):
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                cand = order[:i] + order[i:j + 1][::-1] + order[j + 1:]
                length = _tour_length(points, cand)
                if length + 1e-9 < best:
                    order, best, improved = cand, length, True
        if not improved:
            break
    return order


class TSPPolicy:
    """Cycle through a fixed TSP tour; at each waypoint hover once to collect."""
    name = "tsp"

    def reset(self, env: UAVAoIEnv):
        self.order = tsp_tour(env.sensors, env.pos)
        self.k = 0

    def act(self, env: UAVAoIEnv) -> int:
        mask = env.action_masks()
        target_idx = self.order[self.k % len(self.order)]
        target = env.sensors[target_idx]
        if np.linalg.norm(target - env.pos) <= env.r_eff and mask[0]:
            # env serves the max-AoI sensor in range; advance past every tour stop now fresh
            self.k += 1
            return 0
        return _move_towards(env, target, mask)


HEURISTICS = {"random": RandomPolicy, "greedy_aoi": GreedyAoIPolicy, "tsp": TSPPolicy}


def run_episode(env: UAVAoIEnv, policy, seed: int) -> dict:
    obs, info = env.reset(seed=seed)
    policy.reset(env)
    done = False
    total_r = 0.0
    while not done:
        a = policy.act(env)
        obs, r, term, trunc, info = env.step(a)
        total_r += r
        done = term or trunc
    m = dict(info["episode_metrics"])
    m["return"] = total_r
    return m
