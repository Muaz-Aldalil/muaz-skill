# Build Mode — Full Pipeline for Building New Projects

Load this file when the request is to build, create, design, or scaffold a website/page/UI.

---

## PHASE 1A — AUTO-DETECT (run before intake questions)

Before asking ANY questions, read the project. This is mandatory — never ask what you can read.

### Detection Steps (in order)

1. **Read `package.json`** → stack, dependencies, scripts, framework version
2. **Read `tailwind.config.*`** → colors, fonts, spacing, theme config
3. **Read `src/app/` or `src/pages/`** → page inventory, routing structure
4. **Read `src/components/`** → component count, naming patterns
5. **Read `*.css` or `globals.css`** → design tokens, CSS variables, existing palette
6. **Read `README.md`** → project description, goals, tech choices
7. **Read `.env*`** → API providers, auth services, endpoints
8. **Read `next.config.*` or `vite.config.*`** → build config, deployment target
9. **Run `git log --oneline -5`** → recent changes, contributors
10. **Read `tsconfig.json`** → TypeScript strict mode, path aliases

### Fallback Logic

| Detection result | Action |
|---|---|
| ALL detection fails | Skip to asking all questions from scratch |
| Partial detection | Show summary, ask only gaps |
| Full detection | Pre-fill defaults, confirm with user |

### Project Type Detection (for skip logic)

| Type | Trigger keywords | Questions to skip |
|---|---|---|
| Landing page | "landing", "page", "coming soon" | AUTH, API, STATE |
| Portfolio | "portfolio", "personal", "blog" | AUTH, API, STATE |
| Docs | "docs", "documentation", "wiki" | AUTH, API, STATE |
| SaaS | "saas", "dashboard", "admin", "app" | None |
| E-commerce | "shop", "store", "ecommerce", "cart" | None |
| Blog | "blog", "news", "articles" | AUTH, STATE |

### Detection Summary Format

```
I analyzed your project. Here's what I found:

STACK: [detected or "Not detected — starting from scratch"]
DESIGN SYSTEM: [detected or "None found — will generate"]
PAGES: [detected list or "No routing detected"]
COMPONENTS: [count or "None found"]
BRAND: [detected assets or "No brand assets found"]

Is this correct? I'll ask about what's missing next.
```

See `references/intake-template.md` for full question list, defaults, and confirmation format.

---

## PHASE 2 — DESIGN SYSTEM REASONING

Always generate a design system first.

### Primary: Search Engine
```bash
python scripts/search.py "<query>" --design-system [-p "Project Name"]
```
Returns: pattern, style, colors, typography, effects, anti-patterns, checklist.
See `references/search-guide.md` for all flags and domains.

### Secondary: Design Reference
If user provided a URL, screenshot, or Figma link:
1. Load `references/design-reference-workflow.md`
2. Extract design DNA (colors, typography, layout, effects)
3. Cross-reference with search engine results
4. Merge: reference aesthetic + product-appropriate structure

### Design Domain Search
```bash
python scripts/search.py "<style name>" --domain design
```
Returns: detailed design system prompts for 16 styles (Bauhaus, Monochrome, Modern Dark, SaaS, Terminal, Kinetic, Flat Design, Material Design, Neo Brutalism, Bold Typography, Academia, Cyberpunk, Claymorphism, Enterprise, Sketch, Neumorphism).

### Composition Patterns
```bash
python scripts/search.py "<layout type>" --domain compositions
```
Returns: layout patterns with use cases, anti-patterns, and real product examples. Search by category (hero, features, pricing, testimonials, layout, dashboard, cta) or style tags (minimal, bold, editorial, dark, luxury, playful).

### Fallback: Universal Color & Typography Rules
```
COLORS: Primary (actions) / Secondary (surfaces) / Accent (<=10% of screen) /
        Background (offset +/-3-5% from pure black/white) / Text (>=4.5:1 contrast)
        Never more than 4 intentional colors + neutrals.

TYPE:   Display (expressive headings) / Body (16px min, 1.6 line-height) /
        Mono (only when semantic). Google Fonts only.
```

---

## PHASE 2.5 — PRE-FLIGHT (Mandatory before blueprint)

Complete every item before writing the blueprint. If you can't answer, you can't proceed.

### Design Thinking Checklist

