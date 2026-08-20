# Design rules

Default frontend visual rules for `web/`. Like `ai/ARCHITECTURE_RULES.md`, this file is template contract, not project content — see `docs/TEMPLATE_BOUNDARY.md`. Adjust or override a value for a specific tool's audience or data, but log anything beyond a small tuning tweak (base font family, contrast target, type scale ratio) in `docs/DECISIONS.md`. Do not rewrite this file's rules or structure as part of an ordinary feature/data/UI change.

For how to structure the analytical experience itself — information hierarchy, viewport budget, chart type selection, and when a visual phase is actually done — see `docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md`. This file gives defaults; that playbook gives reasoning.

## Typography

- Type scale: one modular scale; no more than 4 distinct font sizes visible in any single screen.
- Line-height: 1.4–1.6 for body/paragraph text; 1.05–1.2 for large display/heading text.
- Minimum body text size: 14px for Latin script; 15–16px where Traditional Chinese and Latin mix in the same view (CJK glyphs need a slightly larger point size than Latin for equivalent legibility at normal desktop distance). Confirm the real number against the target audience/device before shipping, and record it in `docs/DECISIONS.md` once chosen — don't leave it implicit in component styles.
- Fonts: self-host webfonts; do not add a runtime dependency on a remote font CDN. This matches the local-first, offline-tolerant defaults in `ai/ARCHITECTURE_RULES.md`. Confirm license and weight needs before pinning a specific family.
- Font stack and `lang`: when the UI shows Traditional Chinese, the font stack needs a real fallback after the self-hosted family (e.g. `'PingFang TC', 'Microsoft JhengHei', 微軟正黑體`), and the page/element must declare `lang="zh-Hant"` — not `lang="en"` with Chinese text in it. Han-unified glyphs render differently per language tag even under the same font file, so a wrong `lang` can pick the wrong glyph shape even when the right font loaded correctly.
- CJK/Latin mixed-script spacing: where UI text mixes Chinese with Latin letters, digits, or symbols in the same run (labels, table cells, generated summaries), insert a thin space (`U+2009`) at each boundary so the glyphs don't visually collide. Apply per rendered text node, not to a raw string containing markup. Reference implementation, to add at `web/src/utils/cjkSpacing.ts` once the web workflow starts:

  ```ts
  const THIN_SPACE = " ";
  const isCjk = (ch: string) => {
    const cp = ch.codePointAt(0)!;
    return (cp >= 0x3400 && cp <= 0x4dbf) || (cp >= 0x4e00 && cp <= 0x9fff);
  };
  const isHalfWidth = (ch: string) => {
    const cp = ch.codePointAt(0)!;
    return cp >= 0x21 && cp <= 0x7e;
  };
  const ALREADY_SPACED = new Set([" ", THIN_SPACE, "\t", "\n"]);

  export function insertThinSpaceAtBoundaries(text: string): string {
    if (!text) return text;
    let result = text[0];
    for (let i = 1; i < text.length; i++) {
      const prev = text[i - 1];
      const ch = text[i];
      const boundary = (isCjk(prev) && isHalfWidth(ch)) || (isHalfWidth(prev) && isCjk(ch));
      if (boundary && !ALREADY_SPACED.has(prev) && !ALREADY_SPACED.has(ch)) result += THIN_SPACE;
      result += ch;
    }
    return result;
  }
  ```

- Tabular figures: don't assume `font-variant-numeric: tabular-nums` works on a numeric table column — verify the chosen font actually ships a `tnum` OpenType feature first. If it doesn't, either pick a font that does or accept ragged numeric columns and record that choice in `docs/DECISIONS.md`.

## Color and contrast

- Minimum contrast: WCAG AA 4.5:1 for body text; prefer 7:1 for dense tabular data or small metadata text.
- Balance roughly 60/30/10 (dominant neutral / secondary / accent); at most one accent color per screen.
- Never encode meaning by hue alone. Any status or category color (pass/fail, over/under budget, chart category) needs a second channel too — icon, label, or pattern — so it still reads for colorblind users and in grayscale printing or screenshots.
- Lay out a new screen in grayscale first, then add color last. If the hierarchy (what's primary, what's secondary, what's de-emphasized) already reads correctly in grayscale, color only reinforces it; if it doesn't, color is being used to paper over a layout that isn't actually organized yet.

## Spacing

- Use an 8pt spacing grid. Tailwind's default scale (0.25rem/4px steps) already aligns with this on even-numbered steps (`2`, `4`, `6`, `8` → 8/16/24/32px). Don't introduce one-off arbitrary pixel values in component styles.

## Depth

- Pick exactly one of border, shadow, or background color to separate an element from its surroundings — never stack more than one on the same edge. Reserve borders for cases that need a genuinely hard boundary (a table row, an input's edit state); prefer spacing or a background tint first.
- A shadow implies a light source above the page: vertical offset greater than horizontal offset, and blur greater than the vertical offset. An inconsistent or inverted shadow reads as a rendering bug, not depth.

## States

Every interactive element and every data-bearing region has more than one visual state; shipping only the default state is an unfinished component, not a smaller one.

- Interactive elements (button, link, input, clickable card): default, hover, focus (a visible focus ring — required for accessibility, not optional polish), disabled, and loading for anything that takes over ~200ms.
- Data-bearing regions (list, table, card grid): loading (skeleton or spinner, never a blank pause), empty (a "nothing here yet" message plus the action to fix that, not a bare blank area), error (what happened plus a retry), and no-permission (an explanation, not a raw 403).

## Tables

This template's primary output is spreadsheet-derived data views, so tables are a core component, not a decoration:

- Header row required and visually distinct — bold weight plus a contrasting background, never a thin border alone.
- Left-align text columns; right-align numeric columns.
- Cell padding from the spacing scale (start at 12px / Tailwind `p-3`), not a bespoke value per table.
- Zebra striping off by default; enable it only for a specific dataset dense enough to need row-tracking — a per-table call, not a global default.

## Images and media fit

For a fixed-size container (avatar, thumbnail, card image) hosting a variable-aspect-ratio image:

1. Prefer `object-fit: contain` if it leaves acceptable margins.
2. Otherwise resize the container itself within its own layout bounds.
3. Crop (`object-fit: cover`) only as a last resort, anchored center by default.

## Non-goals

- No fixed-canvas page layout, page-zone hierarchy, or per-page human-approval gate. `web/` is a responsive application, not a fixed-size rendered artifact, and this template already has an iterative, small-change workflow (see `AGENTS.md`'s change protocol) — it doesn't need a slide-deck-style sign-off pipeline on top of it.
- No numeric-approval-tier system for these tokens. A value here is either the current default or a decision recorded in `docs/DECISIONS.md` — nothing in between.
- No mandatory 5-stage "Epic 0" design-system ceremony (framework → style tiles → tokens → component library → layouts, each with its own human gate) before any real feature can ship. That fits a full multi-agent SDLC governance layer, not a small local prototype built one acceptance-testable change at a time. The underlying grain of truth — pick a token or component once, then reuse it rather than re-deriving it per screen — is already covered above and in `docs/DECISIONS.md`'s normal decision-logging process; it doesn't need dedicated gate machinery on top.
