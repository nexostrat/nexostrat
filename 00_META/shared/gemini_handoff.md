## Gemini Handoff Protocol

File-based pattern. Claude is the director; Gemini is the second seat consulted for: web search and fresh-information lookups, adversarial audits, code/document review, alternative brainstorming.

**Files involved (lifecycle):**
- `00_META/handoff/claude_to_gemini.md` — Claude writes the ask. Status: `TEMPLATE` (idle) → `OPEN` (Gemini's turn) → `IN_PROGRESS` → `RESOLVED`.
- `00_META/handoff/gemini_to_claude.md` — Gemini writes the response. Status: `TEMPLATE` → `RESPONSE_READY`.
- `00_META/handoff/archive/YYYY-MM-DD_<slug>.md` — both files moved here once Claude has integrated.

**Raise a handoff (Claude's workflow):**
1. Tell the operator "this warrants Gemini because X."
2. Write `claude_to_gemini.md` with the ask. Set Status: `OPEN`.
3. Tell the operator the handoff is ready.
4. Continue other work; do NOT block on the handoff.

**Session-start check (Claude's workflow):**
1. If `gemini_to_claude.md` status is `RESPONSE_READY`: validate scope + edited-file constraint, validate content against sources where possible, integrate, archive both files to `00_META/handoff/archive/YYYY-MM-DD_<slug>.md`, record in STATUS.md Recent activity.

**Hard constraints:**
- Never edit `gemini_to_claude.md` directly (Gemini's file).
- Never commit Gemini's WIP while a handoff is `IN_PROGRESS`.
- Claude authors all `GEMINI.md` files; Gemini may NOT edit any `CLAUDE.md`.
