# Nexostrat — Master Plan Index

> **Status:** ROADMAP — implementation plans derive from this index
> **Date:** 2026-05-13
> **Source spec:** [`../proposals/2026-05-13_nexostrat-system-design.md`](../proposals/2026-05-13_nexostrat-system-design.md)
> **Plain partner:** [`README-explicado.md`](README-explicado.md)

This is the implementation roadmap from founding spec to Stage 1 live. **Ten plans in dependency order.** Each plan produces working, testable software on its own. Plans 02-10 are written **just-in-time** using the `superpowers:writing-plans` skill when their turn comes. Plan 01 is fully detailed and ready to execute.

The reason for just-in-time writing: tool versions, learned lessons, and small adjustments after each plan would silently invalidate a fully pre-written plan. The architectural decisions are already locked in the spec; only the execution details vary.

---

## Status table

| # | Plan | Status | File | Effort | Started | Done |
|---|---|---|---|---|---|---|
| 01 | Repository Foundation | **READY** | [`2026-05-13_plan-01-repository-foundation.md`](2026-05-13_plan-01-repository-foundation.md) | ~1 week | — | — |
| 02 | Documentation System | DRAFT-PENDING | — | ~3 days | — | — |
| 03 | events.jsonl + Python Agent Framework | DRAFT-PENDING | — | ~1 week | — | — |
| 04 | Telegram Bot Core + Unified Inbox | DRAFT-PENDING | — | ~1 week | — | — |
| 05 | Skill 1 End-to-End (template for 2-5) | DRAFT-PENDING | — | ~1 week | — | — |
| 06 | Skills 2-5 | DRAFT-PENDING | — | ~2 weeks | — | — |
| 07 | Per-Client Chain + Pipeline Orchestrator | DRAFT-PENDING | — | ~1 week | — | — |
| 08 | Meeting Pipeline | DRAFT-PENDING | — | ~1.5 weeks | — | — |
| 09 | Ambient Chat Extraction | DRAFT-PENDING | — | ~3 days | — | — |
| 10 | Observability + Go-Live | DRAFT-PENDING | — | ~3 days | — | — |

Status values:
- `READY` — drafted in full, awaiting execution
- `IN PROGRESS` — partially executed; CHECKPOINT.md has next-task pointer
- `DONE` — all tasks complete; tagged in git
- `DRAFT-PENDING` — header here, full plan to be written via `writing-plans` skill at execution time

---

## Dependency graph

```
Plan 01 (Foundation)
  │
  ├──► Plan 02 (Docs)               ─┐
  │                                   │
  ├──► Plan 03 (Events + Agents)     ─┤
  │       │                           │  All four can run partly in parallel
  │       └──► Plan 04 (Bot + Inbox) ─┤  (Plans 02, 03, 04 only need Plan 01)
  │                                   │
  └──► (Plan 02, 03, 04 in some mix) ─┘
                       │
                       └──► Plan 05 (Skill 1 e2e)
                                │
                                ├──► Plan 06 (Skills 2-5; can fan out)
                                │       │
                                │       └──► Plan 07 (Client chain + orchestrator)
                                │                │
                                │                ├──► Plan 08 (Meeting pipeline)
                                │                │
                                │                └──► Plan 09 (Chat extraction)
                                │                         │
                                │                         └──► Plan 10 (Go-live)
                                │
                                └──► First income-eligible Diagnóstico after Plan 07.
                                     First client meetings after Plan 08.
                                     Stage 1 launch after Plan 10.

Total calendar time for one operator (Ricardo + Claude): ~7-9 weeks.
```

---

## Per-plan headers

Each plan below has: **Goal · Deliverables · Dependencies · Success criteria · Spec references**.

When it's time to draft Plan N in detail, future Claude reads (a) the spec, (b) the spec sections referenced below, (c) the master index, (d) any earlier plan files that are DONE, and (e) the CHECKPOINT.md baton. Then invokes `writing-plans` skill against Plan N's scope.

---

### Plan 01 — Repository Foundation

**Goal:** Scaffold the 3-bucket repository, lock identities (age keys), stand up the backup ladder, and create persona files so all subsequent plans have a stable foundation.

