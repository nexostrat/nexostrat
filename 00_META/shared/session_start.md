## Session Start Protocol

Claude Code is turn-based — Claude never speaks first. Triggered by Ricardo (or JP) writing "Start Session" / "Begin Session" / similar opening phrase.

On the trigger:
1. Read this persona's `CHECKPOINT.md` — the baton from last session.
2. Read this persona's `STATUS.md` — current state, blockers, next milestone.
3. Read root `tasks.json` — what's open, in-progress, blocked, due.
4. Read root `calendar.json` — upcoming deadlines.
5. Read the most recent file in this persona's `00_META/journal/` — last session's narrative.
6. Read this persona's `00_META/inbox/` (via `infra/scripts/nexostrat-memos.py`) — surface unresolved memos addressed to this persona.
7. Summarize per § Session Output Format below, ending with *"What would you like to work on?"*
8. `git pull` if upstream is reachable (skip silently if not).
9. Run `infra/scripts/checkpoint-mtime-check.sh` — warn if CHECKPOINT.md was modified within the last 10 minutes by another process (R4 concurrent-session protection).
