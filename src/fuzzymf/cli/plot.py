"""Command-line plotting for membership-function configuration files."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from fuzzymf.io import load_collection


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plot membership functions from a JSON/YAML config."
    )
    parser.add_argument("config", help="Path to a JSON/YAML membership configuration file.")
    parser.add_argument(
        "--output", "-o", default="membership_functions.png", help="Output PNG path."
    )
    parser.add_argument("--points", type=int, default=501, help="Number of grid points.")
    parser.add_argument("--xmin", type=float, default=None, help="Override universe minimum.")
    parser.add_argument("--xmax", type=float, default=None, help="Override universe maximum.")
    args = parser.parse_args(argv)

    import matplotlib.pyplot as plt

    collection = load_collection(args.config)
    universe = dict(collection.universe or {})
    xmin = args.xmin if args.xmin is not None else float(universe.get("min", 0.0))
    xmax = args.xmax if args.xmax is not None else float(universe.get("max", 100.0))
    if not xmin < xmax:
        raise ValueError("xmin must be smaller than xmax.")
    x = np.linspace(xmin, xmax, args.points)

    plt.figure()
    for spec in collection.memberships:
        plt.plot(x, spec(x), label=spec.name)
    plt.xlabel(str(universe.get("symbol", "u")))
    plt.ylabel("membership")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.tight_layout()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=200)
    print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
