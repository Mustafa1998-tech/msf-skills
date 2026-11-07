"""Shared paths and parsers for the offline command-line tools."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"msf-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
GATE_IDS = ("discovery", "architecture", "design", "engineering", "security",
            "testing", "documentation", "video", "release")
LANGUAGES = ("en", "ar")


def read_json(path: Path):
    def unique_object(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError(f"duplicate key {key!r}")
            obj[key] = value
        return obj

    def invalid_constant(value):
        raise ValueError(f"invalid JSON constant {value!r}")

    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                          parse_constant=invalid_constant)
    except (OSError, ValueError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def registry(root: Path = ROOT) -> list[dict[str, str]]:
    data = read_json(root / "config/skill-registry.yaml")
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("pairs"), list) or not data["pairs"]:
        raise ValueError("skill registry: expected schema version 1 and a nonempty pairs list")
    seen = set()
    for pair in data["pairs"]:
        if not isinstance(pair, dict) or not all(isinstance(pair.get(key), str) for key in ("en", "ar", "category")):
            raise ValueError("skill registry: each pair must have en, ar and category strings")
        en, ar = pair["en"], pair["ar"]
        if not ID.fullmatch(en) or en.endswith("-ar") or ar != f"{en}-ar" or not pair["category"].strip():
            raise ValueError(f"skill registry: invalid pair {pair!r}")
        if seen.intersection((en, ar)):
            raise ValueError(f"skill registry: duplicate pair {en!r}")
        seen.update((en, ar))
    return data["pairs"]
