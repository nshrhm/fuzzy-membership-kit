from __future__ import annotations

from pathlib import Path

from fuzzymf import load_collection, save_collection


def test_load_json_example() -> None:
    path = Path("examples/configs/number_large_umano2025.json")
    collection = load_collection(path)
    assert collection.memberships[0].name == "large_number"
    assert collection.memberships[0](50) == 0.5


def test_roundtrip_json(tmp_path: Path) -> None:
    collection = load_collection(Path("examples/configs/number_large_umano2025.json"))
    out = tmp_path / "roundtrip.json"
    save_collection(collection, out)
    loaded = load_collection(out)
    assert loaded.to_dict() == collection.to_dict()
