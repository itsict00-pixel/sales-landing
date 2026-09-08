# Prompt per Opus 4.8 — Visual upgrade (verde/bianco + WebGL hero + carosello testimonianze)

> Generato il 2026-09-07. Incolla il blocco qui sotto in una sessione Claude Code su **Opus 4.8**
> (ri-attacca anche lo screenshot di riferimento "CRAFT." e la spec WebGL, se disponibili).
> Il file `index.html` e `ghl/*` sono generati — Opus deve editare `blocks/`, `css/`, `js/` e poi
> rilanciare `python3 build.py`.

---

SUBJECT: Visual upgrade — my personal landing page (Digital Marketer), green + white rebrand + WebGL hero + auto-advancing testimonial carousel

CONTEXT
This is my personal landing page (I'm a Digital Marketer — my own site, not a client's). Work inside the existing `sales-landing/` project. It's a static HTML/CSS/JS build pipeline — read this before touching anything:

- `layout.html` + `blocks/*.html` are the SOURCE. `build.py` stitches them into `index.html` AND into the `ghl/` export (GHL-ready section snippets + `ghl/sl-styles.css`).
- `index.html` and everything under `ghl/` are GENERATED — never hand-edit them. Edit `blocks/10-hero.html`, `css/tokens.css`, `css/styles.css`, `js/main.js` as needed, then run `python3 build.py` once to regenerate both outputs.
- All CSS lives scoped under the `.sl` root class (so it can be pasted into GoHighLevel's Custom CSS without leaking into the platform's own styles) — keep every new rule scoped the same way, and use the semantic tokens (`--color-*`) rather than hardcoded colors.

HARD CONSTRAINTS (do not violate)
1. NO contact form / booking form of any kind. `blocks/60-offerta.html` has a native GHL slot (`<div class="ghl-slot">`) — leave that block completely untouched. I embed GHL's own Form/Calendar widget there myself to trigger my automations; a static `<form>` would break that.
2. NO copywriting. Every section already uses bracketed placeholders (`[Headline]`, `[Subheadline]`, `[CTA primaria]`, etc.) — keep that convention everywhere, including anything new (e.g. new testimonial cards get `[Testimonianza 1]` / `[Nome, ruolo]`, not invented quotes). Don't write persuasive copy, and don't fill in `docs/brief.md`, `docs/design-direction.md`, or `copy/homepage.md` — those stay for a later pass.

VISUAL DIRECTION — GREEN + WHITE
Rebrand from the current placeholder blue to green, white-paired, premium feel:
- Current brand tokens in `css/tokens.css` are blue (`--c-brand-600:#1d4ed8`, `--c-brand-700:#1e40af`, `--c-brand-50:#eff6ff`), marked as a placeholder — replace with a green scale. Target the tone of a €100 banknote: a rich, slightly muted green (closer to bottle-green/emerald-deep than mint or neon), not a generic SaaS teal. Keep the same 600/700/50 structure (base / hover-darker / soft tint) so nothing downstream breaks.
- Slightly increase the hero gradient's presence. It's currently near-invisible: `.sl .hero { background: linear-gradient(180deg, var(--color-accent-soft), var(--color-bg)); }`. Recolor it into the new green and make it a touch more perceptible than today — still subtle/premium, not loud — and make sure it doesn't fight visually with the new WebGL layer below (it can sit further back / fade faster if needed).
- White/off-white stays the dominant surface color; green is the accent/brand color for CTAs, links and accents — not a full-bleed color block.

WEBGL HERO BACKGROUND ("neuform" dot-matrix effect)
Add a full-bleed animated WebGL background to the `.hero` section only, recolored from the reference's amber into our green palette. Spec (from a reference site's extracted design notes — adapt the technique, not the color):
- Effect: dot-matrix particle field with soft depth fade, full-bleed behind the hero content.
- Motion: slow orbital drift, ambient/atmospheric — not distracting.
- Interaction: pointer-reactive, but only a subtle parallax drift, nothing snappy.
- Markup pattern: a `<canvas id="webgl-bg">` absolutely positioned to fill `.hero`, `pointer-events: none`, behind the hero content in z-index (the content wrapper gets a higher z-index so text/CTA stay fully readable and clickable).
- Shader approach (reference implementation to adapt, not copy verbatim — recolor to green, tune density/contrast so text stays legible over it):
  ```
  vertex: attribute vec2 position; void main(){ gl_Position = vec4(position,0.,1.); }
  fragment: precision mediump float; uniform float u_time; uniform vec2 u_resolution;
  // noise-based dot field (simplex/perlin-style 2D noise, e.g. a mod289-based helper),
  // driving per-dot position/opacity for the drift + depth fade.
  ```
- MUST degrade gracefully: a static CSS/DOM fallback (e.g. the gradient above, or a static dot pattern) for browsers without WebGL, and MUST fully disable the animated drift (freeze or fall back to the static version) when `prefers-reduced-motion: reduce` is set. Watch mobile perf — reduce particle count or disable below a reasonable viewport/CPU threshold rather than tanking scroll performance on phones.

HERO TESTIMONIAL CAROUSEL (new, auto-advancing)
Add an auto-advancing testimonial carousel directly below the hero CTA (`.hero__cta`), inside `blocks/10-hero.html` — this replaces or absorbs the current minimal `<ul class="trust-strip">` (your call which reads better visually; don't just duplicate both). I'm attaching a reference screenshot of the layout I want (a "CRAFT." example) — match its composition, not its content or its cream/amber color:
- A small pill/eyebrow tag above the headline (the existing `.eyebrow` can serve this role, or be restyled into a pill).
- Below the CTA: a layered/stacked testimonial-card carousel — one sharp, elevated, centered card in front (white card, shadow, avatar + quote + name/role), with the previous/next cards peeking from behind it, partially faded/scaled down, in a shallow stack/coverflow arrangement (not a flat side-by-side row).
- Must auto-advance on a timer (cycle through 4–5 placeholder testimonials), pause on hover/focus and while the user is interacting, and ideally allow manual next/prev (click or swipe). Keep it keyboard-accessible (focusable controls, visible focus states) and respect `prefers-reduced-motion` (no autoplay / instant transitions instead of animated ones when set).
- Content: placeholder testimonials only, same bracket convention as the rest of the page (quote, name, role — no real names/quotes).

GENERAL
- Keep every existing accessibility pattern already in the codebase (skip-link, 44px tap targets, visible focus rings, aria-labels) and extend it to the new pieces (carousel controls, canvas).
- Preserve the rest of the page structure and all other sections exactly as they are — this pass is scoped to: brand color/gradient, the hero WebGL background, and the new hero testimonial carousel. Don't touch `blocks/60-offerta.html` (see hard constraint #1) or rewrite any other section.
- After editing, run `python3 build.py` once (it regenerates both `index.html` and the `ghl/` export from the same source) and verify visually in the browser at 375 / 768 / 1440px, in both normal motion and `prefers-reduced-motion: reduce`, before calling it done.

[Attach: reference screenshot ("CRAFT." testimonial layout)]
