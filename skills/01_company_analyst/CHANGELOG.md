# Changelog — `01_company_analyst`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.2 — 2026-05-18 · JP content delivery + DOCX-skill paradigm fix

**Scope:** integrate JP's 2026-05-18 SKILL.md rewrite (`company-analyst-new` from `SKills updated.zip`) + adapt for Linux + preserve v0.1 DOCX renderer.

- **Replaced** `SKILL.md` with JP's 2026-05-18 deliverable. New frontmatter description adds Mexico (RFC) support alongside Colombia (NIT) — country auto-detection.
- **Replaced** `references/sources_guide.md` and `scripts/extract_financials.py` with JP's updated versions.
- **Replaced** both XLSX assets (`supersociedades_balance_general.xlsx` + `supersociedades_estado_resultados.xlsx`) with JP's updated versions.
- **Preserved** our `scripts/generate_docx.py` from v0.1 — JP did not include a DOCX renderer for this skill in his bundle.
- **Fixed** two `/var/folders/.../skills/docx/SKILL.md` Mac-paradigm references at SKILL.md lines 176 + 487 (Anthropic Skills v2 meta-skill referencing). Replaced with our local `python skills/01_company_analyst/scripts/generate_docx.py <ruta_md> <ruta_docx>` pattern (consistent with the 4 sibling skills' DOCX invocation).

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL.

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