**Deliverables:**
- 3-bucket folder structure at `/srv/Nexostrat/` per spec Section 2
- age keypair for Ricardo + recipients.txt + vault skeleton
- `secrets.env.age` (encrypted) + `run-with-secrets.sh` wrapper
- Gitea origin (already running) + GitHub private mirror via post-receive hook
- Warm-standby provisioning + nightly rsync script
- Root `CLAUDE.md` + `GEMINI.md` (Founder)
- `skills/CLAUDE.md` + `skills/GEMINI.md` (Skills-Master)
- `pipeline/CLAUDE.md` + `pipeline/GEMINI.md` (Client-Owner)
- Canonical shared stanzas at `00_META/shared/*.md`
- Per-machine YAML profiles at `infra/machines/*.yaml`
- `bootstrap-machine.sh` (working, idempotent)
- Pre-commit secret-scan + file-pattern-block hooks (basic versions)
- Smoke test that returns green at end

**Dependencies:** None. This is the entry point.

**Success criteria:**
- `infra/scripts/smoke-test.sh` returns green (all checks pass)
- A simulated HP-down → warm-standby failover documented and dry-run completes
- A test commit on any clone mirrors to GitHub within seconds (verified)
- A planted plaintext secret in a staged file is blocked by pre-commit
- A new clone on a fresh machine runs `bootstrap-machine.sh ricardo-travel` and completes successfully
- Repo tagged `v0.1-foundation`

**Spec references:** §1 (Topology), §2 (Repository Structure), §3 (Foundation Layer), §4.1-§4.5 (Personas + ADRs + Partnership), ADRs 002, 003, 004, 005, 006, 008, 011, 021, 023, 033.

**File:** [`2026-05-13_plan-01-repository-foundation.md`](2026-05-13_plan-01-repository-foundation.md) (FULLY DETAILED, ready to execute)

---

### Plan 02 — Documentation System

**Goal:** Set up the `docs/` Diátaxis structure, the paired-files drift hook, the auto-generated reference docs, and write the first ~10 essential how-tos so Stage 1 has operational docs both Ricardo and JP can read.

**Deliverables:**
- `docs/{tutorials,how-to,reference,explanation,runbooks}/` populated with starter files
- `docs/README.md` + `README-explicado.md` (entry point)
- Pre-commit hook `pre-commit-docs-pair.sh` (refuses unpaired modifications in tier-1 folders)
- Weekly drift audit cron + Python script
- Auto-generators: `gen_telegram_ref.py`, `gen_skill_catalog.py`, `gen_event_taxonomy.py`, `gen_adr_index.py`, `gen_machine_matrix.py`
- All 15 new ADRs (021-035) drafted as `00_GOVERNANCE/adr/ADR-NNN-<slug>.md` with `-explicado.md` partners
- Top ~10 how-tos written: onboard client, run skill manual/api, capture meeting, use Telegram bot, key rotation, machine bootstrap, deploy, send proposal, render Aurora deliverable, decrypt vault file
- All paired `-explicado.md` partners
- `docs/reference/{stack_inventory,machine_matrix,folder_layout,naming_conventions,event_taxonomy,glossary}.md` (some auto-generated)
- Print-to-Aurora-PDF script `print-doc.sh` working

**Dependencies:** Plan 01 (repo scaffold + persona files must exist).

**Success criteria:**
- A test that modifies a tier-1 `.md` without its `-explicado.md` partner is blocked
- All auto-generators produce identical output to what's committed (no drift)
- Running `infra/scripts/print-doc.sh docs/how-to/01_onboard_new_client-explicado.md` produces an Aurora-branded PDF
- All 15 new ADRs present, indexed in `DECISIONS.md`, linked from spec sections that cite them
- JP can read the 10 `-explicado.md` how-tos cold and follow them

**Spec references:** §4.6 (Two-tier docs hook), §4.7 (Cross-folder memos), §4.10 (CHECKPOINT), §4.11 (Unified inbox — docs only; bot in Plan 04), the docs system section. ADRs 014, 015, 025, 031.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 03 — events.jsonl Spine + Python Agent Framework

**Goal:** Build the event-driven backbone — `events.jsonl` schemas, atomic append, the agent dispatcher, the agent template, the event-router daemon, systemd timer/service infrastructure.

