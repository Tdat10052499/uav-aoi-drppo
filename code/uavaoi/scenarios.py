"""Scenario samplers: in-distribution (training) and structured OOD suites.

A scenario sample is a dict with keys:
  L        side length of the square area [m]
  sensors  (N, 2) array of sensor positions [m]
  E_max    onboard energy budget [J]
  start    (2,) UAV start position [m]
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Callable, Optional, Tuple

import numpy as np


def uniform_layout(rng: np.random.Generator, n: int, L: float) -> np.ndarray:
    return rng.uniform(0.0, L, size=(n, 2))


def clustered_layout(rng: np.random.Generator, n: int, L: float,
                     n_clusters: Tuple[int, int] = (2, 4), sigma: float = 80.0) -> np.ndarray:
    """Gaussian clusters; centres kept 1.5 sigma away from the border."""
    k = int(rng.integers(n_clusters[0], n_clusters[1] + 1))
    margin = 1.5 * sigma
    centres = rng.uniform(margin, L - margin, size=(k, 2))
    labels = rng.integers(0, k, size=n)
    pts = centres[labels] + rng.normal(0.0, sigma, size=(n, 2))
    return np.clip(pts, 0.0, L)


@dataclass
class ScenarioSpec:
    """Distribution over scenarios. Ranges are inclusive."""
    name: str = "id"
    layout: str = "uniform"                 # "uniform" | "clustered"
    n_range: Tuple[int, int] = (10, 30)
    n_choices: Optional[Tuple[int, ...]] = None  # overrides n_range if given
    L: float = 1000.0
    E_range: Tuple[float, float] = (0.8e6, 1.2e6)
    random_start: bool = True
    fixed_seed: Optional[int] = None        # if set, every reset returns the same scenario

    def sample(self, rng: np.random.Generator) -> dict:
        if self.fixed_seed is not None:
            rng = np.random.default_rng(self.fixed_seed)
        if self.n_choices:
            n = int(rng.choice(self.n_choices))
        else:
            n = int(rng.integers(self.n_range[0], self.n_range[1] + 1))
        if self.layout == "uniform":
            sensors = uniform_layout(rng, n, self.L)
        elif self.layout == "clustered":
            sensors = clustered_layout(rng, n, self.L)
        else:
            raise ValueError(f"unknown layout {self.layout}")
        E = float(rng.uniform(*self.E_range))
        start = rng.uniform(0.0, self.L, size=2) if self.random_start else np.array([self.L / 2, self.L / 2])
        return {"L": self.L, "sensors": sensors, "E_max": E, "start": start}

    def to_dict(self) -> dict:
        return asdict(self)


# ---- Canonical suites (see docs/03, section 4) --------------------------------
TRAIN_DR = ScenarioSpec(name="train_dr")
# PPO-fixed baseline: a single uniform layout with N=20, E=1.0 MJ, fixed start.
TRAIN_FIXED = ScenarioSpec(name="train_fixed", n_choices=(20,), E_range=(1.0e6, 1.0e6),
                           random_start=False, fixed_seed=0)

SUITES = {
    "id": ScenarioSpec(name="id"),
    "ood_cluster": ScenarioSpec(name="ood_cluster", layout="clustered"),
    "ood_density": ScenarioSpec(name="ood_density", n_choices=(40, 50)),
    "ood_area": ScenarioSpec(name="ood_area", L=1500.0),
    "ood_energy": ScenarioSpec(name="ood_energy", E_range=(0.5e6, 0.7e6)),
}

# Evaluation episode seeds are disjoint from any training seed range.
EVAL_SEED_BASE = 100_000


def eval_seeds(n_episodes: int = 100) -> list:
    return [EVAL_SEED_BASE + i for i in range(n_episodes)]
