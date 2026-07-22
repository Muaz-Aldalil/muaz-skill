# Muaz-v3 v4.1.0 — Upgrade Plan

> **Version:** v4.1.0 (additive, no breaking changes)
> **Scope:** Bug fixes + data expansion + critical tests
> **Time estimate:** ~5.5 hours
> **Date:** 2026-07-21

---

## Phase 1: Bug Fixes (30 min)

### 1.1 Fix quality-gate.md threshold inconsistencies

**File:** `references/quality-gate.md`

Three different thresholds exist for "redesign":
- Line 14: `Max 3 iterations. If still < 96 after 3 → redesign`
- Line 106: `< 72 → Redesign`
- Line 154: `if still < 80, redesign`

**Fix:** Standardize to:
- `96-120` → Ship
- `72-95` → Revise (max 3 iterations)
- `< 72` → Redesign from Phase 3

Change line 154 from `< 80` to `< 72`.

### 1.2 Fix version string in memory-system.md

**File:** `references/memory-system.md`

Line 67 says `Skill: Muaz-v3 v3.0.0`. Change to `Skill: Muaz-v3 v4.1.0`.

### 1.3 Fix SKILL.md version

**File:** `SKILL.md`

Line 10: Change `version: 4.0.0` to `version: 4.1.0`.

### 1.4 Remove missing stacks from SKILL.md

**File:** `SKILL.md`

Line 14: Remove `avalonia`, `javafx`, `uno`, `uwp`, `winui`, `wpf` from the stacks list. These have no CSV files in `data/stacks/`.

Change from:
```
stacks: [html-tailwind, react, next, vue, nuxt, svelte, astro, angular, swiftui, flutter, react-native, laravel, threejs, jetpack-compose, shadcn, nuxt-ui, avalonia, javafx, uno, uwp, winui, wpf]
```
To:
```
stacks: [html-tailwind, react, next, vue, nuxt, svelte, astro, angular, swiftui, flutter, react-native, laravel, threejs, jetpack-compose, shadcn, nuxt-ui]
```

### 1.5 Fix AGENTS.md template version

**File:** `templates/AGENTS.md`

Line 11: Change `Skill: Muaz-v3 v4.0.0` to `Skill: Muaz-v3 v4.1.0`.

### 1.6 Fix Content Footer row in compositions.csv

**File:** `data/compositions.csv`

Row 26 (Content Footer) has **shifted columns** — the `style_tags` field is missing, causing all subsequent fields to shift left. This means the footer data is being parsed incorrectly by the search engine.

**Current broken state:**
```
Content Footer,minimal enterprise saas,"Multi-column footer...","Every landing page...","Don't make footer...",Stripe.com footer | Vercel.com footer | Linear.app footer
```

**Fixed state:**
```
Content Footer,footer,minimal enterprise saas,"Multi-column footer...","Every landing page...","Don't make footer...",Stripe.com footer | Vercel.com footer | Linear.app footer
```

The fix: insert `footer` as the category, shift `minimal enterprise saas` to style_tags, and keep all other fields in their correct positions.

---

## Phase 2: Data Expansion (3 hours)

### 2.1 Expand compositions.csv

**File:** `data/compositions.csv`

Add 19 new patterns (31 → 50 total). Each row must have all 7 columns: `name`, `category`, `style_tags`, `description`, `use_cases`, `anti_patterns`, `examples`.

#### Forms (4 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Single-Step Form | forms | minimal enterprise saas | Single form with 3-5 fields, visible labels, inline validation. Clean layout with clear CTA. | Newsletter signup, contact form, simple registration | Don't exceed 5 fields. Don't use placeholder-only labels. Don't hide error messages. | Stripe.com checkout, Linear.app signup, Cal.com booking |
| Multi-Step Wizard | forms | enterprise saas minimal | Progress indicator at top, one logical group per step, back/next navigation. State preserved on back. | Onboarding flows, complex signup, checkout, profile setup | Don't lose state on back. Don't skip progress indicator. Don't allow jump-ahead without validation. | Stripe.com onboarding, Notion.so setup, Figma.com onboarding |
| Inline Validation Form | forms | minimal saas enterprise | Real-time validation on blur (not keystroke). Error below field. Success checkmark. | Settings forms, profile editing, any form with async validation | Don't validate on keystroke (noisy). Don't show errors before user interacts. Don't use red for everything — use semantic colors. | GitHub.com settings, Linear.app settings, Vercel.com dashboard |
| File Upload Zone | forms | minimal enterprise saas | Drag-and-drop zone with dashed border. File type + size validation. Preview for images. Progress bar for uploads. | Profile avatar, document upload, media management | Don't accept files without validation. Don't upload without progress feedback. Don't allow multiple uploads without queue management. | Notion.so file upload, Figma.com file import, Dropbox.com upload |

