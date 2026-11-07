"""Small helpers for the repository's supported Markdown conventions."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)(?:[ \t]+#+)?\s*$")
INLINE_LINK = re.compile(r"!?\[[^\]\n]+\]\(\s*(?:<([^>\n]+)>|((?:[^\s()\\]|\\.|\([^()\n]*\))+))")
REFERENCE_LINK = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))", re.M)
HTML_ID = re.compile(r"<[a-z][^>]*\b(?:id|name)=[\"']([^\"']+)", re.I)


def outside_fences(markdown: str):
    open_fence = None
    for number, line in enumerate(markdown.splitlines(), 1):
        match = FENCE.match(line)
        if open_fence is not None:
            if match and match[1].startswith(open_fence) and not match[2].strip():
                open_fence = None
            continue
        if match:
            open_fence = match[1]
        else:
            yield number, line


def markdown_links(markdown: str):
    for number, line in outside_fences(markdown):
        # A literal link inside an inline code span is not a reference.
        line = re.sub(r"(?<!`)(`+)(?!`).*?\1(?!`)", "INLINE_CODE", line)
        for pattern in (INLINE_LINK, REFERENCE_LINK):
            for match in pattern.finditer(line):
                yield number, re.sub(r"\\([()])", r"\1", match[1] or match[2])


def anchors(markdown: str) -> set[str]:
    result = set()
    counts: Counter[str] = Counter()
    for _, line in outside_fences(markdown):
        result.update(HTML_ID.findall(line))
        match = HEADING.match(line)
        if match:
            heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match[1].lower())
            slug = "".join(
                c for c in heading if c in "-_ " or unicodedata.category(c)[0] in "LMN"
            ).replace(" ", "-")
            if slug:
                count = counts[slug]
                result.add(f"{slug}-{count}" if count else slug)
                counts[slug] += 1
    return result
