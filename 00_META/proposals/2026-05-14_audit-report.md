# Audit Report — Nexostrat Foundation 2026-05-13

> **Auditor:** risk-auditor (adversarial second seat, no exposure to source session)
> **Date filed:** 2026-05-14
> **Artifacts examined:** founding spec (954 lines), master plan index (440 lines), Plan 01 (3462 lines), prior 2026-05-11 spec (cross-check only)
> **Brief:** [`2026-05-13_audit-request.md`](2026-05-13_audit-request.md)

## Verdict
**RED**

## Summary

Examined the three artifacts (~5400 lines) against the failure categories enumerated in the audit brief. The architecture is *substantively coherent at the level of intent* but is **not executable as written** — Plan 01 has multiple correctness bugs that will fail on first execution, and the spec carries unresolved internal contradictions in scope, ADR status, and persona ownership that will propagate into Plans 02-10. Several catastrophic single-points-of-failure are designed in (vault encrypted to Ricardo only; ambient chat history same; the wrapper-secret-shred pattern leaks plaintext on every invocation). The Stage 1 go-live checklist requires items that no plan delivers.

**Findings:** 4 CRITICAL, 11 HIGH, 9 MEDIUM, 4 LOW = 28 total (15 HIGH+).

> **DESIGN-RETHINK FLAG.** 15 findings of HIGH or above exceed the audit brief's "10+ HIGH" threshold. Amendments alone will not get this to GREEN. The Plan 01 task ordering, the secrets/wrapper pattern, the persona-shared-stanza include mechanism, the JP-key catastrophe model, and the Mode-A/Mode-B "same contract" claim each need a small rethink, not a patch. Recommend: reduce Plan 01 scope (defer warm-standby, persona files, post-receive hook to Plan 02), fix the wrapper before any secret is encrypted, resolve the JP-key SPOF before vault is provisioned (option B in finding 2), then re-audit.

---

## Findings

### Severity scale
- **CRITICAL** — must fix before Plan 01 execution (RED triggers)
- **HIGH** — should fix before Plan 01 execution (YELLOW with amendment)
- **MEDIUM** — fix during Plan 02 or document as known limitation
- **LOW** — nice-to-have; capture as future ADR

---

### Finding 1 — `run-with-secrets.sh` leaks plaintext to /dev/shm on every run; cleanup trap is dead code

**Severity:** CRITICAL
**Artifact:** plan-01
**Location:** `00_META/plans/2026-05-13_plan-01-repository-foundation.md` Task 10, lines 950-1001

**Description:**
The wrapper script registers `trap cleanup EXIT INT TERM` (line 986) and then calls `exec "$@"` (line 1000). `exec` replaces the shell process image; the trap exists in process metadata that is destroyed by the replacement. When the wrapped command later exits, it returns to the parent shell that invoked the wrapper, **not** to a context where the trap can fire. Result: `/dev/shm/nexostrat-secrets-$$.env` containing all decrypted API keys, tokens, and OAuth refresh tokens persists indefinitely.

**Why it's wrong:**
Every Mode B skill run, every CI job, every `docker compose up`, every nightly rsync that needs Drive credentials writes a fresh plaintext file under /dev/shm and never removes it. After 30 days of normal use there are dozens to hundreds of plaintext-secret files in tmpfs. Anyone with shell access on HP (or who compromises any service that can read /tmp/shm) gets the entire secret bag without needing the age key. The Plan 01 Task 10 Step 4 "verify cleanup" test passes by accident: `env` is the wrapped command, env exits cleanly, the parent test script's pipe to `grep` exits — but the trap that supposedly fired is in the wrapper-shell process that no longer exists. Re-run the test with a long-lived wrapped command (`sleep 60 &`) and check `/dev/shm/nexostrat-secrets-*.env` — the file is there.

This is the foundation of the entire secrets posture. It being broken means the spec's "blast radius bounded" claim (§3 Foundation) is false.

**Proposed amendment:**
Replace `exec "$@"` with:
```bash
"$@"
RC=$?
cleanup
exit $RC
```
Or write secrets directly to a `tmpfile` opened with O_TMPFILE-style anonymous mapping (sourced via `source <(age -d ...)` so plaintext never hits the filesystem at all). Add a smoke-test step in Task 27 that wraps `sleep 1 &` and verifies no `/dev/shm/nexostrat-secrets-*` exists after 2s.

---

### Finding 2 — Vault encrypted to Ricardo only is an unrecoverable single-point-of-failure for the firm

**Severity:** CRITICAL
**Artifact:** spec, plan-01
**Location:** spec §3 (Foundation Layer), §3.2 (Vault); Plan 01 Task 7 Step 1 (line 706-710), Task 8 (line 750), Task 11 (deferred)

**Description:**
The spec requires per-user age recipients with envelope encryption to ALL recipients ("either holder can decrypt"). Plan 01 ships with exactly ONE recipient (Ricardo's pubkey) and defers JP's key to "Heavy-mode onboarding" (no date). Until JP onboards Heavy:
- If Ricardo's age key is lost (hardware failure + no backup) and the Bitwarden passphrase is irretrievable, the vault is **permanently unreadable by anyone, including JP**.
- If Ricardo dies, is incapacitated, or simply walks away from the partnership, JP cannot decrypt the firm's signed contracts, tax filings, or 2FA recovery codes.
- The same applies to the chat log .age files (Plan 09) and `secrets.env.age`.

The risk is not academic — Plan 01's own STATUS.md (line 395) acknowledges "Vault is currently encrypted to Ricardo only with an explicit follow-up memo" but the follow-up has no SLA and no fallback recovery path.

**Why it's wrong:**
The vault is supposed to be the firm's catastrophic-loss store. Designing it with an explicit single-point-of-loss for the firm contradicts its purpose. The spec's "blast radius bounded" and "either holder can decrypt" promises are not actually delivered by Plan 01.

**Proposed amendment:**
Pick one of (in order of preference):
1. **Block Plan 01 execution until JP generates an age keypair.** The 5-min Light-mode onboarding includes `age-keygen`; storing a public key on JP's laptop is not Heavy-mode-only. Plan 01 Task 6 grows a sub-task: "JP generates keypair, sends pubkey via Signal, Ricardo adds to recipients before any encryption."
2. **Provision an escrow age recipient.** Generate a third keypair, split the passphrase via Shamir's Secret Sharing across two trusted parties (e.g., Ricardo's spouse + a notary-held envelope). Document at `vault/keys/escrow.md`. This is what real organizations do.
3. **Defer vault provisioning entirely** until either (1) or (2) is in place. Plan 01 ships secrets but not vault; vault waits for Plan 02.

