# 2026-05-26 — Meetings overhaul Phase 0c P-H2 (calendar cache populate + drift cleanup)

**Session type:** work (cross-scope contribution to Brain Hub Phase 0c)
**Duration:** ~1 hour (single-prompt deliverable, session 17)
**Agent:** Claude (Opus 4.7, 1M context, on `ricardo-hp-laptop` / server PC; Google Calendar MCP authenticated to `ricardomejiacaicedo@gmail.com`)

## What was done

- **Discovered brain-hub lives at `/home/ricardo/brain-hub/`** (not `/srv/brain-hub/` as the prompt and master-plan/hub-doc references implied). Ricardo confirmed the path mid-session. `hub.google.calendar_filter_nexostrat` imported cleanly from there; filter constant `FILTER_VERSION = "nexostrat-v1"`.
- **Confirmed JP's canonical attendee email** with Ricardo before any API call: `jpasistentepersonal@gmail.com` (one of two JP Gmail addresses — the other, `juan@juanencripto.com`, also appears in attendee lists but is not the primary). The placeholder `jp@example.com` in `00_META/calendar_filter.md` was stale; amended this session.
- **Fetched events 2026-05-25 → 2026-06-24** via the Google Calendar MCP. Two calendars accessible: `ricardomejiacaicedo@gmail.com` primary (10 events) + `en.spain#holiday@group.v.calendar.google.com` Holidays in Spain (3 events). 13 total upstream.
- **Applied `nexostrat_filter(event, jp_email)` from the brain-hub module.** Per-event injected `source_calendar = <calendar summary>` before the call (Google's API doesn't return that field; the filter's rule 2 needs it to evaluate). Per-event `match` rationale captured.
- **Filter result: 9 / 13 matched.** All 9 matches via `summary_contains_nexo` (rule 1) — the recurring `Nexostrat` weekly events also satisfy `jp_email_in_attendees` (rule 3) but rule 1 short-circuits first. `Trixx Logistics - Ricardo Mejía` (1 event) and the 3 Spain holidays (Whit Monday, Corpus Christi, Saint John the Baptist Day) correctly dropped.
- **Wrote `/srv/Nexostrat/calendar_cache.json`** per master plan §6.2 P-H2 + Brain Hub contribution doc §3 P-H2 contract. Schema: `generated_at` (ISO-8601 UTC), `generated_by: "claude@desktop"`, `filter_applied: "nexostrat-v1"`, `stale_after_hours: 24`, `events[]` with upstream fields (`id, summary, start, end, attendees, location, description`) plus injected `source_calendar` and `match`.
- **Amended `COMMANDS.md`** with a new "Calendar cache refresh" section between Periodic operations and Vault. Documents the source-of-truth references, cache schema table, 4-step refresh procedure (run Claude on a PC with Google Calendar MCP authenticated; ask in `/srv/Nexostrat/` for refresh; verify with a `jq` one-liner), fallback path (hand-author for demo only), and migration trigger (firm-owned Google account flips `filter_applied` to `nexostrat-noop-firm-account-v1`).
- **Master plan §6.2 P-H2 checkbox ticked** + **§7.1 done-row appended** (Brain repo `9b5d8ba`).
- **Nexostrat repo commit `b03d3af`** pushed to Gitea origin (mirrors fire via systemd path-watcher to GitHub + Codeberg).
- **Drift cleanup pass after Ricardo's mid-session "fix them" authorization:** amended `nexostrat_v1` (underscore) → `nexostrat-v1` (hyphen) in master plan §6.2 P-H2 row + done-criterion (lines 435 + 439) and Brain Hub contribution doc §3 P-H2 (lines 85 + 89). Verified no `nexostrat_v1` strings remain in master plan, Brain Hub doc, Nexostrat contribution doc, or `00_META/calendar_filter.md`. Correction logged in §7.1: the prior row at line 628 asserted Nexostrat contribution doc carried the underscore form, which was false — drift was master-plan + Brain-Hub-doc only.
- **`00_META/calendar_filter.md` line 11 amended** — placeholder `jp@example.com` → `jpasistentepersonal@gmail.com` with attribution to Ricardo's 2026-05-25 confirmation.

## Decisions made

- **JP email = `jpasistentepersonal@gmail.com`** (per Ricardo's explicit confirmation, mid-session, when faced with a 3-option AskUserQuestion). This is the canonical attendee identifier for the filter's rule 3 going forward. JP's other Gmail `juan@juanencripto.com` is not the primary; if it ever appears alone on a Nexostrat-relevant event, rule 1 (`summary contains "nexo"`) will likely still catch it.
- **Doc-vs-code drift fixed during the same session that exposed it.** Initially flagged the `nexostrat_v1`/`nexostrat-v1` mismatch as a follow-up task; Ricardo authorized "fix them" so the amendment landed inline. Lesson: when a drift is small, localized, and discovered during a task that depends on the corrected form, fixing it immediately is cheaper than tracking it.
- **No new task added for next cache refresh.** Per Ricardo's session-end directive "rely on commands" — the `COMMANDS.md` "Calendar cache refresh" section is the canonical procedure; no scheduled refresh task. Hub Phase 5 (P-H7) consumer isn't wired yet, so cache staleness has no functional impact until that loop lands.
- **Defensive default honoured.** The filter's "drop on missing fields" rule is the right call — 0 holidays leaked despite none having attendees lists.

## Surprises

- **`brain-hub` is at `/home/ricardo/brain-hub/`, not `/srv/brain-hub/`.** Master plan, deployment doc, and Brain Hub contribution doc all reference `/srv/brain-hub/`. The live path is the user's home directory. This is a doc-vs-on-disk drift across multiple governance artifacts; left untouched this session (not part of the P-H2 scope), but worth root noting for a future audit pass.
- **Both `replace_all` Edit calls on the master plan succeeded silently on different patterns than expected.** The first `replace_all` on `` `filter_applied: "nexostrat_v1"` `` (backtick-delimited token) only matched the §7.1 row I'd authored myself (which used backticks around just the field), not the §6.2 P-H2 row (which has the underscored form inside a wider backtick block surrounding the full schema). Fixed with a second non-backtick Edit. Editing rule: prefer larger anchor strings when the target sits inside a Markdown code span.
- **No "Nexostrat" sub-calendar exists on Ricardo's account.** Only the primary + Holidays in Spain. Rule 2 (`source_calendar == "Nexostrat"`) is therefore dormant today; rules 1 + 3 carry the load. When the firm-owned Google account lands per `calendar_filter.md` § Migration trigger, the whole-account-is-Nexostrat assumption removes the filter entirely.

## Next session

- **Phase 0a P-N3** — ≥50-row calibration labelling at `00_META/calibration/auto_task_extraction.jsonl` (aliases existing `t-confidence-calibration-corpus` task, due 2026-06-22). Last Nexostrat-side prereq for Phase 0 close-out.
- **No P-H2-related follow-up** — the cache is populated, COMMANDS.md procedure is the refresh interface, drift is cleaned. P-H2 is fully closed.
- **Hub-side P-H1 + P-H6 remain open** but are cross-scope (Brain Hub Principal owns); Nexostrat's surface there is the procurement gate (firm Telegram account `t-nexostrat-telegram-account` due 2026-06-15 + firm DeepSeek key) — same items already in the Nexostrat task ledger.

## Verification (end of session)

```
$ jq -r '.filter_applied, .generated_at, .stale_after_hours, (.events | length)' /srv/Nexostrat/calendar_cache.json
nexostrat-v1
2026-05-26T02:59:01Z
24
9

$ grep -rn 'nexostrat_v1' /srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md \
                          /home/ricardo/brain-hub/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md \
                          /srv/Nexostrat/00_META/calendar_filter.md
(no output)
```

Both green.
