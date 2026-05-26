# 2026-05-25 — Meetings Pipeline Overhaul: Nexostrat §8 Contribution Doc

> **Session:** 15 (standalone — distinct from session 13/14 V3-production day)
> **Persona:** Founder
> **Driver:** Ricardo (single prompt with reading list + §8 template target)
> **Working dir:** `/srv/Nexostrat/`
> **PC:** `ricardo-desktop`
> **Duration:** ~25 minutes wall

## The ask

Single-prompt session. Ricardo asked: read the cross-scope meetings-pipeline overhaul master plan at `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`, read this scope's state, and file the Nexostrat contribution doc per the master plan's §8 template at `/srv/Nexostrat/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md`. Commit + push. Append a row to master plan §7.1.

The §8 template asks for: current architectural state, alignment check, prereqs, what this scope adds, what it needs from others, reviewer, notes for root. Reading order was prescribed: master plan §1 + §2.3 + §2.4 + §4 + §6.6 + §6.7, then scope state.

## What happened

### Round 1 — read + draft

Read the master plan end-to-end (685 lines). Read `/srv/Nexostrat/CLAUDE.md`, peeked at `tasks.json` (76 tasks, schema `nexostrat-tasks-v1`), checked the contents of `00_META/`, `pipeline/clients/`, `Pilotos/`. Spotted that the master plan §6.6 step 4.7 references a calibration corpus at `/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl` — the directory did not exist locally. Read the meetings curator's contribution doc (`/srv/meetings/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md`) for tone reference.

Wrote the first draft listing **5 prereqs** (P-N1 schema v2, P-N2 audit dir, P-N3 calibration corpus, P-N4 brief templates, P-N5 calendar filter). Committed as `8ed90e5` ("governance: file Nexostrat contribution doc for meetings pipeline overhaul").

### Round 2 — push rejected, pull, correct

`git push origin main` rejected — "Updates were rejected because the remote contains work that you do not have locally." Fetched: origin had **7 commits ahead** of local (`748b9a3..a1bff0c`). The new tip was `a1bff0c Merge branch 'main'`, with these commits underneath:

```
60038e8 adr: ADR-039 (PROPOSED) — Nexostrat bot runs as tenant in Brain Bot Hub
516681a inbox: brain-bot-platform action items memo (B14 + B15 + B19; Task 6.7)
60669ed calibration: corpus scaffold + rubric (audit B17)
b3bae45 templates: brief templates as separate markdown + README (audit B5)
32e493f calendar filter v1 — Nexostrat-relevance rule (audit B7)
2fbca49 schedule.yaml: 4 nexostrat entries (audit B11)
```

These are commits from the **2026-05-22 BB-Platform action-item sweep** that landed on server-side but hadn't reached desktop until just now. The merge commit `a1bff0c` is the same one the meetings-overhaul root audit referenced in §7.1 ("Per Ricardo's authorization to take the incoming version, Nexostrat re-merge…"). So origin was always going to win this rebase.

Rebased local on top (`git pull --rebase origin main`). Then verified what those 7 commits actually shipped:

| Commit | Path | Shipped? |
|---|---|---|
| `b3bae45` | `00_META/templates/` | **YES** — 7 brief templates (3 dynamic per-meeting + 4 cron-scheduled) + README documenting each variable's data source in plain English. P-N4 in draft was already done. |
| `32e493f` | `00_META/calendar_filter.md` | **YES** — v1 filter rule, references hub-side reference impl at `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py::FILTER_VERSION`. P-N5 in draft was already done. |
| `60669ed` | `00_META/calibration/` | **PARTIAL** — `auto_task_extraction.jsonl` exists with a single `_comment` row + `README.md` carrying the four-tier confidence rubric. Scaffold + rubric done; the ≥50-row labelling pass still pending. P-N3 in draft narrowed to just the labelling. |
| `2fbca49` | `/srv/Nexostrat/schedule.yaml` | **YES** — 4 cron entries for non-meeting briefs (morning, weekly review, eow pipeline, inbox sweep). NEW finding — I hadn't included this in the first draft at all. |
| `516681a` | `00_META/inbox/2026-05-22_brain_bot_platform_action_items.md` | **OPEN MEMO** — tracks B14/B15 (both done) + B19 (still open). First draft claimed inbox was empty. |
| `60038e8` | `00_GOVERNANCE/adr/ADR-039-…` | An older PROPOSED draft of ADR-039 from the merge stream. The currently-ratified Accepted version (2026-05-21) is what governs. Tidy-up commit pending but not blocking. |

