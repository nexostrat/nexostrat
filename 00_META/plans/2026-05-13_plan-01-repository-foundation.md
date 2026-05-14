# Plan 01 — Repository Foundation Implementation Plan

> **⚠️ SUPERSEDED 2026-05-14.** This plan is replaced by Plans **01a / 01b / 01c** per the 2026-05-14 audit amendment plan ([`../proposals/2026-05-14_amendments.md`](../proposals/2026-05-14_amendments.md) §R1). The audit (RED with DESIGN-RETHINK FLAG, 28 findings) showed that a single Plan 01 was the wrong shape — too large to audit reliably and bundled three independently-testable milestones. Plans 01a (scaffold + identity + crypto), 01b (mirrors + warm-standby), and 01c (personas + hooks + integration test) replace it. **Do not execute this plan as written.** Its tasks have been redistributed; read it only for historical context. The header-level replacements live in [`README.md`](README.md) under their respective sections, and the full task detail will be written via `superpowers:writing-plans` in Batch 2 of the amendment-execution sequence.
>
> **Replacement milestones:** v0.1a-foundation (end of 01a) · v0.1b-mirrors (end of 01b) · v0.1-foundation (end of 01c — original Plan 01 milestone).

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the 3-bucket repository structure for Nexostrat, lock identities (age keypairs), stand up the backup ladder, write the persona files, and ship a working smoke test so all subsequent plans have a stable foundation.

**Architecture:** Skills / Pipeline / Operations buckets at root with cross-cutting governance + infra + docs + vault + knowledge. age per-user encryption for vault + secrets, decrypted to `/dev/shm` (RAM tmpfs) at use time. Gitea origin already running; add GitHub private mirror via post-receive hook. Warm-standby second laptop via nightly rsync. Persona files (3 CLAUDE.md + 3 GEMINI.md) and per-machine YAML profiles drive the rest of the system.

**Tech Stack:** Linux Mint 22.2 on HP server; bash + Python 3.12 for scripts; `age` 1.0+ for encryption; `rclone` for Drive; Docker Compose for services (Gitea already running); git 2.40+; Pandoc 3.1+; Tailscale mesh (already active).

**Plain partner:** [`2026-05-13_plan-01-repository-foundation-explicado.md`](2026-05-13_plan-01-repository-foundation-explicado.md)

---

## Prerequisites (verify before Task 1)

Before any task in this plan:

- [ ] You are running this from `/srv/Nexostrat/` (verify: `pwd` returns `/srv/Nexostrat`)
- [ ] Per-repo git author is `Nexostrat <contacto@nexostrat.com>` (verify: `git config user.email`)
- [ ] You have read [`../proposals/2026-05-13_nexostrat-system-design.md`](../proposals/2026-05-13_nexostrat-system-design.md) in full
- [ ] You have read [`README.md`](README.md) (master plan index)
- [ ] The HP laptop is the machine you're working on (verify: `hostname` returns `ricardo-hp-laptop`)
- [ ] Gitea is reachable at `100.64.121.80:3001` (verify: `curl -sI http://100.64.121.80:3001 | head -1`)

**Decision points during this plan** (you will be asked at execution time):
- The hostname / Tailscale IP of the warm-standby laptop (Task 24)
- Whether JP's age public key is available (Task 11; if not, vault is encrypted to Ricardo only with explicit follow-up memo)
- The GitHub username and repo name for the mirror (Task 19)

---

## File map — what gets created or modified

```
NEW FILES (created during this plan):
  /srv/Nexostrat/
  ├─ STATUS.md                              (root, current phase)
  ├─ CHECKPOINT.md                           (root persona baton)
  ├─ .gitattributes                          (LFS rules for binary assets)
  ├─ docker-compose.yml                      (placeholder; populated in Plan 04)
  ├─ .env.example                            (placeholder)
  ├─ secrets.env.age                         (encrypted secrets store)
  │
  ├─ 00_META/
  │  ├─ inbox/.gitkeep, inbox/archive/.gitkeep
  │  └─ shared/{rule1_operator_scope,session_start,session_end,
  │            session_output_format,memo_protocol,gemini_handoff,
  │            vault_access,backup_policy,checkpoint_pattern}.md
  │
  ├─ 00_GOVERNANCE/
  │  ├─ README.md  README-explicado.md
  │  ├─ DECISIONS.md
  │  ├─ adr/.gitkeep
  │  └─ system_map.md
  │
  ├─ 00_PARTNERSHIP/
  │  ├─ README.md  README-explicado.md
  │  ├─ questionnaires/.gitkeep, archive/.gitkeep
  │  ├─ meetings/weekly/.gitkeep, decisions/.gitkeep
  │  └─ reviews/.gitkeep
  │
  ├─ skills/
  │  ├─ CLAUDE.md  GEMINI.md  CHECKPOINT.md
  │  └─ shared/.gitkeep
  │
  ├─ pipeline/
  │  ├─ CLAUDE.md  GEMINI.md  CHECKPOINT.md
  │  ├─ clients/_template/.gitkeep
  │  └─ prospects/.gitkeep
  │
  ├─ operations/
  │  └─ {marketing,sales,accounting,legal,it,templates,assets}/.gitkeep
  │
  ├─ docs/
  │  ├─ README.md  README-explicado.md
  │  └─ {tutorials,how-to,reference,explanation,runbooks}/.gitkeep
  │
  ├─ infra/
  │  ├─ age-recipients.txt
  │  ├─ scripts/
  │  │  ├─ run-with-secrets.sh
  │  │  ├─ bootstrap-machine.sh
  │  │  ├─ warm-standby-rsync.sh
  │  │  └─ smoke-test.sh
  │  ├─ machines/
  │  │  ├─ hp-server.yaml  hp-standby.yaml
  │  │  ├─ ricardo-desktop.yaml  ricardo-travel.yaml
  │  │  ├─ jp-light.yaml  jp-heavy.yaml
  │  │  └─ phones.yaml
  │  ├─ secrets/
  │  │  └─ MANIFEST.md
  │  ├─ hooks/
  │  │  ├─ pre-commit-secret-scan.sh
  │  │  ├─ pre-commit-file-pattern-block.sh
  │  │  ├─ install-hooks.sh
  │  │  └─ tests/test_hooks.sh
  │  ├─ gitea/
  │  │  └─ post-receive-mirror.sh
  │  └─ recovery/                            (folder only; first scripts arrive in Plan 04)
  │     └─ .gitkeep
  │
  ├─ vault/
  │  ├─ README.md  sensitive_index.md
  │  └─ .encrypted/.gitkeep
  │
  └─ knowledge/
     └─ {sectors,quick_wins,source_caches}/.gitkeep

MODIFIED FILES:
  /srv/Nexostrat/
  ├─ README.md                               (already exists; update with brand)
  ├─ CLAUDE.md                               (already exists; rewrite as Founder persona)
  ├─ GEMINI.md                               (already exists; rewrite as Founder Gemini)
  ├─ tasks.json                              (already exists; reset for new phase)
  ├─ events.json                             (already exists; verify empty)
  ├─ 00_META/CHANGELOG.md                    (append Plan 01 entry)
  └─ 00_PARTNERSHIP/questionnaires/          (import 2 .docx files; convert to .md)
```

---

## Phase A — Verify starting state

### Task 1: Confirm clean repo + correct git author

**Files:** No changes.

- [ ] **Step 1: Verify pwd**

Run: `pwd`
Expected: `/srv/Nexostrat`

If wrong: `cd /srv/Nexostrat` and re-verify.

- [ ] **Step 2: Verify git status is clean**

Run: `git status`
Expected: `nothing to commit, working tree clean`

If dirty: investigate before continuing. Do NOT mass-stash without understanding what's there.

- [ ] **Step 3: Verify per-repo git author**

Run: `git config user.email`
Expected: `contacto@nexostrat.com`

If wrong:
```bash
git config user.name "Nexostrat"
git config user.email "contacto@nexostrat.com"
```
Then re-verify.

- [ ] **Step 4: Verify the founding spec is present**

Run: `test -f 00_META/proposals/2026-05-13_nexostrat-system-design.md && echo OK || echo MISSING`
Expected: `OK`

If missing: STOP. Plan 01 derives from this spec; cannot proceed without it.

- [ ] **Step 5: Verify Gitea reachable**

Run: `curl -sI http://100.64.121.80:3001 | head -1`
Expected: `HTTP/1.1 200 OK` (or `302 Found` — both indicate Gitea responding)

If unreachable: check `docker ps | grep gitea` and `tailscale status`. Fix before proceeding.

---

## Phase B — Folder scaffold

### Task 2: Create the 3 bucket folders + cross-cutting top-level folders

**Files:**
- Create: `skills/`, `pipeline/`, `operations/`, `docs/`, `infra/`, `vault/`, `knowledge/`

- [ ] **Step 1: Verify which top-level folders already exist**

Run: `ls -la /srv/Nexostrat/ | grep '^d'`
Note: `00_META/` already exists (with proposals/, journal/, handoff/, skills/, scripts/). The 7 new ones (`skills/`, `pipeline/`, etc.) should NOT exist yet. `00_META/skills/` does exist but is the extracted skill bundles, separate from the new top-level `skills/`.

- [ ] **Step 2: Create the 7 new top-level folders**

Run:
```bash
mkdir -p skills pipeline operations docs infra vault knowledge
```

Verify:
```bash
ls -d skills pipeline operations docs infra vault knowledge
```
Expected: all 7 names returned, one per line.

- [ ] **Step 3: Place .gitkeep in each new bucket so they survive a commit**

Run:
```bash
for d in skills pipeline operations docs infra vault knowledge; do
  touch "$d/.gitkeep"
done
```

- [ ] **Step 4: Stage and commit the buckets**

```bash
git add skills/.gitkeep pipeline/.gitkeep operations/.gitkeep docs/.gitkeep infra/.gitkeep vault/.gitkeep knowledge/.gitkeep
git commit -m "Plan 01 Task 2: scaffold 3-bucket structure + cross-cutting folders"
```

Expected: 1 commit, 7 files created.

---

### Task 3: Create the per-bucket subfolder hierarchy

**Files:**
- Create: many subfolders per the file map above. All initially empty (`.gitkeep`).

- [ ] **Step 1: Create 00_META subfolders that don't yet exist**

Run:
```bash
mkdir -p 00_META/inbox/archive 00_META/shared
touch 00_META/inbox/.gitkeep 00_META/inbox/archive/.gitkeep 00_META/shared/.gitkeep
```

- [ ] **Step 2: Create 00_GOVERNANCE structure**

Run:
```bash
mkdir -p 00_GOVERNANCE/adr
touch 00_GOVERNANCE/adr/.gitkeep
```

- [ ] **Step 3: Create 00_PARTNERSHIP structure**

Run:
```bash
mkdir -p 00_PARTNERSHIP/questionnaires/archive 00_PARTNERSHIP/meetings/weekly 00_PARTNERSHIP/meetings/decisions 00_PARTNERSHIP/reviews
touch 00_PARTNERSHIP/questionnaires/.gitkeep 00_PARTNERSHIP/questionnaires/archive/.gitkeep
touch 00_PARTNERSHIP/meetings/weekly/.gitkeep 00_PARTNERSHIP/meetings/decisions/.gitkeep
touch 00_PARTNERSHIP/reviews/.gitkeep
```

- [ ] **Step 4: Create skills/, pipeline/, operations/, docs/, knowledge/, vault/, infra/ subfolders**

Run:
```bash
# skills
mkdir -p skills/shared
touch skills/shared/.gitkeep

# pipeline
mkdir -p pipeline/clients/_template pipeline/prospects
touch pipeline/clients/_template/.gitkeep pipeline/prospects/.gitkeep

# operations
mkdir -p operations/{marketing,sales,accounting,legal,it,templates,assets}
for d in marketing sales accounting legal it templates assets; do
  touch "operations/$d/.gitkeep"
done

# docs (Diátaxis)
mkdir -p docs/{tutorials,how-to,reference,explanation,runbooks}
for d in tutorials how-to reference explanation runbooks; do
  touch "docs/$d/.gitkeep"
done

# knowledge
mkdir -p knowledge/{sectors,quick_wins,source_caches}
for d in sectors quick_wins source_caches; do
  touch "knowledge/$d/.gitkeep"
done

# vault
mkdir -p vault/.encrypted
touch vault/.encrypted/.gitkeep

# infra
mkdir -p infra/{agents/_lib,scripts,machines,secrets,hooks/tests,gitea,recovery,telegram,events/schemas,shadow,systemd,observability}
for d in agents scripts machines secrets hooks gitea recovery telegram events shadow systemd observability; do
  test -d "infra/$d" || mkdir -p "infra/$d"
done
# Sub-.gitkeeps for placeholders that will be populated in later plans
touch infra/agents/_lib/.gitkeep
touch infra/telegram/.gitkeep
touch infra/events/schemas/.gitkeep
touch infra/shadow/.gitkeep
touch infra/systemd/.gitkeep
touch infra/observability/.gitkeep
```

- [ ] **Step 5: Verify the tree**

Run: `find . -type d -not -path './.git*' | sort`
Expected: All planned folders present, no extras. Spot-check that each bucket has its expected subfolders.

- [ ] **Step 6: Stage and commit**

```bash
git add 00_META/ 00_GOVERNANCE/ 00_PARTNERSHIP/ skills/ pipeline/ operations/ docs/ knowledge/ vault/ infra/
git commit -m "Plan 01 Task 3: per-bucket subfolder hierarchy"
```

Expected: many files (`.gitkeep` × ~30), one commit.

---

## Phase C — Root governance files

### Task 4: Write root README.md, STATUS.md, CHECKPOINT.md, .gitattributes

**Files:**
- Modify: `README.md` (already exists from initial scaffold; replace with brand-locked version)
- Create: `STATUS.md`, `CHECKPOINT.md`, `.gitattributes`, `.env.example`, `docker-compose.yml` (placeholder)

- [ ] **Step 1: Rewrite root README.md with brand identity**

Write the file `README.md` with content:

```markdown
# Nexostrat

AI consulting for small and medium businesses ("PyMEs") in Mexico, Colombia, and Latin America. We diagnose where AI fits, design solutions, implement them, and operate them ongoing — modular, in plain language, results-driven.

**Founders:** Ricardo Mejía Caicedo · Juan Pablo Mejía
**Status:** Pre-launch. Founding spec ratified 2026-05-13. Scaffolding in progress (Plan 01).
**Stack:** see [`docs/reference/stack_inventory.md`](docs/reference/stack_inventory.md) (auto-generated).

## Where to start

If you're a new operator or future Claude session:
1. Read [`00_META/proposals/2026-05-13_nexostrat-system-design.md`](00_META/proposals/2026-05-13_nexostrat-system-design.md) — the founding spec, source of truth for architecture.
2. Read [`00_META/plans/README.md`](00_META/plans/README.md) — the implementation roadmap.
3. Read [`CLAUDE.md`](CLAUDE.md) (root persona) for how to operate at this scope.
4. Read [`CHECKPOINT.md`](CHECKPOINT.md) for where the last session left off.

JP: read [`README-explicado.md`](README-explicado.md) for the plain version.

## Folder map (one-line summary)

| Folder | What |
|---|---|
| `00_META/` | System governance (changelog, proposals, journal, handoff, inbox, shared stanzas) |
| `00_GOVERNANCE/` | Decisions ledger (ADRs), system map, protocols |
| `00_PARTNERSHIP/` | Ricardo + JP co-owned (agreement, conflict protocol, KPIs, meetings) |
| `docs/` | User manual (Diátaxis: tutorials, how-to, reference, explanation, runbooks) |
| `infra/` | Code we build (Python agents, Telegram bot, hooks, machine profiles, recovery) |
| `vault/` | Encrypted catastrophic-loss material (age-encrypted) |
| `knowledge/` | Graduated reference (sector files, Quick Win library, source caches) |
| `skills/` | The 5+1 reusable skills (Skills-Master persona) |
| `pipeline/` | Active client work (Client-Owner persona) |
| `operations/` | Firm back office (marketing, sales, accounting, legal, IT) |

## License

Internal. All rights reserved.

---

*Nexostrat · `contacto@nexostrat.com`*
```

- [ ] **Step 2: Write STATUS.md**

Write `STATUS.md`:

