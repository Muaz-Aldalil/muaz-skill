# Premium Design Guide

Affirmative standard for what "good" looks like. Anti-slop rules say what to avoid; this says what to aim for. Every blueprint must reference specific sections from this guide.

---

## 1 — Spacing & Proportion

### The Grid
- **4px base unit** — all spacing is a multiple of 4px (4/8/12/16/20/24/32/40/48/64/80/96/128)
- **8px rhythm** — vertical spacing between related elements uses 8px increments
- **48px minimum touch target** — any tappable element

### Section Spacing
| Context | Padding | Notes |
|---|---|---|
| Hero section (mobile) | 80-120px vertical | Full viewport minus nav |
| Hero section (desktop) | 120-160px vertical | Generous breathing room |
| Section vertical gap | 96-128px | Consistent between major sections |
| Card internal padding | 24-32px | Proportional to card size |
| Component gap | 8-16px | Between related items (form fields, list items) |
| Inline spacing | 4-8px | Between icon and label, tag and tag |

### Proportion Ratios
- **Hero height:** 70-90vh (never 100vh — leave visible content below fold)
- **Content max-width:** 65-75ch for body text (readability)
- **Section max-width:** 1200-1440px (container)
- **Sidebar width:** 240-280px (if present)

---

## 2 — Typography

### Hierarchy Rules
- **Display font:** 3.5-4x body size for hero headings
- **Heading scale:** Modular scale with ratio >= 1.25 (ideally 1.333 or 1.5)
- **Body size floor:** 16px (1rem) — never smaller
- **Line height:** 1.5 for body, 1.1-1.2 for display headings, 1.3-1.4 for subheadings
- **Line length:** 60-75 characters max (readability ceiling)

### Tracking (Letter-Spacing)
| Context | Tracking | Effect |
|---|---|---|
| Display headings | -0.02 to -0.04em | Tight = premium, editorial feel |
| Subheadings | -0.01 to -0.02em | Slightly tight |
| Body text | 0 (default) | Never modify body tracking |
| Uppercase labels | +0.05 to +0.1em | Open tracking = refined |
| Monospace/code | 0 | Never modify |

### Weight Extremes
- **Display:** 700-900 (bold to black) — never thin/light for display
- **Body:** 400-500 (regular to medium) — never bold for body paragraphs
- **UI labels:** 500-600 (medium to semibold)
- **One family, two weights** is enough — weight contrast > family variety

### Font Pairing Patterns
| Pattern | Example | Use Case |
|---|---|---|
| Serif display + Sans body | Playfair Display + Inter | Editorial, luxury |
| Sans display + Sans body | Sora + DM Sans | SaaS, tech, modern |
| Mono display + Sans body | JetBrains Mono + Inter | Developer tools |
| Slab display + Sans body | Roboto Slab + Roboto | Enterprise, trust |

### Premium Brand Typography (Reference Values)
| Brand | Display Font | Body Font | Tracking |
|---|---|---|---|
| Stripe | Custom (similar to GT America) | Custom sans | -0.02em display |
| Linear | Custom (similar to Cal Sans) | Inter | -0.03em display |
| Vercel | Geist | Geist | -0.02em display |
| Raycast | Inter Tight | Inter | -0.03em display |

---

## 3 — Color

### The 3-Color Rule
- **Max 3 chromatic colors** per design: primary, secondary, accent
- **Accent = <=10% of screen area** — highlights only, not backgrounds
- **2 neutral tones** for backgrounds: base + surface (offset 3-5% from pure black/white)

### Near-Black / Near-White (Never Pure)
| Token | Premium Range | Why |
|---|---|---|
| Background dark | #0a0a0f to #121218 | Pure #000 is harsh; tinted = depth |
| Background light | #fafafa to #f5f5f0 | Pure #fff is clinical; warm = premium |
| Surface dark | #1a1a24 to #1e1e28 | Slight elevation from background |
| Surface light | #ffffff to #f8f8f8 | Subtle separation |

### Color Restraint
- **One brand color** — not two, not three, one dominant
- **Tinted neutrals** — backgrounds carry a 2-5% hue of the brand color
- **Desaturated for dark mode** — reduce saturation 10-20% on dark backgrounds
- **4.5:1 minimum contrast** for text (3:1 for large text)

### Hairline Borders
- Use 1px borders at 8-12% opacity for subtle separation
- Never thick borders (except neo-brutalism style)
- Border color = text color at reduced opacity

