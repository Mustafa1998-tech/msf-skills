#!/usr/bin/env python3
"""Audit local Markdown links, skill payloads and obvious credential mistakes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

from msf_common import ROOT
from msf_markdown import anchors, markdown_links

SKIP = {".git", ".venv", "node_modules", "__pycache__", "dist", "out", "build"}
TEXT = {".md", ".py", ".mjs", ".js", ".css", ".html", ".json", ".yml", ".yaml", ".toml", ".txt", ".sh"}
CREDENTIAL = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|"
    r"(?:AKIA|ASIA)[A-Z0-9]{16}|"
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----|"
    r"(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{35,}"
)


def paths_under(root: Path):
    for child in sorted(root.iterdir()):
        if child.name in SKIP:
            continue
        yield child
        if not child.is_symlink() and child.is_dir():
            yield from paths_under(child)


def audit(root: Path):
    issues = []
    warnings = []
    markdown = {}
    for file in paths_under(root):
        rel = file.relative_to(root)
        mode = file.lstat().st_mode
        in_skill = rel.parts[0] == "skills"
        if file.is_symlink():
            if in_skill:
                issues.append(f"{rel}: symbolic links cannot be installed")
            continue
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            if in_skill:
                issues.append(f"{rel}: expected a regular file")
            continue
        if (file.name == ".env" or file.name.startswith(".env.")) and file.name not in (".env.example", ".env.sample", ".env.template"):
            issues.append(f"{rel}: local environment file in the audited tree")
        if file.suffix.lower() not in TEXT:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            issues.append(f"{rel}: cannot read UTF-8 text ({exc})")
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if CREDENTIAL.search(line):
                issues.append(f"{rel}:{line_no}: possible credential; value omitted")
        if file.suffix.lower() == ".md":
            markdown[file] = text
        if rel.parts[:2] == (".github", "workflows") and file.suffix.lower() in (".yaml", ".yml"):
            for line_no, line in enumerate(text.splitlines(), 1):
                if re.match(r"^\s*(?:-\s*)?uses\s*:", line):
                    target = re.split(r"\s+#", line.split(":", 1)[1], maxsplit=1)[0].strip().strip("\"'")
                    if not target.startswith("./") and not re.fullmatch(r"[^@]+@[0-9a-f]{40}", target):
                        issues.append(f"{rel}:{line_no}: external action is not pinned to a full commit SHA")
                if re.match(r"^\s*permissions\s*:\s*write-all|^\s*[a-z-]+\s*:\s*write(?:\s|$)", line):
                    issues.append(f"{rel}:{line_no}: write permissions are outside the offline CI scope")
                if re.match(r"^\s*(?:-\s*)?pull_request_target\s*:", line):
                    issues.append(f"{rel}:{line_no}: privileged pull_request_target is outside the offline CI scope")
    anchor_cache = {}
    link_count = 0
    for file, text in markdown.items():
        rel = file.relative_to(root)
        for line, destination in markdown_links(text):
            link_count += 1
            try:
                link = urlsplit(destination)
            except ValueError:
                issues.append(f"{rel}:{line}: malformed link {destination!r}")
                continue
            if link.scheme or link.netloc:
                if link.scheme.lower() not in {"https", "http", "mailto", "tel"} or not link.scheme:
                    issues.append(f"{rel}:{line}: unsupported link scheme {destination!r}")
                continue
            try:
                target = (file.parent / unquote(link.path)).resolve() if link.path else file
            except (OSError, RuntimeError, ValueError):
                issues.append(f"{rel}:{line}: cannot resolve local link target {destination!r}")
                continue
            if not target.is_relative_to(root):
                issues.append(f"{rel}:{line}: link leaves the repository: {destination}")
                continue
            if not target.exists():
                issues.append(f"{rel}:{line}: missing local link target {destination}")
                continue
            if link.fragment and target in markdown:
                if target not in anchor_cache:
                    anchor_cache[target] = anchors(markdown[target])
                if unquote(link.fragment) not in anchor_cache[target]:
                    issues.append(f"{rel}:{line}: missing heading or anchor {destination}")
            if len(rel.parts) >= 3 and rel.parts[0] == "skills" and not target.is_relative_to(root.joinpath(*rel.parts[:2])):
                warnings.append(f"{rel}:{line}: reference is available in the checkout but outside this installed skill folder: {destination}")
    return len(markdown), link_count, issues, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    count, links, issues, warnings = audit(ROOT)
    if args.json:
        print(json.dumps({"markdown_files": count, "links": links, "errors": issues, "warnings": warnings}, ensure_ascii=False))
    else:
        for issue in issues:
            print(f"ERROR: {issue}")
        for warning in warnings:
            print(f"NOTICE: {warning}")
        print(f"Audit: {count} Markdown files, {links} links, {len(issues)} errors, {len(warnings)} notices.")
    return bool(issues)


if __name__ == "__main__":
    sys.exit(main())