```markdown
# Nexostrat — STATUS

> **Last updated:** 2026-05-13
> **Current phase:** Plan 01 in flight (Repository Foundation scaffolding)

## Current state

The founding spec has been ratified (2026-05-13). The 10-plan implementation roadmap is locked at `00_META/plans/README.md`. Plan 01 (Repository Foundation) is the active execution.

## Blockers

None.

## Next milestone

Plan 01 complete (tagged `v0.1-foundation`) → start Plan 02 (Documentation System).

## Recent activity

- **2026-05-13** — Founding spec written, self-reviewed, committed (commit `493d0b4`). 10-plan master index written. Plan 01 drafted in full detail.

## Pending JP input

- JP brand top-5 vote (task t-006, due 2026-05-14) — Nexostrat already Ricardo's pick at 8/10; JP confirms.
- JP age public key (for vault encryption to both keys; deferred until JP picks Heavy mode).
- JP attendance for Founding Meeting (Plan Maestro Paso 1) before scaffold of partnership docs is finalized.

## Open follow-ups

- Pilot clients identified: Alfa Bitcoin (JP's company, Spain, first), Sherleg (Colombia), Minca (Colombia/Mexico), Bodai (permanent benchmark, Colombia).
```

- [ ] **Step 3: Write CHECKPOINT.md (Founder persona)**

Write `CHECKPOINT.md`:

```markdown
# CHECKPOINT — root (Founder)

**Updated:** 2026-05-13T20:30:00-07:00
**By:** ricardo (via initial scaffold session)
**Persona:** Founder

## What I just did

- Ratified the founding spec (2026-05-13).
- Committed master plan index + Plan 01 detail.
- Started Plan 01 execution (Repository Foundation).

## In flight — concrete next action

Continue executing Plan 01 starting at Task 4 Step 4 (`.env.example` write) and onward.
Full plan at `00_META/plans/2026-05-13_plan-01-repository-foundation.md`.

## Blocked on

Nothing.

## Open questions

- JP's age public key — when does he generate one? (Deferred to JP Heavy-mode onboarding.)
- Warm-standby laptop hostname — Ricardo needs to confirm at Task 24.

## Files modified but not yet committed

(Updated dynamically as Plan 01 progresses.)

## Estimated time to finish

Plan 01: ~1 week from start. Currently at Task 4 of ~40.

## After this, what's next

Plan 02 (Documentation System), ~3 days.
```

- [ ] **Step 4: Write .gitattributes for LFS rules**

Write `.gitattributes`:

```
# Audio files via LFS (heavy assets)
*.m4a filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text

# Large binary assets via LFS
*.docx filter=lfs diff=lfs merge=lfs -text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text

# Age ciphertexts are binary too
*.age filter=lfs diff=lfs merge=lfs -text

# Markdown gets line-ending normalization
*.md text eol=lf
*.py text eol=lf
*.sh text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.json text eol=lf

# Linguist hints (so GitHub doesn't think the repo is mostly markdown)
*.md linguist-documentation
```

- [ ] **Step 5: Write .env.example placeholder**

Write `.env.example`:

```
# Nexostrat — environment variables template
# Real values live in secrets.env.age (encrypted; decrypt via infra/scripts/run-with-secrets.sh)
# This file is for reference only — DO NOT put real secrets here.

# AI provider keys
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
XAI_API_KEY=

# Self-hosted service keys
GITEA_TOKEN=
TELEGRAM_BOT_TOKEN=
NOTION_API_KEY=

# OAuth refresh tokens
DRIVE_OAUTH_REFRESH_TOKEN=

# GitHub (for mirror push)
GITHUB_PAT=
GITHUB_USERNAME=
GITHUB_REPO=

# Hard caps (enforced via wrapper or provider dashboard)
ANTHROPIC_MONTHLY_CAP_USD=500
```

- [ ] **Step 6: Write minimal docker-compose.yml placeholder**

Write `docker-compose.yml`:

```yaml
# Nexostrat — Docker Compose stack
# Services are added in subsequent plans:
#   Plan 03: event-router daemon
#   Plan 04: nexostrat-bot (Telegram)
#   Plan 08: jitsi-*, nextcloud, whisper-cpp, mcp-* services
#
# Gitea is already running outside this file (managed by HP server's existing docker-compose
# at /home/ricardo/n8n/ — see /home/ricardo/brain/10_INFRA/02_Compute/01_Servers/ricardo-hp-server.md).
# Cal.com (Stage 2) added when scheduling needs justify it.

version: '3.8'

x-restart-policy: &restart-policy
  restart: unless-stopped

services:
  # Services land here in later plans.
  # Empty for now (Plan 01 doesn't add any).
```

- [ ] **Step 7: Stage and commit**

```bash
git add README.md STATUS.md CHECKPOINT.md .gitattributes .env.example docker-compose.yml
git commit -m "Plan 01 Task 4: root governance files (README, STATUS, CHECKPOINT, .gitattributes, .env.example, docker-compose placeholder)"
```

Expected: 1 commit, 6 files (1 modified, 5 created — note: README.md was already in the repo; it gets rewritten).

---

### Task 5: Initialize tasks.json and verify events.json

**Files:**
- Modify: `tasks.json` (reset to Plan 01 work items)
- Modify: `events.json` (verify empty/well-formed)

- [ ] **Step 1: Reset tasks.json for the new phase**

Write `tasks.json`:

```json
{
  "$schema": "brain-tasks-v1",
  "project": "nexostrat",
  "updated": "2026-05-13T20:30:00-07:00",
  "tasks": [
    {
      "id": "t-plan-01",
      "subject": "Execute Plan 01 — Repository Foundation",
      "status": "in_progress",
      "priority": "critical",
      "due": "2026-05-20",
      "created": "2026-05-13",
      "notes": "Plan at 00_META/plans/2026-05-13_plan-01-repository-foundation.md. ~40 tasks. Tag v0.1-foundation on completion."
    },
    {
      "id": "t-jp-brand-vote",
      "subject": "JP vote on top-5 brand HTML (carryover from prior session)",
      "status": "open",
      "priority": "high",
      "due": "2026-05-14",
      "created": "2026-05-12",
      "notes": "Ricardo pick: Nexostrat 8/10, Aurora palette 5/5. JP confirms or amends."
    },
    {
      "id": "t-founding-meeting",
      "subject": "Founding Meeting (Plan Maestro Paso 1) — Ricardo + JP",
      "status": "open",
      "priority": "high",
      "due": "2026-05-20",
      "created": "2026-05-13",
      "notes": "Must happen before partnership docs (Plan 02) are finalized. Both completed questionnaires already in 00_PARTNERSHIP/questionnaires/."
    }
  ]
}
```

- [ ] **Step 2: Verify events.json is well-formed**

Run: `python3 -c "import json; print(json.load(open('events.json')))"`
Expected: a Python dict prints with `events: []`.

If malformed: rewrite as:
```json
{
  "$schema": "brain-events-v1",
  "project": "nexostrat",
  "events": []
}
```

- [ ] **Step 3: Stage and commit**

```bash
git add tasks.json events.json
git commit -m "Plan 01 Task 5: reset tasks.json for foundation phase; verify events.json"
```

---

## Phase D — Identity (age keys)

### Task 6: Detect or generate Ricardo's age keypair

**Files:**
- Create: `~/.age/ricardo.key` (NOT in repo — private key)
- Modify: passphrase memorized + recorded in Ricardo's password manager

- [ ] **Step 1: Detect existing age key on this machine**

Run: `ls -la ~/.age/ 2>/dev/null || echo "NO ~/.age DIR"`

If a private key already exists (e.g., from personal Brain usage):
- Decide: reuse it for Nexostrat, or generate a separate one?
- **Recommendation:** generate a separate keypair for Nexostrat. Different scope, different blast radius if compromised. Ricardo's personal Brain key stays with personal Brain.

- [ ] **Step 2: Generate Nexostrat keypair**

Run:
```bash
mkdir -p ~/.age
age-keygen -o ~/.age/nexostrat-ricardo.key
chmod 600 ~/.age/nexostrat-ricardo.key
```

Expected output: the public key printed to stdout (also stored in the keyfile header).

The key file now contains:
- A header line: `# created: 2026-05-13T...`
- A public-key line: `# public key: age1...`
- The private key (binary-ish, the last line starting with `AGE-SECRET-KEY-1...`)

- [ ] **Step 3: Add a passphrase to the key file (optional but strongly recommended)**

The default `age-keygen` output is unencrypted. To protect against a stolen key file, re-encrypt:

```bash
age-keygen -y ~/.age/nexostrat-ricardo.key > /tmp/nexostrat-pubkey.txt
# Verify pubkey before re-encrypting
cat /tmp/nexostrat-pubkey.txt
```

**DECISION POINT — Ricardo:** at this step, you choose whether to passphrase-protect the key (recommended) or leave it unencrypted (faster but riskier if laptop stolen). The spec recommends passphrase.

If passphrase chosen:
```bash
# Use a strong passphrase from Bitwarden; save the passphrase to Bitwarden under "Nexostrat age key"
age -p -o ~/.age/nexostrat-ricardo.key.age ~/.age/nexostrat-ricardo.key
# Replace the unencrypted file
mv ~/.age/nexostrat-ricardo.key.age ~/.age/nexostrat-ricardo.key
# Now this file is itself age-encrypted with a passphrase
```

For subsequent use, `age -d -i ~/.age/nexostrat-ricardo.key <file>` will prompt for the passphrase.

- [ ] **Step 4: Capture the public key**

If you didn't capture it in Step 3:
```bash
cat /tmp/nexostrat-pubkey.txt
```
The line starting with `age1...` is your public key. You'll add it to `infra/age-recipients.txt` in the next task.

- [ ] **Step 5: Record in MANIFEST**

Add to a personal scratchpad (not committed): the passphrase location (e.g., "Bitwarden, item 'Nexostrat age key'"). This is recovery info — if you forget the passphrase, the vault is unrecoverable.

---

### Task 7: Write infra/age-recipients.txt

**Files:**
- Create: `infra/age-recipients.txt`

- [ ] **Step 1: Capture Ricardo's pubkey to the file**

Write `infra/age-recipients.txt`:

```
# Nexostrat age recipients — public keys of authorized vault readers
# Files in vault/ and secrets.env.age are encrypted to ALL recipients listed here.
# Adding or removing a recipient requires re-encrypting the vault (see docs/runbooks/key_rotation_routine.md).
#
# Lines starting with # are comments.
# Format: one age public key per line.

# Ricardo Mejía Caicedo · nexostrat-ricardo · added 2026-05-13
age1[PASTE YOUR PUBLIC KEY HERE — the line starting with age1 from Task 6 Step 4]

# Juan Pablo Mejía · nexostrat-jp · pending (deferred until JP Heavy-mode onboarding)
# When JP generates his key, add it here via PR + Ricardo approval, then re-encrypt vault.
```

**Replace `[PASTE YOUR PUBLIC KEY HERE — ...]`** with the actual key from Task 6 (e.g., `age1abcdef...`).

- [ ] **Step 2: Verify file format**

Run: `grep -v '^#' infra/age-recipients.txt | grep -v '^$' | wc -l`
Expected: `1` (one recipient line, Ricardo's pubkey, until JP's added).

- [ ] **Step 3: Test that the file is valid age recipients input**

Run:
```bash
echo "test plaintext" | age -R infra/age-recipients.txt | age -d -i ~/.age/nexostrat-ricardo.key
```
Expected: `test plaintext` printed back. Round-trip works.

If it fails: the public key format is wrong; re-extract via `age-keygen -y ~/.age/nexostrat-ricardo.key` and re-paste.

- [ ] **Step 4: Stage and commit**

```bash
git add infra/age-recipients.txt
git commit -m "Plan 01 Task 7: add Ricardo's age public key to infra/age-recipients.txt"
```

---

### Task 8: Build vault structure + sensitive_index.md

**Files:**
- Create: `vault/README.md`, `vault/sensitive_index.md`
- Modify: `vault/.encrypted/.gitkeep` already exists

- [ ] **Step 1: Write vault/README.md**

```markdown
# Vault — encrypted catastrophic-loss store

> **Status:** Active. Encrypted to all recipients in [`../infra/age-recipients.txt`](../infra/age-recipients.txt).
> **Currently encrypted to:** Ricardo only (JP key pending Heavy-mode onboarding).

## What lives here

Only files where loss or exposure would be catastrophic:
- Signed contracts (client, partnership, NDA)
- Tax filings, entity formation docs (when constituted)
- Bank statements
- 2FA recovery codes
- Identity documents (passports, IDs) — when relevant
- Key rotation log (sensitive operational history)

## What does NOT live here

- Routine sensitive operational files (invoices, NDAs in flight) — these go age-encrypted in their function folder per spec §3.2.
- Anything that can be regenerated (transcripts, drafts).

## How to use

**Read a file:**
```bash
age -d -i ~/.age/nexostrat-ricardo.key vault/<path>.age > /dev/shm/temp.<ext>
# use it
shred -u /dev/shm/temp.<ext>
```

**Write a file:**
```bash
age -R infra/age-recipients.txt input.pdf > vault/<path>.pdf.age
rm input.pdf  # original gone; only ciphertext committed
git add vault/<path>.pdf.age sensitive_index.md
git commit -m "vault: add <description>"
```

## Discipline

- NO persistent plaintext mount (unlike Ricardo's personal Brain).
- Decrypt to `/dev/shm` (RAM tmpfs), use, shred.
- Update [`sensitive_index.md`](sensitive_index.md) every time you add or remove a file.
- Quarterly audit: index entries reconciled against actual `.encrypted/` contents.

See [`docs/explanation/why_no_persistent_mount.md`](../docs/explanation/why_no_persistent_mount.md) for the full rationale (written in Plan 02).
```

- [ ] **Step 2: Write vault/sensitive_index.md**

```markdown
# Vault — sensitive index

> Plaintext catalog of what lives in the encrypted vault.
> Updated every time a file is added, removed, or rotated.
> Reconciled quarterly against actual `.encrypted/` contents.

## Index

| Date added | Path | What it is | Why it's here | Owner |
|---|---|---|---|---|
| (no entries yet — vault is freshly provisioned) |||||

## Quarterly audit log

| Date | Auditor | Findings | Actions |
|---|---|---|---|
| (no audits yet) ||||
```

- [ ] **Step 3: Test the vault by encrypting and decrypting a sample file**

```bash
echo "vault test — Plan 01 Task 8 — $(date)" > /tmp/vault-test.txt
age -R infra/age-recipients.txt /tmp/vault-test.txt > vault/.encrypted/test.txt.age
age -d -i ~/.age/nexostrat-ricardo.key vault/.encrypted/test.txt.age
```

Expected: the test message prints back.

- [ ] **Step 4: Clean up the test**

```bash
rm /tmp/vault-test.txt vault/.encrypted/test.txt.age
```

- [ ] **Step 5: Stage and commit**

```bash
git add vault/README.md vault/sensitive_index.md
git commit -m "Plan 01 Task 8: provision vault structure (README + sensitive_index)"
```

---

## Phase E — Secrets workflow

### Task 9: Create secrets.env.age + MANIFEST.md

**Files:**
- Create: `secrets.env.age` (encrypted)
- Create: `infra/secrets/MANIFEST.md`
- Use temporarily: `/dev/shm/secrets.env` (NOT committed)

- [ ] **Step 1: Write the plaintext template to /dev/shm (NEVER to disk in repo)**

```bash
cat > /dev/shm/secrets.env <<'EOF'
# Nexostrat secrets — DO NOT COMMIT PLAINTEXT.
# This file lives encrypted at /srv/Nexostrat/secrets.env.age.
# It is decrypted to /dev/shm at runtime by infra/scripts/run-with-secrets.sh.

# === AI providers ===
ANTHROPIC_API_KEY=sk-ant-PLACEHOLDER
GEMINI_API_KEY=PLACEHOLDER
XAI_API_KEY=xai-PLACEHOLDER

# === Self-hosted ===
GITEA_TOKEN=PLACEHOLDER
TELEGRAM_BOT_TOKEN=PLACEHOLDER
NOTION_API_KEY=PLACEHOLDER

# === Cloud ===
DRIVE_OAUTH_REFRESH_TOKEN=PLACEHOLDER
GITHUB_PAT=PLACEHOLDER
GITHUB_USERNAME=PLACEHOLDER
GITHUB_REPO=nexostrat

# === Budget caps (enforced by wrapper) ===
ANTHROPIC_MONTHLY_CAP_USD=500
EOF
chmod 600 /dev/shm/secrets.env
```

Verify: `head -5 /dev/shm/secrets.env`

- [ ] **Step 2: Encrypt to secrets.env.age**