### Premium Color Palettes (Reference Values)
| Brand | Primary | Accent | Background |
|---|---|---|---|
| Stripe | #635BFF (indigo) | #0A2540 (near-black) | #f6f9fc |
| Linear | #5E6AD2 (indigo) | #F2C94C (gold) | #0e0e10 |
| Vercel | #000000 | #0070F3 (blue) | #ffffff |
| Raycast | #FF6363 (coral) | #FFD43B (yellow) | #1C1C1E |

---

## 4 — Motion

### Timing Standards
| Interaction | Duration | Easing |
|---|---|---|
| Micro (hover, press, focus) | 150-200ms | ease-out |
| Standard transition | 250-300ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Complex animation | 300-400ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Page transition | 300-500ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Luxury/premium feel | 400-600ms | cubic-bezier(0.16, 1, 0.3, 1) |

### The Premium Easing
```
cubic-bezier(0.16, 1, 0.3, 1)  /* standard premium — fast start, gentle land */
cubic-bezier(0.33, 1, 0.68, 1) /* smooth deceleration */
cubic-bezier(0.65, 0, 0.35, 1) /* smooth acceleration-deceleration */
```

### Motion Principles
- **Enter > exit** — elements appear slowly (300ms), disappear quickly (200ms)
- **Always ease-out** — never linear for UI, never ease-in for entering elements
- **Transform + opacity only** — never animate width/height/top/left
- **Stagger children** — 30-50ms delay between sibling animations
- **Respect prefers-reduced-motion** — reduce or disable animations
- **One animation type per page** — don't mix bounce + slide + fade

### Scroll Behavior
- **Scroll-triggered reveals** — fade up + 20-40px translate Y
- **Parallax** — subtle only (10-20% scroll rate), never jarring
- **Sticky headers** — backdrop-blur when scrolled past hero
- **Smooth scrolling** — `scroll-behavior: smooth` on html

---

## 5 — Layout

### Asymmetric > Centered
- Centered layouts are the default AI choice — break the pattern
- **Editorial layouts** — text left, image right (or reverse), with offset
- **Split screens** — 60/40 or 70/30 splits, never 50/50
- **Bento grids** — mixed-size cards in a grid (not equal columns)

### Whitespace = Confidence
- More whitespace = more premium (Apple, Stripe, Linear)
- **Section padding >= 96px** on desktop
- **Between elements:** 24-40px minimum
- **Around headings:** 16-24px above, 8-12px below

### Layout Anti-Patterns (Avoid)
- 3 equal columns as the only layout
- Centered hero → centered features → centered CTA
- Every section full-width with centered content
- Cards all the same size in a grid

### Premium Layout Patterns
| Pattern | When to Use | Example |
|---|---|---|
| Split hero | Product pages, SaaS landing | 60% text / 40% visual |
| Bento grid | Feature showcase, dashboard | Mixed card sizes |
| Editorial flow | Blog, content, case studies | Image + text alternating |
| Masonry | Gallery, portfolio | Pinterest-style |
| Single-column | Long-form reading, mobile | Max 65ch width |

---

## 6 — Content

### Writing Rules
- **No em-dashes** — use commas or periods. Em-dashes are an AI tell.
- **Active voice** — "Build faster" not "Speed is built into every feature"
- **Specific > abstract** — "Saves 3 hours/week" not "Significantly improves productivity"
- **No filler** — cut any word that doesn't add meaning
- **One idea per sentence** — short sentences, clear meaning

### Banned Phrases
```
"Seamlessly integrate"    "Revolutionize your workflow"
"Empower your team"       "The future of X"
"Unlock your potential"   "Built for modern teams"
"Game-changing"           "Cutting-edge"
"Leverage our platform"   "Next-generation"
```

### Premium Copy Patterns
| Instead of... | Use... |
|---|---|
| "We help businesses grow" | "Ship features 2x faster" |
| "A powerful analytics platform" | "Know exactly where your time goes" |
| "Trusted by thousands" | "42,000 teams ship with us daily" |
| "Revolutionary AI technology" | "Cuts review time from 3 hours to 12 minutes" |

---

## 7 — Imagery

### Consistency Rules
- **One illustration style** per project — never mix photos + 3D + line art + cartoon
- **One photo treatment** — all warm, all cool, all desaturated (pick one)
- **Consistent lighting** — match illustration/photo lighting direction
- **Subject relevance** — images relate to adjacent content, not decorative

