from __future__ import annotations

from pathlib import Path

import numpy as np

from fuzzymf import load_collection

config = Path(__file__).parent / "configs" / "emotion_vas_0_100.yaml"
collection = load_collection(config)
u = np.array([0, 25, 50, 75, 100], dtype=float)

for name, values in collection.evaluate(u).items():
    print(name, values)