```bash
age -R infra/age-recipients.txt /dev/shm/secrets.env > secrets.env.age
```

- [ ] **Step 3: Shred the plaintext from /dev/shm**

```bash
shred -u /dev/shm/secrets.env
```

Verify gone: `ls /dev/shm/secrets.env 2>&1` — expect `No such file or directory`.

- [ ] **Step 4: Test round-trip decryption**

```bash
age -d -i ~/.age/nexostrat-ricardo.key secrets.env.age | head -5
```
Expected: the first 5 lines of the template print.

- [ ] **Step 5: Write infra/secrets/MANIFEST.md**

```markdown
# Nexostrat secrets — MANIFEST

> Plaintext index of secrets. NO VALUES — only metadata. Real values live in `../../secrets.env.age` (encrypted).

| Secret | Used by | Rotate at | Last rotated | Hard cap |
|---|---|---|---|---|
| ANTHROPIC_API_KEY | judge agent, /ask, all Mode B skill calls | console.anthropic.com/keys | (set this with first real value) | $500/mo |
| GEMINI_API_KEY | Mode B parallel research (Gemini model) | aistudio.google.com/apikey | (set) | unbounded; cost monitored |
| XAI_API_KEY | Mode B parallel research (Grok model) | console.x.ai | (set) | unbounded; cost monitored |
| GITEA_TOKEN | post-receive hooks, CI access | gitea.local/user/settings/applications | (set) | — |
| TELEGRAM_BOT_TOKEN | nexostrat-bot | @BotFather chat | (set on bot creation) | — |
| NOTION_API_KEY | meeting agent (Notion AI polling) | notion.so/my-integrations | (set when client meetings start) | — |
| DRIVE_OAUTH_REFRESH_TOKEN | rclone heavy-asset sync | `rclone config reconnect gdrive` | (set on first OAuth flow) | — |
| GITHUB_PAT | post-receive hook for GitHub mirror | github.com/settings/tokens | (set with mirror provision, Task 19) | — |
| GITHUB_USERNAME | GitHub mirror target | — (constant) | — | — |
| GITHUB_REPO | GitHub mirror target repo | — (constant) | — | — |

## Rotation procedure

See [`docs/runbooks/secret_leak.md`](../../docs/runbooks/secret_leak.md) and [`docs/how-to/16_add_a_new_secret.md`](../../docs/how-to/16_add_a_new_secret.md) (written in Plan 02 and 03).

In short:
1. Generate new value at the provider.
2. Edit secrets via `infra/scripts/edit-secrets.sh` (decrypts → vim → re-encrypts; never plaintext on disk).
3. Commit the new `secrets.env.age` and update this MANIFEST's "Last rotated" column.
4. Restart any service that holds the old key in memory.
```

- [ ] **Step 6: Stage and commit**

```bash
git add secrets.env.age infra/secrets/MANIFEST.md
git commit -m "Plan 01 Task 9: provision secrets.env.age (placeholders) + MANIFEST.md"
```

---

### Task 10: Write run-with-secrets.sh wrapper

**Files:**
- Create: `infra/scripts/run-with-secrets.sh`

- [ ] **Step 1: Write the wrapper**

```bash
#!/usr/bin/env bash
# Nexostrat — run a command with secrets injected as env vars.
# Secrets live encrypted at /srv/Nexostrat/secrets.env.age.
# Decrypted to /dev/shm (RAM only), sourced, then shredded.

set -euo pipefail

NEXOSTRAT_ROOT="${NEXOSTRAT_ROOT:-/srv/Nexostrat}"
SECRETS_FILE="$NEXOSTRAT_ROOT/secrets.env.age"
AGE_KEY="${AGE_KEY:-$HOME/.age/nexostrat-ricardo.key}"
SHM_FILE="/dev/shm/nexostrat-secrets-$$.env"

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <command> [args...]" >&2
    echo "Example: $0 docker compose up -d" >&2
    exit 1
fi

if [ ! -f "$SECRETS_FILE" ]; then
    echo "ERROR: $SECRETS_FILE not found" >&2
    exit 1
fi

if [ ! -f "$AGE_KEY" ]; then
    echo "ERROR: $AGE_KEY not found" >&2
    echo "Set AGE_KEY env var if your key is elsewhere." >&2
    exit 1
fi

# Cleanup on exit (including on error)
cleanup() {
    if [ -f "$SHM_FILE" ]; then
        shred -u "$SHM_FILE" 2>/dev/null || rm -f "$SHM_FILE"
    fi
}
trap cleanup EXIT INT TERM

# Decrypt to /dev/shm
umask 077  # tight perms on the tmpfile
age -d -i "$AGE_KEY" "$SECRETS_FILE" > "$SHM_FILE"
chmod 600 "$SHM_FILE"

# Source env and exec
set -a  # auto-export sourced vars
# shellcheck disable=SC1090
source "$SHM_FILE"
set +a

# Exec the command (does not return; cleanup trap fires after)
exec "$@"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x infra/scripts/run-with-secrets.sh
```

- [ ] **Step 3: Test with `env` to verify secrets land in environment**

```bash
infra/scripts/run-with-secrets.sh env | grep -E "ANTHROPIC_API_KEY|GEMINI_API_KEY|XAI_API_KEY"
```

Expected: three lines like `ANTHROPIC_API_KEY=sk-ant-PLACEHOLDER`. (The placeholder is fine for the test; real values come later.)

- [ ] **Step 4: Verify /dev/shm cleanup**

After the test above, run: `ls /dev/shm/nexostrat-secrets-*.env 2>&1`
Expected: `No such file or directory`. The trap fired correctly.

- [ ] **Step 5: Test cleanup-on-error**

```bash
infra/scripts/run-with-secrets.sh sh -c 'echo $ANTHROPIC_API_KEY; exit 1' || true
ls /dev/shm/nexostrat-secrets-*.env 2>&1
```
Expected: command exits 1 but no tmpfile lingers. `No such file or directory` again.

- [ ] **Step 6: Stage and commit**

```bash
git add infra/scripts/run-with-secrets.sh
git commit -m "Plan 01 Task 10: run-with-secrets.sh wrapper (decrypts to /dev/shm, shreds on exit)"
```

---

## Phase F — GitHub mirror

### Task 11: Provision GitHub private repo

**DECISION POINT — Ricardo:** GitHub username and repo name.
Recommended: username = your GitHub identity (e.g., `ricardomejiacaicedo`), repo name = `nexostrat`.

- [ ] **Step 1: Create the GitHub repo (manual, via web)**

In your browser, log in to GitHub. Create a NEW PRIVATE repository:
- Name: `nexostrat`
- Visibility: **Private**
- Initialize with: **nothing** (no README, no .gitignore, no LICENSE — we already have content)
- Click "Create repository"

- [ ] **Step 2: Generate a Personal Access Token for mirror pushes**

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token:
- Token name: `nexostrat-mirror-push`
- Expiration: 90 days (we rotate per MANIFEST)
- Repository access: Only select repositories → `nexostrat`
- Permissions:
  - Contents: Read and write
  - Metadata: Read-only

Copy the token (shown only once).

- [ ] **Step 3: Add token + username + repo to secrets**

Use the (to-be-written) edit-secrets script, OR for now manually:

```bash
# Decrypt secrets to /dev/shm
age -d -i ~/.age/nexostrat-ricardo.key secrets.env.age > /dev/shm/secrets-edit.env
chmod 600 /dev/shm/secrets-edit.env

# Edit (replace placeholders for GITHUB_PAT, GITHUB_USERNAME, GITHUB_REPO)
${EDITOR:-vim} /dev/shm/secrets-edit.env

# Re-encrypt
age -R infra/age-recipients.txt /dev/shm/secrets-edit.env > secrets.env.age

# Shred
shred -u /dev/shm/secrets-edit.env
```

- [ ] **Step 4: Update MANIFEST "Last rotated" column for the GITHUB_PAT row**

Edit `infra/secrets/MANIFEST.md`, set the GITHUB_PAT "Last rotated" cell to today's date.

- [ ] **Step 5: Stage and commit (secrets.env.age + MANIFEST changes only)**

```bash
git add secrets.env.age infra/secrets/MANIFEST.md
git commit -m "Plan 01 Task 11: set GitHub PAT + username + repo in secrets"
```

---

### Task 12: Add GitHub remote + initial push

**Files:**
- Modify: `.git/config` (add second remote — this is git internals, not a tracked file)

- [ ] **Step 1: Source secrets via the wrapper for this session**

```bash
eval "$(infra/scripts/run-with-secrets.sh env | grep -E '^(GITHUB_)' | sed 's/^/export /')"
echo "Username: $GITHUB_USERNAME · Repo: $GITHUB_REPO"
```

Expected: prints your GitHub username and `nexostrat`.

- [ ] **Step 2: Add the mirror remote**

```bash
git remote add github "https://${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git"
```

Note: the PAT is embedded in the remote URL. This is the standard way to authenticate; the URL with PAT is stored ONLY in `.git/config` on this machine (not committed). For warm-standby, the standby machine has its own `.git/config` and would have its own remote with its own credentials.

- [ ] **Step 3: Verify the remote is configured**

Run: `git remote -v`
Expected: two remotes listed — `origin` (Gitea) and `github` (GitHub), each with fetch + push.

- [ ] **Step 4: Initial push to GitHub mirror**

```bash
git push github main
```

Expected: pushes all current commits (~5 commits including spec + Plan 01 progress). Auth via the PAT.

- [ ] **Step 5: Verify on GitHub**

Open in browser: `https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}`
Expected: see the commits, README rendered, file tree visible.

---

### Task 13: Configure Gitea post-receive hook to auto-mirror

**Files:**
- Create: `infra/gitea/post-receive-mirror.sh` (the hook script, for documentation)
- Install: corresponding hook inside Gitea's data directory (`/srv/gitea/data/git/repositories/...`)

- [ ] **Step 1: Write the hook script (for docs + version control)**

```bash
#!/usr/bin/env bash
# Nexostrat — Gitea post-receive hook to mirror to GitHub on every push.
# This is the documented version of the hook. The active hook lives inside Gitea's
# internal storage (see install instructions below).

set -euo pipefail

# Hook receives lines on stdin: <old> <new> <ref>
# We don't need to filter — any push triggers a mirror.

# Path to Nexostrat working tree (used to source secrets)
NEXOSTRAT_ROOT="/srv/Nexostrat"

# Source secrets (decrypt + export)
source <(${NEXOSTRAT_ROOT}/infra/scripts/run-with-secrets.sh env | grep -E '^(GITHUB_)' | sed 's/^/export /')

# Mirror push
git push --mirror "https://${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git" \
    || echo "WARN: GitHub mirror push failed (mirror still up-to-date on next successful push)"

# Emit event
echo "$(date -Iseconds)|hook|post-receive|github-mirror-pushed" >> "${NEXOSTRAT_ROOT}/infra/events/events.jsonl"
```

