# fuzzy-membership-kit

[![CI](https://github.com/nshrhm/fuzzy-membership-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/nshrhm/fuzzy-membership-kit/actions/workflows/ci.yml)
[![Version: v0.2.0.dev0 draft](https://img.shields.io/badge/version-v0.2.0.dev0%20draft-blue)](pyproject.toml)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://www.python.org/)
[![Package manager: uv](https://img.shields.io/badge/package%20manager-uv-6f42c1)](https://docs.astral.sh/uv/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docs: MkDocs](https://img.shields.io/badge/docs-MkDocs-526cfe)](https://www.mkdocs.org/)
[![Inspired by Umano 2025](https://img.shields.io/badge/inspired%20by-Umano%202025-orange)](https://doi.org/10.14864/fss.41.0_70)

`fuzzy-membership-kit` is a small, auditable Python package for defining and reusing membership functions in fuzzy-set research.  The design goal is to make membership-function definitions explicit enough for reviewers, reusable enough for experiments, and configurable enough for new models, targets, and theoretical proposals.

The package currently includes:

- classical triangular, trapezoidal, Gaussian, S, Z, and pi membership functions;
- sigmoid-composed S/Z/pi functions for smoothly compressing the universe of discourse before evaluating membership;
- serializable JSON/YAML membership specifications;
- lightweight validation helpers for range and monotonicity checks;
- documentation text that can be adapted into a paper's theory/principles section;
- focus-aware universe warping utilities for the Paper 1 v0.2.0.dev0 draft.

## Installation on Ubuntu

```bash
sudo apt update
sudo apt install -y python3 git make

# Install uv first if it is not already available:
# https://docs.astral.sh/uv/getting-started/installation/

# From the repository root
make setup
uv run pytest
```

For normal use without development tools:

```bash
uv sync
uv run python
```

For optional plotting or documentation tools:

```bash
uv sync --extra plot
uv sync --extra docs
```

## Quick use from Python

```python
import numpy as np
from fuzzymf import compressed_s, s_curve, MembershipSpec

u = np.linspace(0, 100, 501)

# Standard Zadeh-style S curve: 0 at 20, 0.5 at 50, 1 at 80.
mu_standard = s_curve(u, left=20, right=80)

# Sigmoid-composed S curve: 0.5 at 50 and 1 at 90.
# The slope is steep near the focus value and becomes milder farther away.
mu_composed = compressed_s(u, focus=50, far=90, upper_q=0.9)

# Serializable specification
high = MembershipSpec(
    name="high",
    kind="compressed_s",
    params={"focus": 50, "far": 90, "upper_q": 0.9},
)
print(high([40, 50, 60, 90]))
```

## v0.2.0.dev0 draft: Focus-Aware Warping Framework

The Paper 1 development branch generalizes sigmoid-composed membership functions into
a universe-of-discourse warping form:

```text
mu(u) = h(w_theta(u))
```

The warp anchor `q` is a warped-coordinate target: `w(focus)=0.5` and
`w(far)=q`.  The composed membership targets are `mu(focus)=h(0.5)` and
`mu(far)=h(q)`, so `q` is not necessarily the final membership value.

```python
from fuzzymf import FocusAwareMembership, logistic_warp, s_curve

base = lambda x: s_curve(x, left=0.1, right=0.9)
warp = lambda u: logistic_warp(u, focus=50, far=210, q=0.9)
mf = FocusAwareMembership(base=base, warping=warp, name="large_focus_aware")

print(mf([49, 50, 51, 210]))
```

Paper-specific repositories can use this package as a common core dependency
while keeping human data, LLM response data, experiments, and manuscripts outside
this reusable package repository.  For Paper 1 planning and traceability between
manuscript claims and repository artifacts, see `docs/paper1_outline.md` and
`docs/repository_to_paper_map.md`.

## Configuration-based use

```python
from fuzzymf import load_collection

collection = load_collection("examples/configs/emotion_vas_0_100.yaml")
scores = collection.evaluate([0, 25, 50, 75, 100])
print(scores["high_emotion"])
```

Plot from a configuration file:

```bash
uv run fuzzymf-plot examples/configs/emotion_vas_0_100.yaml -o results/emotion_memberships.png
```

## Documentation map

- `docs/theory.md`: English theory notes with equations.
- `docs/theory_ja.md`: Japanese theory notes with equations.
- `docs/implementation.md`: implementation and reproducibility guidance.
- `docs/implementation_ja.md`: Japanese implementation guide.
- `docs/warping_framework.md`: Paper 1 focus-aware warping notes.
- `docs/warping_framework_ja.md`: Japanese Paper 1 warping notes.
- `docs/diagnostics.md`: diagnostics for warps and composed memberships.
- `docs/diagnostics_ja.md`: Japanese diagnostics notes.
- `docs/paper1_outline.md`: Paper 1 planning outline.
- `docs/repository_to_paper_map.md`: traceability map from paper claims to repository artifacts.
- `docs/paper_snippet.md`: text that can be adapted into a manuscript.
- `docs/reviewer_notes.md`: checklist for reviewer-facing repositories.

## Reference

The sigmoid-composed membership-function utilities in this repository are inspired by:

Motohide Umano, "Some Considerations on Membership Functions of Fuzzy Sets," Proceedings of the 41st Fuzzy System Symposium, 2025. https://doi.org/10.14864/fss.41.0_70

## Current scope

This repository provides deterministic membership definitions.  It does not decide which membership function is theoretically correct for a particular dataset.  That decision should be justified in the accompanying paper by specifying the universe of discourse, the semantic anchor points, and the rationale for each parameter.
