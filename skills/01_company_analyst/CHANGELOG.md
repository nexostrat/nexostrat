# Changelog — `01_company_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.1 — 2026-05-17 · Path-hygiene + DOCX renderer + canonical output destination

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** `<skill_dir>/scripts/extract_financials.py` placeholders with concrete repo-relative path `skills/01_company_analyst/scripts/extract_financials.py`. Added note that the script auto-locates via `Path(__file__).parent.parent / "assets"`.
- **Removed** two broken references to the Anthropic Skills DOCX bundle (`/var/folders/.../skills/docx/SKILL.md`) — that bundle is not installed on this machine.
- **Added** `skills/01_company_analyst/scripts/generate_docx.py` — a Mejía-branded renderer modeled on the sibling skills (industry-analyst, competitor-analyst, discovery-meeting). Produces a Word document with shared brand palette (dark blue + accent blue + mid-gray) and consistent typography across the four mature skills' outputs.
- **Added** `## SETUP — Destino de outputs` workflow section at the top of the workflow block. Documents the canonical pipeline destination `pipeline/clients/<slug>/01_company_analysis/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[Empresa]_AnalisisCompania_YYYYMMDD.md/.docx`.
- **Updated** PASO 4 (Generar outputs) to invoke the local `generate_docx.py` directly rather than delegating to the Anthropic Skills DOCX bundle.
- **Registered** via `.claude/skills/company-analyst → ../../skills/01_company_analyst` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 13-section report template, anti-hallucination block, financial-extraction workflow, and quality rules are all preserved verbatim.
