# Meetings Pipeline Overhaul — Nexostrat Contribution

> **Scope:** `/srv/Nexostrat/`
> **Master plan:** [`/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`](../../../../brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md) (governance-traceability reference per ADR-039 anti-decision clause + CLAUDE.md Strict Rule #4 clarification)
> **Author session:** Nexostrat Founder (Claude, desktop)
> **Date:** 2026-05-25
> **Status:** DRAFT

---

## 1. Current architectural state

This scope is a **consumer** for the meetings pipeline, not a producer. The hub writes here (action items into `tasks.json`, audit rows, client minutes into `pipeline/clients/<slug>/transcripts/`), and the hub reads from here (`tasks.json` open items + `00_META/templates/` brief templates + `calendar_cache.json`). The overhaul touches three Nexostrat-owned surfaces: the action-ledger schema, the brief-template surface, and the confidence-calibration corpus. None of the actual hub or pipeline code lives in this scope.

### Built and working

- **`tasks.json`** at `/srv/Nexostrat/tasks.json` — schema `nexostrat-tasks-v1`, top-level object `{$schema, project, updated, tasks: []}`. Each task carries `id, subject, status, priority, due, created, completed, notes`. Live and updated every session (last write `2026-05-25T15:30:00-07:00` per session 14).
- **`calendar.json`** at `/srv/Nexostrat/calendar.json` — session-curated deadline list (not the Google-Calendar cache; see "Designed but not implemented" for `calendar_cache.json`).
- **ADR-039 ratified** — Nexostrat runs as tenant 3 in the central Brain Bot Hub at `/srv/brain-hub/`, with separate Telegram token (`NEXOSTRAT_BOT_TOKEN`) and separate per-tenant API key budget envelope. Supersedes ADR-020. CLAUDE.md Strict Rule #4 clarified the same day to permit `/srv/brain-hub/` infrastructure references while continuing to forbid `/srv/brain` artifact references.
- **Pipeline client routing surface ready.** `/srv/Nexostrat/pipeline/clients/_template/` exists with the canonical 12-stage subfolder structure (`00_intake` … `11_retainer`, plus `archive/ communications/ transcripts/ checkpoint.md state.json README.md`). The `transcripts/` subfolder is the destination Brain Bot Platform §8 B4 names for `client_slug`-routed minutes. One active client folder (`trixx-logistics/`) cloned from the template.
- **Three-persona governance** (Founder + Skills-Master + Client-Owner) with per-persona inboxes at `00_META/inbox/`, `skills/00_META/inbox/`, `pipeline/00_META/inbox/`. `infra/scripts/nexostrat-memos.py` surfaces unread memos. All three currently clean of meetings-overhaul memos.
- **Audit-finding tasks already tracked.** Five ADR-039 B-series follow-ups are open in `tasks.json` with due dates ahead of Stage 1 launch (2026-06-30 → 2026-07-15):
  - `t-nexostrat-telegram-account` (B19, due 2026-06-15) — firm-owned Telegram for `@NexostratBot`
  - `t-weekend-desktop-on-decision` (B16, due 2026-06-15) — Mon 08:00 brief depends on Sun 19:30 extraction running
  - `t-confidence-calibration-corpus` (B17, due 2026-06-22) — 50-example rated corpus for hybrid-by-confidence tuning
  - `t-plan-04-description-update` (due 2026-05-28) — master-index housekeeping, orthogonal to this overhaul
  - `t-plan-08-client-meeting-integration` (B18, due 2026-07-15) — client-meeting integration spec
- **Backup posture** (Gitea origin + GitHub + Codeberg mirrors + nightly rsync to warm-standby) operational per Plan 01b. R12 pre-overhaul tarball verified 2026-05-25 17:30 on server.

### WIP / surfaced inconsistencies

- **`tasks.json` schema gap for hub auto-writes.** Master plan §2.3 + Brain Bot Platform §8 expect the hub to write `extracted_actions[i]` items with provenance metadata: `text`, `due`, `assignee`, `confidence`, source meeting id, `auto_added: true`. The current `nexostrat-tasks-v1` schema has `subject` (not `text`), no `assignee`, no `confidence`/`auto_added`/`source_meeting` fields. The hub can technically write into the existing shape by mapping `text → subject` and dropping the rest, but that loses the audit trail B6 requires (sample 20 auto-written tasks, retune threshold from data). Resolved as **prereq P-N1** below — additive schema extension.
- **`00_META/audit/` directory does not exist.** Brain Bot Platform §8 specifies that hybrid-by-confidence auto-writes land both in `tasks.json` AND append a row to `/srv/Nexostrat/00_META/audit/auto_tasks.log`. The directory has never been created. Trivial fix (P-N2).
- **`00_META/calibration/auto_task_extraction.jsonl` does not exist.** Master plan §6.6 step 4.7 says: "test against the **existing** calibration corpus." It does not yet exist; tracked as `t-confidence-calibration-corpus` (B17) due 2026-06-22. This is a hard gate on Phase 4.7 (DeepSeek migration validation) and on the hybrid-by-confidence auto-write going live. P-N3 below.

### Designed but not implemented

- **Brief templates at `/srv/Nexostrat/00_META/templates/`.** Brain Bot Platform §8 (audit B5) names three required files: `pre_meeting_brief.md`, `t_20m_agenda.md`, `t_1h_reminder.md`, plus `README.md` documenting per-block data sources in plain English so JP or a contractor can edit safely. **None exist.** The `00_META/templates/` directory exists but contains six different `.tmpl` files for CLAUDE.md/GEMINI.md scaffolding (template-of-templates pattern). P-N4 below.
- **`00_META/calendar_filter.md`.** Brain Bot Platform §9 audit B7 mandates this file as the single source of truth for the Nexostrat-relevance filter applied when the Claude session populates `calendar_cache.json` from Ricardo's personal Google Calendar. The filter rule is sketched in BB Platform §9 ("(a) `summary` contains 'Nexo' case-insensitive, OR (b) sub-calendar `Nexostrat`, OR (c) attendees include JP") but not yet captured here. P-N5 below.
- **`calendar_cache.json`** does not exist. Populated lazily by Claude/Gemini sessions when needed (per BB §9 design pattern, refresh is session-mediated; nothing is scheduled to refresh it autonomously). Phase 5 work consumes this file; the first session that triggers a Phase 5 step writes it.
- **`pipeline/clients/<slug>/transcripts/` first real write.** Folder exists as part of `_template/`; no client meeting has yet been recorded with `client_slug` set. Phase 6 end-to-end test will exercise this path.
- **Bot tenancy itself is not yet live.** The Brain Hub session ships the hub-side tenant config (NEXOSTRAT_BOT_TOKEN routing, per-tenant API key envelope, ScopedFS writes against `/srv/Nexostrat/`). No code change in this scope. Master plan Phase 4 (4.1–4.7) is hub-owned; the only thing Nexostrat *contributes* during Phase 4 is the schema extension (P-N1) and audit log shape (P-N2).

### Open inbox memos affecting integration

- `/srv/Nexostrat/00_META/inbox/` — empty (only `.gitkeep` + `archive/`). No memos pending on this overhaul.
- `/srv/Nexostrat/00_META/handoff/claude_to_gemini.md` + `gemini_to_claude.md` both in `TEMPLATE` state — no open Gemini handoff.

---

## 2. Alignment check

Comparing master plan §2 (Architecture) and §4 (Tooling) against this scope's ratified state (founding spec amended 2026-05-14 + ADR-039 2026-05-21):

- **[ALIGNED] Tenant model.** Master plan §6.6 phase 4 assumes Nexostrat runs as a hub tenant; ADR-039 ratified exactly that on 2026-05-21. No deviation.
- **[ALIGNED] Per-tenant API key envelope.** Master plan §4 + ADR-039 amendment #2 both require Nexostrat to operate under its own API key budget cap (independent from Personal/Mevillo). No deviation.
- **[ALIGNED] Hybrid-by-confidence task posture at 0.85.** Master plan §2.3 + Brain Bot Platform §8 audit B6 + Nexostrat acceptance on 2026-05-22. Threshold configurable per tenant in hub `routing.yaml`. No deviation.
- **[ALIGNED] Client meetings → `pipeline/clients/<slug>/transcripts/`.** Master plan §2.8 storage layout (internal Nexostrat meetings under `/srv/meetings/nexostrat/`) and Brain Bot Platform §8 B4 (client meetings routed via `client_slug` to `pipeline/clients/<slug>/transcripts/`) describe two **distinct destinations** that do not collide. The two-root distinction was already designed in MEETINGS_DESIGN.md §1. Nexostrat's `_template/transcripts/` is ready as the receiving end.
- **[ALIGNED] `tasks.json` is the single source of truth.** Master plan §2.4 explicitly forbids a new `_pending_actions.yaml`; Nexostrat already uses `tasks.json` as the only action ledger. No deviation.
- **[ALIGNED] No-`/srv/brain` rule in Nexostrat artifacts.** This contribution doc lives under `/srv/Nexostrat/` and references `/srv/brain/00_META/governance/plans/...` in its preamble. Per ADR-039 anti-decision clause ("Citations like the one in this ADR's frontmatter are governance-traceability, not infrastructure-coupling") and the CLAUDE.md Strict Rule #4 2026-05-21 clarification, governance-traceability references for cross-scope plan participation are permitted.
- **[ALIGNED] DeepSeek migration for Nexostrat tenant only.** Master plan §4 swaps the Nexostrat tenant's extractor from OpenAI to DeepSeek V3.1 (cost-driven). ADR-039's per-tenant key envelope already isolates this choice — swap is one config line in hub `routing.yaml` + base URL change. Personal/Mevillo unaffected.
- **[ALIGNED] Calendar cache pattern.** Master plan §6.7 Phase 5 + Brain Bot Platform §9 both specify `/srv/Nexostrat/calendar_cache.json` populated by Claude sessions, with the Nexostrat-relevance filter applied (B7). Aligned with founding spec.

**No conflicts.** All master plan assumptions consistent with this scope's ratified state as of 2026-05-25. The schema gap on `tasks.json` (§1 WIP) is a prereq, not a conflict — both sides agree on the destination (`tasks.json`); the schema just needs an additive extension to carry the new fields.

---

## 3. Prerequisites we MUST complete first

Five concrete prereqs. All five fit on this scope alone; none cross-scope. P-N1 + P-N2 + P-N4 + P-N5 are small (≤ 2h each) and gate Phase 4/5 ship. P-N3 (calibration corpus) is medium — labelling time, not coding time — and has a clean defer option that ships Phase 4 without auto-write.

- **P-N1: `tasks.json` schema v2 — additive extension for hub auto-writes**
  - **What:** Amend the schema at `/srv/Nexostrat/tasks.json` to `nexostrat-tasks-v2`. Add four optional task-object fields (preserve all v1 fields): `assignee` (string|null), `source_meeting` (slug string|null), `auto_added` (bool, default false), `confidence` (float 0.0–1.0|null), and an alias key `text` accepted as a synonym of `subject` so the hub can write either. Document schema in `00_META/proposals/2026-05-26_tasks-v2-schema.md` (one short proposal, no ADR — additive change to an internal data file, not a decision rethink).
  - **Why:** The hub's hybrid-by-confidence auto-write path (Brain Bot Platform §8) needs provenance metadata to (a) audit auto-writes against the calibration corpus, (b) let the bi-weekly threshold-retuning pass sample auto-written rows with their original confidence scores, (c) link a task back to its source meeting for `/done #N` flows. Without these fields the hub either drops the metadata (loses B6 audit capability) or stores it elsewhere (drifts from the single-source-of-truth posture).
  - **Effort:** S (≤ 2h). Schema doc + one-line `$schema` bump + .schema.json validator if we keep one. No data migration — additive fields default to null/false.
  - **Depends on:** none.
  - **Done criterion:** `00_META/proposals/2026-05-26_tasks-v2-schema.md` exists; `tasks.json` `$schema` field reads `nexostrat-tasks-v2`; a sample auto-extracted task fixture validates; both v1-shaped and v2-shaped tasks coexist in the file without error.
  - **Defer option:** ship Phase 4 with hub writing into v1 fields (`text → subject`, drop the rest). Cost: B6 audit pass loses the per-row confidence + source-meeting trail; threshold retuning has to be done by sampling the hub's own log instead. Acceptable for Stage 1 if calibration corpus (P-N3) ships at v1 quality.

- **P-N2: Create `00_META/audit/` with empty `auto_tasks.log`**
  - **What:** Create `/srv/Nexostrat/00_META/audit/` directory and an empty `auto_tasks.log` file (UTF-8, line-oriented append-only — one JSON object per line: `{ts, source_meeting, extracted_text, score, model, task_id_written}`). Add a `README.md` documenting the row schema and stating the file is hub-owned (written via ScopedFS) but Nexostrat-readable for audit passes.
  - **Why:** Brain Bot Platform §8 names this exact path as the audit log destination for hybrid-by-confidence auto-writes. The hub will refuse to start (or fail silently — depending on hub-side error handling) if the directory does not exist when ScopedFS tries to write the first row.
  - **Effort:** S (≤ 30 min).
  - **Depends on:** none.
  - **Done criterion:** `00_META/audit/auto_tasks.log` exists (empty, committed); `00_META/audit/README.md` documents the row schema.
  - **Defer option:** trivial enough that there is no realistic deferral — fold into the same commit as P-N1.

- **P-N3: Seed `00_META/calibration/auto_task_extraction.jsonl` with ≥ 50 rated examples**
  - **What:** Create `/srv/Nexostrat/00_META/calibration/` directory + `auto_task_extraction.jsonl` with at least 50 manually-rated examples per audit finding B17. Each row: `{meeting_slug, transcript_excerpt, candidate_action, due_extracted, confidence_label (0..1), reviewer (ricardo|jp), reviewed_at}`. Source material: existing meetings under `/srv/meetings/nexostrat/` (four meetings as of audit H3 PASS) plus synthetic examples covering the long tail (ambiguous "we should do X someday" rows, multi-assignee phrasings, dates given only in relative form, etc.).
  - **Why:** Master plan §6.6 step 4.7 explicitly says: "test against the existing calibration corpus at `/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl`." Without this corpus, the DeepSeek-vs-OpenAI A/B for the Nexostrat tenant cannot be validated, and the bi-weekly Brain Architect threshold-retuning pass has nothing to measure against. This is the highest-effort prereq.
  - **Effort:** M (≤ 1d of labelling — four existing meetings × ~5 candidate actions + ~30 synthetic edge cases).
  - **Depends on:** P-N1 (the labels in the corpus mirror the schema fields the hub will write).
  - **Done criterion:** `00_META/calibration/auto_task_extraction.jsonl` exists with ≥ 50 valid JSON rows; each row carries a numeric confidence label and a reviewer attribution; a sample-pass-rate report exists at `00_META/calibration/2026-05-XX_initial-corpus-report.md` showing precision/recall at the proposed 0.85 threshold.
  - **Defer option:** **ship Phase 4 with hybrid-by-confidence DISABLED.** All extracted actions go through Telegram `[✅ Add] [❌ Skip]` confirmation regardless of confidence score. Cost: lose the "auto-write at 0.85" UX win for Stage 1 launch (~6 weeks of friction); Phase 4 step 4.7 (DeepSeek migration) still ships but is validated by spot-check rather than corpus replay. Reasonable fallback if calibration labelling slips past 2026-06-22.

- **P-N4: Author brief templates at `00_META/templates/`**
  - **What:** Create three Spanish-language markdown templates per Brain Bot Platform §8 audit B5: `00_META/templates/pre_meeting_brief.md`, `00_META/templates/t_20m_agenda.md`, `00_META/templates/t_1h_reminder.md`. Each is a render-time markdown template with named placeholders (e.g., `{{prev_meeting.summary_actions}}`, `{{open_tasks_for_participants}}`, `{{calendar_event.title}}`). Add `00_META/templates/README.md` documenting, **in plain Spanish**, the data source for each block ("block 2 = `tasks.json` filtered by `status=open AND assignee IN [ricardo, jp]`") so JP or a contractor can safely edit.
  - **Why:** Master plan §6.7 Phase 5 (pre-meeting briefs) reads these templates from disk at render-time. Hub does not embed them in code; they're hot-reloadable. Without these files Phase 5 has nothing to render.
  - **Effort:** S (≤ 2h). First-draft text; iterate with JP later.
  - **Depends on:** P-N1 + P-N5 (the templates reference `tasks.json` schema fields + the calendar filter naming).
  - **Done criterion:** four files exist (3 templates + README); the README block-by-block data-source documentation is in Spanish; placeholders use a consistent `{{namespace.field}}` syntax; an inline example output (~one rendered example per template) is included in the README for sanity.
  - **Defer option:** ship Phase 5 with hub-side hardcoded templates as a stopgap. Cost: edits require a hub redeploy; JP cannot tune copy without Ricardo's involvement. Acceptable for the first two weeks post-launch while we iterate the copy from real briefs.

- **P-N5: Author `00_META/calendar_filter.md`**
  - **What:** Create `/srv/Nexostrat/00_META/calendar_filter.md` documenting the Nexostrat-relevance filter applied by any Claude/Gemini session when populating `calendar_cache.json` from Ricardo's personal Google Calendar. v1 rule per Brain Bot Platform §9 audit B7: an event qualifies if **(a)** `summary` contains "Nexo" (case-insensitive), OR **(b)** event is on a sub-calendar named `Nexostrat`, OR **(c)** the attendee list contains JP's email. Personal events (gym, family, dentist) MUST NOT land in the cache. Include a version stamp (`filter_version: v1`) that the cache schema's `filter_applied:` field will record, so a future audit detects drift.
  - **Why:** Brain Bot Platform §9 names this file as the single source of truth for the filter. Without it, the Claude session populating the cache has no canonical rule to follow, and JP-readable cache content drifts toward leaking personal events.
  - **Effort:** S (≤ 1h).
  - **Depends on:** none.
  - **Done criterion:** file exists; rule (a/b/c) explicit + examples of qualifying and non-qualifying events; `filter_version` declared; migration trigger noted ("when firm Google account `ops@nexostrat.com` is provisioned and the calendar cuts over, the filter is dropped and the file is updated to `filter_version: v2 — no filter, whole account = Nexostrat`").
  - **Defer option:** none reasonable. This is a privacy/correctness gate, not a feature, and the cost of writing it is one hour. Ship in Phase 0a.

---

## 4. What this scope adds for the overhaul

Concrete deliverables this scope owns, mapped to master plan §6 phase numbers:

- **Phase 0a (per-scope prereqs):** P-N1 through P-N5 above. All land as commits in `/srv/Nexostrat/`. None require code work outside this scope.
- **Phase 4 (hub-side handling):** schema extension (P-N1) lands in this scope; audit log destination (P-N2) lands in this scope. No other Nexostrat-side change for Phase 4 — the hub does the writes via ScopedFS, the Telegram approval flows, the `/done #N` task updates. This scope is purely the **target filesystem** during Phase 4.
- **Phase 5 (calendar integration + pre-meeting briefs):** brief templates (P-N4) + calendar filter spec (P-N5) land in this scope. `calendar_cache.json` is written lazily by Claude sessions; the first session that needs it runs the MCP fetch and writes the cache (this is a one-time bootstrap; subsequent refreshes are mediated by Claude sessions on any cwd-Nexostrat session that touches calendar logic).
- **Phase 6 (end-to-end test):** this scope hosts the test meeting's `client_slug` routing target (`pipeline/clients/<test_slug>/transcripts/`) if the test uses a client-meeting flow, OR receives the action items into `tasks.json` if it's an internal meeting. Either path exercises this scope as a consumer; no Nexostrat-side code change for Phase 6.

Phase-level contribution summary: **5 prereqs, all in Phase 0a, no Nexostrat-side work in Phases 1–3 or 6.** Phases 4 + 5 consume Nexostrat assets; the producer side stays in `/srv/meetings/` and the routing/notification side stays in `/srv/brain-hub/`.

---

## 5. What this scope needs from root or other scopes

- **From Brain Hub session (`/srv/brain-hub/`):**
  - **Tenant config in `routing.yaml`** for the Nexostrat tenant including: `bot_token_env: NEXOSTRAT_BOT_TOKEN`, `api_key_env: DEEPSEEK_API_KEY_NEXOSTRAT` (post-migration) + base URL, `confidence_threshold: 0.85`, `scoped_fs_writes: [/srv/Nexostrat/tasks.json, /srv/Nexostrat/00_META/audit/auto_tasks.log]`, `scoped_fs_reads: [/srv/Nexostrat/tasks.json, /srv/Nexostrat/calendar_cache.json, /srv/Nexostrat/00_META/templates/, /srv/Nexostrat/pipeline/clients/]`.
  - **DeepSeek API key procurement** (`DEEPSEEK_API_KEY_NEXOSTRAT`) before Phase 4 step 4.7 ships. Audit R10 was WAIVED for Phase 0–3 readiness; hard-gated on Phase 4.7. Nexostrat's budget envelope (initial $20/month per ADR-039) covers the spend.
  - **ScopedFS write capability** for `/srv/Nexostrat/tasks.json` and `/srv/Nexostrat/00_META/audit/auto_tasks.log`. Per Brain Bot Platform §8, the hub writes these via ScopedFS scoped to `(/srv/Nexostrat, [])` — confirmation that this scope path is enumerated in the Nexostrat tenant's scope list.
  - **Status-change suggestion handler** (Phase 4 step 4.4) that consumes `status_change_suggestions[]` from the event payload and routes a Telegram DM to Ricardo with `[✅ Mark done] [❌ Keep open] [⏸ Defer]` inline keyboard. On ✅, the hub mutates the matching `tasks.json` row's `status` field to `done` + writes a `completed:` timestamp. Hub-side concern; this scope is the target.

- **From Meetings Curator (`/srv/meetings/`):**
  - **`client_slug` field set at recording time** (per master plan §2.1 Q3 → metadata.yaml + event payload). For Nexostrat-scope client meetings, the producer must emit `client_slug: <slug>` so the hub routes minutes to `/srv/Nexostrat/pipeline/clients/<slug>/transcripts/` per Brain Bot Platform §8 audit B4. Producer side ships this as part of Phase 2 (`meeting finish` Q1–Q5).
  - **`extracted_actions[].scope: "nexostrat"`** routing key correctness — producer must stamp the scope field on every action item it extracts during a Nexostrat-scope meeting (master plan §2.3 step 1 + §2.4 cross-scope handling). Cross-scope items (a Nexostrat meeting that creates an AttenBot todo) carry `extracted_actions[i].scope: "atten_bot"` so the hub routes elsewhere. Already designed in the contract; flagging for completeness.

- **From root (Brain Architect):**
  - **Phase 0a sequencing.** When root populates Phase 0a from this contribution doc, P-N1 (schema) should land before P-N3 (corpus) and P-N4 (templates), since both downstream artifacts reference v2 field names. P-N2 and P-N5 are order-free. Suggested order: P-N5 (independent) → P-N1 + P-N2 (small co-commit) → P-N4 → P-N3 (corpus labelling can run in parallel with P-N4).
  - **Deployment doc step text** for the five prereqs — root's pattern (per master plan §6.2) is to append matching "open Claude in /srv/Nexostrat/, paste this prompt" steps to the deployment doc §2. Five short prompts; trivial.

---

## 6. Reviewer / executing persona

- **Author:** Nexostrat Founder (this session).
- **Reviewer:** Brain Architect (root) for cross-scope integration; Brain Hub session for tenant-config alignment and ScopedFS scope enumeration.
- **Executor (Phase 0a prereqs):** Nexostrat Founder session, working in `/srv/Nexostrat/`. None of the five prereqs require Skills-Master or Client-Owner involvement (no skills change; no client folder change beyond what `_template/transcripts/` already provides).

---

## 7. Notes for root

- **No new strategic decisions in this doc.** Every prereq traces to an already-ratified artifact: ADR-039 (2026-05-21) for tenancy, Brain Bot Platform §8 audit findings B5/B6/B7/B17/B19 (2026-05-22) for the schema/audit/calibration/templates/filter surfaces, master plan §2 (2026-05-25) for the cross-scope contract. The five prereqs are operationalization, not architecture.
- **Five Nexostrat tasks already in flight** for the same overhaul surface (B16/B17/B18/B19/Plan-04). Three of them (B16 weekend-desktop, B17 calibration, B19 firm Telegram) are Phase 4/5 hard gates for hub-side launch but pre-date this overhaul. P-N3 in this doc is the same work as `t-confidence-calibration-corpus` (B17) — should be deduplicated rather than tracked twice. Root may want to mark the contribution-doc P-IDs as ALIASES of the existing task IDs in the Phase 0a write-up.
- **No collision with current session 14 work.** Session 14's write surface (intro V3 production under `operations/marketing/website-intro/`) is fully orthogonal to the meetings overhaul. Phase 0a can land immediately without coordinating around in-flight marketing work.
- **No conflict on the no-`/srv/brain` rule.** This doc's preamble references the master plan path; per ADR-039 anti-decision clause + the Strict Rule #4 clarification, governance-traceability references are permitted. No precedent issue.
- **Stage 1 launch window (2026-06-30 → 2026-07-15)** comfortably accommodates Phase 0a (estimate: 1–2 days end-to-end if P-N3 ships at the deferred posture; 4–5 days if the full 50-example corpus lands first). Suggest decoupling the corpus shipping from the rest of Phase 0a — let P-N1/P-N2/P-N4/P-N5 land within a week, and treat P-N3 as a parallel labelling pass with a 2026-06-22 deadline (matching the existing B17 task).

---

**End of contribution doc.**