#### Auth (3 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Split-Screen Auth | auth | minimal dark luxury | Left panel: brand imagery/headline. Right panel: auth form. 50/50 or 60/40 split. | SaaS signup, premium products, branded experiences | Don't use stock photos. Don't make form too wide (>400px). Don't hide social login below fold. | Linear.app login, Vercel.com login, Stripe.com login |
| Centered Card Auth | auth | minimal saas enterprise | Centered card (max-width 400px) on neutral background. Logo top, form middle, social login bottom. | Most SaaS apps, internal tools, admin panels | Don't make card too wide. Don't use colored background that clashes with brand. Don't forget "forgot password" link. | Notion.so login, GitHub.com login, Slack.com login |
| Passwordless Auth | auth | minimal saas modern | Email-only input. Magic link or OTP sent. No password field. Clear instructions after submit. | Modern SaaS, developer tools, low-friction signup | Don't reveal whether email exists. Don't auto-submit on enter without confirmation. Don't forget to mention "check your email" with spam folder hint. | Linear.app passwordless, Raycast.com login, Vercel.com login |

#### Onboarding (3 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Progress Stepper | onboarding | minimal saas enterprise | Numbered steps (1/5, 2/5...) at top. Current step highlighted. Back/Next at bottom. | Setup wizards, profile completion, multi-step forms | Don't skip step numbers. Don't make steps non-clickable (allow jump-back). Don't lose progress on refresh. | Stripe.com onboarding, Notion.so setup, Linear.app onboarding |
| Interactive Tutorial | onboarding | playful kinetic saas | Overlay tooltips pointing to UI elements. "Next" button advances. "Skip" always visible. | Feature discovery, new user walkthrough, complex app introduction | Don't block entire UI. Don't show on every visit. Don't make tooltips too long. Always allow skip. | Figma.com tutorial, Intercom.com onboarding, Product tour examples |
| Checklist Sidebar | onboarding | minimal enterprise saas | Fixed sidebar with 4-6 items. Checkmarks on completion. Progress percentage. CTA for next incomplete item. | Dashboard onboarding, account setup, feature adoption | Don't show completed items as disabled. Don't auto-remove completed items (user wants to see progress). Don't make checklist block main content. | Linear.app sidebar, Notion.so onboarding, Vercel.com dashboard |

#### Navigation (2 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Mega Menu | navigation | enterprise saas minimal | Dropdown with multiple columns. Categories, links, possibly featured content. Keyboard navigable. | Enterprise sites, complex products, multi-section marketing | Don't trigger on hover alone (add click/tap). Don't make it too wide (>800px). Don't hide sub-categories without visual cue. | GitHub.com nav, Atlassian nav, Notion.so nav |
| Mobile Bottom Sheet | navigation | minimal saas modern | Slide-up panel from bottom. 3-5 options with icons. Drag handle at top. Tap outside to dismiss. | Mobile navigation, action menus, filter panels | Don't use for primary navigation (use bottom tab bar). Don't make content scrollable inside sheet (keep it short). Don't forget drag handle affordance. | Linear.app mobile, Figma.com mobile, iOS native patterns |

#### Notifications (2 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Toast Stack | notifications | minimal saas enterprise | Small cards at bottom-right or top-right. Auto-dismiss in 3-5s. Stacked vertically. Success/error/info variants. | Action feedback, success confirmation, non-critical alerts | Don't stack more than 3. Don't auto-dismiss errors (require manual dismiss). Don't use for critical alerts (use modal instead). | Linear.app toasts, Vercel.com notifications, Notion.so toasts |
| Notification Center | notifications | minimal enterprise saas | Dropdown or sidebar panel. Grouped by date. Unread indicator badge. Mark all as read. | Activity feeds, team updates, system alerts | Don't show unread count >99 (show "99+"). Don't auto-refresh without visual cue. Don't mix notification types without grouping. | GitHub.com notifications, Linear.app inbox, Slack.com activity |

