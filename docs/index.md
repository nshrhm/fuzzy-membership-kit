# fuzzy-membership-kit

This repository provides auditable membership-function definitions for fuzzy-set research.  It is intended for three audiences:

1. reviewers who need to verify the mathematical definition;
2. readers who need a clear account of the membership-function family used in a paper;
3. replicators who need executable, version-controlled definitions.

The recommended reporting unit is not only the function name but also the complete parameterization, e.g.

```text
kind = compressed_s
focus = 50
far = 90
upper_q = 0.9
lower_q = 0.1
```

For a paper, cite the theoretical family and then state the exact configuration file or manifest used to instantiate it.
