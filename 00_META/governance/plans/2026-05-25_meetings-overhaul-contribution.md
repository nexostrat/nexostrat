# Meetings Pipeline Overhaul — Nexostrat Contribution

> **Scope:** `/srv/Nexostrat/`
> **Master plan:** [`/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`](../../../../brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md) (governance-traceability reference per ADR-039 anti-decision clause + CLAUDE.md Strict Rule #4 clarification)
> **Author session:** Nexostrat Founder (Claude, desktop)
> **Date:** 2026-05-25
> **Status:** DRAFT
> **Revision note:** First draft authored against stale local state; corrected after pulling 7 commits from origin (a1bff0c..32e493f) that landed brief templates (B5), calendar filter (B7), calibration scaffold (B17), schedule.yaml (B11), ADR-020 supersession memo, and ADR-039 PROPOSED. This version describes actual on-disk state.

---

## 1. Current architectural state

This scope is a **consumer** for the meetings pipeline, not a producer. The hub writes here (action items into `tasks.json`, audit rows, client minutes into `pipeline/clients/<slug>/transcripts/`), and the hub reads from here (`tasks.json` open items + `00_META/templates/` brief templates + `calendar_cache.json` + `schedule.yaml`). The overhaul touches three Nexostrat-owned surfaces: the action-ledger schema, the auto-write audit log destination, and the calibration corpus labelling pass. Brief templates, calendar filter, and schedule registry all shipped during the 2026-05-22 BB Platform audit-action sweep and are live as of `a1bff0c`.

### Built and working

- **`tasks.json`** at `/srv/Nexostrat/tasks.json` — schema `nexostrat-tasks-v1`, top-level object `{$schema, project, updated, tasks: []}`. Each task carries `id, subject, status, priority, due, created, completed, notes`. Live and updated every session.
- **`calendar.json`** at `/srv/Nexostrat/calendar.json` — session-curated deadline list (distinct from the Google-Calendar cache file `calendar_cache.json`, which is not yet seeded).
- **ADR-039 ratified** — Nexostrat runs as tenant 3 in the central Brain Bot Hub at `/srv/brain-hub/`, with separate Telegram token (`NEXOSTRAT_BOT_TOKEN`) and separate per-tenant API key budget envelope. Supersedes ADR-020. (Note: a separate `60038e8 adr: ADR-039 (PROPOSED) — ...` commit landed on origin via the 2026-05-22 merge — appears to be the predecessor draft; the current ratified version dated 2026-05-21 is what governs.)
- **`/srv/Nexostrat/schedule.yaml`** — 4 cron-scheduled brief entries (morning brief `30 7 * * *`, weekly review `0 19 * * 0` TJ, eow pipeline `0 17 * * 5` TJ, inbox sweep `0 18 * * *`), all `tenant: nexostrat`, all `enabled: true`, all pointing at `00_META/templates/*.md`. Per Brain Bot Platform §10 audit B11 schedule-registry pattern. The hub's filesystem watcher picks this file up at boot.
- **`/srv/Nexostrat/00_META/templates/`** — seven brief templates plus comprehensive `README.md`:
  - **4 cron-scheduled:** `morning_brief.md`, `weekly_review.md`, `eow_pipeline.md`, `inbox_sweep.md`
  - **3 meeting-driven (dynamic per `meeting.summary_ready`):** `pre_meeting_brief.md`, `t_20m_agenda.md`, `t_1h_reminder.md`
  - **README** documents the cron schedule + a variable-by-variable data-source table (where `{{last_recap}}` reads from, what `{{pending_tasks}}` filters on, etc.) — JP-editable, plain English. Closes BB Platform §8 audit B5.
  - Also still carries the older `*.tmpl` files for CLAUDE.md/GEMINI.md scaffolding (independent surface; not part of this overhaul).
- **`/srv/Nexostrat/00_META/calendar_filter.md`** — v1 Nexostrat-relevance filter spec for the Google-Calendar → `calendar_cache.json` populator. Three-clause OR rule: summary contains "nexo" (case-insensitive) OR sub-calendar named `Nexostrat` OR attendees include JP's email. Defensive default: missing fields = drop. References the hub-side reference implementation at `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py::nexostrat_filter()` with `FILTER_VERSION` constant. Cache schema's `filter_applied: "nexostrat-v1"` field carries the version stamp for drift detection. Closes BB Platform §9 audit B7.
- **`/srv/Nexostrat/00_META/calibration/`** — corpus scaffold + rubric:
  - `auto_task_extraction.jsonl` exists with a single `_comment` row documenting the schema (the retuner skips this row via the `_comment` guard).
  - `README.md` (3.8 KB) carries the **four-tier confidence rubric** (0.90–1.00 direct quote · 0.70–0.89 paraphrased commitment · 0.40–0.69 inferred · 0.00–0.39 speculation), full NDJSON schema, field meanings, and rater instructions.
  - The ≥50 manually-rated examples are still to be added (P-N3 below).
- **`/srv/Nexostrat/00_META/inbox/2026-05-22_brain_bot_platform_action_items.md`** — OPEN memo from Brain Bot Platform Session B/C audit (recreated 2026-05-24 from the original 2026-05-22 ship). Tracks B14 (ADR-020 supersession), B15 (Strict Rule #4 clarification), B19 (firm-owned Telegram). All three actions have since landed (B14+B15 closed in commit `0293ed8` on 2026-05-21; B19 still open as `t-nexostrat-telegram-account` due 2026-06-15). Memo should be resolved + archived as a janitor pass during Phase 0a.
- **Pipeline client routing surface ready.** `/srv/Nexostrat/pipeline/clients/_template/` exists with the canonical 12-stage subfolder structure plus `archive/ communications/ transcripts/ checkpoint.md state.json README.md`. The `transcripts/` subfolder is the destination Brain Bot Platform §8 B4 names for `client_slug`-routed minutes. One active client folder (`trixx-logistics/`) cloned from the template.
- **Three-persona governance** (Founder + Skills-Master + Client-Owner) with per-persona inboxes. `infra/scripts/nexostrat-memos.py` surfaces unread memos.
- **Audit-finding tasks tracked.** Five ADR-039 B-series follow-ups are open in `tasks.json` with due dates ahead of Stage 1 launch:
  - `t-nexostrat-telegram-account` (B19, due 2026-06-15)
  - `t-weekend-desktop-on-decision` (B16, due 2026-06-15)
  - `t-confidence-calibration-corpus` (B17, due 2026-06-22) — **same work as P-N3 in §3 below**
  - `t-plan-04-description-update` (due 2026-05-28) — orthogonal to this overhaul
  - `t-plan-08-client-meeting-integration` (B18, due 2026-07-15)
- **Backup posture** operational per Plan 01b. R12 pre-overhaul tarball verified 2026-05-25 17:30 on server.

### WIP / surfaced inconsistencies

- **`tasks.json` schema gap for hub auto-writes.** Master plan §2.3 + Brain Bot Platform §8 expect hub-written `extracted_actions[i]` rows to carry provenance metadata: a body text field, `due`, owner/assignee, `confidence`, source meeting id, `auto_added: true`. Current `nexostrat-tasks-v1` carries `subject` (no body-text alias), no `owner` or `assignee`, no `confidence`/`auto_added`/`source_meeting` fields. Also note: the brief templates' README documents reads using a field called **`owner`** (e.g., `status=open AND owner IN [ricardo, jp]`), while BB Platform §8 uses **`assignee`**. The schema-v2 extension needs to pick one and accept the other as alias. Resolved as **prereq P-N1** below.
- **`00_META/audit/` directory does not exist.** Brain Bot Platform §8 names `/srv/Nexostrat/00_META/audit/auto_tasks.log` as the audit log destination for hybrid-by-confidence auto-writes. The directory has never been created. Trivial fix (P-N2).
- **Calibration corpus labelling pass outstanding.** Scaffold + rubric shipped; the actual ≥50 hand-rated rows still need to be authored (P-N3). Master plan §6.6 step 4.7 references this corpus.

### Designed but not implemented

- **`calendar_cache.json`** at `/srv/Nexostrat/calendar_cache.json` does not exist yet. Populated lazily by Claude/Gemini sessions (per BB §9 design pattern); the first session that triggers a Phase 5 step writes it.
- **`pipeline/clients/<slug>/transcripts/` first real write.** Folder exists as part of `_template/` and the trixx-logistics clone; no client meeting has yet been recorded with `client_slug` set. Phase 6 end-to-end test will exercise this path.
- **Bot tenancy itself is not yet live.** Master plan Phase 4 is hub-owned. The only Nexostrat-side change for Phase 4 is the schema extension (P-N1) + audit log destination (P-N2).

### Open inbox memos affecting integration

- `00_META/inbox/2026-05-22_brain_bot_platform_action_items.md` (described above). Action items B14/B15 done; B19 still open as a tracked task. Memo can be archived once B19 closes.
- `00_META/handoff/claude_to_gemini.md` + `gemini_to_claude.md` both in `TEMPLATE` state — no open Gemini handoff.

---

## 2. Alignment check

Comparing master plan §2 (Architecture) and §4 (Tooling) against this scope's ratified state (founding spec amended 2026-05-14 + ADR-039 2026-05-21 + the 2026-05-22 BB-Platform action-item sweep):

- **[ALIGNED] Tenant model.** Master plan §6.6 phase 4 assumes Nexostrat runs as a hub tenant; ADR-039 ratified exactly that on 2026-05-21.
- **[ALIGNED] Per-tenant API key envelope.** Master plan §4 + ADR-039 amendment #2 both require Nexostrat to operate under its own API-key budget cap independent of Personal/Mevillo.
- **[ALIGNED] Hybrid-by-confidence task posture at 0.85.** Master plan §2.3 + Brain Bot Platform §8 audit B6 + Nexostrat acceptance 2026-05-22. Threshold configurable per tenant in hub `routing.yaml`. Calibration rubric in `00_META/calibration/README.md` already operationalizes the rating semantics.
- **[ALIGNED] Two-root client routing.** Master plan §2.8 (internal Nexostrat meetings under `/srv/meetings/nexostrat/`) + BB Platform §8 B4 (client meetings under `/srv/Nexostrat/pipeline/clients/<slug>/transcripts/`) describe distinct destinations that do not collide. The `_template/transcripts/` exists as the receiving end; the `client_slug` event field is the routing key.
- **[ALIGNED] `tasks.json` is the single source of truth.** Master plan §2.4 forbids a `_pending_actions.yaml`; this scope uses `tasks.json` exclusively.
- **[ALIGNED] No-`/srv/brain` rule in Nexostrat artifacts.** This contribution doc references the master plan path in its preamble; per ADR-039 anti-decision clause and the CLAUDE.md Strict Rule #4 2026-05-21 clarification, governance-traceability references for cross-scope plan participation are permitted.
- **[ALIGNED] DeepSeek migration for Nexostrat tenant only.** Master plan §4 swaps the Nexostrat tenant's extractor from OpenAI to DeepSeek V3.1; ADR-039's per-tenant key envelope already isolates this choice. Personal/Mevillo unaffected.
- **[ALIGNED] Calendar cache pattern.** Master plan §6.7 Phase 5 + Brain Bot Platform §9 both specify `/srv/Nexostrat/calendar_cache.json` populated by Claude sessions, with the Nexostrat-relevance filter applied (B7). `00_META/calendar_filter.md` v1 shipped 2026-05-22 with the canonical rule.
- **[ALIGNED] Brief templates as separate files.** Brain Bot Platform §8 audit B5 (render-time, hot-reloadable). `00_META/templates/` shipped 2026-05-22 with all 7 templates + README documenting per-block data sources in plain English.
- **[ALIGNED] schedule.yaml registry pattern.** Brain Bot Platform §10 ("Any Brain scope drops a `schedule.yaml` in its `00_META/` or scope root"). `/srv/Nexostrat/schedule.yaml` shipped 2026-05-22 with 4 entries. Hub's `schedule_registry` reads it at boot.

**No conflicts.** All master plan assumptions consistent with this scope's ratified state as of 2026-05-25. The `tasks.json` schema gap (§1 WIP) is a prereq, not a conflict — both sides agree on the destination; the schema needs an additive extension to carry the new fields.

---

## 3. Prerequisites we MUST complete first

The 2026-05-22 BB-Platform action-item sweep already shipped what would otherwise be P-N4 (templates) and P-N5 (calendar filter) and the calibration scaffold. **Net remaining prereq surface: three.** P-N1 + P-N2 are small (≤ 2h combined) and gate Phase 4 ship. P-N3 is medium effort (labelling time) and has a clean defer option that ships Phase 4 without auto-write.

- **P-N1: `tasks.json` schema v2 — additive extension for hub auto-writes**
  - **What:** Amend the schema at `/srv/Nexostrat/tasks.json` to `nexostrat-tasks-v2`. Add five optional task-object fields (preserve all v1 fields): `owner` (string|null — matches the brief templates' README convention), `assignee` (string|null — accepted as alias of `owner` for BB-Platform §8 interop), `source_meeting` (slug string|null), `auto_added` (bool, default false), `confidence` (float 0.0–1.0|null). Also accept `text` as a synonym of `subject` so the hub can write either. Document schema in `00_META/proposals/2026-05-26_tasks-v2-schema.md` (additive change to an internal data file — no ADR needed).
  - **Why:** The hub's hybrid-by-confidence auto-write path (Brain Bot Platform §8) needs provenance metadata to (a) audit auto-writes against the calibration corpus, (b) let the bi-weekly threshold-retuning pass sample auto-written rows with their original confidence scores, (c) link a task back to its source meeting for `/done #N` flows. The `owner` vs `assignee` alias resolves an internal naming inconsistency (this scope's brief templates use `owner`; BB Platform §8 uses `assignee`).
  - **Effort:** S (≤ 2h).
  - **Depends on:** none.
  - **Done criterion:** `00_META/proposals/2026-05-26_tasks-v2-schema.md` exists; `tasks.json` `$schema` field reads `nexostrat-tasks-v2`; both v1-shaped and v2-shaped tasks coexist; an example auto-extracted task fixture validates.
  - **Defer option:** ship Phase 4 with hub writing into v1 fields (`text → subject`, drop the rest). Cost: B6 audit pass loses per-row confidence + source-meeting trail. Acceptable for Stage 1 if P-N3 ships at v1 quality.

- **P-N2: Create `00_META/audit/` with empty `auto_tasks.log`**
  - **What:** Create `/srv/Nexostrat/00_META/audit/` + empty `auto_tasks.log` (append-only NDJSON — one row per auto-written task: `{ts, source_meeting, extracted_text, score, model, task_id_written}`). Add `00_META/audit/README.md` documenting the row schema and stating the file is hub-owned (written via ScopedFS) but Nexostrat-readable for audit passes.
  - **Why:** Brain Bot Platform §8 names this exact path. The hub will fail to write the first auto-write if the directory is missing.
  - **Effort:** S (≤ 30 min). Fold into the same commit as P-N1.
  - **Depends on:** none.
  - **Done criterion:** `00_META/audit/auto_tasks.log` exists (empty, committed); `00_META/audit/README.md` documents the row schema.
  - **Defer option:** none reasonable (trivial).

- **P-N3: Hand-rate ≥ 50 examples in `00_META/calibration/auto_task_extraction.jsonl`**
  - **What:** Append ≥ 50 NDJSON rows to `/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl` per the existing schema and rubric (`README.md` already locks both). Source material: four existing meetings under `/srv/meetings/nexostrat/` (audit H3 PASS) yielding ~20 candidate actions, plus ~30 synthetic edge cases covering: ambiguous "we should do X someday" rows, multi-assignee phrasings, dates given only in relative form, JP-language quirks, and the four rubric tiers in balanced ratios. Add a `2026-05-XX_initial-corpus-report.md` reporting precision/recall at the proposed 0.85 threshold against the labelled set.
  - **Why:** Master plan §6.6 step 4.7 explicitly says: "test against the existing calibration corpus." Without ≥50 rated rows, the DeepSeek-vs-OpenAI A/B for the Nexostrat tenant cannot be validated, and the bi-weekly threshold-retuning pass has no signal.
  - **Effort:** M (≤ 1d of labelling). This is identical to the work tracked as `t-confidence-calibration-corpus` (B17, due 2026-06-22) — should be treated as the same line item, not double-tracked.
  - **Depends on:** P-N1 (rows reference owner/source_meeting/auto_added fields the v2 schema introduces).
  - **Done criterion:** ≥ 50 valid NDJSON rows in the corpus file; each row carries `model_score`, `ground_truth_score`, `ground_truth_should_write`, `rater`, `rated_at`; the initial-corpus report file exists with precision/recall numbers + recommended threshold.
  - **Defer option:** **ship Phase 4 with hybrid-by-confidence DISABLED.** All extracted actions route through Telegram `[✅ Add] [❌ Skip]` confirmation regardless of confidence. Cost: lose the "auto-write at 0.85" UX win for Stage 1 launch (~6 weeks of manual confirmation friction); Phase 4 step 4.7 still ships but is validated by spot-check rather than corpus replay. Reasonable fallback if labelling slips past 2026-06-22.

**Housekeeping (not a prereq, but trivially foldable into Phase 0a):**

- Resolve + archive `00_META/inbox/2026-05-22_brain_bot_platform_action_items.md` once `t-nexostrat-telegram-account` (B19) closes. Items B14/B15 are already done; the memo is stale on those two items.

---

## 4. What this scope adds for the overhaul

Concrete deliverables mapped to master plan §6 phase numbers:

- **Phase 0a (per-scope prereqs):** P-N1 + P-N2 + P-N3 land here. All three are Nexostrat-scope-only.
- **Phase 4 (hub-side handling):** schema extension (P-N1) lands here; audit log destination (P-N2) lands here. No other Nexostrat-side change for Phase 4 — the hub does the writes via ScopedFS, the Telegram approval flows, the `/done #N` task updates. This scope is purely the **target filesystem** during Phase 4.
- **Phase 5 (calendar integration + pre-meeting briefs):** **Brief templates + calendar filter already shipped** (commits `b3bae45` + `32e493f`, 2026-05-22). `schedule.yaml` for cron-fired non-meeting briefs also live. The first session that triggers a Phase 5 step will write `calendar_cache.json` via MCP per the existing `calendar_filter.md` v1 rule.
- **Phase 6 (end-to-end test):** this scope hosts the test meeting's routing target — either `pipeline/clients/<test_slug>/transcripts/` (client meeting flow) or `tasks.json` writes (internal meeting). No code change in this scope for Phase 6.

Phase-level summary: **3 prereqs in Phase 0a (P-N1/P-N2/P-N3), Phases 4 + 5 + 6 are pure consumers of this scope's assets, no producer-side work.**

---

## 5. What this scope needs from root or other scopes

- **From Brain Hub session (`/srv/brain-hub/`):**
  - **Tenant config in `routing.yaml`** for the Nexostrat tenant including: `bot_token_env: NEXOSTRAT_BOT_TOKEN`, `api_key_env: DEEPSEEK_API_KEY_NEXOSTRAT` (post-migration) + base URL, `confidence_threshold: 0.85`, ScopedFS read/write enumeration for `/srv/Nexostrat/tasks.json`, `/srv/Nexostrat/00_META/audit/auto_tasks.log`, `/srv/Nexostrat/calendar_cache.json`, `/srv/Nexostrat/00_META/templates/`, `/srv/Nexostrat/pipeline/clients/`, and `/srv/Nexostrat/schedule.yaml`.
  - **DeepSeek API key procurement** (`DEEPSEEK_API_KEY_NEXOSTRAT`) before Phase 4 step 4.7 ships. Audit R10 was WAIVED for Phase 0–3 readiness; hard-gated on Phase 4.7. Nexostrat's budget envelope (initial $20/month per ADR-039) covers spend.
  - **`/srv/brain-hub/hub/google/calendar_filter_nexostrat.py`** reference implementation must exist and export `nexostrat_filter(event, jp_email) -> bool` + `FILTER_VERSION = "nexostrat-v1"` matching the heading of `00_META/calendar_filter.md`. Tests at `/srv/brain-hub/tests/test_nexostrat_calendar_filter.py`. The Claude session populating `calendar_cache.json` imports this filter directly rather than re-implementing the rule.
  - **Status-change suggestion handler** (Phase 4 step 4.4) — consumes `status_change_suggestions[]` from the event payload, DMs Ricardo with `[✅ Mark done] [❌ Keep open] [⏸ Defer]`, mutates the matching `tasks.json` row on ✅. Hub-side concern; this scope is the target.
  - **Brief-render plugin (`hub.plugins.meetings.brief`)** must implement the variable substitutions documented in `00_META/templates/README.md` — `{{last_recap}}`, `{{pending_tasks}}`, `{{chat_items}}`, `{{attendance_yn}}`, `{{open_memos}}`, `{{pipeline_state}}`, `{{cache_age_warning}}`, `{{top_tasks_per_founder}}`, `{{todays_meetings}}`, `{{stale_memos}}`, `{{quick_recap_one_line}}`, `{{agenda_topics}}`, `{{week_start}}`, `{{week_body}}`, `{{per_client_one_liner}}`, `{{date}}`. Source rules are documented in the README; renderer is variable-substitution-only (no logic in the templates).

- **From Meetings Curator (`/srv/meetings/`):**
  - **`client_slug` field set at recording time** (per master plan §2.1 Q3). For Nexostrat-scope client meetings, the producer emits `client_slug: <slug>` so the hub routes minutes to `/srv/Nexostrat/pipeline/clients/<slug>/transcripts/` per BB Platform §8 B4.
  - **`extracted_actions[].scope` correctness** — producer must stamp the scope on every action item it extracts (master plan §2.3 step 1 + §2.4 cross-scope handling). Cross-scope items (a Nexostrat meeting that creates an AttenBot todo) route elsewhere via the scope field.

- **From root (Brain Architect):**
  - **Phase 0a sequencing.** Suggested order: P-N1 + P-N2 as one co-commit (small, mutually supportive), then P-N3 labelling as a parallel labelling pass with a 2026-06-22 deadline matching the existing B17 task.
  - **Deduplication:** P-N3 in this doc is the same line item as `t-confidence-calibration-corpus` in this scope's `tasks.json`. Phase 0a should treat them as a single deliverable, not two.
  - **Deployment doc step text** for the three prereqs (per master plan §6.2 pattern — append "open Claude in /srv/Nexostrat/, paste this prompt" steps to the deployment doc §2).

---

## 6. Reviewer / executing persona

- **Author:** Nexostrat Founder (this session).
- **Reviewer:** Brain Architect (root) for cross-scope integration; Brain Hub session for tenant-config + ScopedFS scope enumeration + filter reference-impl alignment.
- **Executor (Phase 0a prereqs):** Nexostrat Founder session, working in `/srv/Nexostrat/`. None of the three prereqs require Skills-Master or Client-Owner involvement.

---

## 7. Notes for root

- **Net prereq surface shrunk significantly from first draft.** The 2026-05-22 BB-Platform action-item sweep (7 commits, merged via `a1bff0c`) already landed brief templates, calendar filter, calibration scaffold/rubric, schedule.yaml, and ADR-020 supersession. The first draft of this doc was authored against stale local state and listed five prereqs (P-N1..P-N5) — three of them turned out to be already-done. Corrected on push.
- **`t-confidence-calibration-corpus` and P-N3 are the same line item.** Don't double-track. Phase 0a write-up should alias P-N3 to that existing task ID rather than create a parallel one.
- **`owner` vs `assignee` naming mismatch.** Inside this scope, the brief templates' README documents reads using `owner`. BB Platform §8 uses `assignee`. P-N1 lands `owner` as the canonical field and accepts `assignee` as alias. Heads-up to root in case the same mismatch shows up in other scopes.
- **`60038e8 adr: ADR-039 (PROPOSED)`** commit on origin appears to be an older draft of the ADR that landed via the merge sweep. The currently-ratified ADR-039 (dated 2026-05-21, status Accepted) is the governing version. May warrant a tidy-up commit but is not blocking.
- **No collision with current session 14 work.** Session 14's write surface (intro V3 production under `operations/marketing/website-intro/`) is fully orthogonal. Phase 0a can land immediately.
- **No conflict on the no-`/srv/brain` rule.** Per ADR-039 anti-decision clause and the Strict Rule #4 clarification, governance-traceability references are permitted.
- **Stage 1 launch window (2026-06-30 → 2026-07-15)** comfortably accommodates Phase 0a: P-N1+P-N2 land in ≤ ½ day; P-N3 labelling fits the existing 2026-06-22 deadline.

---

**End of contribution doc.**