Rewrote the contribution doc (`5dcc20e`, 93 insertions / 88 deletions). Net remaining prereq surface narrowed **from 5 to 3**: P-N1, P-N2, and the calibration labelling pass (which aliases the existing `t-confidence-calibration-corpus` B17 task — should not be double-tracked). Acknowledged `schedule.yaml`, the inbox memo, and the older ADR-039 PROPOSED commit. Pushed.

### Round 3 — master plan §7.1 row

Edited `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md` §7.1 to append the standard `[date] session@pc | phase.step | action | evidence` row. Brain commit `4bda2b3`, pushed.

## Findings worth recording

1. **`owner` vs `assignee` mismatch.** Inside this scope, the brief templates' README (shipped 2026-05-22, commit `b3bae45`) documents reads using a field called `owner` (e.g., `status=open AND owner IN [ricardo, jp]`). Brain Bot Platform §8 uses `assignee`. The existing `nexostrat-tasks-v1` schema has **neither** — only `subject`. P-N1 (schema v2) needs to pick one and accept the other as alias. The contribution doc lands `owner` as canonical with `assignee` accepted.

2. **Stale local state is real.** Desktop hadn't been pulled since session 14 ended (~3h ago in wall time), and the 2026-05-22 BB-Platform sweep had merged into origin earlier today via the meetings-overhaul root audit's `H7-final` step (master plan §7.1 row at 17:45). The lesson: when filing a cross-scope contribution doc, **`git pull` BEFORE drafting**, not after. Saved as memory? Not yet — this is more about session-start hygiene than a behavioral preference; the existing session-start protocol already mandates `git pull if upstream is reachable`. Treat as a one-time reminder of why that step matters.

3. **P-N3 ≡ existing B17 task.** The contribution doc and `tasks.json::t-confidence-calibration-corpus` describe the same line item (≥50-row calibration corpus). Phase 0a should treat them as one deliverable, not two. Updated the B17 task's `notes` field at session end to make the alias explicit.

4. **Architectural pre-alignment is high.** All 9 master-plan §2/§4 points line up with Nexostrat's ratified state (ADR-039 + the 2026-05-22 sweep). No master-plan amendments needed from this scope; this is the cleanest contribution doc of the four (versus the meetings-curator doc, which flagged 6 intentional master-plan overrides).

## Output artifacts

- `/srv/Nexostrat/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md` (this is the deliverable)
- `/srv/Nexostrat/00_META/governance/` (new directory)
- `/srv/Nexostrat/00_META/governance/plans/` (new directory)

## Commits

- `8ed90e5` — initial draft (superseded but kept in history per CLAUDE.md "Prefer to create a new commit rather than amending an existing commit")
- `5dcc20e` — corrected version reflecting actual on-disk state
- `4bda2b3` (Brain repo) — §7.1 row append in master plan

## Sessions 13/14 collision check

Session 14's write surface (`operations/marketing/website-intro/`) is fully orthogonal to this session's write surface (`00_META/governance/plans/`). No collision, no clean-up needed.

## Next session opens onto

Phase 0a execution: P-N1 + P-N2 co-commit (schema v2 + audit dir, ≤2.5h total), then P-N3 calibration labelling can run as a separate parallel pass against the 2026-06-22 deadline. See CHECKPOINT.md for the baton.