### Premium Image Patterns
| Pattern | Quality Signal |
|---|---|
| Custom illustration | Higher effort than stock |
| Product screenshots | Concrete, specific, real |
| Abstract geometric | Clean, intentional, on-brand |
| Photography with art direction | Treated, not raw stock |
| No images | Bold typography-only (if layout supports it) |

---

## 8 — Components

### Interactive States
Every interactive element must have 6 states:
1. **Default** — rest state
2. **Hover** — mouse over (desktop)
3. **Active/Pressed** — during click/tap
4. **Focus** — keyboard focus (visible ring)
5. **Disabled** — reduced opacity + no interaction
6. **Loading** — async operation in progress

### Button Hierarchy
| Level | Use | Style |
|---|---|---|
| Primary | One per section — the main action | Filled, brand color |
| Secondary | Supporting action | Outlined or ghost |
| Tertiary | Tertiary/inline actions | Text-only, underline on hover |

### Form Standards
- **Visible labels** — never placeholder-only
- **Error below field** — not in a toast, not at top of page
- **Inline validation** — validate on blur, not on keystroke
- **Input height >= 44px** — touch-friendly
- **One column on mobile** — fields full-width

---

## 9 — Brand Analysis (Reference — 13 Premium Sites)

Use these as blueprint references. Every design decision should cite a specific site and value.

### Stripe — stripe.com (SaaS/Fintech)
**The genre-defining fintech editorial system.**

| Token | Value |
|---|---|
| Display hero | 56px / weight 300 / line-height 1.03 / tracking -0.02em |
| Section heads | 34px / weight 300 / line-height 1.03 / tracking -0.02em |
| Body | 16px / weight 300 / line-height 1.4 |
| Primary (blurple) | #533AFD |
| Ink (headings) | #061B31 (blue-black, never pure black) |
| Body text | #50617A (cool slate) |
| Canvas | #FFFFFF |
| Surface soft | #F6F9FC |
| Max width | ~1080-1152px |
| Section rhythm | 56-96px |
| Card padding | 32px |
| Button radius | 4px |
| Shadows | None — depth from tint shifts |
| **Key move** | Weight 300 everywhere + blue-tinted neutrals + one blurple. Animated gradient mesh hero. Diagonally sheared section seams (-6deg). |

### Linear — linear.app (SaaS/Dev Tools)
**Strictest dark-canvas system in SaaS.**

| Token | Value |
|---|---|
| Display XL | 56px / weight 590 / line-height 1.06 / tracking -0.022em |
| Body | 15px / weight 400 / line-height 1.6 ("Linear 15px") |
| Canvas | #010102 (near-black with blue cast) |
| Surface ladder | #0F1011 → #141516 → #18191A → #191A1B |
| Primary (lavender) | #5E6AD2 |
| Ink | #F7F8F8 |
| Hairline | #23252A |
| Section rhythm | 96-160px |
| Button radius | 8px (rounded.md) |
| **Key move** | Elevation = lighter fill, not shadow. Body 15px (not 16px) = dense machined feel. Primary CTAs are white on near-black, not colored. |

### Vercel — vercel.com (SaaS/Dev Tools)
**Starest developer-platform system.**

| Token | Value |
|---|---|
| Display | 72px / weight 600 / tracking -2.4px at 48px |
| Body | 16px / weight 400 / line-height 1.5 |
| Primary (ink) | #171717 |
| Canvas | #FFFFFF |
| Canvas soft | #FAFAFA |
| Body text | #4D4D4D |
| Link blue | #0070F3 |
| Max width | 1200px |
| Section rhythm | 64-96px |
| Button radius | 100px (marketing) / 6px (nav) |
| Shadows | Stacked small offsets (4-12% black) + inset 1px hairline |
| **Key move** | The ink IS the brand — no secondary color. 3-pair gradient stack (develop/preview/ship) is entire decorative system. Geist Mono for headings = technical feel. |

### Raycast — raycast.com (SaaS/Dev Tools)
**Keyboard-first productivity mirrored in marketing.**

| Token | Value |
|---|---|
| Display | Large weight, tight tracking |
| Body | Clean sans at readable sizes |
| Canvas | #FFFFFF |
| Primary text | Near-black |
| Accent | Raycast red/amber gradient (rare) |
| Layout | Single-column scroll, dense feature rows |
| **Key move** | The keyboard image IS the hero — not a screenshot, the actual input device. Trusts product density over whitespace: real extension names, real shortcuts, real tool names. |

