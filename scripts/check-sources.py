#!/usr/bin/env python3
"""Check local provenance records and English/Arabic source register parity."""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlsplit

from msf_common import ROOT, read_json

REGISTER_FILES = ("GITHUB_SOURCES.md", "GITHUB_SOURCES.ar.md")
SOURCE_ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]*\Z")


def https_url(value) -> bool:
    if not isinstance(value, str) or re.search(r"\s", value):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == "https" and bool(parsed.hostname)
                and parsed.username is None and parsed.password is None)
    except ValueError:
        return False


def check_sources(root):
    issues = []
    try:
        catalog = read_json(root / "config/sources.json")
    except ValueError as exc:
        return 0, [str(exc)]
    if not isinstance(catalog, dict) or not isinstance(catalog.get("sources"), list) or not catalog["sources"]:
        return 0, ["config/sources.json: expected a nonempty sources array"]
    ids, urls = set(), set()
    for row in catalog["sources"]:
        if not isinstance(row, dict):
            issues.append("config/sources.json: every source must be an object")
            continue
        id_, url = row.get("id"), row.get("url")
        if not isinstance(id_, str) or not SOURCE_ID.fullmatch(id_):
            issues.append("config/sources.json: invalid source ID")
            continue
        if id_ in ids:
            issues.append(f"config/sources.json: duplicate source ID {id_!r}")
        ids.add(id_)
        if not https_url(url):
            issues.append(f"{id_}: expected a public HTTPS URL")
            continue
        for key in ("name", "category", "type", "type_ar", "branch", "license", "risk_en", "risk_ar"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                issues.append(f"{id_}: missing {key}")
        hosts = row.get("host_support")
        if not ((isinstance(hosts, str) and hosts.strip()) or
                (isinstance(hosts, list) and hosts and all(isinstance(host, str) and host.strip() for host in hosts))):
            issues.append(f"{id_}: missing host_support")
        if not isinstance(row.get("commit"), str) or not re.fullmatch(r"[0-9a-f]{40}", row["commit"]):
            issues.append(f"{id_}: expected a pinned 40-character commit")
        if row.get("status") != "verified":
            issues.append(f"{id_}: source metadata status is not verified")
        if not https_url(row.get("guide_url")):
            issues.append(f"{id_}: expected an HTTPS guide_url")
        if "license_url" not in row or (row["license_url"] is not None and not https_url(row["license_url"])):
            issues.append(f"{id_}: expected an HTTPS license_url or explicit null")
        if url in urls:
            issues.append(f"{id_}: duplicate source URL {url}")
        urls.add(url)
    for filename in REGISTER_FILES:
        try:
            markdown = (root / filename).read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            issues.append(f"{filename}: {exc}")
            continue
        links = set(re.findall(r"https://[^\s<>|)`\]]+", markdown))
        for url in sorted(urls - links):
            issues.append(f"{filename}: missing registered URL {url}")
        github_links = {link.rstrip("/") for link in links if https_url(link) and urlsplit(link).hostname == "github.com"}
        for url in sorted(github_links - {link.rstrip("/") for link in urls}):
            # Links to documentation, licenses and immutable repository revisions
            # are supporting citations; the catalog owns top-level repo URLs.
            if len(urlsplit(url).path.strip("/").split("/")) == 2:
                issues.append(f"{filename}: unregistered GitHub repository {url}")
    return len(urls), issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    count, issues = check_sources(ROOT)
    if args.json:
        print(json.dumps({"registered_sources": count, "errors": issues}, ensure_ascii=False))
    else:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"Source register: {count} URLs checked locally, {len(issues)} errors. Upstream availability was not tested.")
    return bool(issues)


if __name__ == "__main__":
    sys.exit(main())
