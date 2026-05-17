"""Anchor-solving utilities for focus-aware universe warping.

The functions in this module determine closed-form parameters from semantic
anchors.  They are not fitting routines: each solver maps a focus value
``u*``, a far anchor ``uc``, and a warped-coordinate target ``q`` to the
parameters needed by a named warping family.
"""

from __future__ import annotations

import numpy as np


def validate_anchor_inputs(focus: float, far: float, q: float) -> None:
    """Validate common focus-aware anchor parameters.

    Parameters
    ----------
    focus:
        Semantic focus point ``u*``.  Anchored warps satisfy ``w(focus)=0.5``.
    far:
        Distant anchor point ``uc``.  Anchored warps satisfy ``w(far)=q``.
        If ``far > focus`` the resulting warp is increasing; if
        ``far < focus`` it is decreasing.
    q:
        Warped-coordinate target for the far anchor.  It must satisfy
        ``0.5 < q < 1`` so the far anchor lies above the focus value on the
        warped axis.  In a composed membership ``mu(u)=h(w(u))``, the final
        membership target at ``far`` is ``h(q)``, not necessarily ``q``.
    """

    if not np.isfinite(focus):
        raise ValueError("focus must be finite.")
    if not np.isfinite(far):
        raise ValueError("far must be finite.")
    if far == focus:
        raise ValueError("far must differ from focus.")
    if not np.isfinite(q) or not 0.5 < q < 1.0:
        raise ValueError("q must satisfy 0.5 < q < 1.")


def logit(p: float) -> float:
    """Return ``log(p / (1 - p))`` for ``p`` in the open unit interval."""

    if not np.isfinite(p) or not 0.0 < p < 1.0:
        raise ValueError("p must satisfy 0 < p < 1.")
    return float(np.log(p / (1.0 - p)))


def solve_logistic_gain(focus: float, far: float, q: float) -> float:
    """Solve the logistic gain from semantic anchors.

    The logistic warp is ``w(u)=1/(1+exp(-a(u-focus)))``.  With focus ``u*``,
    far anchor ``uc``, and warped-coordinate target ``q``, this returns ``a`` such that
    ``w(focus)=0.5`` and ``w(far)=q``.  The sign of ``a`` follows
    ``far - focus``: positive for increasing warps and negative for
    decreasing warps.
    """

    validate_anchor_inputs(focus, far, q)
    return logit(q) / (far - focus)


def solve_tanh_gain(focus: float, far: float, q: float) -> float:
    """Solve the tanh-warp gain from semantic anchors.

    The tanh warp is ``w(u)=0.5*(1+tanh(a(u-focus)))``.  This closed-form
    solver gives ``w(focus)=0.5`` and ``w(far)=q``.  The warp is increasing
    when ``far > focus`` and decreasing when ``far < focus``.
    """

    validate_anchor_inputs(focus, far, q)
    return float(np.arctanh(2.0 * q - 1.0) / (far - focus))


def solve_arctan_gain(focus: float, far: float, q: float) -> float:
    """Solve the arctan-warp gain from semantic anchors.

    The arctan warp is ``w(u)=0.5+atan(a(u-focus))/pi``.  This returns the
    gain ``a`` satisfying the focus and far-anchor conditions used in the
    Paper 1 focus-aware warping framework.
    """

    validate_anchor_inputs(focus, far, q)
    return float(np.tan(np.pi * (q - 0.5)) / (far - focus))


def solve_gompertz_gain(focus: float, far: float, q: float) -> float:
    """Solve the anchored Gompertz gain from semantic anchors.

    The anchored Gompertz warp uses ``eta=log(2)`` and
    ``w(u)=exp(-eta*exp(-a(u-focus)))``.  This gain gives
    ``w(focus)=0.5`` and ``w(far)=q``.  The monotonicity direction is
    determined by the sign of ``far - focus``.
    """

    validate_anchor_inputs(focus, far, q)
    return float(np.log(np.log(2.0) / (-np.log(q))) / (far - focus))


def solve_generalized_logistic_params(
    focus: float, far: float, q: float, nu: float = 1.0
) -> tuple[float, float]:
    """Solve generalized-logistic ``(a, b)`` parameters from anchors.

    The generalized logistic warp is
    ``w(u)=(1+exp(-a(u-b)))**(-1/nu)`` with ``nu > 0``.  This returns
    ``(a, b)`` so that ``w(focus)=0.5`` and ``w(far)=q``.  As in the other
    Paper 1 anchor solvers, the sign of ``a`` controls whether the warp is
    increasing or decreasing.
    """

    validate_anchor_inputs(focus, far, q)
    if not np.isfinite(nu) or nu <= 0.0:
        raise ValueError("nu must be positive and finite.")

    y_focus = 2.0**nu - 1.0
    y_q = q ** (-nu) - 1.0
    a = -np.log(y_q / y_focus) / (far - focus)
    b = focus + np.log(y_focus) / a
    return float(a), float(b)
