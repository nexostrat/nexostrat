# Plan 01c — Personas + hooks + integration test

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **For humans:** plain-language partner (`-explicado.md`) deferred to execution-start.

**Goal:** Instantiate the three persona CLAUDE.md/GEMINI.md files (Founder, Skills-Master, Client-Owner) from canonical shared stanzas via an inliner script, populate the pre-commit hook surface, and prove the whole foundation works end-to-end via a rich integration smoke test. After 01c, `v0.1-foundation` is tagged — the original Plan-01 milestone reached at the end of the 3-plan split.

**Architecture:** The persona pattern uses **canonical shared stanzas** at `00_META/shared/*.md` (rule1, session_start, session_end, session_output_format, memo_protocol, gemini_handoff, vault_access, backup_posture, change_log) inlined into each persona file via a small Python script (C3 fix). Drift detection runs the same script in `--check` mode. The pre-commit hook surface gains 4 small scripts on top of the basic secret-scan from Plan 01a. The integration smoke test (R2) is the rich version: 6 sub-tests covering crypto + git + rsync + leak + drift + schema, all required to pass before tagging.

**Tech Stack:** Python 3 (stdlib only — no extra deps for the inliner/memos scripts), bash, age (encryption), git, systemd (existing units).

**Plan-level success criteria:**
- `infra/scripts/inline_includes.py --check` reports zero drift across all 6 persona files.
- `infra/scripts/smoke-test.sh` returns green in <3 min; every sub-test prints a clear pass/fail line.
- A test edit to `00_META/shared/session_start.md` followed by re-running the inliner regenerates all 6 persona files with the new content; `git diff` shows the expected change in each.
- Pre-commit hook surface refuses planted violations (secret prefix, vault non-`.age` file, modified tier-1 doc without partner, CHECKPOINT.md without `CHECKPOINT_NO_ACTIVE_WORK` token when otherwise empty).
- Repo tagged `v0.1-foundation`.

**Spec references:** §4 (Personas + protocols — full section), §4.6 (docs-pair hook), §4.7 (cross-folder memo protocol), §4.10 (CHECKPOINT + concurrent-session protection per R4), §4.11 (Unified inbox — files only; Telegram is Plan 04), §10.1 (smoke test layer). ADRs 008 (hooks), 011 (personas), 014 (docs-pair), 025 (two-tier docs), 029 (Python over n8n), 031 (CHECKPOINT), 036 (Stage 1 surface area).

