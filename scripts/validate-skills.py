#!/usr/bin/env python3
"""Validate the bilingual registry, flat skill layout and skill contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from msf_common import LANGUAGES, ROOT, registry
from msf_markdown import outside_fences

HEADINGS = {
    "en": ("Scope", "Inputs", "Prerequisites", "Workflow", "Safety", "Outputs", "Validation", "Failure handling", "References"),
    "ar": ("النطاق", "المدخلات", "المتطلبات", "خطوات العمل", "السلامة", "المخرجات", "التحقق", "معالجة التعثر", "المراجع"),
}


def frontmatter(content: str):
    lines = content.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("expected opening and closing YAML frontmatter delimiters")
    end = lines.index("---", 1)
    fields: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9-]*):\s*(.*)", line)
        if not match or match[1] not in ("name", "description") or match[1] in fields:
            raise ValueError("frontmatter must have exactly one name and one description")
        key, value = match.groups()
        if re.fullmatch(r"[>|][-+]?", value):
            blocks = []
            while index < end and (not lines[index].strip() or lines[index].startswith(" ")):
                blocks.append(lines[index].strip())
                index += 1
            value = (" " if value[0] == ">" else "\n").join(blocks).strip()
        elif value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as exc:
                raise ValueError(f"invalid quoted {key}") from exc
        elif value.startswith("'"):
            if not value.endswith("'") or len(value) < 2:
                raise ValueError(f"invalid quoted {key}")
            value = value[1:-1].replace("''", "'")
        elif re.search(r":\s|\s#", value) or value.startswith(tuple("[{&*!#@>`|")):
            raise ValueError(f"quote {key} to keep it a YAML string")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a nonempty string")
        fields[key] = value
    if set(fields) != {"name", "description"}:
        raise ValueError("frontmatter must contain name and description")
    return fields, "\n".join(lines[end + 1:])


def skill_errors(path: Path, name: str, language: str):
    try:
        fields, body = frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        yield str(exc)
        return
    if fields["name"] != name:
        yield f"frontmatter name must equal folder ID {name!r}"
    if len(fields["description"]) > 1024:
        yield "description exceeds 1024 characters"
    sections = list(outside_fences(body))
    heading_rows = [(line_no, line[3:].strip()) for line_no, line in sections if line.startswith("## ")]
    titles = [title for _, title in heading_rows]
    expected = HEADINGS[language]
    for title in expected:
        if title not in titles:
            yield f"missing required heading: ## {title}"
        elif titles.count(title) != 1:
            yield f"duplicate required heading: ## {title}"
    body_lines = body.splitlines()
    for index, (line, title) in enumerate(heading_rows):
        end = heading_rows[index + 1][0] - 1 if index + 1 < len(heading_rows) else len(body_lines)
        if title in expected and not any(value.strip() for value in body_lines[line:end]):
            yield f"empty required section: ## {title}"
    if all(title in titles for title in expected) and [title for title in titles if title in expected] != list(expected):
        yield "required headings must follow the documented order"
    if language == "ar" and not re.search(r"[\u0621-\u064a]", fields["description"]):
        yield "Arabic description must contain Arabic text"


def validate(root: Path) -> tuple[int, list[str]]:
    issues = []
    try:
        pairs = registry(root)
    except ValueError as exc:
        return 0, [str(exc)]
    expected = {pair[language]: language for pair in pairs for language in LANGUAGES}
    if len(expected) != 24:
        issues.append(f"expected 12 language pairs (24 skills); found {len(pairs)} pairs")
    tree = root / "skills"
    if tree.is_symlink() or not tree.is_dir():
        return 0, issues + ["skills/ must be a regular directory"]
    actual = set()
    for path in sorted(tree.rglob("SKILL.md")):
        relative = path.relative_to(tree)
        if len(relative.parts) != 2:
            issues.append(f"non-flat skill: skills/{relative}")
        else:
            actual.add(relative.parts[0])
    for extra in sorted(actual - expected.keys()):
        issues.append(f"unregistered skill: {extra}")
    for name, language in sorted(expected.items()):
        folder = tree / name
        path = folder / "SKILL.md"
        if folder.is_symlink() or path.is_symlink() or not path.is_file():
            issues.append(f"{name}: missing regular skills/{name}/SKILL.md")
            continue
        issues.extend(f"{name}: {message}" for message in skill_errors(path, name, language))
    return len(actual), issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable result")
    args = parser.parse_args()
    count, issues = validate(ROOT)
    if args.json:
        print(json.dumps({"skills": count, "errors": issues}, ensure_ascii=False))
    else:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"Skill validation: {count} flat skills, {len(issues)} errors.")
    return bool(issues)


if __name__ == "__main__":
    sys.exit(main())
