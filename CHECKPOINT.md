# CHECKPOINT — root (Founder)

**Updated:** 2026-05-19T21:30:00-07:00
**By:** ricardo (via Claude Code session 7 at /srv/Nexostrat/)
**Persona:** Founder
**Session topic:** Plan 02a Chunk B executed end-to-end via `superpowers:subagent-driven-development` · 21 commits · final review APPROVED FOR CHUNK C with timers masked + 3 follow-ups

## What just happened (last session — read once, don't re-litigate)

Multi-hour single-arc session executing Plan 02a Chunk B. Pattern: dispatch implementer subagent per plan task (file work + static checks + commit) → main session runs live API verification under `run-with-secrets.sh` (TTY needed for age passphrase) → spec + quality review subagents → fold in fixes → move on. Seven plan tasks (4–10) + 3 inline-fix waves landed.

**Result:** Baserow has 4 tables (clients/meetings/deliverables/financials) × 45 user-defined fields × 11 predefined views, all populated via idempotent migrations. `infra/baserow/migrations/_api.py` does JWT schema work; `skills/shared/baserow.py` does Token row CRUD with `@_safe` discipline. `new-client.sh` posts client rows on scaffold; all 5 skill renderers post deliverables on .docx write; `baserow-reconcile.sh` nightly catches orphans; weekly schema-drift check protects canonical.json. 16 tests pass across `tests/foss_stack/` + `skills/shared/tests/`.

**Important deviation from plan-as-written:** The two installed nightly timers (reconcile @ 03:30, schema-check @ Mondays 04:00) are **masked** — they would have hung tonight on age passphrase prompt under systemd (no TTY). Final review's Important #1; addressed in follow-up task `t-plan-02a-chunk-b-systemd-creds` (high, due 2026-06-01). Until that lands, both routines are manual cadence: `/srv/Nexostrat/infra/scripts/run-with-secrets.sh /srv/Nexostrat/infra/scripts/baserow-reconcile.sh` (and same for schema-check).

## Decisions locked this session

1. **Two-helper-per-tool pattern.** Schema lives in `infra/<tool>/migrations/_api.py` (JWT, longer timeouts, prints, no @_safe). Runtime lives in `skills/shared/<tool>.py` (Token, shorter timeouts, @_safe never-raise, env-var table-id cache). When BookStack lands in Chunk C and Odoo someday lands, mirror the shape.

2. **Env-var table-id convention.** Database tokens are scoped to `/api/database/rows/...` only — can't list workspaces/databases/tables. Discovery happens once via JWT (`infra/scripts/write-baserow-table-ids.sh`), IDs persist as `BASEROW_TABLE_<NAME>_ID` in `secrets.env.age`, runtime helper reads from env. Pattern lifts to any tool with the same scope split.

3. **Dual-mode wrapper invocation.** Scripts that may be called both manually AND from inside an outer `run-with-secrets.sh` (pytest tests, in particular) detect already-sourced env and skip the wrapper to avoid nested age prompts. `new-client.sh` and `baserow-reconcile.sh` both use the pattern. Lift to a sourceable helper before the 3rd script appears.

4. **`@_safe` decorator for renderer-adjacent helpers.** Anything that runs inside a renderer's `__main__` block must never crash the renderer. `@_safe` catches all exceptions, logs `[baserow] <fn>: <err>` to stderr, returns None. Plan 04 Telegram-notify, BookStack-page-create, future event-emit calls all follow this pattern.

5. **Idempotency strategies differ by entity and that's intentional.** `post_client` finds-by-slug → returns existing id WITHOUT updating (slug is stable identity). `post_deliverable` finds-by-file_md → PATCHes existing (re-renders are real). `post_meeting` always INSERTs (meetings legitimately repeat). Documented per-function in `t-plan-02a-chunk-b-test-coverage` (test #3) — encode the asymmetry as invariants.

6. **Skill 05's renderer hook placement is wrong.** Lives in `main()` while skills 01-04 are in `if __name__ == '__main__':`. Both fire under script invocation, but the placements diverge — if anything ever imports `generate_docx.main()` (e.g., Plan 03 event router), skill 05 emits a deliverables row, skills 01-04 don't. Fix bundled with the hook-lift in follow-up task `t-plan-02a-chunk-b-renderer-hook-lift`.

