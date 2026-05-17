#!/usr/bin/env python3
"""Reproduce Paper 1 draft diagnostics for anchored warping families.

The CSV reports both the warp ``w`` and the composed membership
``mu(u)=h(w(u))``.  For warp rows the far target is the warped-coordinate target
``q``.  For membership rows the far target is ``h(q)``.
"""

from __future__ import annotations

import argparse
import csv
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from fuzzymf import (
    FocusAwareMembership,
    arctan_warp,
    generalized_logistic_warp,
    gompertz_warp,
    logistic_warp,
    s_curve,
    summarize_diagnostics,
    tanh_warp,
)
from fuzzymf.core import NumberOrArray

WarpCallable = Callable[[ArrayLike], NumberOrArray]


def base_membership(x: ArrayLike) -> NumberOrArray:
    """Base S function h(x)=S(x; 0.1, 0.9) used in the Paper 1 draft."""

    return s_curve(x, left=0.1, right=0.9)


def build_warps(focus: float, far: float, q: float) -> dict[str, WarpCallable]:
    """Create anchored warps with ``w(focus)=0.5`` and ``w(far)=q``."""

    return {
        "logistic": lambda u: logistic_warp(u, focus=focus, far=far, q=q),
        "tanh": lambda u: tanh_warp(u, focus=focus, far=far, q=q),
        "arctan": lambda u: arctan_warp(u, focus=focus, far=far, q=q),
        "gompertz": lambda u: gompertz_warp(u, focus=focus, far=far, q=q),
        "generalized_logistic": lambda u: generalized_logistic_warp(
            u, focus=focus, far=far, q=q, nu=1.0
        ),
    }


def build_memberships(
    warps: dict[str, WarpCallable], focus: float, far: float, q: float
) -> dict[str, FocusAwareMembership]:
    """Compose each warp with the Paper 1 base membership h."""

    return {
        name: FocusAwareMembership(
            base=base_membership,
            warping=warp,
            name=f"paper1_{name}",
            metadata={"focus": focus, "far": far, "warped_coordinate_target_q": q},
        )
        for name, warp in warps.items()
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def maybe_write_figure(
    path: Path, grid: np.ndarray, funcs: dict[str, FocusAwareMembership]
) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    except ImportError:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for name, func in funcs.items():
        ax.plot(grid, func(grid), label=name)
    ax.set_xlabel("u")
    ax.set_ylabel("membership")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--focus", type=float, default=50.0)
    parser.add_argument("--far", type=float, default=210.0)
    parser.add_argument("--q", type=float, default=0.9)
    parser.add_argument("--points", type=int, default=1001)
    parser.add_argument("--csv", default="results/csv/paper1_warping_diagnostics.csv")
    parser.add_argument("--figure", default="results/figures/paper1_warping_comparison.png")
    args = parser.parse_args()

    grid = np.linspace(-200.0, 300.0, args.points)
    warps = build_warps(focus=args.focus, far=args.far, q=args.q)
    memberships = build_memberships(warps, focus=args.focus, far=args.far, q=args.q)
    direction = "increasing" if args.far > args.focus else "decreasing"

    warp_focus_target = 0.5
    warp_far_target = args.q
    membership_focus_target = float(np.asarray(base_membership(warp_focus_target)))
    membership_far_target = float(np.asarray(base_membership(args.q)))

    rows: list[dict[str, Any]] = []
    for name, warp in warps.items():
        summary = summarize_diagnostics(
            warp,
            grid,
            focus=args.focus,
            far=args.far,
            q=warp_far_target,
            focus_target=warp_focus_target,
            delta=1.0,
            direction=direction,
        )
        rows.append(
            {
                "family": name,
                "evaluated_function": "warp",
                "focus_target": warp_focus_target,
                "far_target": warp_far_target,
                "warped_coordinate_target_q": args.q,
                **summary,
            }
        )

        membership = memberships[name]
        summary = summarize_diagnostics(
            membership,
            grid,
            focus=args.focus,
            far=args.far,
            q=membership_far_target,
            focus_target=membership_focus_target,
            delta=1.0,
            direction=direction,
        )
        rows.append(
            {
                "family": name,
                "evaluated_function": "membership",
                "focus_target": membership_focus_target,
                "far_target": membership_far_target,
                "warped_coordinate_target_q": args.q,
                **summary,
            }
        )

    write_csv(Path(args.csv), rows)
    maybe_write_figure(Path(args.figure), grid, memberships)
    print(args.csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
