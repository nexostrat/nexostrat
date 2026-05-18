# Changelog — `03_competitor_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.3 — 2026-05-18 · Brand wire-up + shared-module migration

**Scope:** apply Nexostrat Brand Guide v1.0 to `scripts/generate_docx.py`, then migrate to `skills/shared/brand.py`.

- Aurora palette: `DARK_BLUE → #0C1A2E` (Midnight Blue), `ACCENT → #0EA5E9` (Sky Blue), `MID_GRAY → #6B7280` (Gray 500). H2 paragraph bottom-border + table-header background updated.
- Cover logo: `Nexostrat_Logo_Fondo_Arctic_Transparente.png` at 3.8" via `brand.apply_cover_logo(doc)`.
- Body-pages header + footer via `brand.apply_brand_header(doc)` + `brand.apply_brand_footer(doc)`; cover skipped via `different_first_page_header_footer`.
- Migrated to `skills/shared/brand.py` — all 9 brand references resolve through `brand.*`. No domain-specific colors needed.

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL. End-to-end render of pilot competitor-analyst .md → branded .docx passes XML inspection.

---

## v0.2 — 2026-05-18 · JP content delivery + Linux path fix + Nexostrat rebrand

**Scope:** integrate JP's 2026-05-18 SKILL.md rewrite (`competitor-analyst-new` from `SKills updated.zip`).

- **Replaced** `SKILL.md`, `references/competitor_research_guide.md`, both scripts (`extract_financials.py` + `generate_docx.py`), and both XLSX assets with JP's 2026-05-18 deliverable.
- **Frontmatter description** now includes Mexico (RFC) support alongside Colombia (NIT).
- **Fixed** four `/tmp/competitor-analyst/...` Mac/tmp-path references at SKILL.md lines 113-115 + 131 → `skills/03_competitor_analyst/...` (repo-relative).
- **Sed-replaced** 2 legacy `Mejía, IA & CIA` → `Nexostrat` in `scripts/generate_docx.py`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL.

---

## v0.1 — 2026-05-17 · Path-hygiene + canonical output destination

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** four `/tmp/competitor-analyst/...` references (leftovers from the original Anthropic Skills zip extraction) with concrete repo-relative paths under `skills/03_competitor_analyst/`. Affected commands: extract_financials.py invocation in Paso 3, asset XLSX paths (now resolved automatically by the script's self-locating logic), and generate_docx.py invocation in Paso 5.
- **Simplified** the extract_financials.py invocation: previously the SKILL.md passed three explicit arguments (query + 2 XLSX paths); the script auto-locates the XLSX files via `Path(__file__).parent.parent / "assets"`, so only the query argument is needed. SKILL.md updated to reflect this.
- **Added** `## SETUP — Destino de outputs` workflow section at the top of the workflow block. Documents the canonical pipeline destination `pipeline/clients/<slug>/03_competitor_analysis/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[EmpresaCamelCase]_Competencia_CO_YYYYMMDD.md/.docx`. Also flags the company-analyst input dependency.
- **Registered** via `.claude/skills/competitor-analyst → ../../skills/03_competitor_analyst` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 8-section competitive-analysis template, anti-hallucination block, competitor identification criteria, and IA-adoption signal-gathering workflow are all preserved verbatim.
