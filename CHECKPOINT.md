# CHECKPOINT — root (Founder)

**Updated:** 2026-05-26T03:35:00-07:00
**By:** ricardo (via Claude Code session 17; same-night continuation after session 16)
**Persona:** Founder
**Session topic:** Meetings-pipeline overhaul Phase 0c P-H2 — populate `/srv/Nexostrat/calendar_cache.json` via Google Calendar MCP + `hub.google.calendar_filter_nexostrat`. COMMANDS.md refresh procedure documented. Drift cleanup pass: `nexostrat_v1` → `nexostrat-v1` in master plan + Brain Hub doc; `calendar_filter.md` JP placeholder amended to `jpasistentepersonal@gmail.com`. No architecture changes, no ADRs, no Gemini handoff.

## What just happened (last session — read once, don't re-litigate)

**Single-prompt deliverable session, ~1 hour wall-time.** Ricardo opened with a precise prompt referencing master plan §6.2 Phase 0c P-H2 + Brain Hub contribution doc §3 P-H2 + `00_META/calendar_filter.md`. Execute → verify → commit → push → tick master plan → push → drift cleanup → end. Same shape as sessions 15 + 16 (P-N2 / P-N1) but cross-scope (P-H2 was raised by Brain Hub but executes from Nexostrat scope because the Google Calendar MCP auth lives on Ricardo's account, not the hub process).

**1. Read four governance docs** to scope the task: master plan §6.2 + §7.1, Brain Hub contribution doc §3 P-H2, Nexostrat `00_META/calendar_filter.md` (audit B7 source of truth), `/home/ricardo/brain-hub/hub/google/calendar_filter_nexostrat.py` (the imported filter — constant `FILTER_VERSION = "nexostrat-v1"`).

**2. Discovered `brain-hub` lives at `/home/ricardo/brain-hub/`** (not `/srv/brain-hub/` as the master plan + Brain Hub doc imply). Ricardo confirmed the path mid-session via a free-form sidebar reply. Doc-vs-on-disk drift flagged in journal but not fixed (out of P-H2 scope).

**3. Confirmed JP attendee email** via AskUserQuestion before any API call: `jpasistentepersonal@gmail.com` (one of JP's two Gmails — the other, `juan@juanencripto.com`, is secondary). Superseded the `jp@example.com` placeholder in `00_META/calendar_filter.md`.

**4. Google Calendar MCP fetches.** Two calendars accessible to `ricardomejiacaicedo@gmail.com`: primary (10 events) + `Holidays in Spain` (3 events). 13 upstream total. Fetched 2026-05-25 → 2026-06-24.

**5. Filter applied.** Imported `nexostrat_filter` from `/home/ricardo/brain-hub/`. Per-event `source_calendar = <calendar summary>` injected before the call (Google's API doesn't return that field; the filter's rule 2 needs it). 9 / 13 matched (all via `summary_contains_nexo`); 1 Trixx + 3 holidays correctly dropped. Match rationale stored per event.

**6. Cache file written** at `/srv/Nexostrat/calendar_cache.json`. Schema per master plan §6.2 + Brain Hub doc §3: `generated_at` (ISO-8601 UTC), `generated_by: "claude@desktop"`, `filter_applied: "nexostrat-v1"`, `stale_after_hours: 24`, `events[]` with upstream fields + `source_calendar` + `match`.

**7. COMMANDS.md amended.** New "Calendar cache refresh" section (between Periodic operations and Vault). Documents source-of-truth references, full cache schema, 4-step refresh procedure (run Claude on a PC with the Google Calendar MCP authenticated; ask in `/srv/Nexostrat/` for refresh; verify with `jq` one-liner), fallback path (demo-only hand-author), migration trigger.

**8. Master plan §6.2 P-H2 checkbox ticked** (line 435) + **§7.1 done-row appended** (line 628). Brain commit `9b5d8ba`. Nexostrat commit `b03d3af` (cache + COMMANDS.md).

**9. Drift cleanup pass** (after Ricardo's "fix them" mid-session authorization at end-prep). `nexostrat_v1` (underscore) → `nexostrat-v1` (hyphen) in master plan §6.2 P-H2 row + done-criterion (lines 435 + 439) and Brain Hub contribution doc §3 P-H2 (lines 85 + 89). Verified `grep -rn 'nexostrat_v1'` returns empty across master plan, Brain Hub doc, Nexostrat contribution doc, `calendar_filter.md`. Correction logged in §7.1: prior row asserted Nexostrat contribution doc carried the underscore form; verified false. `calendar_filter.md` line 11 amended.

**10. Verification at session close.** `filter_applied = "nexostrat-v1"`, events = 9, `generated_at` < 1h, COMMANDS.md section at line 145, master plan §6.2 ticked + §7.1 row present, zero `nexostrat_v1` residue.

## Decisions locked this session

1. **JP email canonical = `jpasistentepersonal@gmail.com`.** Used for filter's rule 3 (attendee match). Ricardo's mid-session confirmation. JP's other Gmail `juan@juanencripto.com` is secondary; rule 1 (`summary contains "nexo"`) would still catch a Nexostrat event if only that address were present.

2. **Doc-vs-code drift fixed in the same session that exposed it.** Initially proposed as a follow-up task; Ricardo authorized "fix them" at end-prep, so the amendment landed inline. Lesson: when drift is small, localized, and discovered during a task that depends on the corrected form, fix immediately rather than tracking.

3. **No recurring cache-refresh task.** Per Ricardo's directive "rely on commands" — `COMMANDS.md` "Calendar cache refresh" is the canonical procedure; no scheduled refresh gates anything until hub Phase 5 (P-H7) consumer lands.

4. **`brain-hub` on-disk path = `/home/ricardo/brain-hub/`, not `/srv/brain-hub/`** — confirmed by inspection + Ricardo. Multiple governance docs reference `/srv/brain-hub/`; this is a doc-vs-on-disk drift across master plan, Brain Hub contribution doc, deployment doc. Not fixed this session (out of P-H2 scope); flagged for a future audit pass.

## Stack state (live & verifiable next session)

```
/srv/Nexostrat/
├── calendar_cache.json                                ← NEW (this session, b03d3af)
├── 00_META/
│   ├── journal/
│   │   └── 2026-05-26_p-h2-calendar-cache.md         ← NEW
│   ├── calendar_filter.md                             ← MODIFIED (line 11 JP placeholder)
│   ├── governance/plans/
│   │   └── 2026-05-25_meetings-overhaul-contribution.md  (no edits this session)
│   ├── proposals/
│   │   └── 2026-05-26_tasks-v2-schema.md             ← shipped session 16 (784fcf2)
│   ├── audit/                                         ← shipped session 15 (2a5f272)
│   ├── templates/                                     ← shipped 2026-05-22 (b3bae45)
│   ├── calibration/                                   ← shipped 2026-05-22 (60669ed)
│   │   ├── auto_task_extraction.jsonl                 (scaffold; ≥50 rows still pending = P-N3)
│   │   └── README.md                                  (rubric)
│   └── inbox/
│       └── 2026-05-22_brain_bot_platform_action_items.md  (B14+B15 done; B19 open)
├── schedule.yaml                                       ← shipped 2026-05-22 (2fbca49)
├── tasks.json                                          ← MODIFIED session 16 (schema v2, fixture row, P-N1 closed)
├── COMMANDS.md                                         ← MODIFIED (Calendar cache refresh section)
├── STATUS.md                                           ← MODIFIED (seventeenth-session entry)
└── CHECKPOINT.md                                       ← THIS FILE (rewritten)
```

## Open items (this session's, ranked)

| ID | Subject | Priority | Due |
|---|---|---|---|
| `t-confidence-calibration-corpus` (existing B17 = P-N3 alias) | ≥50-row calibration labelling pass | high | 2026-06-22 |
| `t-meetings-overhaul-audit-dir` | P-N2 — stale OPEN status; work actually landed at commit `2a5f272` (session 15). Bookkeeping miss carried from session 16. | high | 2026-06-05 |
| `t-archive-bbp-action-items-memo` | Archive `00_META/inbox/2026-05-22_brain_bot_platform_action_items.md` once B19 closes | low | 2026-06-15 |

> **Note on `brain-hub` path drift:** master plan + Brain Hub contribution doc + deployment doc all reference `/srv/brain-hub/`; the live path is `/home/ricardo/brain-hub/`. Discovered this session, not fixed (out of P-H2 scope). No task added — recommend root run an audit pass to either move the directory or amend the docs, whichever Ricardo prefers.

## Open items (carried from prior sessions, unchanged)

`t-nexostrat-telegram-account` (B19, 2026-06-15), `t-weekend-desktop-on-decision` (B16, 2026-06-15), `t-plan-04-description-update` (2026-05-28), `t-plan-08-client-meeting-integration` (B18, 2026-07-15). Plus 3 intro-V3 polish tasks from session 14 (`t-intro-v3-ceo-vs-cofundador`, `t-intro-v3-diferencia-slide`, `t-intro-v3-web-export`) — `t-intro-v3-ceo-vs-cofundador` + `t-intro-v3-diferencia-slide` both due 2026-05-26 (today).

## Cross-scope context for next session

- **Phase 0a Nexostrat surface 2 of 3 done.** P-N1 (session 16) + P-N2 (session 15). P-N3 (calibration labelling) remaining, due 2026-06-22.
- **Phase 0c P-H2 done this session** (cross-scope contribution). Cache live; hub-side P-H7 (calendar dispatch loop) is the eventual consumer.
- **Phase 0c P-H1 + P-H6 remain open** (cross-scope, Brain Hub Principal owns). Nexostrat-side procurement gates: `t-nexostrat-telegram-account` (firm Telegram account, 2026-06-15) + firm DeepSeek key. Same items already in the task ledger.
- **Phase 0b AttenBot** (P-A2 → P-A3 → P-A1): P-A2 + P-A3 done (sessions late 2026-05-25); P-A1 implementation owned by Gemini at `/home/ricardo/atten-bot/`. Not blocking Nexostrat.
- **No Gemini handoff active.** `claude_to_gemini.md` + `gemini_to_claude.md` both `TEMPLATE` as of last check.

## What next session opens onto

Three plausible first moves:

1. **P-N3 calibration labelling pass** (~1 day labelling). Source: 4 existing meetings under `/srv/meetings/nexostrat/` (~20 candidate actions) + ~30 synthetic edge cases balanced across the four rubric tiers in `00_META/calibration/README.md`. Output: ≥50 NDJSON rows in `auto_task_extraction.jsonl` + `2026-05-XX_initial-corpus-report.md` with precision/recall at the 0.85 threshold. Closes the last Nexostrat-side Phase 0a prereq. Could parallelize via Gemini handoff if the rubric is followed strictly.

2. **Intro V3 polish** — `t-intro-v3-ceo-vs-cofundador` + `t-intro-v3-diferencia-slide` both due today (2026-05-26). Tiny DaVinci edits gated on a decision (CEO vs co-fundador title; Diferencia overlay present or drop-in needed).

3. **Janitor pass** — flip the stale `t-meetings-overhaul-audit-dir` task to `done` (P-N2 actually shipped at `2a5f272`); resolve + archive the BB-Platform action-items memo once `t-nexostrat-telegram-account` (B19) closes.

If Ricardo opens with "Start Session" next, surface P-N3 first (Phase 0a critical path) + intro-V3 polish (due-date pressure today) + the cross-scope flag that `/home/ricardo/brain-hub/` ≠ `/srv/brain-hub/` in governance docs (root may want to act on it).
