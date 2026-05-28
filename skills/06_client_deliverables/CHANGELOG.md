# Changelog — `06_client_deliverables`

All notable changes to this skill's prompt + scripts are listed here, newest first.

The git commit SHA at the time of each version pin is the authoritative artifact (per ADR-022). This file is the human-readable index.

---

## v0.2 — 2026-05-28 · Aurora brand alignment (colors + fonts)

**Scope:** aligned all six generators to the canonical Aurora brand book (`skills/shared/brand.py` + `nexostrat_editorial_designer/references/brand-identity.md`). Content behavior is unchanged — Ricardo explicitly chose to keep JP's skill behavior (emojis + verbatim client quotes); only the visual brand (palette + typography) was remapped. JP's element→color *assignments* were preserved; only the color *values* and fonts changed.

**Driver:** JP authored the generators with an independent palette (navy `#1E3A5F` + teal `#0E7C65`) and Calibri/Arial/Segoe UI fonts, so Skill 6 deliverables didn't visually match the rest of the pipeline (skills 01-05 render Aurora via `brand.py`). Ricardo: "fix so it has the canonical brand book decision taken, include fonts, colors."

**Color remap (by role, applied to all 6 generators):**
- `1E3A5F` / `162D4A` / `0E2A45` / `0F172A` (navy) → Midnight `0C1A2E`
- `374151` (H3 gray) → Ocean Deep `0D4A6B`
- `0E7C65` (teal) → Emerald `10B981`
- `64748B` / `475569` / `94A3B8` (secondary text) → Gray 500 `6B7280`
- `F8FAFC` (alt-row bg) → Gray 100 `F5F5F5`; `F1F5F9` / `EFF6FF` (light blue bg) → Arctic `F0FBFF`
- `E2E8F0` / `CBD5E1` (borders) → Gray Mid `D1D5DB`; `DBEAFE` / `BFDBFE` / `ACEBEF` (tints) → Sky-100 `E0F2FE`
- `1E40AF` (accent blue) → Sky Blue `0EA5E9`
- Unchanged (already on-brand or semantic): Amber Gold `F59E0B`, Dark Text `1F2937`, White, emerald/amber/red tints.

**Font remap:** Calibri (PPTX) / Arial (DOCX) / Segoe UI (HTML) → **Inter** everywhere (per the 2026-05-27 unification override that aligned slides to `brand.py`'s `BRAND_FONT="Inter"`; Century Gothic explicitly dropped). Monospace → JetBrains Mono. HTML generators load Inter + JetBrains Mono via a Google Fonts `@import` with a system-font fallback (matches the meeting-summary PDF template pattern).

**Verified by:** regenerated all 6 sample deliverables from the bundled fixture → PPTX still exactly 9 slides; slide 1 carries Midnight `0C1A2E` + Emerald `10B981` with zero residual navy/teal; HTML loads Inter. `bash infra/scripts/test_skills.sh` → 72 PASS · 1 SKIP · 0 FAIL.

**Note:** const names in the JS files (`NAVY`, `GREEN`) are now slight misnomers (they hold Midnight/Emerald values) — left as-is to keep the diff a pure value swap; the values are authoritative. Century-Gothic-for-print line in `editorial_designer/references/design-specs.md` is stale vs the Inter unification — a docs cleanup for later, not a Skill 6 issue.

---

## v0.1 — 2026-05-28 · Initial install (JP delivery, Pipeline v2 F1)

**Scope:** first installation of the client-facing deliverables skill (Skill 6) into the Nexostrat skills bucket. JP authored and delivered the `.skill` bundle; Ricardo + Founder Claude wrapped it into the canonical `skills/06_client_deliverables/` shape.

**Driver:** Pipeline v2 (`00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md`) roadmap phase F1 — the skeleton/generator for the Ciclo 1 client deliverables. Consumes the refined diagnosis (`*_Diagnostico_Refinado_*.md`) and produces 6 outputs:

1. `{Empresa}_Diagnostico_Presentacion_{YYYYMMDD}.pptx` — pitch ejecutivo 9 slides
2. `{Empresa}_Diagnostico_Presentacion_{YYYYMMDD}.html` — HTML de la presentación
3. `{Empresa}_Diagnostico_Documento_{YYYYMMDD}.docx` — documento completo (10-15 págs)
4. `{Empresa}_Diagnostico_Documento_{YYYYMMDD}.html` — HTML del documento
5. `Ricardo_BriefingInterno_{Empresa}_{YYYYMMDD}.docx` — briefing interno Ricardo (1 pág.)
6. `Ricardo_BriefingInterno_{Empresa}_{YYYYMMDD}.html` — HTML del briefing

**Toolchain note (departs from the other 5 skills):** this skill is **Node-based** for PPTX + DOCX generation (`generate_pptx.js` via `pptxgenjs`, `generate_client_docx.js` + `generate_internal_docx.js` via the `docx` package) plus Python for the HTML renderers (`generate_html_*.py`) and `validate_json.py`. The other 5 skills use a Python `generate_docx.py`. Node v24 + npm 11 confirmed available; deps install at runtime via `npm ci` (lockfile bundled), and `scripts/node_modules/` is gitignored.

**Install steps applied:**
- Extracted `nexostrat-client-deliverables.skill` → `skills/06_client_deliverables/`; archived the bundle to `skills/00_META/skill_packages/`.
- Adapted `SKILL.md` PASO 0.1: replaced the macOS `/var/folders` `SKILL_DIR` discovery with a Linux/repo-relative one (find under `/srv/Nexostrat/skills` + `git rev-parse` fallback).
- Created relative symlink `.claude/skills/nexostrat-client-deliverables → ../../skills/06_client_deliverables`.
- Gitignored `skills/06_client_deliverables/scripts/node_modules/`.
- Adapted `infra/scripts/test_skills.sh`: added 06 to the registry; made CHECK 7 (`generate_docx.py`) skip-tolerant for skills using an alternate DOCX generator; added CHECK 9 (Skill 06 Node toolchain — `validate_json.py` on the bundled fixture always-on + `generate_pptx.js` render gated on node + deps); renumbered checks /8 → /9.

**Verified by:** `bash infra/scripts/test_skills.sh` → **72 PASS · 1 SKIP · 0 FAIL**. The 1 SKIP is the intentional absence of `generate_docx.py`. CHECK 9 rendered a real 230 KB PPTX from the bundled fixture (`tests/data_DistribuidoraLosAndes.json`); `validate_json.py` accepted the fixture.

**Pendiente / not done this install:**
- Brand alignment audit: confirm `generate_pptx.js` / `generate_client_docx.js` Aurora palette matches `skills/shared/brand.py` (JP authored independently). Tracked as a follow-up.
- Canonical pipeline destination `etapa_2_diagnostico/entregables/` not yet created in `pipeline/clients/_template/` — lands on first real client run (Pipeline v2 F5).
- First end-to-end run against a real refined diagnosis (Trixx) — Pipeline v2 F5, gated on the Trixx report iteration (S3).