7. **Test infrastructure baseline.** `python3-pytest` is now installed system-wide via apt (Linux Mint package python3-pytest 7.4.4). Tests under `tests/foss_stack/` and `skills/shared/tests/` skip cleanly when run outside `run-with-secrets.sh`; pass when run inside.

## Stack state (live & verifiable next session)

```
HP (ricardo-hp-laptop, Tailscale 100.64.121.80) — unchanged from session 6:
  baserow + bookstack + bookstack-db + caddy all healthy.
  systemd nexostrat-foss-stack.service enabled (boot-on-start).

Baserow new state (this session):
  Workspace "Nexostrat" (id=107)
  Database "nexostrat" (id=117)
    clients      (id=571) — 17 spec fields + Name primary + 3 link backrefs
    meetings     (id=572) — 11 spec fields + Name primary
    deliverables (id=573) — 9 spec fields + Name primary
    financials   (id=574) — 8 spec fields + Name primary
  11 views (3+3+3+2) — all idempotent, orphan-filter-recovery in place.

Secrets file additions (in secrets.env.age):
  BASEROW_EMAIL=contacto@nexostrat.com
  BASEROW_PASSWORD=...
  BASEROW_TABLE_CLIENTS_ID=571
  BASEROW_TABLE_MEETINGS_ID=572
  BASEROW_TABLE_DELIVERABLES_ID=573
  BASEROW_TABLE_FINANCIALS_ID=574

Systemd timers installed AND MASKED (manual cadence until t-plan-02a-chunk-b-systemd-creds):
  nexostrat-baserow-reconcile.timer       (would-be 03:30 nightly)
  nexostrat-baserow-schema-check.timer    (would-be Mondays 04:00)

Schema snapshot: infra/baserow/schema/canonical.json (449 LOC, sorted, deterministic).
```

## In flight — concrete next actions

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads CHECKPOINT + STATUS + tasks + calendar + latest journal
     (00_META/journal/2026-05-19_plan-02a-chunk-b-execution.md).
  4. Ricardo decides arc.

CRITICAL PATH UNCHANGED:

  ┌── 2026-05-25 1pm Tijuana ─────────────────────────────┐
  │  REUNIÓN TRIXX LOGISTICS                               │
  │  (t-trixx-meeting-execution, critical)                 │
  │  Materiales intactos en Desktop (4 PDFs + PrepLlamada) │
  │  Pipeline cliente sin cambios session 7                │
  └─────────────────────┬──────────────────────────────────┘
                        │
  ┌── 2026-05-27 ─▼─────────────────────────────────────────┐
  │  SKILL 05 (Opportunity Report)                          │
  │  (t-trixx-skill-05-opportunity-report, high)            │
  │  Consume: 4 reportes + grabación + notas reunión        │
  │  → Revisión Ricardo+JP (Fase 5) → entrega (Fase 6)      │
  └─────────────────────────────────────────────────────────┘

PARALLEL TRACK — Chunk B follow-ups (highest priority of architecture work):

  ┌── 2026-06-01 ─┐
  │  t-plan-02a-chunk-b-systemd-creds (high)                │
  │  Write /etc/nexostrat/baserow.env mode 0640 owned by    │
  │  ricardo, scoped to row-CRUD only (BASEROW_URL +        │
  │  BASEROW_API_TOKEN + BASEROW_TABLE_*_ID, NOT email/     │
  │  password). Swap both systemd unit ExecStart to use     │
  │  EnvironmentFile= instead of run-with-secrets.sh.       │
  │  Add a sync script that regenerates the unencrypted     │
  │  file from the age vault on token rotation.             │
  │  systemctl unmask + enable --now both timers after.     │
  │  ~30-45 min.                                             │
  └───────────────┘

  ┌── 2026-06-10 ─┐
  │  t-plan-02a-chunk-b-renderer-hook-lift (medium)         │
  │  Lift 27-LOC inline hook from 5 renderers into          │
  │  skills/shared/baserow.py:post_from_render(md, docx,    │
  │  skill_name). Each renderer becomes 1 line. Also        │
  │  relocate skill 05's hook from main() → __main__ for    │
  │  consistency with 01-04.                                 │
  │  ~45 min including test re-run.                          │
  └───────────────┘

  ┌── 2026-06-10 ─┐
  │  t-plan-02a-chunk-b-test-coverage (medium)              │
  │  4 small test additions: skills 02-05 e2e parametrize   │
  │  (~50 LOC), _find_one filter-syntax regression (~10 LOC),│
  │  post_client no-overwrite invariant (~15 LOC), reconcile│
  │  + render dedupe cooperation (~20 LOC).                  │
  │  ~30 min including run-with-secrets pytest verification. │
  └───────────────┘

