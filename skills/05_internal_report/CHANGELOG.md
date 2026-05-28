# Changelog — `05_internal_report` (formerly `05_opportunity_report`)

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.4 — 2026-05-28 · Rename mecánico opportunity-report → internal-report (Pipeline v2)

**Scope:** rename mecánico del skill (folder + slug + symlink + test registry + frontmatter + docs). Body del prompt NO se reescribe — sigue hablando de "directo al cliente" (audiencia v1). El reprofile completo del body a audiencia interna Nexostrat (`t-skill5-reprofile-body`) queda como task pendiente.

**Driver:** Pipeline v2 sesión 26 — bajo el nuevo flujo, este skill produce un documento INTERNO (hoja de análisis crudo + lista de oportunidades) que después alimenta al Skill 6 (entregables cliente refinados, 10-15 págs DOCX + 10 slides PPTX). El nombre `opportunity-report` confundía sobre la audiencia.

**Cambios:**
- **Folder rename:** `skills/05_opportunity_report/` → `skills/05_internal_report/` (`git mv`, historia preservada).
- **Symlink:** `.claude/skills/opportunity-report` → `.claude/skills/internal-report` (apunta a la nueva carpeta).
- **Frontmatter:** `name: opportunity-report` → `name: internal-report`. Description reescrita para reflejar audiencia interna + trigger phrases nuevas.
- **Nota REPROFILE PENDIENTE** agregada al body para que el lector entienda que el cuerpo del prompt está desactualizado y leer "cliente" como "uso interno Nexostrat".
- **Test registry:** `infra/scripts/test_skills.sh` `05_opportunity_report:opportunity-report` → `05_internal_report:internal-report`. Test harness verde post-rename: 63 PASS · 0 SKIP · 0 FAIL.
- **Docs:** `skills/README.md` + `skills/CLAUDE.md` actualizados con nuevo slug + nota de rename + diagrama del pipeline ahora incluye Skill 6 (entregables cliente) después de la revisión interna.

**Verified by:** `bash infra/scripts/test_skills.sh` post-rename → 63 PASS · 0 SKIP · 0 FAIL. End-to-end render del sample MD → DOCX para internal-report pasó (62 KB DOCX).

**Pendiente:** `t-skill5-reprofile-body` — reescribir el cuerpo del prompt para audiencia interna Nexostrat (cambiar tono de "impresionar al cliente" a "alimentar análisis crítico Nexostrat", adaptar anti-alucinación, redefinir Quick Wins criteria, etc.). No bloqueante para Skill 6 ni para correr el skill sobre clientes nuevos.

---

## v0.3 — 2026-05-26 · Parser tolerance + silent-failure warning

**Scope:** fix `scripts/generate_docx.py` markdown parser for `### TABLA_OPORTUNIDADES`. Discovered while generating the Trixx Logistics report 2026-05-26: a blank line between the heading `### TABLA_OPORTUNIDADES` and the table (standard CommonMark convention) terminated the table parse with 0 rows, producing a reporte cliente-visible without inventory, 5×5 charts or 2×2 matrix — silently (exit 0, no warning).

- **Tolerance added (`process_markdown()` line ~756):** while `in_opp_table` is active AND no table rows have been accumulated yet, skip blank lines. Once any `|`-row exists, blank lines still terminate the table (preserves prior semantics).
- **Silent-failure warning added:** when `parse_opportunity_table()` returns an empty list, the script now prints a `⚠️ WARNING` to stderr explaining the expected format. The report still renders (no breaking change) but the operator sees the alert before delivery to the client.
- **Regression test added:** `tests/fixtures/blank_line_before_table.md` + `tests/test_parser_regression.sh`. Runs the generator on the fixture and asserts 3 opportunities are detected.

