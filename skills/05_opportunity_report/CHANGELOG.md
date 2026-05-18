# Changelog — `05_opportunity_report`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

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