```
1. INSPIRATION: Name 3 real products this design is inspired by.
   → Must be from references/premium-design-guide.md or compositions-detail.md
   → "I'll make it look good" is not an answer.

2. DIFFERENCE: What's different about YOUR version?
   → Cannot be identical to any single reference.
   → Must combine elements from 2+ references or add a unique twist.

3. KEY MOVE: What's the ONE design move that makes this premium?
   → Stripe: weight 300 everywhere + blue-tinted neutrals
   → Linear: 15px body + four-step surface ladder
   → Medium: 120px serif headline at whisper weight
   → YOURS: [must name one]

4. COMPOSITION: Which layout pattern?
   → Run: python scripts/search.py "<query>" --domain compositions
   → Must select one primary pattern per section.

5. STYLE: Which design system?
   → Run: python scripts/search.py "<query>" --domain design
   → Must select one style before blueprint.

6. CONTENT: Write the actual headline and body copy.
   → No placeholder text. No "lorem ipsum".
   → Every word must be specific to this project.
```

**Gate:** If any item is blank or vague, fix it before Phase 3. The blueprint is a contract — vague in = vague out.

---

## PHASE 3 — STRUCTURED BLUEPRINT

Output the structured blueprint before any code. Every field must have a source citation.

### Mandatory Fields (all required before Phase 4)

```
BLUEPRINT: [Project Name]
Source: [AGENTIC]|[CHAT+SEARCH]|[PURE CHAT]
Design Reference: [URL/screenshot/Figma if provided, else "none"]

1. GOAL: [one sentence — what this does]
2. PERSONAS: [who uses this — one line]
3. STACK: [React|Next|Vue|HTML+Tailwind|etc]
4. PATTERN: [landing|dashboard|ecommerce|portfolio|docs|etc — from search engine]
5. STYLE: [style name — must come from search engine or design reference]
6. THEME: [light|dark|both]
7. COLORS:
   - Primary: [hex] — [why: source citation]
   - Secondary: [hex] — [why: source citation]
   - Accent: [hex] — [why: source citation]
   - Background: [hex] — [why]
   - Surface: [hex] — [why]
   - Text: [hex] — [contrast ratio]
8. TYPOGRAPHY:
   - Display: [font] [weight] [tracking] — [source]
   - Body: [font] [weight] [size] — [source]
   - Mono: [font] — [if needed, else "none"]
9. LAYOUT: [editorial|split|bento|masonry|single-col — must differ from industry default]
10. KEY EFFECTS: [scroll reveals, hover states, transitions — specific, not "animations"]
11. ANTI-PATTERNS: [what's avoided for this specific project]
12. ACCEPTANCE: [testable conditions, checkbox list]
13. DESIGN EVIDENCE: [list 3-5 real product screens that informed this design]
    — must come from Mobbin search, user-provided reference, or Figma MCP
    — "invented from training data" is not valid evidence
    — if Mobbin MCP unavailable, cite search.py results or user references
```

### Design Tokens Output
Always output 3 formats immediately after blueprint:
- CSS custom properties (with dark mode override block)
- Tailwind config extension
- JS/TS tokens object
- Full templates: `references/design-tokens.md`

### Design Lock
After blueprint is confirmed, write `.design-lock.md`:
```markdown
# Design Lock — [Project Name]
Locked: [date]
Style: [style name]
Colors: [primary hex]
Typography: [display font] + [body font]
Layout: [layout pattern]
```
Re-read at every session start. Override only with explicit user confirmation.

**Interactive mode:** "Blueprint confirmed? Adjust anything before I build?"
**Agentic mode:** proceed directly to Phase 4.

---

## PHASE 4 — CODE GENERATION

### 4a — Project Init (scaffold project per stack)

| Stack | Command |
|---|---|
| React + Vite | `npm create vite@latest . -- --template react-ts` |
| Next.js | `npx create-next-app@latest . -- --typescript --tailwind --app` |
| Vue | `npm create vue@latest .` |
| Nuxt | `npx nuxi init .` |
| Astro | `npm create astro@latest . -- --template basics --typescript` |
| Svelte | `npm create vite@latest . -- --template svelte-ts` |
| HTML+Tailwind | `npm create vite@latest . -- --template vanilla` + `npm install -D tailwindcss @tailwindcss/vite` |
| React Native | `npx react-native init ProjectName --template react-native-template-typescript` |
| Flutter | `flutter create . --platforms=ios,android,web` |
| SwiftUI | Xcode → New Project → iOS App (SwiftUI) |

### 4b — Universal Code Quality (applies to every stack)

