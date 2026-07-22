# Quality Gate

Scoring rubric + enforcement flow. Agent MUST score before claiming done. No exceptions.

---

## Enforcement Flow

```
Phase 5:
  1. Run anti-slop.sh → fix any pattern violations
  2. Self-score below → get total (0-120)
  3. If total < 96 → fix weakest dimension → re-score
  4. Max 3 iterations. If still < 96 after 3 → redesign from Phase 3.
  5. Paste final score + anti-slop.sh output as proof.
```

**Highest-leverage rule:** Do not claim "done" without tool-verified proof. Paste the proof in your response. Verbal assertions without tool evidence are defects.

---

## Self-Score Rubric (6 dimensions, 0-20 each, total 0-120)

### Dimension 1: Visual Coherence (0-20)

| Score | Criteria |
|---|---|
| 0-5 | Random styles, no consistent palette, mixed font families |
| 6-10 | Consistent palette but no hierarchy, spacing is arbitrary |
| 11-15 | Clear palette + hierarchy, some spacing consistency, minor inconsistencies |
| 16-18 | Cohesive design system, consistent tokens, intentional spacing rhythm |
| 19-20 | Every element feels intentional, consistent micro-details, premium polish |

**Check:** Do all colors come from the blueprint? Is typography consistent across all sections? Is spacing on a grid?

### Dimension 2: Layout & Structure (0-20)

| Score | Criteria |
|---|---|
| 0-5 | Centered-everything, 3-col equal grid, no visual hierarchy |
| 6-10 | Basic hierarchy but default layout patterns, minimal whitespace |
| 11-15 | Intentional layout choices, good whitespace, some editorial/creative layouts |
| 16-18 | Strong visual hierarchy, asymmetric layouts, whitespace as design element |
| 19-20 | Every section has distinct structure, flow is intentional, layout serves content |

**Check:** Does the layout avoid the AI default (centered hero → 3-col features → centered CTA)? Is whitespace >= 96px between major sections?

### Dimension 3: Typography Quality (0-20)

| Score | Criteria |
|---|---|
| 0-5 | Single font, no hierarchy, poor line-height, hard to read |
| 6-10 | Basic hierarchy but generic font choice, no tracking调整 |
| 11-15 | Good pairing, clear hierarchy, appropriate line-height and length |
| 16-18 | Editorial quality, tracking adjustments, consistent scale |
| 19-20 | Typography IS the design, every text element intentional, premium feel |

**Check:** Is display font 3.5-4x body? Is tracking adjusted for headings? Is line length 60-75ch? Is there only 1-2 font families?

### Dimension 4: Motion & Interaction (0-20)

| Score | Criteria |
|---|---|
| 0-5 | No animations or instant transitions, feels static |
| 6-10 | Basic hover effects, inconsistent timing |
| 11-15 | Consistent easing, 150-300ms transitions, some scroll reveals |
| 16-18 | Premium easing (cubic-bezier(0.16,1,0.3,1)), staggered animations, respects prefers-reduced-motion |
| 19-20 | Motion serves UX purpose, every interaction feels responsive and polished |

**Check:** Are all transitions 150-300ms? Is the premium easing used? Are scroll reveals present? Does prefers-reduced-motion work?

### Dimension 5: Content & Copy (0-20)

| Score | Criteria |
|---|---|
| 0-5 | Lorem ipsum, placeholder text, AI buzzwords, generic copy |
| 6-10 | Real text but generic, some buzzwords, em-dashes present |
| 11-15 | Specific copy, no buzzwords, active voice, concrete claims |
| 16-18 | Brand voice consistent, compelling value props, no filler |
| 19-20 | Copy is a design element, every word earns its place, specific metrics |

**Check:** Is there any Lorem ipsum? Any em-dashes? Any banned phrases from premium-design-guide.md? Is copy specific with numbers/metrics?

### Dimension 6: Design Grounding (0-20)

| Score | Criteria |
|---|---|
| 0-5 | No real references, entirely invented from training data |
| 6-10 | Some references but generic ("I looked at Stripe") |
| 11-15 | Specific references with pattern analysis ("3/5 pricing pages use 3-tier grid") |
| 16-18 | Deep pattern analysis, multiple sources, every decision traced |
| 19-20 | Every design decision cites specific evidence from real shipped products |

**Check:** Is blueprint field 13 (DESIGN EVIDENCE) filled? Are references specific (not just "Stripe")? Did agent search Mobbin or use user-provided references? Can every color/layout/typography choice be traced to a source?

---

## Score Thresholds

Total is now 0-120 (6 dimensions × 0-20).

| Total | Action |
|---|---|
| 96-120 | **Ship.** Paste score + proof. |
| 72-95 | **Revise.** Fix weakest dimension(s), re-score. Max 3 iterations. |
| < 72 | **Redesign.** Return to Phase 3. Blueprint needs rethinking. |

---

## AI-Slop Detection Checklist

Deterministic checks (anti-slop.sh handles these automatically):
- [ ] No purple/violet gradient as primary
- [ ] No Inter as sole font family
- [ ] No default Tailwind blue-500/purple-500 as primary
- [ ] No pure #000 background
- [ ] No gradient text (background-clip: text)
- [ ] No backdrop-blur as decorative element
- [ ] No emoji as UI icons
- [ ] No "Welcome to" in hero
- [ ] No AI buzzwords in copy

Manual checks (agent must verify):
- [ ] No centered hero as sole layout pattern
- [ ] No 3 equal-width columns as sole grid
- [ ] No symmetric feature grid without visual hierarchy
- [ ] No stock photo + gradient overlay
- [ ] No glassmorphism by reflex
- [ ] No rounded-full pill buttons as only button style
- [ ] No generic SaaS page structure (hero→features→pricing→testimonials→footer)
- [ ] No em-dashes in copy
- [ ] No filler buzzword copy

---

## Verifiable Proof Requirements

Before claiming "done", the agent MUST paste:

1. **anti-slop.sh output** — full script output showing CLEAN or violations fixed
2. **Self-score** — scores for all 6 dimensions with rationale
3. **Total score** — sum with ship/revise/redesign decision
4. **If revised** — what changed between iterations

Verbal claims without tool evidence are defects.

---

## Iteration Protocol

```
Iteration 1: Score → identify weakest dimension → fix → re-score
Iteration 2: Score → fix next weakest → re-score
Iteration 3: Score → if still < 72, redesign from Phase 3

If iteration 3 fails:
  "Quality gate failed after 3 iterations. Returning to Phase 3
   to redesign the blueprint. The current approach isn't reaching
   premium quality. Need different layout/typography/color strategy."
```
