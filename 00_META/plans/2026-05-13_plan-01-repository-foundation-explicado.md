# Plan 01 — Repository Foundation (plain version)

> **What you're looking at:** the implementation plan for the first phase of building Nexostrat.
> **Companion to:** [`2026-05-13_plan-01-repository-foundation.md`](2026-05-13_plan-01-repository-foundation.md) (the technical version with every command).
> **For:** Ricardo (operator), JP (reviewer at major checkpoints).

## What this plan does

Builds the **foundation** of the company's brain: folders, security (encryption keys), backups, and the rules of who-talks-to-what (the persona files).

When this plan is done, you have:
- A clean, organized repository with three "buckets" (Skills, Pipeline, Operations) plus governance.
- Encryption keys (`age`) that protect all sensitive content. Each person has their own key; either can decrypt the vault.
- A secrets file (API keys, tokens) that's encrypted on disk and only decrypted into RAM when a service needs it. Never sits in plaintext on disk.
- A **backup ladder** with 7 layers: working copy → Gitea (local server) → GitHub (off-site mirror) → Codeberg (later) → warm-standby laptop (nightly sync) → Drive (heavy assets) → NAS (local backup of Drive). If any layer fails, four others have the data.
- A **warm-standby**: a second laptop that's set up identically to the main HP server, idle. If HP dies, you SSH into the standby, start the services, and you're back in 15-30 minutes.
- The **personas**: Claude has 3 "personas" depending on which bucket you're working in (Founder at root, Skills-Master at `skills/`, Client-Owner at `pipeline/`). Each has its own CLAUDE.md file and its own GEMINI.md (second-seat) file. JP reads `-explicado.md` partners for the user-facing ones.
- A **smoke test** that checks all 30+ things at once and tells you "green" or "red." When it's green, the foundation works.

This plan does NOT yet build: the Telegram bot, the Python agents, the skill pipelines, the meeting capture, etc. Those come in plans 02-10.

## How long it takes

**~1 week** of calendar time for one operator (Ricardo + Claude working together, ~1-2 hours/day). The plan has **28 tasks** with ~120 small steps total. Each step is 2-5 minutes of work.

## How it works (the order)

The plan has 12 phases. Each phase is a logical chunk; each phase has 1-4 tasks; each task has several steps.

| Phase | What | Why |
|---|---|---|
| **A. Verify state** | Check we're starting from a clean repo with correct git author. | One bad assumption can cascade. |
| **B. Folder scaffold** | Create the 3 bucket folders + cross-cutting folders. | Everything that follows lives in one of these. |
| **C. Root governance** | Write README, STATUS, CHECKPOINT, .gitattributes, docker-compose placeholder. | These are the "front door" files anyone reads first. |
| **D. Identity (age keys)** | Generate Ricardo's encryption keypair. Set up the vault structure. | Without keys, we can't protect anything sensitive. |
| **E. Secrets workflow** | Create the encrypted secrets file + a wrapper script that decrypts it into RAM only at use time. | API keys never touch disk in plaintext. |
| **F. GitHub mirror** | Push to GitHub automatically on every commit. | Off-site backup #1. |
| **G. Warm-standby** | Configure a second laptop to receive a nightly copy of everything. | If HP dies, recovery in 30 min. |
| **H. Shared stanzas** | Write the canonical short blocks of text that every persona inlines. | One source of truth; persona files inline them. |
| **I. Persona files** | Write the 3 CLAUDE.md and 3 GEMINI.md files. | The rules each persona operates by. |
| **J. Per-machine profiles** | Write a YAML file per machine declaring what should be installed. | Bootstrap script reads these to set up any machine. |
| **K. Pre-commit hooks** | Block plaintext secrets from being committed. | The first defense against accidental leaks. |
| **L. Smoke test + finalize** | Run all 30+ checks; if green, tag the repo `v0.1-foundation`. | "Done" has a definition. |

## Decisions you'll need to make during execution

Three points where Claude will pause and ask:

1. **Warm-standby host:** which of your laptops becomes the standby? (Task 14)
2. **GitHub username + repo name:** what should the mirror repo be called? (Task 11)
3. **JP's age key:** is JP available to generate one now, or do we defer to Heavy mode? (Task 7)

Recommended answers: standby = your travel laptop or a spare; GitHub repo = `nexostrat` (private); JP key = defer to Heavy mode (vault encrypted to Ricardo only with a follow-up memo to add JP later).

## What "done" looks like

The plan defines its own definition of done at the bottom. Short version:

- ✅ Smoke test green (`infra/scripts/smoke-test.sh` returns "all 30+ checks PASS")
- ✅ Repo tagged `v0.1-foundation` on Gitea AND on GitHub
- ✅ A test commit with a planted fake API key is blocked by the pre-commit hook (we verify this manually)
- ✅ A test push to origin shows up on GitHub within seconds (we verify this manually)
- ✅ The warm-standby laptop has the latest rsynced state of HP (we verify this manually)
- ✅ STATUS.md reads "Plan 01 DONE"

If any of these is red: STOP. We don't move to Plan 02 until the foundation is solid. This is what "Boring but Robust" looks like.

## What's at stake

This is the only plan where we **cannot afford to be sloppy**, because every later plan assumes this foundation works. A bug here surfaces 6 weeks later in a way that's hard to diagnose. We're slow and careful in Plan 01 so we can be fast and trusting in Plans 02-10.

Specifically:
- If we mess up the age keys → vault unreadable, recovery painful.
- If we mess up the GitHub mirror → no off-site backup, single point of failure.
- If we mess up the warm-standby → no recovery target if HP dies.
- If we mess up the hooks → an accidental secret commit leaks API keys publicly.

The 28 tasks are spread across these areas in proportion to risk.

## Your role during execution

Ricardo, you:
- Approve key decisions (the 3 listed above + anything Claude flags).
- Make the manual commits (Claude proposes; you approve and run).
- Read what Claude outputs and challenge anything unclear.
- Run the smoke test at the end and verify it returns green.
- Tag the repo `v0.1-foundation` (the final symbolic act of "Plan 01 done").

JP, you:
- Sit out Plan 01 (it's pure infrastructure setup; nothing client-facing).
- When Plan 02 starts, you'll see the user manual taking shape — that's when your input matters most early on.
- Approve the brand top-5 vote (separate task, due 2026-05-14) so we can lock the brand fully before client-facing work in Plan 06+.

## What comes after

Plan 02 — Documentation System. Writes the user manual (this file is a tiny preview of the doc style). Adds the paired-files drift hook. Writes all 15 new ADRs as durable decisions. Then Plan 03 (events + Python agents), Plan 04 (Telegram bot), Plan 05 (first skill end-to-end). Full roadmap at [`README-explicado.md`](README-explicado.md).

## When you want to start

Tell Claude "let's start Plan 01" (or "let's execute Plan 01"). Claude opens the technical plan file, picks execution mode (subagent-driven, recommended, or inline), and starts at Task 1.
