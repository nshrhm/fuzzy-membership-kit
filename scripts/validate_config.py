#!/usr/bin/env python3
"""Generate a compact validation report for a membership configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from fuzzymf import load_collection
from fuzzymf.validation import monotonicity_report, range_report


def infer_direction(kind: str) -> str | None:
    if kind in {"s_curve", "trapezoid_rising", "compressed_s"}:
        return "increasing"
    if kind in {"z_curve", "trapezoid_falling", "compressed_z"}:
        return "decreasing"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--output", default="validation_report.json")
    parser.add_argument("--points", type=int, default=1001)
    args = parser.parse_args()

    collection = load_collection(args.config)
    universe = dict(collection.universe or {})
    xmin = float(universe.get("min", 0.0))
    xmax = float(universe.get("max", 100.0))
    grid = np.linspace(xmin, xmax, args.points)

    report = {"config": args.config, "universe": universe, "memberships": []}
    for spec in collection.memberships:
        rr = range_report(spec, grid)
        item = {
            "name": spec.name,
            "kind": spec.kind,
            "range": rr.__dict__,
        }
        direction = infer_direction(spec.kind)
        if direction:
            item["monotonicity"] = monotonicity_report(spec, grid, direction=direction).__dict__
        report["memberships"].append(item)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
