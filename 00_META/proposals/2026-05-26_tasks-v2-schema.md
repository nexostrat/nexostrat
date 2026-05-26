# `tasks.json` Schema v2 (`nexostrat-tasks-v2`)

> **Status:** ACCEPTED — landed as Phase 0a P-N1 of the 2026-05-25 meetings-pipeline overhaul
> **Date:** 2026-05-26
> **Scope:** `/srv/Nexostrat/tasks.json`
> **Author:** Nexostrat Founder session
> **Driver:** Hub auto-write provenance metadata for the hybrid-by-confidence task path
> **Supersedes:** `nexostrat-tasks-v1` (forward-compatibly — all v1-shaped rows remain valid under v2)

---

## 1. Why

The Brain Bot Hub (`/srv/brain-hub/`) runs Nexostrat as one of its tenants per ADR-039. The hub's hybrid-by-confidence task path (Brain Bot Platform §8 audit B6) writes action items extracted from meeting transcripts directly into this scope's `tasks.json` when the extraction confidence meets or exceeds the per-tenant threshold (initial: 0.85). For that flow to be auditable, each auto-written row needs provenance metadata that v1 does not carry:

- **Which meeting produced it** — so an audit pass can back-reference the transcript that generated each row.
- **What confidence score the model attached** — so the bi-weekly threshold-retuning pass can sample auto-written rows against the labelled calibration corpus.
- **Whether the row was auto-added vs. confirmed via Telegram** — so spot-check audits can filter to the auto-write subset only.
- **An assignee/owner field** — v1 has neither; the hub assigns the row to a founder at write time.

