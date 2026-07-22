"""Tests for anti-slop detection patterns - ensures checks work."""

import unittest
import re
import tempfile
from pathlib import Path


class TestAntiSlopPatterns(unittest.TestCase):
    """Test regex patterns directly (no bash dependency)."""

    def _create_temp_file(self, content, suffix=".css"):
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    def test_purple_gradient_detection(self):
        pattern = re.compile(
            r'linear-gradient.*#(7c3aed|8b5cf6|a78bfa|6d28d9|5b21b6|4c1d95|9333ea)|linear-gradient.*(purple|violet)'
        )
        self.assertTrue(pattern.search("background: linear-gradient(135deg, #7c3aed, #8b5cf6)"))
        self.assertTrue(pattern.search("background: linear-gradient(to right, purple, violet)"))
        self.assertFalse(pattern.search("background: linear-gradient(135deg, #2563eb, #3b82f6)"))

    def test_inter_sole_font_detection(self):
        pattern = re.compile(r"font-family.*Inter[\"']?\s*[;,]|fontFamily.*Inter")
        self.assertTrue(pattern.search("font-family: 'Inter', sans-serif;"))
        self.assertTrue(pattern.search('fontFamily: "Inter"'))
        self.assertFalse(pattern.search("font-family: 'Sora', sans-serif;"))

    def test_ai_buzzword_detection(self):
        pattern = re.compile(
            r'seamless(ly)?|leverage|cutting[- ]edge|game[- ]chang|revolutioniz|paradigm|empower|harness'
        )
        self.assertTrue(pattern.search("seamlessly integrate"))
        self.assertTrue(pattern.search("leverage your workflow"))
        self.assertTrue(pattern.search("cutting-edge technology"))
        self.assertFalse(pattern.search("fast and reliable"))

    def test_gradient_text_detection(self):
        pattern = re.compile(r'background.*-clip:\s*text|text-transparent.*bg-clip')
        self.assertTrue(pattern.search("background: linear-gradient(...); -webkit-background-clip: text;"))
        self.assertTrue(pattern.search("text-transparent bg-clip-text"))
        self.assertFalse(pattern.search("color: #1a1a1a;"))

    def test_pure_black_bg_detection(self):
        pattern = re.compile(r'background(-color)?:\s*(#000000|#000\b|black)')
        self.assertTrue(pattern.search("background: #000000;"))
        self.assertTrue(pattern.search("background-color: black;"))
        self.assertFalse(pattern.search("background: #0a0a0a;"))

    def test_em_dash_detection(self):
        pattern = re.compile(r'\u2014|&#8212;')
        self.assertTrue(pattern.search("feature \u2014 not a bug"))
        self.assertTrue(pattern.search("line one &#8212; line two"))
        self.assertFalse(pattern.search("feature - not a bug"))

    def test_welcome_hero_detection(self):
        pattern = re.compile(r'Welcome\s+to')
        self.assertTrue(pattern.search("Welcome to our platform"))
        self.assertFalse(pattern.search("Start building today"))

    def test_equal_3_col_detection(self):
        pattern = re.compile(r'grid-cols-3(?!.*minmax)')
        self.assertTrue(pattern.search("grid-cols-3"))
        self.assertFalse(pattern.search("grid-cols-3 minmax(280px, 1fr)"))


if __name__ == "__main__":
    unittest.main()
