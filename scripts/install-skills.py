#!/usr/bin/env python3
"""Install or remove only owned, unchanged MSF skill folders."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

sys.dont_write_bytecode = True

from msf_common import LANGUAGES, ROOT, read_json, registry

MARKER = ".msf-install.json"
LOCK = ".msf-install.lock"
CLIENT_DIRS = {"codex": ".agents", "claude": ".claude"}


def no_symlink_path(path: Path) -> None:
    for part in (*reversed(path.parents), path):
        if part.is_symlink():
            raise ValueError(f"symlink is not allowed: {part}")
        if part.exists() and not part.is_dir():
            raise ValueError(f"expected a directory: {part}")


def snapshot(folder: Path) -> dict[str, str]:
    """Fingerprint names, directory presence, content and executable bits."""
    result = {}
    if folder.is_symlink():
        raise ValueError(f"symlink is not allowed: {folder}")
    if not folder.is_dir():
        raise ValueError(f"expected a skill directory: {folder}")
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed: {path}")
        name = path.relative_to(folder).as_posix()
        if name == MARKER:
            continue
        mode = path.stat().st_mode
        if stat.S_ISDIR(mode):
            result[name] = "directory"
        elif stat.S_ISREG(mode):
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            result[name] = f"{mode & 0o111:03o}:{digest}"
        else:
            raise ValueError(f"special file is not allowed: {path}")
    return result


def ownership(folder: Path):
    marker = folder / MARKER
    if folder.is_symlink() or marker.is_symlink() or not marker.is_file():
        return None
    data = read_json(marker)
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("skill") != folder.name or not isinstance(data.get("files"), dict):
        raise ValueError(f"invalid MSF ownership marker: {marker}")
    return data["files"]


@contextmanager
def install_lock(root: Path):
    no_symlink_path(root)
    root.mkdir(parents=True, exist_ok=True)
    lock = root / LOCK
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ValueError(f"another install is active or left a lock: {lock}") from exc
    try:
        yield
    finally:
        lock.rmdir()


def prepare(command: str, target: Path, ids: list[str]):
    changes = []
    for name in ids:
        destination = target / name
        exists = destination.exists() or destination.is_symlink()
        if exists and (destination.is_symlink() or not destination.is_dir()):
            raise ValueError(f"collision at {destination}: expected a regular skill directory")
        if command == "list":
            owned = ownership(destination) if exists else None
            state = ("not installed" if not exists else "unmanaged" if owned is None
                     else "installed" if snapshot(destination) == owned else "modified")
            print(f"{name}: {state}")
            continue
        if command == "uninstall" and not exists:
            print(f"{name}: not installed")
            continue
        owned = ownership(destination) if exists else None
        if exists and owned is None:
            raise ValueError(f"collision: refusing to touch unmanaged folder {destination}")
        if exists and snapshot(destination) != owned:
            raise ValueError(f"modified skill: refusing to touch {destination}")
        if command == "uninstall":
            changes.append((name, owned))
            continue

        source = ROOT / "skills" / name
        no_symlink_path(source)
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"missing SKILL.md: {source}")
        if (source / MARKER).exists() or (source / MARKER).is_symlink():
            raise ValueError(f"reserved installer filename in source: {source / MARKER}")
        expected = snapshot(source)
        if exists:
            if owned != expected:
                raise ValueError(f"collision: installed skill differs from the source; uninstall first: {destination}")
            print(f"{name}: already installed")
        else:
            changes.append((name, expected))
    return changes


def install(target: Path, changes: list) -> None:
    created = []
    try:
        for name, expected in changes:
            destination = target / name
            destination.mkdir()  # Exclusive reservation; never copy into an existing skill.
            created.append(destination)
            shutil.copytree(ROOT / "skills" / name, destination, dirs_exist_ok=True, symlinks=True)
            if snapshot(destination) != expected:
                raise ValueError(f"source changed while installing {name}")
            with (destination / MARKER).open("x", encoding="utf-8") as stream:
                json.dump({"schema_version": 1, "skill": name, "files": expected}, stream, sort_keys=True)
                stream.write("\n")
    except (OSError, ValueError):
        for folder in reversed(created):
            shutil.rmtree(folder)
        raise


def uninstall(target: Path, changes: list) -> None:
    # Move validated copies aside on the same filesystem before removing them.
    quarantine = Path(tempfile.mkdtemp(prefix=".msf-remove-", dir=target))
    moved = []
    try:
        for name, expected in changes:
            destination = target / name
            if ownership(destination) != expected or snapshot(destination) != expected:
                raise ValueError(f"modified while removing {name}")
            destination.rename(quarantine / name)
            moved.append(name)
    except (OSError, ValueError):
        for name in reversed(moved):
            destination = target / name
            if destination.exists() or destination.is_symlink():
                raise ValueError(f"cannot restore {destination}; preserved copies in {quarantine}")
            try:
                (quarantine / name).rename(destination)
            except OSError as exc:
                raise ValueError(f"could not restore {destination}; preserved copies in {quarantine}: {exc}") from exc
        quarantine.rmdir()
        raise
    shutil.rmtree(quarantine)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "uninstall", "list"), nargs="?", default="install")
    parser.add_argument("--target", choices=CLIENT_DIRS, required=True)
    parser.add_argument("--scope", choices=("project", "user"), required=True)
    parser.add_argument("--language", choices=(*LANGUAGES, "both"), default="both")
    parser.add_argument("--project-root", type=Path, help="defaults to the current directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.scope == "user" and args.project_root is not None:
        parser.error("--project-root is only valid with --scope project")
    try:
        base = Path.home() if args.scope == "user" else (args.project_root or Path.cwd())
        base = Path(os.path.abspath(base.expanduser()))
        no_symlink_path(base)
        if not base.is_dir():
            raise ValueError(f"installation root must already exist: {base}")
        target = base / CLIENT_DIRS[args.target] / "skills"
        no_symlink_path(target)
        if target == ROOT / "skills":
            raise ValueError("installation destination cannot be the source directory")
        languages = LANGUAGES if args.language == "both" else (args.language,)
        ids = [pair[lang] for pair in registry() for lang in languages]
        print(f"Skill destination: {target}")
        changes = prepare(args.command, target, ids)
        if not changes:
            return 0
        if args.dry_run:
            for name, _ in changes:
                print(f"Would {args.command}: {name}")
            return 0
        with install_lock(target):
            # Recheck under the lock to close races with another installer run.
            changes = prepare(args.command, target, ids)
            if changes:
                (install if args.command == "install" else uninstall)(target, changes)
        for name, _ in changes:
            print(f"{args.command}: {name}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