(Note: `events.jsonl` doesn't exist yet — it gets created in Plan 03. The hook will silently fail-soft until then; the `|| echo WARN` already handles this.)

- [ ] **Step 2: Install the hook inside Gitea's repo storage**

Find Gitea's repo storage path:
```bash
docker exec gitea ls /data/git/repositories/ 2>/dev/null || ls /srv/gitea/data/git/repositories/
```
Expected: directories per owner; find the Nexostrat one (e.g., `RicardoMejiaCaicedo/nexostrat.git/` or similar).

**DECISION POINT — Ricardo:** confirm the exact path under Gitea's storage.

Once found (substitute the real path):
```bash
GITEA_REPO_PATH="/srv/gitea/data/git/repositories/<owner>/<repo>.git"
sudo cp infra/gitea/post-receive-mirror.sh "$GITEA_REPO_PATH/hooks/post-receive"
sudo chmod +x "$GITEA_REPO_PATH/hooks/post-receive"
sudo chown -R 1000:1000 "$GITEA_REPO_PATH/hooks/"
```
(Gitea container runs as uid/gid 1000.)

- [ ] **Step 3: Make sure the hook script has execute perms on the host copy too**

```bash
chmod +x infra/gitea/post-receive-mirror.sh
```

- [ ] **Step 4: Test the hook by making a no-op commit and pushing**

```bash
# Trivial change
echo "" >> 00_META/CHANGELOG.md
git add 00_META/CHANGELOG.md
git commit -m "Plan 01 Task 13: test post-receive hook with no-op commit"
git push origin main
```

Expected: push succeeds. Check GitHub immediately:
```bash
gh api repos/${GITHUB_USERNAME}/${GITHUB_REPO}/commits/main --jq '.sha'
```
Expected: the SHA matches `git rev-parse HEAD` locally. (If `gh` CLI not installed, check via browser.)

- [ ] **Step 5: Stage and commit (the hook script)**

```bash
git add infra/gitea/post-receive-mirror.sh
git commit -m "Plan 01 Task 13: post-receive hook script (mirror to GitHub on every push)"
git push origin main
```

Verify the hook fired again: GitHub `main` SHA should match local.

---

## Phase G — Warm-standby provisioning

### Task 14: Document warm-standby host choice

**DECISION POINT — Ricardo:** which laptop becomes the standby? Likely options:
- Ricardo travel laptop (smaller, Tailscale-ready)
- A spare laptop you have

You need: a machine that's reachable via Tailscale, has Docker (or can install it), can host the rsync target.

**Files:**
- Create: `00_GOVERNANCE/system_map.md` (or update it) noting standby choice
- Modify: `infra/machines/hp-standby.yaml` (later in Task 27)

- [ ] **Step 1: Document the choice**

Append to `00_META/CHANGELOG.md`:

```markdown
| 2026-05-13 | Ricardo | Warm-standby host decision: **<HOSTNAME>** (Tailscale IP: <IP>). Documented in `00_GOVERNANCE/system_map.md`. |
```
Replace `<HOSTNAME>` and `<IP>` with real values at execution time.

- [ ] **Step 2: Write/update 00_GOVERNANCE/system_map.md**

```markdown
# Nexostrat — System Map

> Live record of which machine plays which role.

## Roles

| Role | Hostname | Tailscale IP | OS | Notes |
|---|---|---|---|---|
| HP server (live) | `ricardo-hp-laptop` | `100.64.121.80` | Linux Mint 22.2 | Always-on; hosts Gitea, n8n (AttenBot), Docker stack |
| Warm-standby | `<HOSTNAME>` | `<IP>` | (specify) | Idle docker-compose; nightly rsync; manual failover |
| Desktop (GPU) | `ricardo-desktop` | (pending Phase 2 Tailscale install) | Linux Mint 22.3 | RTX 3060 Ti / 8 GB; Ollama; office hours 08-20 |
| Ricardo travel | (TBD) | (TBD) | (TBD) | Git clone + Claude Code + Gemini CLI |
| JP laptop | (TBD) | (TBD when Heavy) | (TBD) | Light mode initially; Heavy when JP chooses |

## Diagram

(ASCII topology diagram from spec §1.3 lives here — to be populated in Plan 02.)

## Last updated

2026-05-13 — Plan 01 Task 14
```

- [ ] **Step 3: Stage and commit**

```bash
git add 00_GOVERNANCE/system_map.md 00_META/CHANGELOG.md
git commit -m "Plan 01 Task 14: document warm-standby host choice; create system_map.md"
git push origin main
```

---

### Task 15: Provision standby — initial rsync + Tailscale + Docker

This task may require running commands on the STANDBY machine, not the HP server. The plan assumes you have SSH access to the standby via Tailscale.

- [ ] **Step 1: Verify SSH reachability to standby**

```bash
ssh <STANDBY_HOST> 'hostname && uname -a'
```
Expected: hostname + kernel info from standby. If SSH not set up: configure SSH key auth before proceeding (`ssh-copy-id <STANDBY_HOST>`).

- [ ] **Step 2: Ensure Docker + git + age + rclone installed on standby**

```bash
ssh <STANDBY_HOST> 'which docker git age rclone || echo MISSING'
```
If anything missing: install via the OS package manager on the standby. (Plan 03's bootstrap script will automate this; for now manual is fine.)

- [ ] **Step 3: Create /srv/Nexostrat/ on standby (matching HP path)**

```bash
ssh <STANDBY_HOST> 'sudo mkdir -p /srv/Nexostrat && sudo chown $(id -u):$(id -g) /srv/Nexostrat'
```

- [ ] **Step 4: Initial git clone on standby**

```bash
ssh <STANDBY_HOST> 'cd /srv && git clone http://100.64.121.80:3001/RicardoMejiaCaicedo/nexostrat.git Nexostrat'
```
(Or the appropriate Gitea repo path — substitute owner / repo if different.)

Expected: clone succeeds. Standby now has its own copy.

- [ ] **Step 5: Initial rsync test (HP → standby, data only)**

From HP server:
```bash
rsync -avz --delete --exclude='.git/' --exclude='vault/.encrypted/' /srv/Nexostrat/ <STANDBY_HOST>:/srv/Nexostrat-rsync-data/
```
This is a one-shot test. The persistent script (Task 16) will run nightly.

Verify on standby: `ssh <STANDBY_HOST> 'ls /srv/Nexostrat-rsync-data/'` — should show the same top-level structure as HP.

- [ ] **Step 6: Cleanup the rsync test target**

```bash
ssh <STANDBY_HOST> 'rm -rf /srv/Nexostrat-rsync-data/'
```

---

### Task 16: Write warm-standby-rsync.sh + nightly cron

**Files:**
- Create: `infra/scripts/warm-standby-rsync.sh`
- Create: `infra/systemd/nexostrat-warm-rsync.service` + `.timer`

- [ ] **Step 1: Write the rsync script**

```bash
#!/usr/bin/env bash
# Nexostrat — nightly rsync to warm-standby host.
# Runs via systemd timer at 03:00.

set -euo pipefail

NEXOSTRAT_ROOT="${NEXOSTRAT_ROOT:-/srv/Nexostrat}"
STANDBY_HOST="${STANDBY_HOST:-CHANGE_ME}"
STANDBY_PATH="${STANDBY_PATH:-/srv/Nexostrat}"
LOG_FILE="/var/log/nexostrat/warm-standby-rsync.log"

mkdir -p "$(dirname "$LOG_FILE")"

if [ "$STANDBY_HOST" = "CHANGE_ME" ]; then
    echo "$(date -Iseconds) ERROR STANDBY_HOST not configured" >> "$LOG_FILE"
    exit 1
fi

echo "$(date -Iseconds) START rsync $NEXOSTRAT_ROOT/ -> $STANDBY_HOST:$STANDBY_PATH/" >> "$LOG_FILE"

# Sync everything EXCEPT .git (standby has its own .git from clone)
# and EXCEPT vault/.encrypted (it's already in git, no need to rsync separately)
rsync -avz --delete \
    --exclude='.git/' \
    --exclude='*.swp' \
    --exclude='.DS_Store' \
    "$NEXOSTRAT_ROOT/" \
    "$STANDBY_HOST:$STANDBY_PATH/" \
    >> "$LOG_FILE" 2>&1

RC=$?
echo "$(date -Iseconds) END rc=$RC" >> "$LOG_FILE"

# Emit event if events.jsonl exists (will be created in Plan 03)
if [ -f "$NEXOSTRAT_ROOT/infra/events/events.jsonl" ]; then
    echo "{\"ts\":\"$(date -Iseconds)\",\"actor\":\"system\",\"type\":\"warm_standby.rsync_completed\",\"data\":{\"rc\":$RC,\"host\":\"$STANDBY_HOST\"}}" \
        >> "$NEXOSTRAT_ROOT/infra/events/events.jsonl"
fi

exit $RC
```

Make executable: `chmod +x infra/scripts/warm-standby-rsync.sh`

- [ ] **Step 2: Test it manually first (with STANDBY_HOST set)**

```bash
STANDBY_HOST=<STANDBY_HOST> infra/scripts/warm-standby-rsync.sh
```

Expected: rsync runs without error; check `/var/log/nexostrat/warm-standby-rsync.log` for the START/END lines.

If `/var/log/nexostrat/` lacks write perms: `sudo mkdir -p /var/log/nexostrat && sudo chown $(id -u):$(id -g) /var/log/nexostrat`.

- [ ] **Step 3: Write the systemd service unit**

`infra/systemd/nexostrat-warm-rsync.service`:

```ini
[Unit]
Description=Nexostrat warm-standby nightly rsync
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=oneshot
User=ricardo
Environment="STANDBY_HOST=<STANDBY_HOST>"
ExecStart=/srv/Nexostrat/infra/scripts/warm-standby-rsync.sh
StandardOutput=journal
StandardError=journal
```

Replace `<STANDBY_HOST>` with the real value.

- [ ] **Step 4: Write the systemd timer unit**

`infra/systemd/nexostrat-warm-rsync.timer`:

```ini
[Unit]
Description=Nexostrat warm-standby rsync — nightly at 03:00
Requires=nexostrat-warm-rsync.service

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

- [ ] **Step 5: Install the units**

```bash
sudo cp infra/systemd/nexostrat-warm-rsync.service /etc/systemd/system/
sudo cp infra/systemd/nexostrat-warm-rsync.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nexostrat-warm-rsync.timer
sudo systemctl start nexostrat-warm-rsync.timer
```

- [ ] **Step 6: Verify the timer is scheduled**

```bash
systemctl list-timers | grep nexostrat-warm-rsync
```
Expected: next-fire time at 03:00 tomorrow.

- [ ] **Step 7: Optionally trigger the service manually to verify it works under systemd**

```bash
sudo systemctl start nexostrat-warm-rsync.service
journalctl -u nexostrat-warm-rsync.service --since "5 minutes ago"
```
Expected: log lines showing rsync completion.

- [ ] **Step 8: Stage and commit**

```bash
git add infra/scripts/warm-standby-rsync.sh infra/systemd/nexostrat-warm-rsync.{service,timer}
git commit -m "Plan 01 Task 16: warm-standby-rsync.sh + systemd timer (nightly 03:00)"
git push origin main
```

---

## Phase H — Shared stanzas at 00_META/shared/

### Task 17: Write the canonical shared stanzas

**Files:**
- Create: `00_META/shared/{rule1_operator_scope,session_start,session_end,session_output_format,memo_protocol,gemini_handoff,vault_access,backup_policy,checkpoint_pattern}.md`

These are reusable text blocks inlined into each persona's CLAUDE.md. Pattern lifted from Ricardo's personal Brain at `/srv/brain/00_META/shared/`.

- [ ] **Step 1: Write 00_META/shared/rule1_operator_scope.md**

```markdown
<!-- scope-rule-v1 -->

**Folder scope is operator-driven, not strictly isolated.** When Ricardo or JP is in-session driving, any persona may edit any folder to advance the work — no memo trail required for routine in-session work. Memos remain for **(a)** requests to a specialist persona whose domain expertise is genuinely needed, **(b)** deliberate cross-scope paper trails for high-impact decisions, **(c)** autonomous async work the originating persona surfaces but another persona will pick up later. **Vault namespaces stay strictly isolated regardless** — never write to another bucket's vault path.

**Heuristic:** if the cross-bucket edit takes more than a sentence to explain, send a memo; otherwise just make the edit and update the affected scope's `STATUS.md` / journal / `CHECKPOINT.md` as you go.

Full rule + history: see `00_META/proposals/2026-05-13_nexostrat-system-design.md` §4.3.
```

- [ ] **Step 2: Write 00_META/shared/session_start.md**

```markdown
<!-- session-start-v1 -->

Two layers run on every session:

1. **SessionStart hook** (automatic). Runs `git pull` + prints a tiny safety-net summary: OVERDUE tasks, memos addressed to this scope, events due today, high-priority tasks due in next 2 days, plus the current `CHECKPOINT.md` baton. Silent when nothing is pending.

2. **Claude's session-start brief** (triggered by Ricardo writing "Start Session"). On trigger, Claude reads in order:
   - `CHECKPOINT.md` (this persona) — where the last session left off
   - `STATUS.md` — current state and blockers
   - `tasks.json` — open work items
   - `events.json` — upcoming deadlines
   - the most recent file in `00_META/journal/` — last session's narrative
   - `00_META/plans/README.md` — the master plan index (which plan is in flight)
   - the current plan file (if mid-execution)
   
   Then summarizes to Ricardo in the 5-bullet format (see `session_output_format.md`).
   
   Then runs the inbox scanner: `python3 infra/scripts/nexostrat-memos.py --to <scope>` (where `<scope>` is the current persona).
```

- [ ] **Step 3: Write 00_META/shared/session_end.md**

```markdown
<!-- session-end-v1 -->

Session End ritual — triggered by "Prepare for session termination" / "End session" / similar close phrase.

**Step 1 — Claude:**
1. Summary of what was done this session (2-4 sentences).
2. List every file that will be written at session end.
3. List pending tasks / objectives / follow-ups that came out of this session.
4. For each pending item, propose: priority (low / medium / high / critical) and due date (or "open-ended"). Ricardo confirms or amends in a table.

**Step 2 — Ricardo** replies with confirmations, "proceed."

**Step 3 — Claude applies:**
0. Update `CHECKPOINT.md` with required fields (or `CHECKPOINT_NO_ACTIVE_WORK` if closing cleanly).
1. Update `STATUS.md`.
2. Update `tasks.json`.
3. Update `events.json` if any deadlines changed.
4. Write a journal entry: `00_META/journal/YYYY-MM-DD_<topic>.md`.
5. Update `00_META/CHANGELOG.md` if any architectural change was made.
6. If work remains for Gemini, write handoff in `00_META/handoff/claude_to_gemini.md`.
7. `git add` + `git commit` + `git push` (handled by SessionEnd hook automatically on actual close).

**Step 4 — Ricardo** writes "Finish Session."

**Step 5 — Ricardo** closes with Ctrl-C or `/exit`. SessionEnd hook fires: regenerates aggregate status, commits, pushes.
```

- [ ] **Step 4: Write 00_META/shared/session_output_format.md**

```markdown
<!-- session-format-v1 -->

The session-start brief and session-end Step 1 follow a canonical Nexostrat-wide format.

**Session Start — 5-bullet brief.** Up to 5 bullets, bold label + concise content; omit empty bullets (no padding).

Bullet order:
1. **OVERDUE / critical-imminent** — `<scope> <id>` — `<summary>` — `<Nd late | due today | +Nd>`
2. **Pending inbox / handoffs** — count; highest-priority summary with file path
3. **In-progress work** — `<scope> <id>` — `<status>`
4. **Pending verifications / Stage 5 / other** — one line per item
5. **Flag** — anything else (architectural blockers, stale STATUS.md, cross-scope awareness)

End with: *"What would you like to work on?"*

**Session End — Step 1 format:**

1.1 Session summary (2-4 sentences).
1.2 Files written at session end (bulleted list, one path per line, include purpose if non-obvious).
1.3 Pending items table: `| # | Item | Proposed priority | Proposed due | Rationale |`. Then ask Ricardo to confirm/amend.
1.4 Disambiguation questions — only if truly blocking.

**Never invent counts.** If `BRAIN_STATUS.md` / inbox scanner returns empty, say "none" or omit the bullet.
```

- [ ] **Step 5: Write 00_META/shared/memo_protocol.md**

```markdown
<!-- memo-protocol-v1 -->

Cross-folder memos are file-based, written directly into the target's inbox. Three inboxes:

- `00_META/inbox/` (Founder)
- `skills/00_META/inbox/` (Skills-Master)
- `pipeline/00_META/inbox/` (Client-Owner)

**Send a memo:** write `<target>/00_META/inbox/YYYY-MM-DD_<slug>.md` using the template at `00_META/00_TEMPLATES/memo_template.md` (created in Plan 02). Fill YAML frontmatter: `from`, `to`, `type` (action|info|provision|proposal), `priority`, `subject`. Once written, target owns lifecycle.

**Reply to a memo:** do the work, then write the reply into the originator's inbox at `<originator>/00_META/inbox/YYYY-MM-DD_reply_<slug>.md` with `status: REPLY` and `re: <brain-relative-path>`. Move original to your `00_META/inbox/archive/`.

**Session-start scan:** `python3 /srv/Nexostrat/infra/scripts/nexostrat-memos.py --to <scope>`. Surface open memos in the 5-bullet brief.

Under operator-driven scope (`rule1_operator_scope.md`), the Telegram bot can also write to any scope's inbox via `/note <scope> <text>`, treated identically to manual writes.
```

- [ ] **Step 6: Write 00_META/shared/gemini_handoff.md**

```markdown
<!-- gemini-handoff-v1 -->

File-based handoff pattern. Claude raises an `OPEN` handoff via `00_META/handoff/claude_to_gemini.md`. Gemini flips to `IN_PROGRESS`, writes response in `00_META/handoff/gemini_to_claude.md` with `Status: RESPONSE_READY`, flips claude_to_gemini to `RESOLVED`. Claude integrates the response, archives both to `00_META/handoff/archive/YYYY-MM-DD_<slug>.md`.

**When to raise a handoff:**
- Web search / fresh-information lookup (Gemini has live web)
- Adversarial audit of a plan or doc
- Document review on Spanish-language client deliverables
- Alternative brainstorming frame

**Never:** edit `gemini_to_claude.md` directly (Gemini's file). Never commit Gemini's WIP while a handoff is `IN_PROGRESS`.

**Status transitions Claude owns:** `OPEN` (writing), `ARCHIVED` (after integrating).
**Status transitions Gemini owns:** `IN_PROGRESS` (picking up), `RESOLVED` (on handoff file when done), `RESPONSE_READY` (on response file when written).
```

- [ ] **Step 7: Write 00_META/shared/vault_access.md**

```markdown
<!-- vault-access-v1 -->

Encrypted vault at `vault/.encrypted/` using `age` per-user keys. Public keys in `infra/age-recipients.txt`. Private keys never leave individual user laptops.

**Read:**
```
age -d -i ~/.age/nexostrat-<user>.key vault/<path>.age > /dev/shm/temp.<ext>
# use it
shred -u /dev/shm/temp.<ext>
```

**Write:**
```
age -R infra/age-recipients.txt input > vault/<path>.age
rm input  # original gone; only ciphertext committed
git add vault/<path>.age vault/sensitive_index.md
```

**Discipline:**
- NO persistent plaintext mount.
- Update `vault/sensitive_index.md` on every write.
- Heavy assets (audio, large PDFs) encrypted before Drive upload via the same flow.
- Per-bucket vault namespaces (e.g., `vault/clients/<slug>/`) — Founder writes only `vault/partnership/` and `vault/accounting/`; Client-Owner writes only `vault/clients/<slug>/`; etc. **No cross-bucket vault writes regardless of operator-driven scope rule.**
```

- [ ] **Step 8: Write 00_META/shared/backup_policy.md**

```markdown
<!-- backup-policy-v1 -->

7-layer backup ladder:

1. Working tree on HP (continuous)
2. Gitea origin on HP (per commit)
3. GitHub private mirror (per push, via post-receive hook)
4. Codeberg mirror (per push, Phase B)
5. Warm-standby clone (nightly rsync 03:00)
6. Drive 2TB (continuous rclone for heavy assets, age-encrypted)
7. NAS local mirror of Drive (nightly cron 04:00)

**Verification cron** (weekly Sunday 02:00): sample mirrors for hash match; count Drive heavy-assets vs `vault/sensitive_index.md`. Alert via Telegram on any drift.

**Recovery RTOs:**
- HP down: 15-30 min (warm-standby failover via `infra/recovery/hp_down_failover.sh`)
- HP + standby down: 4-8h (restore from GitHub on any spare laptop)

Runbooks at `docs/runbooks/`.
```

- [ ] **Step 9: Write 00_META/shared/checkpoint_pattern.md**

```markdown
<!-- checkpoint-pattern-v1 -->

`CHECKPOINT.md` per persona at the persona root. Required at session end; read first at session start. Closes the "where did we leave off?" gap.

**Required fields:**
- Updated timestamp + by whom
- Persona
- What I just did
- In flight — concrete next action (with file paths and commands)
- Blocked on
- Open questions
- Files modified but not committed
- Estimated time to finish
- After this, what's next

Empty CHECKPOINT.md commits refused unless explicitly written as `CHECKPOINT_NO_ACTIVE_WORK`.

**Per-client checkpoints** (optional, when work is concentrated on one client): `pipeline/clients/<slug>/checkpoint.md` with the same fields. The persona's CHECKPOINT.md points to it.

**SessionStart hook** reads CHECKPOINT.md first and surfaces it in the safety-net summary.

**Mode B (API pipelines)** writes CHECKPOINT.md automatically when a pipeline pauses awaiting review.

**Telegram `/handoff [scope]`** posts the current CHECKPOINT to the group.
```

- [ ] **Step 10: Stage and commit all shared stanzas**

```bash
git add 00_META/shared/
git commit -m "Plan 01 Task 17: canonical shared stanzas (9 files) for persona inlining"
git push origin main
```

---

## Phase I — Persona files

### Task 18: Write root CLAUDE.md (Founder persona)

**Files:**
- Modify: `CLAUDE.md` (already exists from initial scaffold; rewrite as the Founder for Nexostrat)

- [ ] **Step 1: Inspect existing CLAUDE.md to understand what's there**

Run: `head -30 CLAUDE.md`

The existing file is from when this was `04_MejiaIACia`. Most content carries over; we update the brand, the bucket structure, and inline the shared stanzas correctly.

- [ ] **Step 2: Rewrite CLAUDE.md**

Replace the entire file with:

```markdown
# Nexostrat — Claude Context (Founder)

> **Last Updated:** 2026-05-13
> **Scope:** Founder persona — root of `/srv/Nexostrat/`. Operates all governance, operations, prospects, infra, docs, knowledge, and vault. Defers Skills work to the Skills-Master persona at `skills/CLAUDE.md` and per-client work to the Client-Owner persona at `pipeline/CLAUDE.md`.

## Role

You are the Founder of Nexostrat. Operate this scope as the running head of the firm: positioning, partnership, operations (marketing / sales / accounting / legal / IT), prospect tracking, knowledge curation, governance, cross-cutting infra. Ricardo Mejía Caicedo is the human founder + primary operator; you assist with strategy, written deliverables, pricing, sales materials, ongoing operations. Juan Pablo Mejía is co-founder (50/50 equity) acting as strategy + review.

## About Ricardo and JP

Ricardo: Systems Architect, Automation Engineer, Technical Founder. Low native coding ability, high AI reliance. Currently in Tijuana, Mexico. Communication: direct, concise, no fluff, no emojis. Step-by-step interaction (deliver one step, wait for confirmation). Always provide full code blocks, never snippets. Does not hand-edit JSON/code files — AI edits on his behalf.

JP: in another time zone (Bogotá, COT). 10 hrs/week first 6 months, 5 hrs/week after. Main business is JPMC & Co. JP's role: strategy, pricing, review of deliverables. Reads English fine; preferred operating language Spanish for client material.

Operating principles: "Boring but Robust" (stability over cleverness) · "Freeze Before Building" (analyze first) · Complexity Hard Stop (halt if over-engineering) · Human-in-the-loop always (no destructive action without explicit per-action approval).

## Strict Rules

<!-- inlined: 00_META/shared/rule1_operator_scope.md -->
{{include: 00_META/shared/rule1_operator_scope.md}}

Additional rules:
2. You author all `GEMINI.md` files. Gemini may NOT edit any `CLAUDE.md` (reciprocal rule enforced in every `GEMINI.md`).
3. New top-level folders require Founder approval (an ADR). Sub-folders inside a bucket can be added by the owning persona.
4. No destructive operations without explicit per-action approval.
5. Sensitive content goes in the vault. Never plaintext anywhere in the repo outside vault/.encrypted/.
6. Per-bucket vault namespace isolation: Founder writes only `vault/partnership/`, `vault/legal/`, `vault/accounting/`, `vault/keys/`. Never the client namespaces — those belong to Client-Owner.

## Session Start Protocol

<!-- inlined: 00_META/shared/session_start.md -->
{{include: 00_META/shared/session_start.md}}

## Session End Protocol

<!-- inlined: 00_META/shared/session_end.md -->
{{include: 00_META/shared/session_end.md}}

## Session Output Format

<!-- inlined: 00_META/shared/session_output_format.md -->
{{include: 00_META/shared/session_output_format.md}}

## Architecture / Context

Nexostrat is the firm. The repo at `/srv/Nexostrat/` is the firm's brain. 3-bucket layout (`skills/`, `pipeline/`, `operations/`) plus cross-cutting concerns (`00_META/`, `00_GOVERNANCE/`, `00_PARTNERSHIP/`, `docs/`, `infra/`, `vault/`, `knowledge/`). Founding spec at `00_META/proposals/2026-05-13_nexostrat-system-design.md` — read it before making any architectural decision.

Implementation roadmap in 10 plans at `00_META/plans/README.md`. Plan 01 currently in flight.

## Cross-Folder Memo Protocol

<!-- inlined: 00_META/shared/memo_protocol.md -->
{{include: 00_META/shared/memo_protocol.md}}

## Gemini Handoff Protocol

<!-- inlined: 00_META/shared/gemini_handoff.md -->
{{include: 00_META/shared/gemini_handoff.md}}

## Vault Access

<!-- inlined: 00_META/shared/vault_access.md -->
{{include: 00_META/shared/vault_access.md}}

## Backup Posture

<!-- inlined: 00_META/shared/backup_policy.md -->
{{include: 00_META/shared/backup_policy.md}}

## CHECKPOINT pattern

<!-- inlined: 00_META/shared/checkpoint_pattern.md -->
{{include: 00_META/shared/checkpoint_pattern.md}}

## Subagents

Custom subagents may live at `/srv/Nexostrat/.claude/agents/` (project-scope, committed). Currently none provisioned (Plan 01 ships without; Plans 02-10 may add).

When invoking `risk-auditor` (from personal Brain conventions): before any of these ship, call risk-auditor with a brief describing the proposed change, affected files, and rationale:
- A Brain-wide propagator (`infra/scripts/propagate_*.py`) touching ≥5 scopes
- A change to root `.gitignore`, hooks, or any Stop/Session hook dependency
- An edit to Strict Rules
- A new architectural pattern or policy that propagates Nexostrat-wide
- A cross-bucket destructive operation

If audit returns YELLOW, apply amendments before shipping. If RED, stop and revisit.

## Change Log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (root scaffold) | Founder persona created during Plan 01 execution. Replaces the pre-rename `04_MejiaIACia` persona file with the brand-locked Nexostrat version. Inlines shared stanzas from `00_META/shared/`. |
```

**Important:** the `{{include: ...}}` markers are placeholders. In Plan 02, we'll build a generator script that inlines the actual content into the file at commit time (similar to Ricardo's personal Brain's pattern). For Plan 01, leave these markers as-is — they're readable as references.

- [ ] **Step 3: Stage and commit**

```bash
git add CLAUDE.md
git commit -m "Plan 01 Task 18: rewrite root CLAUDE.md as Nexostrat Founder persona"
git push origin main
```

---

### Task 19: Write root GEMINI.md (Founder second-seat)

**Files:**
- Modify: `GEMINI.md` (already exists; rewrite)

- [ ] **Step 1: Rewrite GEMINI.md**

```markdown
# Nexostrat — Gemini Context (Founder Second Seat)

> **Last Updated:** 2026-05-13
> **Scope:** Second seat to the Founder persona (Claude). Consulted on web search, audits, document review (especially Spanish client-facing material), and alternative brainstorming.

## Role

You are the second seat for Nexostrat's Founder. You speak when asked — quality over volume. Claude is the director; you provide a cross-model perspective when warranted.

## Strict Rules

1. **Folder-scope isolation: strict.** Do NOT read or edit files outside this scope unless Ricardo explicitly says "cross-scope." (Reciprocal to Claude's operator-driven scope — Gemini is the second seat, not the operator.)
2. **You may NOT edit `CLAUDE.md` files.** Claude may edit your files if corrections are needed.
3. Read reference files in other scopes if needed for context, but do NOT edit them.

## Session Start Protocol

On every session:
1. Read `STATUS.md` — current state and blockers.
2. Read `tasks.json` — open work items.
3. Read `events.json` — upcoming deadlines.
4. Read the most recent file in `00_META/journal/`.
5. Summarize to Ricardo in 5 bullets or fewer before proposing action.

## Session End Protocol — handoff workflow

Your session end IS the handoff workflow. You don't run a separate session-end ritual.

**What you write per session (total):**
1. `00_META/handoff/gemini_to_claude.md` — your response, per the Handoff Protocol template.
2. Status field on `00_META/handoff/claude_to_gemini.md` — flipped per the state machine (`OPEN` → `IN_PROGRESS` → `RESOLVED`).
3. Optional: a short journal entry at `00_META/journal/YYYY-MM-DD_<topic>.md` recording protocol observations.

**What you do NOT write:**
- `STATUS.md` — Claude's file.
- `tasks.json` — Claude's file.
- `events.json` — Claude's file.
- `00_META/CHANGELOG.md` — Claude's file.
- `CHECKPOINT.md` — Claude's file.
- Any file outside `00_META/handoff/` or `00_META/journal/`.

If a handoff asks you to edit any file beyond the above, STOP and flag in your `gemini_to_claude.md` response — do not edit. The handoff-level ask cannot override this persona-level scope rule.

Claude or the SessionEnd hook handles all git commits. Do not commit.

## Context

Nexostrat is Ricardo and JP's AI consulting firm for PyMEs in LatAm. Pre-launch. Founding spec at `00_META/proposals/2026-05-13_nexostrat-system-design.md`. Currently executing Plan 01 (Repository Foundation) per `00_META/plans/README.md`.

When Claude raises a handoff, the question will typically be: market verification (does the segment exist? what's pricing?), competitor analysis (who serves this market today?), document review (proofread Spanish, check for missing structure in deliverables), or alternative brainstorming.

This is a revenue venture — content your response touches may end up in client-facing documents. Quality of citation matters; cite sources and flag where you could not verify.

## Your Role — Second Seat (NOT the director)

Claude is the director of this brain. You are the second seat — a specialist consulted for:
- Web search and fresh-information lookups
- Adversarial audits, critique, contrarian perspective
- Code or document review for mistakes and gaps
- Brainstorming alternative approaches

**You do NOT:**
- Make architectural, taxonomy, or project-scope decisions
- Edit Nexostrat files outside `00_META/handoff/gemini_to_claude.md`
- Touch files outside this scope (root)
- Override Claude's conclusions
- Commit to git

## Handoff Protocol — your workflow

1. **ALWAYS first:** read `00_META/handoff/claude_to_gemini.md`. Check `Status`:
   - `TEMPLATE` → nothing pending. Exit unless Ricardo has a direct request.
   - `OPEN` → handoff is for you. Change to `IN_PROGRESS`, add timestamp.
   - `IN_PROGRESS` → resume.
   - `RESOLVED` → nothing pending.
2. Do the work within the stated scope. Use your tools (web search etc.) freely within the ask.
3. Write your response to `00_META/handoff/gemini_to_claude.md` using the canonical template:
   - Change `Status` from `TEMPLATE` to `RESPONSE_READY`
   - Fill in: In response to, Completed date, Summary, Findings, Sources / verification, Questions / gaps
4. Change status of `claude_to_gemini.md` from `IN_PROGRESS` to `RESOLVED`.
5. Write a short journal entry in `00_META/journal/YYYY-MM-DD_<topic>.md`.
6. Exit. Do NOT commit. Do NOT touch any other file.

## Strict handoff constraints

- Work only within the stated ask. No scope expansion.
- Flag uncertainty explicitly. "Unknown" / "could not verify" is a valid answer.
- Don't edit `claude_to_gemini.md` except the `Status` field.
- Don't rewrite any file outside `gemini_to_claude.md`.
- Sensitive data (bank statements, IDs, passwords, contracts) should NOT appear in handoffs. If it does, refuse and flag.

**Status transitions Gemini owns:** `IN_PROGRESS` (picking up), `RESOLVED` (on handoff file when done), `RESPONSE_READY` (on response file when written).

## Change Log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (root scaffold) | Founder Gemini second-seat persona created during Plan 01 execution. |
```

- [ ] **Step 2: Stage and commit**

```bash
git add GEMINI.md
git commit -m "Plan 01 Task 19: rewrite root GEMINI.md as Founder second-seat persona"
git push origin main
```

---

### Task 20: Write skills/CLAUDE.md and skills/GEMINI.md (Skills-Master persona)

**Files:**
- Create: `skills/CLAUDE.md`
- Create: `skills/GEMINI.md`
- Create: `skills/CHECKPOINT.md`
- Create: `skills/STATUS.md`

- [ ] **Step 1: Write skills/CLAUDE.md**

Mirror the structure of root CLAUDE.md, but scoped to skills/. Key sections that differ:

```markdown
# Skills — Claude Context (Skills-Master)

> **Last Updated:** 2026-05-13
> **Scope:** Skills-Master persona — the 5+1 reusable skills (`01_company_analyst/`, `02_industry_analyst/`, `03_competitor_analyst/`, `04_meeting_script/`, `05_opportunity_report/`, `06_discovery_meeting/`) plus shared assets at `skills/shared/`. Designs, versions, tests, maintains skill prompts. Owns benchmark cases (Bodai).

## Role

You are the Skills-Master for Nexostrat. Your domain: the methodology library. Each skill is a recipe — prompt + scripts + references + assets + benchmarks. You version-control prompt iterations, run regression tests against the Bodai benchmark fixture, and refine quality. You do NOT operate on specific clients — that's Client-Owner's job at `pipeline/CLAUDE.md`.

## About Ricardo and JP

(Same as root, with this skill-specific addition: JP proposes initial prompt versions; Ricardo reviews and refines. Per Plan Maestro Paso 2.)

## Strict Rules

<!-- inlined: 00_META/shared/rule1_operator_scope.md -->
{{include: 00_META/shared/rule1_operator_scope.md}}

Additional rules:
2. You author all `GEMINI.md` files within this scope.
3. **Skill prompt edits affect production quality** — never edit a prompt without running the Bodai benchmark regression test. If score drops, commit is refused.
4. **Anti-hallucination marker block** (`skills/shared/anti_hallucination.md`) must appear in every skill prompt. Pre-commit hook enforces.
5. Per-skill folder template (`SKILL.md`, `prompts/`, `versions/`, `scripts/`, `references/`, `assets/`, `tests/`) — adding fields requires an ADR.
6. Vault namespace: Skills-Master does not write to vault. Skills don't store sensitive client data; they operate on `research_input.md` content only.

## Session Start Protocol

<!-- inlined: 00_META/shared/session_start.md -->
{{include: 00_META/shared/session_start.md}}

For this scope specifically: also read the SKILL.md of the skill you're working on, plus `STATUS.md` and `prompts/CHANGELOG.md` for that skill.

## Session End Protocol

<!-- inlined: 00_META/shared/session_end.md -->
{{include: 00_META/shared/session_end.md}}

## Session Output Format

<!-- inlined: 00_META/shared/session_output_format.md -->
{{include: 00_META/shared/session_output_format.md}}

## Architecture / Context

Skills are the firm's methodology library. The 5+1 skills implement the diagnostic pipeline:

1. `01_company_analyst/` — already built; produces a 13-section company report (DOCX 15-25 pp)
2. `02_industry_analyst/` — to build in Plan 06
3. `03_competitor_analyst/` — to build in Plan 06
4. `04_meeting_script/` — to build in Plan 06; PRIVATE (never to client)
5. `05_opportunity_report/` — to build in Plan 06; THE Diagnóstico deliverable (DOCX 20-30 pp)
6. `06_discovery_meeting/` — existing; meeting facilitation skill (different category, supports the meeting itself)

Shared resources at `skills/shared/`:
- `judge_prompt.md` — Claude-as-Judge synthesizer template
- `research_input_template.md` — slices 1+2 of intake
- `our_hypotheses_template.md` — slice 3 (sealed)
- `anti_hallucination.md` — marker block inlined into every skill prompt
- `scoring.py` — benchmark scoring formula

Each skill has: `SKILL.md` (Anthropic Skill manifest), `README.md`, `STATUS.md`, `prompts/v1.md` (+ `versions/`), `scripts/`, `references/`, `assets/`, `tests/benchmark.md`.

Multi-model parallel-then-judge architecture (ADR-026): each skill runs in BOTH Mode A (manual, $0) and Mode B (API, ~$0.20-0.40) using the same prompt. Three models (Claude, Gemini, Grok) produce raw outputs; Claude-as-Judge synthesizes.

## Cross-Folder Memo Protocol

<!-- inlined: 00_META/shared/memo_protocol.md -->
{{include: 00_META/shared/memo_protocol.md}}

## Gemini Handoff Protocol

<!-- inlined: 00_META/shared/gemini_handoff.md -->
{{include: 00_META/shared/gemini_handoff.md}}

## Vault Access

<!-- inlined: 00_META/shared/vault_access.md -->
{{include: 00_META/shared/vault_access.md}}

Note: Skills-Master rarely touches the vault. Skills work on non-sensitive intake content (`research_input.md`). If a skill needs to load encrypted reference data (rare — perhaps proprietary sector reports), use the standard rare-access pattern.

## Backup Posture

<!-- inlined: 00_META/shared/backup_policy.md -->
{{include: 00_META/shared/backup_policy.md}}

## CHECKPOINT pattern

<!-- inlined: 00_META/shared/checkpoint_pattern.md -->
{{include: 00_META/shared/checkpoint_pattern.md}}

## Change Log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (root scaffold) | Skills-Master persona created during Plan 01 execution. |
```

- [ ] **Step 2: Write skills/GEMINI.md**

Mirror structure of root GEMINI.md, scoped to skills/. Same strict isolation. Specialist consultation for: skill prompt review, anti-hallucination audits, benchmark expected-output drafting.

(Use root GEMINI.md as template; substitute "Founder" → "Skills-Master" and scope adjustments.)

- [ ] **Step 3: Write skills/CHECKPOINT.md**

```markdown
# CHECKPOINT — skills (Skills-Master)

**Updated:** 2026-05-13T20:30:00-07:00
**By:** ricardo (via Plan 01 scaffold)
**Persona:** Skills-Master

## What I just did

Scaffolded the Skills-Master persona file as part of Plan 01 Task 20.

## In flight — concrete next action

Skills work doesn't start until Plan 05 (Skill 1 end-to-end). When that plan begins, the Skills-Master persona reads:
- `skills/01_company_analyst/SKILL.md` (already extracted to `00_META/skills/company-analyst/`; migrate to canonical location in Plan 05)
- The Bodai benchmark fixture (to be created in Plan 05)
- The judge prompt template (to be created in Plan 05)

## Blocked on

Plan 05 (Skill 1 e2e) execution. Currently waiting for Plans 01-04 to complete.

## Open questions

None at scaffold time.

## Files modified but not yet committed

None.

## Estimated time to finish

N/A (waiting for Plan 05).

## After this, what's next

Plan 05 execution starts when Plans 01-04 are DONE.
```

- [ ] **Step 4: Write skills/STATUS.md**

```markdown
# Skills — STATUS

> **Last updated:** 2026-05-13
> **Current phase:** Pre-skills-work (waiting for Plan 05 start)

## Current state

Skills-Master persona scaffolded. No active skill development yet. Existing skill bundles (extracted in earlier session) sit at `00_META/skills/` and will be migrated to canonical `skills/0N_<name>/` locations during Plan 05.

## Blockers

Plans 01-04 must complete first.

## Next milestone

Plan 05 — Skill 1 End-to-End.

## Skill catalog

| # | Name | Status | File |
|---|---|---|---|
| 01 | company_analyst | Existing (in `00_META/skills/company-analyst/`; migrate in Plan 05) | TBD |
| 02 | industry_analyst | To build (Plan 06) | — |
| 03 | competitor_analyst | Existing partial (in `00_META/skills/competitor-analyst/`; assess in Plan 06) | TBD |
| 04 | meeting_script | To build (Plan 06) | — |
| 05 | opportunity_report | To build (Plan 06) | — |
| 06 | discovery_meeting | Existing (in `00_META/skills/discovery-meeting/`) | TBD |
```

- [ ] **Step 5: Stage and commit**

```bash
git add skills/CLAUDE.md skills/GEMINI.md skills/CHECKPOINT.md skills/STATUS.md
git commit -m "Plan 01 Task 20: Skills-Master persona files (CLAUDE, GEMINI, CHECKPOINT, STATUS)"
git push origin main
```

---

### Task 21: Write pipeline/CLAUDE.md and pipeline/GEMINI.md (Client-Owner persona)

**Files:**
- Create: `pipeline/CLAUDE.md`, `pipeline/GEMINI.md`, `pipeline/CHECKPOINT.md`, `pipeline/STATUS.md`

Same structure as Task 20, with these scope-specific differences:

- Persona name: Client-Owner
- Scope: `pipeline/clients/*/`, `pipeline/prospects/`
- Strict rules:
  - Active client = parameter, not a separate persona (per ADR-011)
  - Client deliverables (in `06_proposal/`, `07_contract_onboarding/`, `05_opportunity_report/`) require human `/go` gate before delivery
  - Vault namespace: only `vault/clients/<slug>/`
  - Skill 4 outputs (meeting script) NEVER render to PDF/DOCX (PRIVATE)
  - `state.json` transitions go through the state machine — no manual edits to `phase` field; use `/advance`, `/regress`, `/set-phase`

(Implementation pattern same as Task 20 — write CLAUDE.md inlining shared stanzas, GEMINI.md as second-seat scope-isolated, CHECKPOINT.md initial state, STATUS.md.)

- [ ] **Step 1: Write pipeline/CLAUDE.md** (use the Skills-Master pattern; substitute scope; add the client-data-handling rules above)

- [ ] **Step 2: Write pipeline/GEMINI.md** (use Skills GEMINI.md pattern; substitute scope)

- [ ] **Step 3: Write pipeline/CHECKPOINT.md**

```markdown
# CHECKPOINT — pipeline (Client-Owner)

**Updated:** 2026-05-13T20:30:00-07:00
**By:** ricardo (via Plan 01 scaffold)
**Persona:** Client-Owner

## What I just did

Scaffolded the Client-Owner persona during Plan 01 Task 21.

## In flight — concrete next action

Per-client work doesn't start until Plan 07 (Per-Client Chain + Pipeline Orchestrator). When that plan begins:
- Migrate the Bodai client folder from any temporary location to `pipeline/clients/bodai/` per the canonical template.
- Scaffold `pipeline/clients/alfa-bitcoin/` (first pilot per Plan Maestro).
- Wire `/new-client`, `/intake`, `/advance` Telegram plugins.

## Blocked on

Plans 01-06 must complete first.

## Open questions

None at scaffold.

## Files modified but not yet committed

None.

## Estimated time to finish

N/A (waiting for Plan 07).

## After this, what's next

Plan 07 — Per-Client Chain.
```

- [ ] **Step 4: Write pipeline/STATUS.md**

```markdown
# Pipeline — STATUS

> **Last updated:** 2026-05-13
> **Current phase:** Pre-client-work (waiting for Plan 07 start)

## Current state

Client-Owner persona scaffolded. No active clients yet. First pilot (Alfa Bitcoin per Plan Maestro) will be scaffolded during Plan 07.

## Active clients

None.

## Prospects

None.

## Blockers

Plans 01-06 must complete first.

## Next milestone

Plan 07 — Per-Client Chain + Pipeline Orchestrator.
```

- [ ] **Step 5: Stage and commit**

```bash
git add pipeline/CLAUDE.md pipeline/GEMINI.md pipeline/CHECKPOINT.md pipeline/STATUS.md
git commit -m "Plan 01 Task 21: Client-Owner persona files (CLAUDE, GEMINI, CHECKPOINT, STATUS)"
git push origin main
```

---

## Phase J — Per-machine bootstrap profiles

### Task 22: Write per-machine YAML profiles

**Files:**
- Create: `infra/machines/{hp-server,hp-standby,ricardo-desktop,ricardo-travel,jp-light,jp-heavy,phones}.yaml`

- [ ] **Step 1: Write `infra/machines/hp-server.yaml`**

```yaml
# infra/machines/hp-server.yaml — primary live server profile
hostname: ricardo-hp-laptop
role: live-server
os: linux-mint
tailscale:
  required: true
  ip: 100.64.121.80
docker:
  services:
    # Services populated by later plans (3 and 4 and 8):
    # - gitea (already running, separate compose)
    # - nexostrat-bot (Plan 04)
    # - jitsi-* (Plan 08)
    # - nextcloud (Plan 08)
    # - whisper-cpp (Plan 08)
    # - mcp-* (Plan 03)
    - placeholder  # nothing in Plan 01
cli_tools:
  - git
  - age
  - rclone
  - pandoc
  - jq
  - yq
  - python3
  - shred
hooks:
  pre_commit:
    - secret-scan          # Plan 01 Task 25
    - file-pattern-block   # Plan 01 Task 26
    # Added later:
    # - docs-pair-check    # Plan 02
    # - checkpoint-validation # Plan 02
  post_receive_gitea:
    - mirror_to_github     # Plan 01 Task 13
    # - mirror_to_codeberg # Plan 02 Phase B
crons_via_systemd:
  - nexostrat-warm-rsync.timer        # Plan 01 Task 16 (nightly 03:00)
  # Added later:
  # - nexostrat-event-router.service  # Plan 03 (daemon)
  # - nexostrat-daily-brief.timer     # Plan 04 (07:00 daily)
  # - nexostrat-chat-extractor.timer  # Plan 09 (every 4h office hours)
  # - nexostrat-backup-verify.timer   # Plan 10 (weekly Sun 02:00)
```

- [ ] **Step 2: Write `infra/machines/hp-standby.yaml`**

```yaml
# infra/machines/hp-standby.yaml — warm-standby profile
hostname: <STANDBY_HOSTNAME>   # set during Task 14
role: warm-standby
os: linux-mint  # or specify
tailscale:
  required: true
  ip: <STANDBY_TS_IP>
docker:
  services:
    # Same as hp-server, but state=stopped (idle)
    - placeholder
  state: idle  # docker-compose.yml present but services not running
cli_tools:
  - git
  - age
  - rclone
  - pandoc
  - jq
  - yq
  - python3
hooks: {}  # standby doesn't enforce hooks; it's a read replica
crons_via_systemd:
  - receive-rsync-from-hp  # the rsync target side; created in Plan 01 Task 16
```

Replace `<STANDBY_HOSTNAME>` and `<STANDBY_TS_IP>` with real values from Task 14.

- [ ] **Step 3: Write `infra/machines/ricardo-desktop.yaml`**

```yaml
# infra/machines/ricardo-desktop.yaml — GPU worker profile (office hours)
hostname: ricardo-desktop
role: gpu-worker
os: linux-mint-22.3
tailscale:
  required: true
  ip: pending  # set during Phase 2 of desktop bootstrap
docker:
  services:
    # Populated by Plan 03 (Ollama)
    - placeholder
gpu:
  driver: nvidia-driver-580-open
  card: rtx-3060-ti-8gb
  models_planned:
    - llama3.1:8b-instruct-q5_K_M
    - qwen2.5:14b-instruct-q4_K_M
    - mistral:7b-instruct
schedule:
  awake_hours: "08:00-20:00"
  suspend_at: "20:00"
  wake_on_lan: enabled
cli_tools:
  - git
  - claude-code
  - gemini-cli
  - age
  - rclone
  - pandoc
  - ollama  # added in Plan 03
desktop_apps:
  - obsidian
  - telegram-desktop
  - vscode
```

- [ ] **Step 4: Write `infra/machines/ricardo-travel.yaml`**

```yaml
# infra/machines/ricardo-travel.yaml — workstation profile
hostname: <RICARDO_TRAVEL_HOSTNAME>
role: workstation
os: linux-mint
tailscale:
  required: true
docker:
  services: []  # no services
cli_tools:
  - git
  - claude-code
  - gemini-cli
  - age
  - rclone
  - pandoc
desktop_apps:
  - obsidian
  - telegram-desktop
  - vscode
```

- [ ] **Step 5: Write `infra/machines/jp-light.yaml`**

```yaml
# infra/machines/jp-light.yaml — JP's Light mode profile
hostname: <JP_LAPTOP_HOSTNAME>
role: light-client
os: <JP_OS>  # ask JP
tailscale:
  required: false  # optional for Light mode
docker:
  services: []
cli_tools: []
desktop_apps:
  - telegram-desktop
  - browser  # for Gitea web UI
mobile:
  - telegram-mobile
```

- [ ] **Step 6: Write `infra/machines/jp-heavy.yaml`**

```yaml
# infra/machines/jp-heavy.yaml — JP's Heavy mode profile (future)
hostname: <JP_LAPTOP_HOSTNAME>
role: heavy-client
os: <JP_OS>
tailscale:
  required: true
docker:
  services: []
cli_tools:
  - git
  - claude-code
  - gemini-cli
  - age
  - pandoc
desktop_apps:
  - obsidian
  - telegram-desktop
  - vscode
mobile:
  - telegram-mobile
notes: |
  JP activates this profile when he chooses to move from Light to Heavy.
  Onboarding ~1 hour: install CLI tools, generate age keypair, add JP's
  public key to infra/age-recipients.txt (via PR + Ricardo approval),
  re-encrypt vault to include JP's key, git clone repo.
```

- [ ] **Step 7: Write `infra/machines/phones.yaml`**

```yaml
# infra/machines/phones.yaml — phone allowlist + apps
allowlist:
  # Chat IDs from Telegram (populated when bot is created in Plan 04)
  - chat_id: <RICARDO_TELEGRAM_ID>
    role: owner
    display_name: Ricardo
  - chat_id: <JP_TELEGRAM_ID>
    role: owner
    display_name: JP
apps_required:
  - telegram-mobile
permissions:
  read_only: false
  bot_commands: all
```

- [ ] **Step 8: Stage and commit all profiles**

```bash
git add infra/machines/
git commit -m "Plan 01 Task 22: per-machine YAML profiles (7 machines)"
git push origin main
```

---

### Task 23: Write bootstrap-machine.sh

**Files:**
- Create: `infra/scripts/bootstrap-machine.sh`

- [ ] **Step 1: Write the bootstrap script**

```bash
#!/usr/bin/env bash
# Nexostrat — bootstrap a machine from its YAML profile.
# Usage: bootstrap-machine.sh <profile-name>
# Example: bootstrap-machine.sh ricardo-desktop

set -euo pipefail

NEXOSTRAT_ROOT="${NEXOSTRAT_ROOT:-/srv/Nexostrat}"
PROFILE="${1:?Usage: bootstrap-machine.sh <profile>}"
PROFILE_FILE="$NEXOSTRAT_ROOT/infra/machines/${PROFILE}.yaml"

if [ ! -f "$PROFILE_FILE" ]; then
    echo "ERROR: Unknown profile: $PROFILE" >&2
    echo "Available:" >&2
    ls "$NEXOSTRAT_ROOT/infra/machines/" | grep .yaml | sed 's/.yaml$//' >&2
    exit 1
fi

# Ensure yq is available for YAML parsing
if ! command -v yq >/dev/null; then
    echo "ERROR: yq not installed. Install via: sudo apt install yq (or via snap)" >&2
    exit 1
fi

echo "=== Nexostrat bootstrap: $PROFILE ==="
echo "Profile: $PROFILE_FILE"
echo

# Detect OS for branching
OS_ID=$(grep '^ID=' /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '"' || echo unknown)
echo "Detected OS: $OS_ID"

# Install function — branch on OS
install_pkg() {
    local pkg="$1"
    if command -v "$pkg" >/dev/null 2>&1; then
        echo "  [SKIP] $pkg already installed"
        return 0
    fi
    case "$OS_ID" in
        ubuntu|debian|linuxmint)
            sudo apt install -y "$pkg" || echo "  [WARN] $pkg install failed"
            ;;
        fedora|rhel)
            sudo dnf install -y "$pkg" || echo "  [WARN] $pkg install failed"
            ;;
        *)
            echo "  [WARN] Unknown OS — manually install $pkg"
            ;;
    esac
}

# 1. CLI tools
echo ">>> CLI tools"
mapfile -t cli_tools < <(yq -r '.cli_tools[]?' "$PROFILE_FILE" 2>/dev/null)
for tool in "${cli_tools[@]}"; do
    [ -n "$tool" ] && install_pkg "$tool"
done

# 2. Tailscale
echo ">>> Tailscale"
ts_required=$(yq -r '.tailscale.required' "$PROFILE_FILE" 2>/dev/null)
if [ "$ts_required" = "true" ]; then
    if ! command -v tailscale >/dev/null; then
        echo "  Installing Tailscale..."
        curl -fsSL https://tailscale.com/install.sh | sudo sh
    fi
    if ! tailscale status >/dev/null 2>&1; then
        echo "  Tailscale not connected. Run: sudo tailscale up"
        echo "  (manual step; auth in browser)"
    else
        echo "  [OK] Tailscale connected: $(tailscale ip -4)"
    fi
fi

# 3. Desktop apps (Linux Mint specific)
echo ">>> Desktop apps"
mapfile -t desktop_apps < <(yq -r '.desktop_apps[]?' "$PROFILE_FILE" 2>/dev/null)
for app in "${desktop_apps[@]}"; do
    [ -z "$app" ] && continue
    case "$app" in
        obsidian)
            flatpak install -y flathub md.obsidian.Obsidian 2>/dev/null || echo "  [WARN] Obsidian install needs Flatpak"
            ;;
        telegram-desktop)
            install_pkg telegram-desktop
            ;;
        vscode|code)
            if ! command -v code >/dev/null; then
                echo "  Install VS Code manually (https://code.visualstudio.com/) or via Flatpak"
            fi
            ;;
        browser)
            echo "  [SKIP] Browser already on system"
            ;;
        *)
            echo "  [WARN] Unknown app: $app"
            ;;
    esac
done

# 4. Docker (if services list non-empty)
echo ">>> Docker"
n_services=$(yq -r '.docker.services | length' "$PROFILE_FILE" 2>/dev/null)
if [ "$n_services" != "0" ] && [ "$n_services" != "null" ]; then
    if ! command -v docker >/dev/null; then
        echo "  Installing Docker..."
        curl -fsSL https://get.docker.com | sudo sh
        sudo usermod -aG docker "$USER"
        echo "  [NOTE] Log out and back in for docker group to take effect"
    else
        echo "  [OK] Docker already installed"
    fi
else
    echo "  Profile declares no services; skipping Docker install"
fi

# 5. age keypair (if not already present)
echo ">>> age keys"
if [ ! -f "$HOME/.age/nexostrat-$USER.key" ] && [ -z "${SKIP_AGE_KEYGEN:-}" ]; then
    echo "  No Nexostrat age key found at $HOME/.age/nexostrat-$USER.key"
    echo "  Run: age-keygen -o $HOME/.age/nexostrat-$USER.key"
    echo "  Then: add the public key to $NEXOSTRAT_ROOT/infra/age-recipients.txt"
    echo "  See $NEXOSTRAT_ROOT/docs/how-to/11_rotate_age_keys.md (will be written in Plan 02)"
else
    echo "  [OK] Age key present"
fi

# 6. Verify
echo
echo "=== Bootstrap complete for $PROFILE ==="
echo "Next:"
echo "  - If you generated an age key, add the public key to infra/age-recipients.txt"
echo "  - If services are declared, populate docker-compose.yml in later plans"
echo "  - Run smoke test: $NEXOSTRAT_ROOT/infra/scripts/smoke-test.sh"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x infra/scripts/bootstrap-machine.sh
```

- [ ] **Step 3: Idempotency test — run for hp-server (already provisioned)**

```bash
infra/scripts/bootstrap-machine.sh hp-server
```

Expected: most steps print `[SKIP] already installed` because HP is already set up. No errors. Exit code 0.

- [ ] **Step 4: Stage and commit**

```bash
git add infra/scripts/bootstrap-machine.sh
git commit -m "Plan 01 Task 23: bootstrap-machine.sh (idempotent, per-profile)"
git push origin main
```

---

## Phase K — Initial pre-commit hooks

### Task 24: Write the secret-scan hook

**Files:**
- Create: `infra/hooks/pre-commit-secret-scan.sh`
- Create: `infra/hooks/tests/test_secret_scan.sh`

- [ ] **Step 1: Write the failing test first (TDD)**

```bash
mkdir -p infra/hooks/tests
```

Create `infra/hooks/tests/test_secret_scan.sh`:

```bash
#!/usr/bin/env bash
# Test infra/hooks/pre-commit-secret-scan.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="$SCRIPT_DIR/pre-commit-secret-scan.sh"

if [ ! -x "$HOOK" ]; then
    echo "FAIL: $HOOK not executable or missing"
    exit 1
fi

# Test 1: detect Anthropic key pattern
TESTFILE=$(mktemp /tmp/secret-scan-test.XXXXXX.txt)
echo "ANTHROPIC_API_KEY=sk-ant-api03-AAAAAAAAAAAAAAAAAAAAAA" > "$TESTFILE"
if "$HOOK" "$TESTFILE" >/dev/null 2>&1; then
    echo "FAIL: hook did not detect Anthropic key in $TESTFILE"
    rm "$TESTFILE"
    exit 1
fi
rm "$TESTFILE"

# Test 2: detect AWS key pattern
TESTFILE=$(mktemp /tmp/secret-scan-test.XXXXXX.txt)
echo "AKIAIOSFODNN7EXAMPLE" > "$TESTFILE"
if "$HOOK" "$TESTFILE" >/dev/null 2>&1; then
    echo "FAIL: hook did not detect AWS key in $TESTFILE"
    rm "$TESTFILE"
    exit 1
fi
rm "$TESTFILE"

# Test 3: don't false-positive on normal markdown
TESTFILE=$(mktemp /tmp/secret-scan-test.XXXXXX.md)
echo "# Just a heading" > "$TESTFILE"
echo "Some normal markdown content." >> "$TESTFILE"
if ! "$HOOK" "$TESTFILE" >/dev/null 2>&1; then
    echo "FAIL: hook false-positived on plain markdown"
    rm "$TESTFILE"
    exit 1
fi
rm "$TESTFILE"

echo "PASS: all secret-scan tests"
```

Make executable: `chmod +x infra/hooks/tests/test_secret_scan.sh`

- [ ] **Step 2: Run the test to verify it fails (hook doesn't exist yet)**

Run: `infra/hooks/tests/test_secret_scan.sh`
Expected: `FAIL: ... not executable or missing` (because we haven't written the hook).

- [ ] **Step 3: Write the hook**

```bash
#!/usr/bin/env bash
# Nexostrat — pre-commit secret scanner.
# Usage: pre-commit-secret-scan.sh [file ...]
# Without args: scans all staged files in the current commit.
# Exit 0 = clean. Exit 1 = secret pattern detected (commit refused).

set -euo pipefail

# Patterns to detect (extended regex)
# Anthropic API keys: sk-ant-...
# OpenAI: sk-...{20,}
# AWS: AKIA[0-9A-Z]{16}
# GitHub PAT (classic): ghp_[0-9a-zA-Z]{36}
# GitHub PAT (fine-grained): github_pat_...
# Generic JWT: eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}
# Google API: AIza[0-9A-Za-z\-_]{35}
# xAI Grok: xai-[A-Za-z0-9]+

PATTERNS=(
    'sk-ant-[A-Za-z0-9_-]{20,}'
    'sk-[A-Za-z0-9_-]{40,}'
    'AKIA[0-9A-Z]{16}'
    'ghp_[0-9a-zA-Z]{36}'
    'github_pat_[A-Za-z0-9_]+'
    'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
    'AIza[0-9A-Za-z_-]{35}'
    'xai-[A-Za-z0-9]+'
    'BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY'
)

# Files to skip (own MANIFEST and example/test files)
SKIP_FILES=(
    'infra/secrets/MANIFEST.md'
    '.env.example'
    'infra/hooks/pre-commit-secret-scan.sh'
    'infra/hooks/tests/test_secret_scan.sh'
)

is_skipped() {
    local f="$1"
    for skip in "${SKIP_FILES[@]}"; do
        if [ "$f" = "$skip" ] || [[ "$f" == */"$skip" ]]; then
            return 0
        fi
    done
    return 1
}

scan_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    is_skipped "$f" && return 0

    # Skip binary files
    if file "$f" | grep -q 'binary\|executable\|ELF'; then
        return 0
    fi
    # Skip age-encrypted files (they're already encrypted, internals are noise)
    case "$f" in
        *.age|*.gpg|*.enc) return 0 ;;
    esac

    for pat in "${PATTERNS[@]}"; do
        if grep -qE "$pat" "$f"; then
            echo "BLOCKED: secret pattern '$pat' detected in $f" >&2
            return 1
        fi
    done
    return 0
}

