#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".next", ".venv", "venv", "dist", "build", ".pytest_cache"}

ALL_FILES = "**/*.{css,scss,tsx,jsx,ts,js,html}"
CSS_FILES = "**/*.{css,scss}"
TSX_FILES = "**/*.tsx"

CHECKS = [
    {
        "label": "PURPLE_GRADIENT",
        "patterns": [
            re.compile(r'linear-gradient.*#(7c3aed|8b5cf6|a78bfa|6d28d9|5b21b6|4c1d95|9333ea)', re.I),
            re.compile(r'linear-gradient.*(purple|violet)', re.I),
        ],
        "glob": ALL_FILES,
    },
    {
        "label": "INTER_SOLE_FONT",
        "patterns": [re.compile(r'font-family.*Inter["\']?\s*[;,]', re.I)],
        "glob": CSS_FILES,
    },
    {
        "label": "INTER_TAILWIND",
        "patterns": [re.compile(r'font-inter', re.I), re.compile(r'fontFamily.*Inter')],
        "glob": ALL_FILES,
    },
    {
        "label": "TAILWIND_DEFAULT_BLUE",
        "patterns": [re.compile(r'\b(bg|text|border|ring|from|to|via)-(blue-[456]00)\b')],
        "glob": ALL_FILES,
    },
    {
        "label": "TAILWIND_DEFAULT_PURPLE",
        "patterns": [re.compile(r'\b(bg|text|border|ring|from|to|via)-(purple-[456]00)\b')],
        "glob": ALL_FILES,
    },
    {
        "label": "PURE_BLACK_BG",
        "patterns": [re.compile(r'background(-color)?:\s*(#000000|#000\b|black)', re.I)],
        "glob": CSS_FILES,
    },
    {
        "label": "PURE_BLACK_TAILWIND",
        "patterns": [re.compile(r'bg-black(?![0-9])')],
        "glob": ALL_FILES,
    },
    {
        "label": "AI_BUZZWORDS",
        "patterns": [
            re.compile(r'seamless(ly)?|leverage|cutting[- ]edge|game[- ]chang|revolutioniz|paradigm|empower|harness', re.I)
        ],
        "glob": ALL_FILES,
    },
    {
        "label": "GRADIENT_TEXT",
        "patterns": [
            re.compile(r'background.*-clip:\s*text', re.I),
            re.compile(r'text-transparent.*bg-clip'),
        ],
        "glob": ALL_FILES,
    },
    {
        "label": "GLASS_BLUR",
        "patterns": [re.compile(r'backdrop-blur'), re.compile(r'backdrop-filter.*blur', re.I)],
        "glob": ALL_FILES,
    },
    {
        "label": "EQUAL_3_COL",
        "patterns": [re.compile(r'grid-cols-3(?!.*minmax)')],
        "glob": ALL_FILES,
    },
    {
        "label": "EM_DASH",
        "patterns": [re.compile(r'—'), re.compile(r'&#8212;')],
        "glob": TSX_FILES,
    },
    {
        "label": "WELCOME_HERO",
        "patterns": [re.compile(r'Welcome\s+to', re.I)],
        "glob": TSX_FILES,
    },
]


def _expand_braces(pattern: str) -> list:
    if "{" not in pattern:
        return [pattern]
    start, rest = pattern.split("{", 1)
    body, tail = rest.split("}", 1)
    return [start + choice + tail for choice in body.split(",")]


def matches_glob(path: Path, pattern: str) -> bool:
    suffix_part = pattern.split("**/", 1)[1] if "**/" in pattern else pattern
    return any(Path(path.name).match(expanded) for expanded in _expand_braces(suffix_part))


def get_candidate_files(target: Path) -> list:
    files = []
    if target.is_file():
        return [target]
    for path in target.rglob("*"):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.parts):
            files.append(path)
    return files


def scan(target: Path):
    files = get_candidate_files(target)
    results = {}
    for check in CHECKS:
        hits = []
        for path in files:
            if not matches_glob(path, check["glob"]):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lines = text.splitlines()
            for index, line in enumerate(lines, start=1):
                if any(pattern.search(line) for pattern in check["patterns"]):
                    hits.append(f"{path}:{index}:{line.strip()}")
        if hits:
            results[check["label"]] = hits
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(prog="anti-slop.py", description="Deterministic AI-slop detection for frontend code")
    parser.add_argument("target", nargs="?", default=".", help="directory or file to scan")
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"ERROR: target does not exist: {target}", file=sys.stderr)
        return 2

    results = scan(target)

    print("=== MUAZ-V3 ANTI-SLOP CHECK ===")
    print(f"Target: {target}")
    print("")

    if results:
        print(f"RESULT: {len(results)} VIOLATION GROUPS FOUND")
        for label, hits in results.items():
            print(f"FAIL [{label}]:")
            for hit in hits:
                print(hit)
            print("")
        print("ACTION REQUIRED: Fix all violations before claiming done.")
        print("Run again after fixes to verify.")
        return 1
    else:
        print("RESULT: CLEAN - no pattern violations detected.")
        print("NOTE: This checks patterns only. Manual review still required for:")
        print("  - Layout balance and whitespace")
        print("  - Typography hierarchy and restraint")
        print("  - Color palette cohesion")
        print("  - Motion quality and timing")
        print("  - Content tone and specificity")
        return 0


if __name__ == "__main__":
    sys.exit(main())