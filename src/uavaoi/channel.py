"""LoS air-to-ground channel and achievable rate.

Source: Zeng, Xu, Zhang (arXiv:1804.02238), Eq. (1)-(2): free-space LoS channel,
R = B log2(1 + gamma0 / (H^2 + d^2)). Default numbers from Sec. V of that paper:
H = 100 m, B = 1 MHz, gamma0 = 60 dB.
"""
from __future__ import annotations

import math

import numpy as np


def db_to_lin(x_db: float) -> float:
    return 10.0 ** (x_db / 10.0)


def rate_bps(d_horizontal, H: float = 100.0, B: float = 1e6, gamma0_db: float = 60.0):
    """Achievable rate [bit/s] at horizontal distance d [m]."""
    g0 = db_to_lin(gamma0_db)
    d = np.asarray(d_horizontal, dtype=float)
    return B * np.log2(1.0 + g0 / (H ** 2 + d ** 2))


def effective_radius(packet_bits: float, slot_s: float, H: float = 100.0, B: float = 1e6,
                     gamma0_db: float = 60.0) -> float:
    """Largest horizontal distance at which one packet of `packet_bits` can be
    uploaded within one slot (rate * slot >= packet). Returns -1 if impossible
    even directly above the sensor."""
    g0 = db_to_lin(gamma0_db)
    snr_req = 2.0 ** (packet_bits / (B * slot_s)) - 1.0
    d2 = g0 / snr_req - H ** 2
    return math.sqrt(d2) if d2 >= 0 else -1.0