Either way: amend Plan 01 Definition of Done to require the recovery path is testable, not "deferred."

---

### Finding 3 — Persona CLAUDE.md files ship with literal `{{include: ...}}` placeholders; agents read garbage

**Severity:** CRITICAL
**Artifact:** plan-01
**Location:** Plan 01 Task 18 (lines 1744-1798) explicitly `{{include: 00_META/shared/...}}` markers; Task 18 Step 3 (line 1820): "the `{{include: ...}}` markers are placeholders. In Plan 02, we'll build a generator script that inlines the actual content into the file at commit time"

**Description:**
Plan 01 commits root `CLAUDE.md` (and skills/, pipeline/) with **literal text** like `{{include: 00_META/shared/rule1_operator_scope.md}}` in place of the actual rules. Plan 01 explicitly defers the include-resolver script to Plan 02. Until Plan 02 ships:
- Every Claude Code session reads CLAUDE.md and sees the placeholder string. Claude does not know to `cat` the referenced shared stanzas.
- Strict Rules, Session Start Protocol, Session End Protocol, Memo Protocol, Gemini Handoff Protocol, Vault Access, Backup Posture, CHECKPOINT pattern — all 8 critical operating instructions — are EFFECTIVELY ABSENT for the entire window between Plan 01 completion and Plan 02 completion (~3 days estimated, easily a week if Plan 02 slips).

**Why it's wrong:**
The whole point of CLAUDE.md is to set behavior on session start. Plan 01 leaves Plan 02 owning a behavioral cliff: the very first session executed under the new CLAUDE.md (i.e., the session that writes Plan 02 itself) operates with no rules. Risk: that session produces non-compliant work that propagates.

This was probably reasoned as "Plan 02 is right after, no harm." But Plan 01 ships persona files for THREE buckets, all with placeholders. Every session at every scope is degraded until the inliner exists.

**Proposed amendment:**
Pick one:
- **(Preferred)** Move the inliner script (~30 lines of Python) into Plan 01 Task 17.5 (after shared stanzas exist, before Task 18 writes personas). Run it during Task 18 so the committed CLAUDE.md contains real text, not markers. The pre-commit hook (Plan 02) later just verifies the inlined content matches `00_META/shared/*.md`.
- **(Acceptable)** Inline the shared stanza content manually into each CLAUDE.md during Plan 01 Task 18. Yes, it's copy-paste; it's once. Plan 02's drift hook then keeps them in sync going forward.
- **(Unacceptable)** Ship as written.

---

### Finding 4 — Gitea post-receive hook cannot decrypt secrets; mirror push silently fails on every commit

**Severity:** CRITICAL
**Artifact:** plan-01
**Location:** Plan 01 Task 13 Steps 1-4, lines 1148-1224

**Description:**
The post-receive hook (line 1163) executes:
```bash
source <(${NEXOSTRAT_ROOT}/infra/scripts/run-with-secrets.sh env | grep -E '^(GITHUB_)' | sed 's/^/export /')
```

The hook is installed inside Gitea's container at `$GITEA_REPO_PATH/hooks/post-receive` and chowned to uid 1000 (Gitea container user). When the hook runs, it executes inside the Gitea container. Inside that container:
1. `${NEXOSTRAT_ROOT}` (`/srv/Nexostrat`) is the **host** path. Gitea's container does not have `/srv/Nexostrat` mounted (no mention of bind-mounts in Plan 01 or in the existing AttenBot compose referenced at `/home/ricardo/n8n/`).
2. Even if /srv/Nexostrat were mounted, `~/.age/nexostrat-ricardo.key` resolves to the Gitea container user's home (`/data/git` typically), not Ricardo's `/home/ricardo/.age/`. Gitea has no access to Ricardo's age key.
3. The `|| echo WARN` at line 1167 silently swallows the failure. Plan 01 has no test that asserts a real GitHub push happened — the Step 4 "test" only checks `gh api .../commits/main --jq .sha` matches local HEAD, but the LOCAL PUSH already pushed to origin Gitea AND the hook ran. The local `git push origin main` is the only thing that touched GitHub (because the local working tree at line 1126-1128 already did `git push github main` once); the hook never has and the Step 4 SHA match is misleading.

So: Plan 01 ships believing the GitHub mirror is automatic on every Gitea push. It isn't. Mirror is only updated when the human runs `git push github` from a workstation. If Gitea receives a push from anyone other than Ricardo's HP working tree (e.g., the warm-standby), GitHub never sees it. The "7-layer backup ladder" is actually 6.

**Why it's wrong:**
Spec §3 backup table lists GitHub mirror as "per push (hook)." Spec §10.6 go-live checklist requires GitHub mirror operational. Plan 01 thinks it's done; in reality the hook is dead.

**Proposed amendment:**
Two options:
1. **Move the mirror push out of Gitea's hook into a systemd path-watcher on HP host.** A `nexostrat-mirror.path` watches Gitea's repo refs/heads/, fires `nexostrat-mirror.service` running as `ricardo`, which has the age key. Cleaner, host-side, testable.
2. **Bind-mount `/srv/Nexostrat/secrets.env.age` and a *dedicated, mirror-only* age key into Gitea's container.** The dedicated key has a smaller blast radius than Ricardo's full vault key. Requires editing the existing Gitea compose (which lives outside this repo per Plan 01 line 525, an additional pre-req).

Either way: add an explicit Plan 01 test that does `git push origin main`, waits 30s, and verifies the GitHub HEAD commit changed.

---

### Finding 5 — Founding Meeting required "before scaffold" but Plan 01 IS the scaffold; explicit ordering violation

**Severity:** HIGH
**Artifact:** spec, plan-01
**Location:** spec line 930 ("**Founding Meeting (Plan Maestro Paso 1)** before scaffold. Sign partnership agreement."); Plan 01 entire scope

**Description:**
Spec §10.6 Open Items #4 explicitly requires the Founding Meeting (where Ricardo and JP sign the partnership agreement) to happen BEFORE scaffold. Plan 01 IS the scaffold. Plan 01's tasks.json (line 583-590) lists the Founding Meeting as `status: open, due: 2026-05-20` — i.e., scheduled to happen DURING or AFTER Plan 01 execution. Plan 01 STATUS.md update at Task 28 marks Plan 01 done while Founding Meeting is still pending.

**Why it's wrong:**
The spec was self-consistent on this; Plan 01 broke the ordering without an ADR. Concretely:
- Plan 01 commits `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md` (per file map line 86) before it's actually agreed.
- Plan 01 Task 4 Step 1 writes a public-facing root README claiming "Founders: Ricardo Mejía Caicedo · Juan Pablo Mejía" before JP has actually signed.
- If JP rejects any clause at the Founding Meeting (cost-share, revenue split, qualified-prospect threshold), the committed scaffold is wrong and must be rewritten.

