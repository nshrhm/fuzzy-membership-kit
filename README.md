# fuzzy-membership-kit

[![CI](https://github.com/nshrhm/fuzzy-membership-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/nshrhm/fuzzy-membership-kit/actions/workflows/ci.yml)
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
- documentation text that can be adapted into a paper's theory/principles section.

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
- `docs/paper_snippet.md`: text that can be adapted into a manuscript.
- `docs/reviewer_notes.md`: checklist for reviewer-facing repositories.

## Reference

The sigmoid-composed membership-function utilities in this repository are inspired by:

Motohide Umano, "Some Considerations on Membership Functions of Fuzzy Sets," Proceedings of the 41st Fuzzy System Symposium, 2025. https://doi.org/10.14864/fss.41.0_70

## Current scope

This repository provides deterministic membership definitions.  It does not decide which membership function is theoretically correct for a particular dataset.  That decision should be justified in the accompanying paper by specifying the universe of discourse, the semantic anchor points, and the rationale for each parameter.
