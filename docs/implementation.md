# Implementation guide

## 1. Design principles

The repository is designed around four principles.

1. **Mathematical auditability.**  Each implemented function has a one-to-one correspondence with a displayed equation in `docs/theory.md`.
2. **Configuration before hard-coding.**  Experiments should store membership definitions in JSON/YAML manifests rather than burying parameters inside analysis scripts.
3. **Vectorized numerical use.**  Functions accept Python scalars, lists, and NumPy arrays.
4. **Reviewer reproducibility.**  A paper should point reviewers to the exact configuration file and package version used to generate scores.

## 2. Package structure

```text
src/fuzzymf/core.py          # membership definitions and serializable specs
src/fuzzymf/io.py            # JSON/YAML loader and saver
src/fuzzymf/validation.py    # simple numerical checks
src/fuzzymf/cli/plot.py      # command-line plotter
examples/configs/            # reusable configuration examples
tests/                       # unit tests for definitions and configuration
```

## 3. Function naming convention

| Name | Meaning |
| --- | --- |
| `triangular` | classical triangular membership |
| `trapezoid_rising` | increasing shoulder |
| `trapezoid_falling` | decreasing shoulder |
| `trapezoid_pi` | trapezoidal central concept |
| `gaussian` | Gaussian membership with peak 1 |
| `s_curve` | Zadeh-style quadratic S function |
| `z_curve` | complement of S function |
| `pi_curve` | S-left, Z-right smooth pi function |
| `sigmoid` | logistic transformation |
| `compressed_s` | sigmoid-composed S membership |
| `compressed_z` | sigmoid-composed Z membership |
| `compressed_pi` | two-sided sigmoid-composed central membership |

## 4. Configuration schema

A configuration file is a top-level mapping with optional `universe` and `metadata` fields and a required `memberships` list.

```yaml
universe:
  name: Visual analogue scale
  symbol: u
  min: 0
  max: 100
metadata:
  paper: example
  version: 0.1.0
memberships:
  - name: high
    kind: compressed_s
    params:
      focus: 50
      far: 90
      upper_q: 0.9
```

Each membership entry must contain:

- `name`: stable identifier used in downstream outputs;
- `kind`: one of the registered function names;
- `params`: keyword arguments passed to the function;
- `description`: optional human-readable note.

## 5. Recommended experiment manifest fields

When this package is used in a paper, keep a separate manifest containing:

```text
package_name
package_version
repository_commit
membership_config_path
membership_config_sha256
universe_definition
semantic_anchor_policy
parameter_selection_policy
score_input_files
score_output_files
```

This makes it possible to distinguish the mathematical definition, the selected parameters, and the dataset to which the membership functions were applied.

## 6. Validation checks

Use `validation.range_report` to verify that outputs remain inside \([0,1]\).  Use `validation.monotonicity_report` for increasing or decreasing concepts.

```python
import numpy as np
from fuzzymf import compressed_s
from fuzzymf.validation import range_report, monotonicity_report

grid = np.linspace(0, 100, 1001)
func = lambda u: compressed_s(u, focus=50, far=90)

print(range_report(func, grid))
print(monotonicity_report(func, grid, direction="increasing"))
```

These checks are numerical sanity checks, not formal proofs.  They are useful as reviewer-facing evidence that the instantiated configuration behaves as intended.

## 7. Adding a new membership function

1. Add a function to `src/fuzzymf/core.py`.
2. Add its name and callable to the `FUNCTIONS` registry.
3. Add an equation to `docs/theory.md` and `docs/theory_ja.md`.
4. Add at least one unit test under `tests/`.
5. Add an example configuration if the function is intended for public reuse.
