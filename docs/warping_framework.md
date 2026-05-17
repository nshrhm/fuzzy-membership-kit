# Focus-aware warping framework

This page describes the v0.2.0.dev0 draft foundation for Paper 1, "Focus-Aware Membership Functions via Universe-of-Discourse Warping: A Comparative and Reproducible Framework".

The core representation is

\[
\mu(u) = h(w_\theta(u)),
\]

where `u` is a value in the universe of discourse, `w_theta` is a warping function, and `h` is a base membership function such as S, Z, or pi.  The warp maps the original universe into `[0, 1]`; the base membership is then evaluated on this warped scale.

## Semantic anchors

The first draft uses two explicit anchors for the warping function `w`.

- `focus` (`u*`): the semantic focus point, with `w(focus)=0.5`.
- `far` (`uc`): a distant anchor in the warped coordinate, with `w(far)=q`.
- `q`: the warped-coordinate target for the far anchor, with `q` in `(0.5, 1)`.

For the composed membership function `mu(u)=h(w(u))`, these imply

\[
\mu(focus)=h(0.5),\qquad \mu(far)=h(q).
\]

Thus `q` is not necessarily the final membership degree.  For example, if `h(x)=S(x; 0.1, 0.9)` and `q=0.9`, then `h(q)=1.0`, so the far membership target is 1.0 even though the warped-coordinate target is 0.9.

If `far > focus`, the warp is increasing.  If `far < focus`, the warp is decreasing.  This lets the same family describe either direction without changing the anchor convention.

## Warping families

The package provides logistic, tanh, arctan, Gompertz, and generalized logistic warps.  Each family has a closed-form anchor solver, so the user reports semantic anchors instead of fitted black-box parameters.  The existing sigmoid-composed S function is a special case of this wider pattern: it first maps `u` through a logistic warp and then applies an S function on the warped universe.

## Interpretation

The framework explicitly controls local discriminability near a focus value and smooth compression in distant regions.  It is intended to make membership definitions reproducible and comparable, not to claim that one family is universally best for every concept or dataset.

For a minimal example:

```python
from fuzzymf import FocusAwareMembership, logistic_warp, s_curve

base = lambda x: s_curve(x, left=0.1, right=0.9)
warp = lambda u: logistic_warp(u, focus=50, far=210, q=0.9)
mf = FocusAwareMembership(base=base, warping=warp, name="large_focus_aware")
print(mf([49, 50, 51, 210]))
```