```
STRUCTURE     -> semantic HTML, mobile-first CSS, logical section order
PERFORMANCE   -> no unused imports, lazy-load images, font preconnect+swap,
                 critical CSS inline, no layout shift
ACCESSIBILITY -> WCAG AA contrast, aria-label on icon buttons, visible focus,
                 keyboard nav, alt text, prefers-reduced-motion respected
INTERACTIONS  -> cursor-pointer on all clickables, 150-300ms hover transitions,
                 44x44px min touch targets
ICONS         -> SVG only (Heroicons/Lucide/Phosphor), never emoji as UI icon
STATES        -> every interactive/data component handles:
                 Loading (skeleton) / Error (inline+retry) / Empty (CTA) / Disabled
```

### 4z — Anti-Slop Generation Rules (enforce during code, not after)

```
VISUAL BANS:
  NO gradient heroes — use palette from blueprint, not a background gradient
  NO gradient text on headings — solid color only
  NO symmetric 3-column feature grids as the sole layout
  NO centered hero → features → pricing → testimonials → footer (the SaaS template)
  NO stock photo + gradient overlay hero
  NO glassmorphism / frosted glass as decorative element
  NO rounded-full pill buttons as the only button style
  NO purple/indigo/teal as primary unless blueprint explicitly calls for it

CONTENT BANS:
  NO "Revolutionize your workflow" / "Empower your team" / "Seamlessly integrate"
  NO "Built for modern teams" / "The future of X" / "Unlock your potential"
  NO filler buzzword copy — use specific, concrete language

LAYOUT RULES:
  LAYOUT must be named in blueprint and must differ from the industry default
  Every page must have a distinct section structure — no two pages identical
  COLOR reasoning required: "Primary is X because Y" — not just a hex dump
  TYPOGRAPHY must be a pairing with rationale, not "Inter + Inter"
```

### 4c — Stack-Specific Rules

```
HTML+Tailwind -> CDN v3+, CSS vars in <style>, vanilla JS scoped at bottom
React/Next    -> functional+hooks, lucide-react icons, next/font for fonts
Vue/Nuxt      -> <script setup>, scoped styles, useHead() for fonts
Svelte/Astro  -> component-native styles, minimal JS, CSS animations preferred
Angular       -> services for state, SCSS + CSS custom properties
SwiftUI       -> @State/@Binding, native fonts, SF Symbols
Flutter       -> Widget tree, Material/Cupertino, ThemeData
React Native  -> StyleSheet, platform-specific extensions, FlashList
```

### 4d — Common Professional UI Rules

| Rule | Standard | Avoid |
|---|---|---|
| No Emoji as Icons | SVG icons (Lucide, Heroicons) | Emoji for nav/settings/controls |
| Vector-Only Assets | SVG or platform vector icons | Raster PNG that blur |
| Consistent Icon Sizing | Design tokens (icon-sm/md/lg) | Arbitrary 20/24/28px mixing |
| Stroke Consistency | Same stroke width per layer | Mixing thick/thin strokes |
| Filled vs Outline | One icon style per hierarchy | Mixing filled/outline at same level |
| Touch Targets | >=44x44pt (iOS), >=48dp (Android) | Small icons without hitSlop |
| Tap Feedback | Visual feedback within 80-150ms | No response on tap |
| Animation Timing | 150-300ms micro-interactions | Instant or >500ms |
| Disabled State | Reduced opacity + no interaction | Looks tappable but does nothing |
| Safe Areas | Respect notch/Dynamic Island/home indicator | Content under OS chrome |
| Dark Mode Text | Primary >=4.5:1, Secondary >=3:1 | Text blending into background |
| Semantic Tokens | CSS vars mapped per theme | Hardcoded per-screen hex values |
| 8dp Rhythm | 4/8dp incremental spacing | Random spacing values |

### 4e — Priority Rules (from ui-ux-pro-max)

#### Priority 1: Accessibility (CRITICAL)
- color-contrast — Minimum 4.5:1 for normal text (large text 3:1)
- focus-states — Visible focus rings on interactive elements (2-4px)
- alt-text — Descriptive alt text for meaningful images
- aria-labels — aria-label for icon-only buttons
- keyboard-nav — Tab order matches visual; full keyboard support
- heading-hierarchy — Sequential h1->h6, no level skip
- color-not-only — Don't convey info by color alone (add icon/text)
- reduced-motion — Respect prefers-reduced-motion; reduce/disable animations
- skip-links — Skip to main content for keyboard users
- voiceover-sr — Meaningful accessibilityLabel; logical reading order
- escape-routes — Cancel/back in modals and multi-step flows
- dynamic-type — Support system text scaling; avoid truncation

