from __future__ import annotations

import math

import pytest

from fuzzymf import (
    logit,
    solve_arctan_gain,
    solve_generalized_logistic_params,
    solve_gompertz_gain,
    solve_logistic_gain,
    solve_tanh_gain,
    validate_anchor_inputs,
)


def test_closed_form_anchor_solvers() -> None:
    focus = 50.0
    far = 210.0
    q = 0.9

    assert solve_logistic_gain(focus, far, q) == pytest.approx(math.log(9.0) / 160.0)
    assert solve_tanh_gain(focus, far, q) == pytest.approx(math.atanh(0.8) / 160.0)
    assert solve_arctan_gain(focus, far, q) == pytest.approx(
        math.tan(math.pi * 0.4) / 160.0
    )
    assert solve_gompertz_gain(focus, far, q) == pytest.approx(
        math.log(math.log(2.0) / (-math.log(q))) / 160.0
    )


def test_generalized_logistic_solver_anchor_params() -> None:
    a, b = solve_generalized_logistic_params(50.0, 210.0, 0.9, nu=1.0)
    assert a == pytest.approx(math.log(9.0) / 160.0)
    assert b == pytest.approx(50.0)


def test_anchor_validation_errors() -> None:
    with pytest.raises(ValueError, match="far must differ"):
        validate_anchor_inputs(1.0, 1.0, 0.9)
    with pytest.raises(ValueError, match="0.5 < q < 1"):
        validate_anchor_inputs(1.0, 2.0, 0.5)
    with pytest.raises(ValueError, match="0 < p < 1"):
        logit(1.0)
    with pytest.raises(ValueError, match="nu"):
        solve_generalized_logistic_params(1.0, 2.0, 0.9, nu=0.0)
