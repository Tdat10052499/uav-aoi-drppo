"""Rotary-wing UAV propulsion power model.

Source: Y. Zeng, J. Xu, R. Zhang, "Energy Minimization for Wireless Communication
with Rotary-Wing UAV", arXiv:1804.02238v1 (IEEE TWC 2019), Eq. (6) and Eq. (61);
default physical parameters = Table I of arXiv v1.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import numpy as np


@dataclass(frozen=True)
class RotorParams:
    W: float = 100.0      # aircraft weight [N]
    rho: float = 1.225    # air density [kg/m^3]
    R: float = 0.5        # rotor radius [m]
    A: float = 0.79       # rotor disc area [m^2]
    Omega: float = 400.0  # blade angular velocity [rad/s]
    s: float = 0.05       # rotor solidity
    d0: float = 0.3       # fuselage drag ratio
    k: float = 0.1        # incremental correction factor to induced power
    delta: float = 0.012  # profile drag coefficient

    @property
    def U_tip(self) -> float:
        return self.Omega * self.R

    @property
    def P0(self) -> float:
        """Blade profile power in hover, Eq. (61)."""
        return self.delta / 8.0 * self.rho * self.s * self.A * self.Omega ** 3 * self.R ** 3

    @property
    def Pi(self) -> float:
        """Induced power in hover, Eq. (61)."""
        return (1.0 + self.k) * self.W ** 1.5 / math.sqrt(2.0 * self.rho * self.A)

    @property
    def v0(self) -> float:
        """Mean rotor induced velocity in hover."""
        return math.sqrt(self.W / (2.0 * self.rho * self.A))


PRESETS = {
    # Table I of arXiv:1804.02238v1 (verified).
    "zeng2019_arxiv_v1": RotorParams(),
}


def propulsion_power(V, p: RotorParams = PRESETS["zeng2019_arxiv_v1"]):
    """Propulsion power P(V) [W] for horizontal speed V [m/s], Eq. (6)."""
    V = np.asarray(V, dtype=float)
    blade = p.P0 * (1.0 + 3.0 * V ** 2 / p.U_tip ** 2)
    induced = p.Pi * np.sqrt(np.sqrt(1.0 + V ** 4 / (4.0 * p.v0 ** 4)) - V ** 2 / (2.0 * p.v0 ** 2))
    parasite = 0.5 * p.d0 * p.rho * p.s * p.A * V ** 3
    out = blade + induced + parasite
    return float(out) if out.ndim == 0 else out


def hover_power(p: RotorParams = PRESETS["zeng2019_arxiv_v1"]) -> float:
    return p.P0 + p.Pi


def characteristic_speeds(p: RotorParams = PRESETS["zeng2019_arxiv_v1"], v_max: float = 60.0,
                          n: int = 60001) -> dict:
    """Numerically find the maximum-endurance speed V_me = argmin P(V) and the
    maximum-range speed V_mr = argmin P(V)/V (both defined in Sec. II-B of Zeng et al.)."""
    V = np.linspace(0.0, v_max, n)
    P = propulsion_power(V, p)
    i_me = int(np.argmin(P))
    ratio = P[1:] / V[1:]
    i_mr = int(np.argmin(ratio)) + 1
    return {"V_me": float(V[i_me]), "P_me": float(P[i_me]),
            "V_mr": float(V[i_mr]), "P_mr": float(P[i_mr]),
            "P_hover": hover_power(p)}
