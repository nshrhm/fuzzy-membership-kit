"""Focus-aware membership wrappers."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from .core import NumberOrArray


@dataclass(frozen=True)
class FocusAwareMembership:
    """Compose a base membership function with a universe warp.

    ``FocusAwareMembership`` represents the Paper 1 framework
    ``mu(u)=h(w_theta(u))``.  The ``warping`` callable maps universe values to
    the unit interval, while ``base`` maps those warped values to membership
    values.  If the warp satisfies ``w(focus)=0.5`` and ``w(far)=q``, then
    the composed membership satisfies ``mu(focus)=h(0.5)`` and
    ``mu(far)=h(q)``.  Both callables may accept scalars or NumPy-compatible
    arrays.
    """

    base: Callable[[ArrayLike], NumberOrArray]
    warping: Callable[[ArrayLike], NumberOrArray]
    name: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)
    description: str = ""

    def __call__(self, u: ArrayLike) -> NumberOrArray:
        """Evaluate ``base(warping(u))`` for scalar or array-like input."""

        warped = self.warping(u)
        values = self.base(warped)
        if np.isscalar(u):
            return float(np.asarray(values))
        return np.asarray(values, dtype=float)

    def evaluate(self, u: ArrayLike) -> NumberOrArray:
        """Alias for ``__call__`` for consistency with collection objects."""

        return self(u)