#### Priority 2: Touch & Interaction (CRITICAL)
- touch-target-size — Min 44x44pt (iOS) / 48x48dp (Material)
- touch-spacing — Minimum 8px/8dp gap between touch targets
- hover-vs-tap — Use click/tap for primary; don't rely on hover alone
- loading-buttons — Disable button during async; show spinner/progress
- error-feedback — Clear error messages near problem field
- cursor-pointer — Add cursor-pointer to clickable elements (Web)
- tap-delay — Use touch-action: manipulation to reduce 300ms delay (Web)
- press-feedback — Visual feedback on press (ripple/highlight)
- system-gestures — Don't block system gestures (back swipe, Control Center)
- safe-area-awareness — Keep touch targets away from notch/Dynamic Island/gesture bar
- swipe-clarity — Swipe actions must show clear affordance
- no-precision-required — Avoid requiring pixel-perfect taps

#### Priority 3: Performance (HIGH)
- image-optimization — WebP/AVIF, responsive images (srcset/sizes), lazy load
- image-dimension — Declare width/height or aspect-ratio to prevent CLS
- font-loading — Use font-display: swap/optional to avoid FOIT
- lazy-loading — Lazy load non-hero components (dynamic import / route splitting)
- bundle-splitting — Split code by route/feature to reduce initial load
- third-party-scripts — Load async/defer; audit and remove unnecessary ones
- reduce-reflows — Batch DOM reads then writes; avoid layout thrashing
- content-jumping — Reserve space for async content to prevent CLS
- virtualize-lists — Virtualize lists with 50+ items
- main-thread-budget — Keep per-frame work under ~16ms for 60fps
- progressive-loading — Use skeleton screens instead of long spinners
- debounce-throttle — Use debounce/throttle for scroll/resize/input events

#### Priority 4: Style Selection (HIGH)
- style-match — Match style to product type (use --design-system)
- consistency — Same style across all pages
- no-emoji-icons — Use SVG icons (Heroicons, Lucide), not emojis
- color-palette-from-product — Choose palette from product/industry
- effects-match-style — Shadows, blur, radius aligned with chosen style
- platform-adaptive — Respect platform idioms (iOS HIG vs Material)
- state-clarity — Distinct hover/pressed/disabled states on-style
- icon-style-consistent — One icon set across the product
- primary-action — Each screen has one primary CTA; secondary subordinate

#### Priority 5: Layout & Responsive (HIGH)
- viewport-meta — width=device-width initial-scale=1 (never disable zoom)
- mobile-first — Design mobile-first, scale up to tablet/desktop
- breakpoint-consistency — Systematic breakpoints (375/768/1024/1440)
- readable-font-size — Minimum 16px body text on mobile
- line-length-control — Mobile 35-60 chars; desktop 60-75 chars
- horizontal-scroll — No horizontal scroll on mobile
- spacing-scale — 4pt/8dp incremental spacing system
- container-width — Consistent max-width on desktop (max-w-6xl/7xl)
- z-index-management — Defined layered z-index scale (0/10/20/40/100/1000)
- scroll-behavior — Avoid nested scroll regions
- viewport-units — Prefer min-h-dvh over 100vh on mobile
- visual-hierarchy — Hierarchy via size, spacing, contrast — not color alone

#### Priority 6: Typography & Color (MEDIUM)
- line-height — 1.5-1.75 for body text
- line-length — Limit to 65-75 characters per line
- font-pairing — Match heading/body font personalities
- font-scale — Consistent type scale (12/14/16/18/24/32)
- contrast-readability — Darker text on light backgrounds
- color-semantic — Semantic tokens (primary, secondary, error, surface), not raw hex
- color-dark-mode — Desaturated/lighter tonal variants for dark mode
- color-accessible-pairs — Foreground/background must meet 4.5:1 (AA)
- truncation-strategy — Prefer wrapping over truncation
- letter-spacing — Respect default per platform; avoid tight tracking on body
- number-tabular — Tabular/monospaced figures for data columns, prices, timers
- whitespace-balance — Use whitespace intentionally to group related items

#### Priority 7: Animation (MEDIUM)
- duration-timing — 150-300ms for micro-interactions; complex <=400ms
- transform-performance — Use transform/opacity only; never width/height/top/left
- loading-states — Show skeleton/progress when loading >300ms
- easing — ease-out for entering, ease-in for exiting; avoid linear
- motion-meaning — Every animation expresses cause-effect relationship
- state-transition — Smooth transitions for hover/active/expanded, not snap
- continuity — Page transitions maintain spatial continuity (shared element, slide)
- exit-faster-than-enter — Exit ~60-70% of enter duration
- interruptible — Animations must be interruptible; user tap cancels immediately
- motion-consistency — Unify duration/easing tokens globally
- layout-shift-avoid — Animations must not cause CLS; use transform