**Deliverables:**
- `infra/events/events.jsonl` (empty, schema-validated on append)
- `infra/events/schemas/*.json` — JSON schemas for ~80 event types in spec §9.2
- `infra/agents/_lib/{events,secrets,telegram,notion,calendar,models,state,docs_gen,tz}.py`
- `infra/agents/dispatch.py` (CLI entry point: `nexostrat run <agent>`)
- `infra/agents/event_router.py` (long-running daemon tailing events.jsonl, dispatching per routing.yaml)
- Agent template at `infra/agents/_template_agent/` (manifest.json, run.py, README.md, tests/)
- `infra/systemd/` units for: event-router daemon, warm-standby rsync (nightly), backup verification (weekly), daily brief (07:00)
- `infra/scripts/install-systemd-units.sh` (symlinks + enables + tests reload)
- pytest test suite with mocks for Anthropic/Gemini/Grok/Notion/Calendar/Telegram
- `tests/integration/test_event_emission.py` proves atomic-append + schema validation

**Dependencies:** Plan 01 (folder structure + secrets workflow).

**Success criteria:**
- `nexostrat run --help` lists all registered agents
- An event emitted via `infra/agents/_lib/events.emit(...)` lands in `events.jsonl` with correct schema validation
- `infra/agents/event_router.py` running picks up a synthetic event and routes per `routing.yaml`
- systemd units installed and `systemctl status nexostrat-event-router` shows active
- All unit tests pass (≥80% coverage)
- Reading 1 million synthetic events from a rotated `events-YYYY-MM.jsonl.zst` completes in <5 sec

**Spec references:** §5 (Stack), §9.1-§9.3, §9.7 (Wake-on-LAN), §9.8 (chains), §10.1 (testing). ADRs 013, 017 (amended), 029.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 04 — Telegram Bot Core + Unified Inbox

**Goal:** Build the bot service with plugin framework, capture commands, the unified inbox primitive, encrypted chat logger, per-user TZ-aware scheduling, and Telegram surfaces for state inspection.

**Deliverables:**
- `infra/telegram/bot/` complete Python service (Docker container)
- `infra/telegram/plugins/` with all Stage 1 commands: `/note`, `/idea`, `/question`, `/decision`, `/expense`, `/client`, `/meeting` (basic), `/intake`, `/status`, `/pipeline`, `/help`, `/whoami`, `/inbox`, `/resolve`, `/defer`, `/promote`, `/prefs`, `/quiet`, `/dnd`, `/wakeup`, `/whats-queued`, `/handoff`, `/manual`, `/emergency`
- `infra/telegram/users/<userid>.yaml` files for Ricardo + JP
- `infra/telegram/delivery_queue/<userid>.jsonl` per-user queue
- `infra/agents/delivery_flush.py` + systemd timer (5-min flush)
- `infra/telegram/routing.yaml` (event → recipients per tier)
- `infra/telegram/allowlist.yaml` (chat_id allowlist)
- `infra/telegram/templates/{es,en}/*.j2` Jinja2 message templates
- Encrypted chat logger writing to `infra/telegram/chat_log/{group,dm-ricardo,dm-jp}/YYYY-MM-DD.jsonl.age`
- `<scope>/00_META/inbox/` populated and functional for all 3 personas
- Bot reloads on plugin add/edit without restart
- pytest tests + integration test that exercises capture → inbox → resolve

**Dependencies:** Plan 01 (foundation), Plan 03 (events + agent framework).

**Success criteria:**
- `/note pipeline test message` in group chat creates a file at `pipeline/00_META/inbox/YYYY-MM-DD_HHMM_telegram_<slug>.md` with correct frontmatter
- `/inbox pipeline` returns the open items in that scope
- `/resolve <id> "test reply"` archives the item with attribution
- A tier-2 alert at 22:00 Ricardo's local time queues (not delivered) and flushes at 07:00
- `/prefs set tier_2 quiet 22-07` updates `users/<ricardo_id>.yaml` and commits
- An unauthorized chat_id sends a message → silent drop + event `hook.blocked` emitted
- Tests pass; coverage ≥80%

**Spec references:** §4.11 (Unified inbox), §5 (Stack — bot service), §9.4-§9.6 (bot architecture, plugin framework, AI escalation), §10.4 (alerting tiers). ADRs 019, 020, 030, 032.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 05 — Skill 1 End-to-End (Template for 2-5)

**Goal:** Wire the existing company-analyst skill into the production-ready shape — both Mode A (manual) and Mode B (API parallel-then-judge) running end-to-end on the Bodai benchmark fixture. This plan establishes the per-skill pattern that Plans 06 cloned.