#### Empty States (2 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Illustration + CTA | empty states | playful minimal saas | Centered illustration (simple, on-brand). Headline explaining what goes here. CTA to take action. | No data yet, first-time experience, cleared state | Don't use complex illustrations (keep it simple). Don't use "Nothing here" without explanation. Don't forget the CTA — user needs next step. | Linear.app empty states, Notion.so empty pages, Vercel.com empty dashboard |
| Search + Suggestion | empty states | minimal saas enterprise | Search bar at center. Below: suggested actions or popular content. Helps user find what they need. | Search results, filtered views, discovery pages | Don't show zero results without alternatives. Don't make search the only option (add suggestions). Don't forget to clear previous search state. | GitHub.com empty repos, Linear.app search, Figma.com community |

#### Data Display (3 patterns)

| name | category | style_tags | description | use_cases | anti_patterns | examples |
|------|----------|------------|-------------|-----------|---------------|----------|
| Data Table with Filters | data | enterprise saas minimal | Table with sortable columns. Filter bar above. Pagination or infinite scroll. Row hover highlight. | Admin panels, list views, data management | Don't make columns too narrow. Don't hide filters behind a button (show them). Don't use pagination >100 pages (switch to search). | GitHub.com repos list, Linear.app issues, Stripe.com payments |
| Stat Cards Row | data | minimal saas enterprise | 3-5 cards in a row. Each: number (large), label (small), trend indicator (up/down arrow). | Dashboard overview, KPI display, analytics summary | Don't use more than 5 cards. Don't make numbers too small (<24px). Don't forget trend direction (up = good/green, down = bad/red). | Linear.app dashboard, Vercel.com analytics, Stripe.com dashboard |
| Timeline / Activity Feed | data | minimal enterprise saas | Vertical timeline with timestamps. Each entry: icon, title, description, time. Alternating or left-aligned. | Activity logs, changelog, audit trail | Don't use for >50 items without virtual scrolling. Don't make timestamps too prominent (use relative time). Don't forget to handle "loading more" state. | GitHub.com commit history, Linear.app activity, Notion.so page history |

### 2.2 Add compositions regression test

**File:** `tests/test_compositions_regression.py` (new)

```python
"""Regression tests for compositions search — ensures expanded data doesn't break known results."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from core import search

KNOWN_QUERIES = {
    "hero layout": ["Split Hero", "Full Bleed Hero", "Centered Text Hero"],
    "pricing": ["Pricing 3-Tier", "Feature Comparison", "Simple 2-Tier"],
    "dashboard": ["Bento Dashboard", "Sidebar + Content", "Command Palette"],
    "testimonial": ["Social Proof", "Testimonial", "Case Study"],
    "footer": ["Content Footer", "Sticky Footer", "Side CTA"],
}

class TestCompositionsRegression(unittest.TestCase):
    def test_top_queries_return_expected_patterns(self):
        for query, expected_top_patterns in KNOWN_QUERIES.items():
            with self.subTest(query=query):
                results = search(query, "compositions", max_results=3)
                self.assertGreater(results["count"], 0, f"Query '{query}' returned no results")
                returned_names = [r.get("name", "") for r in results["results"]]
                matches = [
                    exp.lower() in name.lower()
                    for name in returned_names
                    for exp in expected_top_patterns
                ]
                self.assertTrue(
                    any(matches),
                    f"Query '{query}' returned {returned_names}, expected one of {expected_top_patterns}"
                )

    def test_compositions_has_all_columns(self):
        results = search("hero", "compositions", max_results=1)
        self.assertEqual(results["domain"], "compositions")
        self.assertGreater(results["count"], 0)
        row = results["results"][0]
        for col in ["name", "category", "style_tags", "description", "use_cases", "anti_patterns", "examples"]:
            self.assertIn(col, row, f"Missing column: {col}")

if __name__ == "__main__":
    unittest.main()
```

### 2.3 Add TODO marker in compositions-detail.md

**File:** `references/compositions-detail.md`

Add after line 3:

```markdown
> **New patterns:** Forms, Auth, Onboarding, Navigation, Notifications, Empty States, 
> and Data Display patterns are defined in `data/compositions.csv` (searchable).
> ASCII diagrams for these patterns will be added in a future update.
```

---

## Phase 3: Critical Tests (1 hour)

### 3.1 Core search tests

**File:** `tests/test_core.py` (new)

