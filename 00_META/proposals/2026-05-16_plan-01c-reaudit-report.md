# Plan 01c re-audit report

> **Audit date:** 2026-05-16
> **Auditor:** dispatched general-purpose agent (Opus 4.7, 1M context) with adversarial risk-auditor persona inlined
> **Audited:** `00_META/plans/2026-05-14_plan-01c-personas.md` (2040 lines, 11 tasks)
> **Audited against:** `v0.1b-mirrors-only` baseline (HEAD `d87504e` on `main`, working tree clean)
> **Audit brief:** inline dispatch (not file-based), inheriting the format from 2026-05-13/14/16 priors (5th audit at this discipline)
> **Verdict:** **YELLOW (large)**
> **Note on file output:** the auditor sub-agent's harness blocked direct `.md` creation per a system reminder; parent agent persisted the report verbatim from the sub-agent's final message into this file.

---

## 1. Verdict + counts

**Verdict: YELLOW (large).** Plan 01c is architecturally sound in intent — the canonical-shared-stanzas pattern, the four-sub-hook surface, and the rich smoke test are all the right shapes. No CRITICAL findings; no DESIGN-RETHINK FLAG. The plan correctly closes F8 (memos), F10 (vault namespace split), F18 (resolved by F10), F20 (BRAIN_STATUS / 00_TEMPLATES leak audit), F27 (Hosted follow-through), C3 (inliner), R4 (CHECKPOINT mtime). It implements ADR-011 (three personas), ADR-014/025 (docs-pair + two-tier), and ADR-031 (CHECKPOINT continuity) coherently. The events.jsonl boundary is respected (no event-router built — correct Plan 03 territory).

What pulls the verdict to YELLOW (large) is **seven HIGH findings**:

1. **Sub-test [3/6] (`warm-rsync real trigger`) targets `nexostrat-warm-rsync.service` which does not exist** because Plan 01b Tasks 7-12 (warm-standby cluster) were DEFERRED on 2026-05-16 — the tag landed as `v0.1b-mirrors-only`. Task 11 says "Do NOT tag until smoke test is fully green." Plan 01c **cannot complete** and `v0.1-foundation` **cannot be tagged** as written. This is the dominant defect.

2. **Two process-substitution age-decrypt sites at lines 1741 and 1756** of the smoke test — same defect class the hard audit pre-flagged and the Plan 01b re-audit closed at three sites via commit `3057714`. Plan 01c re-introduces it.

3. **The Founder CLAUDE.md template DROPS load-bearing content** not represented in any shared stanza: the "Architecture / Context" section (Stage 1 launch target, Tailscale IP, machine name, key collaborators) AND the "Inter-Persona Coordination" section (ADR-013 events.jsonl pointer). Task 5 Step 5 acknowledges the risk in one sentence but gives the operator no checklist.

4. **Task 8 Step 6 Checkpoint sub-hook smoke test destroys the real `/srv/Nexostrat/CHECKPOINT.md`:** `cp /tmp/empty-cp.md /srv/Nexostrat/CHECKPOINT.md.bak` backs up the EMPTY stub, not the real file (11570 bytes). The restore step `mv CHECKPOINT.md.bak CHECKPOINT.md` then overwrites the wiped CHECKPOINT.md with the empty stub. Data-loss bug in plan instructions.

5. **The new `rule1.md` stanza silently broadens cross-persona-editing policy:** current CLAUDE.md says "small obvious cross-persona edits ... fine; one-sentence heuristic" — new stanza says "any persona may edit any folder." Also adds JP-as-driver, at odds with JP-Light (Telegram bot + email + future FOSS dashboard; no session-driving surface).

6. **Sub-test [4/6] (`/dev/shm` leak check) is a false-positive trap under TTY-less execution:** the wrapper hangs at the passphrase prompt, never decrypts, never creates `/dev/shm/nexostrat-secrets-$$`. Post-kill `ls` returns 0. Sub-test PASSES without exercising the leak path. Same class as `t-plan-01a-jp-and-tty-deferred`.

7. **Sub-test [2/6] false-positives if its own `git commit` fails** (stderr suppressed; prior HEAD is already mirrored → convergence loop trivially succeeds) AND pollutes `main` history with `smoke-test <ts>` commits on every run (no cleanup).

The MEDIUM lane carries 8 items: pre-flight tag mismatch (Plan 01c says `v0.1b-mirrors`, actual `v0.1b-mirrors-only`); `nexostrat-memos.py` operator-precedence subtlety; `docs-skip-pair` escape hatch in error text not implemented; GEMINI.md templates inappropriately include `vault_access.md`; R4 mtime check always trips on normal Ricardo workflow; inliner is single-pass (nested includes silently un-expanded); tag-message audit-closure cumulative without per-plan attribution; `jp-heavy.yaml:33` still lists `signal` in `desktop_apps`.