**Deliverables:**
- Skill 1 fully migrated to `skills/01_company_analyst/` per ADR-012 template
- `SKILL.md`, `prompts/v1.md`, `scripts/`, `references/`, `assets/`, `tests/`
- Bodai benchmark fixture: `tests/benchmark_input.md` + `tests/benchmark_expected.md`
- Bodai baseline score recorded; `skills/shared/scoring.py` implementing the formula
- `skills/shared/research_input_template.md`, `our_hypotheses_template.md`, `judge_prompt.md`, `anti_hallucination.md`
- `infra/agents/skill_1_company_analyst/`: `run_manual.py`, `run_api.py`, `manifest.json`, `tests/`
- `infra/agents/judge/run.py` (Claude-as-Judge synthesizer)
- `infra/runbooks/manual/skill_1_manual.md` (Mode A runbook Claude Code follows)
- Aurora pandoc template at `operations/templates/aurora.docx` + `pandoc-aurora.yaml`
- `infra/scripts/render-aurora.sh` (md → Aurora-branded DOCX + PDF)
- Pre-commit hook validating anti-hallucination marker block in all skill prompts
- pytest tests including `test_intake_two_file_isolation.py` proving `our_hypotheses.md` never reaches research stage
- A complete Bodai test run in both Mode A and Mode B saved to `pipeline/clients/bodai/01_company_analysis/runs/`

**Dependencies:** Plans 01, 03, 04.

**Success criteria:**
- `nexostrat run skill_1 --client bodai --mode=manual` walks Claude Code through Mode A start to finish; final_report.md produced
- `nexostrat run skill_1 --client bodai --mode=api` produces three raw_outputs + judge synthesis + Aurora DOCX/PDF, <6 min, <$0.30
- `comparison.md` auto-generated showing diff between Mode A and Mode B runs
- Bodai benchmark score ≥ 7/10
- Regression test: editing the prompt and re-running shows score delta computed correctly; commit blocked if factual-accuracy drops
- `test_intake_two_file_isolation.py` PASSES (sealed file never touched during research stage)

**Spec references:** §6 (Skills, Intake, Multi-Model — all subsections), §7 (Per-client chain — at least Bodai), §10.1 (testing — benchmark + integration), ADRs 010, 012, 022, 026, 027, 033.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 06 — Skills 2-5 (Industry, Competitor, Meeting Script, Opportunity Report)

**Goal:** Apply the Plan-05 pattern to Skills 2, 3, 4, 5 — each scaffolded, prompted to v1, benchmarked against Bodai, and runnable in both modes.

**Deliverables:** Four parallel implementations of the same shape as Skill 1:
- `skills/02_industry_analyst/` with prompts/v1.md, benchmarks, both modes
- `skills/03_competitor_analyst/` with prompts/v1.md, benchmarks, both modes
- `skills/04_meeting_script/` with prompts/v1.md, benchmarks, both modes (**PRIVATE — never produces a client-facing PDF**)
- `skills/05_opportunity_report/` with prompts/v1.md, benchmarks, both modes (**THE Diagnóstico deliverable**)
- Each in `infra/agents/skill_N_<name>/`
- Each with its `infra/runbooks/manual/skill_N_manual.md`
- Bodai benchmark output recorded for each at v1
- Integration test: full 5-skill chain runs on Bodai in Mode B end-to-end, <30 min, <$1.50

**Dependencies:** Plan 05 (the pattern + judge + Aurora render must work).

**Success criteria:**
- Each skill scores ≥7/10 on Bodai benchmark at v1
- Full Diagnóstico (Skills 1→2→3→4→5) chains correctly with each skill reading prior outputs
- Skill 4 output never has `report.docx`/`report.pdf` (private markdown only)
- Skill 5 output passes the "client can explain it to a friend in 30 sec" test (lay-language check)
- All skill prompts contain the anti-hallucination marker block

**Spec references:** §6 (Plan Maestro skill specs), ADRs 012, 022, 026.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 07 — Per-Client Production Chain + Pipeline Orchestrator

**Goal:** Build the 12-station per-client structure, `state.json` schema + transition validators, intake 2-file workflow with `/intake` plugin, the pipeline orchestrator chaining Skills 1-5 with `/go` gates, and scaffold the first pilot client (Alfa Bitcoin).