```python
"""Tests for the BM25 search engine — protects critical paths."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from core import search, search_stack, detect_domain, BM25, CSV_CONFIG, AVAILABLE_STACKS

class TestSearch(unittest.TestCase):
    def test_product_search_returns_results(self):
        results = search("SaaS dashboard", "product")
        self.assertEqual(results["domain"], "product")
        self.assertGreater(results["count"], 0)
        self.assertIn("Product Type", results["results"][0])

    def test_style_search_returns_results(self):
        results = search("minimalism clean", "style")
        self.assertEqual(results["domain"], "style")
        self.assertGreater(results["count"], 0)

    def test_color_search_returns_results(self):
        results = search("fintech", "color")
        self.assertEqual(results["domain"], "color")
        self.assertGreater(results["count"], 0)
        self.assertIn("Primary", results["results"][0])

    def test_compositions_search_returns_results(self):
        results = search("hero", "compositions")
        self.assertEqual(results["domain"], "compositions")
        self.assertGreater(results["count"], 0)

    def test_typography_search_returns_results(self):
        results = search("elegant serif", "typography")
        self.assertEqual(results["domain"], "typography")
        self.assertGreater(results["count"], 0)

    def test_design_search_returns_results(self):
        results = search("cyberpunk", "design")
        self.assertEqual(results["domain"], "design")
        self.assertGreater(results["count"], 0)

    def test_domain_detection(self):
        self.assertEqual(detect_domain("SaaS dashboard"), "product")
        self.assertEqual(detect_domain("color palette hex"), "color")
        self.assertEqual(detect_domain("hero layout"), "compositions")
        self.assertEqual(detect_domain("font pairing"), "typography")
        self.assertEqual(detect_domain("chart graph"), "chart")

    def test_stack_search(self):
        results = search_stack("react", "react")
        self.assertEqual(results["domain"], "stack")
        self.assertEqual(results["stack"], "react")
        self.assertGreater(results["count"], 0)

    def test_unknown_stack_returns_error(self):
        results = search_stack("test", "nonexistent_stack")
        self.assertIn("error", results)

    def test_all_csvs_load(self):
        for domain, config in CSV_CONFIG.items():
            with self.subTest(domain=domain):
                filepath = Path(__file__).parent.parent / "data" / config["file"]
                self.assertTrue(filepath.exists(), f"Missing CSV: {config['file']}")

    def test_bm25_basic(self):
        bm25 = BM25()
        bm25.fit(["hello world", "foo bar baz", "hello foo"])
        scores = bm25.score("hello")
        self.assertEqual(len(scores), 3)
        self.assertGreater(scores[0][1], 0)

class TestSearchResultsStructure(unittest.TestCase):
    def test_search_result_has_required_keys(self):
        result = search("SaaS", "product")
        for key in ["domain", "query", "file", "count", "results"]:
            self.assertIn(key, result, f"Missing key: {key}")

    def test_results_are_dicts(self):
        result = search("minimalism", "style")
        for row in result["results"]:
            self.assertIsInstance(row, dict)

if __name__ == "__main__":
    unittest.main()
```

### 3.2 Anti-slop tests

**File:** `tests/test_anti_slop.py` (new)

```python
"""Tests for anti-slop detection patterns — ensures checks work."""

import unittest
import re
import tempfile
from pathlib import Path

class TestAntiSlopPatterns(unittest.TestCase):
    """Test regex patterns directly (no bash dependency)."""

    def _create_temp_file(self, content: str, suffix: str = ".css") -> Path:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    def test_purple_gradient_detection(self):
        pattern = re.compile(r'linear-gradient.*#(7c3aed|8b5cf6|a78bfa|6d28d9|5b21b6|4c1d95|9333ea)|linear-gradient.*(purple|violet)')
        self.assertTrue(pattern.search("background: linear-gradient(135deg, #7c3aed, #8b5cf6)"))
        self.assertTrue(pattern.search("background: linear-gradient(to right, purple, violet)"))
        self.assertFalse(pattern.search("background: linear-gradient(135deg, #2563eb, #3b82f6)"))

    def test_inter_sole_font_detection(self):
        pattern = re.compile(r"font-family.*Inter[\"']?\s*[;,]|fontFamily.*Inter")
        self.assertTrue(pattern.search("font-family: 'Inter', sans-serif;"))
        self.assertTrue(pattern.search('fontFamily: "Inter"'))
        self.assertFalse(pattern.search("font-family: 'Sora', sans-serif;"))

    def test_ai_buzzword_detection(self):
        pattern = re.compile(r'seamless(ly)?|leverage|cutting[- ]edge|game[- ]chang|revolutioniz|paradigm|empower|harness')
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
        pattern = re.compile(r'—|&#8212;')
        self.assertTrue(pattern.search("feature — not a bug"))
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
```

