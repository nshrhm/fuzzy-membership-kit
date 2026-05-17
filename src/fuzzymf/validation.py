"""Small numerical checks for reviewer-facing validation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .core import NumberOrArray


@dataclass(frozen=True)
class RangeReport:
    minimum: float
    maximum: float
    inside_unit_interval: bool


@dataclass(frozen=True)
class MonotonicityReport:
    direction: str
    max_violation: float
    passed: bool


def range_report(func: Callable[[ArrayLike], NumberOrArray], grid: ArrayLike) -> RangeReport:
    y = np.asarray(func(grid), dtype=float)
    mn = float(np.nanmin(y))
    mx = float(np.nanmax(y))
    return RangeReport(mn, mx, bool(mn >= -1e-12 and mx <= 1.0 + 1e-12))


def monotonicity_report(
    func: Callable[[ArrayLike], NumberOrArray],
    grid: ArrayLike,
    direction: str = "increasing",
    tolerance: float = 1e-10,
) -> MonotonicityReport:
    if direction not in {"increasing", "decreasing"}:
        raise ValueError("direction must be 'increasing' or 'decreasing'.")
    y = np.asarray(func(grid), dtype=float)
    diff = np.diff(y)
    if direction == "increasing":
        violation = float(max(0.0, -np.min(diff))) if diff.size else 0.0
    else:
        violation = float(max(0.0, np.max(diff))) if diff.size else 0.0
    return MonotonicityReport(direction, violation, bool(violation <= tolerance))