Adding these fields to v1 by mutation would risk silently breaking any reader that assumed the v1 shape. The clean path is an **additive extension**: v2 = v1 ∪ five new optional fields + two write-time aliases. Every v1-shaped row stays valid under v2; readers that only know v1 keep working as long as they tolerate unknown fields (the hub's reader and the local Python validators already do).

A second, smaller driver also folds in: this scope's brief templates' `README.md` documents reads using a field called **`owner`** (e.g., `status=open AND owner IN [ricardo, jp]`), while Brain Bot Platform §8 names the field **`assignee`**. v2 resolves the naming mismatch by making `owner` canonical and accepting `assignee` as an alias on write — both sides can express their convention without a flag day.

---

## 2. What changed

The top-level shape is unchanged:

```json
{
  "$schema": "nexostrat-tasks-v2",
  "project": "nexostrat",
  "updated": "<ISO-8601 timestamp>",
  "tasks": [ ... ]
}
```

The only top-level edit is `$schema: "nexostrat-tasks-v1"` → `"nexostrat-tasks-v2"`.

Each task object now accepts five **new optional fields** (all default to absent / null; v1-shaped rows that omit them remain valid) and two **write-time aliases** (canonical + alias forms are both accepted; the canonical form wins if both are present).

### 2.1 v1 fields (unchanged, preserved)

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | Stable task identifier (e.g., `t-meetings-overhaul-tasks-v2-schema`, `t-47`). Format unconstrained; readers treat as opaque. |
| `subject` | string | yes (or `text`) | One-line task title. Canonical write field. |
| `status` | string | yes | One of `open`, `in_progress`, `blocked`, `done`, `completed`, `superseded`, `deferred`, `cancelled`. Both `done` and `completed` are accepted (historical drift; either reads as "closed"). |
| `priority` | string | yes | One of `critical`, `high`, `medium`, `low`. |
| `due` | string (ISO-8601 date) \| null | no | Target completion date. |
| `created` | string (ISO-8601 date) | yes | Date the task was opened. |
| `completed` | string (ISO-8601 date) | no | Date the task closed. Required when `status ∈ {done, completed}`; absent otherwise. |
| `notes` | string | no | Free-text narrative. Multi-line allowed (newlines stay literal `\n` in JSON). |
| `description` | string | no | Optional longer-form description (some tasks carry this; the brief templates' renderer reads `subject ?? text` for the title, `description` for body if present). |
| `blocked_by` | string \| array of strings | no | Task `id` of the blocker(s). |

### 2.2 New v2 fields (additive, optional)

| Field | Type | Default | Meaning |
|---|---|---|---|
| `owner` | string \| null | absent | The founder this task is assigned to. Canonical assignment field. Matches the brief templates' README convention (`status=open AND owner IN [ricardo, jp]`). Values are unconstrained strings; typical: `ricardo`, `jp`, `unassigned`. |
| `assignee` | string \| null | absent | **Alias of `owner`** accepted on write for Brain Bot Platform §8 interop. Readers prefer `owner` when both are present (canonical wins). A row that carries only `assignee` is treated identically to one that carries the same value as `owner`. |
| `source_meeting` | string \| null | absent | Meeting slug under `/srv/meetings/nexostrat/YYYY-MM-DD/<slug>/` that this task was extracted from. Empty / null on tasks created manually. |
| `auto_added` | bool | `false` | `true` when the row was written by the hub's hybrid-by-confidence auto-write path (bypassing the `[✅ Add] [❌ Skip]` Telegram confirmation flow). `false` (or absent) for all other paths: manual edits, Telegram-confirmed extractions, session-end batch updates, etc. |
| `confidence` | float (0.0–1.0) \| null | absent | The model's extraction confidence score at the moment the auto-write fired. Present only on rows where `auto_added == true`. Range matches the calibration rubric in `00_META/calibration/README.md` (0.90–1.00 direct quote · 0.70–0.89 paraphrased commitment · 0.40–0.69 inferred · 0.00–0.39 speculation). |

### 2.3 Write-time aliases

Two aliases let writers use either convention without coordination:

| Canonical | Alias | Resolution rule |
|---|---|---|
| `subject` | `text` | If both present, `subject` wins. If only `text` is present, the row is treated as if `subject = text`. The audit log row's `extracted_text` (in `00_META/audit/auto_tasks.log`) carries the pre-normalised text regardless. |
| `owner` | `assignee` | If both present, `owner` wins. If only `assignee` is present, the row is treated as if `owner = assignee`. |

The hub's writer is free to emit either form. Local edits and the session-end protocol should prefer the canonical form (`subject`, `owner`) for clarity.

### 2.4 Forward compatibility

- All v1-shaped rows validate against v2 unchanged.
- Readers that don't yet understand the new fields ignore them (every Python consumer in this scope already uses `dict.get(...)` access patterns; no positional or schema-strict reads).
- The bump from v1 → v2 is **non-breaking**: there is no migration step. The first commit that bumps `$schema` to `"nexostrat-tasks-v2"` is the entire migration.

---

## 3. Examples

### 3.1 A v1-shaped row (still valid under v2)

```json
{
  "id": "t-confidence-calibration-corpus",
  "subject": "Hand-rate ≥50 examples in 00_META/calibration/auto_task_extraction.jsonl",
  "status": "open",
  "priority": "high",
  "due": "2026-06-22",
  "created": "2026-05-22",
  "notes": "BB Platform §8 audit B17. Same line item as P-N3 in the meetings-overhaul contribution doc."
}
```

No v2 fields, no aliases — reads as a normal pre-v2 row.

### 3.2 A manually-authored v2-shaped row (uses `owner`, no auto-write metadata)

```json
{
  "id": "t-2026-06-01-prep-deck",
  "subject": "Prep deck for Trixx Logistics paid-diagnostic kickoff",
  "status": "in_progress",
  "priority": "high",
  "due": "2026-06-01",
  "created": "2026-05-28",
  "owner": "ricardo",
  "source_meeting": "2026-05-28_trixx-logistics-discovery",
  "auto_added": false,
  "notes": "Pulled out of the discovery-call transcript by hand; not an auto-write."
}
```

Demonstrates `owner` + `source_meeting` on a non-auto-added row.

### 3.3 An auto-added row written by the hub (uses both aliases)

```json
{
  "id": "t-47",
  "text": "JP to ship the revised competitor-analyst prompt by Friday",
  "status": "open",
  "priority": "medium",
  "due": "2026-06-05",
  "created": "2026-05-30",
  "assignee": "jp",
  "source_meeting": "2026-05-30_strategy-alignment",
  "auto_added": true,
  "confidence": 0.92,
  "notes": "Auto-extracted by hub at 2026-05-30T08:14:22-07:00. Audit row in 00_META/audit/auto_tasks.log."
}
```

Uses `text` (alias of `subject`) and `assignee` (alias of `owner`) — both forms accepted because Brain Bot Platform §8 names the fields that way. A reader resolving canonical fields sees `subject = "JP to ship..."` and `owner = "jp"`.

### 3.4 Smoke-test fixture (this commit)

The commit landing this schema includes one v2-shaped task with `status: completed` to prove v1 + v2 rows coexist in the same `tasks` array. See `tasks.json`, id `t-v2-schema-fixture`.

---

## 4. Validation

There is no Python JSON-Schema file enforcing v2 yet (Plan 01a Task 9 shipped a v1 schema at `infra/schemas/tasks.schema.json`; a v2 update is a follow-on, not gated on this proposal). For now:

- The hub's writer (`/srv/brain-hub/hub/plugins/meetings/task_writer/extractor.py`, per Phase 4 of the master plan) emits v2-shaped rows directly.
- Local readers (`infra/scripts/nexostrat-memos.py`, the brief templates' renderer, the session-end protocol) read with `dict.get(...)` and tolerate either shape.
- The bi-weekly retune pass cross-references rows where `auto_added == true` against `00_META/audit/auto_tasks.log` (provenance trail) and `00_META/calibration/auto_task_extraction.jsonl` (labelled corpus).

A v2 JSON Schema file at `infra/schemas/tasks.schema.json` should land alongside Plan 02b's broader schema sweep, or sooner if the hub's writer needs to be validated before its first auto-write fires. Not blocking for Phase 0a P-N1 closure.

---

## 5. Related artifacts

- **Master plan §6.2 Phase 0a P-N1:** [`/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`](../../../../brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md) (governance-traceability reference per ADR-039 anti-decision clause).
- **Nexostrat §8 contribution doc:** [`00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md`](../governance/plans/2026-05-25_meetings-overhaul-contribution.md) §3 P-N1.
- **Audit log destination:** [`00_META/audit/README.md`](../audit/README.md) — `00_META/audit/auto_tasks.log` row schema (links `task_id_written` → the v2 task it produced).
- **Calibration corpus:** [`00_META/calibration/README.md`](../calibration/README.md) — confidence rubric the `confidence` field's range matches.
- **Brief templates README:** [`00_META/templates/README.md`](../templates/README.md) — reads `owner` (canonical here); BB Platform §8 reads `assignee` (alias accepted on write).

---

## 6. Change log

| Date | Description |
|---|---|
| 2026-05-26 | v2 schema accepted + landed in same commit. `$schema` field bumped on `/srv/Nexostrat/tasks.json`. One v2-shaped fixture row (`t-v2-schema-fixture`, status `completed`) added as a smoke test confirming v1 + v2 coexist. |