# Determine files to scan
if [ "$#" -gt 0 ]; then
    files=("$@")
else
    # Pre-commit mode: scan staged files
    mapfile -t files < <(git diff --cached --name-only --diff-filter=AM)
fi

failed=0
for f in "${files[@]}"; do
    scan_file "$f" || failed=1
done

if [ "$failed" = 1 ]; then
    echo "" >&2
    echo "Pre-commit hook BLOCKED this commit." >&2
    echo "To bypass (only for safe content the hook misjudges): git commit --no-verify" >&2
    echo "But verify carefully first — bypassing means accepting responsibility." >&2
    exit 1
fi
exit 0
```

Save as `infra/hooks/pre-commit-secret-scan.sh` and `chmod +x`.

- [ ] **Step 4: Run the test to verify it now passes**

Run: `infra/hooks/tests/test_secret_scan.sh`
Expected: `PASS: all secret-scan tests`

- [ ] **Step 5: Stage and commit**

```bash
git add infra/hooks/pre-commit-secret-scan.sh infra/hooks/tests/test_secret_scan.sh
git commit -m "Plan 01 Task 24: pre-commit secret-scan hook + tests"
git push origin main
```

---

### Task 25: Write the file-pattern-block hook

**Files:**
- Create: `infra/hooks/pre-commit-file-pattern-block.sh`
- Create: `infra/hooks/tests/test_file_pattern_block.sh`

- [ ] **Step 1: Write the failing test**

```bash
#!/usr/bin/env bash
# Test infra/hooks/pre-commit-file-pattern-block.sh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="$SCRIPT_DIR/pre-commit-file-pattern-block.sh"

