from __future__ import annotations

import numpy as np
import pytest

from fuzzymf import FocusAwareMembership, logistic_warp, s_curve


def test_focus_aware_membership_composes_base_and_warp() -> None:
    def base(x):
        return s_curve(x, left=0.1, right=0.9)

    focus = 50.0
    far = 210.0
    q = 0.9

    def warp(u):
        return logistic_warp(u, focus=focus, far=far, q=q)
    mf = FocusAwareMembership(
        base=base,
        warping=warp,
        name="large_focus_aware",
        metadata={"paper": "paper1"},
        description="test wrapper",
    )
    u = np.array([49.0, 50.0, 51.0, 210.0])

    assert np.allclose(mf(u), base(warp(u)))
    assert np.allclose(mf.evaluate(u), mf(u))
    assert warp(focus) == pytest.approx(0.5)
    assert warp(far) == pytest.approx(q)
    assert mf(focus) == pytest.approx(base(0.5))
    assert mf(far) == pytest.approx(base(q))
    assert mf(far) == pytest.approx(1.0)
    assert mf.name == "large_focus_aware"
    assert mf.metadata["paper"] == "paper1"
    assert mf.description == "test wrapper"