**Deliverables:**
- `pipeline/clients/_template/` complete (all 12 stations + 3 cross-cutting folders + state.json template)
- `infra/scripts/new-client.sh` working (`/new-client <slug> "<name>" <country> "<sector>"` in Telegram fires it)
- `state.json` schema + Python validator + transition state machine at `infra/agents/_lib/state.py`
- `infra/agents/pipeline_orchestrator/{orchestrator.py, state_machine.py, tests/}` chaining Skills 1-5
- `/intake <slug>` Telegram plugin walks user through both files
- `/advance`, `/regress`, `/set-phase`, `/block`, `/unblock` plugins
- `/go`, `/stop`, `/note`, `/ask`, `/switch`, `/rerun` gate plugins
- `/new-client` plugin
- `alfa-bitcoin/` scaffolded with state.json = `prospect`
- bodai/ scaffolded (already done in Plan 05) and ready to advance through phases
- pytest tests for every transition (legal + illegal)

**Dependencies:** Plans 01, 03, 04, 05, 06.

**Success criteria:**
- `/new-client alfa-bitcoin "Alfa Bitcoin SL" ES "fintech/bitcoin"` creates the client folder with state.json
- `/intake bodai` (already in `exploring`) updates the intake files and emits `intake.completed` event
- Orchestrator picks up the event and starts Skills 1-3 in parallel via Mode B
- `/go bodai-skills-1-4` advances to Skill 5
- `/go bodai-diagnostico` advances to `diagnostico_delivered`
- Illegal transition (e.g., `prospect` → `cliente_firmado` directly) refused with clear error

**Spec references:** §6.4 (intake), §7 (per-client chain), §9.5 (plugin framework), ADRs 010, 015, 022, 027.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 08 — Meeting Pipeline

**Goal:** Build the dual capture (Notion AI canonical + Jitsi/Whisper shadow for internal; single canonical for client), parity diff job, AI extraction (actions/decisions/dates/questions), morning brief + T-15 reminder + confirmation, Google Calendar integration, meeting lifecycle protocol (start/pause/resume/end/recover).

**Deliverables:**
- `/meeting {start,pause,resume,end,recover,note,decision,action,brief,override}` Telegram plugins
- `/agenda`, `/actions`, `/decisions`, `/confirm`, `/decline`, `/reschedule` plugins
- `infra/shadow/jitsi/docker-compose.yml` + working room
- `infra/shadow/nextcloud/docker-compose.yml` + working
- Whisper.cpp container with Spanish model + transcript queue watcher
- Notion polling agent at `infra/agents/meeting/transcription_watcher.py`
- Parity diff agent at `infra/agents/meeting/parity_diff.py` (Ollama-based)
- Extraction agent at `infra/agents/meeting/extractor.py`
- Brief jobs: `brief_morning.py` (07:00 per user TZ), `brief_t15.py`
- Google Calendar integration via `infra/agents/_lib/calendar.py`
- `00_GOVERNANCE/meeting-protocol.md` (canonical lifecycle) + `-explicado.md`
- pytest tests including end-to-end fixture (audio → transcript → extraction → calendar)
- Per-decision file format implemented; auto-create in `00_PARTNERSHIP/decisions/`

**Dependencies:** Plans 01, 03, 04, 07.

**Success criteria:**
- A 5-min sample audio drops into the queue → Whisper transcribes → extraction produces ≥1 action item → tasks.json updated → Telegram digest posted
- Morning brief at 07:00 in Ricardo's TZ (Tijuana) fires AND at 07:00 in JP's TZ (Bogotá) fires; both with correct content
- A `/meeting pause` followed by `/meeting resume` within 30 min keeps the same meeting_id and joined transcript
- `/meeting recover <id>` triggered on a meeting with no transcript walks human through manual fallback
- Parity score >0.7 on first 3 internal meetings recorded both ways

**Spec references:** §8 all subsections, §9.3 (workflows), §10.4 (alerting), ADRs 024, 030, 035.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 09 — Ambient Chat Extraction

**Goal:** Capture every Telegram group/DM message (encrypted), run Ollama-based extraction during office hours, confirmation loop for found tasks/dates/decisions, wake-on-LAN integration for the desktop.

