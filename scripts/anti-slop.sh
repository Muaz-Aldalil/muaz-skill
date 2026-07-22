#!/usr/bin/env bash
# anti-slop.sh — Deterministic AI-slop detection for frontend code
# Usage: bash scripts/anti-slop.sh <directory>
# Exit code: 0 = clean, 1 = violations found
# Agent MUST run this and paste output before claiming done.

set -uo pipefail

TARGET="${1:-.}"
VIOLATIONS=0
FAILS=""

rg_check() {
  local label="$1"
  shift
  local hits
  hits=$(rg -n --no-heading -g '*.{css,scss,tsx,jsx,ts,js,html}' "$@" "$TARGET" 2>/dev/null || true)
  if [ -n "$hits" ]; then
    VIOLATIONS=$((VIOLATIONS + 1))
    FAILS="$FAILS
FAIL [$label]:
$hits
"
  fi
}

# --- 1. Purple/violet gradients (most common AI tell) ---
rg_check "PURPLE_GRADIENT" -e 'linear-gradient.*#(7c3aed|8b5cf6|a78bfa|6d28d9|5b21b6|4c1d95|9333ea)' -e 'linear-gradient.*(purple|violet)'

# --- 2. Inter as sole/default font ---
rg_check "INTER_SOLE_FONT" -e "font-family.*Inter[\"']?\s*[;,]" -e "fontFamily.*Inter" --glob '*.css'
rg_check "INTER_TAILWIND" -e 'font-inter' -e 'fontFamily.*Inter'

# --- 3. Default Tailwind palette colors (no customization) ---
rg_check "TAILWIND_DEFAULT_BLUE" -e '(bg|text|border|ring|from|to|via)-(blue-[456]00)'
rg_check "TAILWIND_DEFAULT_PURPLE" -e '(bg|text|border|ring|from|to|via)-(purple-[456]00)'

# --- 4. Pure black (#000, #000000) as background ---
rg_check "PURE_BLACK_BG" -e 'background(-color)?:\s*(#000000|#000\b|black)' --glob '*.css'
rg_check "PURE_BLACK_TAILWIND" -e 'bg-black(?![0-9])'

# --- 5. AI buzzwords in visible text ---
rg_check "AI_BUZZWORDS" -e 'seamless(ly)?' -e 'leverage' -e 'cutting[- ]edge' -e 'game[- ]chang' -e 'revolutioniz' -e 'paradigm' -e 'empower' -e 'harness'

# --- 6. Gradient text (common AI decoration) ---
rg_check "GRADIENT_TEXT" -e 'background.*-clip:\s*text' -e 'text-transparent.*bg-clip'

# --- 7. Glassmorphism by reflex (not intentional) ---
rg_check "GLASS_BLUR" -e 'backdrop-blur' -e 'backdrop-filter.*blur'

# --- 8. Equal-width 3-column grid (lazy layout) ---
rg_check "EQUAL_3_COL" -e 'grid-cols-3(?!.*minmax)'

# --- 9. Em-dashes in copy (AI writing tell) ---
rg_check "EM_DASH" -e '—' -e '&#8212;' --glob '*.tsx'

# --- 10. "Welcome to" in hero (cliche) ---
rg_check "WELCOME_HERO" -e 'Welcome\s+to' --glob '*.tsx'

echo "=== MUAZ-V3 ANTI-SLOP CHECK ==="
echo "Target: $TARGET"
echo ""

if [ $VIOLATIONS -gt 0 ]; then
  echo "RESULT: $VIOLATIONS VIOLATION GROUPS FOUND"
  echo "$FAILS"
  echo "ACTION REQUIRED: Fix all violations before claiming done."
  echo "Run again after fixes to verify."
  exit 1
else
  echo "RESULT: CLEAN — no pattern violations detected."
  echo "NOTE: This checks patterns only. Manual review still required for:"
  echo "  - Layout balance and whitespace"
  echo "  - Typography hierarchy and restraint"
  echo "  - Color palette cohesion"
  echo "  - Motion quality and timing"
  echo "  - Content tone and specificity"
  exit 0
fi