if [ ! -x "$HOOK" ]; then
    echo "FAIL: $HOOK missing or not executable"
    exit 1
fi

# Test 1: refuse .env (unencrypted)
if "$HOOK" .env 2>/dev/null; then
    echo "FAIL: hook did not block .env"
    exit 1
fi

# Test 2: refuse *.pem
if "$HOOK" my-server.pem 2>/dev/null; then
    echo "FAIL: hook did not block *.pem"
    exit 1
fi

# Test 3: allow .env.example
if ! "$HOOK" .env.example 2>/dev/null; then
    echo "FAIL: hook blocked .env.example (should be allowed)"
    exit 1
fi

# Test 4: allow secrets.env.age
if ! "$HOOK" secrets.env.age 2>/dev/null; then
    echo "FAIL: hook blocked secrets.env.age (should be allowed; it's encrypted)"
    exit 1
fi

echo "PASS: all file-pattern-block tests"
```

Make executable.

- [ ] **Step 2: Run to verify fail**

Run: `infra/hooks/tests/test_file_pattern_block.sh`
Expected: `FAIL: ... missing or not executable`

- [ ] **Step 3: Write the hook**

```bash
#!/usr/bin/env bash
# Nexostrat — pre-commit file-pattern block.
# Refuses commits containing file paths matching dangerous patterns.