**Proposed amendment:**
Either (a) hold the Founding Meeting before starting Plan 01, OR (b) split Plan 01: tasks 1-22 (folder scaffold + identity + secrets + mirror + warm-standby + bootstrap + hooks) can run pre-meeting; tasks creating partnership content and persona files referencing JP wait until post-meeting. Update spec or master index to reflect chosen ordering.

---

### Finding 6 — Per-user TZ "07:00 each user's TZ" is unimplementable with a single systemd timer

**Severity:** HIGH
**Artifact:** spec
**Location:** spec §8.2.1 (line 639), §9.4 timer examples (line 763), ADR-030

**Description:**
Spec says "Morning send (07:00 each user's TZ)" and lists exactly one timer `nexostrat-meeting-brief.timer` firing "07:00 daily per user TZ" (line 763). A systemd timer fires once at the calendar time **of the host machine's local TZ**. Ricardo (Tijuana, UTC-7/8) and JP (Bogotá, UTC-5) have a 2- to 3-hour offset; a single 07:00 timer cannot serve both. Compounding:
- The HP host runs in some single OS-level TZ. If it's set to UTC, 07:00 local fires at UTC 07:00, which is Tijuana 23:00/24:00 the previous night and Bogotá 02:00. Wrong for both users.
- Even with a finer-grained pattern (timer fires hourly, brief job filters per user), the spec's group-channel briefs cannot satisfy "each user's TZ" because the group is one channel — the brief lands at one wall-clock instant.
- DST transitions in Tijuana (PST↔PDT) cause the local 07:00 to drift relative to JP's local 07:00 twice a year, with a one-week lag if the host TZ is set to America/Bogotá but Ricardo's wall-clock is Tijuana.

**Why it's wrong:**
Plan 08 success criteria (master index line 332) explicitly requires "Morning brief at 07:00 in Ricardo's TZ (Tijuana) fires AND at 07:00 in JP's TZ (Bogotá) fires." Without a per-user timer architecture, this can't pass.

