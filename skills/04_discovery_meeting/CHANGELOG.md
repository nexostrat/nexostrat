# Changelog — `04_discovery_meeting` (renamed from `06_discovery_meeting` on 2026-05-18)

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.2 — 2026-05-18 · Rename 06 → 04 + JP content rewrite (new "PrepLlamada" role) + Nexostrat rebrand

**Scope:** integrate JP's 2026-05-18 SKILL.md rewrite (`discovery-meeting-new` from `SKills updated.zip`) + reposition the skill as **Skill 4 in JP's diagram pipeline** (PrepLlamada / Guía de Preparación para Primera Llamada).

- **Folder renamed via `git mv`: `skills/06_discovery_meeting/` → `skills/04_discovery_meeting/`** to match JP's diagram numbering (Skill 4 in the 5-skill pipeline). The frontmatter slug `discovery-meeting` is unchanged → the `.claude/skills/discovery-meeting` symlink simply re-targets the new folder path; no symlink name change.
- **Replaced** `SKILL.md` and `scripts/generate_docx.py` with JP's 2026-05-18 deliverable.
- **Role shift in content:** previously a 60-min post-pay discovery-meeting script (when this skill served as the last "Stage 1" Plan 06 skill); now a 30-min **pre-pay** PrepLlamada document — Ricardo runs it before the discovery call, uses it as the call-script guide, never shares it with the prospect (CONFIDENCIAL marker preserved).
- **Frontmatter description** updated to reflect the new role: "Guía de Preparación para Primera Llamada — Nexostrat. Genera documento pre-llamada (.docx) para que Ricardo llegue sabiendo exactamente qué preguntar."
- **Sed-replaced** 3 legacy `Mejía, IA & CIA` → `Nexostrat` in `scripts/generate_docx.py`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 32 PASS · 0 SKIP · 0 FAIL. Test-harness skill registry updated to `04_discovery_meeting:discovery-meeting`.

---

## v0.1 — 2026-05-17 · Path-hygiene + canonical output destination

*(applies to the previous-numbered `06_discovery_meeting/` folder — content unchanged across the rename.)*

**Scope:** make the skill cleanly runnable inside Nexostrat's current setup. No prompt-content changes.

- **Replaced** bare relative path `scripts/generate_docx.py` (in PASO 4 — Generar el DOCX) with concrete repo-relative path `skills/06_discovery_meeting/scripts/generate_docx.py`. The previous form was fragile — only worked if the operator ran the command from inside `skills/06_discovery_meeting/`.
- **Added** `## SETUP — Destino de outputs` section before `## PASO 0 — VALIDAR LOS TRES INPUTS`. Documents the canonical pipeline destination `pipeline/clients/<slug>/04_meeting_script/runs/<TIMESTAMP>_mode-a/` per spec §7, plus the standalone naming convention `[EmpresaCamelCase]_GuionReunion_YYYYMMDD.md/.docx`. Explicitly calls out the three input dependencies (company-analyst + industry-analyst + competitor-analyst outputs) and the confidentiality rule (private; never shared with prospect).
- **Updated** PASO 4 to clarify that the DOCX renderer applies skill-specific blockquote color coding (green for opening + credibility, orange for sensitive zones, purple for timing, blue for notes) — important for Ricardo's at-a-glance scanning during the meeting.
- **Registered** via `.claude/skills/discovery-meeting → ../../skills/06_discovery_meeting` symlink at the repo root, making the skill auto-discoverable in any Claude Code session opened at `/srv/Nexostrat/`.

**Verified by:** `bash infra/scripts/test_skills.sh` — 27 PASS · 0 SKIP · 0 FAIL.

**Prompt content unchanged.** The 8-section meeting-script template (opening with credibility, area prioritization, question script, opportunity signals, objection handling, what to document, close + next steps, timing distribution), input-validation gate, anti-hallucination block, and area-priority notation (●●● / ●●) are all preserved verbatim.