**Audit-finding inheritance:** F8 (`nexostrat-memos.py`), F10 (vault namespace split — applied in persona scope sections), F18 (persona ownership table — resolved by F10), F20 (BRAIN_STATUS / 00_TEMPLATES leaks audited out), F27 (Hosted-option follow-through — STATUS.md template doesn't reference it), C3 (inliner script), R2 (rich smoke test), R4 (CHECKPOINT concurrent-session check).

**Coordination gates:** None. JP coordination resolved in 01a. Plan 01b standby host already provisioned. Plan 01c is unblocked once 01b is tagged.

---

## File Structure

**Created in this plan:**

```
/srv/Nexostrat/
├─ 00_META/
│   ├─ shared/                                                      (CREATED — canonical stanzas)
│   │   ├─ rule1.md
│   │   ├─ session_start.md
│   │   ├─ session_end.md
│   │   ├─ session_output_format.md
│   │   ├─ memo_protocol.md
│   │   ├─ gemini_handoff.md
│   │   ├─ vault_access.md
│   │   ├─ backup_posture.md
│   │   ├─ change_log.md
│   │   └─ STATUS.md                                                (template; F27 — no Hosted refs)
│   └─ inbox/                                                       (.gitkeep — Founder's memo inbox)
│
├─ skills/
│   ├─ CLAUDE.md                                                    (CREATED — Skills-Master persona)
│   ├─ GEMINI.md                                                    (CREATED — Claude-authored)
│   ├─ CHECKPOINT.md                                                (CHECKPOINT_NO_ACTIVE_WORK)
│   └─ 00_META/inbox/                                               (CREATED — Skills-Master memo inbox)
│
├─ pipeline/
│   ├─ CLAUDE.md                                                    (CREATED — Client-Owner persona)
│   ├─ GEMINI.md                                                    (CREATED — Claude-authored)
│   ├─ CHECKPOINT.md                                                (CHECKPOINT_NO_ACTIVE_WORK)
│   └─ 00_META/inbox/                                               (CREATED — Client-Owner memo inbox)
│
├─ CLAUDE.md                                                        (REGENERATED via inliner — Founder root)
├─ GEMINI.md                                                        (REGENERATED via inliner — Founder root)
│
├─ infra/
│   ├─ scripts/
│   │   ├─ inline_includes.py                                       (CREATED — C3 fix)
│   │   ├─ nexostrat-memos.py                                       (CREATED — F8)
│   │   ├─ checkpoint-mtime-check.sh                                (CREATED — R4)
│   │   ├─ smoke-test.sh                                            (CREATED — R2 rich version)
│   │   └─ test_inliner.sh                                          (CREATED — TDD test for inliner)
│   └─ hooks/
│       ├─ pre-commit-secret-scan.sh                                (already exists from 01a)
│       ├─ pre-commit-vault-age-only.sh                             (CREATED)
│       ├─ pre-commit-docs-pair.sh                                  (CREATED — basic; full surface Plan 02)
│       ├─ pre-commit-checkpoint.sh                                 (CREATED)
│       └─ pre-commit                                               (REPLACED — orchestrates the 4 sub-hooks)
│
└─ STATUS.md                                                        (MODIFIED if needed — F27 sweep)
```

---

## Pre-flight checks (before Task 1)

- [ ] **Confirm Plan 01a + 01b tags both exist**

```bash
git tag | grep -E 'v0\.1[ab]'
# Expected: v0.1a-foundation  v0.1b-mirrors-only
```

If either is missing, STOP — preceding plans not complete.

Note: `v0.1b-mirrors-only` is the post-mirror-cluster interim tag (Plan 01b
Tasks 1-6). The warm-standby cluster (Tasks 7-12) is gated on a physical
second host (`t-plan-01b-execute-warm-standby`, due 2026-06-30) and will
land later as `v0.1b-mirrors`. Plan 01c can complete at the `mirrors-only`
baseline — sub-test [3/6] in the integration smoke test (Task 10) auto-SKIPs
the warm-rsync trigger when the unit isn't installed.

- [ ] **Confirm working tree is clean and pushed**

```bash
git status --short && git log origin/main..HEAD
# Expected: empty for both
```

- [ ] **Confirm Python 3 stdlib has what's needed (no extra deps)**

```bash
python3 -c "import re, pathlib, sys, json; print('stdlib OK')"
# Expected: stdlib OK
```

---

## Task 1: Canonical shared stanzas + F20 leak audit

**Goal:** Create `00_META/shared/*.md` with the canonical short-form content for each persona-file section. Each stanza is leak-free (no `/srv/brain`, `BRAIN_STATUS`, `00_TEMPLATES/` references). F20 audit folded into the writing pass.

**Files:**
- Create: `00_META/shared/{rule1, session_start, session_end, session_output_format, memo_protocol, gemini_handoff, vault_access, backup_posture, change_log, STATUS}.md`
- Create: `00_META/inbox/.gitkeep`

- [ ] **Step 1: Create 00_META/inbox/ + .gitkeep**

```bash
mkdir -p /srv/Nexostrat/00_META/inbox/archive
touch /srv/Nexostrat/00_META/inbox/.gitkeep \
      /srv/Nexostrat/00_META/inbox/archive/.gitkeep
```

- [ ] **Step 2: Write `00_META/shared/rule1.md`**

```markdown
**Folder-scope discipline.** Each persona's primary write scope is its own folder. When Ricardo is in-session driving, small obvious cross-persona edits are fine. **Heuristic:** if the cross-persona edit takes more than a sentence to explain, defer to that persona's session — route via memo to the appropriate persona inbox instead. Vault namespaces (per ADR-003 + F10) stay strictly isolated regardless: Founder owns `vault/{partnership,legal,accounting,keys}/`; Client-Owner owns `vault/clients/<slug>/`; Skills-Master owns no vault content. Reading anywhere within `/srv/Nexostrat/` is always permitted. (JP-Light per ADR-021bis has no session-driving surface at Stage 1 — Telegram + email + future FOSS dashboard only. If JP later flips to Heavy, that flip lands as an ADR and this stanza updates.)
```

- [ ] **Step 3: Write `00_META/shared/session_start.md`**

```markdown
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
```

- [ ] **Step 4: Write `00_META/shared/session_end.md`**

```markdown
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
```

- [ ] **Step 5: Write `00_META/shared/session_output_format.md`**

```markdown
## Session Output Format

The session-start brief and session-end Step 1 follow this format:

- **Session Start — 5-bullet brief.** Up to 5 bullets, bold label + concise content; omit empty bullets (no padding). Bullet order: (1) OVERDUE / critical-imminent in this scope, (2) Pending handoffs / inbox memos, (3) In-progress work, (4) Pending verifications / next milestone, (5) Flag (anything that doesn't fit but matters). End with: *"What would you like to work on?"*
- **Session End — Step 1 format.** In order: (1.1) 2-4 sentence prose summary; (1.2) bulleted list of every file that will be written; (1.3) pending-items table with proposed priority + due + rationale; (1.4) disambiguation questions only if truly blocking.
- **Never invent counts.** If a query returns empty, say "none" or omit the bullet.
- **Honest state.** If something didn't happen as expected (commit not pushed, hook didn't fire, file missing), surface directly.
```

- [ ] **Step 6: Write `00_META/shared/memo_protocol.md`**

```markdown
## Cross-Folder Memo Protocol

Per ADR-013 + spec §4.7. Each persona has an inbox at `<scope>/00_META/inbox/` and an `archive/`. Each memo is one .md file with YAML frontmatter:

```
---
status: open | resolved | deferred
from: founder | skills-master | client-owner | telegram-<userid>
to: founder | skills-master | client-owner | broadcast
type: question | request | observation | decision | note
priority: critical | high | medium | low
subject: <one-line>
created: <ISO-8601 timestamp>
related: [<paths or task ids>]
due: <ISO-8601 date if applicable>
---

<body>
```

**Operator-driven scope (per Strict Rule 1):** when Ricardo or JP is driving, memos are not required for cross-folder edits — they're a paper trail mechanism for specialist requests, async coordination, and autonomous-agent communication.

**At session start**, this persona reads its inbox via `infra/scripts/nexostrat-memos.py <persona>` which prints a formatted summary filtered by `to:`.

**Resolution lifecycle:** open → resolved (move file to `archive/`) OR deferred (update `due:`, keep in inbox). Telegram `/inbox`, `/resolve <id>`, `/defer <id>` plugins (Plan 04) wrap this.
```

- [ ] **Step 7: Write `00_META/shared/gemini_handoff.md`**

```markdown
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
```

- [ ] **Step 8: Write `00_META/shared/vault_access.md`**

```markdown
## Vault / Sensitive Discipline

Per ADR-003 + ADR-004 + F10:

| Subfolder | Owner |
|---|---|
| `vault/partnership/` | Founder |
| `vault/legal/`, `vault/accounting/`, `vault/keys/` | Founder |
| `vault/clients/<slug>/` | Client-Owner |

Skills-Master owns no vault content.

**Discipline:**
- NEVER commit plaintext secrets to git. The `.gitignore` blocks `*.env`, `*.key`, `*secrets*`, `*.pem`. The pre-commit hook (`infra/hooks/pre-commit-secret-scan.sh`) catches secret prefixes.
- Decrypt to `/dev/shm` (RAM tmpfs) at use time → use → shred. No persistent mounted plaintext.
- Heavy assets (audio, large PDFs) age-encrypted before Drive upload; index in `vault/sensitive_index.md`.
- Secrets loaded into services via `infra/scripts/run-with-secrets.sh` (per CRITICAL 1 fix: explicit cleanup, no `exec` leak).
- The `vault/` folder accepts only `.age` files; `infra/hooks/pre-commit-vault-age-only.sh` enforces.

**Recovery scenarios:** see `docs/runbooks/key_compromise.md` (Plan 02) and `docs/runbooks/total_outage.md` (Plan 10). Short version: each holder's encrypted private key is backed up in their cloud password vault (Bitwarden); recipients file (`infra/age-recipients.txt`) is the canonical "who can decrypt" list.
```

- [ ] **Step 9: Write `00_META/shared/backup_posture.md`**

```markdown
## Backup Posture

Per spec §1 + §3 (post-Plan-01b state):

```
HP working tree (live)
  ▼
Gitea origin (HP, Tailscale only)
  ▼ systemd .path-watcher (Plan 01b)
GitHub mirror (off-site, private)
  ▼ same .path-watcher pattern
Codeberg mirror (off-site, private, second-site)
  ▼ nightly rsync 03:00 America/Tijuana (Plan 01b)
Warm-standby clone (idle until failover; RTO 15-30 min)
  ▼
Drive 2TB (heavy assets only, age-encrypted before upload)
```

**Recovery RTO targets:**
- Single-machine failure: 15-30 min via warm-standby (`docs/runbooks/hp_down.md`).
- Single off-site loss (GitHub OR Codeberg): irrelevant; the other survives.
- Total HP loss + warm-standby unreachable: ~2-4 hours via off-site mirror restore + crypto recovery.

**Verification cadence:** integration smoke test (Plan 01c) does real decrypt round-trip + real `git push` + verify GitHub HEAD changed + warm-rsync trigger. Periodic verification per a yet-undefined schedule (Plan 10 territory).
```

- [ ] **Step 10: Write `00_META/shared/change_log.md`**

```markdown
## Change Log

Per-persona-file change log. Append a row when this persona's CLAUDE.md or GEMINI.md is regenerated or substantively edited:

| Date | Agent | Description |
|------|-------|-------------|
| (rows added as the file evolves) | | |

The file changes are also tracked in root `00_META/CHANGELOG.md` (project-level), but a per-persona log keeps the WHY visible at the persona's own surface.
```

- [ ] **Step 11: Write `00_META/shared/STATUS.md` (template, F27)**

```markdown
# <persona> — STATUS

> **Last updated:** <ISO-8601 date>
> **Current phase:** <one-line>

## Current state

<2-3 paragraphs of where this persona stands.>

## Next sequence (locked)

1. <Next concrete action.>
2. <Following action.>
3. <Following action.>

## Blockers

<Bulleted list. "None" if none.>

## Pending JP input (consolidated)

<Only if relevant for this persona — Founder typically tracks this.>

## Open follow-ups

<Carried items.>

## Recent activity

- **YYYY-MM-DD (<topic>)** — <one-line summary linking to journal entry path>.
```

This template is the foundation of every persona's STATUS.md. F27 is satisfied by absence: there is NO Hosted-mode reference here (per ADR-021bis dropping the option entirely).

- [ ] **Step 12: Audit for leaks (F20)**

```bash
grep -rE '/srv/brain|BRAIN_STATUS|00_TEMPLATES/|brain-tasks-v1' /srv/Nexostrat/00_META/shared/
# Expected: empty output. Any hit means a leak from /srv/brain heritage and must be removed.
```

If anything matches, fix the offending file before committing. F20 closure requires zero leaks at this point.

- [ ] **Step 13: Stage + commit**

```bash
git add 00_META/shared/ 00_META/inbox/
git commit -m "$(cat <<'EOF'
Plan 01c Task 1 · canonical shared stanzas + F20 leak audit + F27 follow-through

00_META/shared/ holds the 9 canonical short-form stanzas inlined into every
persona file via inline_includes.py (Task 2):
- rule1.md
- session_start.md
- session_end.md
- session_output_format.md
- memo_protocol.md
- gemini_handoff.md
- vault_access.md
- backup_posture.md
- change_log.md

Plus 00_META/shared/STATUS.md as the per-persona STATUS template (F27 — no
Hosted-mode reference, consistent with ADR-021bis dropping the option).

F20 closed: grep for /srv/brain | BRAIN_STATUS | 00_TEMPLATES/ | brain-tasks-v1
returns empty across the shared/ tree.

00_META/inbox/ and inbox/archive/ created (.gitkeep) for Founder's memo
inbox (used at session start by nexostrat-memos.py — Task 3).

Spec refs: §4 (personas + stanzas), F20, F27, ADRs 011, 021bis.
EOF
)"
git push origin main
```

---

## Task 2: `inline_includes.py` (C3 fix) + tests

**Goal:** Implement the inliner script. Reads a template file containing `{{include: path}}` markers; replaces each marker with the contents of the referenced file (path relative to the template's directory or repo root). Supports `--check` mode (compares the generated output against the existing file; exit 1 on drift). ~30 lines of Python stdlib.

**Files:**
- Create: `infra/scripts/inline_includes.py`
- Create: `infra/scripts/test_inliner.sh`

- [ ] **Step 1: Write the test FIRST (TDD red)**

Create `/srv/Nexostrat/infra/scripts/test_inliner.sh`:

```bash
#!/usr/bin/env bash
# Test: inline_includes.py replaces {{include: path}} markers correctly,
#       and --check detects drift.
set -uo pipefail

INLINER="/srv/Nexostrat/infra/scripts/inline_includes.py"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Make a fixture: an include source + a template that includes it
echo "INCLUDED-CONTENT" > "$TMPDIR/snippet.md"
cat > "$TMPDIR/template.tmpl" <<'EOF'
Before
{{include: snippet.md}}
After
EOF

# Generate
python3 "$INLINER" --template "$TMPDIR/template.tmpl" --output "$TMPDIR/out.md"
[[ -f "$TMPDIR/out.md" ]] || { echo "FAIL — output file not created"; exit 1; }

# Verify content
if grep -q '^INCLUDED-CONTENT$' "$TMPDIR/out.md"; then
  echo "PASS — content inlined"
else
  echo "FAIL — content not inlined; got:"
  cat "$TMPDIR/out.md"
  exit 1
fi

if grep -q '{{include:' "$TMPDIR/out.md"; then
  echo "FAIL — marker still present"
  exit 1
else
  echo "PASS — marker consumed"
fi

# --check should report no drift
if python3 "$INLINER" --template "$TMPDIR/template.tmpl" --check "$TMPDIR/out.md"; then
  echo "PASS — --check no drift"
else
  echo "FAIL — --check unexpectedly reported drift"
  exit 1
fi

# Mutate the output, expect --check to flag drift
echo "DRIFT" >> "$TMPDIR/out.md"
if python3 "$INLINER" --template "$TMPDIR/template.tmpl" --check "$TMPDIR/out.md"; then
  echo "FAIL — --check missed drift"
  exit 1
else
  echo "PASS — --check detected drift"
fi

# Nested include: the inliner iterates to a fixed point. snippet-outer includes
# snippet-inner, and template includes snippet-outer. Both levels must expand.
echo "INNER" > "$TMPDIR/snippet-inner.md"
cat > "$TMPDIR/snippet-outer.md" <<'EOF'
OUTER-PRE
{{include: snippet-inner.md}}
OUTER-POST
EOF
cat > "$TMPDIR/template-nested.tmpl" <<'EOF'
TOP
{{include: snippet-outer.md}}
BOTTOM
EOF
python3 "$INLINER" --template "$TMPDIR/template-nested.tmpl" --output "$TMPDIR/nested-out.md"
if grep -q '^INNER$' "$TMPDIR/nested-out.md" && ! grep -q '{{include:' "$TMPDIR/nested-out.md"; then
  echo "PASS — nested include fully expanded"
else
  echo "FAIL — nested include not expanded:"
  cat "$TMPDIR/nested-out.md"
  exit 1
fi
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/test_inliner.sh
```

- [ ] **Step 2: Run test — expect FAIL (script doesn't exist yet)**

```bash
bash /srv/Nexostrat/infra/scripts/test_inliner.sh
# Expected: error or non-zero exit
```

- [ ] **Step 3: Implement `inline_includes.py`**

Create `/srv/Nexostrat/infra/scripts/inline_includes.py`:

```python
#!/usr/bin/env python3
"""inline_includes.py — Nexostrat (C3 fix)

Replace {{include: <path>}} markers in a template with the file contents at <path>.
Path is resolved relative to the template's own directory.

Usage:
  inline_includes.py --template <tmpl> --output <out>
      Generate <out> from <tmpl>.

  inline_includes.py --template <tmpl> --check <existing>
      Generate from <tmpl> and compare against <existing>.
      Exit 0 if identical; exit 1 with a unified diff if different.
"""
from __future__ import annotations
import argparse, difflib, pathlib, re, sys

MARKER = re.compile(r'^\{\{include:\s*([^}]+?)\s*\}\}\s*$', re.M)


MAX_DEPTH = 10  # Hard cap to defend against include-cycles; 10 is generous.


def render(template_path: pathlib.Path) -> str:
    text = template_path.read_text(encoding='utf-8')
    base = template_path.parent

    def sub(match: re.Match[str]) -> str:
        rel = match.group(1).strip()
        target = (base / rel).resolve()
        if not target.is_file():
            sys.exit(f"ERROR: include path not found: {rel} (resolved {target})")
        # Strip trailing newline of the included file so {{include}} on its own
        # line doesn't double-blank.
        return target.read_text(encoding='utf-8').rstrip('\n')

    # Iterate to a fixed point so nested {{include}} markers (an include whose
    # content itself contains an include) expand fully. Stanzas at 01c don't
    # nest today, but future stanzas may; the guard bounds depth so a cycle
    # fails loudly instead of looping forever.
    for _ in range(MAX_DEPTH):
        new_text = MARKER.sub(sub, text)
        if new_text == text:
            return text
        text = new_text
    sys.exit(f"ERROR: include depth exceeded {MAX_DEPTH} — possible cycle in {template_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True, type=pathlib.Path)
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument('--output', type=pathlib.Path)
    grp.add_argument('--check',  type=pathlib.Path)
    args = ap.parse_args()

    rendered = render(args.template)

    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
        return 0

    # --check
    existing = args.check.read_text(encoding='utf-8') if args.check.is_file() else ''
    if existing == rendered:
        return 0
    print(f"DRIFT: {args.check}")
    sys.stdout.writelines(difflib.unified_diff(
        existing.splitlines(keepends=True),
        rendered.splitlines(keepends=True),
        fromfile=str(args.check),
        tofile=str(args.template) + ' (rendered)',
    ))
    return 1


if __name__ == '__main__':
    sys.exit(main())
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/inline_includes.py
```

- [ ] **Step 4: Re-run test — expect PASS**

```bash
bash /srv/Nexostrat/infra/scripts/test_inliner.sh
# Expected: every line PASS; exit 0
```

- [ ] **Step 5: Stage + commit**

```bash
git add infra/scripts/inline_includes.py infra/scripts/test_inliner.sh
git commit -m "$(cat <<'EOF'
Plan 01c Task 2 · inline_includes.py (C3 fix)

~50 lines Python stdlib. Replaces {{include: <path>}} markers in a template
with the contents of <path> (resolved relative to the template directory).

Two modes:
- --template T --output O  : generate O from T
- --template T --check  E  : compare rendered T against existing E;
                              exit 0 if identical, 1 with unified diff if not.

The --check mode is what Plan 02's docs-pair drift hook will wrap (regenerate
each persona file, compare to committed; refuse commit on drift).

Test harness at infra/scripts/test_inliner.sh proves both modes (positive +
drift detection).

Spec refs: §4 (Personas), C3, ADRs 011, 029.
EOF
)"
git push origin main
```

---

## Task 3: `nexostrat-memos.py` (F8) + tests

**Goal:** Implement the inbox-summary script called by SessionStart. Reads `**/00_META/inbox/*.md` frontmatter; filters by `to:` field matching the requested persona; prints one-line-per-memo formatted summary sorted by priority.

**Files:**
- Create: `infra/scripts/nexostrat-memos.py`

- [ ] **Step 1: Implement `nexostrat-memos.py`**

Create `/srv/Nexostrat/infra/scripts/nexostrat-memos.py`:

```python
#!/usr/bin/env python3
"""nexostrat-memos.py — Nexostrat (F8)

Scan **/00_META/inbox/*.md across the repo, parse YAML-style frontmatter,
filter by `to:` field, print a formatted summary.

Usage:
  nexostrat-memos.py <persona>
      persona ∈ {founder, skills-master, client-owner, broadcast, all}

Output: one line per memo, sorted by priority then created.

Frontmatter expected:
    ---
    status: open | resolved | deferred
    from: founder | skills-master | client-owner | telegram-<id>
    to: founder | skills-master | client-owner | broadcast
    type: question | request | observation | decision | note
    priority: critical | high | medium | low
    subject: <one-line>
    created: <ISO-8601>
    related: [<paths>]
    due: <ISO-8601>
    ---
"""
from __future__ import annotations
import pathlib, re, sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PRIORITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, '': 4}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return a flat dict of frontmatter fields. Values stay as strings."""
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end < 0:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*?)\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def collect(persona: str) -> list[tuple[str, dict[str, str], pathlib.Path]]:
    out = []
    for inbox in REPO_ROOT.glob('**/00_META/inbox'):
        for memo in sorted(inbox.glob('*.md')):
            if memo.name == '.gitkeep':
                continue
            try:
                text = memo.read_text(encoding='utf-8')
            except Exception:
                continue
            fm = parse_frontmatter(text)
            if not fm:
                continue
            if fm.get('status', 'open') != 'open':
                continue
            to_field = fm.get('to', '')
            # Note: Python `and` binds tighter than `or`, so the `broadcast` clause is parenthesized
            # explicitly to spare future readers a parse step.
            if persona == 'all' or to_field == persona or (to_field == 'broadcast' and persona != 'all'):
                out.append((to_field, fm, memo))
    out.sort(key=lambda t: (PRIORITY_ORDER.get(t[1].get('priority', ''), 4),
                            t[1].get('created', '')))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    persona = sys.argv[1]
    items = collect(persona)
    if not items:
        print(f"  (no open memos for: {persona})")
        return 0
    print(f"  Open memos for: {persona}  ({len(items)} total)\n")
    for _to, fm, memo in items:
        rel = memo.relative_to(REPO_ROOT)
        prio = fm.get('priority', '?')
        typ = fm.get('type', '?')
        frm = fm.get('from', '?')
        subj = fm.get('subject', '<no subject>')
        due = f" due={fm['due']}" if fm.get('due') else ''
        print(f"  [{prio:8}] {typ:10}  from {frm}  →  {subj}{due}")
        print(f"             ({rel})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/nexostrat-memos.py
```

- [ ] **Step 2: Smoke test — empty case**

```bash
python3 /srv/Nexostrat/infra/scripts/nexostrat-memos.py founder
# Expected: "  (no open memos for: founder)"

python3 /srv/Nexostrat/infra/scripts/nexostrat-memos.py all
# Expected: same — no memos exist yet
```

- [ ] **Step 3: Smoke test — synthetic memo**

```bash
TMPDIR="$(mktemp -d)"
mkdir -p /srv/Nexostrat/00_META/inbox

cat > /srv/Nexostrat/00_META/inbox/test_memo_$$.md <<'EOF'
---
status: open
from: client-owner
to: founder
type: request
priority: high
subject: Test memo from synthetic harness
created: 2026-05-14T18:00:00-07:00
---

This is a test memo body. It should be collected by nexostrat-memos.py for `founder`.
EOF

python3 /srv/Nexostrat/infra/scripts/nexostrat-memos.py founder
# Expected: shows the memo with priority "high", from client-owner, subject visible

# Cleanup
rm /srv/Nexostrat/00_META/inbox/test_memo_$$.md
```

- [ ] **Step 4: Stage + commit**

```bash
git add infra/scripts/nexostrat-memos.py
git commit -m "$(cat <<'EOF'
Plan 01c Task 3 · nexostrat-memos.py (F8)

~80 lines Python stdlib. Walks **/00_META/inbox/*.md, parses YAML-style
frontmatter, filters by `to:` field, prints a one-line-per-memo summary
sorted by priority then created.

Called by SessionStart per shared/session_start.md step 6:
  python3 infra/scripts/nexostrat-memos.py <persona>

Telegram /inbox plugin (Plan 04) will wrap the same script.

Personas accepted: founder, skills-master, client-owner, broadcast, all.

Spec refs: §4.7 (Cross-folder memos), F8.
EOF
)"
git push origin main
```

---

## Task 4: `checkpoint-mtime-check.sh` (R4) + tests

**Goal:** R4 fix. SessionStart hook check — if `CHECKPOINT.md` was modified within the last N minutes (default 10) by a process other than the current session, warn loudly. Catches the "second Claude Code session opened by mistake" failure.

**Files:**
- Create: `infra/scripts/checkpoint-mtime-check.sh`

- [ ] **Step 1: Implement the script**

Create `/srv/Nexostrat/infra/scripts/checkpoint-mtime-check.sh`:

```bash
#!/usr/bin/env bash
# checkpoint-mtime-check.sh — Nexostrat (R4)
#
# Warn if any CHECKPOINT.md in the repo was modified within the last
# THRESHOLD_MIN minutes. Catches concurrent-session edits.
#
# Usage:
#   checkpoint-mtime-check.sh [THRESHOLD_MIN]
# Default threshold: 10 minutes.
# Note (MVP scope): in normal single-operator flow the gap between session-end
# (push CHECKPOINT.md) and the next session-start (read CHECKPOINT.md) is well
# under 10 minutes, which means this check will warn often when the system is
# behaving correctly. That noise is the cost of an mtime-only MVP. Plan 03's
# events.jsonl router supersedes this with a proper session-lock; until then
# operators can tune `THRESHOLD_SEC` per host if the warnings are too chatty.
#
# Exit codes:
#   0 — no recent edits (or only by this session, which we can't detect; documented limitation)
#   1 — at least one CHECKPOINT.md modified within the threshold (warning printed)

set -uo pipefail

REPO="/srv/Nexostrat"
THRESHOLD_MIN="${1:-10}"

# find CHECKPOINT.md files modified within the last THRESHOLD_MIN minutes
mapfile -t recent < <(
  find "$REPO" \
    -path '*/.git' -prune -o \
    -name 'CHECKPOINT.md' -type f -mmin "-${THRESHOLD_MIN}" -print 2>/dev/null
)

if [[ ${#recent[@]} -eq 0 ]]; then
  exit 0
fi

echo
echo "========================================================================"
echo "WARNING — CHECKPOINT.md(s) modified within the last ${THRESHOLD_MIN} min:"
for f in "${recent[@]}"; do
  ts=$(stat -c '%y' "$f" | cut -d. -f1)
  rel="${f#$REPO/}"
  echo "  $rel  (mtime $ts)"
done
echo
echo "If ANOTHER Claude Code session is open against this repo, close it"
echo "before continuing — concurrent CHECKPOINT.md edits cause confusion."
echo "If this is intentional (e.g., you just finished writing CHECKPOINT.md"
echo "for THIS session), this warning is safe to ignore."
echo "========================================================================"
echo
exit 1
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/checkpoint-mtime-check.sh
```

- [ ] **Step 2: Smoke test — clean state**

```bash
# Touch all CHECKPOINT files to be old (>10 min)
find /srv/Nexostrat -name 'CHECKPOINT.md' -not -path '*/.git/*' -exec touch -d '20 min ago' {} \;

bash /srv/Nexostrat/infra/scripts/checkpoint-mtime-check.sh
# Expected: silent, exit 0
```

- [ ] **Step 3: Smoke test — recent edit**

```bash
# Pick the root CHECKPOINT.md, touch it now
touch /srv/Nexostrat/CHECKPOINT.md

bash /srv/Nexostrat/infra/scripts/checkpoint-mtime-check.sh
# Expected: WARNING block printed; exit 1
```

- [ ] **Step 4: Stage + commit**

```bash
git add infra/scripts/checkpoint-mtime-check.sh
git commit -m "$(cat <<'EOF'
Plan 01c Task 4 · checkpoint-mtime-check.sh (R4)

R4: SessionStart-time concurrent-session protection. Find all CHECKPOINT.md
files modified within the last N minutes (default 10). If any, print a
warning block; exit 1.

Persona session_start.md stanza (Task 1) calls this in step 9. Test passes
both directions (silent on stale files; warns on recent edit).

Limitation: can't distinguish "this same session just finished writing
CHECKPOINT" from "another session is editing concurrently." Documented in
the warning text — safe-to-ignore disclaimer.

Spec refs: §4.10 (CHECKPOINT), R4, ADR-031.
EOF
)"
git push origin main
```

---

## Task 5: Founder root persona files (regenerated via inliner)

**Goal:** Convert the existing root `CLAUDE.md` and `GEMINI.md` to template-form (with `{{include}}` markers), then regenerate them via the inliner. The terrain-prep CLAUDE.md/GEMINI.md content is preserved; this task swaps inline-section text for include markers so future shared-stanza edits propagate via re-render.

**Files:**
- Create: `00_META/templates/CLAUDE.md.tmpl` (Founder template)
- Create: `00_META/templates/GEMINI.md.tmpl` (Founder template)
- Modify: `CLAUDE.md` (regenerated)
- Modify: `GEMINI.md` (regenerated)

- [ ] **Step 1: Create the templates folder**

```bash
mkdir -p /srv/Nexostrat/00_META/templates
```

- [ ] **Step 2: Write the Founder CLAUDE.md template**

Write `/srv/Nexostrat/00_META/templates/CLAUDE.md.tmpl`:

```markdown
# Nexostrat — Claude Context (Founder)

> **Last Updated:** 2026-05-14 (regenerated via inline_includes.py during Plan 01c)
> **Scope:** Founder persona — root of `/srv/Nexostrat/`. AI consulting firm for SMEs (PyMEs) in Mexico, Colombia, and LatAm.
>
> **⚠️ Architectural source of truth (always read these first):**
> - **Founding spec:** [`00_META/proposals/2026-05-13_nexostrat-system-design.md`](00_META/proposals/2026-05-13_nexostrat-system-design.md) — Batch 1 amendments applied
> - **Master plan index:** [`00_META/plans/README.md`](00_META/plans/README.md)
> - **Current baton:** [`CHECKPOINT.md`](CHECKPOINT.md) — where the last session left off

## Role

You are the **Founder persona** of Nexostrat. Operate this folder (`/srv/Nexostrat/`) as the persona running the consulting firm: pre-launch positioning, service-line definition, prospect pipeline, deliverables, ongoing operations, and architectural integrity.

**Co-founders:** Ricardo Mejía Caicedo + Juan Pablo (JP). 50/50 partnership signed 2026-05-12.

## Strict Rules

1. {{include: ../shared/rule1.md}}
2. **Folder scope = Founder-owned paths.** Write primarily within Founder-owned folders (root level + `00_META/`, `00_GOVERNANCE/`, `00_PARTNERSHIP/`, `infra/`, `docs/`, `operations/`, `vault/{partnership,legal,accounting,keys}/`). Reading anywhere within `/srv/Nexostrat/` is always permitted.
3. **You author all `GEMINI.md` files in this repo.** Edit them as Founder needs. Gemini may NOT edit any `CLAUDE.md` file (reciprocal rule enforced in `GEMINI.md`).
4. **No `/srv/brain` references.** Nexostrat is a standalone entity.
5. **No n8n.** All workflows are Python + systemd timers (per ADR-029).
6. **Bilingual workflow.** Internal/architectural artifacts are English. Client-facing and JP-facing artifacts are Spanish.

{{include: ../shared/session_start.md}}

{{include: ../shared/session_end.md}}

{{include: ../shared/session_output_format.md}}

## Architecture / Context

**Authoritative source:** [`00_META/proposals/2026-05-13_nexostrat-system-design.md`](00_META/proposals/2026-05-13_nexostrat-system-design.md) (founding spec, ADRs 001-038). This CLAUDE.md does NOT duplicate spec content — read the spec for any architectural question.

**Quick orientation:**
- Nexostrat is the AI consulting firm of Ricardo + JP for SMEs (PyMEs) in Mexico, Colombia, and LatAm.
- Lives at `/srv/Nexostrat/` on `ricardo-hp-laptop` (Linux Mint 22.2; Tailscale `100.64.121.80`).
- Standalone git repo. Origin: Gitea at `git@gitea-nexostrat:nexostrat/nexostrat.git` (resolves via `~/.ssh/config` to Tailscale `100.64.121.80:2222`). Mirrors to GitHub + Codeberg landed in Plan 01b (firm namespace `nexostrat/nexostrat` on both).
- Three personas (per ADR-011): **Founder** (root, this file), **Skills-Master** (`skills/`), **Client-Owner** (`pipeline/`).
- Stage 1 launch target: 2026-06-30 to 2026-07-15.

**Key collaborators:**
- **Ricardo** — co-founder, primary technical operator, runs daily sessions.
- **JP** — co-founder, Light mode per ADR-021bis (Telegram bot + email/report digests + future FOSS dashboard from Plan 02; opts out of Gitea web), 10h/wk bandwidth, async coordination via Telegram. Machine: `jp-mac` (macOS Sequoia 15.7.3). Heavy mode (full clone + Claude Code on `jp-mac`) is a future flip event, not a Stage 1 deliverable.
- **Claude (you)** — Founder persona; assists strategy, deliverables, code.
- **Gemini** — second seat (see § Gemini Handoff Protocol).

{{include: ../shared/memo_protocol.md}}

{{include: ../shared/gemini_handoff.md}}

## Inter-Persona Coordination

Per ADR-013: **`infra/events/events.jsonl`** is the cross-persona/cross-folder primitive. Append-only event log. Built in Plan 03.

**Pre-Plan-03 (current state):** memo-style routing via `nexostrat-memos.py` and per-persona `00_META/inbox/` folders (F8 / spec §4.7). Founder's inbox is `/srv/Nexostrat/00_META/inbox/`. Sibling inboxes: `skills/00_META/inbox/`, `pipeline/00_META/inbox/`.

**Post-Plan-03:** any persona that needs another's attention emits an event into `events.jsonl`. The event-router daemon (Plan 03) routes per `routing.yaml` and supersedes the memo protocol. After Plan 03 lands, `events.jsonl` is the single cross-persona primitive.

**External coordination:**
- Ricardo ↔ JP: Telegram (Plan 04+ for in-system events; agreed personal channel for ad-hoc out-of-band).
- Cross-entity (Ricardo's other projects): manually mediated by Ricardo. Nexostrat doesn't participate in any cross-entity protocol.

{{include: ../shared/vault_access.md}}

{{include: ../shared/backup_posture.md}}

{{include: ../shared/change_log.md}}
```

- [ ] **Step 3: Write the Founder GEMINI.md template**

Write `/srv/Nexostrat/00_META/templates/GEMINI.md.tmpl`:

```markdown
# Nexostrat — Gemini Context (Founder, second-seat)

> **Last Updated:** 2026-05-14 (regenerated via inline_includes.py during Plan 01c, authored by Claude per Strict Rule 3)
> **Scope:** Founder persona — Gemini second-seat. AI consulting firm for SMEs in LatAm.

## Role

You are the **second seat** to Claude (Founder persona) at root of `/srv/Nexostrat/`. Claude is the director; you are consulted for: web search and fresh-information lookups, adversarial audits, code/document review, alternative brainstorming.

## Strict Rules

1. **You may NOT edit any `CLAUDE.md` file in this repo.** Reciprocal of Strict Rule 3 in CLAUDE.md.
2. **Stay in scope of the handoff.** Each handoff (`00_META/handoff/claude_to_gemini.md`) names the file you may write to (`gemini_to_claude.md`) and the content you may produce. Do not edit other files unless the handoff explicitly authorizes.
3. **Cite sources.** Whenever you produce a fact-claim, include the source URL or document path. The Founder will validate before integrating.
4. **No `/srv/brain` references.** Nexostrat is standalone.
5. **No n8n.** All workflows are Python + systemd.

{{include: ../shared/gemini_handoff.md}}

## Vault constraint (Gemini)

You have an age private key + passphrase. Decrypt is permitted for review purposes (e.g., reading a sealed proposal or partnership artifact during a handoff). **Do not write into `vault/`** — that namespace is Claude's per ADR-003/F10. If you need to surface a finding from decrypted content, write it into your handoff response (`gemini_to_claude.md`) and let Claude stage the resulting artifact. The wrapper discipline (`run-with-secrets.sh`, `/dev/shm`, `shred`) documented in CLAUDE.md does not apply to your review-only workflows.

{{include: ../shared/change_log.md}}
```

- [ ] **Step 4: Generate root `CLAUDE.md` and `GEMINI.md`**

```bash
cd /srv/Nexostrat
python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/CLAUDE.md.tmpl \
    --output CLAUDE.md

python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/GEMINI.md.tmpl \
    --output GEMINI.md

ls -la CLAUDE.md GEMINI.md
# Expected: both files exist with reasonable sizes (CLAUDE.md ~10-15 KB, GEMINI.md ~5 KB)
```

- [ ] **Step 5: Diff against the previous version (load-bearing-content check)**

The Plan 01c re-audit (2026-05-16) flagged H3: earlier drafts of the Founder
template dropped two load-bearing sections (Architecture/Context + Inter-
Persona Coordination) that lived in the pre-regeneration `CLAUDE.md` but had
no shared stanza. Those blocks are now inlined per-persona in the templates.
This step verifies the regenerated file still carries every load-bearing fact
from the prior version.

```bash
# (a) Full diff for visual scan
git diff CLAUDE.md GEMINI.md | head -100

# (b) Targeted load-bearing-content check against the v0.1b-mirrors-only baseline
for needle in \
  "Stage 1 launch target: 2026-06-30" \
  "Tailscale \`100.64.121.80\`" \
  "ricardo-hp-laptop" \
  "jp-mac" \
  "ADR-013" \
  "events.jsonl" \
  "Light mode per ADR-021bis" \
  "ADR-011"
do
  if grep -qF "$needle" CLAUDE.md; then
    echo "  ok    $needle"
  else
    echo "  MISS  $needle  ← load-bearing content lost; edit template + re-render"
  fi
done

# (c) Cross-check: every section heading in the v0.1b-mirrors-only CLAUDE.md
# should have a matching heading (or be deliberately superseded) in the new one
echo "--- headings in v0.1b-mirrors-only:CLAUDE.md ---"
git show v0.1b-mirrors-only:CLAUDE.md | grep -E '^## '
echo "--- headings in regenerated CLAUDE.md ---"
grep -E '^## ' CLAUDE.md
```

Expected: every `needle` prints `ok`; section-heading set is a superset
(Memo Protocol is new from Plan 01c; nothing from the prior version is missing
without justification).

If any needle prints `MISS`, edit the relevant template (Founder
`00_META/templates/CLAUDE.md.tmpl`, Architecture/Context block) and re-run
Step 4. Don't paper over with a per-file edit to the regenerated `CLAUDE.md` —
that would re-introduce drift at the next inline run.

- [ ] **Step 6: Verify --check is now drift-free**

```bash
python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/CLAUDE.md.tmpl \
    --check /srv/Nexostrat/CLAUDE.md
echo "exit=$?"
# Expected: exit 0 (no drift between template + output)

python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/GEMINI.md.tmpl \
    --check /srv/Nexostrat/GEMINI.md
echo "exit=$?"
# Expected: exit 0
```

- [ ] **Step 7: Stage + commit**

```bash
git add 00_META/templates/CLAUDE.md.tmpl 00_META/templates/GEMINI.md.tmpl \
        CLAUDE.md GEMINI.md
git commit -m "$(cat <<'EOF'
Plan 01c Task 5 · Founder persona files regenerated via inliner

CLAUDE.md (Founder root) regenerated from 00_META/templates/CLAUDE.md.tmpl
which uses {{include: ../shared/<stanza>.md}} markers for session_start,
session_end, output_format, memo_protocol, gemini_handoff, vault_access,
backup_posture, change_log.

GEMINI.md (Founder root, second-seat) regenerated from
00_META/templates/GEMINI.md.tmpl. Includes only the relevant stanzas
(handoff, vault_access, change_log) — Gemini doesn't run sessions.

Both files pass `inline_includes.py --check` (zero drift).

Substantive content preserved from terrain-prep version; future stanza edits
propagate to CLAUDE.md/GEMINI.md via single re-render call.

Spec refs: §4 (Personas), C3, ADR-011.
EOF
)"
git push origin main
```

---

## Task 6: Skills-Master persona files

**Goal:** Create `skills/CLAUDE.md` and `skills/GEMINI.md` from canonical stanzas. The Skills-Master persona owns the 5+1 reusable skills, prompts, versions, benchmark tests; owns NO vault content (per F10).

**Files:**
- Create: `00_META/templates/skills_CLAUDE.md.tmpl`
- Create: `00_META/templates/skills_GEMINI.md.tmpl`
- Create: `skills/CLAUDE.md`
- Create: `skills/GEMINI.md`
- Create: `skills/CHECKPOINT.md`
- Create: `skills/00_META/inbox/.gitkeep`

- [ ] **Step 1: Create skills' inbox folder**

```bash
mkdir -p /srv/Nexostrat/skills/00_META/inbox/archive
mkdir -p /srv/Nexostrat/skills/00_META/journal
touch /srv/Nexostrat/skills/00_META/inbox/.gitkeep \
      /srv/Nexostrat/skills/00_META/inbox/archive/.gitkeep \
      /srv/Nexostrat/skills/00_META/journal/.gitkeep
```

- [ ] **Step 2: Write the Skills-Master CHECKPOINT placeholder**

Write `/srv/Nexostrat/skills/CHECKPOINT.md`:

```markdown
# CHECKPOINT — skills/ (Skills-Master)

**Status:** CHECKPOINT_NO_ACTIVE_WORK

**Updated:** 2026-05-14 (Plan 01c Task 6)
**Persona:** Skills-Master

> No active session work. When this persona starts editing skill prompts,
> running benchmarks, or shipping new skill versions, this file gets the
> standard CHECKPOINT structure (what just happened, in-flight next action,
> etc. — see shared/session_end.md).
>
> Per ADR-031: empty CHECKPOINT.md commits refused unless `CHECKPOINT_NO_ACTIVE_WORK`
> token present.
```

- [ ] **Step 3: Write `00_META/templates/skills_CLAUDE.md.tmpl`**

Write `/srv/Nexostrat/00_META/templates/skills_CLAUDE.md.tmpl`:

```markdown
# Nexostrat — Claude Context (Skills-Master)

> **Last Updated:** 2026-05-14 (generated via inline_includes.py during Plan 01c)
> **Scope:** `/srv/Nexostrat/skills/` — the 5+1 reusable skills bucket.
>
> **⚠️ Architectural source of truth (always read these first):**
> - **Founding spec:** [`../00_META/proposals/2026-05-13_nexostrat-system-design.md`](../00_META/proposals/2026-05-13_nexostrat-system-design.md)
> - **Master plan index:** [`../00_META/plans/README.md`](../00_META/plans/README.md)
> - **Current baton:** [`CHECKPOINT.md`](CHECKPOINT.md)

## Role

You are the **Skills-Master persona**. Operate this folder (`skills/`) as the steward of the 5+1 reusable skills (company-analyst, industry-analyst, competitor-analyst, meeting-script, opportunity-report, discovery-meeting): prompts, versions, benchmarks, regression-test fixtures.

## Strict Rules

1. {{include: ../00_META/shared/rule1.md}}
2. **Folder scope = `skills/`.** Write primarily within `skills/` and `skills/00_META/`. Cross-persona edits are fine when an operator is driving (Strict Rule 1); otherwise route via memo to the appropriate persona inbox.
3. **You author all `GEMINI.md` files within `skills/`.** Gemini may NOT edit any `CLAUDE.md` file.
4. **NO vault writes.** Per F10: Skills-Master owns no vault content. If a skill produces sensitive output (rare for the 5+1), surface to Founder via memo.
5. **Anti-hallucination is non-negotiable.** Every skill prompt under `skills/<NN>_*/prompts/` MUST contain the marker block from `skills/shared/anti_hallucination.md` (Plan 02 hook will enforce). Never relax this requirement.
6. **Versioning + benchmarks are gates, not bureaucracy.** A prompt edit = new version. Bodai benchmark drop > 10% blocks commit; factual-accuracy drop blocks unconditionally.

{{include: ../00_META/shared/session_start.md}}

{{include: ../00_META/shared/session_end.md}}

{{include: ../00_META/shared/session_output_format.md}}

## Architecture / Context

**Authoritative source:** [`../00_META/proposals/2026-05-13_nexostrat-system-design.md`](../00_META/proposals/2026-05-13_nexostrat-system-design.md) (founding spec, ADRs 001-038; especially §4.4 Skills-Master + §7 anti-hallucination + Plan 07 Bodai benchmark).

**Quick orientation:**
- Skills-Master operates `/srv/Nexostrat/skills/` — the 5+1 reusable skills bucket (company-analyst, industry-analyst, competitor-analyst, meeting-script, opportunity-report, discovery-meeting).
- Per-skill structure: `skills/<NN>_<name>/{prompts,versions,benchmarks,tests}/`.
- Stage 1 launch target: 2026-06-30 to 2026-07-15. Skills 1-3 + discovery-meeting are Stage-1 gating; 4-5 land Stage 2.
- The Bodai benchmark dataset (Plan 07) is the regression gate: factual-accuracy drop blocks unconditionally; >10% Bodai drop blocks commit.

**Key collaborators:**
- **Ricardo** — co-founder, primary operator for in-session skill work.
- **JP** — co-founder, Light mode per ADR-021bis (no session-driving surface at Stage 1; consumed-content only via the FOSS dashboard from Plan 02).
- **Claude (you)** — Skills-Master persona, this file.
- **Gemini** — second seat (prompt review + factual sourcing; see § Gemini Handoff Protocol).
- **Sibling personas** — Founder Claude at repo root; Client-Owner Claude at `../pipeline/`. Skill outputs feed Client-Owner chains; see § Inter-Persona Coordination.

{{include: ../00_META/shared/memo_protocol.md}}

{{include: ../00_META/shared/gemini_handoff.md}}

## Inter-Persona Coordination

Per ADR-013: **`/srv/Nexostrat/infra/events/events.jsonl`** is the cross-persona/cross-folder primitive. Built in Plan 03.

**Pre-Plan-03 (current state):** memo-style routing via `nexostrat-memos.py` and per-persona inboxes (F8 / spec §4.7). Skills-Master's inbox is `skills/00_META/inbox/`. Sibling inboxes: `../00_META/inbox/` (Founder), `../pipeline/00_META/inbox/` (Client-Owner).

**Post-Plan-03:** events.jsonl supersedes memos. Common cross-persona signals from Skills-Master: skill-version pin notifications (→ Client-Owner), Bodai-benchmark regressions (→ Founder), prompt-template changes affecting active chains (→ Client-Owner).

{{include: ../00_META/shared/vault_access.md}}

{{include: ../00_META/shared/backup_posture.md}}

{{include: ../00_META/shared/change_log.md}}
```

- [ ] **Step 4: Write `00_META/templates/skills_GEMINI.md.tmpl`**

Write `/srv/Nexostrat/00_META/templates/skills_GEMINI.md.tmpl`:

```markdown
# Nexostrat — Gemini Context (Skills-Master, second-seat)

> **Last Updated:** 2026-05-14 (generated via inline_includes.py during Plan 01c, authored by Claude)
> **Scope:** `/srv/Nexostrat/skills/` — second seat to Skills-Master Claude.

## Role

You are the **second seat** to Claude (Skills-Master persona) within `skills/`. Consulted for: prompt-engineering review, alternative phrasings, fact-checking factual claims in skill outputs, sourcing fresh industry information for skills 2-3.

## Strict Rules

1. **You may NOT edit any `CLAUDE.md` file in this repo.** Reciprocal of Strict Rule 3.
2. **Stay in scope of the handoff.** Edit only `00_META/handoff/gemini_to_claude.md` (in this scope or root, depending on the handoff target).
3. **Cite sources.** Skills-Master deliverables are factual; cite every claim.
4. **NO vault writes.** Per F10.

{{include: ../00_META/shared/gemini_handoff.md}}

## Vault constraint (Gemini)

Skills-Master Gemini owns no vault content (per F10). You do not decrypt or write to `vault/`. Sensitive material in a skill output — rare — should be flagged in your handoff response so Skills-Master Claude can route via memo to Founder Claude for proper vault staging. The wrapper discipline documented in CLAUDE.md does not apply to you.

{{include: ../00_META/shared/change_log.md}}
```

- [ ] **Step 5: Generate the Skills-Master persona files**

```bash
cd /srv/Nexostrat
python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/skills_CLAUDE.md.tmpl \
    --output skills/CLAUDE.md

python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/skills_GEMINI.md.tmpl \
    --output skills/GEMINI.md

ls -la skills/CLAUDE.md skills/GEMINI.md
```

- [ ] **Step 6: Verify drift-free**

```bash
python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/skills_CLAUDE.md.tmpl \
    --check /srv/Nexostrat/skills/CLAUDE.md && echo "OK skills/CLAUDE.md"

python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/skills_GEMINI.md.tmpl \
    --check /srv/Nexostrat/skills/GEMINI.md && echo "OK skills/GEMINI.md"
```

- [ ] **Step 7: Stage + commit**

```bash
git add 00_META/templates/skills_*.tmpl \
        skills/CLAUDE.md skills/GEMINI.md skills/CHECKPOINT.md \
        skills/00_META/

git commit -m "$(cat <<'EOF'
Plan 01c Task 6 · Skills-Master persona files

skills/CLAUDE.md + skills/GEMINI.md generated from templates at
00_META/templates/skills_*.tmpl, inlining the shared stanzas via
inline_includes.py.

Persona-specific Strict Rules:
- Folder scope = skills/
- NO vault writes (per F10)
- Anti-hallucination marker block required in every skill prompt
- Versioning + benchmark = commit gates

skills/CHECKPOINT.md placeholder with CHECKPOINT_NO_ACTIVE_WORK token.
skills/00_META/{inbox,journal}/ scaffold landed.

Both files pass inline_includes.py --check.

Spec refs: §4 (Three personas), F10, F18, ADR-011.
EOF
)"
git push origin main
```

---

## Task 7: Client-Owner persona files (F10 vault scope)

**Goal:** Create `pipeline/CLAUDE.md` and `pipeline/GEMINI.md`. Client-Owner owns active client work AND `vault/clients/<slug>/` (per F10 namespace split).

**Files:**
- Create: `00_META/templates/pipeline_CLAUDE.md.tmpl`
- Create: `00_META/templates/pipeline_GEMINI.md.tmpl`
- Create: `pipeline/CLAUDE.md`
- Create: `pipeline/GEMINI.md`
- Create: `pipeline/CHECKPOINT.md`
- Create: `pipeline/00_META/inbox/.gitkeep`

- [ ] **Step 1: Create pipeline's inbox folder**

```bash
mkdir -p /srv/Nexostrat/pipeline/00_META/inbox/archive
mkdir -p /srv/Nexostrat/pipeline/00_META/journal
touch /srv/Nexostrat/pipeline/00_META/inbox/.gitkeep \
      /srv/Nexostrat/pipeline/00_META/inbox/archive/.gitkeep \
      /srv/Nexostrat/pipeline/00_META/journal/.gitkeep
```

- [ ] **Step 2: Write `pipeline/CHECKPOINT.md` placeholder**

Write `/srv/Nexostrat/pipeline/CHECKPOINT.md`:

```markdown
# CHECKPOINT — pipeline/ (Client-Owner)

**Status:** CHECKPOINT_NO_ACTIVE_WORK

**Updated:** 2026-05-14 (Plan 01c Task 7)
**Persona:** Client-Owner

> No active session work. When client engagements move past `prospect`
> phase, this file gets the standard CHECKPOINT structure.
>
> Per ADR-031: empty CHECKPOINT.md commits refused unless
> `CHECKPOINT_NO_ACTIVE_WORK` token present.
```

- [ ] **Step 3: Write `00_META/templates/pipeline_CLAUDE.md.tmpl`**

Write `/srv/Nexostrat/00_META/templates/pipeline_CLAUDE.md.tmpl`:

```markdown
# Nexostrat — Claude Context (Client-Owner)

> **Last Updated:** 2026-05-14 (generated via inline_includes.py during Plan 01c)
> **Scope:** `/srv/Nexostrat/pipeline/` — active client work + prospects + per-client vault.
>
> **⚠️ Architectural source of truth (always read these first):**
> - **Founding spec:** [`../00_META/proposals/2026-05-13_nexostrat-system-design.md`](../00_META/proposals/2026-05-13_nexostrat-system-design.md)
> - **Master plan index:** [`../00_META/plans/README.md`](../00_META/plans/README.md)
> - **Current baton:** [`CHECKPOINT.md`](CHECKPOINT.md)
> - **Per-client template:** [`clients/_template/README.md`](clients/_template/README.md)

## Role

You are the **Client-Owner persona**. Operate `pipeline/` and `vault/clients/`: per-client production chains (12 stations + 3 cross-cutting), prospects intake, state management, and the engagement lifecycle from `prospect` → `retainer_active` (or `churned`).

## Strict Rules

1. {{include: ../00_META/shared/rule1.md}}
2. **Folder scope = `pipeline/` + `vault/clients/<slug>/`** (per F10 vault namespace split). Cross-persona edits when an operator is driving; otherwise memos.
3. **You author all `GEMINI.md` files within `pipeline/`.** Gemini may NOT edit any `CLAUDE.md` file.
4. **State machine is non-negotiable.** Phase transitions in `state.json` follow the legal-transition graph (see `clients/_template/README.md`). Illegal transitions get refused — don't bypass.
5. **Per-client `CHECKPOINT.md`** for any client past `intake` phase. Empty checkpoints refused unless `CHECKPOINT_NO_ACTIVE_WORK`.
6. **Sensitive client material → `vault/clients/<slug>/`** as `.age`. Never plaintext NDA/contract/invoice in `pipeline/clients/<slug>/`.

{{include: ../00_META/shared/session_start.md}}

{{include: ../00_META/shared/session_end.md}}

{{include: ../00_META/shared/session_output_format.md}}

## Architecture / Context

**Authoritative source:** [`../00_META/proposals/2026-05-13_nexostrat-system-design.md`](../00_META/proposals/2026-05-13_nexostrat-system-design.md) (founding spec, ADRs 001-038; especially §4.5 Client-Owner + §6 state.json + §8 chain stations).

**Quick orientation:**
- Client-Owner operates `/srv/Nexostrat/pipeline/` (per-client production chains) and `vault/clients/<slug>/` (encrypted client material).
- Per-client structure follows `clients/_template/` (12 stations + 3 cross-cutting; state machine in `state.json`).
- Stage 1 launch target: 2026-06-30 to 2026-07-15. First paying client marks the Stage-1-Stage-2 boundary.
- Engagement lifecycle: `prospect` → `qualified` → `discovery` → `proposal` → `retainer_active` (or `churned`).

**Key collaborators:**
- **Ricardo** — co-founder, primary operator; closes engagements + reviews proposals.
- **JP** — co-founder, Light mode per ADR-021bis (no session-driving surface; visibility via Telegram + future FOSS dashboard from Plan 02).
- **Claude (you)** — Client-Owner persona, this file.
- **Gemini** — second seat (prospect research + draft review; see § Gemini Handoff Protocol).
- **Sibling personas** — Founder Claude at repo root; Skills-Master Claude at `../skills/`. Client chains consume skill outputs; see § Inter-Persona Coordination.

{{include: ../00_META/shared/memo_protocol.md}}

{{include: ../00_META/shared/gemini_handoff.md}}

## Inter-Persona Coordination

Per ADR-013: **`/srv/Nexostrat/infra/events/events.jsonl`** is the cross-persona/cross-folder primitive. Built in Plan 03.

**Pre-Plan-03 (current state):** memo-style routing via `nexostrat-memos.py` and per-persona inboxes (F8 / spec §4.7). Client-Owner's inbox is `pipeline/00_META/inbox/`. Sibling inboxes: `../00_META/inbox/` (Founder), `../skills/00_META/inbox/` (Skills-Master).

**Post-Plan-03:** events.jsonl supersedes memos. Common cross-persona signals from Client-Owner: skill-version pin requests (→ Skills-Master), partnership/legal escalations (→ Founder), vault-recipient changes per client (→ Founder for `infra/age-recipients.txt` updates).

{{include: ../00_META/shared/vault_access.md}}

{{include: ../00_META/shared/backup_posture.md}}

{{include: ../00_META/shared/change_log.md}}
```

- [ ] **Step 4: Write `00_META/templates/pipeline_GEMINI.md.tmpl`**

Write `/srv/Nexostrat/00_META/templates/pipeline_GEMINI.md.tmpl`:

```markdown
# Nexostrat — Gemini Context (Client-Owner, second-seat)

> **Last Updated:** 2026-05-14 (generated via inline_includes.py during Plan 01c, authored by Claude)
> **Scope:** `/srv/Nexostrat/pipeline/` — second seat to Client-Owner Claude.

## Role

You are the **second seat** to Claude (Client-Owner persona) within `pipeline/`. Consulted for: prospect-research lookups, draft review of client-facing artifacts (proposals, scopes), source verification.

## Strict Rules

1. **You may NOT edit any `CLAUDE.md` file in this repo.** Reciprocal of Strict Rule 3.
2. **Stay in scope of the handoff.**
3. **Cite sources.** Client-facing material is on the line — every claim cited.
4. **NO writes to `vault/clients/<slug>/`.** Decryption permitted (you have a key); writing isn't your job — Client-Owner Claude staging the .age artifact is.

{{include: ../00_META/shared/gemini_handoff.md}}

## Vault constraint (Gemini)

You have an age private key. Decrypt of `vault/clients/<slug>/*.age` is permitted for review-only purposes — e.g., reading a sealed proposal during draft review or fact-checking a signed scope. **Do not write into `vault/clients/`** — Client-Owner Claude stages the encrypted artifact per F10. If a decrypted content surface a finding, write it into your handoff response (`gemini_to_claude.md`) so Claude can stage the correction. Wrapper discipline (`run-with-secrets.sh`, `/dev/shm`, `shred`) documented in CLAUDE.md does not apply to your review workflows.

{{include: ../00_META/shared/change_log.md}}
```

- [ ] **Step 5: Generate the Client-Owner persona files**

```bash
cd /srv/Nexostrat
python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/pipeline_CLAUDE.md.tmpl \
    --output pipeline/CLAUDE.md

python3 infra/scripts/inline_includes.py \
    --template 00_META/templates/pipeline_GEMINI.md.tmpl \
    --output pipeline/GEMINI.md

ls -la pipeline/CLAUDE.md pipeline/GEMINI.md
```

- [ ] **Step 6: Verify drift-free**

```bash
python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/pipeline_CLAUDE.md.tmpl \
    --check /srv/Nexostrat/pipeline/CLAUDE.md && echo "OK pipeline/CLAUDE.md"

python3 /srv/Nexostrat/infra/scripts/inline_includes.py \
    --template /srv/Nexostrat/00_META/templates/pipeline_GEMINI.md.tmpl \
    --check /srv/Nexostrat/pipeline/GEMINI.md && echo "OK pipeline/GEMINI.md"
```

- [ ] **Step 7: Stage + commit**

```bash
git add 00_META/templates/pipeline_*.tmpl \
        pipeline/CLAUDE.md pipeline/GEMINI.md pipeline/CHECKPOINT.md \
        pipeline/00_META/

git commit -m "$(cat <<'EOF'
Plan 01c Task 7 · Client-Owner persona files (F10)

pipeline/CLAUDE.md + pipeline/GEMINI.md generated from templates at
00_META/templates/pipeline_*.tmpl.

Persona-specific Strict Rules:
- Folder scope = pipeline/ + vault/clients/<slug>/ (F10 namespace split)
- State machine non-negotiable (transitions per state.json schema)
- Per-client CHECKPOINT.md required for clients past intake phase
- Sensitive client material → vault/clients/<slug>/ as .age, never plaintext

Both files pass inline_includes.py --check.

Spec refs: §4 (Three personas), F10, F18, ADRs 010, 011.
EOF
)"
git push origin main
```

---

## Task 8: Pre-commit hook surface (4 sub-hooks)

**Goal:** Replace the symlinked `pre-commit` script (currently pointing at the secret-scan only) with an orchestrator that runs all four sub-hooks: secret-scan (existing), vault-age-only (new), docs-pair (basic — full surface in Plan 02), checkpoint-validation (new).

**Files:**
- Create: `infra/hooks/pre-commit-vault-age-only.sh`
- Create: `infra/hooks/pre-commit-docs-pair.sh`
- Create: `infra/hooks/pre-commit-checkpoint.sh`
- Create: `infra/hooks/pre-commit` (orchestrator — replaces the symlink-target logic)

- [ ] **Step 1: Write `pre-commit-vault-age-only.sh`**

Create `/srv/Nexostrat/infra/hooks/pre-commit-vault-age-only.sh`:

```bash
#!/usr/bin/env bash
# pre-commit-vault-age-only.sh — Nexostrat
#
# Refuse any staged file under vault/ that isn't:
#   - a .age file
#   - sensitive_index.md or README.md
#   - a .gitkeep
#
# This is belt-and-suspenders with .gitignore which already excludes
# plaintext under vault/ (matches *.pdf, *.docx, *.txt, *.md but
# !sensitive_index.md / !README.md / !.gitkeep).

set -uo pipefail

violations=0
mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR)

for f in "${staged[@]}"; do
  [[ "$f" =~ ^vault/ ]] || continue
  case "$f" in
    *.age) continue ;;
    vault/*/sensitive_index.md|vault/sensitive_index.md) continue ;;
    vault/*/README.md|vault/README.md) continue ;;
    */.gitkeep) continue ;;
    *)
      echo "BLOCKED: $f staged under vault/ but is not .age/index/README/.gitkeep"
      violations=$((violations+1))
      ;;
  esac
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Vault accepts only .age ciphertext (+ sensitive_index/README/.gitkeep)."
  echo "Encrypt the file first:"
  echo "  age -R infra/age-recipients.txt -o vault/<path>/file.age <plaintext>"
  echo "Hook: infra/hooks/pre-commit-vault-age-only.sh"
  exit 1