CHUNK C — next major arc (architecture):

  ┌── 2026-06-12 ─┐
  │  t-plan-02a-execute-chunk-c (medium)                    │
  │  Plan 02a Tasks 11-20: BookStack 4 shelves + 9 books +  │
  │  7 seeded pages (Spanish content), backup scripts +     │
  │  nightly 02:30 timer, 3 recovery scripts (restore-      │
  │  baserow, restore-bookstack, baserow-rotate-token),     │
  │  sync-state-from-baserow.sh, 5 runbooks, hp_down.md     │
  │  extension, smoke-test extension with 7 new checks, e2e │
  │  integration test, master index update + tag            │
  │  v0.2a-foss-stack. ~1h subagent-driven OR ~2h inline.   │
  │  Recommended: do the 3 follow-ups FIRST so timers are   │
  │  live again when backup timer joins them.                │
  └───────────────┘

  ┌── 2026-06-30 ─┐
  │  t-plan-02b-write (medium)                              │
  │  Just-in-time write via writing-plans skill. Scope:     │
  │  docs/ Diátaxis + drift hook + 5 auto-generators + 15   │
  │  ADRs 021-035 + 10 how-tos + paired -explicado.md.      │
  └───────────────┘

OTHER OPEN (unchanged from session 6 unless noted):
  - t-vault-backup-foss-env (medium, due 2026-06-30) — plan defect
    to correct before warm-standby useful
  - t-whatsapp-andrea-audiencia (high, due 2026-05-23) — optional
  - t-practice-meeting-jp (low, due 2026-05-24) — optional
  - t-migrate-pilotos-to-clients (medium, due 2026-05-30) — parallel
  - t-presentation-refresh-post-adr-038 (high, due 2026-06-01)