LOW lane: 6 stylistic items.

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| HIGH | 7 |
| MEDIUM | 8 |
| LOW | 6 |

---

## 2. Findings table

| ID | Title | Plan line(s) | Source-of-truth ref | Reality | Severity | Recommendation |
|---|---|---|---|---|---|---|
| H1 | Sub-test [3/6] targets `nexostrat-warm-rsync.service` which doesn't exist (Plan 01b Tasks 7-12 deferred) | 1784-1795, 1900-1906, 1941 | `git tag` shows `v0.1b-mirrors-only` (not `v0.1b-mirrors`); `ls infra/systemd/` shows only mirror units; STATUS.md "Tasks 7-12 deferred to t-plan-01b-execute-warm-standby" | Sub-test runs `sudo systemctl start nexostrat-warm-rsync.service` → unit-not-found; `RES` + `RC` empty; FAIL. Task 11 "do not tag until green" → blocks tag. | HIGH | Gate on `systemctl cat nexostrat-warm-rsync.service`; SKIP-not-FAIL when not installed. Doc in Task 10/11 narrative. Rename expected-tag at line 88. |
| H2 | Two process-sub age-decrypt sites in smoke-test.sh | 1741, 1756 | `run-with-secrets.sh:56` direct-`-i` canonical; precedent `7e950ee` (01a) + `3057714` (01b); hard audit named Plan 01c as remaining territory | Both sites use `age -d -i <(age -d ...)`. Will fail in non-TTY contexts. | HIGH | Mechanical: `age -d -i <(age -d $KEY) $CT` → `age -d -i $KEY $CT`. |
| H3 | Founder CLAUDE.md template drops Architecture/Context + Inter-Persona Coordination sections | 894-937 vs current CLAUDE.md:83-142 | Current sections carry Stage 1 launch target, Tailscale IP `100.64.121.80`, machine `ricardo-hp-laptop`/`jp-mac`, ADR-013 events.jsonl pointer, JP-Light details | Template has 8 includes + 2-line Role + 6-rule Strict Rules. No architecture-context, no inter-persona-coordination. ~30 lines of load-bearing facts dropped. | HIGH | Option B (recommended): inline architecture-context block per-template (Founder + Skills-Master + Client-Owner). Add Task 5 verification sub-step: `diff` regenerated CLAUDE.md vs `git show v0.1b-mirrors-only:CLAUDE.md`. |
| H4 | Task 8 Step 6 Checkpoint test destroys real CHECKPOINT.md (11570 bytes) | 1616-1630 | ADR-031: CHECKPOINT.md is the session-continuity baton | `cp /tmp/empty-cp.md /srv/Nexostrat/CHECKPOINT.md.bak` — backs up EMPTY stub. Restore `mv CHECKPOINT.md.bak CHECKPOINT.md` overwrites wiped real file with empty stub. | HIGH | Fix `cp` direction: `cp /srv/Nexostrat/CHECKPOINT.md /srv/Nexostrat/CHECKPOINT.md.bak`. Add non-empty-backup assertion before mutation; non-empty-restore assertion after. |
| H5 | `rule1.md` stanza silently broadens cross-persona-editing policy | 128 vs current CLAUDE.md:23 | ADR-011 establishes non-overlapping persona scopes; ADR-021bis JP-Light has no session-driving surface | New rule1: "any persona may edit any folder" + "Ricardo OR JP driving"; current: "small obvious + one-sentence heuristic" + Ricardo-only. | HIGH | Restore tighter language; drop JP-as-driver (matches JP-Light reality). |
| H6 | Sub-test [4/6] is a TTY-less false-positive trap | 1797-1813 | `run-with-secrets.sh:56` needs TTY for passphrase prompt; `t-plan-01a-jp-and-tty-deferred` exists for this reason | Wrapper hangs at prompt; never decrypts; INTRA=0; POST=0; PASS reported without exercising leak path. | HIGH | TTY-gate: `if [ ! -t 0 ] || [ ! -t 1 ]; then SKIP; fi`. Assert INTRA>0 before declaring PASS. |
| H7 | Sub-test [2/6] silent false-positive on commit-fail + commit pollution | 1764-1782 | Post-Task-8 orchestrator hook can refuse commits; stderr suppressed → silent failure; mirror is already current → convergence trivially succeeds | Each successful run leaves `smoke-test <ts>` in main history; failed runs PASS silently. | HIGH | Fix 2 (recommended): no-commit; just check `git ls-remote {github,codeberg} main` parity vs current HEAD. |
| M1 | Pre-flight expects `v0.1b-mirrors`, actual is `v0.1b-mirrors-only` | 88, 1992 | Plan 01b Tasks 7-12 deferred 2026-05-16; tag renamed | Grep regex matches both; misleading comment. | MEDIUM | Update to `v0.1b-mirrors-only`. Bundles with H1. |
| M2 | `nexostrat-memos.py:666` operator-precedence fragile | 666 | Python `or`/`and` binding; intent works but is implicit | Future readers may misread. | MEDIUM | Add explicit parens around the `broadcast and ...` disjunct. |
| M3 | `pre-commit-docs-pair.sh` advertises `docs-skip-pair` escape it doesn't implement | 1458, 1493-1494 | Spec §4.6 / ADR-014 names the escape; Plan 01c says Plan-02 territory | Hook is pre-commit, not commit-msg → can't inspect commit message. Operator follows advice, gets refused again. | MEDIUM | Either implement (move to commit-msg) or honest error: "use `git commit --no-verify` to bypass; escape hatch lands in Plan 02." |
| M4 | GEMINI.md templates include `vault_access.md` — Gemini doesn't run the wrapper | 963, 1151, 1326 | `vault_access.md` covers Claude/operator wrapper discipline | Misleading bloat in Gemini's context. | MEDIUM | Drop the include, or replace with small `gemini_vault_constraint.md`. |
| M5 | `checkpoint-mtime-check.sh` 10-min window always trips on normal workflow | 795, 819-820 | Normal session-end→next-session-start gap < 10 min | R4 protection is signal-free white noise. | MEDIUM | Keep as MVP; document limitation in Task 4 commit message; Plan 03's event-router will supersede with a proper lock. Consider raising threshold. |
| M6 | `inline_includes.py` single-pass; nested includes silently un-expanded | 498-516 | `re.sub` runs once; output not re-scanned | Not currently exploited; undocumented limitation. | MEDIUM | Iterate to fixed-point with recursion guard. Update `test_inliner.sh`. |
| M7 | Tag-message audit-closure cumulative; no per-plan attribution | 1955-1957 | 19 F + 4 R + 4 C listed flat across 01a/01b/01c | Future archaeologist loses per-plan contribution. | MEDIUM | Restructure to "01a closed F11/F12/...; 01b closed C4/F7/...; 01c closed F8/F10/F18/F20/F27/C3/R2/R4." |
| M8 | `jp-heavy.yaml:33` still lists `signal` in `desktop_apps` | infra/machines/jp-heavy.yaml:33 (out-of-plan, surfaced here) | Telegram-not-Signal directive 2026-05-16; jp-light.yaml cleaned, jp-heavy.yaml missed | Pre-existing debt. | MEDIUM | Task 9 sub-step: Signal sweep across yaml + md (excluding plans/proposals/journal/archive); remove `signal` from jp-heavy.yaml. |
| L1 | Tasks 5/6/7 structurally identical; Plan-01b bundling precedent | 876-1383 | Plan 01b bundled Tasks 2+3, 4+5 | 3 × 7-step tasks ~80% identical. | LOW | Leave as-is (per-persona commit messages have audit value). |
| L2 | Self-Review "Missing items — none" missed H1-H7 | 2022 | Plan 01a + 01b precedents: self-review catches typos not architectural drift | Pattern repeats. | LOW | Append "(amended post-re-audit 2026-05-16 — H1-H7 corrected)" after patches. |
| L3 | `find -path '*/.git' -prune` could also prune `.superpowers`/`.claude` | 798-802 | Repo has both dirs; find recurses unnecessarily | Harmless. | LOW | Extend prune list. |
| L4 | Vault-age-only test uses `.test-violation` (no extension); naming obscures hook-vs-gitignore | 1605 | `.gitignore` patterns block `*.pdf/*.docx/*.txt/*.md` in vault; `.test-violation` matches none | Test is correct; just unclear. | LOW | Add a comment explaining the filename choice. |
| L5 | Smoke-test `.last-mirror-test` shares filename with Plan 01b path-watcher validation | 1768 | `git log -- infra/systemd/.last-mirror-test` shows Plan-01b validation commit | Archaeology confusion. | LOW | Rename to `.last-smoke-test`. Bundles with H7. |
| L6 | Templates hardcode "Last Updated: 2026-05-14" | 899, 946, 1090, 1135, 1264, 1310 | Inliner does no date substitution | Regenerated files will be incorrectly dated. | LOW | Either teach inliner a `{{date}}` marker or update literal after first render. |