#### Priority 8: Forms & Feedback (MEDIUM)
- input-labels — Visible label per input (not placeholder-only)
- error-placement — Show error below the related field
- submit-feedback — Loading then success/error state on submit
- required-indicators — Mark required fields (e.g. asterisk)
- empty-states — Helpful message and action when no content
- toast-dismiss — Auto-dismiss toasts in 3-5s
- confirmation-dialogs — Confirm before destructive actions
- inline-validation — Validate on blur (not keystroke)
- input-type-keyboard — Use semantic input types (email, tel, number) for mobile keyboard
- password-toggle — Show/hide toggle for password fields
- autofill-support — Use autocomplete/textContentType attributes
- multi-step-progress — Step indicator + back navigation in multi-step flows
- error-clarity — State cause + how to fix (not just "Invalid input")
- touch-friendly-input — Mobile input height >=44px

#### Priority 9: Navigation Patterns (HIGH)
- bottom-nav-limit — Bottom navigation max 5 items; labels + icons
- drawer-usage — Drawer/sidebar for secondary navigation, not primary
- back-behavior — Predictable and consistent back; preserve scroll/state
- deep-linking — Key screens reachable via deep link/URL
- nav-state-active — Current location visually highlighted (color, weight, indicator)
- nav-hierarchy — Primary vs secondary navigation clearly separated
- modal-escape — Clear close/dismiss affordance; swipe-down on mobile
- state-preservation — Navigating back restores scroll position, filter state, input
- adaptive-navigation — Large screens (>=1024px) sidebar; small screens bottom/top nav
- avoid-mixed-patterns — Don't mix Tab + Sidebar + Bottom Nav at same level
- focus-on-route-change — Move focus to main content for screen readers

#### Priority 10: Charts & Data (LOW)
- chart-type — Match chart type to data (trend->line, comparison->bar, proportion->pie)
- color-guidance — Accessible palettes; avoid red/green only for colorblind
- data-table — Provide table alternative for screen readers
- legend-visible — Always show legend; position near chart
- tooltip-on-interact — Tooltips on hover (Web) or tap (mobile) showing exact values
- axis-labels — Label axes with units; avoid truncated/rotated labels on mobile
- responsive-chart — Charts reflow or simplify on small screens
- empty-data-state — Meaningful empty state, not blank chart
- loading-chart — Skeleton shimmer while data loads
- large-dataset — Aggregate or sample 1000+ points; provide drill-down
- number-formatting — Locale-aware formatting for numbers, dates, currencies
- no-pie-overuse — Avoid pie/donut for >5 categories; use bar chart

### 4f — Testing Strategy

| Stack | Unit | Component | E2E |
|---|---|---|---|
| React/Vite | Vitest + @testing-library/react | Storybook + test-runner | Playwright |
| Next.js | Vitest/Jest + testing-library | Storybook + test-runner | Playwright |
| Vue | Vitest + @vue/test-utils | Storybook | Playwright / Cypress |
| Angular | Jest + Angular Testing Library | Storybook | Playwright / Cypress |
| Svelte | Vitest + svelte-testing-library | Storybook | Playwright |
| React Native | Jest + @testing-library/react-native | Storybook | Detox |
| Flutter | flutter_test | widget tests | integration_test |

**Naming**: `ComponentName.test.tsx` co-located with the component. E2E in `e2e/` at root.

**Coverage targets**: Unit >= 80%, critical user flows covered by E2E.

**What to test**: API integration (mock service layer), user interactions (click/submit), state transitions (loading→error→success), accessibility (jest-axe).

### 4g — Animation Decision Framework

| Need | Best tool | When NOT to use |
|---|---|---|
| Micro-interactions (hover, press) | CSS transitions | Don't need JS lib |
| Scroll reveals (fade/slide on viewport enter) | IntersectionObserver + CSS | Can use Framer if already in project |
| Page transitions (route change) | View Transitions API (Chrome 111+) or Framer | No JS needed for native VT |
| Shared element / hero animations | Framer Motion `LayoutGroup` | CSS can't do this |
| Complex timelines (choreography) | GSAP or CSS `@keyframes` | Framer overhead for simple sequences |
| SVG line drawing / morphing | GSAP MorphSVG | Overkill for single shapes |
| Drag / reorder | Framer Motion `Reorder` | React DnD alternative |

**Defaults**: CSS for hover/press/scroll reveals, Framer only when you need layout animations or shared elements. Always respect `prefers-reduced-motion`.

