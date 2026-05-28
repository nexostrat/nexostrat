# Session 27 — Skill 6 install + Aurora brand alignment + Odoo CE decision

**Date:** 2026-05-28 (twenty-seventh session)
**Persona:** Founder
**Host:** `ricardo-desktop` (`100.104.83.2`)
**Topic:** Install JP's Skill 6 (`nexostrat-client-deliverables`, Pipeline v2 F1), align it to the canonical Aurora brand, run it end-to-end, and lock the Odoo CE direction (deferring the build).

## Narrative

Ricardo opened with "continue implementing the updates." After surfacing that the Pipeline v2 roadmap's next phases were mostly JP-gated, he redirected: he'd uploaded a new skill (`nexostrat-client-deliverables`) to install, descoped the F4 capabilities catalog (escalate-to-partner via Neo instead), and asked me to read today's meeting to re-sync. A new test meeting (`2026-05-28_13-44_avances-tareas`) reported several items done (catalog, Plan 04, social handles) — but it was a "prueba" and at least Plan 04's claim didn't hold up against the repo.

**Skill 6 install (Pipeline v2 F1).** Found the bundle at `skills/nexostrat-client-deliverables.skill`. Extracted to `skills/06_client_deliverables/`, archived the bundle to `skills/00_META/skill_packages/`, created the relative `.claude/skills/` symlink. Key wrinkle: this is the **first Node-based skill** (`generate_pptx.js` via pptxgenjs, `generate_client_docx.js`/`generate_internal_docx.js` via the `docx` package) plus Python HTML generators — the other 5 skills use a Python `generate_docx.py` that the harness smoke-tests (CHECK 7). Adapted `infra/scripts/test_skills.sh`: registered 06, made CHECK 7 skip-tolerant for skills without `generate_docx.py`, added CHECK 9 (Node toolchain: `validate_json.py` always-on + `generate_pptx.js` node-gated), renumbered /8→/9. Fixed the macOS `/var/folders` `SKILL_DIR` discovery in PASO 0.1 to a Linux/repo-relative form. Node deps installed via `npm ci`. Harness: **72 PASS · 1 SKIP · 0 FAIL** (the SKIP is the intentional absent `generate_docx.py`); CHECK 9 rendered a real 230 KB PPTX from the bundled fixture.

**Ran it end-to-end.** Generated all six deliverables from the `DistribuidoraLosAndes` fixture into a Desktop folder — PPTX exactly 9 slides, client DOCX with the full 10-section structure (32 headings, 19 tables), 1-page internal briefing. Surfaced two honest brand/content findings: emojis (⚡) and verbatim client quotes, both of which conflict with Ricardo's locked style memories. **Ricardo overruled his own rules for Skill 6** — keep JP's skill behavior as-is. Recorded the carve-out in both memory files (`no-emojis`, `no-verbatim-quotes`).

**Brand alignment v0.2.** Ricardo then asked to align the *visual* brand to the canonical Aurora book (colors + fonts), keeping JP's content behavior. Confirmed the font decision: the 2026-05-27 unification override (`pptx_expert`/`editorial_designer` brand-identity docs + `skills/shared/brand.py`) put everything on **Inter** (+ JetBrains Mono), dropping Century Gothic. Remapped all six generators by *role* (not nearest-hue): JP navy `#1E3A5F` → Midnight `#0C1A2E`, teal `#0E7C65` → Emerald `#10B981`, H3 gray → Ocean Deep, the grays/tints → Aurora grays/Arctic/Sky-100; Amber (`#F59E0B`) and Dark Text (`#1F2937`) were already exactly Aurora. Fonts Calibri/Arial/Segoe UI → Inter; HTML loads Inter via a Google Fonts `@import`. Kept JP's element→color *assignments* (his design), only swapped values + fonts. Regenerated and verified: 9 slides held, slide 1 carries Midnight+Emerald with zero residual navy/teal, HTML loads Inter. Logged as Skill 6 v0.2.

**Odoo.** Ricardo wants to "concentrate in and learn Odoo." Brainstormed it: Odoo CE is free self-hosted (no subscription); he chose to **replace Baserow fully**, **broad suite**, on the **HP server**, deploying by **extending the FOSS-stack compose**. I recommended Docker (less chore than native apt; learning goes into Odoo, not the install). He then deferred the whole build to a dedicated install session on the HP — so I captured the locked decisions + 4-phase migration into `00_META/protocols/sesion-S2` (reframed from "investigate" to "install") rather than writing the full spec/plan now. Notably, Baserow turned out to be a designed-but-dormant state-store Ricardo had never used by hand — which makes replacing it low-regret.

**Close.** Per Ricardo's request, the commit was pushed **directly to all three remotes** (origin + GitHub + Codeberg) so every machine has it over Tailscale — an explicit one-off override of the origin-only push rule (`t-pre-push-hook-block-mirrors` still pending as the mechanical guard).

## Decisions locked
1. Skill 6 installed as a Node-based pipeline skill; harness now tolerates non-`generate_docx.py` skills + has a Node check.
2. Skill 6 visual brand = canonical Aurora (Inter + Aurora palette); content behavior (emojis + verbatim quotes) stays JP's — memories carved out.
3. F6 CRM = **Odoo Community Edition**, self-hosted on HP, replaces Baserow, broad suite, Docker via FOSS-stack compose, 4-phase migration. Build deferred to a dedicated install session (protocol S2).
4. F4 capabilities catalog **descoped** (Neo escalate-to-partner model).

## Files touched
- New: `skills/06_client_deliverables/**` (skill + CHANGELOG v0.1/v0.2), `skills/00_META/skill_packages/nexostrat-client-deliverables.skill`, `.claude/skills/nexostrat-client-deliverables`, this journal.
- Modified: `infra/scripts/test_skills.sh`, `.gitignore`, `skills/README.md`, `skills/CLAUDE.md`, `00_META/CHANGELOG.md`, `00_META/protocols/sesion-S2-investigacion-odoo.md`, `STATUS.md`, `tasks.json`, `CHECKPOINT.md`.
- Memory (outside repo): `no-emojis-no-symbols`, `no-verbatim-quotes-in-copy` (Skill 6 carve-out).

## Next session
Re-scoped `t-trixx-reporte-iteracion-notas-ricardo` (high, due 2026-05-31): discuss the internal report vs the refined diagnosis, produce `Trixx_Diagnostico_Refinado`, then run Skill 6 → first real deliverables (F5). Everything on our end is ready; the only missing input is that refined diagnosis. The Odoo install is its own session on the HP (protocol S2, `t-012`, due 2026-06-15).
