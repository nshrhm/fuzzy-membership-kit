# Reviewer-facing notes

This repository is intended to reduce ambiguity around membership-function definitions in fuzzy-set publications.

## What reviewers can verify

1. The mathematical family used for each membership function.
2. The exact parameter values used in experiments.
3. The package version and source commit used to compute membership scores.
4. Numerical sanity checks, including range \([0,1]\) and intended monotonicity.
5. Whether a paper's verbal description matches the executable configuration.

## Minimal reviewer checklist

- [ ] Does the manuscript specify the universe of discourse?
- [ ] Does it state why the selected function family is appropriate?
- [ ] Does it report all parameters rather than only the function name?
- [ ] Are the parameters stored in a public JSON/YAML configuration file?
- [ ] Do plotted membership functions match the textual description?
- [ ] Are output scores reproducible from the configuration file?

## Suggested repository artifacts for a paper

```text
configs/membership_functions.yaml
results/membership_function_plot.png
results/membership_scores.csv
results/validation_report.json
MANIFEST.json
```

`MANIFEST.json` records file-level SHA-256 checksums.  Source commit and tag information should be verified from the repository history or release artifact, rather than from a committed manifest that would become stale when committed.

## Common pitfalls

- Reporting only "triangular" or "S-shaped" without parameter values.
- Mixing membership definitions with downstream statistical code.
- Failing to state the universe scale and semantic anchor points.
- Using a Gaussian membership when exact 0 or 1 regions are theoretically required.
- Changing membership parameters during revision without updating the manifest.