### 4h — Font Strategy

- **Source**: Google Fonts only for display/body. System fonts for UI (buttons, labels, inputs).
- **Preloading**: Preload only the hero heading weight (e.g. 700). Preconnect to Google Fonts origin.
- **font-display**: `swap` for body text (content visible instantly, font loads after). `optional` if layout stability is critical and the fallback is close.
- **Subsetting**: Use Google Fonts `&text=` param to subset to only needed characters, or use `unicode-range` in CSS.
- **Variable vs Static**: Variable fonts preferred (one file covers all weights). Fallback to static for wide browser support.
- **Self-host vs CDN**: CDN for prototypes and content sites. Self-host for sensitive apps (no third-party request).
- **Performance**: Max 2 families, max 3 weights per family. Each additional weight adds ~15-30KB.

### 4i — State Management Decision

| Need | Solution | When to skip |
|---|---|---|
| Server data (API, cache) | TanStack Query (React), SWR (Next.js), Vue Query | If app has no async data |
| Client state (theme, sidebar) | React Context + useReducer, Zustand (lightweight), Pinia (Vue) | If only 1-2 values, prop drilling is fine |
| URL state (filters, page) | useSearchParams (Next/React Router), URL params | If state doesn't need to be shareable |
| Form state | React Hook Form, Vue FormKit, Formik | If form has 1-3 fields, uncontrolled is fine |
| Global app state (auth, user) | Zustand, Pinia, Context | If only passed down one level, props are simpler |

**Rule**: Start with the simplest solution. Add complexity only when you have a concrete problem (prop drilling, stale data, race conditions).

### 4j — RTL / Bilingual Guidance

- **Always use logical CSS properties**: `inset-inline-start` instead of `left`, `margin-inline-end` instead of `margin-right`, `padding-inline` instead of `padding-left` + `padding-right`. Tailwind: `ms-4`/`me-4` instead of `ml-4`/`mr-4`, `ps-4`/`pe-4`, `start-4`/`end-4`.
- **Set `dir` at document root**: toggle `<html dir="rtl">` based on language state. Never per-component overrides.
- **Flip directional icons** (arrows, chevrons, progress indicators) in RTL: CSS `scaleX(-1)` for simple cases, or provide mirrored SVG assets.
- **Font pairing across scripts**: match x-height and weight so both scripts feel balanced. For Arabic: Noto Sans Arabic, IBM Plex Sans Arabic, Cairo, or Tajawal paired with Inter.
- **Time/date/currency**: use `Intl.DateTimeFormat` and `Intl.NumberFormat` with the user's locale. Never hardcode format strings.
- **Testing**: test every page in both LTR and RTL. Common breakage: fixed-width containers, text-overflow, misaligned icons, background-position.
- **Translation files**: use i18next (React/Vue), next-i18next (Next.js), or vue-i18n. Keep translations in JSON files, one per locale.

### 4k — SEO (public-facing sites)

See full reference: `references/seo.md`

- Meta tags (title, description, OG, Twitter) set per page via framework API
- JSON-LD structured data for Organization (homepage), Product, Article, FAQ, BreadcrumbList
- Canonical URL on every page to prevent duplicate content
- Sitemap.xml generated via framework plugin
- robots.txt — allow all for public, disallow `/admin` `/api` for authenticated
- hreflang tags for i18n sites
- OG image: 1200×630px, < 200KB, unique per page type, branded

**Why:** Structured data = rich search results. OG tags = control over social previews. Without these, Google and social platforms guess.

### 4l — Error Monitoring & RUM

See full reference: `references/error-monitoring.md`

- SDK init at app entry with `beforeSend` stripping PII
- Error Boundaries wrapping route-level components (React: class-based, Vue: `errorCaptured`, Angular: `ErrorHandler`)
- Source maps uploaded to monitoring service after build, never public
- Session replay sampled at 10% (100% on error)
- Console.log stripped in production
- Alert when error rate > 1% of page loads

**Why:** You catch crashes users see but don't report. Session replay shows exactly what broke.

### 4m — PWA & Offline

See full reference: `references/pwa-offline.md`

- Service worker strategy per resource: NetworkFirst (API), StaleWhileRevalidate (static), CacheFirst (fonts/images)
- manifest.json with icons (192+512), theme_color, display: standalone
- Install prompt deferred until user signal (completed action, 2+ page visits)
- Offline fallback page for uncached requests
- Push notification permission flow (opt-in only, never on first visit)

**Why:** Users in bad reception still see content. Install prompt puts app on home screen.

