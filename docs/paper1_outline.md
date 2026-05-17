# Paper 1 Manuscript Outline

This is a reviewer-facing and author-facing planning document for a future Paper 1 manuscript repository.  It is not the manuscript itself, and it does not add paper-specific experiments or datasets to this core package repository.

## 1. Working title

Focus-Aware Membership Functions via Universe-of-Discourse Warping: A Comparative and Reproducible Framework

## 2. Target contribution

Paper 1 should present a reproducible framework for constructing and comparing focus-aware membership functions.  The central contribution is not a claim that one membership function is universally best.  The contribution is a transparent parameterization that explicitly controls local discriminability near a semantic focus value and smooth compression in distant regions.

## 3. Motivation and problem setting

Classical membership functions often encode useful qualitative shapes, but the same distance in the universe of discourse need not have the same semantic importance everywhere.  In applications with a focus value, nearby values may need clearer separation, while far-away values can be compressed smoothly.  Paper 1 should frame this as a design and reproducibility problem: how to state, instantiate, compare, and audit such membership functions without black-box fitting.

## 4. Relation to classical membership functions

The manuscript should review the baseline families already implemented in the package.

- Triangular functions: simple piecewise-linear baselines with one peak.
- Trapezoidal functions: piecewise-linear shoulder and plateau baselines.
- Gaussian functions: smooth peak-centered functions without exact compact support.
- S/Z/pi functions: Zadeh-style smooth monotone and central-membership shapes.
- Sigmoid-composed S/Z/pi functions: existing compressed-universe constructions that motivate the more general warping framework.

## 5. Proposed framework

The framework is

\[
\mu(u) = h(w_\theta(u)),
\]

where `u` is an element of the universe of discourse, `w_theta` is a universe-of-discourse warping function, and `h` is a base membership function.  The semantic focus point is `u*`, the far anchor is `uc`, and `q` is the warped-coordinate target.

The anchor distinction must be stated explicitly:

\[
w(focus)=0.5,\qquad w(far)=q,
\]

while the composed membership satisfies

\[
\mu(focus)=h(0.5),\qquad \mu(far)=h(q).
\]

Thus `q` is not necessarily the final membership degree.

## 6. Warping families

Paper 1 should compare a small set of warping families.

- Identity: conceptual baseline for no universe warping.
- Logistic: sigmoid warp with closed-form gain from anchors.
- Tanh: symmetric smooth warp equivalent in shape to a scaled logistic form.
- Arctan: heavier-tailed monotone warp.
- Gompertz: asymmetric smooth warp.
- Generalized logistic: adjustable asymmetric logistic family.
- Monotone spline: future or optional extension, not implemented in the current v0.2.0.dev0 package.

## 7. Anchor-based parameter determination

The paper should emphasize semantic-anchor parameter determination rather than black-box fitting.  Given `focus`, `far`, and warped-coordinate target `q`, each implemented warp solves its parameters so that `w(focus)=0.5` and `w(far)=q`.  Paper 1 should not introduce human calibration or data-fitting claims.

## 8. Diagnostic criteria

The diagnostic section should connect design goals to numerical checks.

- Range validity: outputs remain in `[0, 1]` within tolerance.
- Monotonicity: increasing or decreasing behavior matches the semantic direction.
- Local discriminability: finite-difference separation near selected points.
- Tail compression ratio: far-anchor discriminability relative to focus discriminability.
- Anchor error: numerical deviation from the stated anchor target.
- Numerical slope: maximum and pointwise first-derivative estimates.
- Numerical curvature: second-derivative estimates for shape discussion.
- Smoothness discussion: numerical evidence is useful for implementation audit, but it is not a universal proof of theoretical optimality.

## 9. Reproducible implementation

The manuscript should point to this repository as the common core package.

- Python package with public APIs under `fuzzymf`.
- NumPy-friendly scalar and array functions.
- YAML/JSON examples for reusable configuration.
- Unit tests for core functions, anchor solvers, warps, composition, and diagnostics.
- Reproduction script for Paper 1 diagnostic comparisons.
- `MANIFEST.json` and `scripts/generate_manifest.py` for file-level checksum metadata.

## 10. Demonstration plan

The v0.2.0.dev0 demonstration should use `focus=50`, `far=210`, and `q=0.9`.  It should compare the implemented warping families, diagnose both `w` and the composed `mu`, and generate CSV summaries plus optional figures.  No external data are required.

## 11. Expected figures and tables

- Figure 1: classical membership functions.
- Figure 2: universe-of-discourse warping concept.
- Figure 3: warping family comparison.
- Figure 4: composed membership functions `mu(u)`.
- Figure 5: local discriminability or slope diagnostics.
- Table 1: function family definitions and anchor conditions.
- Table 2: diagnostics summary.
- Table 3: repository-to-paper artifact map.

## 12. Limitations

Paper 1 should avoid overclaiming.

- It does not claim a universally best membership function.
- It does not include human VAS calibration experiments.
- It does not include LLM emotional intelligence applications.
- It does not include interval-valued or type-2 fuzzy-set extensions.
- Numerical diagnostics are implementation diagnostics and comparative evidence, not universal theoretical proofs.

## 13. Future work

- Paper 2: VAS emotion calibration and human-facing parameter selection.
- Paper 3: interval-valued and type-2 extensions.
- Possible later extension: monotone spline warping when a richer shape vocabulary is justified.

## 14. Candidate abstract

Membership-function design often requires a balance between local sensitivity near semantically important values and smooth compression in distant regions of the universe of discourse.  This paper proposes a focus-aware membership-function framework based on universe-of-discourse warping, expressed as `mu(u)=h(w_theta(u))`, where `w_theta` maps original universe values to a warped coordinate and `h` is a reusable base membership function.  The framework uses semantic anchors, including a focus point satisfying `w(focus)=0.5` and a far anchor satisfying `w(far)=q`, where `q` is a warped-coordinate target rather than necessarily a final membership value.  We compare logistic, tanh, arctan, Gompertz, and generalized logistic warping families; provide closed-form anchor-based parameter determination; and report numerical diagnostics for range validity, monotonicity, local discriminability, tail compression, slope, curvature, and anchor error.  A NumPy-based Python implementation, tests, configuration examples, diagnostic scripts, and checksum metadata support reproducibility.  The framework is intended to make focus-aware membership definitions explicit, comparable, and auditable; it does not claim to identify a universally optimal membership function.
