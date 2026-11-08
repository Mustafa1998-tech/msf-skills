#!/usr/bin/env python3
"""Verify or extract an archived upstream snapshot without running its code."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
MAX_FILES = 1000
MAX_BYTES = 32 * 1024 * 1024


def read_index():
    registry = json.loads((ROOT / "config/sources.json").read_text(encoding="utf-8"))
    sources = {row["id"]: row for row in registry["sources"]}
    index = json.loads((VENDOR / "index.json").read_text(encoding="utf-8"))
    if index.get("schema_version") != 1 or not index.get("snapshots"):
        raise ValueError("Invalid vendor index")
    snapshots = {}
    for row in index["snapshots"]:
        name = row["id"]
        if not re.fullmatch(r"[a-z][a-z0-9-]+", name) or name in snapshots:
            raise ValueError(f"Invalid or duplicate snapshot ID: {name}")
        source = sources[name]
        if (row["url"], row["commit"]) != (source["url"], source["commit"]):
            raise ValueError(f"{name}: provenance differs from the source registry")
        if row["archive"] != f"archives/{name}.zip":
            raise ValueError(f"{name}: unexpected archive path")
        snapshots[name] = row
    return snapshots


def validate_members(archive, expected_files, license_path):
    members = archive.infolist()
    if not 1 <= len(members) <= MAX_FILES or len(members) != expected_files:
        raise ValueError("Unexpected archive file count")
    if sum(member.file_size for member in members) > MAX_BYTES:
        raise ValueError("Archive exceeds the expanded size limit")
    paths = set()
    for member in members:
        name = member.filename
        path = PurePosixPath(name)
        mode = member.external_attr >> 16
        if (path.is_absolute() or path.as_posix() != name or
                any(part in {".", "..", ".git"} or ":" in part or "\\" in part for part in path.parts) or
                not stat.S_ISREG(mode) or member.flag_bits & 1):
            raise ValueError(f"Unsafe archive member: {name!r}")
        normalized = name.casefold()
        if normalized in paths:
            raise ValueError(f"Duplicate archive member: {name!r}")
        paths.add(normalized)
    if any(str(parent) in paths for path in paths for parent in PurePosixPath(path).parents):
        raise ValueError("Archive file and directory paths overlap")
    if license_path not in archive.namelist():
        raise ValueError("Missing upstream license inside archive")
    if archive.testzip() is not None:
        raise ValueError("Archive CRC check failed")
    return members


def verify_or_extract(row, destination=None):
    path = VENDOR / row["archive"]
    if path.is_symlink():
        raise ValueError("Archive path is a symbolic link")
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != row["sha256"]:
            raise ValueError(f"{row['id']}: archive SHA-256 mismatch")
        stream.seek(0)
        with zipfile.ZipFile(stream) as archive:
            members = validate_members(archive, row["file_count"], row["license_path"])
            if destination is not None:
                destination.mkdir()
                try:
                    for member in members:
                        target = destination.joinpath(*PurePosixPath(member.filename).parts)
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with archive.open(member) as source, target.open("xb") as output:
                            shutil.copyfileobj(source, output)
                        target.chmod((member.external_attr >> 16) & 0o777)
                except BaseException:
                    shutil.rmtree(destination)
                    raise
    print(f"{row['id']}: {row['file_count']} verified files, {row['license']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    commands.add_parser("verify")
    extract = commands.add_parser("extract")
    extract.add_argument("snapshot")
    extract.add_argument("destination", type=Path, help="new directory under an existing parent")
    args = parser.parse_args()
    try:
        snapshots = read_index()
        if args.command == "list":
            for row in snapshots.values():
                print(f"{row['id']}: {row['commit']} ({row['license']})")
        elif args.command == "verify":
            for row in snapshots.values():
                verify_or_extract(row)
        else:
            verify_or_extract(snapshots[args.snapshot], args.destination)
    except (KeyError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Vendor snapshot error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
