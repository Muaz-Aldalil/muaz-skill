"""Tests for design system generator - protects the generation pipeline."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from design_system import generate_design_system, DesignSystemGenerator


class TestDesignSystemGeneration(unittest.TestCase):
    def test_generate_returns_string(self):
        result = generate_design_system("SaaS dashboard", "TestProject")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 100)

    def test_generate_markdown_format(self):
        result = generate_design_system("SaaS dashboard", "TestProject", output_format="markdown")
        self.assertIn("## Design System", result)
        self.assertIn("TestProject", result)

    def test_generate_contains_required_sections(self):
        result = generate_design_system("SaaS dashboard", "TestProject")
        self.assertIn("PATTERN", result)
        self.assertIn("STYLE", result)
        self.assertIn("COLORS", result)
        self.assertIn("TYPOGRAPHY", result)
        self.assertIn("PRE-DELIVERY CHECKLIST", result)

    def test_generator_returns_dict_with_all_keys(self):
        gen = DesignSystemGenerator()
        ds = gen.generate("SaaS dashboard", "TestProject")
        required_keys = ["project_name", "category", "pattern", "style", "colors", "typography", "key_effects", "anti_patterns"]
        for key in required_keys:
            self.assertIn(key, ds, f"Missing key: {key}")

    def test_colors_have_required_fields(self):
        gen = DesignSystemGenerator()
        ds = gen.generate("SaaS dashboard", "TestProject")
        colors = ds["colors"]
        for field in ["primary", "secondary", "accent", "background", "foreground"]:
            self.assertIn(field, colors, f"Missing color field: {field}")

    def test_typography_has_required_fields(self):
        gen = DesignSystemGenerator()
        ds = gen.generate("SaaS dashboard", "TestProject")
        typo = ds["typography"]
        for field in ["heading", "body"]:
            self.assertIn(field, typo, f"Missing typography field: {field}")


if __name__ == "__main__":
    unittest.main()
