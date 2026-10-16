"""Use Gymnasium when installed; otherwise fall back to a minimal shim so the
environment, heuristics, tests and statistics run with NumPy only."""
from __future__ import annotations

import numpy as np

try:  # pragma: no cover - exercised only when gymnasium is installed
    import gymnasium as gym
    from gymnasium import spaces
    HAS_GYM = True
except ImportError:  # minimal stand-ins with the same attributes we use
    HAS_GYM = False

    class _Box:
        def __init__(self, low, high, shape, dtype=np.float32):
            self.low, self.high, self.shape, self.dtype = low, high, tuple(shape), dtype

        def contains(self, x) -> bool:
            x = np.asarray(x)
            return x.shape == self.shape and bool(np.all(x >= self.low) and np.all(x <= self.high))

    class _Discrete:
        def __init__(self, n: int):
            self.n = int(n)
            self.shape = ()

        def contains(self, x) -> bool:
            return 0 <= int(x) < self.n

    class spaces:  # noqa: N801 - mimic module namespace
        Box = _Box
        Discrete = _Discrete

    class _Env:
        metadata: dict = {}
        np_random = None

        def reset(self, *, seed=None, options=None):
            if seed is not None or self.np_random is None:
                self.np_random = np.random.default_rng(seed)

        @property
        def unwrapped(self):
            return self

    class gym:  # noqa: N801
        Env = _Env