**Deliverables:**
- Encrypted chat logger writing daily JSONL files to `infra/telegram/chat_log/{group,dm-ricardo,dm-jp}/YYYY-MM-DD.jsonl.age`
- `infra/agents/chat_extractor/extract_loop.py` (Ollama via Qwen 2.5 14B Q4)
- Sensitive-content filter at `infra/telegram/bot/middleware/sensitive_filter.py`
- Confirmation plugins: `/confirm-extract`, `/reject-extract`, `/edit-extract`
- `/chat search`, `/chat from`, `/chat extractions pending`, `/chat last`, `/chat tasks-from-chat` inspection commands
- `infra/agents/infrastructure/desktop_wake.py` (wake-on-LAN via etherwake)
- systemd timer `nexostrat-chat-extractor.timer` (every 4h office hours)
- Auto-confirm after 24h with low priority + provenance attribution
- Reaction marks on Telegram (📌 confirmed, 🚫 rejected)
- pytest tests including a 100-message synthetic chat → expected extractions

**Dependencies:** Plans 01, 03, 04 (bot must be running with chat logger).

**Success criteria:**
- A test message "Recordemos mandarle a Bodai el v2 deck antes del miércoles" produces a confirmation prompt within 4h
- `/confirm-extract <id>` creates the task with correct assignee + due date
- A message containing a fake API key pattern is filtered (not extracted; alert emitted)
- Desktop suspended at 20:00; a queued extraction job at 21:00 sends WoL; desktop wakes within 60s; job processes; desktop returns to suspend
- All chat logs unreadable without age private key (verify by attempting `cat *.age`)

**Spec references:** §8.10 (ambient chat capture), §9.7 (Wake-on-LAN), ADRs 028, 034.

**File:** *(to be written via writing-plans when execution starts)*

---

### Plan 10 — Observability + Go-Live

**Goal:** Wire all the Telegram inspection surfaces (`/status`, `/pipeline`, `/infra`, `/events`, `/metrics`, `/errors`), write the daily brief job, write all failure-mode runbooks, run the Stage 1 go-live checklist to green, tag v1.0, emit `deploy.released`.

**Deliverables:**
- All inspection plugins functional and rate-limited
- `infra/agents/infrastructure/daily_brief.py` running at 07:00 with bundled digest
- All failure-mode runbooks under `docs/runbooks/*.md` + partners (30+ files)
- All recovery scripts under `infra/recovery/*.sh` (hp_down_failover, rotate_age_key, rotate_api_key, restore_from_mirror, etc.)
- `infra/scripts/smoke-test.sh` covering all Stage 1 services
- Stage 1 go-live checklist (spec §10.6) executed; every box green
- v1.0 git tag created
- `deploy.released` event emitted with version metadata
- Final journal entry summarizing readiness

**Dependencies:** Plans 01-09 all DONE.

**Success criteria:**
- Every checklist item in spec §10.6 is satisfied
- `/status` returns truthful health summary
- Daily brief at 07:00 has run for 3 consecutive days successfully
- Alfa Bitcoin (first pilot) is in `intake` phase with both intake files complete
- Bodai (benchmark) is in `diagnostico_delivered` state with both modes runs visible
- `git tag v1.0` exists; `deploy.released` event in `events.jsonl`

**Spec references:** §10 (all subsections), the Stage 1 go-live checklist.

**File:** *(to be written via writing-plans when execution starts)*

---

## Execution model

Each plan, when its turn comes, executes via one of two patterns:

### Subagent-driven (recommended)

Use the `superpowers:subagent-driven-development` skill. Each task in the plan becomes a fresh subagent dispatch:

```
Plan task 1 → spawn subagent → subagent does the work + commits → main agent reviews → next
Plan task 2 → ... (fresh subagent, no contaminated context) ...
```

Fast iteration, clean context per task, main agent maintains the bird's-eye view.

### Inline execution

Use the `superpowers:executing-plans` skill. Tasks run in the same session as the planning context, batched with checkpoints. Use when you want to be deeper in the loop with the agent.

---

## What this index does NOT replace

- The **spec** (`../proposals/2026-05-13_nexostrat-system-design.md`) is the source of truth for architectural decisions. This index is the source of truth for **sequencing and dependencies**.
- The **CHECKPOINT.md** files are the source of truth for **immediate next action** during an in-flight plan.
- The **journal entries** are the source of truth for **what actually happened** during each session.

Each layer is intentionally redundant with the others — different audiences, different lookup paths, lower probability of any single layer becoming the bottleneck.

---

## Change log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (Opus 4.7, with Ricardo at root) | Master plan index created. 10 plans drafted at header-level; Plan 01 fully detailed. Plans 02-10 status `DRAFT-PENDING` — to be written via `writing-plans` skill at execution time. |
