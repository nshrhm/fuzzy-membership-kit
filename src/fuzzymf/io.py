"""Configuration-file helpers for membership specifications."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .core import MembershipCollection


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("Install PyYAML or use JSON configuration files.") from exc
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping at top level in {path}.")
    return data


def load_collection(path: str | Path) -> MembershipCollection:
    """Load a membership collection from JSON, YAML, or YML."""

    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    elif suffix in {".yaml", ".yml"}:
        data = _load_yaml(p)
    else:
        raise ValueError(f"Unsupported configuration suffix: {suffix!r}.")
    return MembershipCollection.from_dict(data)


def save_collection(collection: MembershipCollection, path: str | Path) -> None:
    """Save a membership collection as pretty JSON."""

    p = Path(path)
    with p.open("w", encoding="utf-8") as f:
        json.dump(collection.to_dict(), f, ensure_ascii=False, indent=2)
        f.write("\n")
