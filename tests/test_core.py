from __future__ import annotations

import math

import numpy as np
import pytest

from fuzzymf import (
    MembershipCollection,
    MembershipSpec,
    compressed_pi,
    compressed_s,
    compressed_z,
    gaussian,
    pi_curve,
    s_curve,
    sigmoid_gain_from_quantile,
    triangular,
    z_curve,
)


def test_triangular_anchor_values() -> None:
    assert triangular(0, 0, 5, 10) == 0.0
    assert triangular(5, 0, 5, 10) == 1.0
    assert triangular(10, 0, 5, 10) == 0.0
    assert triangular(2.5, 0, 5, 10) == 0.5
    assert triangular(7.5, 0, 5, 10) == 0.5


def test_s_curve_anchor_values() -> None:
    assert s_curve(0, 0, 10) == 0.0
    assert s_curve(5, 0, 10) == 0.5
    assert s_curve(10, 0, 10) == 1.0
    assert z_curve(0, 0, 10) == 1.0
    assert z_curve(5, 0, 10) == 0.5
    assert z_curve(10, 0, 10) == 0.0


def test_pi_curve_plateau() -> None:
    u = np.array([0, 2, 4, 6, 8, 10], dtype=float)
    y = pi_curve(u, 0, 4, 6, 10)
    assert np.all((0 <= y) & (y <= 1))
    assert y[2] == pytest.approx(1.0)
    assert y[3] == pytest.approx(1.0)


def test_gaussian_peak() -> None:
    assert gaussian(5, center=5, sigma=2) == pytest.approx(1.0)
    assert gaussian(7, center=5, sigma=2) < 1.0


def test_sigmoid_gain_from_quantile() -> None:
    gain = sigmoid_gain_from_quantile(focus=50, far=90, quantile=0.9)
    assert gain == pytest.approx(math.log(9) / 40)


def test_compressed_s_anchor_values() -> None:
    assert compressed_s(50, focus=50, far=90, upper_q=0.9) == pytest.approx(0.5)
    assert compressed_s(90, focus=50, far=90, upper_q=0.9) == pytest.approx(1.0)
    assert compressed_s(10, focus=50, far=90, upper_q=0.9) == pytest.approx(0.0)


def test_compressed_z_anchor_values() -> None:
    assert compressed_z(50, focus=50, far=90, upper_q=0.9) == pytest.approx(0.5)
    assert compressed_z(90, focus=50, far=90, upper_q=0.9) == pytest.approx(0.0)
    assert compressed_z(10, focus=50, far=90, upper_q=0.9) == pytest.approx(1.0)


def test_compressed_pi_range() -> None:
    u = np.linspace(0, 100, 101)
    y = compressed_pi(u, left_focus=25, left_far=40, right_focus=65, right_far=85)
    assert np.all((0 <= y) & (y <= 1))
    assert np.max(y) == pytest.approx(1.0)


def test_membership_spec_and_collection() -> None:
    spec = MembershipSpec(
        name="high", kind="compressed_s", params={"focus": 50, "far": 90, "upper_q": 0.9}
    )
    collection = MembershipCollection((spec,), universe={"min": 0, "max": 100})
    out = collection.evaluate([50, 90])
    assert set(out) == {"high"}
    assert out["high"][0] == pytest.approx(0.5)
    assert out["high"][1] == pytest.approx(1.0)