### Notion — notion.so (SaaS/Productivity)
**Functional dual-mode design.**

| Token | Value |
|---|---|
| Display XL | 80px / weight 600 / line-height 1.05 / tracking -2px |
| Display LG | 56px / weight 600 / line-height 1.10 / tracking -1px |
| Body | 16px / weight 400 / line-height 1.55 |
| Primary (purple) | #5645D4 |
| Brand navy | #0A1530 (hero background) |
| Surface | #F6F5F4 (warm off-white, paper tone) |
| Ink | #1A1A1A |
| Charcoal | #37352F |
| Card tints | Peach #FFE8D4, Mint #D9F3E1, Lavender #E6E0F5, Sky #DCEBFA |
| Max width | 1200px |
| Section rhythm | 64-96px; hero: 120px |
| Button radius | 8px (rounded, NOT pills) |
| **Key move** | Warm neutrals (yellow-brown undertones) = paper, not glass. Rectangular buttons feel like document blocks, not consumer apps. Pastel card tints provide personality. |

### Apple Store — apple.com/store (E-commerce)
**Photography-first museum gallery.**

| Token | Value |
|---|---|
| Display hero | 80px / weight 600 / line-height 1.05 / tracking -1.2px |
| Body | 17px / weight 400 / line-height 1.47 / tracking -0.374px |
| Action blue | #0071E3 |
| Ink | #1D1D1F (never pure #000000) |
| Parchment | #F5F5F7 (alternating tile background) |
| Dark tile | #272729 |
| Max width | 1680px with 90px padding |
| Button radius | 980px (fully pill) |
| Shadows | Only one: rgba(0,0,0,0.22) 3px 5px 30px — on product photography only |
| **Key move** | 17px body text (not 16px) defines reading pace. Edge-to-edge tiles with alternating canvas colors (white/parchment/near-black) = no borders needed. Weight 500 deliberately absent from type ladder. |

### Nike — nike.com (E-commerce/Athletic)
**Photography-first athletic minimalism.**

| Token | Value |
|---|---|
| Display campaign | 96px / weight 500 / line-height 0.9 / uppercase |
| Body | 16px / weight 400 / line-height 1.75 |
| Primary (ink) | #111111 (not pure #000000) |
| Soft cloud | #F5F5F5 |
| Sale | #D30005 (price text only, no badge) |
| Max width | 1440px |
| Section rhythm | 48px |
| Button radius | 30px (pill) |
| Cards | 0px radius |
| Shadows | Zero — depth from photography and 1px hairline only |
| **Key move** | Extreme typographic contrast: 96px uppercase Futura directly above 16px Helvetica Now with no middle ground. Only "chrome color" is #111111. Product photography provides all chromatic interest. |

### Aesop — aesop.com (E-commerce/Luxury Beauty)
**Apothecary minimalism — most imitated luxury beauty system.**

| Token | Value |
|---|---|
| Display hero | 31px / weight 400 / line-height 1.33 (small for luxury) |
| Body | 14px / weight 400 / line-height 1.6 |
| Parchment (canvas) | #FFFEF2 (warm, aged-paper) |
| Charcoal | #333333 |
| Stone | #666666 |
| Max width | 1600px |
| Section rhythm | 96-128px |
| Border radius | 0px on ALL UI elements — no rounded corners anywhere |
| Shadows | None |
| **Key move** | Zero-corner-radius apothecary. Dual-typeface tension: humanist serif (Optima) for headlines + neutral sans for body. Parchment canvas instead of white = tactile aged-paper. Product photography IS the decoration. |

### Medium — medium.com (Editorial/Publishing)
**Reading room translated to the web.**

| Token | Value |
|---|---|
| Display hero | 120px / weight 400 / line-height 0.83 / tracking -6.6px |
| Body (article) | 21px / weight 400 / line-height 1.58 (Charter serif) |
| Canvas (newsprint cream) | #F7F4ED |
| Ink (headings) | #242424 |
| Button black | #191919 |
| Link green | #1A8917 |
| Max width | 1200px |
| Section rhythm | 64px |
| Button radius | 9999px (pills) |
| Cards | 0px radius |
| **Key move** | 120px GT Super serif at weight 400 — literary serif at billboard scale. Cream canvas = newsprint. Line-height 0.83 causes optical overlap between descenders/ascenders. Page commits entire viewport to one sentence. |

### Substack — substack.com (Editorial/Publishing)
**Feed of posts dressed as marketing page.**