set -euo pipefail

# Blocked patterns (regex matched against file paths)
BLOCK_PATTERNS=(
    '(^|/)\.env$'                # .env without encryption (allow .env.example, .env.age)
    '\.pem$'
    '\.key$'                     # private keys (RSA, DSA, etc.)
    '\.p12$'
    '\.pfx$'
    '_rsa$'
    '_dsa$'
    'id_ed25519$'                # SSH private keys
    '\.kdbx$'                    # KeePass DB
)

# Allowed exceptions (override BLOCK_PATTERNS)
ALLOW_PATTERNS=(
    '\.env\.example$'
    '\.env\.age$'
    '\.key\.age$'
    'secrets\.env\.age$'
)

is_allowed() {
    local path="$1"
    for pat in "${ALLOW_PATTERNS[@]}"; do
        echo "$path" | grep -qE "$pat" && return 0
    done
    return 1
}

is_blocked() {
    local path="$1"
    is_allowed "$path" && return 1
    for pat in "${BLOCK_PATTERNS[@]}"; do
        echo "$path" | grep -qE "$pat" && return 0
    done
    return 1
}

# Determine files to check
if [ "$#" -gt 0 ]; then
    files=("$@")
else
    mapfile -t files < <(git diff --cached --name-only --diff-filter=AM)
fi

failed=0
for f in "${files[@]}"; do
    if is_blocked "$f"; then
        echo "BLOCKED: $f matches a refused file pattern" >&2
        failed=1
    fi
done

if [ "$failed" = 1 ]; then
    echo "" >&2
    echo "Pre-commit hook BLOCKED this commit." >&2
    echo "Possible fixes:" >&2
    echo "  - Encrypt the file first: age -R infra/age-recipients.txt <file> > <file>.age" >&2
    echo "  - If this is a legitimate non-secret with a clashing name, rename it" >&2
    echo "  - To bypass (last resort): git commit --no-verify" >&2
    exit 1
fi
exit 0
```

Save as `infra/hooks/pre-commit-file-pattern-block.sh` and `chmod +x`.

- [ ] **Step 4: Run test to verify pass**

Run: `infra/hooks/tests/test_file_pattern_block.sh`
Expected: `PASS: all file-pattern-block tests`

- [ ] **Step 5: Stage and commit**

```bash
git add infra/hooks/pre-commit-file-pattern-block.sh infra/hooks/tests/test_file_pattern_block.sh
git commit -m "Plan 01 Task 25: pre-commit file-pattern-block hook + tests"
git push origin main
```

---

### Task 26: Write install-hooks.sh and wire into .git/hooks

**Files:**
- Create: `infra/hooks/install-hooks.sh`

- [ ] **Step 1: Write the installer**

```bash
#!/usr/bin/env bash
# Nexostrat — install pre-commit hooks into .git/hooks/
# Idempotent: re-running is safe.

set -euo pipefail

NEXOSTRAT_ROOT="${NEXOSTRAT_ROOT:-/srv/Nexostrat}"
HOOKS_SRC="$NEXOSTRAT_ROOT/infra/hooks"
GIT_HOOKS="$NEXOSTRAT_ROOT/.git/hooks"

if [ ! -d "$GIT_HOOKS" ]; then
    echo "ERROR: $GIT_HOOKS not found. Are you in a git repo?" >&2
    exit 1
fi

# Composite pre-commit hook — chains our checks
cat > "$GIT_HOOKS/pre-commit" <<'EOF'
#!/usr/bin/env bash
# Nexostrat composite pre-commit hook
# Runs each registered check; first failure blocks the commit.

set -euo pipefail
NEXOSTRAT_ROOT="$(git rev-parse --show-toplevel)"

# Registered checks (in order)
CHECKS=(
    "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-secret-scan.sh"
    "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-file-pattern-block.sh"
    # Added in later plans:
    # "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-docs-pair.sh"   # Plan 02
    # "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-checkpoint.sh"   # Plan 02
)

for check in "${CHECKS[@]}"; do
    if [ -x "$check" ]; then
        if ! "$check"; then
            echo ""
            echo "Pre-commit check FAILED: $check"
            exit 1
        fi
    fi
done
exit 0
EOF
chmod +x "$GIT_HOOKS/pre-commit"

echo "Installed: .git/hooks/pre-commit (composite hook chaining ${#CHECKS[@]} checks)"
echo ""
echo "To verify: try committing a file with a fake API key:"
echo "  echo 'sk-ant-api03-fake' > /tmp/test.txt && git add /tmp/test.txt && git commit -m test"
echo "  → should be BLOCKED"
```

Save as `infra/hooks/install-hooks.sh` and `chmod +x`.

- [ ] **Step 2: Run the installer**

```bash
infra/hooks/install-hooks.sh
```

Expected: prints `Installed: .git/hooks/pre-commit...`

- [ ] **Step 3: Verify the composite hook is in place**

```bash
ls -l .git/hooks/pre-commit
head -5 .git/hooks/pre-commit
```
Expected: file exists, executable, starts with `#!/usr/bin/env bash`.

- [ ] **Step 4: End-to-end test — planted secret blocked**

```bash
echo 'ANTHROPIC_API_KEY=sk-ant-api03-AAAAAAAAAAAAAAAAAAAAAA' > /tmp/secret-test.txt
git add /tmp/secret-test.txt 2>/dev/null || true   # may fail because /tmp is outside repo
# Actual test: stage a file inside the repo
mkdir -p /tmp/secret-test-inside-repo
cp /tmp/secret-test.txt /srv/Nexostrat/operations/marketing/test-leak.txt
git add operations/marketing/test-leak.txt
git commit -m "Testing the hook (this should fail)" || echo "GOOD — commit was blocked"
# Clean up
git reset HEAD operations/marketing/test-leak.txt
rm operations/marketing/test-leak.txt /tmp/secret-test.txt
```

Expected: commit blocked with message `BLOCKED: secret pattern 'sk-ant-...' detected in operations/marketing/test-leak.txt`.

- [ ] **Step 5: Stage and commit the installer**

```bash
git add infra/hooks/install-hooks.sh
git commit -m "Plan 01 Task 26: install-hooks.sh installs composite pre-commit chain"
git push origin main
```

---

## Phase L — Smoke test + finalize

### Task 27: Write infra/scripts/smoke-test.sh

**Files:**
- Create: `infra/scripts/smoke-test.sh`

