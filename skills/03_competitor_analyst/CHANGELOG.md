# Changelog — `03_competitor_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.1 — 2026-05-17 · Path-hygiene + canonical output destination

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** four `/tmp/competitor-analyst/...` references (leftovers from the original Anthropic Skills zip extraction) with concrete repo-relative paths under `skills/03_competitor_analyst/`. Affected commands: extract_financials.py invocation in Paso 3, asset XLSX paths (now resolved automatically by the script's self-locating logic), and generate_docx.py invocation in Paso 5.
- **Simplified** the extract_financials.py invocation: previously the SKILL.md passed three explicit arguments (query + 2 XLSX paths); the script auto-locates the XLSX files via `Path(__file__).parent.parent / "assets"`, so only the query argument is needed. SKILL.md updated to reflect this.
- **Added** `## SETUP — Destino de outputs` workflow section at the top of the workflow block. Documents the canonical pipeline destination `pipeline/clients/<slug>/03_competitor_analysis/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[EmpresaCamelCase]_Competencia_CO_YYYYMMDD.md/.docx`. Also flags the company-analyst input dependency.
- **Registered** via `.claude/skills/competitor-analyst → ../../skills/03_competitor_analyst` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 8-section competitive-analysis template, anti-hallucination block, competitor identification criteria, and IA-adoption signal-gathering workflow are all preserved verbatim.
