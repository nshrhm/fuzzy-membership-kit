from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pytest
from numpy.typing import ArrayLike

from fuzzymf import (
    arctan_warp,
    check_monotonicity,
    check_range,
    generalized_logistic_warp,
    gompertz_warp,
    logistic_warp,
    tanh_warp,
)
from fuzzymf.core import NumberOrArray

WARP_FAMILIES: tuple[Callable[[ArrayLike, float, float, float], NumberOrArray], ...] = (
    logistic_warp,
    tanh_warp,
    arctan_warp,
    gompertz_warp,
)


@pytest.mark.parametrize("warp", WARP_FAMILIES)
def test_warp_anchor_conditions_increasing(
    warp: Callable[[ArrayLike, float, float, float], NumberOrArray],
) -> None:
    focus = 50.0
    far = 210.0
    q = 0.9
    grid = np.linspace(-200.0, 300.0, 1001)
    values = np.asarray(warp(grid, focus, far, q), dtype=float)

    assert warp(focus, focus, far, q) == pytest.approx(0.5)
    assert warp(far, focus, far, q) == pytest.approx(q)
    assert np.all(np.isfinite(values))
    assert check_range(values)
    assert check_monotonicity(values, direction="increasing")


@pytest.mark.parametrize("warp", WARP_FAMILIES)
def test_warp_anchor_conditions_decreasing(
    warp: Callable[[ArrayLike, float, float, float], NumberOrArray],
) -> None:
    focus = 50.0
    far = -110.0
    q = 0.9
    grid = np.linspace(-200.0, 300.0, 1001)
    values = np.asarray(warp(grid, focus, far, q), dtype=float)

    assert warp(focus, focus, far, q) == pytest.approx(0.5)
    assert warp(far, focus, far, q) == pytest.approx(q)
    assert np.all(np.isfinite(values))
    assert check_range(values)
    assert check_monotonicity(values, direction="decreasing")


def test_logistic_scalar_and_array_return_shapes() -> None:
    scalar = logistic_warp(50.0, focus=50.0, far=210.0, q=0.9)
    array = logistic_warp([50.0, 210.0], focus=50.0, far=210.0, q=0.9)
    assert isinstance(scalar, float)
    assert isinstance(array, np.ndarray)
    assert array.tolist() == pytest.approx([0.5, 0.9])


@pytest.mark.parametrize("nu", [0.5, 1.0, 2.0])
def test_generalized_logistic_warp_nu_values(nu: float) -> None:
    focus = 50.0
    far = 210.0
    q = 0.9
    grid = np.linspace(-200.0, 300.0, 1001)
    values = np.asarray(generalized_logistic_warp(grid, focus, far, q, nu=nu), dtype=float)

    assert generalized_logistic_warp(focus, focus, far, q, nu=nu) == pytest.approx(0.5)
    assert generalized_logistic_warp(far, focus, far, q, nu=nu) == pytest.approx(q)
    assert np.all(np.isfinite(values))
    assert check_range(values)
    assert check_monotonicity(values, direction="increasing")
