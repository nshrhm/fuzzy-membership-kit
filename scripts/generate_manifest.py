#!/usr/bin/env python3
"""Generate MANIFEST.json with per-file checksums for reproducibility."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "MANIFEST.json"
EXCLUDED_PATHS = {"MANIFEST.json"}
SCHEMA_VERSION = "1.0"
GENERATOR = "scripts/generate_manifest.py"


def run_git(args: list[str], *, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def package_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', text, flags=re.MULTILINE)
    if match is None:
        raise RuntimeError("Could not find project.version in pyproject.toml.")
    return match.group(1)


def git_files() -> list[str]:
    """Return tracked and untracked non-ignored files for pre-commit manifests."""

    tracked = run_git(["ls-files", "-z"], binary=True)
    untracked = run_git(["ls-files", "--others", "--exclude-standard", "-z"], binary=True)
    paths = {
        item.decode("utf-8")
        for blob in (tracked, untracked)
        for item in blob.split(b"\0")
        if item
    }
    return sorted(path for path in paths if path not in EXCLUDED_PATHS)


def file_record(path: str) -> dict[str, Any]:
    data = (ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


def membership_config_examples(paths: list[str]) -> list[str]:
    suffixes = {".json", ".yaml", ".yml"}
    return [
        path
        for path in paths
        if path.startswith("examples/configs/") and Path(path).suffix.lower() in suffixes
    ]


def local_git_state() -> dict[str, Any]:
    status_short = run_git(["status", "--short"])
    return {
        "source_commit": run_git(["rev-parse", "HEAD"]),
        "git_branch": run_git(["branch", "--show-current"]),
        "worktree_dirty": bool(status_short),
        "generated_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
    }


def build_manifest(include_git_state: bool = False) -> dict[str, Any]:
    paths = git_files()
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "package_name": "fuzzy-membership-kit",
        "package_version": package_version(),
        "generated_by": GENERATOR,
        "membership_config_examples": membership_config_examples(paths),
        "files": [file_record(path) for path in paths],
    }
    if include_git_state:
        manifest["local_git_state"] = local_git_state()
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--include-git-state",
        action="store_true",
        help=(
            "Include local git branch, HEAD, dirty state, and generation time for local audit "
            "artifacts. Do not use this flag for committed MANIFEST.json."
        ),
    )
    args = parser.parse_args()

    output = Path(args.output)
    manifest = build_manifest(include_git_state=args.include_git_state)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
