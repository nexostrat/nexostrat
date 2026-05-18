# CHECKPOINT — root (Founder)

**Updated:** 2026-05-18T22:30:00-07:00
**By:** ricardo (via Claude Code session at /srv/Nexostrat/)
**Persona:** Founder
**Session topic:** Intake-upload workflow shipped end-to-end · ADR-027 2-file split implemented · `infra/scripts/new-client.sh` interim scaffolder built · trigger phrase `Analiza <slug>` locked · Critical-path Priority 1 closed 4 days ahead of due

## What just happened (last session — read once, don't re-litigate)

~1-hour single-arc execution opened with Ricardo's directive *"Lets continue with the setup."* No detours. Five concrete deliverables landed:

**1. ADR-027 2-file intake templates** at `skills/shared/`:
- `research_input_template.md` — facts (identity, presence, contacts, origin, LinkedIn pre-trabajo, audience + factual operational context — slice 1+2 of legacy form). Pasted as context when invoking Skills 01-03.
- `our_hypotheses_template.md` — judgment (dolor hypothesis, decisor read, presupuesto estimate, tono, sensibilidades, capability-fit, "things we expect research to confirm/refute" — slice 3). **SEALED during Skills 01-03** per ADR-027; only opens at Skill 04+05 synthesis.
- Both files self-document via YAML frontmatter (`file_type` / `adr` / `slice` / `read_by` / `sealed_during` / `companion`) making the discipline machine-introspectable for future tooling.

**2. `infra/scripts/new-client.sh`** — interim scaffolder. ~170 LOC bash, executable, `set -euo pipefail`. Usage:
```
bash infra/scripts/new-client.sh <slug> <country-ISO2> '<Legal Name>' <sector> [--pilot]
```
Validates slug + country regex; refuses to overwrite existing target; copies `_template/` → `clients/<slug>/`; drops the 2 intake templates into `00_intake/`; sed-substitutes 8 placeholders in `state.json` + 3 in `checkpoint.md` + slug-stamps the 2 intake template title headers; flips `pilot=true` when `--pilot` flag present; replaces the carried-over meta-README with a per-client stub (the meta-README stays on `_template/`); prints a clear next-steps banner including the `Analiza <slug>` trigger.

**3. Stage-folder rename `_template/04_meeting_script/` → `04_prep_llamada/`** via `git mv` (history preserved). Closes naming drift from yesterday's `06_*` → `04_*` integration. Canonical stage table in `skills/README.md` was already correct; `_template/README.md` row 4 updated (folder + owning-skill name = `discovery-meeting`).

**4. Legacy `operations/templates/fase_0_intake_form.md` deleted** via `git rm` (single-file form superseded by ADR-027 2-file split). Live operational references updated: `calendar.json` (`e-intake-upload-workflow` title flipped to DONE + notes refreshed), `tasks.json` (`t-intake-upload-workflow` closed; `t-trixx-logistics-setup` notes refreshed with concrete `new-client.sh` invocation; `t-migrate-pilotos-to-clients` had stale `04_meeting_script/` ref → corrected; `updated` timestamp bumped). Historical references (STATUS Recent activity older entries, CHANGELOG row 6, journal `2026-05-18_jp-delivery...`, proposal `2026-05-18_impacto-redesign...`) left as-is — they describe what was true then.

**5. Trigger phrase locked: `Analiza <slug>`.** Ricardo picked option 3 from AskUserQuestion (Spanish, brief, slug-anchored, matches SKILL.md description-field activation patterns already in place). Documented in `pipeline/clients/_template/README.md` (new "Scaffolding a new client" + "Post-scaffold workflow" sections with the 7-step canonical workflow: scaffold → fill research_input → fill our_hypotheses → trigger pipeline → human review between every skill → 30-min discovery call → Skill 05 → mandatory Ricardo+JP review → manual send) + `skills/README.md` (new "Per-client invocation" section between Path B and Canonical output destination). The per-client stub README that `new-client.sh` writes also includes the slug-anchored trigger example.

**Smoke test:** ran `bash infra/scripts/new-client.sh smoketest-tmp MX 'Smoke Test SA de CV' logistica --pilot` against a throwaway slug. All 13 expected stage folders present with `.gitkeep`; `state.json` valid against `nexostrat-client-state-v1` (all 8 placeholders substituted, `pilot=true` flipped correctly, ISO timestamps populated); `checkpoint.md` slug-stamped + `CHECKPOINT_NO_ACTIVE_WORK` token preserved; both intake templates copied + title headers slug-substituted; per-client stub README written with country + sector + pilot flag visible; idempotency check (second invocation against same slug) refused cleanly. Cleaned up via `rm -rf`. Test harness `bash infra/scripts/test_skills.sh` held **32 PASS · 0 SKIP · 0 FAIL** throughout. `validate_schemas.sh` PASS for tasks.json + calendar.json after edits.

## Decisions locked this session — DO NOT re-open without explicit cause