fi
exit 0
```

```bash
chmod +x /srv/Nexostrat/infra/hooks/pre-commit-vault-age-only.sh
```

- [ ] **Step 2: Write `pre-commit-docs-pair.sh` (basic — full surface in Plan 02)**

Create `/srv/Nexostrat/infra/hooks/pre-commit-docs-pair.sh`:

```bash
#!/usr/bin/env bash
# pre-commit-docs-pair.sh — Nexostrat (BASIC version; Plan 02 ships the full hook)
#
# In tier-1 folders (00_PARTNERSHIP/, 00_GOVERNANCE/, root README.md), if X.md
# is modified, X-explicado.md must also be staged (or vice versa). Escape
# hatch: 'docs-skip-pair' in the commit message body (handled by Plan 02).
#
# This basic version covers only the most rigid case (00_PARTNERSHIP/ +
# 00_GOVERNANCE/ + root README.md). docs/ tier-1 enforcement comes in Plan 02
# alongside the auto-generators.

set -uo pipefail

mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR)

violations=0

for f in "${staged[@]}"; do
  case "$f" in
    00_PARTNERSHIP/*.md|00_GOVERNANCE/*.md|README.md) ;;
    *) continue ;;
  esac

  # Skip already -explicado partners and the raised_hand_log
  case "$f" in
    *-explicado.md|*/raised_hand_log.md|*/CHANGELOG.md|*/DECISIONS.md) continue ;;
  esac

  partner="${f%.md}-explicado.md"

  # If partner exists in the working tree but is NOT staged → block
  if [[ -f "$partner" ]] && ! printf '%s\n' "${staged[@]}" | grep -qFx "$partner"; then
    echo "BLOCKED: $f modified but its partner $partner is not staged"
    violations=$((violations+1))
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Tier-1 docs require the -explicado partner to be staged in the same commit."
  echo "Either stage the partner, or use 'git commit --no-verify' if intentionally"
  echo "skipping the pair. (A 'docs-skip-pair' commit-body escape-hatch is planned"
  echo "for Plan 02; pre-commit hooks can't inspect the commit message yet, so for"
  echo "now --no-verify is the documented escape.)"
  echo "Hook: infra/hooks/pre-commit-docs-pair.sh"
  exit 1