### 4n — Real-Time Communication

See full reference: `references/realtime.md`

- Socket.io for bi-directional (chat, collab, live dashboards). SSE for server→client only (notifications, feed).
- Reconnection strategy: exponential backoff (1s → 10s max), infinite retries
- Auth token in handshake, refresh on reconnect after expiry
- Connection status UI: connected / reconnecting / failed
- Socket/SSE in service layer, never in components

**Why:** Without reconnection strategy, a dropped socket shows "something broke" with no recovery.

### 4o — Feature Flags (optional)

See full reference: `references/feature-flags.md`

- Tier 1: inline config for prototypes (< 5 flags)
- Tier 2: PostHog/Flagsmith for gradual rollout (1% → 10% → 50% → 100%)
- Single gateway component per flag, not scattered conditionals
- Kill switch: toggle OFF → feature hidden, no deploy needed
- Remove flags older than 6 months

**Why:** Ship unfinished features behind a flag. If something breaks, toggle off — no rollback.

### 4p — Forms & Validation

See full reference: `references/forms.md`

- Multi-step wizard: validate per-step, preserve state on back, final validate on submit
- Dynamic field arrays with min/max limits, stable IDs per row
- File upload: drag & drop zone, size+type validation, preview, progress bar
- Draft auto-save: debounced to 1s to localStorage, restore on mount, clear on submit
- Cross-field validation (password match), async validation (email unique)
- Submit button disabled during pending, server errors mapped to fields

**Why:** Forms are the most interacted-with UI element. A broken form loses users, sales, or data.

### 4q — API Patterns

See full reference: `references/api-patterns.md`

- Pagination: cursor for infinite scroll/feeds, offset for admin tables with page jump
- Optimistic updates: update cache immediately, rollback on error, idempotency key
- Request deduplication: merge concurrent same-endpoint GETs
- Retry with backoff: exponential 1s→10s, jitter, 5xx/network only, max 3 retries
- Race condition: cancel inflight on unmount (AbortController), stale query detection
- Loading/empty/error states per data fetch

**Why:** Raw fetch() in a useEffect is fragile. These patterns prevent the most common API bugs.

### 4r — Analytics

See full reference: `references/analytics.md`

- Platform: Plausible/Umami for privacy-first, PostHog for product analytics, GA4 for enterprise
- Auto page views on route change, outbound link clicks, form submissions
- Custom events for key actions (CTA, signup, purchase) with snake_case naming
- GDPR consent banner with accept/reject, no analytics until consent
- No PII in event properties
- Cookie-less analytics preferred (Plausible/Umami = no cookie banner)

**Why:** Without analytics, you're shipping blind. Without GDPR consent, you're shipping illegally (in the EU).

### 4s — Internationalization (i18n)

See full reference: `references/i18n.md`

- ICU message syntax for all translations (no string concatenation)
- Per-locale pluralization rules (English: one/other, Arabic: one/two/few/many/other)
- `Intl` built-ins for date, number, currency, relative time — no moment.js
- Translation files organized by feature namespace, flat keys
- Pseudo-locale testing to catch hardcoded strings and overflow
- RTL: `dir="rtl"` at root, logical CSS, directional icons flipped

**Why:** i18n done wrong means re-translating every string when a page changes. ICU messages survive restructures.

---

## PHASE 5 — PRE-DELIVERY CHECKLIST + QUALITY GATE

### Step 1: Anti-Slop Script
```bash
bash scripts/anti-slop.sh <project-directory>
```
Paste full output. Fix any violations before proceeding.

### Step 2: Self-Score (0-120)
Load `references/quality-gate.md`. Score 6 dimensions (0-20 each):
1. Visual Coherence
2. Layout & Structure
3. Typography Quality
4. Motion & Interaction
5. Content & Copy
6. Design Grounding

### Step 3: Enforcement
| Score | Action |
|---|---|
| 96-120 | Ship. Paste score + anti-slop.sh output. |
| 72-95 | Revise weakest dimension(s), re-score. Max 3 iterations. |
| < 72 | Redesign from Phase 3. Blueprint needs rethinking. |

### Step 4: Verifiable Proof
Paste in final response:
1. `anti-slop.sh` output (full script output)
2. Self-score with rationale per dimension
3. Total score and ship/revise/redesign decision
4. If revised: what changed between iterations

**Highest-leverage rule:** Do not claim "done" without tool-verified proof. Verbal assertions without tool evidence are defects.

