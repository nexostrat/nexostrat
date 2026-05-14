# Nexostrat — Master Plan Index (plain version)

> **What you're looking at:** the roadmap from design to launch.
> **Companion to:** [`README.md`](README.md) (the technical version with all the details)
> **The design itself lives in:** [`../proposals/2026-05-13_nexostrat-system-design.md`](../proposals/2026-05-13_nexostrat-system-design.md)

## What this is

We agreed on the architecture (the design spec). Now we need to actually build it. This file lists the **10 implementation plans** that, in order, take us from "scaffolded folders" to "first pilot client running, system live."

Think of the spec as the architectural blueprint of a house. This file is the **construction schedule**: foundation first, then framing, then roof, then plumbing, then electrical, then finishes. Each plan is one "phase of construction" and produces something that works on its own.

## How long this takes

Realistic total for one operator (Ricardo + Claude working together): **~7-9 weeks of calendar time**. Some plans can run partly in parallel. First income-eligible Diagnóstico after plan #7 (~3 weeks in). First client meetings after plan #8. System fully live after plan #10.

## The 10 plans, in plain words

| # | Plan | What you'll see at the end | How long |
|---|---|---|---|
| 01 | **Foundation** — folders, encryption keys, backups | A clean repo. Anyone can clone it. Everything sensitive is encrypted. If the laptop dies, we restore in 30 min. | ~1 week |
| 02 | **Documentation** — manuals JP and I can both read | An honest user manual (in `docs/`) with how-tos for every common task. Every doc has a plain-language partner. | ~3 days |
| 03 | **Events + Python agents** — the wiring under the hood | A log file that records everything the system does + Python programs that do the work + schedules them to run | ~1 week |
| 04 | **Telegram bot + Inbox** — the interface for JP and me | A working bot. You can `/note`, `/idea`, `/decision`, etc. and the bot files everything in the right place. Replies in your time zone. | ~1 week |
| 05 | **Skill 1 working end-to-end** — the first analyst skill | Run "analyze Bodai" → get an Aurora-branded PDF report. Works in 2 modes: manual (you drive Claude Code) or automatic (APIs do it for you). | ~1 week |
| 06 | **Skills 2-5** — the other four analyst skills | Industry analysis. Competitor analysis. Meeting script (your private prep doc). Opportunity report (the Diagnóstico we sell). | ~2 weeks |
| 07 | **Per-client production line** — chains all 5 skills for any client | One command (or one Telegram message) runs the full 5-skill chain on any client, with you reviewing between skills. | ~1 week |
| 08 | **Meetings** — record + transcribe + extract actions | Every meeting recorded. Transcripts in the repo. Action items go to tasks.json. Dates go to Google Calendar. Brief before each meeting. | ~1.5 weeks |
| 09 | **Chat extraction** — bot understands the Telegram group | Anything you and I say in the group that's a task/date/decision, the bot notices and asks us to confirm. No more lost messages. | ~3 days |
| 10 | **Launch** — observability + go-live checklist | Status dashboards. Daily brief at 7 AM. All emergency procedures written. Tag v1.0. First pilot can start. | ~3 days |

## How we work each plan

For each plan, when it's our turn to build it:

1. We open Claude Code at the Nexostrat folder.
2. Claude reads the spec + this index + the previous plan's results.
3. Claude writes the plan in full detail (specific tasks, 2-5 min each, with the exact commands).
4. We review the written plan.
5. We execute it — task by task, committing after each. We either:
   - **Subagent-driven** (recommended): Claude spawns a fresh "subagent" per task with no context contamination. Faster.
   - **Inline**: tasks run in our current session, batched. More hands-on.
6. When all tasks done: the plan is marked DONE. We move to the next one.

## Why we don't write all 10 plans in detail today

We considered it. The reason we don't:
- The architecture is already locked (in the spec). The plans are just "how we build it."
- Plans written 8 weeks before execution become silently wrong (tool versions change, we learn things from earlier plans, etc.).
- Writing a plan takes ~30 min when it's your turn. The pre-writing savings are illusory.
- What we *do* lock today: the **order**, the **dependencies**, and **what each plan delivers** — that's what this file does.

The only plan with full task-by-task detail today is **Plan 01** (it's ready to execute right now).

## Your role at each step

- **Ricardo:** the operator. Runs the commits, the manual steps, the final reviews.
- **Claude:** writes the tasks, executes the steps, commits when approved, asks before destructive actions.
- **JP:** reads the `-explicado.md` files (this one + each plan's plain partner). Approves at major checkpoints. Otherwise doesn't need to be in the loop day-to-day.

## What to do next

If you want to **start building right now:** open Plan 01 ([`2026-05-13_plan-01-repository-foundation-explicado.md`](2026-05-13_plan-01-repository-foundation-explicado.md)) and tell Claude "let's go." Plan 01 takes about a week.

If you want to **review first, build later:** read the plain version of Plan 01, then come back when you're ready.

If you want to **pick a different starting plan:** Plan 01 unblocks everything else, so it really is the right starting point.