- [ ] **Step 1: Write the smoke test**

```bash
#!/usr/bin/env bash
# Nexostrat — Stage 0 smoke test. Run after Plan 01 to verify the foundation.
# Exit 0 = all green. Exit 1 = at least one check failed.

set -uo pipefail  # NOT -e — we want to report all failures, not stop at first

NEXOSTRAT_ROOT="${NEXOSTRAT_ROOT:-/srv/Nexostrat}"
PASS=0
FAIL=0

check() {
    local name="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo "[PASS] $name"
        PASS=$((PASS+1))
    else
        echo "[FAIL] $name"
        FAIL=$((FAIL+1))
    fi
}

echo "=== Nexostrat Stage 0 smoke test ==="
echo ""

# 1. Filesystem checks
check "Repo root exists" test -d "$NEXOSTRAT_ROOT"
check "Three buckets exist" test -d "$NEXOSTRAT_ROOT/skills" && test -d "$NEXOSTRAT_ROOT/pipeline" && test -d "$NEXOSTRAT_ROOT/operations"
check "Cross-cutting folders exist" test -d "$NEXOSTRAT_ROOT/00_META" && test -d "$NEXOSTRAT_ROOT/00_GOVERNANCE" && test -d "$NEXOSTRAT_ROOT/00_PARTNERSHIP" && test -d "$NEXOSTRAT_ROOT/docs" && test -d "$NEXOSTRAT_ROOT/infra" && test -d "$NEXOSTRAT_ROOT/vault" && test -d "$NEXOSTRAT_ROOT/knowledge"

# 2. Persona files
check "Root CLAUDE.md exists" test -f "$NEXOSTRAT_ROOT/CLAUDE.md"
check "Root GEMINI.md exists" test -f "$NEXOSTRAT_ROOT/GEMINI.md"
check "Root CHECKPOINT.md exists" test -f "$NEXOSTRAT_ROOT/CHECKPOINT.md"
check "Skills CLAUDE.md exists" test -f "$NEXOSTRAT_ROOT/skills/CLAUDE.md"
check "Pipeline CLAUDE.md exists" test -f "$NEXOSTRAT_ROOT/pipeline/CLAUDE.md"

# 3. Shared stanzas (all 9)
for s in rule1_operator_scope session_start session_end session_output_format memo_protocol gemini_handoff vault_access backup_policy checkpoint_pattern; do
    check "shared/$s.md exists" test -f "$NEXOSTRAT_ROOT/00_META/shared/$s.md"
done

# 4. age + secrets
check "infra/age-recipients.txt exists" test -f "$NEXOSTRAT_ROOT/infra/age-recipients.txt"
check "infra/age-recipients.txt has a recipient" bash -c "grep -v '^#' '$NEXOSTRAT_ROOT/infra/age-recipients.txt' | grep -v '^\$' | grep -q '^age1'"
check "secrets.env.age exists" test -f "$NEXOSTRAT_ROOT/secrets.env.age"
check "secrets.env.age decrypts" bash -c "$NEXOSTRAT_ROOT/infra/scripts/run-with-secrets.sh env | grep -q '^ANTHROPIC_API_KEY='"

# 5. Vault
check "vault/README.md exists" test -f "$NEXOSTRAT_ROOT/vault/README.md"
check "vault/sensitive_index.md exists" test -f "$NEXOSTRAT_ROOT/vault/sensitive_index.md"

# 6. Per-machine profiles
for p in hp-server hp-standby ricardo-desktop ricardo-travel jp-light jp-heavy phones; do
    check "Profile $p.yaml exists" test -f "$NEXOSTRAT_ROOT/infra/machines/$p.yaml"
done

# 7. Hooks
check "Composite pre-commit hook installed" test -x "$NEXOSTRAT_ROOT/.git/hooks/pre-commit"
check "Secret-scan hook executable" test -x "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-secret-scan.sh"
check "Secret-scan hook tests pass" "$NEXOSTRAT_ROOT/infra/hooks/tests/test_secret_scan.sh"
check "File-pattern-block hook executable" test -x "$NEXOSTRAT_ROOT/infra/hooks/pre-commit-file-pattern-block.sh"
check "File-pattern-block hook tests pass" "$NEXOSTRAT_ROOT/infra/hooks/tests/test_file_pattern_block.sh"

# 8. Git remotes
check "Gitea origin remote configured" bash -c "cd '$NEXOSTRAT_ROOT' && git remote get-url origin | grep -q '100.64.121.80'"
check "GitHub mirror remote configured" bash -c "cd '$NEXOSTRAT_ROOT' && git remote get-url github | grep -q 'github.com'"

# 9. Per-repo git identity
check "Git author is Nexostrat" bash -c "cd '$NEXOSTRAT_ROOT' && git config user.email | grep -q 'contacto@nexostrat.com'"

# 10. Warm-standby
check "warm-standby-rsync.sh executable" test -x "$NEXOSTRAT_ROOT/infra/scripts/warm-standby-rsync.sh"
check "warm-rsync systemd timer enabled" bash -c "systemctl is-enabled nexostrat-warm-rsync.timer 2>/dev/null | grep -q enabled"

# 11. Bootstrap
check "bootstrap-machine.sh executable" test -x "$NEXOSTRAT_ROOT/infra/scripts/bootstrap-machine.sh"

echo ""
echo "=== Result ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
if [ "$FAIL" = 0 ]; then
    echo ""
    echo "🟢 Stage 0 foundation is GREEN. Ready to start Plan 02."
    exit 0
else
    echo ""
    echo "🔴 Stage 0 foundation has $FAIL failure(s). Fix before proceeding."
    exit 1
fi
```

Make executable: `chmod +x infra/scripts/smoke-test.sh`

- [ ] **Step 2: Run the smoke test**

```bash
infra/scripts/smoke-test.sh
```

Expected: all checks PASS. If any FAIL: read the message, fix, re-run.

If you used emojis in the script and the terminal doesn't render them well, that's cosmetic — the PASS/FAIL counts are what matter.

- [ ] **Step 3: Stage and commit**

```bash
git add infra/scripts/smoke-test.sh
git commit -m "Plan 01 Task 27: smoke-test.sh covering 30+ Stage 0 foundation checks"
git push origin main
```

---

### Task 28: Update CHANGELOG, STATUS, CHECKPOINT; tag v0.1-foundation

**Files:**
- Modify: `00_META/CHANGELOG.md`, `STATUS.md`, `CHECKPOINT.md`, `tasks.json`

- [ ] **Step 1: Append Plan 01 completion entry to 00_META/CHANGELOG.md**

```markdown
| 2026-05-13 | Claude + Ricardo | **Plan 01 — Repository Foundation complete.** 3-bucket scaffold (skills/, pipeline/, operations/) + cross-cutting (00_META/, 00_GOVERNANCE/, 00_PARTNERSHIP/, docs/, infra/, vault/, knowledge/). age keypair for Ricardo, age-recipients.txt with one recipient (JP pending Heavy mode), secrets.env.age with placeholders, run-with-secrets.sh wrapper. GitHub private mirror + Gitea post-receive hook mirroring on every push. Warm-standby host provisioned + nightly rsync via systemd timer at 03:00. Six persona files (root CLAUDE+GEMINI Founder, skills CLAUDE+GEMINI Skills-Master, pipeline CLAUDE+GEMINI Client-Owner) with shared stanzas at 00_META/shared/. Per-machine YAML profiles for 7 machines. bootstrap-machine.sh idempotent + tested. Pre-commit composite hook chaining secret-scan + file-pattern-block, with TDD tests for each. Smoke test covers 30+ checks, all green. Tagged v0.1-foundation. |
```

- [ ] **Step 2: Update STATUS.md**

Replace existing STATUS.md content:

```markdown
# Nexostrat — STATUS

> **Last updated:** 2026-05-13
> **Current phase:** Plan 01 DONE — ready for Plan 02 (Documentation System)

## Current state

Foundation phase complete. The 3-bucket repository structure is scaffolded, identities (age keys) are locked, the backup ladder is operational, all six persona files are in place, the warm-standby is provisioned with nightly rsync, GitHub mirror is live, pre-commit hooks block plaintext secrets. Smoke test at `infra/scripts/smoke-test.sh` returns green. Tagged `v0.1-foundation`.

## Blockers

None.

## Next milestone

Plan 02 — Documentation System. Start with the writing-plans skill against the master index entry for Plan 02. Expected effort: ~3 days.

## Recent activity

- **2026-05-13** — Plan 01 executed and completed. ~28 commits, foundation green. Smoke test passes 30+ checks.
- **2026-05-13** — Founding spec written + committed (commit `493d0b4`).

## Pending JP input

- JP brand top-5 vote (t-006, due 2026-05-14). Ricardo's pick: Nexostrat 8/10, Aurora palette 5/5.
- JP age public key (deferred until Heavy mode). Vault is currently encrypted to Ricardo only with an explicit follow-up memo in 00_META/inbox/.
- JP attendance for the Founding Meeting (Plan Maestro Paso 1) — before partnership docs are finalized in Plan 02.

## Open follow-ups

- Plan 02 — Documentation System (~3 days)
- Plan 03 — events.jsonl + Python agent framework (~1 week)
- See full roadmap at `00_META/plans/README.md`.
```

- [ ] **Step 3: Update CHECKPOINT.md to reflect Plan 01 done**

```markdown
# CHECKPOINT — root (Founder)

**Updated:** 2026-05-13T22:00:00-07:00
**By:** ricardo (Plan 01 wrap-up)
**Persona:** Founder

## What I just did

Completed Plan 01 — Repository Foundation. All 28 tasks executed end-to-end. Smoke test green. Tagged `v0.1-foundation`.

## In flight — concrete next action

Start Plan 02 — Documentation System. Action:
1. Open Claude Code at `/srv/Nexostrat/`.
2. Invoke writing-plans skill against the Plan 02 entry in `00_META/plans/README.md`.
3. Claude drafts Plan 02 in full task-by-task detail, similar in length and shape to Plan 01.
4. Review the drafted plan; approve; execute.

## Blocked on

Nothing.

## Open questions

- Do we want a per-bucket CHECKPOINT.md auto-write hook in Plan 02, or save for Plan 03?
- Plan 02 should write all 15 new ADRs (021-035); confirm acceptable scope.

## Files modified but not yet committed

None — Plan 01 finished cleanly with `git status` showing nothing pending.

## Estimated time to finish

Plan 02: ~3 days.

## After this, what's next

Plans 03 and 04 (events spine + Telegram bot) can run partly in parallel after Plan 02.
```

- [ ] **Step 4: Update tasks.json**

Mark t-plan-01 as completed; add t-plan-02 as the next active task:

```json
{
  "$schema": "brain-tasks-v1",
  "project": "nexostrat",
  "updated": "2026-05-13T22:00:00-07:00",
  "tasks": [
    {
      "id": "t-plan-01",
      "subject": "Execute Plan 01 — Repository Foundation",
      "status": "completed",
      "priority": "critical",
      "due": "2026-05-20",
      "created": "2026-05-13",
      "completed": "2026-05-13",
      "notes": "DONE. 28 commits. Smoke test green. Tagged v0.1-foundation."
    },
    {
      "id": "t-plan-02",
      "subject": "Execute Plan 02 — Documentation System",
      "status": "open",
      "priority": "high",
      "due": "2026-05-17",
      "created": "2026-05-13",
      "notes": "Header in 00_META/plans/README.md. To be written in detail when starting, via writing-plans skill."
    },
    {
      "id": "t-jp-brand-vote",
      "subject": "JP vote on top-5 brand HTML",
      "status": "open",
      "priority": "high",
      "due": "2026-05-14",
      "created": "2026-05-12",
      "notes": "Carryover."
    },
    {
      "id": "t-founding-meeting",
      "subject": "Founding Meeting (Plan Maestro Paso 1) — Ricardo + JP",
      "status": "open",
      "priority": "high",
      "due": "2026-05-20",
      "created": "2026-05-13"
    }
  ]
}
```

- [ ] **Step 5: Write a session journal entry**

Create `00_META/journal/2026-05-13_plan-01-execution.md`:

```markdown
# 2026-05-13 — Plan 01 execution

**Session type:** implementation
**Duration:** ~Plan 01 elapsed time (varies by execution speed)
**Agent:** Claude Code (via subagent-driven-development OR executing-plans, per Ricardo's choice)

## What was done

Executed Plan 01 — Repository Foundation start to finish. 28 tasks (~120 individual steps). Output:

- 3-bucket folder scaffold + cross-cutting governance folders
- Root persona files (Founder CLAUDE.md + GEMINI.md + CHECKPOINT.md + STATUS.md)
- skills/ persona files (Skills-Master variants)
- pipeline/ persona files (Client-Owner variants)
- Shared stanzas at 00_META/shared/ (9 files)
- age keypair for Ricardo; vault structure; secrets.env.age + MANIFEST + wrapper
- GitHub private mirror via Gitea post-receive hook (verified active)
- Warm-standby provisioned + nightly rsync via systemd timer 03:00
- Per-machine YAML profiles for 7 machines
- bootstrap-machine.sh + idempotency tested on hp-server
- Pre-commit composite hook (secret-scan + file-pattern-block) with TDD tests
- Smoke test (30+ checks) returning green
- Tagged v0.1-foundation

## Decisions made

(Captured here as they came up during execution — supplement with anything Ricardo decided live.)

- Standby host: <FILL IN with the chosen hostname>
- Used per-repo git config for `contacto@nexostrat.com` (no global change).
- JP's age public key deferred to Heavy-mode onboarding; vault currently encrypted to Ricardo only.

## Open items

- Start Plan 02 in the next session.
- JP brand top-5 vote still pending (t-006).
- Founding Meeting still to be scheduled.

## Notes

- Smoke test caught a fixed issue with [insert any specific issue if encountered, otherwise: "no issues"].
- The composite pre-commit hook successfully blocked a planted Anthropic key during testing.
- Warm-standby rsync completed in <2 min for the initial sync.

## Files written this session

- All Plan 01 artifacts (~50 new files, ~5 modified)
- This journal entry
- Updated CHANGELOG, STATUS, CHECKPOINT, tasks.json
```

- [ ] **Step 6: Stage and commit the wrap-up**

```bash
git add 00_META/CHANGELOG.md STATUS.md CHECKPOINT.md tasks.json 00_META/journal/2026-05-13_plan-01-execution.md
git commit -m "Plan 01 Task 28: wrap up (CHANGELOG, STATUS, CHECKPOINT, tasks, journal)"
git push origin main
```

- [ ] **Step 7: Tag v0.1-foundation**

```bash
git tag -a v0.1-foundation -m "Plan 01 complete: Repository Foundation. 3-bucket structure, identity, vault, mirror, warm-standby, persona files, hooks, smoke test green."
git push origin v0.1-foundation
```

- [ ] **Step 8: Final smoke test run**

```bash
infra/scripts/smoke-test.sh
```

Expected: all 30+ checks PASS. Plan 01 is officially complete.

---

## Plan 01 — Definition of Done

All of the following must be true:

- [ ] Smoke test (`infra/scripts/smoke-test.sh`) returns green (exit 0)
- [ ] `git tag v0.1-foundation` exists locally AND on GitHub (verify with `git ls-remote --tags github`)
- [ ] Every task above is marked complete
- [ ] `STATUS.md` reads "Plan 01 DONE — ready for Plan 02"
- [ ] `CHECKPOINT.md` says "In flight: start Plan 02"
- [ ] Mention in `00_META/plans/README.md` status table — Plan 01 = DONE (update this manually after tagging)
- [ ] A test commit with a planted secret is blocked by the pre-commit hook
- [ ] A test push to origin successfully mirrors to GitHub (verify GitHub main SHA matches local HEAD)
- [ ] A manual SSH into the warm-standby host shows the latest rsynced state matches HP

If any of these is not green: STOP. Do not start Plan 02 until Plan 01 is fully done. This is what "Boring but Robust" looks like at the foundation layer.

---

## What happens next

Plan 02 (Documentation System) writes the user manual that this foundation deserves. Plans 03 + 04 build the event spine and the Telegram bot — these are the first chance the system "comes alive" with automation. Plan 05 is the first end-to-end skill running on the Bodai benchmark — that's when the firm starts to do real work.

The master plan index at `00_META/plans/README.md` is the source of truth for what's next.

---

## Change Log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (writing-plans skill) | Plan 01 written in full task-by-task detail. ~28 tasks, ~120 steps. Ready for execution via subagent-driven-development or executing-plans. |
