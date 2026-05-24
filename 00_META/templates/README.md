# Nexostrat brief templates

Read at render-time by the hub's brief plugin (`hub.plugins.meetings.brief`). Edits apply at the next fire — **no deploy needed**. Source-of-truth for what each block means; the renderer is dumb (variable substitution only).

## Schedule (per /srv/Nexostrat/schedule.yaml)

| Template | Cron | Source schedule id | Audience |
|---|---|---|---|
| `morning_brief.md` | `30 7 * * *` daily | `nexo-morning-brief` | Ricardo + JP DMs |
| `weekly_review.md` | `0 19 * * 0` Sun TJ | `nexo-weekly-review` | Ricardo DM |
| `eow_pipeline.md` | `0 17 * * 5` Fri TJ | `nexo-eow-pipeline` | Ricardo DM |
| `inbox_sweep.md` | `0 18 * * *` daily | `nexo-inbox-sweep` | Ricardo DM |
| `pre_meeting_brief.md` | dynamic (T-2h before each meeting) | scheduled per `meeting.summary_ready` event | Ricardo + JP DMs |
| `t_20m_agenda.md` | dynamic (T-20m) | same | Nexostrat group |
| `t_1h_reminder.md` | dynamic (T-1h) | same | Nexostrat group |

## Variables — where each block's data comes from

| Variable | Data source | Notes |
|---|---|---|
| `{{meeting_title}}` | event payload | from `metadata.yaml meeting_id` |
| `{{meeting_time}}` | event payload | local TJ time |
| `{{last_recap}}` | `meetings/<prev_slug>/summary.md` | "Decisiones" + "Acciones" sections, truncated to 8 bullets max |
| `{{pending_tasks}}` | `tasks.json` | `status=open AND owner IN [ricardo, jp]`, sorted by priority desc → due asc; max 6 |
| `{{chat_items}}` | `groups/<chat_id>/extractions/<yesterday>.md` | Action items section |
| `{{attendance_yn}}` | inline keyboard widget | `[Y]` `[N]` buttons for each invitee — rendered live by the brief plugin |
| `{{open_memos}}` | `brain_memos.py --to nexostrat`-equivalent | Nexostrat-internal inboxes |
| `{{pipeline_state}}` | `pipeline/clients/*/state.json` | one line per client: slug · phase · last gate event |
| `{{cache_age_warning}}` | `calendar_cache.json` mtime | "⚠ {{N}}h stale, run claude to refresh" when > 24h |
| `{{top_tasks_per_founder}}` | `tasks.json` | top 3 per `owner ∈ {ricardo, jp}`, same sort as block 2 |
| `{{todays_meetings}}` | `calendar_cache.json` | events for today's date, after the v1 filter |
| `{{stale_memos}}` | inbox scan | memos with `created` older than 48h, addressee=ricardo or jp |
| `{{quick_recap_one_line}}` | `meetings/<prev_slug>/summary.md` | first decision bullet |
| `{{agenda_topics}}` | computed | past 7 days of extractions + last meeting's open items, deduped |
| `{{week_start}}` | computed | Monday of the rendered week |
| `{{week_body}}` | weekly-review skill | the actual review content, written by the skill |
| `{{per_client_one_liner}}` | `pipeline/clients/*/state.json` | one client per line, phase + last gate event |
| `{{date}}` | computed | local TJ date, `YYYY-MM-DD` |

## Editing checklist

1. Make the change.
2. Commit + push (this `Nexostrat` repo — **NOT** the `brain-hub` repo).
3. Hub picks up the new template on the next scheduled fire (no restart needed).

## Missing-variable behaviour

The renderer (`hub.plugins.meetings.brief.plugin.render_brief`) substitutes `{{var}}` placeholders and **preserves the literal `{{var}}` when a key is missing from the BriefContext**. This is intentional — a template typo or a renamed variable surfaces visibly in the rendered output rather than silently dropping a section. The renderer is unit-tested at `/srv/brain-hub/tests/test_meeting_brief_renders.py`.

## Audit B5 traceability

The template + data-source mapping above is the audit B5 deliverable: every block in the pre-meeting brief traces to a deterministic data source. No LLM at fire-time (the group-chat extraction block is **pre-computed** at the previous evening's 19:30 run by `hub.plugins.groups.extractor`).
