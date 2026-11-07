"""Feature extractors live in an importable module, so models pickle them by reference.
Run with `python tests/test_nets.py`; skipped when torch / SB3 are not installed."""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))


def main() -> int:
    try:
        import cloudpickle  # noqa: F401
        import torch  # noqa: F401
        import stable_baselines3  # noqa: F401
    except ImportError as e:
        print(f"SKIP test_nets: {e}")
        return 0
    import cloudpickle
    from uavaoi import nets
    import train_ppo
    failed = 0
    for name in ("SmallCNN", "MapCandExtractor"):
        cls = getattr(nets, name)
        checks = {
            "module is uavaoi.nets": cls.__module__ == "uavaoi.nets",
            "train_ppo re-exports the same class": getattr(train_ppo, name) is cls,
            # by reference: the pickle names the class instead of embedding its bytecode
            "pickled by reference": b"uavaoi.nets" in cloudpickle.dumps(cls) and len(cloudpickle.dumps(cls)) < 200,
        }
        for k, ok in checks.items():
            print(f"{'PASS' if ok else 'FAIL'} {name}: {k}")
            failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