**Verified by:** new regression test passes (3 of 3 opportunities detected from fixture) + backward-compatibility re-run of the Trixx report (10 opportunities, Quick Wins #1 #2 identified correctly) + negative test (empty table emits warning correctly).

**Source:** memo `skills/00_META/inbox/archive/2026-05-26_2310_client-owner_skill05-parser-bug.md` (Client-Owner → Skills-Master).

---

## v0.2 — 2026-05-18 · Brand wire-up + shared-module migration

**Scope:** apply Nexostrat Brand Guide v1.0 to `scripts/generate_docx.py`, then migrate to `skills/shared/brand.py`. Preserve the Midnight Blue cover band, 2×2 priority matrix, 5×5 grid chart, and callout color semantics.

- Aurora palette at module level: `DARK_BLUE → #0C1A2E` (Midnight Blue), `ACCENT → #0EA5E9` (Sky Blue), `MID_GRAY → #6B7280` (Gray 500). All `1A2E4A` cell shadings (cover band, opportunity table header, 5×5 grid borders, generic table header) replaced with `brand.HEX_MIDNIGHT_BLUE`. Cover divider line replaced with `brand.HEX_SKY_BLUE`.
- **Cover band redesign:** the top Midnight Blue band now hosts the actual logo image (`Nexostrat_Logo_Fondo_Midnight_Transparente.png` at 3.0") instead of the previous "NEXOSTRAT" text — produced via the new `brand.insert_logo_in_cell()` helper. Band height grown from 0.8 cm → 2.0 cm to accommodate the logo.
- Body-pages header personalized: `"NEXOSTRAT · <company_name>"` via `brand.apply_brand_header(doc, extra=company_name)`. Footer: `"nexostrat.com · Confidencial · Pág. <PAGE>"` via `brand.apply_brand_footer(doc, extra="Confidencial")`. The original 40-line `add_header_footer()` function shrank to a 3-line shim that delegates to brand.
- Migrated to `skills/shared/brand.py` — 16 brand references resolve through `brand.*`. Domain-specific colors kept local: `LIGHT_GRAY #F4F5F7` (table-row tint), `GREEN_DARK #1B5E20` (Quick Win indicator), `AMBER_DARK #E65C00` (effort indicator), `SUCCESS_GRN #2E7D32` (badge), Q_VICTORIA/Q_ESTRATEGIC/Q_RAPIDO/Q_DESCARTAR (2×2 quadrant tints), callout-type Material-Design palette (🟢 INSIGHT / ⚠️ ALERTA / 💡 QUICK WIN / ℹ️ NOTA — these are functional UI semantics, not brand palette).

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL. End-to-end render of pilot discovery-meeting .md (placeholder for missing opportunity-report .md) → branded .docx passes XML inspection (logo in cover band, header/footer parts present, Aurora hex codes present, zero legacy hex codes).

---

## v0.1 — 2026-05-18 · Initial delivery by JP

**Scope:** brand-new skill. Previously a placeholder folder at `skills/05_opportunity_report/` (created 2026-05-15 as a Plan 06 stub). JP delivered initial content + DOCX renderer in `SKills updated.zip` on 2026-05-18; integrated same day.

- **Created** `SKILL.md` from JP's `opportunity-report-new/SKILL.md`. Role: final client-facing deliverable — the **Reporte de Oportunidades de IA** that consolidates the 4 prior skill outputs + the discovery-call notes into a 6-10-opportunity report with 2 Quick Wins + 4-week plan. 7 sections per JP's design. Ratio: 90 % value delivered / 10 % invitation to the paid "Hoja de Ruta de IA" (post-engagement service, scope TBD).
- **Inputs (required):** `*_AnalisisCompania_*.md` (Skill 01), `*_CO_*.md` or `*_MX_*.md` (Skill 02 industry), `*_Competencia_*.md` (Skill 03), `*_NotasCliente_*.md` (post-call meeting notes).
- **Output:** `[Empresa]_ReporteOportunidades_YYYYMMDD.docx` — professional .docx for direct client delivery.
- **Anti-hallucination discipline:** the SKILL.md carries the data-confidence label system (✅ / ⚠️ / ❓) plus three absolute prohibitions (no unsourced ROI, no fabricated client processes, no unnamed competitor comparisons). This is the strictest anti-hallucination block of all 5 skills because the output is the only one that goes directly to the client.
- **Created** `scripts/generate_docx.py` from JP's bundle. Renders the .docx with Nexostrat branding (palette + typography matching the 4 sibling skills' renderers).
- **Sed-replaced** 5 legacy `Mejía, IA & CIA` → `Nexostrat` in `scripts/generate_docx.py` (JP forgot to update the .py file when finalizing the bundle).
- **Registered** via `.claude/skills/opportunity-report → ../../skills/05_opportunity_report` symlink at the repo root — auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.
- **Registered** in `infra/scripts/test_skills.sh` SKILLS array as `05_opportunity_report:opportunity-report`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL.

**Pipeline position** (per JP's 2026-05-18 diagram): this skill runs **after** the 30-min discovery call. Its output is the FREE deliverable that Nexostrat sends to the prospect. The internal review (Ricardo + JP) before send is **mandatory** — no report leaves without explicit approval.
