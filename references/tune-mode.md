# Tune Mode — Improving Existing UI

Load this file when the request is to improve, fix, redesign, or optimize an existing UI.

---

## STEP 1 — AUDIT

```
Issues Found:
- [VISUAL]       [Description + why it's wrong]
- [UX]           [Description + user impact]
- [PERFORMANCE]  [Description + metric affected]
- [A11Y]         [Description + WCAG criterion]
- [SECURITY]     [Description + vulnerability type]
- [STATES]       [Missing loading/error/empty states]
```

## STEP 2 — PROPOSE

Rank changes by user impact:

```
- [HIGH]   [Change] — expected improvement
- [MEDIUM] [Change] — expected improvement
- [LOW]    [Change] — expected improvement
```

**Decision Brief:** Best case / Realistic / Risks for each change.

## STEP 3 — IMPLEMENT

Apply changes surgically. Don't rebuild what isn't broken.

- Edit existing components, don't rewrite
- Follow the stack rules in `references/build-mode.md` §4c
- Respect the existing design system; match what's there

## STEP 4 — DIFF SUMMARY

```
Changed: [list of what changed]
Reason:  [why each change was made]
Result:  [expected measurable outcome]
```