---

## 3. Detailed findings — HIGH

### Finding H1 — Smoke test sub-test [3/6] depends on `nexostrat-warm-rsync.service` which does not exist; Plan 01c cannot complete

**Severity:** HIGH (single most blocking issue; if not for Task 11's "do not tag until smoke test is fully green" gate this would arguably be CRITICAL)
**Lines:** 1784-1795 (sub-test), 1900-1906 (Task 11 narrative), 1941 (tag message claims `[3] warm-rsync real trigger Result=success PASS`)

**What's wrong:** Sub-test [3/6] does `sudo systemctl start nexostrat-warm-rsync.service` then asserts `Result=success ExecMainStatus=0`. Plan 01b Tasks 7-12 (warm-standby cluster, including this unit) were DEFERRED 2026-05-16; the tag landed `v0.1b-mirrors-only`. The task `t-plan-01b-execute-warm-standby` is open with due 2026-06-30, gated on physical second host.

**Evidence:**
```
$ git tag -l | sort
v0.1a-foundation
v0.1b-mirrors-only

$ ls /srv/Nexostrat/infra/systemd/
nexostrat-mirror-codeberg.path
nexostrat-mirror-codeberg.service
nexostrat-mirror-github.path
nexostrat-mirror-github.service
# No warm-rsync unit
```

When the smoke test runs: `systemctl start ...` → unit not found (stderr suppressed via `2>/dev/null`); `systemctl show ... --property=Result --value` returns empty string for non-existent units; `[[ "$RES" == "success" && "$RC" == "0" ]]` evaluates false; sub-test FAILS. Task 11: "If anything is FAIL ... Do NOT tag until smoke test is fully green." → `v0.1-foundation` cannot be tagged. Plan 01c stalls 6+ weeks waiting on physical second host.

**Why it matters:** Plan 01c's stated goal is "After 01c, `v0.1-foundation` is tagged — the original Plan-01 milestone reached at the end of the 3-plan split." If 01c cannot tag without 01b Tasks 7-12, the 3-plan split's promised independence collapses. The failure mode is silent (stderr suppressed); operator sees only "FAIL warm-rsync.service Result= ExecMainStatus=" — no diagnostic for "unit doesn't exist yet."

**Recommendation:** Gate sub-test [3/6] on warm-rsync existence:

```bash
echo "[3/6] warm-rsync real trigger"
if ! systemctl cat nexostrat-warm-rsync.service >/dev/null 2>&1; then
  echo "  SKIP  nexostrat-warm-rsync.service not installed (Plan 01b Tasks 7-12 deferred to t-plan-01b-execute-warm-standby; due 2026-06-30)"
else
  # ... existing test
fi
```

Also: update line 88 expected-tag → `v0.1b-mirrors-only`; update line 1941 tag-message → `[3] warm-rsync real trigger SKIP (Plan 01b Tasks 7-12 pending)`. Document explicitly in Task 10/11: "v0.1-foundation may tag at 5-PASS + 1-SKIP; the SKIP becomes PASS once Plan 01b Tasks 7-12 land."

**Effort:** 15 minutes.

---

### Finding H2 — Two process-sub age-decrypt sites in smoke-test.sh

**Severity:** HIGH
**Lines:** 1741, 1756

**What's wrong:** Both use `age -d -i <(age -d "$HOME/.config/age/nexostrat.key.age") <ciphertext>`. The inner age runs in a subshell with no TTY → cannot prompt for passphrase → fails silently or with a confusing error. Same defect class as the 11 sites in 01a (fixed in `7e950ee`) and 3 sites in 01b (fixed in `3057714`). Live canonical pattern at `run-with-secrets.sh:56`: `age -d -i "$PRIV_KEY_AGE" "$ENC"` — direct -i, no subshell. The hard system audit's "What audit did NOT cover" item 4 named Plan 01c smoke test as the remaining territory.

**Evidence:**
```
$ grep -nE "age -d -i <\(" /srv/Nexostrat/00_META/plans/2026-05-14_plan-01c-personas.md
1741:if age -d -i <(age -d "$HOME/.config/age/nexostrat.key.age") \
1756:   && age -d -i <(age -d "$HOME/.config/age/nexostrat.key.age") "$TMP_CT" > "$TMP_DEC" \
```

**Why it matters:** Sub-test [1/6] is the load-bearing crypto round-trip. Under non-TTY execution (subagent-driven-development, scripted), both decrypts hang or fail. Operator may misdiagnose as a real crypto break.

**Recommendation:** Mechanical patch at both sites: `age -d -i <(age -d "$HOME/.config/age/nexostrat.key.age")` → `age -d -i "$HOME/.config/age/nexostrat.key.age"`.

**Effort:** 3 minutes.

---

### Finding H3 — Founder CLAUDE.md template drops two load-bearing sections not in any shared stanza

**Severity:** HIGH
**Lines:** 894-937 (Founder template) vs current `CLAUDE.md:83-142`

**What's wrong:** Current CLAUDE.md has 12 sections; Plan 01c template has 8 includes + 2-line Role + 6-rule Strict Rules. Two sections are DROPPED with no replacement stanza:

1. **"Architecture / Context"** (current lines 83-102) — Stage 1 launch target (2026-06-30 to 2026-07-15), Tailscale IP `100.64.121.80`, machine names (`ricardo-hp-laptop`, `jp-mac`), ADR-011 three-personas pointer, current-phase status, key-collaborators list (including JP-Light details, 10h/wk bandwidth, FOSS dashboard from Plan 02).

2. **"Inter-Persona Coordination"** (current lines 132-142) — ADR-013 pointer (`infra/events/events.jsonl` is the cross-persona spine, built in Plan 03), pre-Plan-03 explicit state, post-Plan-03 forward statement.

Task 5 Step 5 says "If anything load-bearing was lost ... edit the templates and re-render" — but the operator has no checklist of what to preserve. Plan 01a/01b precedent: self-review misses real defects.

**Why it matters:** Future Claude sessions read CLAUDE.md as orientation. Without Architecture/Context, a fresh session lacks Stage 1 timeline + machine names + JP-mode context. Without Inter-Persona Coordination, a future Claude pre-Plan-03 has no pointer to events.jsonl.

**Recommendation:** **Option B (recommended)** — inline the architecture-context block directly in each of the three Claude template bodies (Founder/Skills-Master/Client-Owner). Content is genuinely persona-specific anyway (scopes differ per persona). Accept ~15 lines of per-template duplication; single source of truth per persona. Add Task 5 verification sub-step: `diff` regenerated CLAUDE.md vs `git show v0.1b-mirrors-only:CLAUDE.md` to confirm preservation.

**Effort:** 30 minutes (write block × 3, paste into templates, re-verify drift-free).

---

### Finding H4 — Task 8 Step 6 Checkpoint sub-hook smoke test destroys the real `/srv/Nexostrat/CHECKPOINT.md`

**Severity:** HIGH
**Lines:** 1616-1630

**What's wrong:**
```bash
echo "" > /tmp/empty-cp.md
cp /tmp/empty-cp.md /srv/Nexostrat/CHECKPOINT.md.bak    # ← BUG: backs up EMPTY stub, not real CHECKPOINT.md
echo "" > /srv/Nexostrat/CHECKPOINT.md                  # wipes real file
git add /srv/Nexostrat/CHECKPOINT.md
git commit -m "should be blocked" 2>&1 | tail -5
mv /srv/Nexostrat/CHECKPOINT.md.bak /srv/Nexostrat/CHECKPOINT.md  # ← Restores EMPTY stub over wiped file
```

Net effect: the real CHECKPOINT.md (11570 bytes of active session baton) is destroyed.

**Evidence:**
```
$ wc -c /srv/Nexostrat/CHECKPOINT.md
11570 /srv/Nexostrat/CHECKPOINT.md
```

**Why it matters:** ADR-031 says CHECKPOINT.md is the session-continuity baton; Session Start Protocol step 1 reads it FIRST. An empty CHECKPOINT.md silently breaks session continuity. The operator could `git checkout HEAD -- CHECKPOINT.md` to recover but the plan doesn't tell them. A careless follow-on commit could push the empty file.

**Recommendation:** Fix `cp` direction:
```bash
cp /srv/Nexostrat/CHECKPOINT.md /srv/Nexostrat/CHECKPOINT.md.bak  # back up the REAL file
[[ ! -s /srv/Nexostrat/CHECKPOINT.md.bak ]] && { echo "ABORT: empty backup"; exit 1; }
# ... mutate + test ...
mv /srv/Nexostrat/CHECKPOINT.md.bak /srv/Nexostrat/CHECKPOINT.md
[[ ! -s /srv/Nexostrat/CHECKPOINT.md ]] && { echo "ABORT: restore failed"; exit 1; }
```

Better: run the test in a throwaway tempdir, never touch the real CHECKPOINT.md.

**Effort:** 5 min for cp fix; 15 min for tempdir version.

---

### Finding H5 — `rule1.md` stanza silently broadens cross-persona-editing policy

**Severity:** HIGH (policy change introduced as stanza polish)
**Lines:** 128 (proposed rule1.md) vs current `CLAUDE.md:23`

**What's wrong:** Three substantive changes silently introduced:

- "**small obvious** cross-persona edits" → "**any** persona may edit **any** folder."
- Drop of the "one-sentence heuristic" litmus test.
- "Ricardo in-session driving" → "Ricardo **or JP** in-session driving." But JP-Light per ADR-021bis is Telegram + email + future FOSS dashboard — NOT session-driving. JP only drives sessions if he flips to Heavy.

**Why it matters:** ADR-011 establishes three personas with non-overlapping write scopes. The new rule1 effectively says "when an operator is driving, scope is dissolved." Architectural shift, not stanza polish. Once Plan 01c lands, the original heuristic disappears from CLAUDE.md with no ADR or commit-message audit trail. JP-as-driver presupposes Heavy mode that doesn't exist at Stage 1.

**Recommendation:** Restore tighter language (Option A):

```markdown
**Folder-scope discipline.** Each persona's primary write scope is its own folder. When Ricardo is in-session driving, small obvious cross-persona edits are fine. **Heuristic:** if the cross-persona edit takes more than a sentence to explain, defer to that persona's session. Vault namespaces (per ADR-003 + F10) stay strictly isolated regardless. Reading anywhere within `/srv/Nexostrat/` is always permitted.
```

If the policy change IS intentional, land it as ADR-039 with explicit rationale (Option B).

**Effort:** 10 minutes.

---

### Finding H6 — Sub-test [4/6] (`/dev/shm` leak check) is a TTY-less false-positive trap

**Severity:** HIGH
**Lines:** 1797-1813

**What's wrong:** `run-with-secrets.sh` calls `age -d -i $PRIV_KEY_AGE $ENC` which prompts on `/dev/tty`. The smoke test backgrounds the wrapper with no stdin/TTY → age hangs at the passphrase prompt → never decrypts → `/dev/shm/nexostrat-secrets-$$` never exists. `INTRA=0`. `kill $WPID` → trap fires but has nothing to shred. `POST=0`. Sub-test PASSES — without exercising the leak path. The error message even confesses: "intra-run had $INTRA which is expected" — but 0 is NOT expected if the wrapper works.

**Why it matters:** `t-plan-01a-jp-and-tty-deferred` exists because the wrapper needs a real TTY. Plan 01c's smoke test doesn't acknowledge this. Future agent reads 6 × PASS and assumes the leak path is hardened.

**Recommendation:** TTY-gate + INTRA>0 assertion:

```bash
if [ ! -t 0 ] || [ ! -t 1 ]; then
  echo "  SKIP  no TTY; leak check requires interactive passphrase entry"
else
  # ... background wrapper, sleep 5 (not 2) ...
  if [[ $INTRA -eq 0 ]]; then
    no "wrapper never decrypted — INTRA=0"
  else
    # check POST after kill
  fi
fi
```

Cross-reference `t-plan-01a-jp-and-tty-deferred` in Task 10/11 narrative.

**Effort:** 15 minutes.

---

### Finding H7 — Sub-test [2/6] false-positives on commit-fail + pollutes main history

**Severity:** HIGH
**Lines:** 1764-1782

**What's wrong:** Two problems:

1. **Silent false-positive.** Once Task 8's orchestrator hook is installed, the smoke-test's `git commit -q ... 2>/dev/null` runs all 4 sub-hooks. If any trip, stderr is suppressed; `git rev-parse HEAD` returns prior HEAD (already mirrored); convergence loop succeeds instantly → PASS reported. The smoke-test's own commit failed but the test thinks the mirror is healthy.

2. **History pollution.** Each successful run leaves a permanent `smoke-test <ts>` commit in `origin main`. No cleanup. Task 11 "Re-run until green" means failed→passing runs still accumulate commits.

**Why it matters:** A false-positive PASS could tag `v0.1-foundation` with a broken mirror chain that nobody notices. The history pollution is permanent and grows monotonically.

**Recommendation:** **Fix 2 (recommended)** — no-commit redesign. Plan 01b already proved mirror works; just assert current HEAD parity:

```bash
LOCAL=$(git rev-parse HEAD)
GH=$(git ls-remote github main 2>/dev/null | awk '{print $1}')
CB=$(git ls-remote codeberg main 2>/dev/null | awk '{print $1}')
if [[ "$GH" == "$LOCAL" && "$CB" == "$LOCAL" ]]; then
  ok "GitHub + Codeberg at HEAD ($LOCAL) without intervention"
else
  no "mirror not in sync: GH=$GH CB=$CB local=$LOCAL"
fi
```

Eliminates both problems simultaneously.

**Effort:** 30 minutes.

---

## 4. Detailed findings — MEDIUM

**M1 — Pre-flight tag mismatch (lines 88, 1992):** Plan says `v0.1b-mirrors`, actual is `v0.1b-mirrors-only` post-deferral. Grep regex matches both; comment misleads. Update to match reality. Bundles with H1.

**M2 — `nexostrat-memos.py:666` operator precedence:** `if persona == 'all' or to_field == persona or to_field == 'broadcast' and persona != 'all':` works (Python `and` binds tighter than `or`) but is implicit. Add explicit parens: `or (to_field == 'broadcast' and persona != 'all'):`.

**M3 — `pre-commit-docs-pair.sh` advertises unimplemented escape (lines 1458, 1493-1494):** Hook prints "add 'docs-skip-pair' to commit body" but hook is pre-commit, not commit-msg → can't read the message. Operator follows advice, gets refused again. Either implement the escape (move to commit-msg or scan `.git/COMMIT_EDITMSG`) or rewrite error: "the escape lands in Plan 02; for now use `git commit --no-verify`."

**M4 — GEMINI.md templates include `vault_access.md` (lines 963, 1151, 1326):** That stanza covers `run-with-secrets.sh`, `/dev/shm` decrypt, recipients-file ownership — all Claude/operator territory. Gemini doesn't run the wrapper. Drop the include, or replace with small `gemini_vault_constraint.md` (~5 lines: "decrypt for review only; no writes to vault/clients/").

**M5 — `checkpoint-mtime-check.sh` 10-min window always trips:** Normal Ricardo workflow: session-end → push → next session minutes later. CHECKPOINT.md mtime always < 10 min. Script always warns; warning text disclaims itself. R4 protection is signal-free. Keep as MVP; document in Task 4 commit message: "Plan 03's event-router will supersede with a proper lock." Consider raising threshold.

**M6 — `inline_includes.py` single-pass (lines 498-516):** `re.sub` runs once; nested includes silently un-expanded. Not currently exploited but undocumented limitation. Iterate to fixed-point with recursion guard (~3 lines). Update `test_inliner.sh` to cover nested case.

**M7 — Tag-message audit-closure cumulative (lines 1955-1957):** Flat list of 19 F + 4 R + 4 C "across 01a/01b/01c." Restructure: "01a closed F11/F12/F13/F14/F15/F16/F17/F19/F21/F23/F26/R3/R5/R6; 01b closed C4/F7/F22/F24/F25; 01c closed F8/F10/F18/F20/F27/C3/R2/R4."

**M8 — `jp-heavy.yaml:33` lists `signal` in desktop_apps:** Pre-existing debt from before the 2026-05-16 Telegram-only directive. jp-light.yaml was cleaned; jp-heavy.yaml missed (future-state stub). Plan 01c persona-mode pass is the natural patch cycle. Add Task 9 sub-step: `grep -rn -i signal /srv/Nexostrat/ --include='*.yaml' --include='*.md' --exclude-dir={.git,.superpowers,.claude,00_META/plans,00_META/proposals,00_META/journal,00_META/handoff/archive}`; sweep.

---

## 5. Deferred findings — LOW

- **L1** Tasks 5/6/7 structurally identical (~500 lines 80% duplicate template); Plan-01b bundling precedent. Recommend leave as-is.
- **L2** Self-Review "Missing items — none" missed H1-H7. Append "(amended post-re-audit 2026-05-16)" after patches.
- **L3** `find -path '*/.git' -prune` could also prune `.superpowers`/`.claude` (lines 798-802). Polish.
- **L4** Vault-age-only test uses `.test-violation` (no extension); add a comment clarifying why (line 1605).
- **L5** Smoke-test `.last-mirror-test` shares filename with Plan 01b path-watcher validation (line 1768). Bundles with H7 (rename or eliminate file).
- **L6** Templates hardcode "Last Updated: 2026-05-14" (lines 899/946/1090/1135/1264/1310). Teach inliner a `{{date}}` marker or update literal after first render.

---

## 6. Production-readiness assessment

Post-patch (H1-H7 applied), `v0.1-foundation` delivers:
- 3 personas live (Founder/Skills-Master/Client-Owner) with CLAUDE.md/GEMINI.md/CHECKPOINT.md/inbox each.
- Canonical-shared-stanza pattern with drift detection.
- `nexostrat-memos.py` for session-start memo discovery.
- 4-sub-hook pre-commit surface.
- R4 concurrent-session warning (mtime MVP).
- Rich smoke test: 5 sub-tests PASS + 1 SKIP (warm-rsync, gated on Plan 01b Tasks 7-12).

**Hidden gaps (all correctly Plan-02-or-later territory):**
1. `events.jsonl` event-router not built (Plan 03).
2. docs-pair hook covers only the rigid tier-1 (`docs/` enforcement + escape Plan 02).
3. R4 MVP is mtime-only (Plan 03 event-router will supersede).
4. No `-explicado.md` partners exist for any tier-1 doc → docs-pair hook is defensive-but-inert until Plan 02.
5. TTY-side leak validation deferred to `t-plan-01a-jp-and-tty-deferred`.
6. JP-side roundtrip cleanup pending (same tracked task).

None block Stage 1 launch (2026-06-30 to 2026-07-15).

---

## 7. Recommended actions

**(a) Patch inline before Plan 01c execution (HIGH; ~1.5 hours):** apply H1-H7 in a single commit. Bundle suggested commit message:

```
Plan 01c re-audit patches · H1-H7 closed in single pass

H1: Sub-test [3/6] gated on warm-rsync.service existence; SKIP-not-FAIL when
    Plan 01b Tasks 7-12 deferred. Pre-flight tag v0.1b-mirrors → v0.1b-mirrors-only.
H2: Two process-sub age-decrypt sites in smoke-test → direct -i (lines 1741, 1756).
H3: Founder/Skills-Master/Client-Owner CLAUDE.md templates regain architecture-
    context block (Stage 1 target, Tailscale IP, machine names, ADR-013 pointer,
    key collaborators) — was load-bearing in current CLAUDE.md.
H4: Task 8 Step 6 Checkpoint test cp source fixed; non-empty-backup assertion.
H5: rule1.md restored to tighter language (small obvious + one-sentence heuristic;
    Ricardo-only-driving). Drops silent "any folder" widening + ADR-021bis conflict.
H6: Sub-test [4/6] TTY-gated; asserts INTRA>0 before declaring PASS.
H7: Sub-test [2/6] no-commit redesign (current HEAD parity vs mirrors); eliminates
    pollution + false-positive-on-commit-fail.

Re-audit report: 00_META/proposals/2026-05-16_plan-01c-reaudit-report.md
```

**(b) Bundle MEDIUM into the same commit (~45 min):** M1 (bundled with H1), M2 (parens), M3 (honest error), M4 (drop include), M5 (commit-message note), M6 (iterate-to-fixed-point), M7 (per-plan attribution), M8 (Signal sweep + jp-heavy.yaml).

**(c) Track as new tasks:** None — all H + M patchable inline.

**(d) Polish-pass post-Plan-01c:** L1-L6 bundled into a `t-plan-01c-text-polish` follow-up or absorbed into Plan 02 brainstorm.

---

## 8. What this audit did NOT cover

1. Live execution of `inline_includes.py` against the 9 stanzas + 6 templates — static reading only; execution-time may surface Unicode/path-length/race issues.
2. Pre-commit orchestrator interaction with secret-scan hook under real commit conditions — auditor confirmed file paths but didn't dry-run all 4 sub-hooks in sequence.
3. Post-H3 + post-H5 stanza content for drift-check survival — whoever lands the patch should re-verify `inline_includes.py --check` passes.
4. `pre-commit-docs-pair.sh` block-path behavior — no `-explicado.md` partners exist in repo today; hook is defensive-but-inert until Plan 02.
5. Live mirror behavior under post-H7 no-commit sub-test [2/6] — should work given Plan 01b's measured 3-8s convergence, but not run.
6. R4 mtime threshold tuning under real session cadence — auditor can't measure from a single seat.
7. R6 (calendar honesty) audit-closure claim — should be verified by Ricardo + Claude during the patch walk.

---

*End of Plan 01c re-audit report. Sibling priors: `2026-05-14_audit-report.md` (founding spec, RED), `2026-05-14_plan-01a-audit-report.md` (YELLOW large), `2026-05-16_hard-system-audit-report.md` (YELLOW small at v0.1a-foundation), `2026-05-16_plan-01b-reaudit-report.md` (YELLOW small). This audit's 7 HIGH should follow the same patch-in-session pattern as the priors.*
