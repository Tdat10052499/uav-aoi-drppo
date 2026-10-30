"""UAV-assisted IoT data collection environment (single rotary-wing UAV, AoI + energy).

Design documented in docs/02_mo_hinh_he_thong.md. Gymnasium API (reset/step/action_masks).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Optional

import numpy as np

from ._compat import gym, spaces
from .channel import effective_radius
from .energy import PRESETS, RotorParams, characteristic_speeds, hover_power, propulsion_power
from .scenarios import ScenarioSpec, TRAIN_DR

# 8 compass directions (unit vectors), index 0 = East, counter-clockwise.
_ANG = np.arange(8) * (np.pi / 4.0)
DIRECTIONS = np.stack([np.cos(_ANG), np.sin(_ANG)], axis=1)
N_ACTIONS = 17  # 0 = hover+collect, 1..8 = dirs at V_me, 9..16 = dirs at V_mr


@dataclass
class EnvConfig:
    T: int = 300                  # decision slots per episode
    dt: float = 3.0               # slot length [s]
    H: float = 100.0              # flight altitude [m]
    B: float = 1e6                # bandwidth [Hz]
    gamma0_db: float = 60.0       # reference SNR at 1 m [dB]
    packet_bits: float = 15e6     # status packet size [bit]
    Pc: float = 50.0              # communication power [W]
    rotor_preset: str = "zeng2019_arxiv_v1"
    G: int = 16                   # grid cells per side (observation)
    lam: float = 0.1              # energy weight in reward
    mu: float = 0.1               # boundary penalty
    count_norm: float = 3.0       # sensor-count channel normalisation
    use_action_mask_clip: bool = True  # if False, out-of-area moves are clipped + penalised
    single_speed: bool = False    # ablation A5: only V_me moves (actions 9..16 always masked)

    def to_dict(self) -> dict:
        return asdict(self)


class UAVAoIEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, scenario: Optional[ScenarioSpec] = None, cfg: Optional[EnvConfig] = None):
        self.cfg = cfg or EnvConfig()
        self.scenario = scenario or TRAIN_DR
        self.rotor: RotorParams = PRESETS[self.cfg.rotor_preset]
        sp = characteristic_speeds(self.rotor)
        self.V_slow, self.V_fast = sp["V_me"], sp["V_mr"]
        self.P_hover = hover_power(self.rotor)
        self.P_slow = propulsion_power(self.V_slow, self.rotor)
        self.P_fast = propulsion_power(self.V_fast, self.rotor)
        # Energy per action [J]
        self.E_move = np.array([self.P_slow] * 8 + [self.P_fast] * 8) * self.cfg.dt
        self.E_hover_tx = (self.P_hover + self.cfg.Pc) * self.cfg.dt
        self.E_min_action = float(min(self.E_move.min(), self.E_hover_tx))
        self.rho_max = max(self.P_hover + self.cfg.Pc, self.P_slow, self.P_fast) / self.P_hover
        # Upper bound of the cost any single slot can incur (AoI term <= 1, energy, boundary).
        self.worst_step_cost = 1.0 + self.cfg.lam * self.rho_max + self.cfg.mu
        self.r_eff = effective_radius(self.cfg.packet_bits, self.cfg.dt, self.cfg.H, self.cfg.B,
                                      self.cfg.gamma0_db)
        if self.r_eff < 0:
            raise ValueError("packet cannot be delivered within one slot even directly overhead")
        self.Delta_max = float(self.cfg.T)
        M = 2 * self.cfg.G - 1
        self.observation_space = spaces.Box(low=0.0, high=np.inf, shape=(5, M, M), dtype=np.float32)
        self.action_space = spaces.Discrete(N_ACTIONS)
        self._scn = None

    # ------------------------------------------------------------------ API
    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        options = options or {}
        self._scn = options.get("scenario") or self.scenario.sample(self.np_random)
        self.L = float(self._scn["L"])
        self.sensors = np.asarray(self._scn["sensors"], dtype=float)
        self.N = len(self.sensors)
        self.E_max = float(self._scn["E_max"])
        self.energy = self.E_max
        self.pos = np.asarray(self._scn["start"], dtype=float).copy()
        self.aoi = np.ones(self.N, dtype=float)
        self.t = 0
        self.aoi_sum = 0.0          # sum over elapsed slots of mean AoI
        self.peak_aoi = 1.0
        self.n_served = np.zeros(self.N, dtype=int)
        self.action_counts = np.zeros(3, dtype=int)  # hover, slow, fast
        self.boundary_hits = 0
        self.energy_used = 0.0
        self.early_terminated = False
        return self._obs(), self._info()

    def action_masks(self) -> np.ndarray:
        mask = np.ones(N_ACTIONS, dtype=bool)
        for a in range(1, N_ACTIONS):
            step = self._step_len(a)
            nxt = self.pos + DIRECTIONS[(a - 1) % 8] * step
            if np.any(nxt < 0.0) or np.any(nxt > self.L):
                mask[a] = False
            if self.E_move[a - 1] > self.energy:
                mask[a] = False
            if self.cfg.single_speed and a > 8:
                mask[a] = False
        if self.E_hover_tx > self.energy:
            mask[0] = False
        if not mask.any():
            mask[0] = True  # keep at least one action valid; episode will terminate
        return mask

    def step(self, action: int):
        a = int(action)
        cfg = self.cfg
        served = -1
        penalty = 0.0
        if cfg.single_speed and a > 8:
            raise ValueError(f"action {a} uses V_mr but single_speed=True (ablation A5); "
                             "the policy must respect action_masks()")
        # --- energy feasibility: not enough energy for the chosen action -> terminate
        e_needed = self.E_hover_tx if a == 0 else self.E_move[a - 1]
        if e_needed > self.energy:
            return self._terminate_early(extra_slots=cfg.T - self.t)

        if a == 0:
            self.action_counts[0] += 1
            d = np.linalg.norm(self.sensors - self.pos, axis=1)
            feas = np.flatnonzero(d <= self.r_eff)
            if feas.size:
                served = int(feas[np.argmax(self.aoi[feas])])
                e = self.E_hover_tx
            else:
                e = self.P_hover * cfg.dt   # hovering without transmission
        else:
            self.action_counts[1 if a <= 8 else 2] += 1
            nxt = self.pos + DIRECTIONS[(a - 1) % 8] * self._step_len(a)
            if np.any(nxt < 0.0) or np.any(nxt > self.L):
                self.boundary_hits += 1
                penalty = cfg.mu
                nxt = np.clip(nxt, 0.0, self.L)
            self.pos = nxt
            e = self.E_move[a - 1]

        self.energy -= e
        self.energy_used += e
        # AoI update (docs/02 section 5)
        self.aoi = np.minimum(self.aoi + 1.0, self.Delta_max)
        if served >= 0:
            self.aoi[served] = 1.0
            self.n_served[served] += 1
        mean_aoi = float(self.aoi.mean())
        self.aoi_sum += mean_aoi
        self.peak_aoi = max(self.peak_aoi, float(self.aoi.max()))
        self.t += 1

        reward = -mean_aoi / self.Delta_max - cfg.lam * e / (self.P_hover * cfg.dt) - penalty
        truncated = self.t >= cfg.T
        terminated = False
        if not truncated and self.energy < self.E_min_action:
            # cannot act any more: account for the remaining slots (anti reward-hacking)
            obs, r_extra, terminated, _, info = self._terminate_early(extra_slots=cfg.T - self.t)
            return obs, reward + r_extra, terminated, False, info
        info = self._info(final=truncated)
        return self._obs(), float(reward), terminated, truncated, info

    # ------------------------------------------------------------ helpers
    def _step_len(self, a: int) -> float:
        return (self.V_slow if a <= 8 else self.V_fast) * self.cfg.dt

    def _terminate_early(self, extra_slots: int):
        """Battery exhausted: no more collection. AoI keeps growing for the rest of
        the horizon (used for the metric); the reward gets a penalty that upper-bounds
        any cost the remaining slots could have incurred, so dying early never pays."""
        k = np.arange(1, extra_slots + 1, dtype=float)[:, None]
        future = np.minimum(self.aoi[None, :] + k, self.Delta_max).mean(axis=1) if extra_slots > 0 else np.zeros(0)
        self.aoi_sum += float(future.sum())
        if future.size:
            self.peak_aoi = max(self.peak_aoi, float(np.minimum(self.aoi.max() + extra_slots, self.Delta_max)))
        r_extra = -float(extra_slots) * self.worst_step_cost
        self.early_terminated = True
        self.t = self.cfg.T
        info = self._info(final=True, early=True)
        return self._obs(), r_extra, True, False, info

    def _obs(self) -> np.ndarray:
        G = self.cfg.G
        M = 2 * G - 1
        cell = self.L / G
        idx = np.clip((self.sensors // cell).astype(int), 0, G - 1)
        aoi_map = np.zeros((G, G), dtype=np.float32)
        cnt_map = np.zeros((G, G), dtype=np.float32)
        np.add.at(aoi_map, (idx[:, 0], idx[:, 1]), self.aoi / self.Delta_max)
        np.add.at(cnt_map, (idx[:, 0], idx[:, 1]), 1.0 / self.cfg.count_norm)
        ux, uy = np.clip((self.pos // cell).astype(int), 0, G - 1)
        obs = np.zeros((5, M, M), dtype=np.float32)
        obs[2, :, :] = 1.0  # outside mask; inside region cleared below
        ox, oy = G - 1 - ux, G - 1 - uy
        obs[0, ox:ox + G, oy:oy + G] = aoi_map
        obs[1, ox:ox + G, oy:oy + G] = cnt_map
        obs[2, ox:ox + G, oy:oy + G] = 0.0
        obs[3, :, :] = max(self.energy, 0.0) / self.E_max
        obs[4, :, :] = (self.cfg.T - self.t) / self.cfg.T
        return obs

    def _info(self, final: bool = False, early: bool = False) -> dict:
        info = {"t": self.t, "energy": self.energy, "mean_aoi_now": float(self.aoi.mean())}
        if final:
            T = self.cfg.T
            info["episode_metrics"] = {
                "mean_aoi": self.aoi_sum / T,                  # time- and sensor-averaged AoI [slots]
                "peak_aoi": self.peak_aoi,
                "energy_used_J": self.energy_used,
                "energy_frac": self.energy_used / self.E_max,
                "collections": int(self.n_served.sum()),
                "coverage": float((self.n_served > 0).mean()),  # share of sensors served at least once
                "hover_frac": float(self.action_counts[0] / max(1, self.action_counts.sum())),
                "slow_frac": float(self.action_counts[1] / max(1, self.action_counts.sum())),
                "fast_frac": float(self.action_counts[2] / max(1, self.action_counts.sum())),
                "boundary_hits": self.boundary_hits,
                "early_termination": bool(early),
                "N": self.N, "L": self.L, "E_max": self.E_max,
            }
        return info
