"""Statistics for RL evaluation (NumPy only; SciPy used if available).

Unit of analysis = one *training seed* (mean over its evaluation episodes), as
recommended by Agarwal et al., "Deep RL at the Edge of the Statistical Precipice"
(NeurIPS 2021). Episodes of the same seed are not independent replicates.
"""
from __future__ import annotations

from typing import Callable, Sequence

import numpy as np


def iqm(x) -> float:
    """Interquartile mean: mean of the middle 50% of values."""
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    lo, hi = int(np.floor(0.25 * n)), int(np.ceil(0.75 * n))
    return float(x[lo:hi].mean()) if hi > lo else float(x.mean())


def bootstrap_ci(x, stat: Callable = np.mean, n_boot: int = 10_000, alpha: float = 0.05,
                 seed: int = 0) -> tuple:
    """Percentile bootstrap CI. Returns (point, low, high)."""
    x = np.asarray(x, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    boots = np.array([stat(x[i]) for i in idx])
    return float(stat(x)), float(np.quantile(boots, alpha / 2)), float(np.quantile(boots, 1 - alpha / 2))


def permutation_test(x, y, alternative: str = "less", n_perm: int = 20_000, seed: int = 0) -> float:
    """Two-sample permutation test on the difference of means (x - y).
    alternative: 'less' (H1: mean x < mean y), 'greater', or 'two-sided'."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    obs = x.mean() - y.mean()
    pooled = np.concatenate([x, y])
    rng = np.random.default_rng(seed)
    nx = len(x)
    diffs = np.empty(n_perm)
    for i in range(n_perm):
        p = rng.permutation(pooled)
        diffs[i] = p[:nx].mean() - p[nx:].mean()
    if alternative == "less":
        count = np.sum(diffs <= obs)
    elif alternative == "greater":
        count = np.sum(diffs >= obs)
    else:
        count = np.sum(np.abs(diffs) >= abs(obs))
    return float((count + 1) / (n_perm + 1))


def cliffs_delta(x, y) -> float:
    """P(X > Y) - P(X < Y); |d| < 0.147 negligible, < 0.33 small, < 0.474 medium, else large
    (Romano et al. thresholds, commonly used)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    gt = (x[:, None] > y[None, :]).sum()
    lt = (x[:, None] < y[None, :]).sum()
    return float((gt - lt) / (len(x) * len(y)))


def holm(pvalues: Sequence[float]) -> list:
    """Holm-Bonferroni adjusted p-values (same order as input)."""
    p = np.asarray(pvalues, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj.tolist()


def welch_t(x, y, alternative: str = "two-sided"):
    """Welch t-test via SciPy if installed, else None."""
    try:
        from scipy import stats as st
    except ImportError:
        return None
    return float(st.ttest_ind(x, y, equal_var=False, alternative=alternative).pvalue)


def ood_degradation(metric_ood, metric_id) -> np.ndarray:
    """Relative degradation per training seed: (OOD - ID) / ID. For AoI, higher = worse."""
    a, b = np.asarray(metric_ood, float), np.asarray(metric_id, float)
    return (a - b) / b
