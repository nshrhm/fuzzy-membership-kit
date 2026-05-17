"""Core membership-function definitions.

The functions in this module are intentionally small and explicit.  They are
suitable both for numerical use and for checking against the formulae reported
in a paper.  All public functions accept scalars, lists, or NumPy arrays.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

NumberOrArray = float | np.ndarray


def _array(u: ArrayLike) -> np.ndarray:
    """Return *u* as a floating NumPy array without modifying the input."""

    return np.asarray(u, dtype=float)


def _return_like_input(original: ArrayLike, value: np.ndarray) -> NumberOrArray:
    """Return a Python float for scalar input and an ndarray otherwise."""

    if np.isscalar(original):
        return float(np.asarray(value))
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_open_interval(value: float, name: str, lower: float = 0.0, upper: float = 1.0) -> None:
    _require(lower < value < upper, f"{name} must satisfy {lower} < {name} < {upper}.")


def _logit(p: float) -> float:
    _require_open_interval(p, "p")
    return float(np.log(p / (1.0 - p)))


def triangular(u: ArrayLike, a: float, b: float, c: float) -> NumberOrArray:
    """Triangular membership function.

    Parameters
    ----------
    u:
        Universe-of-discourse value(s).
    a, b, c:
        Breakpoints satisfying ``a < b < c``.  The membership value is 0 at
        and below ``a``, 1 at ``b``, and 0 at and above ``c``.
    """

    _require(a < b < c, "triangular requires a < b < c.")
    x = _array(u)
    y = np.zeros_like(x, dtype=float)
    rising = (a < x) & (x <= b)
    falling = (b < x) & (x < c)
    y[rising] = (x[rising] - a) / (b - a)
    y[falling] = 1.0 - (x[falling] - b) / (c - b)
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def trapezoid_rising(u: ArrayLike, c: float, d: float) -> NumberOrArray:
    """Rising trapezoidal shoulder: 0, linear increase, then 1."""

    _require(c < d, "trapezoid_rising requires c < d.")
    x = _array(u)
    y = np.empty_like(x, dtype=float)
    y[x <= c] = 0.0
    middle = (c < x) & (x <= d)
    y[middle] = (x[middle] - c) / (d - c)
    y[d < x] = 1.0
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def trapezoid_falling(u: ArrayLike, a: float, b: float) -> NumberOrArray:
    """Falling trapezoidal shoulder: 1, linear decrease, then 0."""

    return _return_like_input(u, 1.0 - _array(trapezoid_rising(u, a, b)))


def trapezoid_pi(u: ArrayLike, a: float, b: float, c: float, d: float) -> NumberOrArray:
    """Trapezoidal pi membership with plateau between ``b`` and ``c``."""

    _require(a < b <= c < d, "trapezoid_pi requires a < b <= c < d.")
    x = _array(u)
    y = np.zeros_like(x, dtype=float)
    rising = (a < x) & (x <= b)
    plateau = (b < x) & (x <= c)
    falling = (c < x) & (x < d)
    y[rising] = (x[rising] - a) / (b - a)
    y[plateau] = 1.0
    y[falling] = 1.0 - (x[falling] - c) / (d - c)
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def gaussian(u: ArrayLike, center: float, sigma: float) -> NumberOrArray:
    """Gaussian membership function with peak 1 at ``center``.

    Unlike a normal probability density, this function is not normalized by an
    integration constant because a membership function is not a probability
    density.
    """

    _require(sigma > 0.0, "sigma must be positive.")
    x = _array(u)
    y = np.exp(-((x - center) ** 2) / (2.0 * sigma**2))
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def s_curve(u: ArrayLike, left: float, right: float) -> NumberOrArray:
    """Zadeh-style S membership function, a C1 quadratic spline.

    ``left`` is the point where membership starts increasing from 0.
    ``right`` is the point where membership reaches 1.
    The midpoint ``(left + right) / 2`` has membership 0.5.
    """

    _require(left < right, "s_curve requires left < right.")
    x = _array(u)
    y = np.empty_like(x, dtype=float)
    width = right - left
    mid = (left + right) / 2.0

    y[x <= left] = 0.0
    first = (left < x) & (x <= mid)
    y[first] = 2.0 * ((x[first] - left) / width) ** 2
    second = (mid < x) & (x <= right)
    y[second] = 1.0 - 2.0 * ((x[second] - right) / width) ** 2
    y[right < x] = 1.0
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def z_curve(u: ArrayLike, left: float, right: float) -> NumberOrArray:
    """Z membership function, defined as ``1 - s_curve``."""

    return _return_like_input(u, 1.0 - _array(s_curve(u, left, right)))


def pi_curve(u: ArrayLike, a: float, b: float, c: float, d: float) -> NumberOrArray:
    """Smooth pi membership using S on the left and Z on the right.

    The function rises from 0 to 1 over ``[a, b]``, remains 1 over
    ``[b, c]``, and falls from 1 to 0 over ``[c, d]``.
    """

    _require(a < b <= c < d, "pi_curve requires a < b <= c < d.")
    x = _array(u)
    y = np.where(x <= c, _array(s_curve(x, a, b)), _array(z_curve(x, c, d)))
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def sigmoid(u: ArrayLike, gain: float, center: float) -> NumberOrArray:
    """Numerically stable logistic sigmoid.

    The value is 0.5 at ``center``.  Positive ``gain`` gives an increasing
    curve; negative ``gain`` gives a decreasing curve.
    """

    x = _array(u)
    z = gain * (x - center)
    y = np.empty_like(z, dtype=float)
    pos = z >= 0.0
    y[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    exp_z = np.exp(z[~pos])
    y[~pos] = exp_z / (1.0 + exp_z)
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def sigmoid_gain_from_quantile(focus: float, far: float, quantile: float = 0.9) -> float:
    """Return gain ``a`` such that ``sigmoid(far; a, focus) = quantile``.

    This implements

    ``a = log(quantile / (1 - quantile)) / (far - focus)``.

    For an increasing membership definition, ``far`` is normally greater than
    ``focus`` and ``quantile`` is normally greater than 0.5.
    """

    _require_open_interval(quantile, "quantile")
    _require(far != focus, "far must differ from focus.")
    return _logit(quantile) / (far - focus)


def compressed_s(
    u: ArrayLike,
    focus: float,
    far: float,
    upper_q: float = 0.9,
    lower_q: float | None = None,
) -> NumberOrArray:
    """Sigmoid-composed S membership for an increasing concept.

    This function first compresses the universe value ``u`` by a sigmoid
    ``f(u; gain, focus)`` and then applies a Zadeh S function on the compressed
    axis.  By default, ``lower_q = 1 - upper_q``.

    Semantics for the default symmetric setting:
    - membership is 0.5 at ``focus``;
    - membership reaches 1.0 at ``far``;
    - membership reaches 0.0 at the symmetric lower point implied by the
      sigmoid quantiles.
    """

    _require_open_interval(upper_q, "upper_q")
    if lower_q is None:
        lower_q = 1.0 - upper_q
    _require_open_interval(lower_q, "lower_q")
    _require(lower_q < 0.5 < upper_q, "compressed_s requires lower_q < 0.5 < upper_q.")
    gain = sigmoid_gain_from_quantile(focus=focus, far=far, quantile=upper_q)
    compressed = _array(sigmoid(u, gain=gain, center=focus))
    y = _array(s_curve(compressed, left=lower_q, right=upper_q))
    return _return_like_input(u, y)


def compressed_z(
    u: ArrayLike,
    focus: float,
    far: float,
    upper_q: float = 0.9,
    lower_q: float | None = None,
) -> NumberOrArray:
    """Sigmoid-composed Z membership for a decreasing concept.

    Semantics for the default symmetric setting:
    - membership is 0.5 at ``focus``;
    - membership reaches 0.0 at ``far`` when ``far > focus``;
    - membership reaches 1.0 at the symmetric lower point implied by the
      sigmoid quantiles.
    """

    _require_open_interval(upper_q, "upper_q")
    if lower_q is None:
        lower_q = 1.0 - upper_q
    _require_open_interval(lower_q, "lower_q")
    _require(lower_q < 0.5 < upper_q, "compressed_z requires lower_q < 0.5 < upper_q.")
    gain = sigmoid_gain_from_quantile(focus=focus, far=far, quantile=upper_q)
    compressed = _array(sigmoid(u, gain=gain, center=focus))
    y = _array(z_curve(compressed, left=lower_q, right=upper_q))
    return _return_like_input(u, y)


def compressed_pi(
    u: ArrayLike,
    left_focus: float,
    left_far: float,
    right_focus: float,
    right_far: float,
    upper_q: float = 0.9,
    lower_q: float | None = None,
) -> NumberOrArray:
    """Two-sided sigmoid-composed pi membership.

    The function is the minimum of a rising compressed S side and a falling
    compressed Z side.  This parameterization is useful when a concept should
    be fully compatible over a central region but become less distinguishable
    as values move farther away on either side.

    Parameters
    ----------
    left_focus:
        0.5 point of the rising side.
    left_far:
        point where the rising side reaches 1.0.
    right_focus:
        0.5 point of the falling side.
    right_far:
        point where the falling side reaches 0.0.
    """

    _require(left_focus < left_far, "left_focus must be smaller than left_far.")
    _require(right_focus < right_far, "right_focus must be smaller than right_far.")
    _require(left_focus <= right_focus, "left_focus must be <= right_focus.")
    rising = _array(compressed_s(u, left_focus, left_far, upper_q, lower_q))
    falling = _array(compressed_z(u, right_focus, right_far, upper_q, lower_q))
    return _return_like_input(u, np.minimum(rising, falling))


MembershipCallable = Callable[..., NumberOrArray]


FUNCTIONS: dict[str, MembershipCallable] = {
    "triangular": triangular,
    "trapezoid_rising": trapezoid_rising,
    "trapezoid_falling": trapezoid_falling,
    "trapezoid_pi": trapezoid_pi,
    "gaussian": gaussian,
    "s_curve": s_curve,
    "z_curve": z_curve,
    "pi_curve": pi_curve,
    "sigmoid": sigmoid,
    "compressed_s": compressed_s,
    "compressed_z": compressed_z,
    "compressed_pi": compressed_pi,
}


@dataclass(frozen=True)
class MembershipSpec:
    """Serializable membership-function specification.

    This class is intentionally lightweight so that it can be stored in JSON,
    YAML, CSV-derived metadata, or experiment manifests.
    """

    name: str
    kind: str
    params: Mapping[str, Any]
    description: str = ""

    def __post_init__(self) -> None:
        _require(self.kind in FUNCTIONS, f"Unknown membership kind: {self.kind!r}.")

    def __call__(self, u: ArrayLike) -> NumberOrArray:
        return FUNCTIONS[self.kind](u, **dict(self.params))

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "params": dict(self.params),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MembershipSpec:
        return cls(
            name=str(data["name"]),
            kind=str(data["kind"]),
            params=dict(data.get("params", {})),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True)
class MembershipCollection:
    """Named collection of membership specifications."""

    memberships: tuple[MembershipSpec, ...]
    universe: Mapping[str, Any] | None = None
    metadata: Mapping[str, Any] | None = None

    def evaluate(self, u: ArrayLike) -> dict[str, NumberOrArray]:
        return {spec.name: spec(u) for spec in self.memberships}

    def to_dict(self) -> dict[str, Any]:
        return {
            "universe": dict(self.universe or {}),
            "metadata": dict(self.metadata or {}),
            "memberships": [spec.to_dict() for spec in self.memberships],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MembershipCollection:
        specs = tuple(MembershipSpec.from_dict(item) for item in data.get("memberships", []))
        return cls(
            memberships=specs,
            universe=dict(data.get("universe", {})),
            metadata=dict(data.get("metadata", {})),
        )
