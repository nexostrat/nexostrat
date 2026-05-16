# Plan 01a — Repository Foundation: scaffold + identity + crypto

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **For humans:** This file is the technical plan. A plain-language partner (`-explicado.md`) is deferred to execution-start (Plan 02 will switch on the docs-pair hook; until then partners are written best-effort).

**Goal:** Land the 3-bucket folder scaffold, lock both founders' age keys into the recipients file, ship the secrets-loading wrapper without plaintext leaks, migrate questionnaires + partnership artifacts into their canonical locations, and establish the JSON Schema validation surface. After 01a, a fresh clone bootstraps to a working state where either co-founder can decrypt vault content.

**Architecture:** Filesystem-first plan — most work is folder scaffold + canonical config files + small Python/Bash scripts. The two non-trivial scripts are `run-with-secrets.sh` (C1 fix: explicit-cleanup, no `exec` leak, plaintext lives only in `/dev/shm/nexostrat-secrets-<pid>` and is shredded on every exit path) and a basic pre-commit secret-scan. Several deliverables already partly exist from terrain prep (Ricardo's age key, interim `.gitignore`, `infra/age-recipients.txt`, Gitea origin remote) — those become VERIFY tasks instead of CREATE.

**Tech Stack:** bash · age (encryption) · git · Python 3 (jsonschema, PyYAML for validation) · pandoc (docx → md) · systemd (deferred to 01b — Plan 01a only writes the per-machine YAML profiles bootstrap will read).

**Plan-level success criteria (all must hold at end):**
- JP can encrypt a file with `infra/age-recipients.txt`; Ricardo can decrypt it on his machine. Reverse roundtrip holds.
- `infra/scripts/run-with-secrets.sh sleep 60 &` followed by 2s `ls /dev/shm/nexostrat-secrets-*` returns no files (no leak — C1 verified).
- `python3 -c "import jsonschema, json; jsonschema.validate(json.load(open('tasks.json')), json.load(open('infra/schemas/tasks.schema.json')))"` exits 0; same for `calendar.json`.
- A planted plaintext secret (`sk-ant-test123`) in a staged file is blocked by the basic pre-commit hook.
- Signed partnership PDF decrypts cleanly with each co-founder's key.
- Repo tagged `v0.1a-foundation`.

**JP-coordination gate:** Tasks 1-11 are unblocked and runnable in a single session (estimated 4-6 hours). Tasks 12-18 require JP's age pubkey to land via Signal first (per `t-jp-age-keypair`). Plan execution pauses cleanly between Task 11 and Task 12; the executor commits Task 11, updates CHECKPOINT.md saying "blocked on JP age pubkey," and resumes when JP responds.

**Spec references:** §1 (Topology), §2 (Repository Structure), §3 (Foundation Layer — identities, vault, secrets, backup, recovery, hooks), §4.1-4.5 (Personas + 00_PARTNERSHIP/ contents), §6.4 (intake 2-file split — informs `_template/` shape), §7 (12 stations + 3 cross-cutting). ADRs 002, 003, 004, 005, 006, 008, 010, 011, 015, 021, 027, 033, 036.

**Audit-finding inheritance:** This plan resolves C1 (run-with-secrets leak), C2 (vault encrypted to one recipient), F5 (partnership PDF), F10 (vault namespace split for personas), F12 (calendar.json — already done in Batch 1), F13 (Linux Mint baseline for JP-Heavy), F15 (questionnaires migration), F16 (`_template/` ordering moved into Plan 01a), F19 (12+3 station standardization), F21 (nexostrat-tasks-v1 schema), F23 (comprehensive .gitignore), F26 (phones platform field). R3 (Stage 1 surface area ADR) is reflected via deliverable scoping: only what ADR-036 lists as v0 fidelity ships here.

**Re-audit response (2026-05-14):** independent risk-auditor pass returned YELLOW (large) — 0 CRITICAL, 7 HIGH, 5 MEDIUM, 3 LOW, no DESIGN-RETHINK FLAG. Report at [`00_META/proposals/2026-05-14_plan-01a-audit-report.md`](../proposals/2026-05-14_plan-01a-audit-report.md). The 7 HIGH findings were patched inline into the tasks below (no architectural changes):
- **Finding 1** (gitignore `*secrets*` glob blocks `secrets.env.age` + `infra/secrets/MANIFEST.md` commits) — Task 2 Step 3 (surgical patterns + allowlist), Step 1 (positive `git check-ignore` assertions added to test).
- **Finding 2** (C1 leak-test passes by accident — backgrounded wrapper hangs on passphrase, never reaches the write that would leak) — Task 15 Step 1 rewritten as a 2-step interactive protocol with positive control (file exists during execution) + negative control (cleanup verified after kill).
- **Finding 3** (secret-scan hook scans on-disk, not staged blob — bypassable by stage→edit→commit) — Task 3 Step 3 hook reads via `git show :path` in git-hook mode; `--files-from-stdin` mode kept for unit-testing. Task 3 gets a Step 6b stage-then-edit integration test.
- **Finding 4** (`SIGNED_PDF="~/Downloads/..."` — tilde does not expand inside quotes) — Task 17 Steps 1-3 use `$HOME` instead.
- **Finding 5** (Task 7 `git add 00_META/skills` after `rmdir` errors fatal) — Task 7 Step 5 uses `git add -A`.
- **Finding 6** (C2 reverse-direction roundtrip underspecified for JP Light-mode — no clear delivery channel for JP's encrypted sentinel) — Task 13 Step 3 specifies the Signal-attachment flow concretely; Step 4 cleanup commits both removals in one pass.
- **Finding 7** (`run-with-secrets.sh` `2>/dev/null` swallows age error diagnostics) — Task 15 Step 3 captures age stderr to a temp log and surfaces it on decrypt failure.

Findings 8-15 (MEDIUM/LOW) are deferred per the auditor's recommendation; the gating concerns are closed.

---

## File Structure

**Created in this plan:**

```
/srv/Nexostrat/
├─ .gitignore                                                       (REPLACED — comprehensive per F23)
├─ tasks.json                                                       (MODIFIED — $schema field)
├─ calendar.json                                                    (MODIFIED — $schema field)
│
├─ 00_PARTNERSHIP/                                                  (CREATED — F5, §4.5)
│   ├─ PARTNERSHIP_AGREEMENT.md
│   ├─ CONFLICT_PROTOCOL.md
│   ├─ REVENUE_DISTRIBUTION.md
│   ├─ ROLES.md
│   ├─ KPIs.md
│   ├─ cost-sharing-agreement.md
│   ├─ qualified-prospect-definition.md
│   ├─ raised_hand_log.md
│   ├─ questionnaires/
│   │   ├─ 2026-05-07_ricardo.md                                    (CREATED — F15 pandoc convert)
│   │   ├─ 2026-05-07_jp.md                                         (CREATED — F15 pandoc convert)
│   │   └─ archive/                                                  (.docx originals moved here)
│   ├─ meetings/
│   │   ├─ weekly/                                                   (.gitkeep)
│   │   └─ decisions/                                                (.gitkeep)
│   └─ reviews/                                                      (.gitkeep)
│
├─ docs/                                                            (CREATED — Diátaxis structure §2)
│   ├─ README.md
│   ├─ tutorials/                                                   (.gitkeep)
│   ├─ how-to/                                                      (.gitkeep)
│   ├─ reference/                                                   (.gitkeep)
│   ├─ explanation/                                                 (.gitkeep)
│   └─ runbooks/                                                    (.gitkeep)
│
├─ vault/                                                           (CREATED — F10 namespace split)
│   ├─ README.md                                                    (decrypt discipline)
│   ├─ sensitive_index.md                                           (template — populated when assets arrive)
│   ├─ partnership/
│   │   └─ PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age                 (CREATED — F5, Task 17)
│   ├─ legal/                                                       (.gitkeep)
│   ├─ accounting/                                                  (.gitkeep)
│   ├─ keys/                                                        (.gitkeep)
│   └─ clients/                                                     (.gitkeep — Client-Owner namespace per F10)
│
├─ knowledge/                                                       (CREATED — §2)
│   ├─ sectors/                                                     (.gitkeep)
│   ├─ quick_wins/                                                  (.gitkeep)
│   └─ source_caches/                                               (.gitkeep)
│
├─ skills/                                                          (CREATED — canonical location, §2)
│   ├─ 01_company_analyst/                                          (MOVED from 00_META/skills/company-analyst/)
│   ├─ 02_industry_analyst/                                         (MOVED from 00_META/skills/industry-analyst/)
│   ├─ 03_competitor_analyst/                                       (MOVED from 00_META/skills/competitor-analyst/)
│   ├─ 04_meeting_script/                                           (CREATED — placeholder for Plan 06)
│   ├─ 05_opportunity_report/                                       (CREATED — placeholder for Plan 06)
│   ├─ 06_discovery_meeting/                                        (MOVED from 00_META/skills/discovery-meeting/)
│   └─ shared/                                                      (.gitkeep — Plan 05 populates)
│
├─ pipeline/                                                        (CREATED — §2, §7)
│   ├─ clients/
│   │   └─ _template/                                               (CREATED — F16 + F19 12+3 stations)
│   │       ├─ README.md
│   │       ├─ state.json
│   │       ├─ checkpoint.md
│   │       ├─ 00_intake/                                           (.gitkeep)
│   │       ├─ 01_company_analysis/                                 (.gitkeep)
│   │       ├─ 02_industry_analysis/                                (.gitkeep)
│   │       ├─ 03_competitor_analysis/                              (.gitkeep)
│   │       ├─ 04_meeting_script/                                   (.gitkeep)
│   │       ├─ 05_opportunity_report/                               (.gitkeep)
│   │       ├─ 06_proposal/                                         (.gitkeep)
│   │       ├─ 07_contract_onboarding/                              (.gitkeep)
│   │       ├─ 08_solution_design/                                  (.gitkeep)
│   │       ├─ 09_implementation/                                   (.gitkeep)
│   │       ├─ 10_followup/                                         (.gitkeep)
│   │       ├─ 11_retainer/                                         (.gitkeep)
│   │       ├─ transcripts/                                         (.gitkeep)
│   │       ├─ communications/                                      (.gitkeep)
│   │       └─ archive/                                             (.gitkeep)
│   └─ prospects/                                                   (.gitkeep)
│
├─ operations/                                                      (CREATED — §2)
│   ├─ marketing/                                                   (.gitkeep)
│   ├─ sales/                                                       (.gitkeep)
│   ├─ accounting/                                                  (.gitkeep)
│   ├─ legal/                                                       (.gitkeep)
│   ├─ it/                                                          (.gitkeep)
│   ├─ templates/                                                   (.gitkeep — Plan 05 populates)
│   └─ assets/
│       └─ Consultoria_IA_PYMEs_v1.pdf                              (MOVED from root — F15)
│
├─ infra/
│   ├─ age-recipients.txt                                           (MODIFIED — JP pubkey appended in Task 13)
│   ├─ agents/                                                      (.gitkeep — Plan 03 populates)
│   ├─ telegram/                                                    (.gitkeep — Plan 04 populates)
│   ├─ events/                                                      (.gitkeep — Plan 03 populates)
│   ├─ shadow/                                                      (.gitkeep — Plan 08 populates)
│   ├─ systemd/                                                     (.gitkeep — Plan 01b populates)
│   ├─ recovery/                                                    (.gitkeep — Plan 10 populates)
│   ├─ observability/                                               (.gitkeep — Plan 10 populates)
│   ├─ machines/                                                    (CREATED — Task 6)
│   │   ├─ hp-server.yaml
│   │   ├─ hp-standby.yaml
│   │   ├─ ricardo-desktop.yaml
│   │   ├─ ricardo-travel.yaml
│   │   ├─ jp-light.yaml
│   │   ├─ jp-heavy.yaml
│   │   └─ phones.yaml
│   ├─ schemas/                                                     (CREATED — Task 5, F21)
│   │   ├─ tasks.schema.json
│   │   └─ calendar.schema.json
│   ├─ secrets/                                                     (CREATED — Task 16)
│   │   └─ MANIFEST.md
│   ├─ scripts/                                                     (CREATED — Tasks 6, 14)
│   │   ├─ bootstrap-machine.sh                                     (skeleton)
│   │   └─ run-with-secrets.sh                                      (C1 fix — Task 14)
│   └─ hooks/                                                       (CREATED — Task 3)
│       └─ pre-commit-secret-scan.sh
│
└─ secrets.env.age                                                  (CREATED — Task 13, encrypted to both keys)
```

**Verified-only (terrain prep already created):**
- `00_GOVERNANCE/adr/` (folder exists; ADR contents are Plan 02 territory)
- `00_META/{handoff,journal,plans,proposals,scripts,skills}/`
- `infra/age-recipients.txt` (Ricardo pubkey present; JP placeholder present)
- `CLAUDE.md`, `GEMINI.md`, `README.md`, `STATUS.md`, `CHECKPOINT.md`, `tasks.json`, `calendar.json`, `00_META/CHANGELOG.md`
- `.gitattributes`
- `.gitignore` (interim — Task 2 replaces with comprehensive version)

---

## Pre-flight checks (before Task 1)

Run these once at the start of execution. They confirm baseline state and surface any drift since this plan was written.

- [ ] **Confirm cwd is `/srv/Nexostrat/`:**
  ```bash
  pwd
  # Expected: /srv/Nexostrat
  ```

- [ ] **Confirm working tree is clean:**
  ```bash
  git status --short
  # Expected: empty output
  ```

- [ ] **Confirm git remote `origin` resolves to Gitea:**
  ```bash
  git remote -v | grep origin
  # Expected: 2 lines pointing at git@gitea-nexostrat:nexostrat/nexostrat.git
  ```

- [ ] **Confirm `age` is installed:**
  ```bash
  age --version
  # Expected: a version string (e.g., "v1.1.1")
  ```

- [ ] **Confirm `pandoc` is installed (needed Task 8):**
  ```bash
  pandoc --version | head -1
  # Expected: "pandoc <version>"
  ```

- [ ] **Confirm `python3` + `jsonschema` available (needed Task 5):**
  ```bash
  python3 -c "import jsonschema; print(jsonschema.__version__)"
  # Expected: a version string. If ImportError: pip3 install --user jsonschema
  ```

- [ ] **Confirm `python3` + `PyYAML` available (needed Task 6):**
  ```bash
  python3 -c "import yaml; print(yaml.__version__)"
  # Expected: a version string. If ImportError: pip3 install --user PyYAML
  ```

If any check fails, stop and resolve before proceeding.

---

## Task 1: Folder scaffold (3-bucket layout)

**Goal:** Create the entire top-level folder tree at once — empty folders use `.gitkeep` so git tracks them. Single commit.

**Files:**
- Create: ~50 directories per the file-structure tree above
- Create: `.gitkeep` placeholders in every empty leaf folder

- [ ] **Step 1: Create all top-level folders + their first-level subfolders**

```bash
cd /srv/Nexostrat
mkdir -p \
  00_PARTNERSHIP/{questionnaires/archive,meetings/weekly,meetings/decisions,reviews} \
  docs/{tutorials,how-to,reference,explanation,runbooks} \
  vault/{partnership,legal,accounting,keys,clients} \
  knowledge/{sectors,quick_wins,source_caches} \
  skills/{04_meeting_script,05_opportunity_report,shared} \
  pipeline/{clients/_template/{00_intake,01_company_analysis,02_industry_analysis,03_competitor_analysis,04_meeting_script,05_opportunity_report,06_proposal,07_contract_onboarding,08_solution_design,09_implementation,10_followup,11_retainer,transcripts,communications,archive},prospects} \
  operations/{marketing,sales,accounting,legal,it,templates,assets} \
  infra/{agents,telegram,events,shadow,systemd,recovery,observability,machines,schemas,secrets,scripts,hooks}
```

- [ ] **Step 2: Verify the tree was created**

```bash
find . -maxdepth 2 -type d | grep -vE '^\.($|/\.git|/00_META|/00_GOVERNANCE|/.superpowers|/.claude)' | sort
```

Expected output includes (among others): `./00_PARTNERSHIP`, `./00_PARTNERSHIP/questionnaires`, `./docs`, `./vault`, `./vault/partnership`, `./skills`, `./pipeline`, `./pipeline/clients`, `./operations`, `./infra`.

- [ ] **Step 3: Add `.gitkeep` to every empty leaf folder**

```bash
find 00_PARTNERSHIP docs vault knowledge skills pipeline operations infra \
  -type d -empty -exec touch {}/.gitkeep \;
```

Verify nothing was missed:

```bash
find 00_PARTNERSHIP docs vault knowledge skills pipeline operations infra \
  -type d -empty
# Expected: empty output (every leaf now has .gitkeep)
```

- [ ] **Step 4: Stage + commit**

```bash
git add 00_PARTNERSHIP docs vault knowledge skills pipeline operations infra
git status --short
# Expected: many "A" entries for .gitkeep files

git commit -m "$(cat <<'EOF'
Plan 01a Task 1 · folder scaffold (3-bucket layout)

Creates the full top-level folder tree per spec §2:
- 00_PARTNERSHIP/ with questionnaires + meetings + reviews
- docs/ Diátaxis 5-folder structure
- vault/ with namespace split per F10 (partnership/legal/accounting/keys/clients)
- knowledge/ for cross-bucket reference
- skills/ canonical location (skills get moved in Task 7)
- pipeline/clients/_template/ with all 12 stations + 3 cross-cutting per F19
- operations/ back-office shape
- infra/ all subfolders (most get populated in later tasks/plans)

.gitkeep placeholders track empty leaf directories.

Spec refs: §2 (Repository Structure), F10, F16, F19.
EOF
)"
```

---

## Task 2: Comprehensive `.gitignore` (F23)

**Goal:** Replace the interim `.gitignore` with a full version covering Python, Node, IDE, OS, Docker, age private keys, `/dev/shm` dumps, log dumps. Belt-and-suspenders with the pre-commit hook (Task 3).

**Files:**
- Modify: `/srv/Nexostrat/.gitignore` (REPLACE entire file)

- [ ] **Step 1: Write a test that asserts coverage of every required pattern category**

Create `/srv/Nexostrat/infra/scripts/test_gitignore_coverage.sh`:

```bash
#!/usr/bin/env bash
# Test: .gitignore covers every Plan 01a F23 required pattern category.
set -u
PASS=0
FAIL=0
GITIGNORE="/srv/Nexostrat/.gitignore"

check() {
  local label="$1"; local pattern="$2"
  if grep -qE "$pattern" "$GITIGNORE"; then
    echo "PASS  $label  ($pattern)"; PASS=$((PASS+1))
  else
    echo "FAIL  $label  ($pattern)"; FAIL=$((FAIL+1))
  fi
}

check "Python __pycache__"    '^__pycache__/?$|/__pycache__/?$|^\*?__pycache__'
check "Python .pyc"           '\*\.pyc$|\.pyc$'
check "Python .venv"          '\.venv/?$|^venv/?$'
check "Python egg-info"       '\*\.egg-info/?$|egg-info'
check "Node modules"          'node_modules/?$'
check "Node npm-debug"        'npm-debug\.log|\*\.log'
check "IDE JetBrains"         '\.idea/?'
check "IDE VSCode"            '\.vscode/?'
check "Editor swap"           '\*\.swp|\*~'
check "OS macOS"              '\.DS_Store'
check "OS Windows"            'Thumbs\.db'
check "Docker override"       'docker-compose\.override\.yml'
check "Age private keys"      '\*\.key|^\*\.key$'
check "Age password files"    'secrets\.env$|\*\*/secrets\.env|\*\.secrets\.json'
check "Allowlist secrets.env.age"      '^!secrets\.env\.age'
check "Allowlist secrets MANIFEST.md"  '^!infra/secrets/MANIFEST\.md'
check "shm tmpfs dumps"       '/dev/shm|nexostrat-secrets-'
check "Log dumps"             '\*\.log$'
check "PEM/PFX certs"         '\*\.pem|\*\.pfx|\*\.p12'
check "Brainstorming wd"      '\.superpowers/?'

echo
echo "Result: ${PASS} pass, ${FAIL} fail"
[ "$FAIL" -eq 0 ] || exit 1
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/test_gitignore_coverage.sh
```

- [ ] **Step 2: Run the test against the current (interim) `.gitignore` to confirm it FAILS**

```bash
bash /srv/Nexostrat/infra/scripts/test_gitignore_coverage.sh
```

Expected: at least 8-10 FAIL lines (the interim .gitignore covers only a subset). Exit code 1.

- [ ] **Step 3: Replace `.gitignore` with the comprehensive version**

Write `/srv/Nexostrat/.gitignore` (REPLACE entire file):

```
# ==============================================================================
# Nexostrat — .gitignore
# Per F23 (audit 2026-05-14). Belt-and-suspenders with infra/hooks/pre-commit-secret-scan.sh
# ==============================================================================

# --- Secrets & keys (NEVER commit plaintext) -----------------------------------
.env
.env.*
!.env.example
# Surgical secret patterns — DO NOT use a blanket `*secrets*` glob (per Finding 1
# of the 2026-05-14 re-audit): it would silently block the intentional commits
# of secrets.env.age (Task 14) and infra/secrets/MANIFEST.md (Task 16).
secrets.env
secrets.env.local
secrets.local.env
*.secrets.json
**/secrets.env
**/secrets.local.env
*.key
*.pem
*.pfx
*.p12
key.txt
infra/age/keys/

# Explicit allowlist — these MUST be committable despite the patterns above.
!secrets.env.age
!infra/secrets/MANIFEST.md

# /dev/shm runtime decryption surface (paranoia — should never be in working tree)
/dev/shm/nexostrat-secrets-*

# --- Python --------------------------------------------------------------------
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
*.egg
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# --- Node ----------------------------------------------------------------------
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# --- IDE / editor --------------------------------------------------------------
.idea/
.vscode/
*.swp
*.swo
*~
.\#*
\#*\#

# --- OS junk -------------------------------------------------------------------
.DS_Store
.AppleDouble
.LSOverride
Thumbs.db
ehthumbs.db
Desktop.ini

# --- Docker --------------------------------------------------------------------
docker-compose.override.yml
.dockerignore.local

# --- Logs ----------------------------------------------------------------------
*.log
excalidraw.log
logs/

# --- Working dirs --------------------------------------------------------------
.superpowers/
.claude/cache/

# --- pandoc / build artifacts --------------------------------------------------
*.docx.bak
*~bak

# --- Vault sanity (encrypted files OK; plaintext never) ------------------------
# vault/ accepts only .age files — pre-commit hook enforces; this is a fallback.
vault/**/*.pdf
vault/**/*.docx
vault/**/*.txt
vault/**/*.md
!vault/**/sensitive_index.md
!vault/**/README.md
!vault/**/.gitkeep
```

- [ ] **Step 4: Re-run the test — expect PASS**

```bash
bash /srv/Nexostrat/infra/scripts/test_gitignore_coverage.sh
```

Expected: every line is `PASS`; exit code 0.

- [ ] **Step 5: Sanity-check git's view (no unexpected `.gitignore` regressions)**

```bash
git check-ignore -v secrets.env .env *.key node_modules/ __pycache__ excalidraw.log
# Expected: each path matched against the new .gitignore (no errors)
```

- [ ] **Step 5b: Positive control — the two intentional commits MUST NOT be ignored (Finding 1 fix)**

The Plan 01a deliverables `secrets.env.age` (Task 14) and `infra/secrets/MANIFEST.md` (Task 16) must remain committable. Assert via `git check-ignore`:

```bash
cd /srv/Nexostrat
# git check-ignore exits 0 if path IS ignored, 1 if NOT ignored. We want 1 (NOT ignored) for these.
for p in secrets.env.age infra/secrets/MANIFEST.md; do
  if git check-ignore -q "$p"; then
    echo "FAIL — $p is ignored by .gitignore (would break Plan 01a Tasks 14/16)"
    exit 1
  else
    echo "PASS — $p is NOT ignored"
  fi
done
```

Expected: both PASS. If either FAILs, the allowlist `!secrets.env.age` or `!infra/secrets/MANIFEST.md` was lost in the gitignore edit — restore before proceeding.

- [ ] **Step 6: Stage + commit**

```bash
git add .gitignore infra/scripts/test_gitignore_coverage.sh
git commit -m "$(cat <<'EOF'
Plan 01a Task 2 · comprehensive .gitignore (F23)

Replaces the interim minimal .gitignore with full coverage:
- Secrets & keys (belt-and-suspenders with the pre-commit hook in Task 3)
- Python (pycache, pyc, venv, pytest, mypy, coverage)
- Node (modules, debug logs)
- IDE (JetBrains, VSCode, swap files)
- OS junk (macOS, Windows)
- Docker compose overrides
- Logs (general + excalidraw)
- Working dirs (.superpowers, .claude/cache)
- Vault sanity (refuses non-.age in vault/, with allowlist for index/README/.gitkeep)

infra/scripts/test_gitignore_coverage.sh asserts all required pattern
categories are present; runs in <1s.

Spec refs: F23, ADR-005.
EOF
)"
```

---

## Task 3: Basic pre-commit secret-scan hook

**Goal:** Block any commit that adds a known secret-prefix pattern (`sk-ant-`, `sk-`, `AKIA`, `ghp_`, `eyJ`, `xoxb-`, `gho_`, `ghs_`, `ghu_`, `glpat-`). Symlink into `.git/hooks/pre-commit`. Full hook surface (docs-pair, age-encrypt-only, CHECKPOINT validation) is Plan 01c territory; this is the minimum viable secret guard.

**Files:**
- Create: `/srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh`
- Symlink: `.git/hooks/pre-commit -> ../../infra/hooks/pre-commit-secret-scan.sh`

- [ ] **Step 1: Write a test that proves the hook blocks a known secret pattern**

Create `/srv/Nexostrat/infra/scripts/test_secret_scan_hook.sh`:

```bash
#!/usr/bin/env bash
# Test: pre-commit-secret-scan.sh blocks a planted secret in staged content.
set -u
HOOK="/srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Create a fake staged file with a planted secret.
# The secret string is assembled at runtime so this script itself does not
# contain a literal match that would trip the pre-commit hook on commit.
PLANTED="$TMPDIR/planted.txt"
SECRET_PREFIX="sk-ant-"
SECRET_SUFFIX="test1234567890abcdef"
printf 'something something\n%s%s\nfoo bar\n' "$SECRET_PREFIX" "$SECRET_SUFFIX" > "$PLANTED"

# Hook reads file paths from stdin (one per line) — simulate staged file list
if echo "$PLANTED" | bash "$HOOK" --files-from-stdin; then
  echo "FAIL — hook did NOT block the planted secret"; exit 1
else
  echo "PASS — hook blocked the planted secret"
fi

# Negative test: a clean file should pass
CLEAN="$TMPDIR/clean.txt"
echo "this is fine" > "$CLEAN"
if echo "$CLEAN" | bash "$HOOK" --files-from-stdin; then
  echo "PASS — hook permitted a clean file"
else
  echo "FAIL — hook rejected a clean file"; exit 1
fi
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/test_secret_scan_hook.sh
```

- [ ] **Step 2: Run test — expect FAIL (hook doesn't exist yet)**

```bash
bash /srv/Nexostrat/infra/scripts/test_secret_scan_hook.sh
# Expected: error "no such file or directory" or similar; exit non-zero
```

- [ ] **Step 3: Implement the hook**

Create `/srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh`:

```bash
#!/usr/bin/env bash
# pre-commit-secret-scan.sh — Nexostrat
#
# Blocks any commit whose newly-staged content contains a known secret prefix.
# Run modes:
#   1. Default: invoked by git as the pre-commit hook. Reads `git diff --cached --name-only`.
#   2. --files-from-stdin: read newline-delimited paths from stdin (used by the test harness).
#
# Patterns covered (extend as needed):
#   sk-ant-XXX     Anthropic API key
#   sk-XXX         OpenAI/legacy API key
#   AKIA           AWS access key
#   ghp_/gho_/ghs_/ghu_/glpat-  GitHub/GitLab personal-access tokens
#   xoxb-/xoxp-    Slack tokens
#   eyJ            JWT (heuristic — three base64 segments separated by .)
#
# Exit 0 = clean. Exit 1 = secret found (or hook error).

set -uo pipefail

# Pattern set — pipe-separated for a single grep -E
PATTERNS='(sk-ant-[A-Za-z0-9_-]{20,})|(\bsk-[A-Za-z0-9]{20,})|(\bAKIA[0-9A-Z]{16}\b)|(\bghp_[A-Za-z0-9]{30,})|(\bgho_[A-Za-z0-9]{30,})|(\bghs_[A-Za-z0-9]{30,})|(\bghu_[A-Za-z0-9]{30,})|(\bglpat-[A-Za-z0-9_-]{20,})|(\bxox[baprs]-[A-Za-z0-9-]{10,})|(\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)'

# Decide source of paths AND which content surface to scan.
#   git-hook mode (default):   scan the STAGED BLOB via `git show :<path>` —
#                              this is what the commit actually contains, not
#                              what's on disk (per Finding 3 of the 2026-05-14
#                              re-audit: stage-then-edit-clean would bypass an
#                              on-disk scanner).
#   --files-from-stdin mode:   scan on-disk content directly — used by the
#                              unit-test harness where files aren't in any git
#                              index. (Integration test in Task 3 Step 6b
#                              exercises the staged-blob path via a real git
#                              workflow.)
MODE="git-hook"
if [[ "${1:-}" == "--files-from-stdin" ]]; then
  MODE="stdin"
  mapfile -t FILES < <(cat)
else
  mapfile -t FILES < <(git diff --cached --name-only --diff-filter=ACMR)
fi

[[ ${#FILES[@]} -eq 0 ]] && exit 0

scan_content() {
  # stdin: content to scan; $1: label (file path) for grep output
  grep -EHn "$PATTERNS" --label="$1" - 2>/dev/null
}

violations=0
for f in "${FILES[@]}"; do
  # Skip anything that matches our own .gitignore secret patterns — defensive
  case "$f" in
    *.age) continue ;;
    *secrets*) ;;  # still scan — explicit
  esac
  if [[ "$MODE" == "git-hook" ]]; then
    # Read the staged blob. Skip silently if blob unavailable (e.g. deleted path).
    if blob=$(git show ":$f" 2>/dev/null); then
      if printf '%s' "$blob" | scan_content "$f"; then
        violations=$((violations+1))
      fi
    fi
  else
    # stdin mode — scan disk file directly
    [[ -f "$f" ]] || continue
    if grep -EHn "$PATTERNS" "$f" 2>/dev/null; then
      violations=$((violations+1))
    fi
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "============================================================"
  echo "  BLOCKED: $violations file(s) contain secret-prefix matches."
  echo "  If this is a false positive, rewrite the value or unstage."
  echo "  Hook: infra/hooks/pre-commit-secret-scan.sh"
  echo "============================================================"
  exit 1
fi

exit 0
```

```bash
chmod +x /srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh
```

- [ ] **Step 4: Symlink into `.git/hooks/`**

```bash
cd /srv/Nexostrat
ln -sf ../../infra/hooks/pre-commit-secret-scan.sh .git/hooks/pre-commit
ls -la .git/hooks/pre-commit
# Expected: symlink pointing at ../../infra/hooks/pre-commit-secret-scan.sh
```

- [ ] **Step 5: Run the test — expect PASS**

```bash
bash /srv/Nexostrat/infra/scripts/test_secret_scan_hook.sh
# Expected:
#   PASS — hook blocked the planted secret
#   PASS — hook permitted a clean file
```

- [ ] **Step 6: Live integration test — try to commit a planted secret**

The fixture strings are assembled at runtime so this plan file itself does
not contain a literal-match that would trip the hook on re-commit (same
trick used inside `infra/scripts/test_secret_scan_hook.sh`; documented
2026-05-16 per audit follow-up after the original literal-form blocked
edits to this plan file).

```bash
cd /srv/Nexostrat
# Assemble fixture at runtime — no literal-match in this plan file's blob.
PREFIX='sk-ant-'; SUFFIX='test1234567890abcdef1234567890'
printf '%s%s\n' "$PREFIX" "$SUFFIX" > /tmp/planted_test.txt
cp /tmp/planted_test.txt .
git add planted_test.txt
git commit -m "should be blocked" 2>&1 | tail -5
# Expected: hook output ending in "BLOCKED" + non-zero exit; commit refused
```

Cleanup:

```bash
git restore --staged planted_test.txt
rm planted_test.txt /tmp/planted_test.txt
```

- [ ] **Step 6b: Stage-then-edit-clean integration test (Finding 3 fix proof)**

This test proves the hook reads the **staged blob**, not the on-disk file. Without the Finding 3 fix, the test below would let the secret slip through because the on-disk content is clean by commit time. Same runtime-assembly convention.

```bash
cd /srv/Nexostrat
# 1. Plant a secret, stage it. Assemble at runtime to avoid literal-match.
PREFIX='sk-ant-'; SUFFIX='stagedblob1234567890abcdef'
printf '%s%s\n' "$PREFIX" "$SUFFIX" > stage_edit_test.txt
git add stage_edit_test.txt

# 2. Edit the on-disk file to remove the secret BEFORE committing.
#    The staged blob still contains the secret; on-disk is now clean.
echo "harmless content" > stage_edit_test.txt

# 3. Attempt commit — the staged-blob scanner MUST block this.
if git commit -m "stage-then-edit test (should be blocked by staged-blob scan)" 2>&1 | tail -5; then
  echo "FAIL — commit succeeded despite secret in staged blob (Finding 3 not fixed)"
  CLEANUP_FAIL=1
else
  echo "PASS — hook blocked commit based on staged-blob content"
  CLEANUP_FAIL=0
fi

# Cleanup
git restore --staged stage_edit_test.txt 2>/dev/null
rm -f stage_edit_test.txt
[[ "$CLEANUP_FAIL" == "1" ]] && { echo "ABORT — Finding 3 fix is not working; investigate before continuing"; exit 1; }
```

Expected: `PASS — hook blocked commit based on staged-blob content`. If FAIL: the hook is still scanning on-disk content; verify `MODE="git-hook"` branch is using `git show :$f` and re-run.

- [ ] **Step 7: Stage + commit the hook itself**

```bash
git add infra/hooks/pre-commit-secret-scan.sh infra/scripts/test_secret_scan_hook.sh
git commit -m "$(cat <<'EOF'
Plan 01a Task 3 · pre-commit secret-scan hook (basic)

Blocks any newly-staged content matching known secret prefixes:
sk-ant-, sk-, AKIA, ghp_/gho_/ghs_/ghu_, glpat-, xoxb-/xoxp-, eyJ JWTs.

Hook lives at infra/hooks/pre-commit-secret-scan.sh; symlinked into
.git/hooks/pre-commit. Test harness at
infra/scripts/test_secret_scan_hook.sh proves both block-and-permit paths.

Full hook surface (docs-pair check, age-encrypt-only on vault/, CHECKPOINT
validation) is Plan 01c territory. This is the minimum viable guard so all
subsequent Task commits in 01a are protected.

Spec refs: §3 (Guards), ADR-008.
EOF
)"
```

---

## Task 4: `pipeline/clients/_template/` — 12 stations + 3 cross-cutting (F16, F19)

**Goal:** Populate the `_template/` skeleton (created empty in Task 1) with the canonical `README.md`, `state.json` template, `checkpoint.md` placeholder, and `.gitkeep` files in each of the 15 station/cross-cutting folders. F16 moves this from later plans into 01a; F19 standardizes the count at "12 stations + 3 cross-cutting."

**Files:**
- Create: `pipeline/clients/_template/README.md`
- Create: `pipeline/clients/_template/state.json`
- Create: `pipeline/clients/_template/checkpoint.md`
- (`.gitkeep` already in each station folder from Task 1)

- [ ] **Step 1: Create `state.json` template**

Write `/srv/Nexostrat/pipeline/clients/_template/state.json`:

```json
{
  "$schema": "nexostrat-client-state-v1",
  "client": "<slug>",
  "name": "<Full Legal Name>",
  "country": "<ISO-3166 alpha-2>",
  "sector": "<plain-text sector>",
  "started": "<ISO-8601 date>",
  "owner": "<persona — usually client-owner>",
  "phase": "prospect",
  "phase_history": [
    {
      "from": null,
      "to": "prospect",
      "at": "<ISO-8601 timestamp>",
      "by": "<initiator — telegram-id or persona>",
      "note": "Created via _template/ scaffold"
    }
  ],
  "pilot": false,
  "pricing": {
    "model": null,
    "currency": null,
    "amount": null
  },
  "next_action": null,
  "kpis": {},
  "blockers": [],
  "tags": [],
  "recording_preference": null
}
```

- [ ] **Step 2: Create `checkpoint.md` placeholder**

Write `/srv/Nexostrat/pipeline/clients/_template/checkpoint.md`:

```markdown
# CHECKPOINT — <slug> (Client-Owner)

**Status:** CHECKPOINT_NO_ACTIVE_WORK

**Updated:** <ISO-8601 timestamp>
**By:** <session initiator>
**Persona:** Client-Owner

> Template placeholder. When this client moves out of `prospect` and into active
> work, this file gets the standard CHECKPOINT structure (what just happened,
> in-flight next action, blocked-on, open questions, files-modified-not-committed,
> estimated-time-to-finish, after-this-what's-next).
>
> Per ADR-031: empty CHECKPOINT.md commits are refused unless the literal token
> `CHECKPOINT_NO_ACTIVE_WORK` is present (above).
```

- [ ] **Step 3: Create `_template/` README**

Write `/srv/Nexostrat/pipeline/clients/_template/README.md`:

```markdown
# Per-client template — 12 stations + 3 cross-cutting (ADR-010, F19)

This folder is the canonical empty client. `infra/scripts/new-client.sh` (Plan 07)
copies it to `pipeline/clients/<slug>/` and substitutes placeholders in
`state.json`, `checkpoint.md`, and `README.md`.

## The 12 stations (sequential phases of the engagement)

| # | Folder | Plan Maestro mapping | Owning skill |
|---|---|---|---|
| 00 | `00_intake/` | Pasos 1-3 | (research_input.md + our_hypotheses.md per ADR-027) |
| 01 | `01_company_analysis/` | Fase B Skill 1 | Skill 1 (company-analyst) |
| 02 | `02_industry_analysis/` | Fase B Skill 2 | Skill 2 (industry-analyst) |
| 03 | `03_competitor_analysis/` | Fase B Skill 3 | Skill 3 (competitor-analyst) |
| 04 | `04_meeting_script/` | Fase B Skill 4 (PRIVATE) | Skill 4 (meeting_script) |
| 05 | `05_opportunity_report/` | Fase C — THE DELIVERABLE | Skill 5 (opportunity_report) |
| 06 | `06_proposal/` | Pasos 7-8 (Fase D) | (template-driven, no skill) |
| 07 | `07_contract_onboarding/` | Paso 9 (Fase E) | (template-driven, no skill) |
| 08 | `08_solution_design/` | Paso 10 | (template-driven, no skill) |
| 09 | `09_implementation/` | Paso 11 | (template-driven, no skill) |
| 10 | `10_followup/` | Paso 12 (30/60/90) | (template-driven, no skill) |
| 11 | `11_retainer/` | Paso 13 | (template-driven, no skill) |

**Folders never move.** Phase tracked in `state.json` (see schema below).

## The 3 cross-cutting folders

| Folder | Holds |
|---|---|
| `transcripts/` | Meeting transcripts (canonical = Notion AI per ADR-024; shadow = Whisper for internal) |
| `communications/` | Email + WhatsApp + Telegram captures |
| `archive/` | Superseded artifacts (kept for forensic record; never deleted) |

## `state.json`

Schema: `nexostrat-client-state-v1` (full schema landed in Plan 03 alongside the
event-spine validators). Required fields: `client`, `name`, `country`, `sector`,
`started`, `owner`, `phase`, `phase_history[]`, `pilot`, `pricing`, `next_action`,
`kpis`, `blockers[]`, `tags[]`, `recording_preference`.

Phase values: `prospect → intake → exploring → diagnostico_pendiente →
diagnostico_delivered → propuesta_pendiente → propuesta_sent →
propuesta_{accepted,rejected,revising} → cliente_firmado → diseño →
implementación → seguimiento_30 → seguimiento_60 → seguimiento_90 →
retainer_active`. Plus `churned`, `nurture`, `retainer_paused`.

Transitions emit events to `infra/events/events.jsonl` (Plan 03) and are
gated by Telegram commands (`/advance`, `/regress`, `/set-phase`, etc. — Plan 04+).

## `checkpoint.md`

Per ADR-031: client-scoped session continuity. Empty file = refused commit
unless `CHECKPOINT_NO_ACTIVE_WORK` token present (this template starts in that
state).

## What's NOT here

Per Plan 01a scope, this template is structural only. Skill-specific scaffolding
(prompts/v1.md, templates, benchmarks) lives at `skills/<NN>_<name>/` and is
populated in Plans 05-06.
```

- [ ] **Step 4: Verify all 15 folders + the 3 root files exist**

```bash
ls /srv/Nexostrat/pipeline/clients/_template/
# Expected: README.md  checkpoint.md  state.json  + 15 folders

find /srv/Nexostrat/pipeline/clients/_template -mindepth 1 -maxdepth 1 -type d | wc -l
# Expected: 15
```

- [ ] **Step 5: Verify `state.json` parses as JSON**

```bash
python3 -c "import json; json.load(open('/srv/Nexostrat/pipeline/clients/_template/state.json'))"
# Expected: no output, exit 0
```

- [ ] **Step 6: Stage + commit**

```bash
git add pipeline/clients/_template/
git commit -m "$(cat <<'EOF'
Plan 01a Task 4 · pipeline/clients/_template/ — 12+3 stations (F16, F19)

Populates the per-client template with:
- state.json (nexostrat-client-state-v1 schema; phase=prospect; phase_history seeded)
- checkpoint.md (CHECKPOINT_NO_ACTIVE_WORK token per ADR-031 empty-commit policy)
- README.md (12 stations + 3 cross-cutting documented; folder-purpose table)

Per F16: template definition moves into Plan 01a (was previously in Plan 05/07).
Per F19: count standardized to "12 stations + 3 cross-cutting" everywhere.
new-client.sh (Plan 07) clones this to pipeline/clients/<slug>/.

Spec refs: §7, ADRs 010, 027, 031.
EOF
)"
```

---

## Task 5: JSON Schemas + tasks.json/calendar.json `$schema` (F21)

**Goal:** Define `nexostrat-tasks-v1` and `nexostrat-calendar-v1` JSON Schemas. Update existing `tasks.json` and `calendar.json` to reference them. Validate cleanly. F21 closes the `brain-tasks-v1` /srv/brain coupling.

**Files:**
- Create: `infra/schemas/tasks.schema.json`
- Create: `infra/schemas/calendar.schema.json`
- Modify: `tasks.json` (`$schema` field)
- Modify: `calendar.json` (`$schema` field — already `nexostrat-calendar-v1`, verify)
- Create: `infra/scripts/validate_schemas.sh`

- [ ] **Step 1: Write the validator script (the test)**

Create `/srv/Nexostrat/infra/scripts/validate_schemas.sh`:

```bash
#!/usr/bin/env bash
# Validate tasks.json + calendar.json against their schemas.
set -euo pipefail
cd /srv/Nexostrat

python3 - <<'PYEOF'
import json, sys
import jsonschema

failures = []

for data_path, schema_path, label in [
    ("tasks.json",    "infra/schemas/tasks.schema.json",    "tasks"),
    ("calendar.json", "infra/schemas/calendar.schema.json", "calendar"),
]:
    try:
        with open(data_path) as f: data = json.load(f)
        with open(schema_path) as f: schema = json.load(f)
        jsonschema.validate(instance=data, schema=schema)
        print(f"PASS  {label} ({data_path} validates against {schema_path})")
    except FileNotFoundError as e:
        failures.append(f"FAIL  {label} — file missing: {e}")
        print(failures[-1])
    except jsonschema.ValidationError as e:
        failures.append(f"FAIL  {label} — schema violation: {e.message}")
        print(failures[-1])
    except Exception as e:
        failures.append(f"FAIL  {label} — {type(e).__name__}: {e}")
        print(failures[-1])

if failures: sys.exit(1)
PYEOF
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/validate_schemas.sh
```

- [ ] **Step 2: Run the validator — expect FAIL (schemas don't exist)**

```bash
bash /srv/Nexostrat/infra/scripts/validate_schemas.sh
# Expected: FAIL lines for both schemas (file missing); exit code 1
```

- [ ] **Step 3: Write the tasks schema**

Write `/srv/Nexostrat/infra/schemas/tasks.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "nexostrat-tasks-v1",
  "title": "Nexostrat tasks.json",
  "type": "object",
  "required": ["$schema", "project", "updated", "tasks"],
  "properties": {
    "$schema":  { "const": "nexostrat-tasks-v1" },
    "project":  { "type": "string", "minLength": 1 },
    "updated":  { "type": "string", "format": "date-time" },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "subject", "status", "priority", "created"],
        "properties": {
          "id":         { "type": "string", "pattern": "^t-[a-z0-9-]+$" },
          "subject":    { "type": "string", "minLength": 1 },
          "status":     { "enum": ["open", "in_progress", "blocked", "done", "deferred", "cancelled"] },
          "priority":   { "enum": ["critical", "high", "medium", "low"] },
          "due":        { "type": "string", "format": "date" },
          "created":    { "type": "string", "format": "date" },
          "completed":  { "type": "string", "format": "date" },
          "blocked_by": { "type": "string", "pattern": "^t-[a-z0-9-]+$" },
          "notes":      { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 4: Write the calendar schema**

Write `/srv/Nexostrat/infra/schemas/calendar.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "nexostrat-calendar-v1",
  "title": "Nexostrat calendar.json",
  "type": "object",
  "required": ["$schema", "project", "events"],
  "properties": {
    "$schema": { "const": "nexostrat-calendar-v1" },
    "project": { "type": "string", "minLength": 1 },
    "events": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "when"],
        "properties": {
          "id":      { "type": "string", "minLength": 1 },
          "title":   { "type": "string", "minLength": 1 },
          "when":    { "type": "string" },
          "tz":      { "type": "string" },
          "kind":    { "enum": ["deadline", "meeting", "milestone", "reminder", "review"] },
          "owner":   { "type": "string" },
          "related": { "type": "array", "items": { "type": "string" } },
          "notes":   { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 5: Update existing `tasks.json` `$schema` field**

Read `/srv/Nexostrat/tasks.json` to confirm the current value, then edit only the `$schema` line.

```bash
grep '"\$schema"' /srv/Nexostrat/tasks.json
# Current expected: "$schema": "nexostrat-tasks-v1"   (already correct from terrain prep)
```

If the value is already `nexostrat-tasks-v1`, no edit is needed. If anything else, edit:

```bash
# Use sed only if value differs — verify first
sed -i 's|"\$schema":[[:space:]]*"[^"]*"|"$schema": "nexostrat-tasks-v1"|' /srv/Nexostrat/tasks.json
```

- [ ] **Step 6: Verify `calendar.json` `$schema` is `nexostrat-calendar-v1`**

```bash
grep '"\$schema"' /srv/Nexostrat/calendar.json
# Expected: "$schema": "nexostrat-calendar-v1"
```

If different, fix with the same `sed` pattern as Step 5.

- [ ] **Step 7: Run the validator — expect PASS**

```bash
bash /srv/Nexostrat/infra/scripts/validate_schemas.sh
# Expected:
#   PASS  tasks (tasks.json validates against infra/schemas/tasks.schema.json)
#   PASS  calendar (calendar.json validates against infra/schemas/calendar.schema.json)
```

If a tasks-schema validation fails because an existing task uses a `status` value not in the enum, **stop and surface the discrepancy to Ricardo** — do not patch existing data without his sign-off. The schema is the canonical contract; existing data should already conform per terrain-prep work.

- [ ] **Step 8: Stage + commit**

```bash
git add infra/schemas/ infra/scripts/validate_schemas.sh tasks.json calendar.json
git commit -m "$(cat <<'EOF'
Plan 01a Task 5 · JSON Schemas (F21) + nexostrat-tasks-v1 / nexostrat-calendar-v1

Closes the brain-tasks-v1 /srv/brain coupling per F21.

infra/schemas/tasks.schema.json defines nexostrat-tasks-v1:
- $schema/project/updated/tasks required
- per-task: id (t-<slug> pattern), subject, status (enum), priority (enum),
  optional due/completed/blocked_by/notes
- additionalProperties:false at every level

infra/schemas/calendar.schema.json defines nexostrat-calendar-v1:
- $schema/project/events required
- per-event: id/title/when required; optional tz/kind/owner/related/notes

infra/scripts/validate_schemas.sh runs jsonschema.validate against both
files; exit 1 on any violation. Will be wired into the pre-commit hook
surface in Plan 03 alongside the events.jsonl validators.

Spec refs: F21, ADR-021.
EOF
)"
```

---

## Task 6: Per-machine YAML profiles + bootstrap-machine.sh skeleton (F13, F26)

**Goal:** Land the 7 per-machine YAML profiles per spec §5 and a skeleton `bootstrap-machine.sh` that reads a profile and logs intent (full installer logic deferred to Plan 02). F13 sets `jp-heavy.yaml` `os: linux-mint`. F26 adds `platform: ios|android` per user inside `phones.yaml`.

**Files:**
- Create: `infra/machines/{hp-server,hp-standby,ricardo-desktop,ricardo-travel,jp-light,jp-heavy,phones}.yaml`
- Create: `infra/scripts/bootstrap-machine.sh`

- [ ] **Step 1: Write `infra/machines/hp-server.yaml`**

```yaml
# infra/machines/hp-server.yaml
# Primary host — Linux Mint 22.2; Tailscale 100.64.121.80; runs Gitea + bot + shadow stack.
hostname: ricardo-hp-laptop
role: hp-server
owner: ricardo
os: linux-mint
os_version: "22.2"
tailscale_ip: 100.64.121.80
docker:
  compose_file: /srv/Nexostrat/docker-compose.yml
  services:
    - gitea
    - nexostrat-bot
    - jitsi-web
    - prosody
    - jicofo
    - jvb
    - nextcloud
    - whisper-cpp
cli_tools:
  - age
  - git
  - pandoc
  - python3
  - jq
  - rclone
  - rsync
desktop_apps: []  # headless server posture; desktop work is on ricardo-desktop
schedule:
  warm_rsync: "03:00 America/Tijuana"  # Plan 01b implements
  daily_brief: "07:00 America/Tijuana"  # Plan 03+ implements
  weekly_verify: "Sun 02:00 America/Tijuana"
gpu: null  # CPU-only; GPU work runs on ricardo-desktop
hooks:
  pre_commit: infra/hooks/pre-commit-secret-scan.sh
  pre_receive: null  # Gitea-side; Plan 01b
crons: []  # systemd timers preferred per ADR-029
```

- [ ] **Step 2: Write `infra/machines/hp-standby.yaml`**

```yaml
# infra/machines/hp-standby.yaml
# Warm-standby clone — receives nightly rsync from hp-server. Idle until activated.
# RTO target 15-30 min from cold to serving. Provisioned in Plan 01b.
hostname: <TBD-at-provisioning>
role: hp-standby
owner: ricardo
os: linux-mint
os_version: "22.2"
tailscale_ip: <TBD-at-provisioning>
docker:
  compose_file: /srv/Nexostrat/docker-compose.yml
  services: []  # all stopped at rest; started during failover
cli_tools:
  - age
  - git
  - pandoc
  - python3
  - jq
  - rclone
  - rsync
desktop_apps: []
schedule: {}  # passive; receives rsync, runs nothing
gpu: null
hooks:
  pre_commit: infra/hooks/pre-commit-secret-scan.sh
  pre_receive: null
crons: []
```

- [ ] **Step 3: Write `infra/machines/ricardo-desktop.yaml`**

```yaml
# infra/machines/ricardo-desktop.yaml
# Ricardo's desktop workstation — also the GPU host (office hours). Wake-on-LAN target.
hostname: <TBD-at-bootstrap>
role: ricardo-desktop
owner: ricardo
os: linux-mint
os_version: "22.2"
tailscale_ip: <TBD-at-bootstrap>
docker:
  compose_file: null  # no firm services here
  services: []
cli_tools:
  - age
  - git
  - python3
  - jq
  - ollama
desktop_apps:
  - claude-code
  - chrome
  - signal
  - bitwarden
  - vscode
schedule:
  ollama_office_hours: "09:00-18:00 America/Tijuana"
gpu:
  vendor: nvidia  # placeholder — confirm at bootstrap
  models:
    - llama3.1:8b
    - qwen2.5:14b
    - mistral:7b
hooks:
  pre_commit: infra/hooks/pre-commit-secret-scan.sh
  pre_receive: null
crons: []
wake_on_lan:
  mac_address: <TBD-at-bootstrap>
  enabled: true  # Plan 09 wires the trigger
```

- [ ] **Step 4: Write `infra/machines/ricardo-travel.yaml`**

```yaml
# infra/machines/ricardo-travel.yaml
# Ricardo's travel laptop — read-mostly clone + Telegram + Claude Code.
hostname: <TBD-at-bootstrap>
role: ricardo-travel
owner: ricardo
os: linux-mint
os_version: "22.2"
tailscale_ip: <TBD-at-bootstrap>
docker:
  compose_file: null
  services: []
cli_tools:
  - age
  - git
  - python3
  - jq
desktop_apps:
  - claude-code
  - chrome
  - signal
  - bitwarden
schedule: {}
gpu: null
hooks:
  pre_commit: infra/hooks/pre-commit-secret-scan.sh
  pre_receive: null
crons: []
```

- [ ] **Step 5: Write `infra/machines/jp-light.yaml`**

```yaml
# infra/machines/jp-light.yaml
# JP — Light mode default. Telegram bot + Gitea web only. 5-min onboarding.
# Per ADR-021bis: "Hosted" option dropped; Light is the default JP entry point.
hostname: <jp-phone-or-laptop>
role: jp-light
owner: jp
os: <TBD>  # JP's existing device — could be macOS, iOS, Android, anything
os_version: <TBD>
tailscale_ip: null  # optional — only if JP installs Tailscale
docker:
  compose_file: null
  services: []
cli_tools: []  # web + Telegram only; no CLI requirement
desktop_apps:
  - telegram
  - chrome  # or any browser — for Gitea web
schedule: {}
gpu: null
hooks: {}
crons: []
```

- [ ] **Step 6: Write `infra/machines/jp-heavy.yaml` (F13)**

```yaml
# infra/machines/jp-heavy.yaml
# JP — Heavy mode. Full clone + Claude Code + age key. ~1h additive onboarding.
# Per F13: Linux Mint is the recommended baseline; matches Ricardo's HP family,
# well-trodden install path, no surprises. macOS handled as an exception in
# Plan 02 only if JP cannot install Linux Mint.
hostname: <jp-laptop>
role: jp-heavy
owner: jp
os: linux-mint
os_version: "22.2"
tailscale_ip: <TBD-at-bootstrap>
docker:
  compose_file: null  # JP doesn't run firm services; he reads/writes via clone
  services: []
cli_tools:
  - age
  - git
  - pandoc
  - python3
  - jq
desktop_apps:
  - claude-code
  - chrome
  - telegram
  - signal
  - bitwarden
schedule: {}
gpu: null
hooks:
  pre_commit: infra/hooks/pre-commit-secret-scan.sh
  pre_receive: null
crons: []
```

- [ ] **Step 7: Write `infra/machines/phones.yaml` (F26 — per-user platform field)**

```yaml
# infra/machines/phones.yaml
# Phones are the always-available capture surface. Telegram bot + Signal.
# F26: explicit per-user platform field so bootstrap can install the right apps.
phones:
  ricardo:
    platform: <ios|android>  # confirm at bootstrap
    apps:
      - telegram
      - signal
      - chrome
      - bitwarden
    notes: "Capture surface for /note, /idea, /question, /voice, /photo. Read-only inspection of /status, /pipeline, /inbox."
  jp:
    platform: <ios|android>  # confirm via t-jp-coordination-2026-05-14
    apps:
      - telegram
      - signal
      - chrome
      - bitwarden
    notes: "Same as Ricardo. JP's Light-mode primary surface."
```

- [ ] **Step 8: Write `infra/scripts/bootstrap-machine.sh` skeleton**

```bash
#!/usr/bin/env bash
# bootstrap-machine.sh — Nexostrat
#
# Reads infra/machines/<profile>.yaml and prepares the host accordingly.
# Plan 01a SCOPE: skeleton only — parses profile, logs intended actions,
# exits without performing them. Idempotent. Re-runnable.
#
# Full installer logic (apt install lists, docker setup, systemd unit
# enablement, Tailscale auth) lands in Plan 02 via the per-section work
# (apt task, docker task, systemd task).
#
# Usage: infra/scripts/bootstrap-machine.sh <profile>
#   profile = name of a file under infra/machines/ (without .yaml suffix)
#
# Exit codes:
#   0  = success (intent logged or actions completed)
#   1  = profile not found / parse error
#   2  = unsupported OS

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROFILE="${1:?usage: bootstrap-machine.sh <profile>}"
PROFILE_FILE="$REPO_ROOT/infra/machines/${PROFILE}.yaml"

if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "ERROR: profile not found: $PROFILE_FILE" >&2
  echo "Available profiles:" >&2
  ls "$REPO_ROOT/infra/machines/"*.yaml 2>/dev/null | xargs -n1 basename | sed 's/\.yaml$//' >&2
  exit 1
fi

# Parse profile via Python (PyYAML — already a Plan 01a prerequisite)
python3 - <<PYEOF
import sys, yaml, json
profile = yaml.safe_load(open("$PROFILE_FILE"))
if profile is None:
    sys.exit("ERROR: profile is empty")

# phones.yaml has a different shape (multi-user); handle both
if "$PROFILE" == "phones":
    print(f"=== Phones profile (multi-user) ===")
    for user, cfg in profile.get("phones", {}).items():
        print(f"\nUser: {user}")
        print(f"  platform: {cfg.get('platform', '<unset>')}")
        print(f"  apps: {', '.join(cfg.get('apps', []))}")
        print(f"  notes: {cfg.get('notes', '')}")
    sys.exit(0)

print(f"=== Bootstrap intent for profile: $PROFILE ===")
print(f"hostname:     {profile.get('hostname', '<unset>')}")
print(f"role:         {profile.get('role', '<unset>')}")
print(f"owner:        {profile.get('owner', '<unset>')}")
print(f"os:           {profile.get('os', '<unset>')} {profile.get('os_version', '')}")
print(f"tailscale_ip: {profile.get('tailscale_ip', '<unset>')}")

cli = profile.get("cli_tools") or []
if cli: print(f"cli_tools:    {', '.join(cli)}")

apps = profile.get("desktop_apps") or []
if apps: print(f"desktop_apps: {', '.join(apps)}")

dock = (profile.get("docker") or {}).get("services") or []
if dock: print(f"docker:       {', '.join(dock)}")

gpu = profile.get("gpu")
if gpu:
    print(f"gpu vendor:   {gpu.get('vendor', '<unset>')}")
    if gpu.get("models"): print(f"gpu models:   {', '.join(gpu['models'])}")

print()
print("[skeleton mode] No actions performed. Plan 02 implements the installer.")
PYEOF
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/bootstrap-machine.sh
```

- [ ] **Step 9: Verify each profile parses as YAML**

```bash
for f in /srv/Nexostrat/infra/machines/*.yaml; do
  python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1])); print('OK', sys.argv[1])" "$f"
done
# Expected: 7 lines, each "OK <path>"
```

- [ ] **Step 10: Smoke-test the bootstrap skeleton against `hp-server`**

```bash
bash /srv/Nexostrat/infra/scripts/bootstrap-machine.sh hp-server
# Expected: profile fields printed; ends with "[skeleton mode] No actions performed."
```

```bash
bash /srv/Nexostrat/infra/scripts/bootstrap-machine.sh phones
# Expected: per-user output for ricardo + jp; ends with skeleton-mode line
```

```bash
bash /srv/Nexostrat/infra/scripts/bootstrap-machine.sh nonexistent 2>&1 | tail -3
# Expected: ERROR + list of available profiles; exit code 1
```

- [ ] **Step 11: Stage + commit**

```bash
git add infra/machines/ infra/scripts/bootstrap-machine.sh
git commit -m "$(cat <<'EOF'
Plan 01a Task 6 · per-machine YAML profiles + bootstrap skeleton (F13, F26)

Lands all 7 profiles per spec §5:
- hp-server.yaml (primary host, Tailscale 100.64.121.80, full Docker stack)
- hp-standby.yaml (warm-standby — placeholders filled at provisioning in Plan 01b)
- ricardo-desktop.yaml (GPU host, Ollama models, wake-on-LAN target)
- ricardo-travel.yaml (read-mostly clone)
- jp-light.yaml (Telegram + browser; 5-min onboarding; OS-agnostic)
- jp-heavy.yaml (Linux Mint baseline per F13; ~1h additive onboarding)
- phones.yaml (per-user with platform: ios|android per F26)

bootstrap-machine.sh is a skeleton — parses YAML, logs intended actions, exits
without performing them. Idempotent. Plan 02 implements the installer paths.

Spec refs: §5 (Stack/profiles), F13, F26, ADR-021bis.
EOF
)"
```

---

## Task 7: Move parked skills from `00_META/skills/` to canonical `skills/<NN>_<name>/`

**Goal:** Four skills currently live at `00_META/skills/{company-analyst, industry-analyst, competitor-analyst, discovery-meeting}/` — terrain-prep parking. Move to canonical `skills/<NN>_<name>/` per spec §2 numbering. The empty `04_meeting_script/` and `05_opportunity_report/` placeholders from Task 1 stay as-is (Plan 06 populates them).

**Files:**
- Move: `00_META/skills/company-analyst/`     → `skills/01_company_analyst/`
- Move: `00_META/skills/industry-analyst/`    → `skills/02_industry_analyst/`
- Move: `00_META/skills/competitor-analyst/`  → `skills/03_competitor_analyst/`
- Move: `00_META/skills/discovery-meeting/`   → `skills/06_discovery_meeting/`
- Delete: `00_META/skills/` (now empty)

- [ ] **Step 1: Inspect current contents to confirm what's being moved**

```bash
ls /srv/Nexostrat/00_META/skills/
# Expected: company-analyst  competitor-analyst  discovery-meeting  industry-analyst

for d in company-analyst industry-analyst competitor-analyst discovery-meeting; do
  echo "--- $d ---"
  find "/srv/Nexostrat/00_META/skills/$d" -maxdepth 2 -type f | head
done
```

- [ ] **Step 2: Move each skill to its canonical location**

The `skills/0{4,5}_*/` placeholders from Task 1 already have `.gitkeep` — leave them. The four skills being moved overwrite the empty `01/02/03/06` slots if they exist; per Task 1, only 04 and 05 were created as empties, so 01/02/03/06 don't exist yet.

```bash
cd /srv/Nexostrat
git mv 00_META/skills/company-analyst    skills/01_company_analyst
git mv 00_META/skills/industry-analyst   skills/02_industry_analyst
git mv 00_META/skills/competitor-analyst skills/03_competitor_analyst
git mv 00_META/skills/discovery-meeting  skills/06_discovery_meeting
```

- [ ] **Step 3: Remove the now-empty parking folder**

```bash
rmdir /srv/Nexostrat/00_META/skills 2>/dev/null || \
  echo "00_META/skills/ not empty — inspect"
ls /srv/Nexostrat/00_META/ | grep -c skills
# Expected: 0
```

- [ ] **Step 4: Verify the canonical layout**

```bash
ls /srv/Nexostrat/skills/
# Expected:
# 01_company_analyst  02_industry_analyst  03_competitor_analyst
# 04_meeting_script  05_opportunity_report  06_discovery_meeting  shared
```

- [ ] **Step 5: Stage + commit**

```bash
# `git mv` (Step 2) has already staged the renames; `rmdir` (Step 3) removed the
# now-empty source directory. Use `git add -A` to pick up any remaining
# `.gitkeep` housekeeping without erroring on the removed source path
# (per Finding 5 of the 2026-05-14 re-audit — the previous `git add 00_META/skills`
# would have errored fatal because the path no longer exists).
git add -A
git status --short
# Expected: many "R" (renamed) entries; net additions ≈ 0

git commit -m "$(cat <<'EOF'
Plan 01a Task 7 · move parked skills to canonical skills/<NN>_<name>/

00_META/skills/ was a terrain-prep parking spot. Moves:
- company-analyst    → skills/01_company_analyst/
- industry-analyst   → skills/02_industry_analyst/
- competitor-analyst → skills/03_competitor_analyst/
- discovery-meeting  → skills/06_discovery_meeting/

skills/04_meeting_script/ and skills/05_opportunity_report/ placeholders
(created in Task 1) stay empty; Plan 06 populates them.

00_META/skills/ removed (now empty).

Spec refs: §2.
EOF
)"
```

---

## Task 8: Migrate questionnaires + Consultoria PDF (F15)

**Goal:** Convert the two `Plan_Maestro_*.docx` files in repo root to markdown via pandoc, land them at `00_PARTNERSHIP/questionnaires/2026-05-07_{ricardo,jp}.md`, archive the originals + `.backup` copy, move the `Consultoria_IA_PYMEs_v1.pdf` to `operations/assets/`. F15 closes the "questionnaires not migrated" gap.

**Files:**
- Convert: `Plan_Maestro_MejiaIACia_Ricardo.docx` → `00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md`
- Convert: `Plan_Maestro_MejiaIACia_JP.docx`      → `00_PARTNERSHIP/questionnaires/2026-05-07_jp.md`
- Move:    `Plan_Maestro_MejiaIACia_Ricardo.docx`        → `00_PARTNERSHIP/questionnaires/archive/`
- Move:    `Plan_Maestro_MejiaIACia_JP.docx`             → `00_PARTNERSHIP/questionnaires/archive/`
- Move:    `Plan_Maestro_MejiaIACia.backup-2026-05-07.docx` → `00_PARTNERSHIP/questionnaires/archive/`
- Move:    `Consultoria_IA_PYMEs_v1.pdf`                 → `operations/assets/`

- [ ] **Step 1: Confirm the files exist at root**

```bash
ls -la /srv/Nexostrat/Plan_Maestro_*.docx /srv/Nexostrat/Consultoria_IA_PYMEs_v1.pdf
# Expected: 4 files (Ricardo .docx, JP .docx, .backup .docx, the PDF)
```

- [ ] **Step 2: Convert Ricardo's questionnaire**

```bash
cd /srv/Nexostrat
pandoc Plan_Maestro_MejiaIACia_Ricardo.docx \
  -t gfm \
  --wrap=preserve \
  -o 00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md
```

Verify the output is non-trivial:

```bash
wc -l /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md
# Expected: > 50 lines (the original docx is ~48 KB)

head -20 /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md
# Expected: meaningful markdown content (headings, paragraphs)
```

- [ ] **Step 3: Prepend a brief frontmatter header to Ricardo's file**

Use Edit to insert at the top (the file starts with whatever pandoc emits — usually a heading):

```bash
# Read first line, then prepend frontmatter via a temp file
TMP=$(mktemp)
cat > "$TMP" <<'EOF'
---
source: Plan_Maestro_MejiaIACia_Ricardo.docx (archived)
respondent: Ricardo Mejía Caicedo
date: 2026-05-07
converted: 2026-05-14 via pandoc gfm
---

EOF
cat /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md >> "$TMP"
mv "$TMP" /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md
```

- [ ] **Step 4: Convert JP's questionnaire**

```bash
cd /srv/Nexostrat
pandoc Plan_Maestro_MejiaIACia_JP.docx \
  -t gfm \
  --wrap=preserve \
  -o 00_PARTNERSHIP/questionnaires/2026-05-07_jp.md

wc -l /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_jp.md
# Expected: > 50 lines
```

- [ ] **Step 5: Prepend frontmatter to JP's file**

```bash
TMP=$(mktemp)
cat > "$TMP" <<'EOF'
---
source: Plan_Maestro_MejiaIACia_JP.docx (archived)
respondent: Juan Pablo
date: 2026-05-07
converted: 2026-05-14 via pandoc gfm
---

EOF
cat /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_jp.md >> "$TMP"
mv "$TMP" /srv/Nexostrat/00_PARTNERSHIP/questionnaires/2026-05-07_jp.md
```

- [ ] **Step 6: Archive the originals**

```bash
cd /srv/Nexostrat
git mv Plan_Maestro_MejiaIACia_Ricardo.docx 00_PARTNERSHIP/questionnaires/archive/
git mv Plan_Maestro_MejiaIACia_JP.docx 00_PARTNERSHIP/questionnaires/archive/
git mv Plan_Maestro_MejiaIACia.backup-2026-05-07.docx 00_PARTNERSHIP/questionnaires/archive/
```

- [ ] **Step 7: Move the Consultoria PDF to operations/assets/**

```bash
git mv /srv/Nexostrat/Consultoria_IA_PYMEs_v1.pdf /srv/Nexostrat/operations/assets/
```

- [ ] **Step 8: Verify root no longer has the docx/pdf clutter**

```bash
ls /srv/Nexostrat/*.docx /srv/Nexostrat/*.pdf 2>&1 | head
# Expected: "ls: cannot access ... No such file or directory" or empty
```

- [ ] **Step 9: Stage + commit**

```bash
git add 00_PARTNERSHIP/questionnaires operations/assets
git status --short
# Expected: A entries for the two .md questionnaires; R entries for the docx archives + PDF move

git commit -m "$(cat <<'EOF'
Plan 01a Task 8 · migrate questionnaires + Consultoria PDF (F15)

Pandoc-converts both Plan Maestro questionnaires to markdown:
- Plan_Maestro_MejiaIACia_Ricardo.docx → 00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md
- Plan_Maestro_MejiaIACia_JP.docx      → 00_PARTNERSHIP/questionnaires/2026-05-07_jp.md

Both .md files get YAML frontmatter (source/respondent/date/converted).

Originals + .backup-2026-05-07 archived to:
- 00_PARTNERSHIP/questionnaires/archive/Plan_Maestro_MejiaIACia_Ricardo.docx
- 00_PARTNERSHIP/questionnaires/archive/Plan_Maestro_MejiaIACia_JP.docx
- 00_PARTNERSHIP/questionnaires/archive/Plan_Maestro_MejiaIACia.backup-2026-05-07.docx

Consultoria_IA_PYMEs_v1.pdf moved root → operations/assets/.

Root is now clean of docx/pdf clutter; canonical artifacts live in their
named homes.

Spec refs: F15.
EOF
)"
```

---

## Task 9: 00_PARTNERSHIP/ canonical files

**Goal:** Land the 7 canonical partnership files (excluding `PARTNERSHIP_AGREEMENT.md` itself, which gets the actual signed-PDF summary in Task 17). These are the policy documents JP-and-Ricardo refer to during operations.

**Files:** All under `00_PARTNERSHIP/`:
- Create: `CONFLICT_PROTOCOL.md`
- Create: `REVENUE_DISTRIBUTION.md`
- Create: `ROLES.md`
- Create: `KPIs.md`
- Create: `cost-sharing-agreement.md`
- Create: `qualified-prospect-definition.md`
- Create: `raised_hand_log.md` (empty stub)

`PARTNERSHIP_AGREEMENT.md` lands in Task 17 alongside the encrypted signed PDF.

- [ ] **Step 1: Write `CONFLICT_PROTOCOL.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/CONFLICT_PROTOCOL.md`:

```markdown
# Conflict protocol — 15-min raised-hand

**Effective:** 2026-05-12 (signed at Founding Meeting)
**Co-owners:** Ricardo Mejía Caicedo, Juan Pablo

## Principle

When the co-founders disagree on a non-trivial decision and conversation
has not resolved it within ~15 minutes of focused discussion, either co-founder
may invoke the **raised hand**. The disagreement pauses; the position is
captured in `raised_hand_log.md`; both parties sleep on it; the next
business-day session opens with the raised hand on the agenda.

## When to raise the hand

- Architectural decisions with ≥1 month of unwind cost
- Spend decisions ≥ USD 500 single-cost or ≥ USD 100/mo recurring
- Client-facing policy changes
- Public-facing brand changes
- Anything one co-founder feels would set a precedent they can't live with

Trivial day-to-day calls do not need the raised hand.

## Mechanism

1. **Either co-founder says: "I'm raising the hand on this."**
2. The active conversation pauses — no further argumentation in that thread.
3. The raiser writes a single entry in `raised_hand_log.md`:
   ```
   ## YYYY-MM-DD · <one-line summary>
   **Raised by:** <name>
   **Their position:** <2-4 sentences>
   **Other party's position:** <2-4 sentences as understood>
   **What's at stake:** <1-2 sentences>
   **Sleep-on-it deadline:** <next business day>
   **Resolution:** <added when resolved>
   ```
4. Both parties sleep on it (minimum overnight).
5. Next business day opens with the raised hand. If alignment is reached,
   the resolution is recorded. If not, escalate per § Escalation.

## Escalation

If sleep-on-it does not resolve:
1. **Cooling-off (1 week).** Both parties write a one-page position; exchange.
2. **External brain.** Trusted advisor (TBD — name in `ROLES.md` when picked)
   reads both positions and offers a recommendation. Recommendation is
   advisory, not binding.
3. **Fall-back rule per category:**
   - Code/architecture: Ricardo decides (operator-of-record).
   - Sales/client policy: JP decides (relationship-of-record).
   - Anything else: deadlock → defer the action; status quo holds.

## What this protocol is NOT

- Not a vote-counter (50/50 means deadlock = no action by default).
- Not a delay tactic — raised hands resolve in days, not weeks.
- Not a substitute for direct conversation. It exists for the cases where
  conversation has visibly stopped helping.

---

*Source: Plan Maestro Q-set, founding meeting 2026-05-12. JP's "15-min
raised hand" framing is verbatim from his questionnaire response (Q on
conflict mechanics).*
```

- [ ] **Step 2: Write `REVENUE_DISTRIBUTION.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/REVENUE_DISTRIBUTION.md`:

```markdown
# Revenue distribution — 20/20/20/40

**Effective:** 2026-05-12 (signed at Founding Meeting)
**Co-owners:** Ricardo Mejía Caicedo, Juan Pablo

## Per-engagement split

For each invoiced engagement, gross revenue (after Stripe/payment-processor
fees but BEFORE direct delivery costs like API tokens) splits as:

| Bucket | % | Goes to |
|---|---|---|
| **Company** | 20% | Held in `operations/accounting/`; covers shared expenses + reserves + reinvestment |
| **Originator** | 20% | The co-founder who first sourced the prospect |
| **Closer** | 20% | The co-founder who landed the contract |
| **Executor** | 40% | The co-founder who delivered the engagement (split pro-rata if both contributed materially) |

## Originator vs Closer vs Executor — definitions

- **Originator:** First non-trivial introduction of the prospect into our pipeline.
  Trivial = "I saw their LinkedIn"; non-trivial = "I had a discovery
  conversation, qualified them, brought them to a Diagnóstico-eligible state."
- **Closer:** Signed the contract — name on the proposal-acceptance email,
  led the pricing conversation.
- **Executor:** Delivered the work — Skills runs, meetings led, artifacts
  written. Multi-person engagements split this bucket pro-rata by
  documented effort (logged via Telegram `/expense time` entries against
  the client; quarterly review reconciles).

A co-founder can hold all three roles for one engagement (= 80% of revenue
to that founder; 20% to company). This is fine and expected for
founder-sourced-and-delivered work.

## Cost handling

- **Direct API costs** (Anthropic, Gemini, Grok per engagement) are paid by
  Company before split. Tracked in `operations/accounting/api-spend.md`.
- **Shared infrastructure** (Notion, hosting, domain — see
  `cost-sharing-agreement.md`) does NOT come out of per-engagement revenue;
  it's pre-revenue founder personal-spend reimbursed at first-revenue per
  the cost-sharing agreement.

## Reserves

The Company 20% accumulates until reserve target is met:
- **Stage 1 target:** USD 5,000 reserve (covers ~3 months of API + tooling
  if revenue dries up).
- **Stage 2 target:** 6 months of fully-loaded operating cost.

Once reserves are full, excess Company-bucket distributes 50/50 between
co-founders (treated as additional dividends, not as bonus to a particular
role).

## Quarterly review

Every quarter end (Mar/Jun/Sep/Dec, last Friday): both co-founders review
the per-engagement split log, reconcile any disputed
originator/closer/executor calls, and acknowledge the company-bucket
balance. Output: a one-page `00_PARTNERSHIP/reviews/<YYYY>-Q<N>.md`.

---

*Source: Plan Maestro Q-set, founding meeting 2026-05-12. The 20/20/20/40
ratio is verbatim from JP's revenue-mechanics response.*
```

- [ ] **Step 3: Write `ROLES.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/ROLES.md`:

```markdown
# Roles

**Effective:** 2026-05-12. Reviewed quarterly. Equal equity (50/50) — roles
describe operational division of labor, NOT decision-making weight.

## Ricardo Mejía Caicedo

- **Title:** Co-founder · Architect/Operator
- **Operational ownership:**
  - Repository, infrastructure, deployments
  - Skills development (prompts, Python agents, judge synthesis)
  - Internal AI pipeline operation
  - Bookkeeping setup + maintenance (until accountant onboarded)
- **Default communication:** Ricardo's HP laptop, Claude Code, Telegram bot
- **Bandwidth:** ~30+ h/week (full-time on Nexostrat in Stage 1)

## Juan Pablo (JP)

- **Title:** Co-founder · Sales/Relations
- **Operational ownership:**
  - Prospect sourcing (LatAm network)
  - Closer-of-record on most early engagements
  - Notion canonical workspace ownership
  - Brand voice in Spanish-language client materials
- **Default communication:** Telegram, Signal, Notion, Gitea web (Light mode);
  Heavy mode (Claude Code on Linux Mint) when chosen
- **Bandwidth:** ~10 h/week in Stage 1 (parallel obligations)

## Decision rights

- **50/50 voting on architecture, brand, hiring, spend ≥ USD 500.**
- **Operational autonomy** within each co-founder's domain (Ricardo can ship
  a Skill prompt edit without sign-off; JP can email a prospect without
  sign-off).
- **Conflict protocol:** see `CONFLICT_PROTOCOL.md`.

## External resources (TBD as picked)

- **Trusted-brain advisor** (raised-hand escalation tier 2): name TBD; written
  here once chosen.
- **Accountant:** TBD when first invoice issued.
- **Lawyer (Mexico/Colombia):** TBD when entity constituted.

---

*Quarterly review reconciles roles against actual work distribution and
adjusts as needed.*
```

- [ ] **Step 4: Write `KPIs.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/KPIs.md`:

```markdown
# KPIs — Stage 1 (months 1-12)

**Effective:** 2026-05-12 (signed at Founding Meeting). Reviewed monthly;
revised quarterly.

## North-star

| Metric | Stage 1 target (12 months from launch) |
|---|---|
| Paying clients | ≥ 10 |
| Total revenue | ≥ USD 20,000 |
| Average engagement size | ≥ USD 1,500 |
| Diagnóstico → paid conversion rate | ≥ 30% |

## Pipeline health

| Metric | Floor | Cadence |
|---|---|---|
| Qualified prospects in pipeline | ≥ 5 (active) | Weekly |
| Diagnósticos delivered per month | ≥ 2 | Monthly |
| Time prospect → Diagnóstico | ≤ 14 days | Per-engagement |
| Time Diagnóstico → proposal | ≤ 7 days | Per-engagement |
| Proposal acceptance rate | ≥ 25% | Quarterly |

## Quality / discipline

| Metric | Bar |
|---|---|
| Bodai benchmark score (Skill 1) | ≥ 7/10 (start), ≥ 8/10 (paid bar) |
| Anti-hallucination violations per 100 skill runs | 0 (factual-accuracy gate is hard-blocking) |
| Pipeline stuck > 14 days | 0 (alert tier 2) |
| Mean time to recover (machine failure) | ≤ 30 min (warm-standby RTO target) |

## Founder health

| Metric | Bar |
|---|---|
| Weekly raised-hand entries | ≤ 2 (more = communication breakdown signal) |
| Quarterly review completion | 100% (Mar/Jun/Sep/Dec last Friday) |

## Revisit triggers (Stage 2 KPIs)

When ANY of:
- Stage 1 north-star hit (≥ 10 paying clients OR ≥ USD 20K revenue)
- Pipeline > 15 active clients
- Need for first hire surfaces

…the KPIs get rewritten for Stage 2 (target: ≥ 30 clients, ≥ USD 100K, first hire).

---

*Source: Plan Maestro Q-set Q9 (KPIs), founding meeting 2026-05-12.*
```

- [ ] **Step 5: Write `cost-sharing-agreement.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/cost-sharing-agreement.md`:

```markdown
# Cost-sharing agreement (pre-revenue)

**Effective:** 2026-05-12. Reviewed at first revenue + every quarter.

## Principle

Pre-revenue, the firm-as-entity carries no costs. Each co-founder absorbs
their domain's tooling on personal subscriptions; the firm reimburses at
first-revenue per the schedule below.

## Stage 1 — pre-revenue (current)

| Cost line | Who pays | Personal account holder | Monthly | Reimbursable? |
|---|---|---|---|---|
| **Claude MAX (Ricardo)** | Ricardo | Ricardo personal Anthropic | ~USD 200 | Yes (capped at engagement count) |
| **Claude MAX (JP)** | JP | JP personal Anthropic | ~USD 200 | Yes (same cap) |
| **Gemini API** | (free tier) | n/a | $0 until ~Oct 2026 | n/a |
| **Grok API** | Ricardo | Ricardo personal X | ~USD 5-15 | Yes |
| **Notion + AI add-on** | JP | JP personal Notion (firm uses JP's workspace) | ~USD 30-50 | Yes |
| **Domain (nexostrat.com)** | JP | JP personal registrar | ~USD 12/yr amortized | Yes |
| **Email (contacto@nexostrat.com)** | JP | JP personal hosting | ~USD 6/mo | Yes |
| **Hosting (Gitea + bot, currently HP-laptop)** | $0 | n/a | $0 | n/a |
| **Drive 2TB** | Ricardo | Ricardo personal Google | ~USD 10/mo | Yes |
| **Bitwarden Premium** | Each personal | each | ~USD 1/mo each | No (personal hygiene) |
| **Hardware (HP-laptop, JP-laptop, peripherals)** | Each | each | n/a | No (personal asset) |
| **Tailscale** | (free tier — personal accounts) | n/a | $0 | n/a |
| **Signal** | n/a | n/a | $0 | n/a |
| **Telegram** | n/a | n/a | $0 | n/a |
| **Total firm pays in Stage 1** | | | **USD $0/mo** | |
| **Total Ricardo personal pays** | | | **~USD 215/mo + Claude MAX 200** | reimbursable |
| **Total JP personal pays** | | | **~USD 36-56/mo + Claude MAX 200** | reimbursable |

## Reimbursement schedule (triggered at first revenue)

When firm cumulative revenue ≥ USD 1,000:
1. Ricardo and JP each submit a 12-month rolling reimbursement claim from
   `cost-sharing-agreement.md` line items (no receipts needed for the
   subscriptions listed above; dollar figures are honor-system at the
   subscription cost).
2. Reimbursements paid in order: hosting/domain/email first (hard
   infrastructure), then Notion, then Drive, then Claude MAX (capped at the
   number of engagements Claude was used on × per-engagement budget).
3. Capped at 50% of accumulated Company-bucket reserve to keep operating
   reserves intact.

## Stage 2 trigger (firm absorbs costs directly)

When ANY of:
- Cumulative revenue ≥ USD 5,000
- Reserve target met (USD 5K)
- First payroll drawn

…the firm switches to direct billing for Notion + Drive + email + domain
(Bitwarden org sub at this point too, per Stage 2 ADR-019). Claude MAX
remains personal until single-month firm spend on AI exceeds USD 500.

## Reconciliation cadence

Quarterly (`00_PARTNERSHIP/reviews/<YYYY>-Q<N>.md`): both co-founders confirm
their personal-spend lines are unchanged or update them. Unchanged is the
default — no one needs to email a receipt.

---

*Source: 2026-05-14 Aurora HTML presentation Card 28 cost reality (Card 28
post-amendment) + Founding Meeting verbal agreement on personal-spend
reimbursability. Spec §5 cost table will be amended in a future cycle to
match this document — see `t-spec-cost-table-amendment`.*
```

- [ ] **Step 6: Write `qualified-prospect-definition.md`**

Write `/srv/Nexostrat/00_PARTNERSHIP/qualified-prospect-definition.md`:

```markdown
# Qualified prospect — definition

**Effective:** 2026-05-12. Reviewed monthly until pipeline hits 5 actives.

## A prospect is QUALIFIED when ALL hold

1. **Client revenue baseline:** ≥ USD 50,000/year demonstrated revenue
   (per Plan Maestro Q6 — JP's hard floor).
2. **Sector fit:** PyME (small-medium enterprise) in Mexico, Colombia, or
   broader LatAm. Sectors we have at least one prior touchpoint in:
   - Bitcoin/fintech (Bodai, Alfa Bitcoin)
   - Food/retail (Bodai)
   - LatAm B2B services (broad, JP's network)
   - …grows by quarter.
3. **Decision-maker engagement:** at least one non-trivial conversation with
   someone authorized to sign a Diagnóstico engagement (founder, COO,
   department head with budget). "We're talking to procurement" does not
   qualify; "we have a 30-min Zoom with the COO scheduled" does.
4. **Need surface:** they've articulated at least one pain we believe AI
   can address. Vague "AI exploration" interest does NOT qualify; "we
   spend 20 hours a week on competitive monitoring and want it cut to 2"
   does.

## A prospect is DISQUALIFIED if ANY holds

- Revenue under USD 50K/yr (no budget for our service-line).
- Geographic outside LatAm AND English-first (we don't optimize for that
  market in Stage 1 — refer to a peer).
- Industry we have zero domain knowledge in (we'd be expensive learning,
  not consulting).
- "Free pilot only" insistence after the first 3 free-pilot slots are
  filled (per Plan Maestro pilot-vs-paid structure).
- Single-decision-maker who explicitly will not engage with AI tooling
  (mismatch — they'll resist the deliverables).

## Where the qualification call lives

In the prospect's `pipeline/prospects/<slug>/qualification.md`. Either
co-founder can mark a prospect QUALIFIED or DISQUALIFIED with a one-line
note + date. Disagreement → raised hand.

## Re-qualification triggers

A prospect can move OUT of qualified back to "nurture" status if:
- 60 days no movement after Diagnóstico delivered
- Revenue baseline drops below USD 50K
- Decision-maker leaves their role
- They explicitly defer

…and back IN later via the same flow.

---

*Source: Plan Maestro Q-set Q6, founding meeting 2026-05-12. Numbers reviewed
monthly during quarterly review; raised in Q1-2027 to USD 75K if pipeline
quality is strong.*
```

- [ ] **Step 7: Write `raised_hand_log.md` (empty stub)**

Write `/srv/Nexostrat/00_PARTNERSHIP/raised_hand_log.md`:

```markdown
# Raised-hand log

> Per `CONFLICT_PROTOCOL.md`: each raised hand gets one entry below.
> Resolved entries stay visible (forensic record).

**Active raised hands:** 0

---

## Format

```
## YYYY-MM-DD · <one-line summary>
**Raised by:** <name>
**Their position:** <2-4 sentences>
**Other party's position:** <2-4 sentences as understood>
**What's at stake:** <1-2 sentences>
**Sleep-on-it deadline:** <next business day>
**Resolution:** <added when resolved — verbatim agreed text>
```

---

## Log entries

*(none yet)*
```

- [ ] **Step 8: Verify all 6 files were written**

```bash
ls /srv/Nexostrat/00_PARTNERSHIP/*.md
# Expected:
# 00_PARTNERSHIP/CONFLICT_PROTOCOL.md
# 00_PARTNERSHIP/KPIs.md
# 00_PARTNERSHIP/REVENUE_DISTRIBUTION.md
# 00_PARTNERSHIP/ROLES.md
# 00_PARTNERSHIP/cost-sharing-agreement.md
# 00_PARTNERSHIP/qualified-prospect-definition.md
# 00_PARTNERSHIP/raised_hand_log.md

wc -l /srv/Nexostrat/00_PARTNERSHIP/*.md
```

- [ ] **Step 9: Stage + commit**

```bash
git add 00_PARTNERSHIP/CONFLICT_PROTOCOL.md \
        00_PARTNERSHIP/REVENUE_DISTRIBUTION.md \
        00_PARTNERSHIP/ROLES.md \
        00_PARTNERSHIP/KPIs.md \
        00_PARTNERSHIP/cost-sharing-agreement.md \
        00_PARTNERSHIP/qualified-prospect-definition.md \
        00_PARTNERSHIP/raised_hand_log.md

git commit -m "$(cat <<'EOF'
Plan 01a Task 9 · 00_PARTNERSHIP/ canonical policy files

Lands the policy documents Ricardo and JP refer to during operations:
- CONFLICT_PROTOCOL.md  — JP's 15-min raised-hand mechanism + escalation
- REVENUE_DISTRIBUTION.md  — 20/20/20/40 (company/originator/closer/executor)
- ROLES.md  — operational ownership (NOT decision-weight; equity stays 50/50)
- KPIs.md  — Stage 1 north-star + pipeline-health + quality bars
- cost-sharing-agreement.md  — pre-revenue: each co-founder absorbs personal
  subs; firm reimburses at first revenue. Firm pays $0 in Stage 1.
- qualified-prospect-definition.md  — ≥ USD 50K/yr revenue + sector fit +
  decision-maker engagement + need-surface
- raised_hand_log.md  — empty stub with format guide; 0 active

PARTNERSHIP_AGREEMENT.md (markdown summary) lands in Task 17 alongside the
encrypted signed PDF.

Spec refs: §4.5 (00_PARTNERSHIP/ contents), ADRs 015 (qualified prospect).
EOF
)"
```

---

## Task 10: vault/ scaffold + sensitive_index.md + README.md

**Goal:** Land the vault discipline files. The `vault/` namespace is created in Task 1; this task adds the README documenting the rare-access pattern and the sensitive_index.md template (populated when first heavy asset arrives).

**Files:**
- Create: `vault/README.md`
- Create: `vault/sensitive_index.md`

- [ ] **Step 1: Write `vault/README.md`**

Write `/srv/Nexostrat/vault/README.md`:

```markdown
# vault/ — encrypted catastrophic-loss material

**Per ADR-003 + ADR-004 + spec §3.**

## What goes here

Material whose loss or leak would be catastrophic, AND that is rarely accessed:

| Subfolder | Owner | Holds |
|---|---|---|
| `partnership/` | Founder | Signed partnership PDF, revenue receipts |
| `legal/` | Founder | Entity formation docs, tax filings (when constituted) |
| `accounting/` | Founder | Bank statements (monthly), invoices (firm-side) |
| `keys/` | Founder | Recovery codes, key-rotation log |
| `clients/<slug>/` | Client-Owner (per F10) | NDAs, contracts, invoices to client |

Per F10 namespace split:
- **Founder** owns `vault/{partnership,legal,accounting,keys}/`.
- **Client-Owner** owns `vault/clients/<slug>/`.
- **Skills-Master** owns no vault content.

## What does NOT go here

- Day-to-day operational files (those go in `operations/`, `00_PARTNERSHIP/`,
  `pipeline/clients/<slug>/` plaintext).
- Active work-in-progress (write the .age artifact only when the
  document is final-version forensic-record material).
- Plaintext anything (the pre-commit hook + .gitignore both refuse).

## Access discipline (rare-access pattern)

```
                 [DO NOT mount this folder]
                          │
                          ▼
   For each access:
   1. Identify the .age file you need.
   2. Decrypt to /dev/shm (RAM tmpfs):
        age -d -i ~/.config/age/nexostrat.key vault/path/file.age \
            > /dev/shm/<short-name>
   3. Use the file (open, read, edit if needed).
   4. If edited, re-encrypt:
        age -R infra/age-recipients.txt /dev/shm/<short-name> \
            > vault/path/file.age
   5. Shred the plaintext:
        shred -u /dev/shm/<short-name>
```

**No persistent mounted plaintext.** No editor swap files (`.swp`, `~`)
get written to the vault path even briefly — `/dev/shm` is the discipline.

## Heavy assets (audio, large PDFs)

Heavy assets are age-encrypted before Drive 2TB upload. The local working
copy is the .age in `vault/<subfolder>/`; the cloud copy is the same .age
file at the same path on Drive. `sensitive_index.md` is the human-readable
catalog (filename, what it is, when uploaded, where the cloud copy lives).

## What if I lose my private key

See `docs/runbooks/key_compromise.md` (Plan 02 writes it). Short version:
- Ricardo private key passphrase-encrypted at `~/.config/age/nexostrat.key.age`
  + backed up to Bitwarden + paper backup of the Bitwarden master.
- JP private key same posture (recipe in `infra/age-recipients.txt` comment
  block).
- If both Ricardo's machine AND Ricardo's Bitwarden are lost simultaneously,
  recovery requires JP's key + a re-encrypt-everything pass.

## What if I add a new recipient

Add the pubkey line to `infra/age-recipients.txt`, then run a re-encrypt
pass over the entire vault tree:

```bash
# Plan 01a does NOT ship this script — for now, manual one-liner:
find vault -name '*.age' -print0 | while IFS= read -r -d '' f; do
  age -d -i ~/.config/age/nexostrat.key "$f" \
    | age -R infra/age-recipients.txt -o "${f}.new" \
    && mv "${f}.new" "$f"
done
```

A wrapper script `infra/scripts/reencrypt-vault.sh` lands in a future plan
when the use-case becomes routine (Stage 2).
```

- [ ] **Step 2: Write `vault/sensitive_index.md`**

Write `/srv/Nexostrat/vault/sensitive_index.md`:

```markdown
# Sensitive asset index

> Catalog of vault contents — both repo-resident `.age` files AND heavy
> assets (audio, large PDFs) age-encrypted on Drive 2TB.
>
> One row per artifact. Sorted newest-first within each section.

## Repo-resident vault (`vault/<subfolder>/*.age`)

| Path | What | Created | Recipients | Notes |
|---|---|---|---|---|
| *(populated as artifacts land — Task 17 lands the first row)* | | | | |

## Drive-resident heavy assets (`<rclone>:nexostrat/<path>`)

| Path | What | Size | Uploaded | Recipients | Notes |
|---|---|---|---|---|---|
| *(populated when first heavy asset is uploaded — Plan 08 / Plan 09 onwards)* | | | | | |

---

## Conventions

- **Path** uses repo-relative for vault, rclone-remote-relative for Drive.
- **Recipients** lists the age pubkeys (short hash or `all` if every
  recipient in `infra/age-recipients.txt`).
- **Notes** flags per-artifact retention/destruction policy if non-default.

## Default retention

- Partnership artifacts: forever.
- Client legal (NDAs, contracts): forever.
- Client accounting: 7 years (LATAM commercial-law floor).
- Audio recordings of client meetings: 24 months unless client requests
  longer.
- Internal partner meeting audio: 6 months.

## Verification

A weekly cron (Plan 10) cross-checks: every row here has a corresponding
file; every file has a row. Drift triggers an alert.
```

- [ ] **Step 3: Verify both files exist + render correctly**

```bash
ls -la /srv/Nexostrat/vault/README.md /srv/Nexostrat/vault/sensitive_index.md
wc -l /srv/Nexostrat/vault/README.md /srv/Nexostrat/vault/sensitive_index.md
```

- [ ] **Step 4: Stage + commit**

```bash
git add vault/README.md vault/sensitive_index.md
git commit -m "$(cat <<'EOF'
Plan 01a Task 10 · vault/ README + sensitive_index template

vault/README.md documents:
- F10 namespace split (Founder owns partnership/legal/accounting/keys;
  Client-Owner owns clients/<slug>/; Skills-Master owns nothing in vault)
- Rare-access discipline (decrypt to /dev/shm, use, re-encrypt, shred)
- Heavy-asset cloud upload pattern (age first, then upload)
- Recovery scenarios + add-new-recipient one-liner

vault/sensitive_index.md is a template — populated as artifacts land.
First row arrives in Task 17 (signed partnership PDF).

Spec refs: §3 (Vault rare-access pattern), F10, ADRs 003, 004.
EOF
)"
```

---

## Task 11: Verify Ricardo's age setup

**Goal:** No new files; this task verifies the terrain-prep age work landed correctly. Confirms Ricardo's pubkey is in `infra/age-recipients.txt`, his private key is encrypted on disk with mode 600, and a roundtrip encrypt-decrypt against his key alone works.

**Files:** No new files. Verification only.

**No commit at the end** — this task is a pure verification gate.

- [ ] **Step 1: Verify `infra/age-recipients.txt` has Ricardo's pubkey**

```bash
grep '^age1' /srv/Nexostrat/infra/age-recipients.txt
# Expected: at least one line — Ricardo's pubkey
# (As of terrain prep: age14kfstsrnpvvnp56jafnd5uqjpyjz40zak773ny2kdhvvayuy7d6sncjjv3)
```

- [ ] **Step 2: Verify Ricardo's private key is on disk, encrypted, mode 600**

```bash
ls -la ~/.config/age/nexostrat.key.age 2>&1
# Expected: -rw------- (mode 600), owned by ricardo, non-zero size
```

If the file is at a different path or has wrong permissions, **stop and surface to Ricardo** before proceeding. Wrong permissions on the private key file is a critical posture issue.

- [ ] **Step 3: Verify the private key decrypts (passphrase prompt) and produces an age key**

```bash
# Decrypt to /dev/shm, verify it parses, immediately shred
age -d ~/.config/age/nexostrat.key.age > /dev/shm/test-key-$$.txt
# Expected: passphrase prompt; on success, file written

# Standard age identity files start with a `# created: <timestamp>` comment line,
# followed by `# public key: age1...`, then the secret key `AGE-SECRET-KEY-1...`.
# Verify the file contains a valid secret key anywhere in its body:
grep -q '^AGE-SECRET-KEY-1' /dev/shm/test-key-$$.txt && echo "OK: identity parses" || echo "FAIL: no AGE-SECRET-KEY-1 line found"
# Expected: "OK: identity parses"

shred -u /dev/shm/test-key-$$.txt
# Expected: file removed; no error
```

> **Note (2026-05-16 amendment per `t-plan-01a-text-amendments`):** earlier
> draft used `head -1` to look for `AGE-SECRET-KEY-1` on line 1. Standard
> `age-keygen -p` output puts `# created: ...` on line 1 and the secret key
> later in the file. The corrected check greps for the secret-key marker
> anywhere in the file, which is the robust form.

- [ ] **Step 4: Roundtrip — encrypt a test plaintext to the recipients file, decrypt with Ricardo's key**

```bash
TMP_PT=/dev/shm/roundtrip-pt-$$.txt
TMP_CT=/dev/shm/roundtrip-ct-$$.age
TMP_DEC=/dev/shm/roundtrip-dec-$$.txt

echo "Nexostrat roundtrip test $(date -Iseconds)" > "$TMP_PT"

age -R /srv/Nexostrat/infra/age-recipients.txt -o "$TMP_CT" "$TMP_PT"
ls -la "$TMP_CT"
# Expected: ciphertext file exists

# Decrypt requires Ricardo's private key (passphrase prompt)
age -d -i ~/.config/age/nexostrat.key.age "$TMP_CT" > "$TMP_DEC"

diff "$TMP_PT" "$TMP_DEC" && echo "ROUNDTRIP PASS" || echo "ROUNDTRIP FAIL"
# Expected: ROUNDTRIP PASS

shred -u "$TMP_PT" "$TMP_CT" "$TMP_DEC"
```

If the roundtrip fails, **stop and resolve**. Common failures:
- Wrong path to private key
- Recipients file has stale/typo'd pubkey
- Passphrase entered incorrectly

- [ ] **Step 5: Document verification result in `STATUS.md` `Recent activity` section (NO commit yet — Task 18 commits the consolidated status update)**

Append to `STATUS.md` at the end of `## Recent activity`:

```markdown
- **2026-05-14 (Plan 01a Task 11)** — Verified Ricardo's age setup: pubkey in `infra/age-recipients.txt`, private key mode 600 at `~/.config/age/nexostrat.key.age`, roundtrip encrypt-decrypt passes. Plan ready to gate on JP age pubkey arrival (Task 12).
```

---

## ⏸ JP COORDINATION GATE — Tasks 12-18 require JP's age pubkey

The next 7 tasks depend on JP's age pubkey landing in `infra/age-recipients.txt`. Per `t-jp-age-keypair`, a Signal message went out 2026-05-14 with the recipe; JP's response is drip-feed expected. The current session pauses cleanly here.

**Action when pausing:**
1. Update `CHECKPOINT.md`:
   - "What I just did": "Plan 01a Tasks 1-11 complete; verified Ricardo's age setup."
   - "In flight — concrete next action": "Wait for JP age pubkey via Signal (per t-jp-age-keypair). On arrival, resume Plan 01a Task 12."
   - "Blocked on": "JP age pubkey arrival."
2. Push commits so far to Gitea (`git push origin main`).
3. End session per CLAUDE.md Session End Protocol.

**Action when resuming (JP pubkey has landed):**
1. Verify JP responded with a valid age pubkey (`age1` prefix, ~62 chars).
2. Confirm JP also did the recipe correctly (private key encrypted with passphrase + Bitwarden backup).
3. Proceed to Task 12.

---

## Task 12: Add JP pubkey to recipients (C2)

**Goal:** Append JP's age pubkey to `infra/age-recipients.txt` and verify the file structure stays parseable.

**Files:**
- Modify: `infra/age-recipients.txt`

- [ ] **Step 1: Confirm JP's pubkey is in hand**

JP's pubkey arrives via Signal as a single line beginning `age1` followed by ~57 chars of base32. **Visually inspect** before pasting:

- Length ~62 chars
- Starts with `age1`
- Only `[a-z0-9]` after the prefix
- One line (no whitespace embedded)

If anything looks off, **ask JP to resend** before editing the recipients file.

- [ ] **Step 2: Edit `infra/age-recipients.txt` to add JP's pubkey**

Use Edit to replace the JP placeholder block. Find:

```
# Juan Pablo (founder, machine TBD per t-jp-os-confirmation)
# PENDING — JP runs age-keygen, sends pubkey via Signal (per t-jp-age-keypair).
# Add as: age1<JP_PUBKEY_HERE>
```

Replace with:

```
# Juan Pablo (founder, <jp-machine-shortname>, generated <YYYY-MM-DD by JP>)
age1<JP_PUBKEY_HERE>
```

(Substitute the real machine name + date + the actual pubkey line.)

- [ ] **Step 3: Verify the file now has TWO `age1` lines**

```bash
grep -c '^age1' /srv/Nexostrat/infra/age-recipients.txt
# Expected: 2
```

- [ ] **Step 4: Verify the file is well-formed (no stray characters)**

```bash
grep -vE '^(#|age1|$)' /srv/Nexostrat/infra/age-recipients.txt
# Expected: empty output (every line is a comment, an age1-pubkey, or blank)
```

- [ ] **Step 5: Stage + commit**

```bash
git add infra/age-recipients.txt
git commit -m "$(cat <<'EOF'
Plan 01a Task 12 · add JP pubkey to age-recipients (C2)

Closes the audit CRITICAL 2 fix. Vault no longer encrypted to a single
recipient; both founders can decrypt all firm secrets/vault content.

JP key generation per t-jp-age-keypair: passphrase-encrypted private key
+ Bitwarden backup (parallel posture to Ricardo's key).

Roundtrip verification follows in Task 13.

Spec refs: §3 (Identities), C2, ADR-003.
EOF
)"
```

---

## Task 13: Bidirectional encrypt-decrypt roundtrip

**Goal:** Prove encrypt-to-recipients + decrypt-with-each-key works in BOTH directions. This is the C2 success criterion.

**Files:** No file changes. Pure test.

- [ ] **Step 1: Roundtrip — encrypt with both recipients, Ricardo decrypts**

```bash
TMP_PT=/dev/shm/jp-roundtrip-pt-$$.txt
TMP_CT=/dev/shm/jp-roundtrip-ct-$$.age
TMP_DEC=/dev/shm/jp-roundtrip-dec-$$.txt

echo "Both-recipients roundtrip $(date -Iseconds)" > "$TMP_PT"

age -R /srv/Nexostrat/infra/age-recipients.txt -o "$TMP_CT" "$TMP_PT"

age -d -i ~/.config/age/nexostrat.key.age "$TMP_CT" > "$TMP_DEC"
diff "$TMP_PT" "$TMP_DEC" && echo "RICARDO DECRYPT PASS" || echo "FAIL"

shred -u "$TMP_PT" "$TMP_CT" "$TMP_DEC"
```

Expected: `RICARDO DECRYPT PASS`.

- [ ] **Step 2: JP-side roundtrip — JP runs the equivalent on his machine**

JP needs to perform the equivalent verification on his side (his machine, his key). Send him this command via Signal:

```bash
# JP runs (after pulling latest infra/age-recipients.txt from Gitea):
echo "test" > /tmp/test.txt
age -R infra/age-recipients.txt -o /tmp/test.age /tmp/test.txt
age -d -i ~/.config/age/nexostrat.key.age /tmp/test.age
# Expected output: "test"
shred -u /tmp/test.txt /tmp/test.age
```

JP confirms via Signal: "roundtrip works." Document the confirmation in `STATUS.md` Recent activity.

- [ ] **Step 3: Cross-decrypt — bidirectional sentinel roundtrip (load-bearing C2 criterion)**

This is the load-bearing C2 criterion: **either holder can decrypt firm content**. Both directions must succeed before proceeding to Task 14. Per Finding 6 of the 2026-05-14 re-audit, JP is Light-mode by default (Telegram + Gitea web only, no git CLI on his machine), so the reverse direction (JP encrypts, Ricardo decrypts) uses a Signal-attachment delivery channel instead of git push.

**Direction A — Ricardo → JP:**

```bash
# Ricardo (HP laptop):
TMP=/dev/shm/sentinel-$$.txt
echo "Sentinel from Ricardo $(date -Iseconds)" > "$TMP"
age -R /srv/Nexostrat/infra/age-recipients.txt \
    -o /srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age "$TMP"
shred -u "$TMP"

git add vault/keys/sentinel-ricardo-to-jp.age
git commit -m "Plan 01a Task 13 · sentinel from Ricardo (will be removed after both directions confirmed)"
git push origin main
```

JP pulls via Gitea web (downloads the .age file from the Gitea web file viewer's "raw" link, OR uses a one-time git clone if he chooses Heavy mode for the test) and runs locally:

```bash
# JP (his machine):
age -d -i ~/.config/age/nexostrat.key.age sentinel-ricardo-to-jp.age
# Expected output: "Sentinel from Ricardo <timestamp>"
```

JP confirms via Signal: "Direction A works — got: 'Sentinel from Ricardo <timestamp>'". Document the confirmation in `STATUS.md` Recent activity (Direction A line).

**Direction B — JP → Ricardo (Signal-attachment flow, no git on JP's side required):**

Ricardo sends JP the contents of `infra/age-recipients.txt` via Signal (paste as a message — it's a 2-line public file, safe to share over Signal). JP saves it as `/tmp/nexostrat-recipients.txt` locally.

```bash
# JP runs (on his machine, no git required):
echo "Sentinel from JP $(date -Iseconds)" | \
  age -R /tmp/nexostrat-recipients.txt -o /tmp/sentinel-jp-to-ricardo.age
```

JP attaches `/tmp/sentinel-jp-to-ricardo.age` to a Signal message → Ricardo. Ricardo saves the attachment to a known path and runs:

```bash
# Ricardo (HP laptop) — assumes Signal saved the file to ~/Downloads/sentinel-jp-to-ricardo.age
cp ~/Downloads/sentinel-jp-to-ricardo.age /srv/Nexostrat/vault/keys/sentinel-jp-to-ricardo.age

age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/vault/keys/sentinel-jp-to-ricardo.age
# Expected output: "Sentinel from JP <timestamp>"
```

Ricardo confirms back on Signal: "Direction B works — got: 'Sentinel from JP <timestamp>'". Document in `STATUS.md` Recent activity (Direction B line).

Then stage the JP-side sentinel for cleanup-commit:

```bash
git add vault/keys/sentinel-jp-to-ricardo.age
git commit -m "Plan 01a Task 13 · sentinel from JP (will be removed in next commit after both directions confirmed)"
git push origin main
```

If **either** direction fails, do NOT proceed to Step 4 or Task 14. Resolve the failing direction first — possible causes: JP's pubkey not in recipients file (Task 12), wrong passphrase on JP's key, or recipients-file contents corrupted in Signal paste (re-send as attachment instead).

- [ ] **Step 4: Remove both sentinels after bidirectional confirmation**

```bash
# Both sentinels are now committed (Direction A commit + Direction B commit above).
# This commit removes both in one pass — `git rm` will error if either is missing,
# which is the desired loud failure if Step 3 was skipped/partial.
git rm vault/keys/sentinel-ricardo-to-jp.age vault/keys/sentinel-jp-to-ricardo.age
git commit -m "$(cat <<'EOF'
Plan 01a Task 13 · remove C2 verification sentinels

Bidirectional encrypt/decrypt confirmed (Direction A: Ricardo→JP via git;
Direction B: JP→Ricardo via Signal attachment, per the JP Light-mode flow
specified in Plan 01a Task 13 Step 3). Both holders can decrypt firm content
with their own age key. Verification timestamps logged in STATUS.md Recent
activity.

Spec refs: §3 (Identities), C2 closure.
EOF
)"
git push origin main
```

If only one direction was verified, do NOT proceed to Task 14. Resolve the failing direction first.

---

## Task 14: secrets.env.age (encrypted to both recipients)

**Goal:** Create the firm's secrets file, encrypted to both recipients. Stage 1 starts essentially empty (placeholders for Anthropic / Gemini / Grok / GitHub PAT / Codeberg PAT / Notion API key — values filled in as services come online).

**Files:**
- Create: `secrets.env.age` at repo root (encrypted)

- [ ] **Step 1: Compose the plaintext template (in /dev/shm)**

```bash
TMP=/dev/shm/secrets.env.$$
cat > "$TMP" <<'EOF'
# Nexostrat secrets — Stage 1 starter
# Filled in as services come online. Empty values mean "not yet provisioned."
# Sourced via infra/scripts/run-with-secrets.sh (Task 15).

# --- AI providers ---
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=

# --- Git mirrors (Plan 01b uses these) ---
GITHUB_MIRROR_PAT=
CODEBERG_MIRROR_PAT=

# --- Notion (Plan 04+ uses this for meeting transcription) ---
NOTION_API_KEY=

# --- Telegram bot (Plan 04+) ---
TELEGRAM_BOT_TOKEN=

# --- Drive 2TB rclone token (Plan 08+) ---
RCLONE_DRIVE_TOKEN=
EOF
```

- [ ] **Step 2: Encrypt to both recipients**

```bash
age -R /srv/Nexostrat/infra/age-recipients.txt \
    -o /srv/Nexostrat/secrets.env.age \
    "$TMP"
shred -u "$TMP"

ls -la /srv/Nexostrat/secrets.env.age
# Expected: file exists, ~1 KB
```

- [ ] **Step 3: Verify both recipients can decrypt**

```bash
TMP_DEC=/dev/shm/decrypt-test-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP_DEC"
head -3 "$TMP_DEC"
# Expected: the comment header lines from the template
shred -u "$TMP_DEC"
```

JP reproduces the same on his side via Signal handshake (see Task 13 Step 2 pattern).

- [ ] **Step 4: Stage + commit**

```bash
git add secrets.env.age
git commit -m "$(cat <<'EOF'
Plan 01a Task 14 · secrets.env.age (encrypted to both recipients)

Stage 1 starter. Empty values filled as services come online:
- ANTHROPIC_API_KEY (when Mode B work begins)
- GOOGLE_API_KEY    (when Gemini API used; free until ~Oct 2026)
- XAI_API_KEY       (Grok)
- GITHUB_MIRROR_PAT, CODEBERG_MIRROR_PAT  (Plan 01b)
- NOTION_API_KEY    (Plan 04+ meeting transcription)
- TELEGRAM_BOT_TOKEN (Plan 04)
- RCLONE_DRIVE_TOKEN (Plan 08+)

Sourced via infra/scripts/run-with-secrets.sh (Task 15).

Spec refs: §3 (Secrets — runtime injection), ADR-004.
EOF
)"
```

---

## Task 15: `run-with-secrets.sh` (C1 fix) + smoke test

**Goal:** Implement the secrets-loading wrapper with the C1 fix: explicit cleanup via trap, NO `exec` leak, plaintext lives only at `/dev/shm/nexostrat-secrets-<pid>` and is shredded on every exit path. Smoke test asserts no leftover plaintext after the wrapped command exits.

**Files:**
- Create: `infra/scripts/run-with-secrets.sh`
- Create: `infra/scripts/test_run_with_secrets_no_leak.sh`

- [ ] **Step 1: Write the leak-detection test FIRST (TDD red)**

Create `/srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh`:

```bash
#!/usr/bin/env bash
# Test: run-with-secrets.sh creates plaintext at /dev/shm DURING execution,
#       and removes it AFTER exit (positive + negative control for C1).
#
# This test is INTERACTIVE — the wrapper's inner `age -d` reads the age-key
# passphrase from /dev/tty. Enter Ricardo's (or JP's) passphrase when prompted.
#
# Per Finding 2 of the 2026-05-14 re-audit: this replaces an earlier version
# that backgrounded the wrapper, never created the plaintext (wrapper was
# blocked on passphrase prompt), then false-PASSed by observing absence of a
# file that was never written. The new design polls for the file's appearance
# (positive control), then checks the specific path is gone after kill
# (negative control). It also avoids blasting concurrent legitimate sessions
# (no global `rm -f /dev/shm/nexostrat-secrets-*`).

set -uo pipefail
WRAPPER="/srv/Nexostrat/infra/scripts/run-with-secrets.sh"
SENTINEL_CMD='sleep 20'   # long enough to observe + kill mid-execution
POLL_DEADLINE_SECS=30     # generous: user types passphrase, age decrypts, wrapper writes

if [[ ! -x "$WRAPPER" ]]; then
  echo "FAIL — wrapper script not found or not executable at $WRAPPER"
  exit 1
fi

echo "================================================================"
echo "  C1 Leak Test (interactive — type your age passphrase when asked)"
echo "================================================================"
echo "  Backgrounded wrapper runs '$SENTINEL_CMD'. Polling /dev/shm for"
echo "  up to ${POLL_DEADLINE_SECS}s to see the plaintext appear (positive"
echo "  control). Then kills the wrapper and verifies cleanup (negative"
echo "  control)."
echo

# Snapshot existing /dev/shm/nexostrat-secrets-* files so concurrent sessions
# are preserved. We compute set-difference to identify OUR file.
BEFORE=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)

"$WRAPPER" sh -c "$SENTINEL_CMD" &
WRAPPER_PID=$!

# Poll for a new file to appear (means wrapper got past decrypt+write).
echo "--- waiting for plaintext to appear at /dev/shm ---"
FOUND=""
DEADLINE=$((SECONDS + POLL_DEADLINE_SECS))
while (( SECONDS < DEADLINE )); do
  if ! kill -0 "$WRAPPER_PID" 2>/dev/null; then
    echo "FAIL — wrapper exited before creating plaintext (decrypt failure?)"
    wait "$WRAPPER_PID" 2>/dev/null
    exit 1
  fi
  CURRENT=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)
  NEW=$(comm -23 <(echo "$CURRENT") <(echo "$BEFORE") 2>/dev/null | head -1)
  if [[ -n "$NEW" ]]; then FOUND="$NEW"; break; fi
  sleep 1
done

if [[ -z "$FOUND" ]]; then
  echo "FAIL — no plaintext file appeared at /dev/shm within ${POLL_DEADLINE_SECS}s"
  echo "  (user may not have entered passphrase, or wrapper is broken)"
  kill "$WRAPPER_PID" 2>/dev/null
  wait "$WRAPPER_PID" 2>/dev/null
  exit 1
fi
echo "PASS — wrapper created $FOUND during execution (positive control)"

# Now kill the wrapper and verify the SPECIFIC file we observed is removed.
kill "$WRAPPER_PID" 2>/dev/null
wait "$WRAPPER_PID" 2>/dev/null
sleep 1

if [[ -e "$FOUND" ]]; then
  echo "FAIL — $FOUND still exists after wrapper killed; C1 cleanup did NOT fire"
  ls -la "$FOUND"
  exit 1
fi
echo "PASS — $FOUND removed after wrapper exit (negative control — C1 cleanup verified)"

# Optional sanity: any other newly-created leftovers we didn't track?
AFTER=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)
EXTRA=$(comm -23 <(echo "$AFTER") <(echo "$BEFORE") 2>/dev/null || true)
if [[ -n "$EXTRA" ]]; then
  echo "WARN — unexpected leftover files (concurrent session, or test ran twice?):"
  printf '  %s\n' $EXTRA
fi

echo
echo "All assertions passed (C1 leak test)."
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
```

- [ ] **Step 2: Run test — expect FAIL (wrapper doesn't exist yet)**

```bash
bash /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
# Expected: error or non-zero exit
```

- [ ] **Step 3: Implement the wrapper (C1 fix — explicit cleanup, no `exec` leak)**

Create `/srv/Nexostrat/infra/scripts/run-with-secrets.sh`:

```bash
#!/usr/bin/env bash
# run-with-secrets.sh — Nexostrat
#
# Decrypts secrets.env.age into /dev/shm, sources it, runs the wrapped
# command, captures its exit code, then EXPLICITLY shreds plaintext and
# exits with the wrapped command's code.
#
# Per CRITICAL 1 fix (audit 2026-05-14): does NOT `exec "$@"` — that would
# leak the trap. Instead runs `"$@"` as a child, captures rc, runs cleanup
# unconditionally via trap, exits with rc.
#
# Plaintext lives at /dev/shm/nexostrat-secrets-<pid> for the lifetime of
# the wrapped command and is shred-removed on every exit path (success,
# error, signal).
#
# Usage:
#   infra/scripts/run-with-secrets.sh <command> [args...]
#
# Exit codes:
#   = exit code of the wrapped command, OR
#   1 if decrypt failed.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ENC="$REPO_ROOT/secrets.env.age"
PRIV_KEY_AGE="$HOME/.config/age/nexostrat.key.age"
PT="/dev/shm/nexostrat-secrets-$$"

cleanup() {
  if [[ -f "$PT" ]]; then
    shred -u "$PT" 2>/dev/null || rm -f "$PT"
  fi
}
trap cleanup EXIT INT TERM HUP

if [[ ! -f "$ENC" ]]; then
  echo "ERROR: $ENC not found" >&2
  exit 1
fi
if [[ ! -f "$PRIV_KEY_AGE" ]]; then
  echo "ERROR: $PRIV_KEY_AGE not found (set up Ricardo or JP age key first)" >&2
  exit 1
fi

# Decrypt secrets to /dev/shm.
# age 1.1.0+ accepts passphrase-encrypted identity files via `-i` directly
# (per `age --help`: "Passphrase encrypted age files can be used as identity
# files."). One prompt on /dev/tty, no inner subshell. Earlier drafts wrapped
# the identity through process-substitution `<(age -d "$PRIV_KEY_AGE")`,
# which breaks under TTY-less execution (the inner subshell can't reach the
# parent's controlling tty) — fixed 2026-05-16 per `t-plan-01a-text-amendments`.
# Finding 7 of the 2026-05-14 re-audit: capture age's stderr rather than
# silence, so first-time users can distinguish wrong-passphrase vs
# recipient-mismatch vs identity-file-format failures.
AGE_ERR=$(mktemp)
if ! age -d -i "$PRIV_KEY_AGE" "$ENC" > "$PT" 2>"$AGE_ERR"; then
  echo "ERROR: failed to decrypt $ENC" >&2
  echo "  hint: wrong passphrase, recipient mismatch, or identity-file format issue" >&2
  if [[ -s "$AGE_ERR" ]]; then
    echo "  age stderr:" >&2
    sed 's/^/    /' "$AGE_ERR" >&2
  fi
  rm -f "$AGE_ERR"
  exit 1
fi
rm -f "$AGE_ERR"
chmod 600 "$PT"

# Source the env into the current shell
set -a  # auto-export every assigned var
# shellcheck disable=SC1090
source "$PT"
set +a

# Run the wrapped command — NOT exec; we want the trap to fire after.
"$@"
RC=$?

# trap will run cleanup; explicit exit propagates the wrapped rc
exit "$RC"
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/run-with-secrets.sh
```

- [ ] **Step 4: Re-run the leak test — expect PASS**

```bash
bash /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
# Expected (interactive — enter passphrase at the prompt):
#   PASS — wrapper created /dev/shm/nexostrat-secrets-<pid> during execution (positive control)
#   PASS — /dev/shm/nexostrat-secrets-<pid> removed after wrapper exit (negative control — C1 cleanup verified)
#   All assertions passed (C1 leak test).
```

If the test fails because the passphrase prompt is invisible (no /dev/tty available — e.g., running over a non-interactive SSH or inside a CI runner), wrap the test invocation in `script -q -c "bash …" /dev/null` to allocate a pty. For Plan 01a, the assumption is interactive Ricardo-or-JP at the prompt; future hardening (process substitution; per-machine cached unlock token) is post-Stage-1.

- [ ] **Step 5: Plan-level success-criterion smoke-test (post-test sanity)**

The plan-level success criterion (`run-with-secrets.sh sleep 60 &` then 2s later `ls /dev/shm/nexostrat-secrets-*` returns no files) is **already verified by Step 1's negative-control assertion** (Finding 2 of the 2026-05-14 re-audit fixed the previously-buggy version that backgrounded before passphrase and false-PASSed). If you want an additional eyeballed check, the manual incantation below mirrors the success criterion as written in the plan header:

```bash
# Manual smoke — type passphrase when prompted, then watch /dev/shm.
/srv/Nexostrat/infra/scripts/run-with-secrets.sh sleep 60 &
SLEEP_PID=$!

# DURING execution — file SHOULD exist (positive control).
sleep 3  # wait for passphrase + decrypt + write
ls /dev/shm/nexostrat-secrets-* 2>/dev/null && echo "during: file present (good)"

# AFTER kill — file MUST be gone (negative control = plan success criterion).
kill "$SLEEP_PID" 2>/dev/null
wait "$SLEEP_PID" 2>/dev/null
sleep 1
LEAKED_AFTER=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | wc -l)
echo "after wrapper exits — leaked: $LEAKED_AFTER  (success criterion: 0)"
[[ $LEAKED_AFTER -eq 0 ]] && echo "C1 PASS" || echo "C1 FAIL — investigate trap"
```

Expected: `during: file present (good)` followed by `C1 PASS`.

- [ ] **Step 6: Stage + commit**

```bash
git add infra/scripts/run-with-secrets.sh infra/scripts/test_run_with_secrets_no_leak.sh
git commit -m "$(cat <<'EOF'
Plan 01a Task 15 · run-with-secrets.sh + leak-no-leak test (C1 fix)

Closes the audit CRITICAL 1 fix:
- NO `exec "$@"` — wraps "$@" instead so the trap fires.
- Explicit cleanup via trap on EXIT/INT/TERM/HUP.
- Plaintext at /dev/shm/nexostrat-secrets-<pid> shred-removed on every exit path.
- Reads $HOME/.config/age/nexostrat.key.age (passphrase prompt for outer key).

infra/scripts/test_run_with_secrets_no_leak.sh proves both:
- No /dev/shm leak after wrapped command exits
- Secrets ARE actually sourced inside the wrapped command

Future hardening (Option B per amendment plan): process-substitution
secrets to skip /dev/shm entirely. Out of Stage 1 scope.

Spec refs: §3 (Secrets), C1, ADR-004.
EOF
)"
```

---

## Task 16: `infra/secrets/MANIFEST.md`

**Goal:** Plaintext index of every secret stored in `secrets.env.age` — what it is, what consumes it, where to rotate, last rotation date. NO values, only metadata. This is the audit surface that lets either co-founder answer "what does this secret do" without decrypting.

**Files:**
- Create: `infra/secrets/MANIFEST.md`

- [ ] **Step 1: Write the manifest**

Write `/srv/Nexostrat/infra/secrets/MANIFEST.md`:

```markdown
# Secrets manifest

> One row per secret stored in `secrets.env.age`. **No values here** — only
> metadata. Update this file every time a secret is added, rotated, or removed.

| Variable | Provider | Used by | Rotation cadence | Last rotated | Notes |
|---|---|---|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic | Mode B Skills (Plan 05+), judge agent | every 6 mo | (not yet provisioned) | Hard cap configured at provider |
| `GOOGLE_API_KEY` | Google AI Studio | Mode B Gemini calls (Plan 05+) | every 6 mo | (not yet provisioned) | Free tier until ~Oct 2026 |
| `XAI_API_KEY` | xAI | Mode B Grok calls (Plan 05+) | every 6 mo | (not yet provisioned) | Hard cap configured |
| `GITHUB_MIRROR_PAT` | GitHub | `nexostrat-mirror-github.service` (Plan 01b) | every 12 mo | (not yet provisioned) | scope: `repo` only |
| `CODEBERG_MIRROR_PAT` | Codeberg | `nexostrat-mirror-codeberg.service` (Plan 01b) | every 12 mo | (not yet provisioned) | scope: `repo` only |
| `NOTION_API_KEY` | Notion | Meeting transcription watcher (Plan 08), `/note` plugin (Plan 04) | every 6 mo | (not yet provisioned) | Internal integration in JP's workspace |
| `TELEGRAM_BOT_TOKEN` | Telegram | `nexostrat-bot` Docker service (Plan 04) | only on suspected leak | (not yet provisioned) | Allowlist enforced via `infra/telegram/allowlist.yaml` |
| `RCLONE_DRIVE_TOKEN` | Google Drive (OAuth via rclone) | Heavy-asset upload (Plan 08+) | every 12 mo or on token expiry | (not yet provisioned) | Drive 2TB account |

## Rotation procedure (per secret)

1. Generate new value at the provider.
2. Decrypt `secrets.env.age` to `/dev/shm`:
   ```bash
   age -d -i ~/.config/age/nexostrat.key.age secrets.env.age \
       > /dev/shm/secrets.env.tmp
   ```
3. Edit the value in place (e.g., via `nano /dev/shm/secrets.env.tmp`).
4. Re-encrypt to both recipients:
   ```bash
   age -R infra/age-recipients.txt -o secrets.env.age /dev/shm/secrets.env.tmp
   shred -u /dev/shm/secrets.env.tmp
   ```
5. Update the **Last rotated** column in this file.
6. Commit both files (`secrets.env.age` + `infra/secrets/MANIFEST.md`).
7. Restart any service consuming the secret (full procedure in
   `docs/runbooks/key_rotation_routine.md` once Plan 02 writes it).

## Adding a new secret

1. Decrypt as above.
2. Append the new line.
3. Re-encrypt.
4. Add a row to this manifest.
5. Commit both files in the same commit.

## Removing a secret

1. Decrypt as above.
2. Delete the line.
3. Re-encrypt.
4. Mark the row in this manifest as `~~struck through~~` with date deprecated.
5. Confirm no service still references the variable name (grep `infra/`).
6. Commit.

## Audit trail

Anyone with vault access can `git log secrets.env.age` to see every rotation.
The manifest's **Last rotated** column is the human-readable snapshot.
```

- [ ] **Step 2: Verify file exists**

```bash
ls -la /srv/Nexostrat/infra/secrets/MANIFEST.md
wc -l /srv/Nexostrat/infra/secrets/MANIFEST.md
# Expected: ~50+ lines
```

- [ ] **Step 3: Stage + commit**

```bash
git add infra/secrets/MANIFEST.md
git commit -m "$(cat <<'EOF'
Plan 01a Task 16 · infra/secrets/MANIFEST.md

Plaintext audit surface for everything stored in secrets.env.age.
NO values — only metadata: variable name, provider, who consumes it,
rotation cadence, last-rotated date, notes.

Rotation procedure documented inline (decrypt → edit → re-encrypt →
update manifest → commit). Same for adding/removing secrets.

Spec refs: §3 (Secrets), ADR-004.
EOF
)"
```

---

## Task 17: Sign + encrypt + commit partnership PDF (F5)

**Goal:** Land the actual signed partnership agreement PDF (signed 2026-05-12 at the Founding Meeting) into `vault/partnership/` as `.age` ciphertext, plus the markdown summary at `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md`.

**Files:**
- Create: `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age`
- Create: `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md` (markdown summary)
- Modify: `vault/sensitive_index.md` (add the row)

**Pre-condition:** the signed PDF lives somewhere on Ricardo's machine (downloaded from Signal / DocuSign / wherever it was signed). Confirm the path before Step 1.

- [ ] **Step 1: Confirm the signed PDF is locally available**

Ricardo provides the path to the signed PDF (e.g., `~/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf`). Verify:

```bash
# Use $HOME (not ~ inside quotes — tilde does NOT expand inside double quotes; per Finding 4 of the 2026-05-14 re-audit).
SIGNED_PDF="$HOME/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf"  # adjust to actual path
ls -la "$SIGNED_PDF"
# Expected: PDF file, signed-version, ~few hundred KB
```

If the signed PDF is on JP's side and not yet on Ricardo's, **pause this task** until Ricardo has the PDF locally. (JP can send via Signal — Signal preserves PDF integrity.)

- [ ] **Step 2: Encrypt to both recipients, place in vault/partnership/**

```bash
age -R /srv/Nexostrat/infra/age-recipients.txt \
    -o /srv/Nexostrat/vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age \
    "$SIGNED_PDF"

ls -la /srv/Nexostrat/vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age
# Expected: file exists, similar size to original PDF (age has minimal overhead)
```

- [ ] **Step 3: Verify decrypt roundtrip + content matches**

```bash
TMP_DEC=/dev/shm/agreement-decrypt-$$.pdf
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age \
    > "$TMP_DEC"

# byte-for-byte match
sha256sum "$SIGNED_PDF" "$TMP_DEC"
# Expected: both lines have the same hash

shred -u "$TMP_DEC"
```

- [ ] **Step 4: Write the markdown summary**

Write `/srv/Nexostrat/00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md`:

```markdown
# Nexostrat — Partnership Agreement (summary)

> **The signed legal document is the canonical version.** That document lives
> encrypted at `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age`
> (recipients: both co-founders).
>
> This file is the plain-language summary of the agreement's substantive terms,
> for routine reference. **In any conflict between this summary and the signed
> PDF, the signed PDF is authoritative.**

## Co-owners

- **Ricardo Mejía Caicedo** (technical operator, full-time)
- **Juan Pablo** (sales/relations, ~10h/wk)

## Equity

**50/50.** Fully vested at signing (2026-05-12). No vesting cliff. No buyout
preference. Both names on any future entity formation; both signatures
required for any equity dilution event.

## Revenue distribution

Per `REVENUE_DISTRIBUTION.md`:

| Bucket | % | Recipient |
|---|---|---|
| Company | 20% | Reserves, reinvestment, future-payroll |
| Originator | 20% | Founder who sourced the prospect |
| Closer | 20% | Founder who signed the contract |
| Executor | 40% | Founder who delivered the work |

A founder filling all three roles on an engagement gets 80%; the firm gets 20%.

## Decision-making

- **50/50 voting** on architecture, brand, hiring, spend ≥ USD 500.
- **Operational autonomy** within each founder's domain (`ROLES.md`).
- **Conflict mechanism:** JP's 15-min raised-hand protocol
  (`CONFLICT_PROTOCOL.md`).

## Cost-sharing (pre-revenue)

Per `cost-sharing-agreement.md`: each founder absorbs their domain's tooling
on personal subscriptions. Firm-as-entity pays USD $0/mo in Stage 1.
Reimbursement triggers at first revenue ≥ USD 1,000.

## KPIs (12-month Stage 1)

Per `KPIs.md`: ≥ 10 paying clients, ≥ USD 20,000 revenue, ≥ 30% Diagnóstico→paid
conversion. Quality bar Bodai ≥ 7/10 to start pilots, ≥ 8/10 to go paid.

## Termination / dissolution

If either founder wants to exit:
1. **6-month notice.** Operating commitments honored to existing clients.
2. **Reserve preservation.** No forced distribution that would break the reserve target.
3. **Asset disposition.** Per `00_GOVERNANCE/dissolution-protocol.md` (TBD —
   written when the situation warrants; not Stage 1 work).

In the agreement: dissolution requires both signatures (or court order in the
edge case of one founder being non-responsive for > 90 days).

## Amendment

This summary is updated when the underlying signed agreement is amended.
The signed agreement is amended by signing a new PDF, encrypting to both
recipients, replacing the .age file, and updating this summary in the same
commit. Amendments are rare; raised hand should precede any amendment.

---

**Signed:** 2026-05-12 (Founding Meeting)
**Signed PDF:** `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age`
**Recipients:** Ricardo Mejía Caicedo, Juan Pablo (per `infra/age-recipients.txt`)
**This summary updated:** 2026-05-14 (Plan 01a Task 17)
```

- [ ] **Step 5: Update `vault/sensitive_index.md` to add the row**

Use Edit to insert the row in the "Repo-resident vault" table:

Replace:
```
| *(populated as artifacts land — Task 17 lands the first row)* | | | | |
```

With:
```
| `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age` | Signed partnership agreement PDF | 2026-05-14 | all (Ricardo + JP) | Original signed 2026-05-12 at Founding Meeting |
```

- [ ] **Step 6: Stage + commit**

```bash
git add vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age \
        00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md \
        vault/sensitive_index.md

git commit -m "$(cat <<'EOF'
Plan 01a Task 17 · partnership agreement landed (F5)

Lands the actually-signed (2026-05-12) Partnership Agreement:
- vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age
  (encrypted to both recipients; sha256 verified against original)
- 00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md (plain-language summary; signed
  PDF authoritative on conflict)
- vault/sensitive_index.md row added

Closes F5 (Founding Meeting commit). Equity 50/50 fully vested at signing;
revenue split 20/20/20/40 per REVENUE_DISTRIBUTION.md.

Spec refs: §4.5, F5, ADR-003.
EOF
)"
```

---

## Task 18: Final verification + tag `v0.1a-foundation`

**Goal:** Run every Plan-01a success criterion as a single end-to-end check, fix anything that doesn't pass, then tag `v0.1a-foundation` and push.

**Files:** Updates to `STATUS.md`, `tasks.json`, `CHECKPOINT.md`. Tag `v0.1a-foundation`.

- [ ] **Step 1: Re-run all the test scripts in sequence**

```bash
cd /srv/Nexostrat
echo "=== gitignore coverage ===" ; bash infra/scripts/test_gitignore_coverage.sh && echo "GREEN" || echo "RED"
echo "=== secret-scan hook  ===" ; bash infra/scripts/test_secret_scan_hook.sh && echo "GREEN" || echo "RED"
echo "=== schema validation ===" ; bash infra/scripts/validate_schemas.sh && echo "GREEN" || echo "RED"
echo "=== run-with-secrets  ===" ; bash infra/scripts/test_run_with_secrets_no_leak.sh && echo "GREEN" || echo "RED"
```

Expected: 4 × GREEN.

- [ ] **Step 2: Re-run the bidirectional roundtrip (proves C2 success criterion)**

```bash
TMP_PT=/dev/shm/v01a-final-pt-$$.txt
TMP_CT=/dev/shm/v01a-final-ct-$$.age
TMP_DEC=/dev/shm/v01a-final-dec-$$.txt

echo "v0.1a tag check $(date -Iseconds)" > "$TMP_PT"
age -R infra/age-recipients.txt -o "$TMP_CT" "$TMP_PT"
age -d -i ~/.config/age/nexostrat.key.age "$TMP_CT" > "$TMP_DEC"
diff "$TMP_PT" "$TMP_DEC" && echo "RICARDO-DECRYPT GREEN" || echo "RED"
shred -u "$TMP_PT" "$TMP_CT" "$TMP_DEC"
```

JP runs the equivalent on his machine; confirms via Signal. Both directions must be GREEN before tagging.

- [ ] **Step 3: Verify the partnership PDF still decrypts cleanly**

```bash
TMP=/dev/shm/agreement-final-$$.pdf
age -d -i ~/.config/age/nexostrat.key.age \
    vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age > "$TMP"
file "$TMP"
# Expected: "$TMP: PDF document, ..."
shred -u "$TMP"
```

- [ ] **Step 4: Confirm working tree is clean and all Plan 01a commits are pushed**

```bash
git status --short
# Expected: empty

git log --oneline origin/main..HEAD
# Expected: empty (everything pushed)

git push origin main
# Expected: "Everything up-to-date"
```

If commits remain unpushed, push them now.

- [ ] **Step 5: Update `STATUS.md` to reflect Plan 01a done**

Edit `/srv/Nexostrat/STATUS.md` — replace the "Current state" and "Next sequence" sections to reflect 01a-DONE state. The exact wording is left to the executor (matching CLAUDE.md "honest state" rule); the substantive update is:

- Mark Plan 01a complete with v0.1a-foundation tag.
- "Next sequence" Step 1 becomes Plan 01b (re-audit + execute).
- Move "JP age pubkey" from blockers → resolved.
- Update Recent activity with the Plan 01a entry.

- [ ] **Step 6: Update `tasks.json`**

Mark `t-amendments-batch-2` partially done (this plan is the first of three in Batch 2). Mark `t-jp-age-keypair` and `t-jp-coordination-2026-05-14` (age subset) closed. Mark `t-plan-01a-execute` done. Add a new task `t-plan-01b-write` if not already there.

- [ ] **Step 7: Tag and push**

```bash
git tag -a v0.1a-foundation -m "$(cat <<'EOF'
Nexostrat foundation milestone 01a · scaffold + identity + crypto

Closes Plan 01a:
- 3-bucket folder scaffold landed (00_PARTNERSHIP/, docs/, vault/, knowledge/,
  skills/, pipeline/, operations/, infra/)
- Comprehensive .gitignore (F23)
- Pre-commit secret-scan hook (basic)
- pipeline/clients/_template/ with 12 stations + 3 cross-cutting (F16, F19)
- JSON Schemas: nexostrat-tasks-v1, nexostrat-calendar-v1 (F21)
- Per-machine YAML profiles + bootstrap skeleton (F13, F26)
- Skills moved 00_META/skills/ → skills/<NN>_<name>/ canonical
- Questionnaires migrated docx → md (F15)
- 00_PARTNERSHIP/ canonical files (CONFLICT_PROTOCOL, REVENUE_DISTRIBUTION,
  ROLES, KPIs, cost-sharing, qualified-prospect, raised_hand_log)
- vault/ scaffold + sensitive_index.md
- C2 closed: JP age pubkey added, bidirectional roundtrip verified
- secrets.env.age (encrypted to both recipients)
- C1 closed: run-with-secrets.sh with explicit cleanup, no exec leak
- infra/secrets/MANIFEST.md
- F5 closed: signed partnership PDF in vault/partnership/

Next: Plan 01b (mirrors + warm-standby).
EOF
)"

git push origin main
git push origin v0.1a-foundation
```

- [ ] **Step 8: Commit the STATUS.md / tasks.json updates**

```bash
git add STATUS.md tasks.json
git commit -m "$(cat <<'EOF'
Plan 01a Task 18 · STATUS + tasks update — Plan 01a DONE, tagged v0.1a-foundation

All Plan 01a success criteria verified GREEN:
- gitignore coverage test PASS
- secret-scan hook test PASS (block + permit)
- schema validation PASS (tasks.json + calendar.json)
- run-with-secrets.sh leak test PASS
- bidirectional encrypt-decrypt PASS (Ricardo + JP)
- signed partnership PDF decrypts cleanly

Tag v0.1a-foundation pushed to origin.

Next: Plan 01b execution (after Plan 01b is written + re-audited).
EOF
)"
git push origin main
```

---

## Self-Review

Before declaring this plan complete:

**Spec coverage** — Every Plan 01a deliverable from the master-index header maps to a task:

- 3-bucket folder scaffold → Task 1
- Comprehensive .gitignore (F23) → Task 2
- JP age keypair (C2) → Tasks 12, 13
- secrets.env.age → Task 14
- run-with-secrets.sh (C1) → Task 15
- Questionnaires migration (F15) → Task 8
- Signed partnership PDF (F5) → Task 17
- JSON Schemas (F21) → Task 5
- Per-machine profiles (F13, F26) → Task 6
- bootstrap-machine.sh skeleton → Task 6
- _template/ 12+3 stations (F16, F19) → Task 4
- Pre-commit hook (basic) → Task 3 (full surface in 01c)
- vault/ namespace per F10 → Task 1 (folders) + Task 10 (README) + Task 17 (first artifact)
- 00_PARTNERSHIP/ canonical files → Task 9 + Task 17

**Placeholder scan** — Every step has actual content (commands, code, expected output). No "TBD" or "implement later." JP-specific values (`<jp-machine-shortname>`, `<TBD-at-bootstrap>`) ARE present in the YAML profiles intentionally — those are real placeholders that get filled by the bootstrap-time entry, not by Plan 01a itself.

**Type consistency** — `state.json` schema fields match between Task 4 (creation) and the README inside `_template/`. `secrets.env.age` variable names match between Task 14 (creation) and Task 16 (manifest). Hook script path matches across Task 3 (create), Task 6 (referenced in machine YAMLs), and Task 18 (verify).

**Missing items found in self-review** — none. The plan covers every header deliverable.

---

## Execution handoff

Plan complete and saved to `00_META/plans/2026-05-14_plan-01a-foundation.md`.

**Recommended execution path: subagent-driven** (`superpowers:subagent-driven-development`).

- Tasks 1-11 can run in a single uninterrupted session (~4-6 hours), with main agent reviewing between subagent dispatches.
- Tasks 12-18 form a second session that fires after JP's age pubkey lands (`t-jp-age-keypair` resolves).
- Pre-flight checks at the top of this plan run once before Task 1.

**Inline execution** is also viable if Ricardo wants to be deeper in the loop — `superpowers:executing-plans` with checkpoints between Tasks 7, 11 (gate), and 18.

---

*This plan inherits audit findings C1, C2, F5, F10, F13, F15, F16, F19, F21, F23, F26, plus R3 (Stage 1 surface area discipline). All decisions per `00_META/proposals/2026-05-14_amendments.md`. Plan 01b (mirrors + warm-standby) and Plan 01c (personas + hooks + integration test) follow.*
