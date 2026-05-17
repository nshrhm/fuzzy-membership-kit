"""Numerical diagnostics for warps, base functions, and memberships.

The helpers operate on the callable supplied by the caller.  If the callable is
a warp ``w``, anchor targets are warped-coordinate targets.  If the callable is
a composed membership ``mu(u)=h(w(u))``, anchor targets should be membership
targets such as ``h(0.5)`` and ``h(q)``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from .core import NumberOrArray


def _values(func: Callable[[ArrayLike], NumberOrArray], u: ArrayLike) -> np.ndarray:
    return np.asarray(func(u), dtype=float)


def numerical_derivative(func: Callable[[ArrayLike], NumberOrArray], grid: ArrayLike) -> np.ndarray:
    """Estimate the first derivative over ``grid`` using finite differences."""

    x = np.asarray(grid, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("grid must be a one-dimensional array with at least two points.")
    y = _values(func, x)
    edge_order = 2 if x.size >= 3 else 1
    return np.asarray(np.gradient(y, x, edge_order=edge_order), dtype=float)


def numerical_second_derivative(
    func: Callable[[ArrayLike], NumberOrArray], grid: ArrayLike
) -> np.ndarray:
    """Estimate the second derivative over ``grid`` using finite differences."""

    x = np.asarray(grid, dtype=float)
    if x.ndim != 1 or x.size < 3:
        raise ValueError("grid must be a one-dimensional array with at least three points.")
    first = numerical_derivative(func, x)
    return np.asarray(np.gradient(first, x, edge_order=2), dtype=float)


def local_discriminability(
    func: Callable[[ArrayLike], NumberOrArray], u: float, delta: float = 1.0
) -> float:
    """Return the local absolute finite-difference slope around ``u``.

    Larger values indicate that nearby universe values are more separated by
    the function.  This is a numerical diagnostic, not a formal derivative.
    """

    if delta <= 0.0 or not np.isfinite(delta):
        raise ValueError("delta must be positive and finite.")
    lo = float(np.asarray(func(u - delta)))
    hi = float(np.asarray(func(u + delta)))
    return abs(hi - lo) / (2.0 * delta)


def anchor_error(func: Callable[[ArrayLike], NumberOrArray], point: float, target: float) -> float:
    """Return ``abs(func(point) - target)`` for an anchor condition."""

    return abs(float(np.asarray(func(point))) - target)


def tail_compression_ratio(
    func: Callable[[ArrayLike], NumberOrArray],
    focus: float,
    far: float,
    delta: float = 1.0,
) -> float:
    """Compare local discriminability at the far anchor to the focus anchor.

    Values below 1 indicate that the function changes more slowly near
    ``far`` than near ``focus`` under the chosen finite-difference window.
    """

    focus_disc = local_discriminability(func, focus, delta=delta)
    far_disc = local_discriminability(func, far, delta=delta)
    if focus_disc == 0.0:
        return float("inf") if far_disc > 0.0 else 0.0
    return far_disc / focus_disc


def check_range(
    values: ArrayLike, lower: float = 0.0, upper: float = 1.0, atol: float = 1e-9
) -> bool:
    """Return whether all finite ``values`` lie in ``[lower, upper]``."""

    y = np.asarray(values, dtype=float)
    return bool(
        np.all(np.isfinite(y))
        and np.nanmin(y) >= lower - atol
        and np.nanmax(y) <= upper + atol
    )


def check_monotonicity(
    values: ArrayLike, direction: str = "increasing", atol: float = 1e-9
) -> bool:
    """Return whether ``values`` are monotone in the requested direction."""

    if direction not in {"increasing", "decreasing"}:
        raise ValueError("direction must be 'increasing' or 'decreasing'.")
    y = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(y)):
        return False
    diff = np.diff(y)
    if direction == "increasing":
        return bool(np.all(diff >= -atol))
    return bool(np.all(diff <= atol))


def summarize_diagnostics(
    func: Callable[[ArrayLike], NumberOrArray],
    grid: ArrayLike,
    focus: float | None = None,
    far: float | None = None,
    q: float | None = None,
    focus_target: float = 0.5,
    delta: float = 1.0,
    direction: str = "increasing",
) -> dict[str, Any]:
    """Summarize reviewer-facing numerical diagnostics for ``func``.

    The returned dictionary includes range and monotonicity checks, observed
    extrema, maximum absolute slope, and optional focus/far anchor diagnostics
    when the corresponding semantic anchors are provided.  The parameter ``q``
    is the far-anchor target for the function being diagnosed: use the warped
    coordinate target when diagnosing ``w`` and use ``h(q)`` when diagnosing a
    composed membership ``mu``.  ``focus_target`` follows the same convention;
    its default is 0.5.
    """

    x = np.asarray(grid, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("grid must be a one-dimensional array with at least two points.")
    y = _values(func, x)
    slope = numerical_derivative(func, x)
    summary: dict[str, Any] = {
        "range_ok": check_range(y),
        "monotone_ok": check_monotonicity(y, direction=direction),
        "min_value": float(np.nanmin(y)),
        "max_value": float(np.nanmax(y)),
        "max_abs_slope": float(np.nanmax(np.abs(slope))),
    }

    if focus is not None:
        summary["slope_at_focus"] = float(np.interp(focus, x, slope))
        summary["anchor_error_focus"] = anchor_error(func, focus, focus_target)
        summary["local_discriminability_focus"] = local_discriminability(
            func, focus, delta=delta
        )
    if far is not None:
        summary["slope_at_far"] = float(np.interp(far, x, slope))
        summary["local_discriminability_far"] = local_discriminability(func, far, delta=delta)
    if far is not None and q is not None:
        summary["anchor_error_far"] = anchor_error(func, far, q)
    if focus is not None and far is not None:
        summary["tail_compression_ratio"] = tail_compression_ratio(
            func, focus, far, delta=delta
        )
    return summary