**Proposed amendment:**
Replace the single `nexostrat-meeting-brief.timer` with:
- One timer per user: `nexostrat-meeting-brief-ricardo.timer` (OnCalendar=`*-*-* 07:00:00 America/Tijuana`), `nexostrat-meeting-brief-jp.timer` (`America/Bogota`). systemd 248+ supports per-timer TZ via `OnCalendar=America/Tijuana 07:00:00`.
- Spec section 9.4 must explicitly state: timer-per-user pattern; group briefs are sent at a separately-defined "group TZ" (probably the firm's nominal TZ).
- Add ADR-030 amendment covering the implementation pattern, not just the requirement.

---

### Finding 7 — Stage 1 go-live checklist requires Codeberg mirror; no plan delivers it

**Severity:** HIGH
**Artifact:** spec, master-index
**Location:** spec §10.6 line 911 ("Foundation: ... Gitea + GitHub + Codeberg"); master index Plan 01 (only GitHub mirror), Plans 02-10 (no mention of Codeberg)

**Description:**
Spec backup ladder includes 7 layers, layer 4 = Codeberg. Stage 1 go-live checklist requires Codeberg present. Plan 01 ships GitHub only. Plan 01 line 2297 has a commented-out `# - mirror_to_codeberg # Plan 02 Phase B` but Plan 02's master-index entry (lines 114-141) doesn't mention Codeberg at all. No plan creates the second mirror.

**Why it's wrong:**
Stage 1 cannot reach green. Either the checklist is wrong (fix spec), or a plan must own Codeberg provisioning (fix master index). Without one, the foundation grows without a mirror that the spec's recovery RTO depends on.

**Proposed amendment:**
Add Codeberg mirror to Plan 02's deliverables list, OR add a sub-task in Plan 01 Task 12.5 mirroring the GitHub flow (different remote, different PAT). The ~15-min effort doesn't justify a separate plan; just fold into Plan 01 Phase F.

---

### Finding 8 — Stage 1 checklist requires `infra/scripts/nexostrat-memos.py`; no plan creates it

**Severity:** HIGH
**Artifact:** spec, plan-01, master-index
**Location:** spec §4.7 line 378 + spec line 416 (memo scanner referenced); Plan 01 shared stanza session_start.md (line 1516) AND memo_protocol.md (line 1592) reference `python3 /srv/Nexostrat/infra/scripts/nexostrat-memos.py --to <scope>`

**Description:**
Every persona's session-start protocol (after Plan 01) calls a script that doesn't exist. Plan 01's Phase H writes the shared stanzas referencing the script; no Plan 01 task writes the script. Plan 02-10 don't mention it either.

**Why it's wrong:**
First session after Plan 01 → SessionStart hook (or Claude itself) attempts `python3 .../nexostrat-memos.py --to root` → `python3: can't open file` → broken session-start brief, no memo surfacing. Operator-driven scope rule depends on memos as the cross-bucket signal; if the scanner doesn't exist, the safety net doesn't exist.

**Proposed amendment:**
Either:
- Add Plan 01 Task 17.5: write `infra/scripts/nexostrat-memos.py` (~40 lines reading `**/00_META/inbox/*.md` frontmatter, filtering by `to:` field). Smoke-test it.
- Or update the shared stanza to gracefully degrade ("Until Plan 03, surface inbox contents via `ls 00_META/inbox/`").

---

### Finding 9 — Mode A and Mode B do NOT produce the same `runs/` artifacts; "same contract" claim fails spot-check

**Severity:** HIGH
**Artifact:** spec
**Location:** spec §6 (lines 538-544), Mode A + Mode B descriptions

**Description:**
Spec claims (line 16, 544): "Both modes write to the same folders so we can run them in parallel during the trial phase and compare outputs." Concrete spot-check:

Mode A workflow (manual):
- User pastes Gemini output into a file. The "raw_output" is a markdown file with whatever Gemini wrote.
- No `manifest.json` field for `model_version`, `finish_reason`, `tokens_in/out`, `latency_ms`, `prompt_hash` — the human can't capture what they didn't see.

Mode B workflow (API):
- `run_api.py` invokes Anthropic + Gemini + Grok SDKs. Each response carries `model`, `usage`, `stop_reason`, `id`. The agent writes a `manifest.json` rich with these fields.

`comparison.md` "auto-diffs the two runs" (line 544) — but the diff is between two artifacts whose schemas don't match. The judge prompt synthesizes the same `final_report.md`, but only when both modes produced raw_outputs in the same shape. They don't.

Worse: Mode A's "raw_output" is a single chat exchange; Mode B's is a single API call. If a model in Mode A required Ricardo to follow up clarifying the prompt (multi-turn), the saved file may be only the final response — losing the corrections. Mode B is single-turn by construction.

**Why it's wrong:**
ADR-022 promises Mode A↔B parity for trust-building. If `comparison.md` diffs disagree just because of metadata or multi-turn artifacts, the parity signal is noise. Audit cannot regress.

**Proposed amendment:**
Define `runs/<id>/manifest.json` schema explicitly in the spec (or in `skills/shared/`). Define which fields are MANDATORY for both modes (e.g., `mode`, `model`, `prompt_version`, `inputs_hash`, `final_report_hash`) and which are MODE-SPECIFIC (e.g., `tokens_in`, `latency_ms` only in Mode B). `comparison.md` should diff only the mandatory fields + the final_report content. Add a Plan 05 test asserting both modes write the mandatory schema.

---

### Finding 10 — Founder owns `prospects/` in §4 persona table, but `prospects/` lives at `pipeline/prospects/`

**Severity:** HIGH
**Artifact:** spec
**Location:** spec line 325 (Founder owns `prospects/`); line 233 (`pipeline/prospects/`)

**Description:**
Spec §4.1 persona table: Founder owns "Root governance, `operations/*`, `prospects/`, `infra/`, `docs/`, `knowledge/`, `vault/`". Spec §2 layout: prospects live as `pipeline/prospects/<slug>/intake/ qualification.md` — i.e., inside the Pipeline bucket owned by Client-Owner. The same applies to `vault/clients/` (lives in Founder's `vault/` but spec shared/vault_access.md says Founder MUST NOT write there).

**Why it's wrong:**
Persona scope rule conflict. When a prospect arrives:
- Founder reads it (their domain) but is structurally writing into Pipeline's bucket — strict-rules violation absent operator-driven override.
- Pipeline/Client-Owner sees prospect file appear inside their bucket and may treat it as their territory.
- Memo lifecycle ownership becomes ambiguous: which inbox does a "promote prospect to client" memo land in?

This will cause repeated cross-persona confusion in plain Claude Code sessions.

**Proposed amendment:**
Pick one: either move `prospects/` to root (Founder bucket, top-level), OR amend the persona table to say "Client-Owner owns `pipeline/clients/` and `pipeline/prospects/`; Founder owns prospect *intake processing* via memos to Client-Owner." Update spec §4.1 + the persona CLAUDE.md scope sections in Plan 01 Task 18-21 to match.

Also: the vault namespace conflict — spec line 325 says Founder owns `vault/`; vault_access.md stanza says per-bucket isolation prevents cross-bucket vault writes. Resolve: either Founder owns vault root (and partnership/legal/accounting/keys subdirs) but Client-Owner owns `vault/clients/`, OR move `vault/clients/` to `pipeline/vault/`. Pick one and write it consistently.

---

### Finding 11 — ADR-005 (PR-protected paths) and ADR-008 (Drive auth model) are marked "Accepted" but are materially changed; ADR ledger is misleading

**Severity:** HIGH
**Artifact:** spec
**Location:** spec ADR Map lines 38, 41

**Description:**
- ADR-005 in 2026-05-11 spec lists PR-protected paths as `clients/*/deliverables/`, `clients/*/proposals/`, `clients/*/contracts/`. New spec §3 Guards says protected paths are `pipeline/clients/*/{06_proposal,07_contract_onboarding}/` — different folder names, different folder hierarchy. ADR-005 is marked "Accepted" with no amendment note.
- ADR-008 in 2026-05-11 spec mandates Drive **service account** with explicit rationale "service accounts don't work cleanly with personal (non-Workspace) Drive accounts" — wait, the old spec already says "dedicated OAuth client credentials with a long-lived refresh token (managed by rclone)." The new spec table says "Drive 2TB via OAuth" — this is consistent if we squint, but the table also marks it "Accepted." Fine here, but ADR-005 above is the harder problem.
- ADR-009 is properly marked "Superseded" by ADR-021. Why is ADR-005 not marked "Amended"? The table format anticipates this (ADR-006, ADR-015, ADR-016, ADR-017 all show "Amended").

**Why it's wrong:**
A future Claude (or JP) reading the ADR ledger will see ADR-005 as Accepted, look up the old text in the prior spec, and follow stale path names. The pre-receive hook implementation (Plan 04 or so) will mismatch the ADR if implementer reads ADR-005-as-stated-in-2026-05-11.

**Proposed amendment:**
Mark ADR-005 as "Amended" in the table with note "(path naming updated for ADR-021 3-bucket structure)." Audit other ADR-001..020 for similar drift. Specifically: ADR-013 (events.jsonl path was `00_META/events.jsonl` in old spec; new spec puts it at `infra/events/events.jsonl` — also Amended, currently marked Accepted); ADR-018 (agent inventory significantly expanded — also probably needs Amended).

---

### Finding 12 — `events.json` (calendar) and `events.jsonl` (event spine) collide in name and are confused throughout Plan 01

**Severity:** HIGH
**Artifact:** spec, plan-01
**Location:** spec line 156 (`tasks.json events.json`), line 720 (`infra/events/events.jsonl`); Plan 01 line 553, 596, 1383

**Description:**
The repo has a root file `events.json` (currently exists, exists for calendar/deadline tracking — legacy from /srv/brain pattern) AND a future `infra/events/events.jsonl` (the event spine, Plan 03 deliverable). Plan 01 Task 5 verifies `events.json` is a JSON dict with `events: []`. Spec §1 file map keeps `events.json` at root. But Plan 01's warm-rsync hook (line 1383), the Gitea post-receive hook (line 1170), the shared stanza session_start.md, and the future Plan 03 all use `events.jsonl` — without the .l, plus inside `infra/events/`.

A new operator (or future Claude) reading "update events.json" in shared/session_end.md (line 1538) will not know whether to update root `events.json` (calendar) or the line-delimited `infra/events/events.jsonl` (event spine).

**Why it's wrong:**
Two files, almost-identical names, completely different schemas (JSON object vs JSON Lines), completely different purposes. Confusion is inevitable. Mode B agents that intend to append to `events.jsonl` may end up with `events.json` (a dict) clobbering the calendar.

**Proposed amendment:**
Rename root `events.json` to `calendar.json` (or merge it into `tasks.json` as a `due_dates` section). Update spec §1, Plan 01 Task 5, and shared/session_*.md stanzas accordingly. Or rename the spine to `infra/events/spine.jsonl`. Pick one rename, do it once.

---

### Finding 13 — bootstrap-machine.sh has zero macOS support; jp-heavy and likely jp-light cannot bootstrap

**Severity:** HIGH
**Artifact:** plan-01
**Location:** Plan 01 Task 23 (lines 2486-2621)

**Description:**
`bootstrap-machine.sh` branches on OS (`/etc/os-release`) for `ubuntu|debian|linuxmint` and `fedora|rhel`. macOS has no `/etc/os-release` — `OS_ID` becomes `unknown`. The `install_pkg` function then prints `[WARN] Unknown OS — manually install $pkg` for every tool. The Tailscale section runs `curl -fsSL https://tailscale.com/install.sh | sudo sh` which is Linux-only (the macOS Tailscale binary ships via the App Store). Flatpak install for Obsidian is Linux-only.

Plan 01 Task 22 Step 5/6 leave `<JP_OS>` as a placeholder ("ask JP"). If JP runs macOS (probable for a strategy-and-review consultant working out of Bogotá), then `bootstrap-machine.sh jp-heavy` produces a wall of warnings and installs nothing.

**Why it's wrong:**
Master index Plan 01 success criterion: "A new clone on a fresh machine runs `bootstrap-machine.sh ricardo-travel` and completes successfully." This passes only because Ricardo's machines are all Linux. The replicability promise (audit brief: "Could JP onboard cold from these docs?") is false for any non-Linux JP.

**Proposed amendment:**
Either (a) add Darwin branch with `brew` (and document `brew` as a prerequisite), OR (b) explicitly scope `bootstrap-machine.sh` to Linux-only and write a separate `bootstrap-macos.md` runbook in Plan 02 covering the manual install path. Don't ship a script that silently does nothing.

---

### Finding 14 — Notion is "$0 to firm" but the Notion AI used for canonical meeting capture requires a paid plan

**Severity:** HIGH
**Artifact:** spec
**Location:** spec §5 cost table line 431; §8 line 631 ("Internal R+JP | Notion AI | ..."); §8 line 650 ("Notion AI default polished")

**Description:**
The cost table says "Notion | $0 to firm | JP (his account)." But the canonical meeting capture (the spine of §8) uses **Notion AI** for transcription + summarization, which requires Notion AI Add-on at $10/user/month for the workspace where meetings are recorded. If JP's personal Notion is the workspace, JP pays personally; if the firm's account is separate, the firm pays. Either way it's not $0.

Compounding: spec line 633 says "Notion AI default polished" for client meetings too, and ADR-024 Option A is "Notion AI (default)." If clients are polled to pick A, B, or C, every Option-A client multiplies the seat cost.

**Why it's wrong:**
Stage 1 cost claim "USD $36-91/month" is undercounted by at least $10/seat × N seats. With R + JP both needing Notion AI for internal meetings, that's already $20/month off the books. With clients picking A, scales further.

**Proposed amendment:**
Either (a) update §5 cost table: "Notion AI add-on | $10-30/mo | JP/firm | Meeting transcription" and revise the $36-91 envelope to $46-121, OR (b) make Whisper.cpp the canonical for ALL internal meetings (Notion AI moves to "shadow" or removed entirely) and re-derive ADR-024.

---

### Finding 15 — Plan 01 file map promises questionnaires migration, but no Plan 01 task does the conversion

**Severity:** HIGH
**Artifact:** plan-01
**Location:** Plan 01 line 118 ("MODIFIED FILES: ... 00_PARTNERSHIP/questionnaires/ (import 2 .docx files; convert to .md)"); Plan 01 Tasks 1-28 — none touch the docx files

**Description:**
The file map in Plan 01 explicitly promises that the existing `Plan_Maestro_MejiaIACia_Ricardo.docx` and `Plan_Maestro_MejiaIACia_JP.docx` (currently sitting at `/srv/Nexostrat/`) are converted to markdown and migrated into `00_PARTNERSHIP/questionnaires/`. No task in Plan 01 actually does this; Task 3 just `touch`es `.gitkeep` in the empty folder. The two .docx files remain at the root of the repo (where they don't belong per spec §2 — root only has a small set of governance files, not .docx legacy artifacts).

**Why it's wrong:**
Plan 01 self-reports as complete with a stale promise. Stage 1 go-live checklist (spec §10.6) requires "partnership docs filled + signed" — questionnaires are the input to that. They never get filed.

**Proposed amendment:**
Add Plan 01 Task 5.5 (or 21.5): "Migrate Plan Maestro questionnaires." Steps:
1. `pandoc Plan_Maestro_MejiaIACia_Ricardo.docx -o 00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md`
2. Same for JP.
3. Move the original .docx files to `00_PARTNERSHIP/questionnaires/archive/` (preserving via .gitattributes LFS rule from Task 4).
4. Move the `.backup-2026-05-07.docx` to `archive/` too.
5. Move `Consultoria_IA_PYMEs_v1.pdf` to `operations/assets/`.
6. Commit.

---

### Finding 16 — `pipeline/clients/_template/` ships empty in Plan 01; Plan 07 success criteria assume it's populated; ordering trap

**Severity:** MEDIUM
**Artifact:** master-index, plan-01
**Location:** Plan 01 line 256-257 (creates `_template/.gitkeep` only); master index Plan 07 line 281 ("`_template/` complete (all 12 stations + 3 cross-cutting folders + state.json template)")

**Description:**
Plan 01 creates `pipeline/clients/_template/` as an empty folder (just `.gitkeep`). Master index Plan 07 says Plan 07 deliverable IS `_template` complete with all 12 stations. Reasonable in principle. But the spec §2 layout (line 230) shows `_template/` as "canonical empty client folder" sitting next to `bodai/` (which Plan 05 populates). Plan 05 deliverables don't mention `_template`. So between Plan 05 (Bodai populated) and Plan 07 (`_template` populated), `bodai/` exists with full structure but `_template/` is empty. Any agent looking up the "canonical structure" between Plan 05 and Plan 07 has no canonical to read.

**Why it's wrong:**
Plan 05 populates Bodai by ad-hoc decision; Plan 07 documents the template afterwards. The order should be: (1) define template, (2) clone for Bodai. Otherwise Bodai's structure becomes the de-facto template by precedent rather than design.

**Proposed amendment:**
Move "_template/ structure (12 stations + state.json schema)" into Plan 01 Task 3 or a new Plan 01 Task 21.5. The structure is just folders + a state.json schema file; doesn't depend on agents or skills. ~15 min of work moved earlier prevents Plan-05/07 ordering ambiguity.

---

### Finding 17 — Encrypted ambient chat logs have no concurrent-write protection; race on simultaneous messages

**Severity:** MEDIUM
**Artifact:** spec
**Location:** spec §8.10 line 700 (`infra/telegram/chat_log/{group,dm-ricardo,dm-jp}/YYYY-MM-DD.jsonl.age`)

**Description:**
The bot must add each Telegram message to a daily `.age`-encrypted JSONL file. Atomic append via `O_APPEND` works on plain JSONL (POSIX guarantees writes < PIPE_BUF are atomic). But for `.age` ciphertext, "append" means: decrypt the existing file in RAM, append the new line in plaintext, re-encrypt the entire file, replace. This is a read-modify-write cycle, NOT atomic. Two messages arriving in the same second to the bot — handled in two concurrent threads or async tasks — cause:

1. Thread A reads ciphertext_v1 → decrypts → appends line A.
2. Thread B (microseconds later) reads ciphertext_v1 → decrypts → appends line B.
3. Thread A re-encrypts → writes ciphertext_v2 (with line A only).
4. Thread B re-encrypts → writes ciphertext_v3 (with line B only, A is gone).

Result: line A is silently lost. No corruption signal because the file is still valid age ciphertext.

The audit brief flagged "race conditions if two messages arrive simultaneously with same timestamp." This is the structural cause.

**Why it's wrong:**
Bot must serialize writes. Spec doesn't specify how. The `events.jsonl` spine (line 741) uses "atomic append" — works because plaintext + O_APPEND. The chat log can't use the same pattern because it's encrypted at rest.

**Proposed amendment:**
Either:
- Append plaintext JSONL to `/dev/shm/chat_log/group/YYYY-MM-DD.jsonl` during the day (using O_APPEND atomicity), then have a daily 23:59 job that encrypts the whole day's file to .age at the end. Trade-off: plaintext on RAM tmpfs for ~24h.
- Use a single async event loop in the bot that serializes all writes via a per-file asyncio.Lock. Requires explicit spec.
- Use a SQLite WAL-mode database keyed by chat_id+date, encrypted via SQLCipher. Different file format but mature concurrency story.

Pick one and document in spec §8.10 + Plan 09.

---

### Finding 18 — Persona ownership table and operator-driven scope rule are mutually inconsistent for vault writes

**Severity:** MEDIUM
**Artifact:** spec
**Location:** spec §4.1 line 325 (Founder "owns" vault); shared/vault_access.md (Plan 01 line 1641: "Per-bucket vault namespaces ... No cross-bucket vault writes regardless of operator-driven scope rule.")

**Description:**
Founder is listed as owner of `vault/`. Vault stanza says "No cross-bucket vault writes regardless of operator-driven scope rule." Then how does Founder write `vault/clients/<slug>/` (which spec §3.2 shows as a folder)? Either Founder is the writer (consistent with persona table) and the per-bucket isolation is wrong, or per-bucket isolation is correct and Founder is NOT the writer of `vault/clients/`.

**Why it's wrong:**
Real scenario: Ricardo signs first contract with Bodai. The signed PDF goes into `vault/clients/bodai/contracts/`. Ricardo is in a Founder session. Per persona table he can write the file (Founder owns vault). Per vault_access.md stanza he cannot (only Client-Owner writes `vault/clients/`). Same operator, same action, two contradictory rules.

**Proposed amendment:**
Update §4.1 persona table: split vault by namespace. Founder writes `vault/{partnership,legal,accounting,keys}/`. Client-Owner writes `vault/clients/<slug>/`. Skills-Master writes none (no vault content). Make the table show namespace ownership explicitly. Then vault_access.md stanza is consistent.

---

### Finding 19 — Spec uses "13-station chain" in §4 persona table but "12 stations + 3 cross-cutting" in §7

**Severity:** MEDIUM
**Artifact:** spec
**Location:** spec §4 line 327 ("Active client work (the 13-station chain)"); §7 line 565 ("12 stations + 3 cross-cutting"); spec §2 line 232 ("12-station chain inside")

**Description:**
Three different counts in three sections. §7 actually has 12 ordered stations (`00_intake/` through `11_retainer/`) plus 3 cross-cutting (`transcripts/`, `communications/`, `archive/`) — so 15 folders total inside a client. The "13" in §4 is a leftover from the 2026-05-11 spec which counted the 12 + 2 (didn't include `archive/`). Naming drift confuses operators.

**Why it's wrong:**
A future operator reading §4 expects 13 folders, looks at §7, finds 15. Trivially confusing.

**Proposed amendment:**
Pick one description and use it everywhere. Recommend "12-station chain plus 3 cross-cutting folders" (the §7 wording). Update §2 and §4 to match.

---

### Finding 20 — `BRAIN_STATUS.md` reference in shared/session_output_format.md is a leak from /srv/brain personal-Brain conventions

**Severity:** MEDIUM
**Artifact:** plan-01
**Location:** Plan 01 line 1574 (shared/session_output_format.md): "Never invent counts. If `BRAIN_STATUS.md` / inbox scanner returns empty, say 'none' or omit the bullet."

**Description:**
Nexostrat is a separate repo from /srv/brain. There is no `BRAIN_STATUS.md` in this repo. The reference is copy-paste from Ricardo's personal Brain stanza. Operators following the protocol will look for a file that doesn't exist.

**Why it's wrong:**
Carryover artifact undermines the "self-contained spec" promise. Could be missed for months — the surface symptom (Claude says "BRAIN_STATUS.md not found") is recoverable but signals to JP that the docs are stale.

**Proposed amendment:**
Replace `BRAIN_STATUS.md` with the appropriate Nexostrat file (probably `STATUS.md`) or remove the clause entirely. Audit all 9 shared stanzas in Plan 01 Task 17 for similar leaks (`/srv/brain/`, `BRAIN_STATUS`, `00_TEMPLATES/` etc. — the memo_protocol.md stanza references `00_META/00_TEMPLATES/memo_template.md` which isn't created until Plan 02).

---

### Finding 21 — `tasks.json $schema` is `brain-tasks-v1`, a personal-Brain schema; nothing in Nexostrat enforces it

**Severity:** MEDIUM
**Artifact:** plan-01
**Location:** Plan 01 line 561 (`"$schema": "brain-tasks-v1"`)

**Description:**
The schema string identifies the task list as conforming to a schema defined in /srv/brain. Nexostrat has no validator for this schema. If schema drifts (root brain tweaks fields), Nexostrat tasks.json is silently invalidated. If Nexostrat needs different fields (per ADR or per persona), there's no clean way to evolve.

**Why it's wrong:**
Coupling without validation. Eventually one repo or the other drifts; nobody notices until something breaks.

**Proposed amendment:**
Define `nexostrat-tasks-v1` (~20 lines of JSON Schema) and commit at `infra/schemas/tasks.schema.json`. Validate in pre-commit hook or in a Plan 03 unit test. Use that schema string. Same for `brain-events-v1`.

---

### Finding 22 — Inconsistency: spec line 461 says n8n at `/srv/atten-bot/`, Plan 01 line 525 says `/home/ricardo/n8n/`

**Severity:** MEDIUM
**Artifact:** spec, plan-01
**Location:** spec line 461; Plan 01 docker-compose.yml comment line 525

**Description:**
Spec asserts n8n lives at `/srv/atten-bot/`. Plan 01 docker-compose.yml header comment says it lives at `/home/ricardo/n8n/`. Both can't be right. Operationally relevant because Plan 01 Task 13 (Gitea hook install) needs to find Gitea's storage path, which is also a separate stack.

**Why it's wrong:**
Future Claude trying to interact with n8n (e.g., to confirm it's NOT touched, per ADR-029) needs to know where to look. Two different paths makes this unreliable.

**Proposed amendment:**
Verify the actual location (`docker inspect` or `docker compose ls`), update both spec line 461 and Plan 01 line 525 to the correct path. Add to `00_GOVERNANCE/system_map.md` (Plan 01 Task 14 deliverable) explicitly: "AttenBot n8n stack: <path>".

---

### Finding 23 — Plan 01 `.gitignore` is not updated; only `excalidraw.log` is ignored; ~/.age, /dev/shm leaks possible if scripts mis-write

**Severity:** MEDIUM
**Artifact:** plan-01
**Location:** Plan 01 file map (no `.gitignore` modification)

**Description:**
Existing `.gitignore` (verified: 1 line, just `excalidraw.log`). Plan 01 doesn't update it. If any operator-error or buggy script writes a `.env` file at the repo root, an age private key, a `/dev/shm` symlink, or a Python `__pycache__/` dir, it would be staged by `git add .` patterns. The pre-commit file-pattern-block hook (Task 25) catches `.env` and `*.key`, but not `__pycache__/`, `.pyc`, `.venv/`, IDE artifacts (`.idea/`, `.vscode/`), `node_modules/`, `*.log`, `.DS_Store`, etc. As Python infra grows in Plan 03, accidental `__pycache__` commits are nearly inevitable.

**Why it's wrong:**
Belt-and-suspenders missing. Pre-commit hook is one layer; .gitignore is the lower layer. Both are needed.

**Proposed amendment:**
Add Plan 01 Task 4 Step 4.5: write a comprehensive `.gitignore` covering Python, Node, IDE, OS, Docker, age private keys (`*.key`, `*.key.age` is allowed but the script that decrypts should never write into the repo), shm dumps, log files, etc.

---

### Finding 24 — Smoke test claims "warm-rsync systemd timer enabled" but Plan 01 Task 16 leaves `<STANDBY_HOST>` as a placeholder; smoke test fails on fresh execution

**Severity:** MEDIUM
**Artifact:** plan-01
**Location:** Plan 01 Task 16 Step 3 (line 1414: `Environment="STANDBY_HOST=<STANDBY_HOST>"`) + Task 27 line 3165 (`check "warm-rsync systemd timer enabled" ...`)

**Description:**
Task 16 says "Replace `<STANDBY_HOST>` with the real value." The systemd unit file then gets installed with whatever the user pasted. If user forgets, the timer is enabled but the service errors on first fire. Task 27 smoke test only checks `systemctl is-enabled` (returns "enabled" regardless of whether the unit can run). It doesn't test the unit succeeds.

**Why it's wrong:**
False positive. Smoke test passes; warm-standby is broken. Discovered only at first 03:00 cron fire (i.e., the next day, after Plan 01 is "done").

**Proposed amendment:**
Add Task 27 check: `systemctl start nexostrat-warm-rsync.service && systemctl status nexostrat-warm-rsync.service --no-pager | grep -q 'Main PID:.*code=exited, status=0/SUCCESS'`. Alternatively, run the script in dry-run mode (rsync --dry-run) and verify exit 0.

---

### Finding 25 — Gitea owner inconsistency: spec says org `nexostrat`, Plan 01 paths say `RicardoMejiaCaicedo`

**Severity:** LOW
**Artifact:** spec, plan-01
**Location:** spec ADR-002 line 35 (Gitea org `nexostrat`); Plan 01 lines 1181, 1314 (`RicardoMejiaCaicedo/nexostrat.git`)

**Description:**
ADR-002 in the new spec says the Gitea org is `nexostrat` (renamed from `Mejia-IACia`). Plan 01 example paths assume the repo is at `RicardoMejiaCaicedo/nexostrat.git` (Ricardo's personal username, not the firm's org).

**Why it's wrong:**
Either ADR-002 is wrong (the repo lives under Ricardo's personal namespace, not under a firm org), or Plan 01 paths are wrong (should say `nexostrat/nexostrat.git`). Either way: inconsistent and the smoke test/grep that matches `100.64.121.80` doesn't catch it.

**Proposed amendment:**
Decide: org or personal namespace. Update both spec ADR-002 and Plan 01 references. Org gives JP equal-owner posture; personal namespace is operationally simpler.

---

### Finding 26 — `phones.yaml` doesn't differentiate iOS vs Android nuances; minor but flagged in audit brief

**Severity:** LOW
**Artifact:** plan-01
**Location:** Plan 01 Task 22 Step 7 (lines 2451-2466)

**Description:**
phones.yaml lists `apps_required: [telegram-mobile]` and chat_id allowlists. No platform field. iOS Telegram has stricter background restrictions (push tokens, no long-lived background tasks); Android can run a background polling agent if the user wants. Voice notes via `/voice` (spec §4.11) may upload differently. Allowlist mechanics are identical, but operational behavior differs.

**Why it's wrong:**
Mostly fine — Telegram client UX is consistent enough for v1. But phones.yaml should at least record platform so future runbooks (battery optimization, push token re-auth) can branch.

**Proposed amendment:**
Add per-user `platform: ios|android` field in phones.yaml. No code change needed at Plan 01.

---

### Finding 27 — Old spec offered 3 JP options (Heavy/Hosted/Light); new spec drops Hosted with no ADR; `STATUS.md` (Plan 01) still references Hosted

**Severity:** LOW
**Artifact:** spec, plan-01
**Location:** 2026-05-11 spec lines 53-74 (Hosted = code-server option); new spec line 133-136 (only Heavy + Light listed); Plan 01 STATUS.md hand-off note line 931 ("JP interface choice (Heavy/Hosted/Light). Confirmed approved as Light")

**Description:**
Hosted (code-server on HP) was option B in the original. New spec mentions code-server only as Stage 2 trigger ("code-server ← JP picks Hosted") — implicitly retains Hosted as a future option, but the JP-laptop description (line 133-136) covers only Heavy and Light. Plan 01 ships only `jp-light.yaml` and `jp-heavy.yaml` profiles (no `jp-hosted.yaml`).

**Why it's wrong:**
Minor inconsistency. Either Hosted is dead (write an ADR superseding it) or it's alive (add the profile or document the deferral explicitly).

**Proposed amendment:**
Either (a) write an explicit ADR-021bis "Drop Hosted from JP options," or (b) keep Hosted but make jp-hosted.yaml a Stage 2 trigger deliverable. Update Plan 01 STATUS.md to reflect.

---

### Finding 28 — Plan 01 internal task-count contradiction: tasks.json says "~40 tasks", journal says 28, Plan body has 28

**Severity:** LOW
**Artifact:** plan-01
**Location:** Plan 01 line 440 ("Currently at Task 4 of ~40"), line 572 ("~40 tasks"), line 3269 ("All 28 tasks executed"), line 3364 ("28 tasks")

**Description:**
Pure documentation drift. Plan 01 body has Tasks 1 through 28. tasks.json and CHECKPOINT.md reference "~40 tasks." Journal entry and CHANGELOG say 28.

**Why it's wrong:**
Trivial; only confusing.

**Proposed amendment:**
Search/replace "~40" → "28" in Plan 01 lines 440 and 572.

---

## Surface coverage

**Thoroughly examined:**
- All 10 sections of the founding spec (full read pass).
- All 28 Plan 01 tasks (full read of task bodies, scripts, validation checks).
- Master plan index dependency graph + per-plan deliverables/success criteria.
- Cross-references between spec ADR Map and the prior 2026-05-11 spec (drift check on ADRs 001-020).
- Secrets workflow: `secrets.env.age` lifecycle, wrapper script trap behavior, /dev/shm cleanup claims.
- Gitea post-receive hook execution context.
- Vault key recovery model.
- Per-user TZ / DST handling.
- Mode A vs Mode B contract.
- File map vs task body reconciliation.
- Persona ownership table vs filesystem layout.
- Repository state on disk (git status, current `.gitignore`, current `00_META/skills/`).

**Skimmed (read but not exhaustively cross-checked):**
- Per-skill folder template (ADR-012) — checked it's referenced consistently; didn't audit prompt structure.
- Aurora pandoc template (ADR-033) — out of architectural scope.
- Per-machine YAML profiles 4-7 (ricardo-travel, jp-light, jp-heavy, phones) — checked structure, didn't deeply audit deps.
- Failure modes catalog (§10) — verified categories exist; didn't audit each of ~30 specific failure modes for runbook completeness.
- Glossary terms — spot-checked for consistency.

**Not examined:**
- Existing docker-compose stacks for AttenBot or n8n (not in scope of this repo).
- Whether the existing `00_META/skills/company-analyst/` extracted bundle is actually well-formed (Plan 05 territory).
- Plain-English `-explicado.md` partners (`README-explicado.md`, `2026-05-13_plan-01-repository-foundation-explicado.md`) — audit brief says "optional supporting context"; spent budget on the canonical artifacts.
- Subagent-driven-development skill execution mechanics (whether Plan 01 tasks decompose cleanly to subagents — would need to read superpowers skill itself).
- Network/Tailscale ACL configuration (would need to inspect Tailscale admin console state).
- Whether `age` 1.0+ behaves as the spec assumes on Linux Mint 22.2 (would need actual install test).

---

## Recommendations beyond findings

1. **Right-size Plan 01.** The plan attempts: scaffold + identity + secrets + GitHub mirror + warm-standby + persona files + bootstrap + hooks + smoke test, all in one ~1-week plan with ~120 atomic steps. Several findings (1, 2, 3, 4, 8, 13, 15) point to Plan 01 being overstuffed. Consider splitting:
   - Plan 01a (scaffold + identity + vault recovery decision) — 1-2 days.
   - Plan 01b (secrets + mirror + warm-standby) — 2-3 days.
   - Plan 01c (persona files + hooks + smoke test) — 2 days.
   Each independently testable. Reduces blast radius of a single bug.

2. **Pre-flight test harness.** The smoke test (Task 27) checks file existence and timer enable-state, not real correctness. Several findings (1, 4, 24) are bugs the smoke test doesn't catch. Build a richer integration test harness that actually decrypts a sample, pushes a test commit, waits for mirror, and verifies the GitHub HEAD changed. Spend the 2-3 hours on it.

3. **The "marginal cost of completeness near zero with AI" principle is sound, but execution complexity remains non-zero.** Examples: the per-user TZ delivery flush every 5 min; the chat extractor with confidence loop and confirmation timer; the dual meeting capture with parity diff. Each is a moving part. Consider an ADR explicitly listing "Stage 1 surface area" — items where v1 is lower-fidelity OK (e.g., morning brief at one shared TZ until per-user is needed). The current plan tries to ship everything at the foundation level.

4. **The CHECKPOINT.md pattern (ADR-031) is good, but needs concurrent-session protection.** What happens if Ricardo is in a Claude Code session at root AND Claude Code at `/skills/` simultaneously? Both write CHECKPOINT.md at session-end. The persona-scoped CHECKPOINTs (one per persona) help, but the root CHECKPOINT.md can still race if Ricardo opens two roots. Spec doesn't address. Add a SessionStart hook check: if CHECKPOINT.md has been modified within the last N minutes by a different session, warn.

5. **Consider whether Notion's role is really $0.** Finding 14 surfaces a price; the bigger question is whether Notion is the right canonical for client meeting transcripts at all. It's JP's personal account, it's a third-party SaaS holding firm IP, the API is rate-limited, and Notion AI workflows change frequently. The shadow (Whisper.cpp + Jitsi) is self-hosted and free. Inverting them — making Whisper canonical for everything, Notion shadow only for the client UX nicety — would simplify cost, security, and recovery models. Worth an ADR.

6. **Document the Plan 01 happy-path duration in calendar time, not "~1 week."** Real duration depends heavily on whether DECISION POINTs (warm-standby host, JP age key, GitHub username, Gitea storage path) take 5 min or 5 days to resolve. Current Plan 01 lists "Plan 01 due 2026-05-20" (7 days) but several decision points are blocked on JP availability (10h/wk). More honest planning: 2-3 weeks calendar.
