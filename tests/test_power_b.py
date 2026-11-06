"""Tests for scripts/power_b.py (W4-LDN-04).  python tests/test_power_b.py"""
from __future__ import annotations

import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "src"))

import power_b  # noqa: E402


def test_signflip_exact_extremes():
    signs = power_b.signflip_matrix(10)
    assert signs.shape == (1024, 10)
    d = np.array([[1.0] * 10])                       # all positive: only the identity flip is as large
    assert abs(power_b.signflip_p(d, signs)[0] - 1 / 1024) < 1e-12
    d0 = np.array([[1.0, -1.0] * 5])                  # mean 0: half of the null is >= 0
    assert power_b.signflip_p(d0, signs)[0] > 0.5


def test_signflip_size_under_null():
    rng = np.random.default_rng(1)
    signs = power_b.signflip_matrix(10)
    p = power_b.signflip_p(rng.normal(0, 1, (4000, 10)), signs)
    assert abs((p < 0.05).mean() - 0.05) < 0.015


def test_perm2_size_under_null():
    rng = np.random.default_rng(2)
    x, y = rng.normal(0, 1, (1000, 10)), rng.normal(0, 1, (1000, 10))
    p = power_b.perm2_p(x, y, 500, rng)
    assert abs((p < 0.05).mean() - 0.05) < 0.025


def test_power_at_delta_is_about_a_quarter_for_two_suites():
    """'significant AND estimate >= delta' on two suites: ~0.5 * 0.5 when the true effect is delta."""
    rng = np.random.default_rng(3)
    pw = power_b.power_h5(0.10, 0.02, 10, 0.10, 2000, rng)
    assert 0.18 < pw < 0.32, pw


def test_power_large_effect_and_null():
    rng = np.random.default_rng(4)
    assert power_b.power_h5(0.40, 0.05, 10, 0.10, 500, rng) > 0.99
    assert power_b.power_h5(0.00, 0.10, 10, 0.10, 500, rng) < 0.01
    assert power_b.power_h7(0.60, 0.10, 10, 0.10, 300, rng) > 0.99
    assert power_b.power_h6(1.00, 0.01, 10, 0.10, 100, rng) > 0.99
    assert power_b.power_h6(1.20, 0.01, 10, 0.10, 100, rng) < 0.01


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    bad = 0
    for f in fns:
        try:
            f()
            print(f"PASS {f.__name__}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"FAIL {f.__name__}: {e!r}")
    print(f"\n{len(fns) - bad}/{len(fns)} passed")
    sys.exit(1 if bad else 0)