```

## Architecture-conflict check (passed)

| Decision session 7 | Verification |
|---|---|
| Two helpers (JWT schema + Token rows) instead of one | Matches Baserow's auth scope reality — Database Token cannot list workspaces. Documented in both files. |
| Env-var table-id pattern | Pragmatic given Database Token's scope; simpler than running JWT in every script. write-baserow-table-ids.sh discovers + persists. |
| Schema-strip Notes+Active, keep Name primary | Stage 1 acceptable — Name is Baserow's mandatory primary; primary-swap via change_primary_field is out of scope. |
| Inline plan defects patched in commits, not deferred | Matches "do it right, do it once" + "complete or nothing" feedback memories. Each commit message records the *why*. |
| Mask timers instead of fix-credentials-now | Conditional approval from final review. Time-boxed: t-plan-02a-chunk-b-systemd-creds is high priority due 2026-06-01. |
| Skill 05 hook placement diverges from 01-04 | Implementer flagged; final review flagged; bundled into hook-lift follow-up task. Doesn't break Stage 1 — `main()` is called from `if __name__ == '__main__':` in skill 05 too, just one level deeper. |

## Blocked on

**Next-session priority 1 (Trixx meeting):** nada del lado nuestro — materiales intactos en Ricardo's Desktop, espera lunes 2026-05-25 1pm Tijuana.

**Chunk B follow-up tasks (3):** Ricardo can pick when to land. Recommended order: systemd-creds → hook-lift → test-coverage. Each independent of the others; systemd-creds is the most operationally pressing (re-enables timers).

**Chunk C execution:** technically can start without the follow-ups; pragmatically better to land systemd-creds first so the Chunk C nightly backup timer (02:30) joins a healthy timer ecosystem. ~30-45 min upfront for systemd-creds is worth it.

**Warm-standby Tasks 7-12 Plan 01b:** physical second host (unchanged).

## Open questions (no blocking)

1. **systemd creds path.** Cleanest is `/etc/nexostrat/baserow.env` mode 0640 owned by `ricardo:ricardo`, sourced via systemd's `EnvironmentFile=`. Should there also be a sops-encrypted variant for off-host deploys later? For Stage 1, unencrypted on a Tailscale-only HP is fine — same blast radius as the unencrypted plaintext `infra/docker/foss-stack/.env` already on disk.

2. **Pytest installed system-wide.** Used `sudo apt install python3-pytest`. If we ever need a different version or plugins, may need to revisit (venv-per-project or pipx). For now, the system pytest 7.4.4 is sufficient — Plan 02b can lock the version via a tools-doc reference.

3. **Schema canonical.json includes Name primary + link backrefs.** These are Baserow-managed, not Nexostrat-spec'd. The drift check WILL fire if anything changes there (e.g., Baserow rename Name to Title in v2.0). That's a feature (we want to know) but the runbook for "drift alert: Name → ???" needs to clearly say "this is Baserow upgrade behavior, decide whether to update canonical or revert Baserow."

## Files modified this session

Session-end commit will include:

- 21 commits already on `main` between `4e8dd31..141d7c7` (plus the test-bug fix `141d7c7`). See `git log --oneline 4e8dd31..HEAD`.
- `STATUS.md` (header + new session block prepended)
- `tasks.json` (closed t-plan-02a-execute-chunk-b; added 3 follow-ups)
- `00_META/CHANGELOG.md` (new row session 7)
- `00_META/journal/2026-05-19_plan-02a-chunk-b-execution.md` (NEW)
- `CHECKPOINT.md` (this file, rewritten)

**Outside the repo (manual changes on HP):**
- `/etc/systemd/system/nexostrat-baserow-reconcile.timer` symlinked then MASKED
- `/etc/systemd/system/nexostrat-baserow-schema-check.timer` symlinked then MASKED
- `python3-pytest` installed via apt (7.4.4)
- `/tmp/strip_defaults.py`, `/tmp/add_manual_source_option.py`, `/tmp/cleanup_test_rows.py`, `/tmp/debug_*.py`, `/tmp/list_clients.py`, `/tmp/debug_new_client.sh` — ad-hoc debug + cleanup helpers in `/tmp/`, not committed (cleared on next reboot)

## Memory updates this session

None new. Existing memories applied consistently throughout.

## Estimated time to next milestones

- **Trixx meeting (2026-05-25):** 30 min prep immediately prior + 30 min meeting + recording.
- **Skill 05 Opportunity Report (post-meeting):** 30-45 min execution + 30 min Ricardo+JP review + manual delivery.
- **t-plan-02a-chunk-b-systemd-creds:** ~30-45 min — small mini-arc.
- **t-plan-02a-chunk-b-renderer-hook-lift:** ~45 min.
- **t-plan-02a-chunk-b-test-coverage:** ~30 min.
- **Plan 02a Chunk C:** ~1h subagent-driven OR ~2h inline.
- **Plan 02b write + execute:** ~1 session write, ~2-3 days execute.
- **Stage 1 launch realistic:** 2026-07-15 to 2026-07-30 (unchanged).

## After this, what's next

Reunión Trixx 2026-05-25 → grabación → Skill 05 → revisión Ricardo+JP → entrega → seguimiento D+4. In parallel (Ricardo's choice): Chunk B follow-ups → Chunk C → Plan 02b → Plans 03/04 → Plans 05-10 → Stage 1 launch.

## For a future auditor reading this baton

This was the 16th execution arc major desde 2026-05-15. Pattern reinforced: write the plan → subagent-driven execute task-by-task → main session does live-API verification → spec + quality reviews per task → cross-cutting final review at end → fold conditionals + defer follow-ups via explicit tracked tasks. The mask-timers-instead-of-fix-now decision is a deliberate Stage 1 tradeoff: prevents a tonight landmine, encodes the follow-up as a high-priority near-due task, doesn't block subsequent work.

Reading order to re-audit this arc:

1. This CHECKPOINT.
2. `STATUS.md` Current state + "Done this session (2026-05-19 PM seventh session)" block (top).
3. Journal `00_META/journal/2026-05-19_plan-02a-chunk-b-execution.md`.
4. Plan 02a `00_META/plans/2026-05-19_plan-02a-foss-stack.md` Tasks 4-10 (what was specified).
5. The 21 commits' messages — each captures the *why* of any inline plan-defect patch.
6. CHANGELOG row session 7 (top).

The session-end bookkeeping commit (next) locks all of this. Next session opens with: Ricardo's choice among (a) post-Trixx Skill 05 if meeting has occurred, (b) Chunk B follow-ups (recommended: systemd-creds first), (c) Chunk C straight, (d) something else.

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the path forward.*
