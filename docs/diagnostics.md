# Diagnostics

The v0.2.0.dev0 diagnostics are numerical checks for reviewer-facing evidence.  They do not replace mathematical derivations, but they make instantiated warps, base functions, and composed membership functions easier to audit.

## What is checked

- Range: values remain within `[0, 1]` up to tolerance.
- Monotonicity: sampled values are increasing or decreasing as expected.
- Anchor error: numerical deviation from a target for the function being diagnosed.
- Local discriminability: a finite-difference slope near a selected point.
- Tail compression ratio: local discriminability near `far` divided by local discriminability near `focus`.

For a warp `w`, the far-anchor target is the warped-coordinate target `q`.  For a focus-aware membership `mu(u)=h(w_theta(u))`, the far-anchor target is the membership target `h(q)`.  The same distinction applies at the focus: `w(focus)=0.5`, while `mu(focus)=h(0.5)`.

## Example

```python
import numpy as np
from fuzzymf import FocusAwareMembership, logistic_warp, s_curve, summarize_diagnostics

grid = np.linspace(-200, 300, 1001)
focus, far, q = 50, 210, 0.9
base = lambda x: s_curve(x, left=0.1, right=0.9)
warp = lambda u: logistic_warp(u, focus=focus, far=far, q=q)
mf = FocusAwareMembership(base=base, warping=warp)

print(summarize_diagnostics(warp, grid, focus=focus, far=far, q=q))
print(
    summarize_diagnostics(
        mf,
        grid,
        focus=focus,
        far=far,
        q=base(q),
        focus_target=base(0.5),
    )
)
```

The summary is a dictionary so it can be written directly to JSON, CSV, or experiment manifests.
