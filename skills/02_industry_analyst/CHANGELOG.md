# Changelog — `02_industry_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.1 — 2026-05-17 · Path-hygiene + canonical output destination

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** `/tmp/industry-analyst/scripts/generate_docx.py` reference (leftover from the original Anthropic Skills zip extraction) with concrete repo-relative path `skills/02_industry_analyst/scripts/generate_docx.py`.
- **Added** `## SETUP — Destino de outputs` workflow section at the top of the workflow block. Documents the canonical pipeline destination `pipeline/clients/<slug>/02_industry_analysis/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[SectorCamelCase]_CO_YYYYMMDD.md/.docx`. Also flags the per-sector reusability pattern (~6-12 month vigencia) for sector-report caching.
- **Updated** Paso 3 (Generar el .docx) instructions to use the corrected path and reference the canonical output naming.
- **Registered** via `.claude/skills/industry-analyst → ../../skills/02_industry_analyst` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 10-section sector-report template, anti-hallucination block, research order, and reusability rules are all preserved verbatim.
