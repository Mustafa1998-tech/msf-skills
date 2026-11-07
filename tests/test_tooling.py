"""Behavioral tests for safety boundaries and release evidence."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ToolingTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.repo = self.base / "repo"
        self.project = self.base / "project"
        self.project.mkdir()
        (self.repo / "config").mkdir(parents=True)
        (self.repo / "skills").mkdir()
        shutil.copytree(ROOT / "scripts", self.repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        pairs = [{"en": "msf-example", "ar": "msf-example-ar", "category": "example"}]
        (self.repo / "config/skill-registry.yaml").write_text(json.dumps({"schema_version": 1, "pairs": pairs}), encoding="utf-8")
        for name in ("msf-example", "msf-example-ar"):
            directory = self.repo / "skills" / name
            (directory / "references").mkdir(parents=True)
            (directory / "SKILL.md").write_text(name, encoding="utf-8")
            (directory / "references/guide.md").write_text("local guide", encoding="utf-8")
        self.dest = self.project / ".agents/skills"

    def install(self, command, *extra, language="both"):
        return subprocess.run(
            [sys.executable, str(self.repo / "scripts/install-skills.py"), command, "--project-root", str(self.project),
             "--target", "codex", "--scope", "project", "--language", language, *extra],
            capture_output=True, text=True, check=False,
        )

    def command(self, script, *args):
        return subprocess.run(
            [sys.executable, str(self.repo / "scripts" / script), *args],
            capture_output=True, text=True, check=False,
        )

    def test_audit_rejects_reference_that_leaves_repository(self):
        (self.repo / "README.md").write_text("[external relative file](../outside.md)\n")
        (self.base / "outside.md").write_text("outside")
        result = self.command("audit-skills.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("leaves the repository", result.stdout)

    def test_validator_rejects_name_mismatch_and_missing_sections(self):
        skill = self.repo / "skills/msf-example/SKILL.md"
        skill.write_text("---\nname: msf-wrong\ndescription: Test skill\n---\n# Example\n")
        result = self.command("validate-skills.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("name must equal", result.stdout)
        self.assertIn("required heading", result.stdout)

    def test_source_checker_rejects_unlisted_markdown_source(self):
        url = "https://github.com/example/sample"
        row = {
            "id": "sample", "name": "Sample", "url": url, "category": "test",
            "type": "reference", "type_ar": "مرجع", "host_support": ["Codex"],
            "commit": "a" * 40, "branch": "main", "license": "MIT",
            "license_url": url + "/blob/" + "a" * 40 + "/LICENSE",
            "guide_url": url + "/blob/" + "a" * 40 + "/README.md",
            "risk_en": "Example", "risk_ar": "مثال", "status": "verified",
        }
        (self.repo / "config/sources.json").write_text(json.dumps({"sources": [row]}))
        (self.repo / "GITHUB_SOURCES.md").write_text(f"[sample]({url})\n")
        (self.repo / "GITHUB_SOURCES.ar.md").write_text("[sample](https://github.com/example/wrong)\n")
        result = self.command("check-sources.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GITHUB_SOURCES.ar.md", result.stdout)
        self.assertIn(url, result.stdout)

    def test_release_evidence_rejects_stale_digest(self):
        artifact = self.repo / "review.txt"
        artifact.write_text("changed since review")
        evidence = self.repo / "evidence.json"
        evidence.write_text(json.dumps({"schema_version": 1, "gates": {"release": {
            "status": "PASS", "reviewer": "Example Reviewer", "artifact": "review.txt", "sha256": "0" * 64,
        }}}))
        result = self.command("run-quality-gates.py", "--strict", "--evidence", str(evidence))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("digest mismatch", result.stdout)

    def test_dry_run_creates_no_project_paths(self):
        result = self.install("install", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_installs_whole_folder_and_removes_only_selected_language(self):
        result = self.install("install")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.dest / "msf-example/references/guide.md").read_text(), "local guide")
        result = self.install("uninstall", language="ar")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.dest / "msf-example-ar").exists())
        self.assertTrue((self.dest / "msf-example").is_dir())

    @unittest.skipUnless(os.name == "posix", "isolated HOME uses POSIX semantics")
    def test_user_claude_scope_uses_home_and_leaves_other_language_absent(self):
        home = self.base / "home"
        home.mkdir()
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts/install-skills.py"), "install",
             "--target", "claude", "--scope", "user", "--language", "ar"],
            capture_output=True, text=True, check=False, cwd=self.project,
            env={**os.environ, "HOME": str(home)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((home / ".claude/skills/msf-example-ar/SKILL.md").is_file())
        self.assertFalse((home / ".claude/skills/msf-example").exists())
        self.assertEqual(list(self.project.iterdir()), [])

    def test_repeat_install_leaves_owned_copy_unchanged(self):
        result = self.install("install", language="en")
        self.assertEqual(result.returncode, 0, result.stderr)
        path = self.dest / "msf-example/SKILL.md"
        original_mtime = path.stat().st_mtime_ns
        result = self.install("install", language="en")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.stat().st_mtime_ns, original_mtime)

    def test_collision_preflights_all_selected_skills(self):
        collision = self.dest / "msf-example-ar"
        collision.mkdir(parents=True)
        (collision / "keep.txt").write_text("user data")
        result = self.install("install")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("collision", result.stderr.lower())
        self.assertEqual((collision / "keep.txt").read_text(), "user data")
        self.assertFalse((self.dest / "msf-example").exists())

    def test_uninstall_refuses_to_remove_edited_or_added_content(self):
        result = self.install("install")
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.dest / "msf-example-ar/user-notes.txt").write_text("keep me")
        result = self.install("uninstall")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("modified", result.stderr.lower())
        self.assertTrue((self.dest / "msf-example/SKILL.md").exists())
        self.assertTrue((self.dest / "msf-example-ar/user-notes.txt").exists())

    @unittest.skipUnless(os.name == "posix", "POSIX symbolic links required")
    def test_rejects_symlinked_target_ancestor(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        result = self.install("install")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr.lower())
        self.assertEqual(list(outside.iterdir()), [])

    @unittest.skipUnless(os.name == "posix", "POSIX symbolic links required")
    def test_rejects_symlinked_source_file(self):
        target = self.base / "outside.md"
        target.write_text("private")
        (self.repo / "skills/msf-example-ar/references/outside.md").symlink_to(target)
        result = self.install("install")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr.lower())
        self.assertFalse(self.dest.exists())


if __name__ == "__main__":
    unittest.main()
