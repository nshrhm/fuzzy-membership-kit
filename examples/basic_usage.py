from __future__ import annotations

import numpy as np

from fuzzymf import compressed_s, s_curve

u = np.array([0, 25, 50, 75, 90, 100], dtype=float)
print("standard S:", s_curve(u, left=20, right=80))
print("compressed S:", compressed_s(u, focus=50, far=90, upper_q=0.9))
