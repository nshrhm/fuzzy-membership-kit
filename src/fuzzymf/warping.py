"""Anchored universe-of-discourse warping functions.

Each public function maps universe values ``u`` to the unit interval and is
parameterized by a focus anchor and a far anchor.  The common anchor convention
is ``w(focus)=0.5`` and ``w(far)=q`` for warped-coordinate target ``q``
in ``(0.5, 1)``.  For a composed membership ``mu(u)=h(w(u))``, this implies
``mu(focus)=h(0.5)`` and ``mu(far)=h(q)``.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from .anchors import (
    logit,
    solve_arctan_gain,
    solve_generalized_logistic_params,
    solve_gompertz_gain,
    solve_logistic_gain,
    solve_tanh_gain,
    validate_anchor_inputs,
)
from .core import NumberOrArray

_EXP_LIMIT = 709.0


def _array(u: ArrayLike) -> np.ndarray:
    return np.asarray(u, dtype=float)


def _return_like_input(original: ArrayLike, value: np.ndarray) -> NumberOrArray:
    if np.isscalar(original):
        return float(np.asarray(value))
    return value


def _stable_sigmoid(z: np.ndarray) -> np.ndarray:
    y = np.empty_like(z, dtype=float)
    pos = z >= 0.0
    y[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    exp_z = np.exp(z[~pos])
    y[~pos] = exp_z / (1.0 + exp_z)
    return y


def logistic_warp(u: ArrayLike, focus: float, far: float, q: float) -> NumberOrArray:
    """Logistic anchored warp from the universe of discourse to ``[0, 1]``.

    Parameters
    ----------
    u:
        Scalar, list, or NumPy array of universe values.
    focus:
        Focus anchor ``u*`` with ``w(focus)=0.5``.
    far:
        Far anchor ``uc`` with ``w(far)=q``.  The warp is increasing when
        ``far > focus`` and decreasing when ``far < focus``.
    q:
        Warped-coordinate target for the far anchor, satisfying
        ``0.5 < q < 1``.  This is the target for ``w(far)``, not necessarily
        the final membership value after applying a base function ``h``.

    Returns
    -------
    float or ndarray
        Warped values in ``[0, 1]`` up to numerical tolerance.
    """

    a = solve_logistic_gain(focus, far, q)
    x = _array(u)
    y = _stable_sigmoid(a * (x - focus))
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def tanh_warp(u: ArrayLike, focus: float, far: float, q: float) -> NumberOrArray:
    """Hyperbolic-tangent anchored warp.

    The formula is ``w(u)=0.5*(1+tanh(a(u-focus)))``.  The function maps the
    real line to ``(0, 1)``, satisfies ``w(focus)=0.5`` and ``w(far)=q``, and
    is monotone according to the sign of ``far - focus``.
    """

    a = solve_tanh_gain(focus, far, q)
    x = _array(u)
    y = 0.5 * (1.0 + np.tanh(a * (x - focus)))
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def arctan_warp(u: ArrayLike, focus: float, far: float, q: float) -> NumberOrArray:
    """Arctangent anchored warp.

    The formula is ``w(u)=0.5+atan(a(u-focus))/pi``.  It has heavier tails
    than logistic and tanh warps, preserves ``w(focus)=0.5`` and ``w(far)=q``,
    and is increasing for ``far > focus`` or decreasing for ``far < focus``.
    """

    a = solve_arctan_gain(focus, far, q)
    x = _array(u)
    y = 0.5 + np.arctan(a * (x - focus)) / np.pi
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def gompertz_warp(u: ArrayLike, focus: float, far: float, q: float) -> NumberOrArray:
    """Anchored Gompertz warp.

    The formula is ``w(u)=exp(-eta*exp(-a(u-focus)))`` with ``eta=log(2)``.
    This fixes ``w(focus)=0.5`` and chooses ``a`` so ``w(far)=q``.  The range
    is ``[0, 1]`` up to numerical tolerance, with monotonicity controlled by
    whether ``far`` is greater or smaller than ``focus``.
    """

    a = solve_gompertz_gain(focus, far, q)
    x = _array(u)
    eta = np.log(2.0)
    inner = np.exp(np.clip(-a * (x - focus), -_EXP_LIMIT, _EXP_LIMIT))
    y = np.exp(-eta * inner)
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


def generalized_logistic_warp(
    u: ArrayLike, focus: float, far: float, q: float, nu: float = 1.0
) -> NumberOrArray:
    """Generalized-logistic anchored warp.

    The formula is ``w(u)=(1+exp(-a(u-b)))**(-1/nu)`` with ``nu > 0``.
    Parameters ``a`` and ``b`` are solved from ``w(focus)=0.5`` and
    ``w(far)=q``.  The parameter ``nu`` changes asymmetry while retaining the
    same semantic anchors and monotonic direction.
    """

    a, b = solve_generalized_logistic_params(focus, far, q, nu=nu)
    x = _array(u)
    exp_term = np.exp(np.clip(-a * (x - b), -_EXP_LIMIT, _EXP_LIMIT))
    y = (1.0 + exp_term) ** (-1.0 / nu)
    return _return_like_input(u, np.clip(y, 0.0, 1.0))


__all__ = [
    "arctan_warp",
    "generalized_logistic_warp",
    "gompertz_warp",
    "logistic_warp",
    "logit",
    "tanh_warp",
    "validate_anchor_inputs",
]