| Token | Value |
|---|---|
| Display | 32px / weight 500 / line-height 1.24 (serif) |
| Body | 16px / weight 400 / line-height 1.5 (system-ui) |
| Primary (orange) | #FF6719 |
| Ink primary | #363737 (warm near-black) |
| Hairline | #EEEEEE |
| Border radius | 9999px (pills), 12px (cards), 8px (buttons) |
| Elevation | No shadows — 1px #EEEEEE hairlines |
| **Key move** | Marketing surface IS the product surface — below hero, the page IS the platform. Single orange does work most brands spread across 5 colors. System-ui for all UI = zero font-loading delay. |

### Apple Newsroom — apple.com/newsroom (Editorial/Corporate)
**Journalistic restraint inside Apple's design system.**

| Token | Value |
|---|---|
| Article headlines | 40-56px SF Pro Display / weight 600 |
| Body | 17px / weight 400 / generous leading |
| Canvas | #FFFFFF |
| Ink | #1D1D1F |
| Action blue | #0071E3 |
| Hairlines | #D2D2D7 |
| **Key move** | Same design language as Apple Store applied to editorial. Hero photography, centered headline, single "Read more" link instead of dashboard-style cards. Trusts headline and image to do hierarchy work. |

### Mercury — mercury.com (Fintech/Banking)
**Dark-canvas fintech that inverts Stripe's convention.**

| Token | Value |
|---|---|
| Display hero | 65px / weight 360 / line-height 1.05 / tracking +0.42px |
| Heading | 22px / weight 480 / line-height 1.3 |
| Body | 15px / weight 400 / line-height 1.625 |
| Primary (indigo) | #5266EB |
| Canvas (dark) | #171721 (indigo-black) |
| Ink emphasized | #1E1E2A |
| Ink subdued | #C3C3CC |
| Max width | ~1200px, 12-column grid |
| Section rhythm | 96px+ |
| Button radius | 4px (primary), 32px (CTA pill) |
| **Key move** | Dark-canvas-first. Weight 480 (between 400 and 500) is signature heading weight. Positive letter-spacing (+0.42px) on display inverts negative-tracking default. Body 1.625 line-height = most generous in fintech. |

### Robinhood — robinhood.com (Fintech/Trading)
**Chartreuse voltage on warm-black.**

| Token | Value |
|---|---|
| Display hero | 110px / weight 400 / line-height 1.0 / tracking -2.5px |
| Body | 16px / weight 400 / line-height 1.55 |
| Primary (lime) | #CCFF00 |
| Canvas (warm black) | #110E08 (coffee-tinted) |
| Ink default | #FFFFFF |
| Ink subdued | #4D4A46 |
| Max width | ~1200px |
| Section rhythm | 96px; hero: 128px |
| Button radius | 36px (singular — ALL interactive surfaces) |
| **Key move** | Chartreuse lime (#CCFF00) = color that looks like nothing else in fintech. Warm-black canvas with barely-perceptible yellow shift. Serif headline (Martina Plantijn) at 110px/400 weight inverts geometric-sans convention. Single 36px pill radius for everything. |

---

## 10 — The 7 Rules That Recur Across Premium Sites

1. **One action color, not three.** Stripe (blurple), Linear (lavender), Mercury (indigo), Robinhood (lime), Substack (orange) — each has exactly one saturated color used only for CTAs and brand mark.

2. **Blue-tinted or warm neutrals, never pure gray.** Stripe (#50617A is blue-gray), Notion (#F6F5F4 is warm), Robinhood (#110E08 is coffee-black), Medium (#F7F4ED is newsprint cream). The temperature is intentional.

3. **Light weight at display sizes.** Dark type at weight 300-400 (Stripe, Medium, Robinhood) signals confidence through restraint compared to bold competitors.

4. **Negative tracking on headlines.** Every premium site tightens letter-spacing at display sizes. The ratio is typically -0.02em to -0.025em at 56px+. Mercury reverses this convention by using positive tracking.

5. **No pure black.** Replace #000000 with #061B31 (Stripe), #171717 (Vercel), #111111 (Nike), #110E08 (Robinhood), #1D1D1F (Apple).

6. **Shadows are optional; most premium sites avoid them.** Stripe, Linear, Apple, Aesop, Nike, Medium, Substack use zero drop shadows. Depth comes from surface tint shifts, hairlines, or photography.

7. **Section gaps at 96px.** Almost every site uses 96px as the standard vertical rhythm between major sections.
