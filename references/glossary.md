# Glossary

Single source of truth for terminology (`03_WRITING_STANDARDS.md` §14 pattern). One definition per term. Reference files link here on first use; they do not redefine terms.

## Pipeline Terms

| Term | Definition |
|---|---|
| **Blueprint** | Phase 3 structured output: all 13 mandatory fields + Decision Briefs + Design Tokens, every field source-cited. The contract between design intent and code. |
| **Decision Brief** | Per-major-design-choice tradeoff statement. Five parts: **Advantages / Disadvantages / Alternatives (incl. doing nothing) / Appropriate situations / Inappropriate situations**. Replaces the earlier 3-part "Best case / Realistic / Risks". |
| **Decision Framework** | Blueprint block for major choices: Problem → Constraints → Options → Tradeoffs → Decision → Consequences. |
| **Design Tokens** | Named design values (color, type, spacing, motion) output in 3 formats: CSS custom properties, Tailwind config, JS/TS object. |
| **Design Lock** | `.design-lock.md` written after blueprint confirmation — the frozen style/color/type/layout contract re-read at every session start. |
| **Design DNA** | Structured JSON extracted from a reference design (URL/screenshot/Figma): colors, typography, layout, effects. Becomes the source citation for blueprint fields. |
| **Evidence Class** | Label on every blueprint citation: `[STANDARD]` (WCAG/W3C/MDN/official docs — for factual, a11y, performance claims), `[PRODUCT]` (real shipped screens — for aesthetic decisions), `[HEURISTIC]` (judgment, not verifiable). |
| **Fallback/Exception** | Blueprint field 14: one line stating when this design is the wrong answer and the recommended pivot (handbook "when NOT to use"). |
| **Pre-flight** | Phase 2.5 gate: inspiration (3 real products), difference, key move, composition, style, content — all answered before blueprint. Vague in = vague out. |

## Quality Terms

| Term | Definition |
|---|---|
| **Anti-Slop** | Deterministic checks for common AI tell-patterns (purple gradients, Inter-only, default Tailwind palette, pure black bg, buzzwords, gradient text, glass blur, equal 3-col grid, em-dashes, "Welcome to"). Run via `scripts/anti_slop.py` (Windows-safe) or legacy `scripts/anti-slop.sh`. |
| **Quality Gate** | Phase 5 enforcement: self-score 6 dimensions (0-120). 96-120 ship / 72-95 revise (max 3 iterations) / <72 redesign from Phase 3. Paste score + tool output as proof. |
| **Three States** | Every data/interactive component implements loading (skeleton), error (inline + retry), empty (CTA). All 3, always. |
| **Premium Signals** | Affirmative markers of "good" design per `premium-design-guide.md`: intentional spacing rhythm, editorial type scale, restrained palette, meaningful motion — the opposite of AI-slop. |
| **Acceptance** | Blueprint field 12: testable checkbox conditions that define "done" for the delivery. |

## Security Terms

| Term | Definition |
|---|---|
| **Security Level L1** | Public — static, portfolio, no login. |
| **Security Level L2** | Authenticated — SaaS, dashboard, e-commerce, sessions. |
| **Security Level L3** | Sensitive — fintech, healthcare, admin, PII. |
| Auto-detect during intake; override with "security level: [1/2/3]". Full checklists: `security-levels.md`. |

## Memory Terms

| Term | Definition |
|---|---|
| **AGENTS.md** | Project memory file auto-read by OpenCode each session. Max 60 lines. Never stale more than one session. |
| **DECISIONS.md** | `.context` log of architectural decisions (WHY, not WHAT) using the D-00N format: Context / Chose / Over / Because / Revisit. |
| **PROGRESS.md** | `.context` log of what's built, what's active, what's next, with a `LESSONS` block (what worked / failed / corrected, last 5 entries). |
| **PROJECT_BRIEF.md** | `.context` single source of truth for the project, written after blueprint confirmation, read first in every response. |

## Search Engine Terms

| Term | Definition |
|---|---|
| **Style** | One of 67 design styles in `data/styles.csv` (e.g., Neo Brutalism, Academia, Cyberpunk). Selected via `search.py --design-system` or `--domain design`. |
| **Composition Pattern** | One of 50+ layout patterns in `data/compositions.csv` (hero, pricing, auth, onboarding, empty states...). Selected via `--domain compositions`. |
| **Palette** | One of 161 color palettes in `data/colors.csv`, mapped to Primary/Secondary/Accent/Background/Text. |
| **Typography Pairing** | One of 57 pairings in `data/google-fonts.csv` — display + body, never "Inter + Inter". |