### Web UI Checklist
```
VISUAL        -> colors/type match blueprint exactly, no lorem ipsum,
                 sections in order, theme handled if specified
FUNCTIONALITY -> cursor-pointer, real hrefs, all states implemented,
                 no console errors
RESPONSIVE    -> 375/768/1024/1440px verified, no horizontal overflow
ACCESSIBILITY -> contrast >=4.5:1, focus visible, alt text, labels
PERFORMANCE   -> lazy-load images, font-display: swap, no CLS
SECURITY      -> apply rules for detected level (references/security-levels.md)
I18N/RTL      -> dir="rtl" if applicable, logical CSS properties
ACCEPTANCE    -> every blueprint criterion satisfied or flagged with fix plan
ANTI-PATTERN  -> no purple-AI-gradient-on-white, no Inter-for-display,
                 no generic-card-grid-as-sole-design, no emoji icons,
                 no gradient text, no stock-photo+gradient-hero,
                 no default-SaaS-page-structure, no filler-buzzword-copy,
                 no glassmorphism-decoration, no pill-buttons-only
MAINTAINABILITY -> no fetch() in components, no magic numbers, no `any`,
                 files grouped by feature, all API states handled
```

### App UI Checklist (iOS/Android/RN/Flutter)
```
VISUAL        -> No emojis as icons, SVG/vector icons consistent family,
                 official brand assets with correct proportions
INTERACTION   -> All tappable elements provide pressed feedback,
                 touch targets >=44x44pt (iOS) / >=48dp (Android),
                 micro-interactions 150-300ms with native easing,
                 no gesture conflicts (tap/drag/back-swipe)
THEMING       -> Primary text contrast >=4.5:1 in light AND dark mode,
                 secondary text >=3:1 in both modes,
                 dividers/borders visible in both themes
LAYOUT        -> Safe areas respected for headers/tab bars/bottom CTA,
                 scroll not hidden behind fixed bars,
                 4/8dp spacing rhythm maintained
ACCESSIBILITY -> All meaningful images/icons have accessibility labels,
                 form fields have labels/hints/error messages,
                 color not the only indicator,
                 reduced motion and dynamic text supported
```

### Deployment
- [ ] Build passes: `npm run build` or framework equivalent
- [ ] TypeScript: `npx tsc --noEmit` — 0 errors
- [ ] Lint: `npx eslint . --max-warnings 0` — 0 warnings
- [ ] Choose platform: Vercel (Next/React/Vite), Netlify (static), Railway (full-stack), or Firebase (SPA + functions)
- [ ] Environment variables configured in deploy platform (never in .env committed)
- [ ] Custom domain connected with SSL active
- [ ] Analytics: Plausible, Vercel Analytics, or Umami (privacy-respecting) — not Google Analytics unless required
- [ ] Favicon + OG image set and previewed
- [ ] 404 page styled (even if SPA — configure platform's fallback)
- [ ] Sitemap.xml + robots.txt (for content sites)
- [ ] Error monitoring SDK initialized (see `references/error-monitoring.md`)
- [ ] SEO meta tags + JSON-LD structured data verified (see `references/seo.md`)
- [ ] CI/CD pipeline configured: lint → tsc → test → build → Lighthouse (template: `templates/github-actions.yml`)
- [ ] Storybook built and Chromatic visual regression set up (see `references/storybook.md`)
- [ ] Docker image builds (template: `templates/Dockerfile` + `nginx.conf`)
- [ ] PWA manifest.json + service worker (see `references/pwa-offline.md`)
- [ ] Feature flags documented with rollout plan (see `references/feature-flags.md`)
- [ ] Forms: validation schemas, error states, disabled-submit pattern (see `references/forms.md`)
- [ ] API patterns: retry/backoff, pagination, optimistic updates (see `references/api-patterns.md`)
- [ ] Analytics initialized with GDPR consent flow (see `references/analytics.md`)
- [ ] i18n: ICU messages, pseudo-locale tested, RTL verified (see `references/i18n.md`)

### Performance Budget Enforcement
- [ ] Run Lighthouse: target >= 90 all categories
- [ ] Or automate: `npx lhci autorun` (template: `templates/lighthouserc.json`)
- [ ] Check bundle size: `npx vite build` — verify JS < 200KB gzip, CSS < 50KB gzip
- [ ] Use `npx size-limit` or `npx bundlesize` to enforce budgets in CI
- [ ] Check Largest Contentful Paint element — is it optimized?
- [ ] Check no render-blocking resources (fonts, scripts, CSS)
- [ ] RUM monitoring active (Core Web Vitals from real users)
- [ ] PWA Lighthouse audit passing (installable, offline, service worker)
