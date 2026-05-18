# 2026-05-18 (4th session) — Intake-upload workflow shipped end-to-end

**Persona:** Founder
**Operator:** Ricardo
**Duration:** ~1 hour, single execution arc, no detours
**Critical-path priority closed:** P1 (was renumbered from yesterday's P3) — `t-intake-upload-workflow`, 4 days ahead of the 2026-05-22 due date

---

## Why this session

Yesterday's CHECKPOINT laid out the 3-priority critical path for Monday's Trixx Logistics pilot (2026-05-25 1pm Tijuana). P2 (brand renderer wire-up) closed in the second session of 2026-05-18 PM, ahead of due. P1 (intake-upload workflow) was the next gating item: the convention by which Ricardo drops a filled intake form and Claude picks it up to start the 4-skill pipeline. P1 unblocks P2 (`t-trixx-logistics-setup`) which unblocks P3 (`t-monday-meeting-prep`).

Ricardo's directive on session open: *"Lets continue with the setup."* No detours.

---

## What landed

### 1. ADR-027 two-file intake split (templates)

Yesterday's session left a single-file template at `operations/templates/fase_0_intake_form.md` (Spanish, 7 sections, mixed facts + judgment). That conflicts with **ADR-027** in the founding spec, which mandates a **2-file split**:

| File | Slice | Contents | Who reads it |
|---|---|---|---|
| `00_intake/research_input.md` | facts (1+2) | identity, presence, contacts, origin, LinkedIn pre-trabajo, audience + factual operational context | Skills **01, 02, 03** |
| `00_intake/our_hypotheses.md` | judgment (3) | dolor hypothesis, decisor read, presupuesto estimate, tono, sensibilidades, capability-fit, "things we expect research to confirm/refute" | Skills **04, 05** only |

**Why the split matters:** if Skills 01-03 (research stage) read our hypotheses, their output is contaminated. We lose the *"what we expected vs what research found"* signal that Claude-as-Judge consumes at Skill 05 synthesis (per ADR-027). The discipline is socially enforced at Stage 1 — the operator does not paste `our_hypotheses.md` content into the model while running research skills. Plan 03 (events.jsonl) can later enforce mechanically.

Templates written at:
- `skills/shared/research_input_template.md` — 7 sections, all factual
- `skills/shared/our_hypotheses_template.md` — 7 sections, all judgment, with frontmatter `sealed_during: [skill-01..., skill-02..., skill-03...]` self-documentation and an explicit footer warning *"NO pegar este archivo como contexto al invocar Skills 01-03."*

Both files include YAML frontmatter declaring `file_type`, `adr`, `slice`, `read_by`, `sealed_during`, `companion` — making the discipline machine-introspectable for future tooling.

### 2. `infra/scripts/new-client.sh` — interim scaffolder

The CHECKPOINT projected this task as `(~30-45 min)` for docs + convention. After the AskUserQuestion on whether to build a helper script vs document the manual cp, Ricardo picked **"Build it now"** with the rationale that reproducibility beats fragility for a workflow about to be used on a real client.

Script characteristics:
- `set -euo pipefail`, ~170 LOC bash
- Usage: `bash infra/scripts/new-client.sh <slug> <country-ISO2> '<Legal Name>' <sector> [--pilot]`
- Slug validation: `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` (lowercase + dashes, no leading/trailing dash)
- Country validation: ISO-3166 alpha-2
- **Idempotent failure**: refuses to overwrite an existing `pipeline/clients/<slug>/` with clear instructions
- Effect:
  - `cp -r _template/ clients/<slug>/`
  - Copy 2 intake templates from `skills/shared/` to `00_intake/`
  - sed-substitute placeholders in `state.json` (8 placeholders) + `checkpoint.md` (3 placeholders) + intake template title headers (slug)
  - Flip `pilot=true` if `--pilot` flag present
  - Replace the carried-over meta-README with a per-client stub (with the meta-README — `_template/README.md` — staying on the template)
  - Print clear "next steps" to stdout including the `Analiza <slug>` trigger phrase

Plan 07 will replace this with a fuller version that also emits to `events.jsonl` and exposes a `/intake` Telegram trigger. Until then, this is the canonical scaffolder.

### 3. Stage-folder drift fix: `04_meeting_script/` → `04_prep_llamada/`

The `_template/04_meeting_script/` folder name dates from before yesterday's `06_discovery_meeting/` → `04_discovery_meeting/` integration. The canonical stage table in `skills/README.md` already says `04_prep_llamada` (the station name; `04_discovery_meeting` is the skill folder). The `_template/` folder was stale.

Fixed via `git mv pipeline/clients/_template/04_meeting_script pipeline/clients/_template/04_prep_llamada` (history preserved). `_template/README.md` row 4 updated: folder + owning-skill name corrected to `discovery-meeting`.

### 4. Legacy single-file form deprecated

`operations/templates/fase_0_intake_form.md` deleted via `git rm`. Live operational references updated:
- `calendar.json` event `e-intake-upload-workflow` title flipped to "DONE 2026-05-18 ahead of deadline" + notes refreshed to point to the new convention
- `tasks.json` notes for both `t-intake-upload-workflow` (now closed) and `t-trixx-logistics-setup` (refreshed with concrete `new-client.sh` invocation)
- `tasks.json` `t-migrate-pilotos-to-clients` had a stale `04_meeting_script/` path reference — corrected to `04_prep_llamada/`

Historical references (STATUS.md Recent activity, `00_META/CHANGELOG.md`, yesterday's journal, the impacto-redesign proposal doc) left as-is — they describe what was true *then*.

### 5. Trigger phrase locked: `Analiza <slug>`

Ricardo picked option 3 from the AskUserQuestion. Reasoning:
- Brief, Spanish, natural muscle memory
- Matches the SKILL.md description-field activation phrasing already in place (e.g., *"analiza la empresa X"*)
- Slug-anchored — Claude can disambiguate clients without ceremony

Documented in:
- `pipeline/clients/_template/README.md` (new "Post-scaffold workflow" section, 7-step canonical)
- `skills/README.md` (new "Per-client invocation" section between Path B and Canonical output destination)
- The per-client stub README that `new-client.sh` writes (slug-anchored example)

### 6. Smoke test

Ran `bash infra/scripts/new-client.sh smoketest-tmp MX 'Smoke Test SA de CV' logistica --pilot` against a throwaway slug:
- All 13 expected stage folders present with `.gitkeep`
- `state.json` valid against `nexostrat-client-state-v1` (all 8 placeholders substituted; `pilot=true` flipped correctly; ISO date + ISO timestamp populated; `phase=prospect` preserved)
- `checkpoint.md` slug-stamped + operator-stamped + `CHECKPOINT_NO_ACTIVE_WORK` token preserved
- Both intake templates copied + title headers slug-substituted
- Per-client stub README written with country + sector + pilot flag
- Idempotency: second invocation against the same slug refused cleanly with directive to `rm -rf` first

Cleaned up the smoketest folder via `rm -rf`. Test harness re-run: **32 PASS · 0 SKIP · 0 FAIL** held throughout.

---

## Decisions locked this session — DO NOT re-open without explicit cause

1. **`skills/shared/{research_input_template.md, our_hypotheses_template.md}` are the canonical intake templates.** Any future tweak to the intake convention (adding a field, splitting a section, tightening discipline) is a single-file edit in `skills/shared/` and propagates to every new client via `new-client.sh`.

2. **`infra/scripts/new-client.sh` is the only sanctioned way to scaffold a new client folder.** Manual `cp -r _template/` is forbidden going forward — drift between the helper and the manual approach is a guaranteed source of bugs. Plan 07 replaces this with a richer scaffolder; until then, this script is the source of truth.

3. **`Analiza <slug>` is the locked trigger phrase.** No alternates documented (avoid ambiguity). Plan 07's `/intake` Telegram plugin will also emit `intake.completed` events; once that lands, this manual trigger remains the in-Claude-Code path while Telegram triggers the same handoff from outside.

4. **ADR-027 two-file split is enforced socially at Stage 1.** Operator discipline only. Plan 03's events.jsonl + Plan 07's intake plugin can enforce mechanically later. Self-documenting frontmatter on both templates (the `sealed_during:` field) is the social-enforcement anchor.

5. **Stage folder name = `04_prep_llamada/`.** This is the canonical name. Skill folder remains `04_discovery_meeting/`. The two-name pattern (station name vs skill name) is the spec's design — don't try to unify them.

---

## What's still open after this session

Critical path remaining (2 priorities, both gating Monday's pilot meeting):

| Priority | Task | Due | Gates |
|---|---|---|---|
| **P1 (was P2)** | `t-trixx-logistics-setup` | 2026-05-24 | Run `new-client.sh` + populate the 2 intake files for Trixx Logistics |
| **P2 (was P3)** | `t-monday-meeting-prep` | 2026-05-25 1pm Tijuana | Skills 1→2→3→4 serial with review between each + PrepLlamada as guide |

Parallel (non-gating):
- `t-migrate-pilotos-to-clients` — due 2026-05-30

Concrete next-session opening command (locked into the `t-trixx-logistics-setup` task notes):
```
bash infra/scripts/new-client.sh trixx-logistics MX 'Trixx Logistics Corp. (Grupo Trixx)' 'logistica-cross-border' --pilot
```

Then human-fills `00_intake/research_input.md` from the WhatsApp + site-scrape intel already captured in this session's STATUS + tasks notes.

---

## Files committed this session

**New:**
- `skills/shared/research_input_template.md`
- `skills/shared/our_hypotheses_template.md`
- `infra/scripts/new-client.sh` (executable)
- `00_META/journal/2026-05-18c_intake-workflow.md` (this file)

**Deleted:**
- `operations/templates/fase_0_intake_form.md`

**Renamed (git mv, history preserved):**
- `pipeline/clients/_template/04_meeting_script/.gitkeep` → `pipeline/clients/_template/04_prep_llamada/.gitkeep`

**Modified:**
- `pipeline/clients/_template/README.md`
- `skills/README.md`
- `calendar.json` (event `e-intake-upload-workflow` title + notes)
- `tasks.json` (close `t-intake-upload-workflow`, refresh `t-trixx-logistics-setup` notes, fix stale `04_meeting_script` reference in `t-migrate-pilotos-to-clients`, bump `updated` timestamp)
- `STATUS.md` (header + Current phase + Done-this-session + Next sequence + Recent activity)
- `00_META/CHANGELOG.md` (new row for 4th-session 2026-05-18)
- `CHECKPOINT.md` (rewritten baton)

---

## For a future auditor

This was the 10th major execution arc since 2026-05-15. Pattern continues unbroken: each arc was an executed-and-audited release; the deliverable surface keeps moving forward. The **production-pipeline ergonomics surface** is now locked — Ricardo can scaffold a new client and start the 4-skill chain with two commands (`bash infra/scripts/new-client.sh ...` + `Analiza <slug>`). The friction at the intake boundary is gone.

Reading order for re-auditing this arc:
1. This journal entry.
2. `STATUS.md` Current state + Done-this-session + top Recent activity entry.
3. `infra/scripts/new-client.sh` (the script itself, ~170 LOC, fully documented).
4. The two templates at `skills/shared/` (read both — the seal-during-research discipline only makes sense when you see both sides).
5. `pipeline/clients/_template/README.md` § "Scaffolding a new client" + "Post-scaffold workflow" (the canonical 7-step workflow).
6. `skills/README.md` § "Per-client invocation" (the trigger-phrase contract).

The session-end commit locks all of this. Next session opens at `t-trixx-logistics-setup`: run the scaffolder, populate the intake files, push state.json into `prospect` phase, write the initial-contact communication, write the awaiting-Skill-01 checkpoint. T-6 days to Monday.
