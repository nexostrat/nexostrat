# `00_META/audit/` — Hub-owned audit trail

This directory hosts append-only audit logs written by the **Brain Bot Hub** (`/srv/brain-hub/`) when the Nexostrat tenant's hybrid-by-confidence path auto-writes a task to `/srv/Nexostrat/tasks.json`.

## Ownership

| Aspect | Owner |
|---|---|
| **Writes** | Brain Bot Hub (`/srv/brain-hub/`), via ScopedFS with write permission scoped to this directory. The Nexostrat tenant's `meeting_task_writer` plugin appends one NDJSON row per auto-written task. |
| **Reads** | Nexostrat session (audit passes, calibration corpus replay, threshold-retuning analysis) — read-only. |
| **Schema authority** | Brain Bot Platform §8 audit B6. Schema changes land via ADR in `/srv/brain-hub/00_META/governance/adr/`. |

> Nexostrat owns the *filesystem location*; the hub owns the *write semantics*. Do not hand-edit `auto_tasks.log` from a Nexostrat session — it would race the hub's append path and break the audit invariant.

## `auto_tasks.log` — NDJSON row schema

Per Brain Bot Platform §8 audit B6, each row is a single-line JSON object:

```json
{"ts": "<ISO-8601 timestamp>", "source_meeting": "<meeting slug>", "extracted_text": "<original action-item text>", "score": <float 0.0–1.0>, "model": "<model id>", "task_id_written": "<t-N id in tasks.json>"}
```

### Field reference

| Field | Type | Required | Meaning |
|---|---|---|---|
| `ts` | string (ISO-8601) | yes | Wall-clock timestamp at the moment the hub appended the task to `tasks.json`. UTC or local-with-offset both acceptable; the hub stamps consistently. |
| `source_meeting` | string | yes | Meeting slug under `/srv/meetings/nexostrat/YYYY-MM-DD/<slug>/` that the action item was extracted from. Enables back-reference to the transcript + summary for audit. |
| `extracted_text` | string | yes | The action-item text as extracted by the model (pre-normalisation). Used by calibration replay to compare against the labelled corpus. |
| `score` | float | yes | The model's confidence score for this extraction (0.0–1.0). Auto-write fires only when `score >= auto_task_threshold` (initial threshold: 0.85 per routing.yaml). |
| `model` | string | yes | Model identifier that produced the extraction (e.g., `deepseek-chat`, `gpt-4o-mini`). Required because the threshold is model-specific and the bi-weekly retune samples per-model. |
| `task_id_written` | string | yes | The `id` field assigned by `tasks.json` (e.g., `t-47`). Closes the loop from audit log → task ledger. |

## Append semantics

- **One row per auto-write.** Tasks that route through the `[✅ Add] [❌ Skip]` Telegram confirmation flow are **not** logged here — only auto-writes that bypass confirmation.
- **Append-only.** Never rewrite or truncate. Rotation (if needed) is a future hub-side concern; for Stage 1, the file grows unbounded.
- **Atomic appends.** The hub writes each row as a single `O_APPEND` write so concurrent appends from multiple plugin invocations don't interleave.
- **Newline-terminated.** Each row ends with `\n`. Empty file (0 bytes) is the initial valid state.

## Audit uses

The Nexostrat session reads `auto_tasks.log` for:

1. **Calibration corpus replay** — sample auto-written rows, compare `score` against the labelled `00_META/calibration/auto_task_extraction.jsonl` to check that the threshold is holding precision.
2. **Bi-weekly threshold retuning** — review the score distribution of auto-written rows vs. confirmed-via-Telegram rows; recommend threshold adjustments.
3. **Spot-check audits** — for any task in `tasks.json` with `auto_added: true`, look up its `task_id_written` to find the source meeting + extracted text, verify it's a legitimate action.
4. **Source-meeting cross-reference** — given a meeting slug, list every auto-written task it produced.

## Related artifacts

- **Task ledger:** `/srv/Nexostrat/tasks.json` (schema v2 once P-N1 ships — `auto_added`, `confidence`, `source_meeting` fields).
- **Calibration corpus:** `/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl` (labelling target — P-N3).
- **Hub-side writer:** `/srv/brain-hub/hub/plugins/meetings/task_writer/extractor.py` (the producer).
- **Routing config:** `/srv/brain-hub/routing.yaml` — Nexostrat tenant block, `auto_task_threshold: 0.85`.
- **Spec:** Brain Bot Platform §8 audit B6 (schema authority); master plan §6.6 Phase 4 (auto-write flow).
- **Contribution doc:** `/srv/Nexostrat/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md` §3 P-N2.
