#!/usr/bin/env python3
"""Run offline repository gates and optionally verify human release evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from msf_common import GATE_IDS, ROOT, read_json

PASS, FAIL, BLOCKED, NOT_APPLICABLE = "PASS", "FAIL", "BLOCKED", "NOT APPLICABLE"
SOURCE_SCRIPT = "scripts/check-sources.py"
VIDEO_SCRIPT = "examples/software-training-video/smoke.py"


def run(*argv: str, timeout: int = 60):
    try:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                                errors="replace", timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return FAIL, str(exc)
    detail = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return (PASS if result.returncode == 0 else FAIL), detail or f"exit {result.returncode}"


def gate_config():
    try:
        factory = read_json(ROOT / "config/factory.yaml")
        config = read_json(ROOT / "config/quality-gates.yaml")
        if not isinstance(factory, dict) or factory.get("schema_version") != 1:
            raise ValueError("config/factory.yaml: expected an object with schema_version 1")
        if factory.get("languages") != ["en", "ar"] or factory.get("external_integrations") != "opt-in":
            raise ValueError("config/factory.yaml: expected English and Arabic and opt-in integrations")
        rows = config.get("gates") if isinstance(config, dict) else None
        if not isinstance(rows, list) or config.get("schema_version") != 1:
            raise ValueError("config/quality-gates.yaml: expected version 1 and gates array")
        ids = []
        for row in rows:
            if not isinstance(row, dict) or not all(isinstance(row.get(key), str) and row[key].strip() for key in ("id", "en", "ar")):
                raise ValueError("config/quality-gates.yaml: every gate needs id, en and ar text")
            ids.append(row["id"])
        if tuple(ids) != GATE_IDS:
            raise ValueError(f"config/quality-gates.yaml: expected ordered IDs {', '.join(GATE_IDS)}")
    except ValueError as exc:
        return FAIL, str(exc)
    return PASS, f"Factory configuration and {len(GATE_IDS)} bilingual gate definitions validated."


def dashboard():
    file = ROOT / "examples/arabic-rtl-dashboard/model.test.mjs"
    node = shutil.which("node")
    if not file.is_file():
        return FAIL, "Missing Arabic dashboard model tests."
    if node is None:
        return BLOCKED, "Node is unavailable; Arabic dashboard checks were not run."
    return run(node, "--test", str(file))


def video():
    result = run(sys.executable, "scripts/verify-environment.py", "--require", "video")
    if result[0] != PASS:
        return BLOCKED, result[1]
    return run(sys.executable, VIDEO_SCRIPT, timeout=120)


def documentation():
    expected = (
        "README.md", "README.ar.md", "INSTALL.md", "INSTALL.ar.md",
        "LICENSE", "CONTRIBUTING.md", "CONTRIBUTING.ar.md", "CODE_OF_CONDUCT.md",
        "SECURITY.md", "CHANGELOG.md", "AGENTS.md", "CLAUDE.md", ".gitignore",
        "templates/project-plan.md", "templates/architecture-review.md",
        "templates/design-review.md", "templates/security-report.md", "templates/test-report.md",
        "templates/release-report.md", "templates/video-storyboard.json",
    )
    missing = [path for path in expected if not (ROOT / path).is_file()]
    if len(list((ROOT / ".github/ISSUE_TEMPLATE").glob("*"))) < 2:
        missing.append(".github/ISSUE_TEMPLATE/ (bug and feature templates)")
    if missing:
        return FAIL, f"Missing required files: {', '.join(missing)}"
    try:
        if not isinstance(read_json(ROOT / "templates/video-storyboard.json"), dict):
            raise ValueError("templates/video-storyboard.json: expected a JSON object")
    except ValueError as exc:
        return FAIL, str(exc)
    return PASS, "Repository documentation, community files and reusable templates are present."


def records(path: Path | None):
    if path is None:
        return {}, None
    try:
        evidence = read_json(path)
        if not isinstance(evidence, dict) or evidence.get("schema_version") != 1 or not isinstance(evidence.get("gates"), dict):
            raise ValueError("evidence must have schema_version 1 and a gates object")
        extra = set(evidence["gates"]).difference(GATE_IDS)
        if extra:
            raise ValueError(f"unknown evidence gate(s): {', '.join(sorted(extra))}")
        return evidence["gates"], None
    except ValueError as exc:
        return {}, str(exc)


def verify_record(record, base: Path):
    if not isinstance(record, dict) or record.get("status") != PASS:
        return False, "review evidence must be an object with status PASS"
    reviewer, artifact, digest = (record.get(key) for key in ("reviewer", "artifact", "sha256"))
    if not isinstance(reviewer, str) or not reviewer.strip():
        return False, "reviewer is required"
    if not isinstance(artifact, str) or not artifact.strip() or Path(artifact).is_absolute():
        return False, "artifact must be a nonempty path relative to the evidence file"
    if not isinstance(digest, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
        return False, "sha256 must be a 64-character hexadecimal digest"
    try:
        file = (base / artifact).resolve()
        if not file.is_relative_to(base) or not file.is_file():
            return False, "artifact must be an existing file inside the evidence directory"
        if file.stat().st_size == 0:
            return False, "artifact is empty"
        with file.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
    except (OSError, RuntimeError, ValueError) as exc:
        return False, f"cannot read evidence artifact: {exc}"
    if actual != digest.lower():
        return False, f"digest mismatch for {artifact}"
    return True, f"review artifact verified: {artifact}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="require verified review evidence for every gate")
    parser.add_argument("--evidence", type=Path, help="JSON review manifest; artifact paths are relative to it")
    parser.add_argument("--with-video", action="store_true", help="run the optional local FFmpeg render smoke")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    evidence, error = records(args.evidence)
    baselines = {
        "discovery": run(sys.executable, SOURCE_SCRIPT),
        "architecture": gate_config(),
        "design": dashboard(),
        "engineering": run(sys.executable, "scripts/validate-skills.py"),
        "security": run(sys.executable, "scripts/audit-skills.py", "--json"),
        "testing": run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"),
        "documentation": documentation(),
        "video": video() if args.with_video else (NOT_APPLICABLE, "Render smoke outside the default offline scope; use --with-video."),
        "release": (BLOCKED, "Release review evidence is required."),
    }
    try:
        base = args.evidence.parent.resolve() if args.evidence else ROOT
    except (OSError, RuntimeError) as exc:
        base, error = ROOT, str(exc)
    results = {}
    for id_, (baseline, detail) in baselines.items():
        status = baseline
        review = "review evidence not supplied"
        if id_ in evidence:
            record = evidence[id_]
            if isinstance(record, dict) and record.get("status") == NOT_APPLICABLE:
                reason = record.get("reason")
                if baseline == NOT_APPLICABLE and isinstance(reason, str) and reason.strip():
                    status, review = NOT_APPLICABLE, reason.strip()
                else:
                    status, review = FAIL, "NOT APPLICABLE requires an out-of-scope gate and a reason."
                results[id_] = {"status": status, "baseline": baseline, "detail": detail, "review": review}
                continue
            verified, review = verify_record(record, base)
            if not verified:
                status = FAIL
            elif (baseline == BLOCKED and id_ == "release") or baseline == NOT_APPLICABLE:
                status = PASS
        elif args.strict and baseline in {PASS, NOT_APPLICABLE}:
            status = BLOCKED
        results[id_] = {"status": status, "baseline": baseline, "detail": detail, "review": review}
    if args.json:
        print(json.dumps({"strict": args.strict, "evidence_error": error, "gates": results}, ensure_ascii=False))
    else:
        if error:
            print(f"FAIL    evidence: {error}")
        for id_, result in results.items():
            print(f"{result['status']:14} {id_}")
            if id_ == "security" and result["baseline"] == PASS:
                summary = json.loads(result["detail"])
                print(f"        {summary['markdown_files']} Markdown files, {summary['links']} local and external link references, {len(summary['warnings'])} notices.")
            else:
                for line in result["detail"].splitlines():
                    print(f"        {line}")
            if id_ in evidence or args.strict:
                print(f"        {result['review']}")
    return bool(error) or any(
        result["status"] == FAIL or (result["status"] == BLOCKED and (args.strict or (args.with_video and id_ == "video")))
        for id_, result in results.items()
    )


if __name__ == "__main__":
    sys.exit(main())
