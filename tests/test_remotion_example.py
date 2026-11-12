"""Offline structural contract for the optional bilingual Remotion example."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "remotion-training-video"


class RemotionExampleTests(unittest.TestCase):
    def test_pinned_optional_dependencies_and_scripts(self):
        package = json.loads((DEMO / "package.json").read_text(encoding="utf-8"))
        self.assertTrue(package["private"])
        self.assertEqual(package["dependencies"]["remotion"], package["dependencies"]["@remotion/cli"])
        self.assertNotIn("^", package["dependencies"]["remotion"])
        for script in ("dev", "typecheck", "render:ar", "render:en", "render:ar:4k", "render:en:4k"):
            self.assertIn(script, package["scripts"])
        self.assertIn("--scale=2", package["scripts"]["render:ar:4k"])
        self.assertIn("--scale=2", package["scripts"]["render:en:4k"])

    def test_bilingual_compositions_and_synthetic_content(self):
        root = (DEMO / "src" / "Root.tsx").read_text(encoding="utf-8")
        video = (DEMO / "src" / "TrainingVideo.tsx").read_text(encoding="utf-8")
        self.assertIn('id="MSFTrainingAR"', root)
        self.assertIn('id="MSFTrainingEN"', root)
        self.assertIn("width: 1920", root)
        self.assertIn("height: 1080", root)
        self.assertIn("fps: 30", root)
        self.assertIn("direction: locale === 'ar' ? 'rtl' : 'ltr'", video)
        self.assertIn("DEMO-001", video)
        self.assertIn("تم حفظ الأصل بنجاح", video)
        self.assertIn("Asset saved successfully", video)

    def test_skills_and_bilingual_guides(self):
        for locale in ("", "-ar"):
            base = ROOT / "skills" / ("msf-video-studio" + locale)
            self.assertIn("references/remotion.md", (base / "SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue((base / "references" / "remotion.md").is_file())
        self.assertTrue((DEMO / "README.md").is_file())
        self.assertTrue((DEMO / "README.ar.md").is_file())


if __name__ == "__main__":
    unittest.main()