fi
exit 0
```

```bash
chmod +x /srv/Nexostrat/infra/hooks/pre-commit-docs-pair.sh
```

- [ ] **Step 3: Write `pre-commit-checkpoint.sh`**

Create `/srv/Nexostrat/infra/hooks/pre-commit-checkpoint.sh`:

```bash
#!/usr/bin/env bash
# pre-commit-checkpoint.sh — Nexostrat
#
# Per ADR-031: empty CHECKPOINT.md commits refused unless they contain the
# token CHECKPOINT_NO_ACTIVE_WORK.
#
# "Empty" = file size < 100 bytes OR no body content beyond a heading.

set -uo pipefail

mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR | grep -E '(^|/)CHECKPOINT\.md$' || true)
[[ ${#staged[@]} -eq 0 ]] && exit 0

violations=0
for f in "${staged[@]}"; do
  [[ -f "$f" ]] || continue
  if grep -q 'CHECKPOINT_NO_ACTIVE_WORK' "$f"; then
    continue  # explicit no-active-work marker
  fi
  # File must have substantive content (≥ 200 bytes is an OK proxy)
  bytes=$(wc -c < "$f")
  if [[ "$bytes" -lt 200 ]]; then
    echo "BLOCKED: $f is too short (${bytes} bytes) and lacks CHECKPOINT_NO_ACTIVE_WORK token"
    violations=$((violations+1))
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Per ADR-031: CHECKPOINT.md must either have substantive content or"
  echo "explicitly contain the literal token: CHECKPOINT_NO_ACTIVE_WORK"
  echo "Hook: infra/hooks/pre-commit-checkpoint.sh"
  exit 1
fi
exit 0
```

```bash
chmod +x /srv/Nexostrat/infra/hooks/pre-commit-checkpoint.sh
```

- [ ] **Step 4: Write the orchestrator `pre-commit`**

The current `.git/hooks/pre-commit` is a symlink to `infra/hooks/pre-commit-secret-scan.sh`. Replace with a new orchestrator script (still under `infra/hooks/` for git-trackability) that runs all four sub-hooks.

Create `/srv/Nexostrat/infra/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
# pre-commit — Nexostrat orchestrator
#
# Runs all sub-hooks under infra/hooks/pre-commit-*.sh in order. Fails fast on
# the first non-zero exit.

set -uo pipefail
HOOKS_DIR="/srv/Nexostrat/infra/hooks"

for hook in \
  "$HOOKS_DIR/pre-commit-secret-scan.sh" \
  "$HOOKS_DIR/pre-commit-vault-age-only.sh" \
  "$HOOKS_DIR/pre-commit-docs-pair.sh" \
  "$HOOKS_DIR/pre-commit-checkpoint.sh"
do
  if [[ ! -x "$hook" ]]; then
    echo "WARN: $hook not executable; skipping" >&2
    continue
  fi
  if ! bash "$hook"; then
    echo
    echo "Pre-commit halted at: $hook"
    exit 1
  fi
done

exit 0
```

```bash
chmod +x /srv/Nexostrat/infra/hooks/pre-commit
```

- [ ] **Step 5: Re-symlink `.git/hooks/pre-commit` to the orchestrator**

```bash
cd /srv/Nexostrat
ln -sf ../../infra/hooks/pre-commit .git/hooks/pre-commit
ls -la .git/hooks/pre-commit
# Expected: symlink → ../../infra/hooks/pre-commit
```

- [ ] **Step 6: Quick smoke tests of each sub-hook**

Vault-age-only:

```bash
echo "fake plaintext" > /srv/Nexostrat/vault/keys/.test-violation
git add /srv/Nexostrat/vault/keys/.test-violation
git commit -m "should be blocked" 2>&1 | tail -5
# Expected: BLOCKED line, exit non-zero

git restore --staged /srv/Nexostrat/vault/keys/.test-violation
rm /srv/Nexostrat/vault/keys/.test-violation
```

Docs-pair (intentionally skip — verifying the basic version works in the integration smoke test below).

Checkpoint:

```bash
# Back up the REAL CHECKPOINT.md (NOT an empty stub — the earlier draft had
# the cp source/dest reversed, which silently destroyed the real file on
# restore). Assertions guard both ends.
cp /srv/Nexostrat/CHECKPOINT.md /srv/Nexostrat/CHECKPOINT.md.bak
[[ -s /srv/Nexostrat/CHECKPOINT.md.bak ]] || { echo "ABORT: empty backup (CHECKPOINT.md was already empty?)"; exit 1; }

echo "" > /srv/Nexostrat/CHECKPOINT.md
git add /srv/Nexostrat/CHECKPOINT.md
git commit -m "should be blocked" 2>&1 | tail -5
# Expected: BLOCKED — too short, no token

# Restore
mv /srv/Nexostrat/CHECKPOINT.md.bak /srv/Nexostrat/CHECKPOINT.md
[[ -s /srv/Nexostrat/CHECKPOINT.md ]] || { echo "ABORT: restore failed — CHECKPOINT.md is empty"; exit 1; }
git restore --staged /srv/Nexostrat/CHECKPOINT.md
```

- [ ] **Step 7: Stage + commit**

```bash
git add infra/hooks/pre-commit \
        infra/hooks/pre-commit-vault-age-only.sh \
        infra/hooks/pre-commit-docs-pair.sh \
        infra/hooks/pre-commit-checkpoint.sh

git commit -m "$(cat <<'EOF'
Plan 01c Task 8 · pre-commit hook surface (4 sub-hooks + orchestrator)

infra/hooks/pre-commit is the new orchestrator — runs each sub-hook in
order, fails fast on first non-zero exit.

Sub-hooks:
1. pre-commit-secret-scan.sh    (already shipped in 01a)
2. pre-commit-vault-age-only.sh (refuses non-.age in vault/, with allowlist
                                 for sensitive_index/README/.gitkeep)
3. pre-commit-docs-pair.sh      (basic — tier-1 X.md needs X-explicado.md
                                 staged. Plan 02 ships full version with
                                 docs/ enforcement + 'docs-skip-pair' escape)
4. pre-commit-checkpoint.sh     (per ADR-031: empty CHECKPOINT.md refused
                                 unless CHECKPOINT_NO_ACTIVE_WORK token)

.git/hooks/pre-commit re-symlinked to the orchestrator.

Spec refs: §3 (Guards), §4.6 (docs-pair), §4.10 (CHECKPOINT), R4, ADRs 008,
014, 025, 031.
EOF
)"
git push origin main
```

---

## Task 9: F27 follow-through + STATUS.md template integration

**Goal:** F27 closure: confirm STATUS.md (root + persona-level) carries no Hosted-mode references. Confirm `00_META/shared/STATUS.md` template is the canonical version. Run a full repo grep.

**Files:**
- Modify: `STATUS.md` (if any Hosted-leak found)
- Possibly Modify: `skills/STATUS.md` and `pipeline/STATUS.md` if they were created prematurely

- [ ] **Step 1: Grep for Hosted references**

```bash
grep -rE 'Hosted|jp-hosted|hosted-mode' /srv/Nexostrat/ \
  --exclude-dir={.git,.superpowers,.claude} \
  --exclude='*.docx' --exclude='*.pdf'
# Expected: empty (or only matches inside Plan 01a/01b/01c plan files
#           where they describe the dropping of the Hosted option).
```

If anything else matches (e.g., a leftover STATUS.md sentence saying "JP Hosted onboarding"), edit it out.

- [ ] **Step 2: Confirm `infra/machines/jp-light.yaml` doesn't reference Hosted**

```bash
grep -i hosted /srv/Nexostrat/infra/machines/*.yaml
# Expected: empty
```

- [ ] **Step 2b: Signal sweep (per 2026-05-16 Telegram-only directive)**

The Plan 01c re-audit (2026-05-16) flagged `jp-heavy.yaml` still listing
`signal` in `desktop_apps` (M8 — pre-existing debt from before the
Telegram-not-Signal lock). That entry was removed in commit landing the
Plan 01c re-audit MEDIUM patches; this step verifies no other Nexostrat
artifact carries Signal references as a documented in-system channel.
Historical mentions in plans/proposals/journal/handoff-archive are
intentionally preserved (they describe what was; current code+config
is what is).

```bash
grep -rn -i signal /srv/Nexostrat/ \
  --include='*.yaml' --include='*.md' --include='*.sh' --include='*.py' \
  --exclude-dir={.git,.superpowers,.claude,00_META/plans,00_META/proposals,00_META/journal,00_META/handoff/archive}
# Expected: empty (or only matches in actively-edited plan body referencing the
# 2026-05-16 directive itself).
```

If anything else matches, edit it out (or replace with "agreed personal
channel" / "out-of-band" wording).

- [ ] **Step 3: If anything was edited in Step 1 or Step 2b, stage + commit**

```bash
# Only if changes were made:
git status --short
git add <files>
git commit -m "Plan 01c Task 9 · F27 follow-through + Signal-residue sweep"
git push origin main
```

If nothing was edited, this task is a verification-only no-op — skip the commit and just record a one-line update in STATUS.md Recent activity at Task 11.

---

## Task 10: Integration smoke test (R2 rich version)

**Goal:** Implement `infra/scripts/smoke-test.sh` that runs all 6 success-criterion checks end-to-end. Per R2, this is the rich version: real decrypt round-trip, real `git push` + verify GitHub HEAD, real warm-rsync trigger, leak detection, drift detection, schema validation.

**Files:**
- Create: `infra/scripts/smoke-test.sh`

- [ ] **Step 1: Implement the smoke test**

Create `/srv/Nexostrat/infra/scripts/smoke-test.sh`:

```bash
#!/usr/bin/env bash
# smoke-test.sh — Nexostrat (R2)
#
# End-to-end integration smoke test for the foundation milestone.
# Runs 6 sub-tests; each prints a clear PASS/FAIL line. Exit 0 only if all green.

set -uo pipefail

REPO="/srv/Nexostrat"
PASS=0; FAIL=0
echo "============================================================"
echo "Nexostrat smoke test  ($(date -Iseconds))"
echo "============================================================"

ok()  { echo "  PASS  $1"; PASS=$((PASS+1)); }
no()  { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

# ---- 1. Crypto round-trip -------------------------------------------------
echo
echo "[1/6] Decrypt round-trip on secrets.env.age"
TMP=/dev/shm/smoke-test-secrets-$$
if age -d -i "$HOME/.config/age/nexostrat.key.age" \
        "$REPO/secrets.env.age" > "$TMP" 2>/dev/null \
   && grep -q 'ANTHROPIC_API_KEY' "$TMP"; then
  ok "secrets.env.age decrypts and contains expected key"
else
  no "secrets.env.age decrypt failed"
fi
shred -u "$TMP" 2>/dev/null || rm -f "$TMP"

# Re-encrypt round-trip to confirm both recipients still work
TMP_PT=/dev/shm/smoke-pt-$$.txt
TMP_CT=/dev/shm/smoke-ct-$$.age
TMP_DEC=/dev/shm/smoke-dec-$$.txt
echo "smoke-test $(date -Iseconds)" > "$TMP_PT"
if age -R "$REPO/infra/age-recipients.txt" -o "$TMP_CT" "$TMP_PT" \
   && age -d -i "$HOME/.config/age/nexostrat.key.age" "$TMP_CT" > "$TMP_DEC" \
   && diff -q "$TMP_PT" "$TMP_DEC" >/dev/null; then
  ok "encrypt-to-recipients + decrypt-with-Ricardo-key round-trip"
else
  no "round-trip failed"
fi
shred -u "$TMP_PT" "$TMP_CT" "$TMP_DEC" 2>/dev/null || rm -f "$TMP_PT" "$TMP_CT" "$TMP_DEC"

# ---- 2. Mirror HEAD parity (no-commit; uses current state) ---------------
# Earlier draft pushed a smoke-test commit to verify convergence; that
# (a) polluted main history with a permanent smoke-test <ts> commit per
# run, and (b) silently false-positived when the pre-commit hook refused
# the commit (HEAD unchanged → convergence loop trivially succeeded).
# Plan 01b already proved end-to-end convergence (3 s GitHub / 8 s
# Codeberg at d38e865). This sub-test just asserts the mirrors are at
# current HEAD — if the path-watchers fell behind, this catches it
# without mutating main.
echo
echo "[2/6] GitHub + Codeberg mirror HEAD parity"
cd "$REPO"
LOCAL=$(git rev-parse HEAD)
GH=$(git ls-remote github main 2>/dev/null | awk '{print $1}')
CB=$(git ls-remote codeberg main 2>/dev/null | awk '{print $1}')
if [[ "$GH" == "$LOCAL" && "$CB" == "$LOCAL" ]]; then
  ok "GitHub + Codeberg at HEAD ($LOCAL) without intervention"
else
  no "mirror not in sync: GH=$GH CB=$CB local=$LOCAL"
fi

# ---- 3. Warm-rsync real-trigger ------------------------------------------
# Plan 01b Tasks 7-12 (warm-standby cluster, including this unit) were
# DEFERRED 2026-05-16; tag landed v0.1b-mirrors-only. The warm-rsync
# unit doesn't exist until t-plan-01b-execute-warm-standby completes
# (gated on physical second host; due 2026-06-30). Gate this sub-test
# on unit presence and SKIP-not-FAIL when absent — v0.1-foundation can
# tag at 5-PASS + 1-SKIP. The SKIP becomes PASS once the warm-standby
# cluster lands.
echo
echo "[3/6] warm-rsync real trigger"
if ! systemctl cat nexostrat-warm-rsync.service >/dev/null 2>&1; then
  echo "  SKIP  nexostrat-warm-rsync.service not installed"
  echo "        (Plan 01b Tasks 7-12 deferred to t-plan-01b-execute-warm-standby;"
  echo "         gates on physical second host; due 2026-06-30)"
else
  sudo systemctl start nexostrat-warm-rsync.service 2>/dev/null
  sleep 5
  RES=$(sudo systemctl show nexostrat-warm-rsync.service --property=Result --value 2>/dev/null)
  RC=$(sudo systemctl show nexostrat-warm-rsync.service --property=ExecMainStatus --value 2>/dev/null)
  if [[ "$RES" == "success" && "$RC" == "0" ]]; then
    ok "warm-rsync.service Result=success ExecMainStatus=0"
  else
    no "warm-rsync.service Result=$RES ExecMainStatus=$RC"
  fi
fi

# ---- 4. run-with-secrets.sh leak check -----------------------------------
# The wrapper calls `age -d -i $PRIV_KEY_AGE` which prompts on /dev/tty.
# Under TTY-less execution (subagent-driven-development, scripted runs)
# the wrapper hangs at the prompt and never decrypts — INTRA stays 0,
# POST stays 0, the test silently false-positives. TTY-gate the check
# and assert INTRA>0 before declaring PASS so the leak path is actually
# exercised. Companion item tracked in t-plan-01a-jp-and-tty-deferred.
echo
echo "[4/6] run-with-secrets.sh /dev/shm leak check"
if [ ! -t 0 ] || [ ! -t 1 ]; then
  echo "  SKIP  no TTY; leak check requires interactive passphrase entry"
  echo "        (run via t-plan-01a-jp-and-tty-deferred TTY-side rerun)"
else
  "$REPO/infra/scripts/run-with-secrets.sh" sh -c 'sleep 60' &
  WPID=$!
  sleep 5
  INTRA=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | wc -l)
  kill $WPID 2>/dev/null
  pkill -P $WPID 2>/dev/null
  sleep 1
  POST=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | wc -l)
  if [[ $INTRA -eq 0 ]]; then
    no "wrapper never decrypted — INTRA=0 (passphrase not entered or wrapper broken)"
  elif [[ $POST -eq 0 ]]; then
    ok "no /dev/shm leak after wrapper exit (intra-run had $INTRA as expected)"
  else
    no "leftover plaintext in /dev/shm: $POST file(s)"
    rm -f /dev/shm/nexostrat-secrets-*
  fi
fi

# ---- 5. Inliner drift across all 6 persona files -------------------------
echo
echo "[5/6] inline_includes.py drift check across 6 persona files"
DRIFT=0
for pair in \
  "00_META/templates/CLAUDE.md.tmpl  CLAUDE.md" \
  "00_META/templates/GEMINI.md.tmpl  GEMINI.md" \
  "00_META/templates/skills_CLAUDE.md.tmpl  skills/CLAUDE.md" \
  "00_META/templates/skills_GEMINI.md.tmpl  skills/GEMINI.md" \
  "00_META/templates/pipeline_CLAUDE.md.tmpl  pipeline/CLAUDE.md" \
  "00_META/templates/pipeline_GEMINI.md.tmpl  pipeline/GEMINI.md"
do
  read -r tmpl out <<<"$pair"
  if ! python3 "$REPO/infra/scripts/inline_includes.py" \
        --template "$REPO/$tmpl" --check "$REPO/$out" >/dev/null 2>&1; then
    DRIFT=$((DRIFT+1))
    echo "    DRIFT: $out vs $tmpl"
  fi
done
if [[ $DRIFT -eq 0 ]]; then
  ok "all 6 persona files in sync with templates"
else
  no "$DRIFT persona file(s) drifted"
fi

# ---- 6. JSON schema validation -------------------------------------------
echo
echo "[6/6] tasks.json + calendar.json schema validation"
if bash "$REPO/infra/scripts/validate_schemas.sh" >/dev/null 2>&1; then
  ok "both files validate against their schemas"
else
  no "schema validation failed"
fi

# ---- Summary --------------------------------------------------------------
echo
echo "============================================================"
echo "  Result: $PASS pass, $FAIL fail"
echo "============================================================"
[[ $FAIL -eq 0 ]] || exit 1
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/smoke-test.sh
```

- [ ] **Step 2: Stage + commit**

```bash
git add infra/scripts/smoke-test.sh
git commit -m "$(cat <<'EOF'
Plan 01c Task 10 · integration smoke test (R2 rich version)

infra/scripts/smoke-test.sh runs 6 end-to-end sub-tests:
1. Crypto round-trip — secrets.env.age decrypts; encrypt-to-recipients +
   decrypt-with-Ricardo-key round-trip works
2. Mirror push + GitHub HEAD parity within 60s
3. warm-rsync real trigger Result=success ExecMainStatus=0
4. run-with-secrets.sh leaves no /dev/shm leak after exit
5. inline_includes.py --check drift-free across all 6 persona files
6. tasks.json + calendar.json validate against schemas

Per R2: replaces the original Plan-01 thin smoke. Each sub-test prints clear
PASS/FAIL; exit 0 only if all green.

Spec refs: §10.1 (testing), R2.
EOF
)"
git push origin main
```

---

## Task 11: Run smoke test, verify GREEN, tag `v0.1-foundation`

**Goal:** End-to-end run of `smoke-test.sh`. Must be all-PASS before tagging. Then tag, push, update STATUS/tasks/CHECKPOINT, declare foundation milestone reached.

- [ ] **Step 1: Run the smoke test**

```bash
bash /srv/Nexostrat/infra/scripts/smoke-test.sh
```

Expected: 5 × PASS + 1 × SKIP (warm-rsync), "Result: 5 pass, 0 fail, 1 skip", exit 0. The SKIP becomes PASS once `t-plan-01b-execute-warm-standby` lands (Plan 01b Tasks 7-12 on a physical second host). Sub-test [4/6] additionally SKIPs under TTY-less execution; the operator running the tag step interactively will see it PASS.

If anything is FAIL:
- Re-read the output, identify which sub-test failed
- Fix the underlying issue (re-run individual checks via the corresponding script)
- Re-run smoke test until all green (FAIL → PASS or SKIP).

Do NOT tag until every sub-test is PASS or a documented SKIP. A SKIP must
correspond to a tracked deferred task (e.g., [3] → `t-plan-01b-execute-warm-standby`;
[4] → `t-plan-01a-jp-and-tty-deferred` for the TTY-side rerun).

- [ ] **Step 2: Update `STATUS.md` to reflect Plan 01c done + foundation milestone reached**

Edit `/srv/Nexostrat/STATUS.md`:
- "Current state": Plan 01c done; v0.1-foundation tagged; foundation milestone reached.
- "Next sequence" Step 1: Plan 02 (documentation system) — write via writing-plans skill, then re-audit + execute.
- Move all foundation-related items from Open follow-ups → done.
- Update Recent activity with Plan 01c summary.

- [ ] **Step 3: Update `tasks.json`**

- Mark `t-plan-01c-execute` done.
- Mark `t-amendments-batch-2` done (Plan 01c is the third of three).
- Add `t-plan-02-write` if not already there (Plan 02 is the next critical action).

- [ ] **Step 4: Update root `CHECKPOINT.md`**

Rewrite the baton:
- "What I just did": Plan 01c complete; foundation milestone reached; v0.1-foundation tagged.
- "In flight — concrete next action": Write Plan 02 via writing-plans skill.
- "Blocked on": Nothing.

- [ ] **Step 5: Tag and push**

```bash
cd /srv/Nexostrat
git tag -a v0.1-foundation -m "$(cat <<'EOF'
Nexostrat foundation milestone — v0.1-foundation

Closes the original Plan-01 milestone, reached at the end of the 3-plan
split (01a → 01b → 01c).

All Plan 01c success criteria green (smoke-test.sh):
[1] Crypto round-trip PASS
[2] GitHub + Codeberg mirror HEAD parity PASS
[3] warm-rsync real trigger SKIP (Plan 01b Tasks 7-12 deferred; t-plan-01b-execute-warm-standby due 2026-06-30) — becomes PASS once warm-standby lands
[4] run-with-secrets.sh /dev/shm leak check PASS (or SKIP under TTY-less execution; see t-plan-01a-jp-and-tty-deferred)
[5] inline_includes.py drift-free across 6 persona files PASS
[6] tasks.json + calendar.json schema validation PASS

Persona surface complete:
- Founder       (root CLAUDE.md + GEMINI.md)
- Skills-Master (skills/CLAUDE.md + GEMINI.md)
- Client-Owner  (pipeline/CLAUDE.md + GEMINI.md)

Hook surface complete (basic):
- secret-scan, vault-age-only, docs-pair (basic), checkpoint validation

Audit findings closed per plan (cumulative from the 2026-05-13 founding-spec audit + each plan's re-audit):
  Plan 01a closed: C1 (process-sub leak), C2 (recipients/JP-roundtrip key-on-file),
                   F5 (partnership artifact — by alternate-satisfaction markdown),
                   F11 (3-bucket scaffold), F12 (gitignore comprehensive),
                   F13 (machine profiles), F15 (questionnaire pandoc),
                   F16 (pipeline _template state.json), F17 (skills canonical layout),
                   F19 (per-client checkpoint), F21 (JSON schemas + validator),
                   F23 (.gitignore secrets discipline), F26 (bootstrap-machine.sh),
                   R3 (Stage 1 surface area minimization), R5 (deferred-Hosted path),
                   R6 (calendar honesty)
  Plan 01b closed: C4 (Gitea-internal hook decrypt impossibility → host-side path-watcher),
                   F7 (Codeberg mirror missing from original Plan 01),
                   F22 (Gitea bare-repo on-disk verification, n8n removed),
                   F24 (real systemctl start vs --dry-run),
                   F25 (firm-namespace topology nexostrat/nexostrat on both mirrors)
  Plan 01c closed: C3 (canonical-shared-stanzas inliner — drift detection),
                   F8 (nexostrat-memos.py + per-persona inboxes),
                   F10 (vault namespace split per persona scope),
                   F18 (persona ownership table resolved by F10),
                   F20 (BRAIN_STATUS / 00_TEMPLATES leak audit — Task 1 gate),
                   F27 (Hosted-option follow-through — STATUS template scope),
                   R2 (rich integration smoke test — 6 sub-tests),
                   R4 (CHECKPOINT mtime concurrent-session warning — MVP)

Remaining audit work: post-Plan-01c polish-pass collects the LOW findings
deferred from each re-audit (Plan 01a re-audit MEDIUM/LOW residue,
Plan 01b re-audit L1-L5, Plan 01c re-audit L1-L6). Cost-table amendment
folded into the 2026-05-16 ADR-038 sweep (commit 1b2f653).

Next: Plan 02 (Documentation System).
EOF
)"

git add STATUS.md tasks.json CHECKPOINT.md
git commit -m "$(cat <<'EOF'
Plan 01c Task 11 · foundation milestone reached, tagged v0.1-foundation

All Plan 01c success criteria verified green via smoke-test.sh (6/6 PASS).

STATUS.md, tasks.json, CHECKPOINT.md updated to reflect:
- Plan 01a/01b/01c all DONE
- v0.1-foundation tagged
- Foundation work complete; Plan 02 (Documentation System) next

The 28 audit findings + 6 recommendations from 2026-05-14_audit-report.md
are closed (or documented as future cycle items).
EOF
)"

git push origin main
git push origin v0.1-foundation
```

- [ ] **Step 6: Final verification**

```bash
git tag | grep -E 'v0\.1[abc]?-'
# Expected:
#   v0.1-foundation
#   v0.1a-foundation
#   v0.1b-mirrors-only
# (v0.1b-mirrors will appear later when the warm-standby cluster lands)

git log --oneline -10
# Expected: recent commits all pushed, working tree clean

bash /srv/Nexostrat/infra/scripts/smoke-test.sh | tail -5
# Expected: "Result: 6 pass, 0 fail" — re-run as final sanity-check
```

---

## Self-Review

**Spec coverage** — Every Plan 01c deliverable from the master-index header maps to a task:

- 9 canonical shared stanzas + F20 leak audit + F27 follow-through → Task 1, Task 9
- inline_includes.py (C3) → Task 2
- nexostrat-memos.py (F8) → Task 3
- checkpoint-mtime-check.sh (R4) → Task 4
- 6 persona files (Founder + Skills-Master + Client-Owner; CLAUDE + GEMINI each) → Tasks 5, 6, 7
- F10 vault namespace reflected in persona scope sections → Tasks 5, 6, 7
- Pre-commit hook surface (secret + vault + docs-pair + checkpoint) → Task 8
- Rich smoke test (R2) → Task 10
- 00_META/shared/STATUS.md template (F27) → Task 1
- v0.1-foundation tag → Task 11

**Placeholder scan** — Every step has actual content. The persona templates use `{{include: ../shared/<stanza>.md}}` markers — these are the literal payload of the inliner, not placeholders.

**Type consistency** — `MARKER` regex in `inline_includes.py` (Task 2) matches the `{{include: path}}` syntax used in templates (Tasks 5-7). Sub-hook script paths in the orchestrator (Task 8 Step 4) match the file names created in Task 8 Steps 1-3. Persona name strings in `nexostrat-memos.py` (Task 3) match the `to:` field values used in `shared/memo_protocol.md` (Task 1 Step 6).

**Missing items found in self-review** — none.

---

## Execution handoff

Plan complete and saved to `00_META/plans/2026-05-14_plan-01c-personas.md`.

**Recommended execution path: subagent-driven** (`superpowers:subagent-driven-development`).

- All 11 tasks can run in a single session (no JP coordination, no physical-host gating).
- Estimated effort: 4-6 hours. Heaviest tasks are Task 1 (writing 9 stanzas + STATUS template) and Task 8 (4 hooks + orchestrator).
- Pre-flight checks at the top of this plan run once.

**Inline execution** also viable — `superpowers:executing-plans` with checkpoints at Tasks 4, 8, 10, 11.

---

*This plan inherits audit findings F8, F10, F18 (resolved by F10), F20, F27, C3, R2, R4. Plus closes the original Plan-01 milestone via the v0.1-foundation tag (replacing the SUPERSEDED single-plan version). Plans 02-10 follow per the master plan index, written just-in-time.*