1. **`skills/shared/{research_input_template.md, our_hypotheses_template.md}` are the canonical intake templates.** Any future tweak to the intake convention (adding a field, splitting a section, tightening discipline) is a single-file edit in `skills/shared/` and propagates to every new client via `new-client.sh`.

2. **`infra/scripts/new-client.sh` is the only sanctioned way to scaffold a new client folder.** Manual `cp -r _template/` is forbidden going forward — drift between the helper and the manual approach is a guaranteed source of bugs. Plan 07 replaces this with a richer scaffolder; until then, this script is the source of truth.

3. **`Analiza <slug>` is the locked trigger phrase.** No alternates documented (avoid ambiguity). Plan 07's `/intake` Telegram plugin will also emit `intake.completed` events; once that lands, this manual trigger remains the in-Claude-Code path while Telegram triggers the same handoff from outside.

4. **ADR-027 two-file split is enforced socially at Stage 1.** Operator discipline only. Plan 03's events.jsonl + Plan 07's intake plugin can enforce mechanically later. Self-documenting frontmatter on both templates (the `sealed_during:` field) is the social-enforcement anchor.

5. **Stage folder name = `04_prep_llamada/`.** This is the canonical name. Skill folder remains `04_discovery_meeting/`. The two-name pattern (station name vs skill name) is the spec's design — don't try to unify them.

## In flight — concrete next action

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads this CHECKPOINT + STATUS + tasks + calendar
     + latest journal (2026-05-18c_intake-workflow.md).
  4. Claude presents the 2-priority path forward (P1 already done).

CRITICAL PATH (2 remaining priorities — execute in order):

  ┌── 2026-05-24 ──────────────────────────────────────┐
  │  1. (was P2) Scaffold Trixx Logistics + intake.   │
  │                                                    │
  │     bash infra/scripts/new-client.sh \             │
  │       trixx-logistics MX \                         │
  │       'Trixx Logistics Corp. (Grupo Trixx)' \      │
  │       'logistica-cross-border' --pilot             │
  │                                                    │
  │     Then fill 00_intake/research_input.md from     │
  │     WhatsApp + site-scrape intel (offices, services│
  │     contacts, no-RFC-on-site, "0 Años" bug, etc.). │
  │     Then fill 00_intake/our_hypotheses.md with our │
  │     judgment (sealed — not pasted to Skills 01-03).│
  │     Save initial-contact comm to communications/.  │
  │     Write checkpoint.md "Awaiting Skill 01".       │
  │     t-trixx-logistics-setup (~30 min)              │
  └─────────────────────┬─────────────────────────────┘
                        │
  ┌── 2026-05-25 1pm Tijuana ──▼──────────────────────┐
  │  2. (was P3) Run Skills 1→2→3→4 serially on      │
  │     Trixx Logistics with human review + notes     │
  │     between each. Trigger: "Analiza               │
  │     trixx-logistics" → Skill 01 (reads            │
  │     research_input.md). Then review → Skill 02 →  │
  │     review → Skill 03 → review → Skill 04         │
  │     (PrepLlamada, first skill to also read        │
  │     our_hypotheses.md). PrepLlamada is the        │
  │     meeting guide. Optionally practice meeting    │
  │     with JP first. Then: meeting → record →       │
  │     Skill 5 → Ricardo+JP review → manual send.    │
  │     t-monday-meeting-prep                         │
  └───────────────────────────────────────────────────┘

PARALLEL (non-blocking, can run any time):

  ┌── 2026-05-30 ─┐
  │  Migrate Bodai, Ascenso, Scarab from Pilotos/ to
  │  pipeline/clients/<slug>/ per canonical structure.
  │  Use new-client.sh for each then move existing
  │  artifacts into station folders.
  │  t-migrate-pilotos-to-clients
  └───────────────┘

DEFERRED PER JP DIRECTIVE (wait for pilot evidence):
  - t-redesign-technical-brainstorm
  - t-build-automation-surface
  - t-update-phase-state-machine
