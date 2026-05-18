# Changelog — `02_industry_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.2 — 2026-05-18 · JP content delivery + Linux path fix + Nexostrat rebrand

**Scope:** integrate JP's 2026-05-18 SKILL.md rewrite (`industry-analyst-new` from `SKills updated.zip`).

- **Replaced** `SKILL.md` and `scripts/generate_docx.py` with JP's 2026-05-18 deliverable.
- **Added** `references/sector_associations.md` (new reference doc from JP).
- **Replaced** `references/sources_guide.md`.
- **Frontmatter description** now includes Mexico (RFC) support — accepts company-analyst report and detects country (CO vs MX) automatically.
- **Fixed** `/tmp/industry-analyst/scripts/generate_docx.py` Mac/tmp-path reference at SKILL.md line 113 → `skills/02_industry_analyst/scripts/generate_docx.py` (repo-relative).
- **Sed-replaced** 2 legacy `Mejía, IA & CIA` → `Nexostrat` in `scripts/generate_docx.py` (JP forgot to update the .py files when rewriting the SKILL.md).

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL.

---

## v0.1 — 2026-05-17 · Path-hygiene + canonical output destination

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** `/tmp/industry-analyst/scripts/generate_docx.py` reference (leftover from the original Anthropic Skills zip extraction) with concrete repo-relative path `skills/02_industry_analyst/scripts/generate_docx.py`.
- **Added** `## SETUP — Destino de outputs` workflow section at the top of the workflow block. Documents the canonical pipeline destination `pipeline/clients/<slug>/02_industry_analysis/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[SectorCamelCase]_CO_YYYYMMDD.md/.docx`. Also flags the per-sector reusability pattern (~6-12 month vigencia) for sector-report caching.
- **Updated** Paso 3 (Generar el .docx) instructions to use the corrected path and reference the canonical output naming.
- **Registered** via `.claude/skills/industry-analyst → ../../skills/02_industry_analyst` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 10-section sector-report template, anti-hallucination block, research order, and reusability rules are all preserved verbatim.
