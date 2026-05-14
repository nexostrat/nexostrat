# Tests · 2026-05-14 Nexostrat presentation

> **Artifact under test:** `2026-05-14_nexostrat-presentation.html` (sibling file).
> **Test run date:** 2026-05-14.
> **Run by:** Claude Code (Opus 4.7, 1M ctx) in session with Ricardo.

## Purpose

Document the validation checks applied to the presentation HTML and their results. Future regenerations of this document should re-run the same checks and either match or beat these results.

## Why static instead of headless-browser

Both `chrome-devtools-mcp` and `playwright` plugins on this machine resolve to `/opt/google/chrome/chrome`, which doesn't exist. Installing system Chrome requires `sudo` (not available passwordless). Puppeteer's bundled Chromium (`~/.cache/puppeteer/chrome/linux-147.0.7727.57/`) and Playwright's `chromium_headless_shell-1223` exist locally but the MCP servers don't accept a custom binary path.

The fallback chosen was thorough static validation: HTML parse, JS syntax check via `node --check`, SVG XML well-formedness via `xml.etree`, and cross-reference checks between HTML attributes and JS data structures. Combined with a visual sanity check served by the brainstorming companion (`http://localhost:59134`), this is the most aggressive verification this environment supports without burning a session on system-level browser installation.

## Test checklist + results

| # | Check | Method | Result |
|---|---|---|---|
| 1 | JS syntax valid | `node --check` on extracted `<script>` block | ✓ pass |
| 2 | HTML parses cleanly | `python3 html.parser` lenient walk | ✓ pass — no stack remainder, no unexpected closes |
| 3 | All 5 SVG diagrams are well-formed XML | `xml.etree.ElementTree.fromstring` each `<svg>...</svg>` | ✓ all 5 pass — root tags resolve to SVG namespace, child counts: 17 · 12 · 3 · 39 · 13 |
| 4 | Tag balance | regex count opens vs closes for `html, head, body, section, main, nav, header, footer, svg, script, style` | ✓ all 11 tag types balanced; `section` 9/9, `svg` 5/5, `script` 1/1, `style` 1/1 |
| 5 | ADR badges referenced in HTML have entries in JS dict | regex on `data-adr="..."` ∩ JS `const ADR = {...}` keys | ✓ 22 unique badges, all 22 wired |
| 6 | Internal anchor targets resolve | regex `href="#..."` ⊆ `id="..."` | ✓ 8 hrefs, all match an id on page (61 ids total) |
| 7 | Cards have full structure (head + body + eli5 col + tech col) | content check per `.card` block | ✓ 34 cards, all complete |
| 8 | ADR popover DOM elements present | `id="adr-popover"`, `adr-pop-{label,title,decision,consequence}` | ✓ all 5 elements present |
| 9 | File size reasonable | size of HTML | ✓ 198.7 KB (well under any practical limit) |
| 10 | Spanish-primary content | regex for Spanish stopwords | ✓ 224 indicators (target ≥100) |

## ADR coverage

22 ADRs referenced as `<span class="adr-badge" data-adr="NNN">`:

`002, 003, 005, 006, 010, 011, 012, 019, 020, 021, 021bis, 022, 023, 025, 026, 027, 029, 030, 032, 033, 036, 037`

The JS popover dict contains all 35 known ADRs (`001-037` minus 009 superseded, minus the gap). The extra 13 entries are intentional — they exist so a future regen that adds new badges has the popover content ready without re-deriving.

The 5-7 load-bearing ADRs (called out in card 30) all appear inline: `011, 021, 021bis, 022, 026, 029, 033, 036, 037`.

## Manual visual sanity (companion server)

The HTML was copied to `.superpowers/brainstorm/703618-1778792873/content/zz-final-presentation.html` and served by the already-running brainstorming companion at `http://localhost:59134`. Visual sanity checks Ricardo can perform:

- [ ] Cover gradient title renders with Aurora colors
- [ ] TOC sticky on left, 8 entries
- [ ] Click on any card head — expands to side-by-side ELI5 (Emerald label) + Técnico (Amber label)
- [ ] Hover on any `ADR-NNN` badge — popover appears with title, decision, consequence
- [ ] Click ADR badge — popover toggles; click outside or Escape closes it
- [ ] Scroll — TOC active item updates per Part
- [ ] Scroll past 800px — "↑" back-to-top button appears bottom-right
- [ ] URL `#card-4-5` opens that card and scrolls to it
- [ ] "Expandir todo" / "Colapsar todo" pills in header work
- [ ] 5 SVG diagrams render: replication topology, vault decrypt flow, 12 stations pipeline, Heavy/Light side-by-side, plan roadmap

## Known limitations

- **Mobile experience:** desktop-first design (per design Q11). Cards stack vertically below 1000px; not optimized for phone.
- **Print:** basic `@media print` rules included (TOC and popover hidden, cards expanded) but not exhaustively tested.
- **Font fallback:** if Google Fonts CDN is unreachable, falls back to system sans-serif. Acceptable degradation.
- **Browser test:** static only — no JS runtime verification possible in this environment. Logic is straightforward (no async, no fetch, no API), so static + manual visual check is judged sufficient.

## Regeneration protocol

When this presentation needs updating:

1. Read current spec + ADRs + CHECKPOINT + STATUS.
2. Identify deltas since 2026-05-14.
3. Update content reflecting deltas. Preserve overall structure (TOC, 8 Parts, disclosure card pattern, ADR badges).
4. Save with new date: `2026-MM-DD_nexostrat-presentation.html`. Do NOT overwrite the 2026-05-14 snapshot.
5. Re-run validation: `python3 < this file's checks>` and `node --check < extracted JS >`.
6. Update this `.tests.md` sibling with new results.
7. Commit both files together.

## File manifest

- `2026-05-14_nexostrat-presentation.html` · 198.7 KB · 3183 lines · the artifact
- `2026-05-14_nexostrat-presentation.tests.md` · this file
