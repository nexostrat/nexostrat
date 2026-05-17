## Session End Protocol

Triggered by Ricardo (or JP) writing "End Session" / "Prepare for session termination" / "Finish Session" / similar close phrase.

**Step 1 — Claude, on close phrase:**
1. 2-4 sentence prose summary of what this session accomplished.
2. Bulleted list of every file that will be written at session end.
3. Pending-items table with proposed priority + due date + rationale; ask the operator to confirm/amend.
4. Disambiguation questions only if truly blocking.

**Step 2 — Operator confirms.**

**Step 3 — Claude applies everything:**
1. Update this persona's `STATUS.md`.
2. Update root `tasks.json` (close completed; add new with priorities/dates).
3. Update root `calendar.json` if any deadlines changed.
4. Write journal entry at `00_META/journal/YYYY-MM-DD_<topic>.md`.
5. Update root `00_META/CHANGELOG.md` if any context file (CLAUDE.md, GEMINI.md, README.md) was edited.
6. Rewrite this persona's `CHECKPOINT.md` baton for the next session.
7. If work remains for Gemini, write handoff in `00_META/handoff/claude_to_gemini.md`.
8. If a memo is needed for another persona, write to `<target>/00_META/inbox/YYYY-MM-DD_HHMM_<from>_<topic>.md` per § Cross-Folder Memo Protocol.
9. `git add` + `git commit` + `git push origin main` (manual via Bash tool — no Stop hook yet; Plan 06 may automate).

**Step 4 — Operator writes "Finish Session" or closes the conversation.**