### 3.3 Design system tests

**File:** `tests/test_design_system.py` (new)

```python
"""Tests for design system generator — protects the generation pipeline."""

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
```

---

## Phase 4: Cleanup (15 min)

### 4.1 Add .gitignore

**File:** `.gitignore` (new, in skill root)

```
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.pytest_cache/
*.log
```

### 4.2 Clean __pycache__

```bash
rm -rf scripts/__pycache__
```

### 4.3 Archive PLAN-MCP.md

**File:** `PLAN-MCP.md`

Add at the top:

```markdown
> **STATUS: COMPLETED** (all 10 steps executed). Archived for reference.
```

---

## Execution Order

| Step | Time | What | Files |
|------|------|------|-------|
| 1 | 5 min | Fix quality-gate.md thresholds | `references/quality-gate.md` |
| 2 | 5 min | Fix version strings | `SKILL.md`, `references/memory-system.md`, `templates/AGENTS.md` |
| 3 | 5 min | Remove missing stacks | `SKILL.md` |
| 4 | 5 min | Fix Content Footer row (data bug) | `data/compositions.csv` |
| 5 | 5 min | Add .gitignore + clean pycache | `.gitignore`, `scripts/__pycache__/` |
| 6 | 30 min | Write test files | `tests/test_core.py`, `tests/test_anti_slop.py`, `tests/test_design_system.py` |
| 7 | 15 min | Write regression test | `tests/test_compositions_regression.py` |
| 8 | 3 hours | Expand compositions.csv | `data/compositions.csv` |
| 9 | 5 min | Add TODO marker | `references/compositions-detail.md` |
| 10 | 5 min | Archive PLAN-MCP.md | `PLAN-MCP.md` |
| 11 | 5 min | Run all tests | `python -m unittest discover tests/ -v` |

---

## Verification

After all changes:

```bash
# 1. Run all tests
python -m unittest discover tests/ -v
# Expected: OK (all tests pass)

# 2. Verify search still works
python scripts/search.py "SaaS dashboard" --design-system -p "Verify"
# Expected: ASCII box output with pattern, style, colors, typography

# 3. Verify compositions expanded
python scripts/search.py "hero" --domain compositions
# Expected: 3+ results including new patterns

# 4. Verify Content Footer fix
python scripts/search.py "footer" --domain compositions
# Expected: "Content Footer" appears with correct category "footer"

# 5. Verify anti-slop still works (Windows: use git bash)
bash scripts/anti-slop.sh scripts/
# Expected: RESULT: CLEAN

# 6. Verify no regressions in known queries
python -m unittest tests.test_compositions_regression -v
# Expected: OK
```

---

## What's NOT in This Plan (intentionally deferred)

| Feature | Why deferred |
|---------|-------------|
| Split design_system.py monolith | Works fine, one maintainer, coupling makes split messy |
| BM25 index cache | Negligible performance gain (~5ms), adds complexity |
| Multi-brand theming | No current use case |
| Design system docs generator | No current use case |
| Visual regression baselines | No current use case |
| Figma-to-component | No current use case |
| Auto quality gate execution | Manual works fine |
| Design system versioning | No current use case |
| CI pipeline for the skill | premature until there are contributors |
| New CLI flags (--brand, --docs, etc.) | No current use case |

---

## Key Findings from Re-Review

1. **Data bug found:** Content Footer row in compositions.csv has shifted columns — `style_tags` is missing, causing all fields to shift left. This affects search quality today.

2. **Monolith split is not worth it:** After re-reading the code, `design_system.py` has tight coupling between persistence, search, and generation. Splitting creates more confusion than it solves.

3. **Test assertions must be structural, not exact:** BM25 results change when data changes. Tests should assert `count > 0` and key presence, not exact values.

4. **Windows compatibility is critical:** The skill runs on Windows. All verification must include Windows testing with git bash.

5. **Bilingual README:** Any changes to README.md need Arabic translation. Internal files (references, tests) don't need translation.

6. **Import structure:** Scripts use `from core import search` which only works when run from within the `scripts/` directory. Tests must use `sys.path.insert()` to handle this.