```

## Architecture-conflict check (passed)

Both remaining critical-path priorities use canonical paths from spec §6.4 + ADR-027. None conflicts with future Plans 02-10 execution:

| Priority | Canonical path used | Conflict risk |
|---|---|---|
| 1 Trixx scaffold | `pipeline/clients/_template/` → `trixx-logistics/` via `new-client.sh`; 2-file intake per ADR-027 | None — exactly the shape Plan 07 expects. `new-client.sh` is the documented interim until Plan 07's full version |
| 2 Skills 1-4 run | Production-registered skills + brand layer + intake layer locked | None — exercises what exists end-to-end |
| Parallel: Pilots migration | `pipeline/clients/<slug>/` per spec; per-skill outputs to canonical station folders | None — cleans up architectural drift; can reuse `new-client.sh` for the 3 scaffolds |

**Workflow layer status:** intake convention (`new-client.sh` + 2-file templates + `Analiza <slug>` trigger) is independent of any pending plan. Plan 07 supersedes `new-client.sh` with a richer scaffolder + Telegram trigger; until then, today's script + templates are the source of truth.

## Blocked on

**For next-session priority 1 (Trixx scaffold):** nothing. Single command + 2 markdown fills.

**For priority 2 (Skills run on Trixx):** priority 1 must land first (state.json + intake files must exist before `Analiza trixx-logistics` triggers Skill 01).

**For warm-standby Tasks 7-12 (parallel):** physical second host (unchanged).

**For JP-side TTY-deferred items (parallel):** JP availability (Telegram message ready in `t-plan-01a-jp-and-tty-deferred`).

## Open questions

**None blocking.** Soft items to surface at next session start:

1. **Trixx intel gaps that Skill 01 will research** — RFC (not visible on site, needs search), team size, real financial state (vs site "0 Años" placeholder bug), real years founded, certifications likely (C-TPAT and OEA for cross-border), specific China-MX or LATAM-USA niche. Intake captures what we know; Skill 01 fills gaps.
2. **Sector slug choice for Trixx** — locked as `logistica-cross-border` to capture the customs + freight + cross-border MX-US niche. Could be more granular (`logistica-aduanal-cross-border`) but adds noise. Confirm at scaffolding time or override on the `new-client.sh` invocation.

## Files modified but not yet committed at session start

Session-end commit will land all of:

- `skills/shared/research_input_template.md` (NEW)
- `skills/shared/our_hypotheses_template.md` (NEW)
- `infra/scripts/new-client.sh` (NEW, executable)
- `operations/templates/fase_0_intake_form.md` (DELETED via `git rm`)
- `pipeline/clients/_template/04_meeting_script/.gitkeep` → `pipeline/clients/_template/04_prep_llamada/.gitkeep` (RENAMED via `git mv`)
- `pipeline/clients/_template/README.md` (stage row corrected + scaffold + post-scaffold workflow sections)
- `skills/README.md` (new "Per-client invocation" section)
- `calendar.json` (`e-intake-upload-workflow` title + notes refreshed to DONE state)
- `tasks.json` (`t-intake-upload-workflow` closed; `t-trixx-logistics-setup` notes refreshed; `t-migrate-pilotos-to-clients` stale ref fixed; `updated` timestamp bumped)
- `STATUS.md` (header + Current phase + Done-this-session + Next sequence + new Recent activity entry)
- `00_META/CHANGELOG.md` (2026-05-18 PM third-session row added)
- `00_META/journal/2026-05-18c_intake-workflow.md` (NEW — full session narrative)
- `CHECKPOINT.md` (this file, rewritten)

## Estimated time to finish (roadmap)

- **Critical path (priorities 1-2):** ~1 day's worth of focused work across two sessions, completing 2026-05-25 with the Trixx Logistics pilot meeting.
- **Architecture migration (parallel):** ~1-2h, due 2026-05-30. `new-client.sh` makes each of the 3 scaffolds a one-liner.
- **Stage 1 launch realistic:** unchanged at 2026-07-15 to 2026-07-30. Depends on 1-2 successful pilots under the new process + JP's "ready to keep building" signal.

## After this, what's next

Trixx Logistics pilot → Ricardo+JP post-meeting review → 1-2 more real pilots if Trixx surfaces process gaps OR Skill 05 to first delivered report if Trixx accepts → real client closes via "Hoja de Ruta de IA" → architecture brainstorm reopens (deferred items) → Plans 02-10 sequenced just-in-time.

## For a future auditor reading this baton

This was the 10th major execution arc since 2026-05-15 (Plan 01a Tasks 1-11 + Plan 01a Tasks 12-18 + hard-system-audit + Plan 01b mirror cluster + Plan 01b re-audit + Plan 01c re-audit + Plan 01c execute + skill-hygiene + 3-company-pilot batch + JP-delivery-and-integration + brand-wire-up-and-shared-module + this intake-workflow arc). Pattern unbroken: each arc was an executed-and-audited release.

The 2026-05-18 PM third-session arc is where **the production-pipeline ergonomics surface becomes locked**. The intake boundary now has zero friction: scaffold with one command, fill two markdown files, trigger with one phrase. Brand layer (locked in PM second session) + intake layer (locked in this session) = Trixx pilot can run on Monday with the same surface that every future client will use.

Reading order for re-auditing this arc:
1. This CHECKPOINT.
2. `STATUS.md` Current state + Done-this-session + top Recent activity entry.
3. Journal `00_META/journal/2026-05-18c_intake-workflow.md` (full narrative + decisions).
4. `infra/scripts/new-client.sh` (the script itself, ~170 LOC, fully documented).
5. Both templates at `skills/shared/` (read both — the seal-during-research discipline only makes sense when you see both sides).
6. `pipeline/clients/_template/README.md` § "Scaffolding a new client" + "Post-scaffold workflow" (the canonical 7-step workflow).
7. `skills/README.md` § "Per-client invocation" (the trigger-phrase contract).

The session-end bookkeeping commit (next) locks all of this. Next session opens at the Trixx Logistics scaffold (P1 → P2 for Monday's meeting).

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the 2-priority path forward.*
