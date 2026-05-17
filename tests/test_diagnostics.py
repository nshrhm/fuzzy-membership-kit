from __future__ import annotations

import numpy as np
import pytest

from fuzzymf import (
    FocusAwareMembership,
    anchor_error,
    check_monotonicity,
    check_range,
    local_discriminability,
    logistic_warp,
    numerical_derivative,
    numerical_second_derivative,
    s_curve,
    summarize_diagnostics,
    tail_compression_ratio,
)


def test_numerical_derivatives_have_expected_shapes() -> None:
    grid = np.linspace(-1.0, 1.0, 11)
    first = numerical_derivative(lambda x: np.asarray(x) ** 2, grid)
    second = numerical_second_derivative(lambda x: np.asarray(x) ** 2, grid)
    assert first.shape == grid.shape
    assert second.shape == grid.shape
    assert second[5] == pytest.approx(2.0)


def test_basic_diagnostic_helpers() -> None:
    values = np.array([0.0, 0.2, 0.5, 1.0])
    assert check_range(values)
    assert check_monotonicity(values, direction="increasing")
    assert check_monotonicity(values[::-1], direction="decreasing")
    def func(u):
        return logistic_warp(u, focus=50.0, far=210.0, q=0.9)
    assert anchor_error(func, 50.0, 0.5) == pytest.approx(0.0)
    assert local_discriminability(func, 50.0) > local_discriminability(func, 210.0)
    assert tail_compression_ratio(func, 50.0, 210.0) < 1.0


def test_summarize_diagnostics_keys_and_values() -> None:
    grid = np.linspace(-200.0, 300.0, 1001)
    def func(u):
        return logistic_warp(u, focus=50.0, far=210.0, q=0.9)
    summary = summarize_diagnostics(
        func,
        grid,
        focus=50.0,
        far=210.0,
        q=0.9,
        focus_target=0.5,
        direction="increasing",
    )
    expected = {
        "range_ok",
        "monotone_ok",
        "min_value",
        "max_value",
        "max_abs_slope",
        "slope_at_focus",
        "slope_at_far",
        "anchor_error_focus",
        "anchor_error_far",
        "local_discriminability_focus",
        "local_discriminability_far",
        "tail_compression_ratio",
    }
    assert expected <= set(summary)
    assert summary["range_ok"] is True
    assert summary["monotone_ok"] is True
    assert summary["anchor_error_focus"] == pytest.approx(0.0)
    assert summary["anchor_error_far"] == pytest.approx(0.0)
    assert summary["max_abs_slope"] > 0.0



def test_summarize_diagnostics_uses_membership_far_target() -> None:
    grid = np.linspace(-200.0, 300.0, 1001)
    focus = 50.0
    far = 210.0
    q = 0.9

    def base(x):
        return s_curve(x, left=0.1, right=0.9)

    def warp(u):
        return logistic_warp(u, focus=focus, far=far, q=q)

    mf = FocusAwareMembership(base=base, warping=warp)
    summary = summarize_diagnostics(
        mf,
        grid,
        focus=focus,
        far=far,
        q=float(base(q)),
        focus_target=float(base(0.5)),
        direction="increasing",
    )

    assert warp(far) == pytest.approx(q)
    assert mf(focus) == pytest.approx(base(0.5))
    assert mf(far) == pytest.approx(base(q))
    assert mf(far) == pytest.approx(1.0)
    assert summary["anchor_error_focus"] == pytest.approx(0.0)
    assert summary["anchor_error_far"] == pytest.approx(0.0)
