# MIGRATION_REQUIREMENTS — Nexostrat
> Declared by: Founder persona · Date: 2026-05-29 · Consumed by: desktop root (ADR-027)

> **Migration posture (important):** Nexostrat is **already desktop-canonical**. This session
> ran ON `ricardo-desktop` (`100.104.83.2`) and confirmed HEAD `91f4fcf` (session 30) is
> committed and reachable on all three remotes (github / codeberg / gitea — all return
> `91f4fcf` as HEAD). `/srv/Nexostrat` is already a real directory, not a symlink. There is
> **NO move and NO git drain** for this folder. This manifest is therefore a DECLARE +
> verify-completeness exercise: confirm the git-invisible essentials are present on the
> desktop and that the toolchain can build the canonical deliverables here.

---

## 1. Identity
- **Target path:** `/srv/Nexostrat/` (already correct — real dir, not symlink)
- **Canonical remote (post-migration):** `git@github-nexostrat:nexostrat/nexostrat.git` (GitHub)
  - Mirrors: `git@codeberg-nexostrat:nexostrat/nexostrat.git` (Codeberg, off-site #2)
  - ⚠️ `origin` currently = Gitea `git@gitea-nexostrat:...` whose HostName resolves to
    `100.64.121.80` — **the laptop's Tailscale IP**. When the laptop goes cold (ADR-027),
    this Gitea origin dies. GitHub must become the canonical/`origin` remote on the desktop.
    See §9.
- **Runtime owner persona:** Founder (root). Sub-personas: Skills-Master (`skills/`),
  Client-Owner (`pipeline/`).

## 2. Software / runtimes required on desktop
- **OS packages:**
  - `libreoffice` / `soffice` — **PRESENT** (`/usr/bin/soffice`). Required by the docx/pptx
    "office" scripts (`skills/*/scripts/office/soffice.py`) for render + validate + pack.
  - `pandoc` — **PRESENT** (`/usr/bin/pandoc`). Used for markdown→docx/html conversion.
  - `age` — **PRESENT** (used for `secrets.env.age` decrypt; passphrase-protected identity).
  - `git`, `rsync`, standard build tools — present.
- **Language runtimes + exact versions:**
  - **Python 3.12.3** — PRESENT. (No project venv; deps live in user/system Python — see §4.)
  - **Node v24.15.0** — PRESENT. (Skill 06 deliverables generator.)
- **System services (systemd units, etc.):** **NONE.** No Nexostrat systemd units exist on
  this desktop (`systemctl list-unit-files | grep -i nexostrat` → empty). The Plan 01b mirror
  units (`nexostrat-mirror-{github,codeberg}.service`) are **not installed** — mirroring is
  currently done by direct `git push` to all three remotes over SSH, which works today.

## 3. Docker
- **Images:** NONE deployed. A FOSS-stack compose exists at `infra/docker/foss-stack/`
  (Baserow et al., Plan 02 territory) but is **not deployed** on this desktop and is out of
  scope for this migration step. The `tests/foss_stack/` suite tests the *helper code*, not a
  running container.
- **Named volumes holding STATE:** none in use.
- **Ports exposed:** none in use.
- **compose file path:** `infra/docker/foss-stack/docker-compose.yml` (dormant).

## 4. Python / Node environments (REBUILD, never copy)
- **Python:** NO venv and NO `requirements.txt` — skill scripts import from the user/system
  Python 3.12 site-packages. Desktop audit of the modules the skills import:
  - **Already present:** `python-docx` (1.1.0), `pandas` (2.1.4), `Pillow`/`PIL` (10.2.0),
    `lxml` (5.2.1), `defusedxml` (0.7.1), `pytest` (7.4.4), `pyyaml`, `requests`.
  - **MISSING — must install on desktop:** `python-pptx` (→ `import pptx`), `reportlab`,
    `jsonschema`.
    ```bash
    pip install --user python-pptx reportlab jsonschema
    ```
  - `baserow` import in `skills/shared/baserow.py` / `tests/foss_stack/` is the **local helper
    module**, not a PyPI package — no install needed.
  - Gotcha / debt: there is no pinned requirements file. Recommend authoring
    `infra/requirements.txt` capturing the above so future rebuilds are deterministic
    (tracked separately, not blocking this migration).
- **Node:** `skills/06_client_deliverables/scripts/` — lockfile/`package.json` deps are
  `docx@^9.7.1` + `pptxgenjs@^4.0.1`. **REBUILD with `npm ci`** in that dir (node_modules is
  gitignored; it is currently present on the desktop but should be rebuilt, never copied).
    ```bash
    cd skills/06_client_deliverables/scripts && npm ci
    ```

## 5. Cron / timers
- **NONE.** Nexostrat has no crontab entries and no systemd timers on this desktop. No port
  needed. (When Plans 01b/03/04 land their automation, this section updates.)

## 6. Git-invisible essentials (MUST TRANSFER via Tailscale)
All items below are **already physically present on the desktop** (confirmed this session) —
the desktop is the canonical host. Listed for completeness and so the laptop's matching copies
can be retired as cold backup. None need a laptop→desktop rsync.

| file/dir | what it is | sensitive? | transfer / rebuild |
|----------|-----------|-----------|--------------------|
| `~/.ssh/nexostrat_ed25519` (+ `.pub`) | SSH key for git@{github,codeberg,gitea}-nexostrat — powers ALL three remotes | yes | **present** (all 3 `git ls-remote` succeed). Lives in `~`, outside repo — laptop-transfer line item only if absent (it is present). |
| `~/.config/age/nexostrat.key.age` | age **master identity** (passphrase-protected). Unlocks `secrets.env.age`. 371 B. | yes (key) | **present.** Also backed up in Bitwarden per CLAUDE.md. CRITICAL: without it no firm secret decrypts. |
| `infra/age/keys/nexostrat.key.age` | second copy of the age identity (gitignored via `infra/age/keys/`) | yes (key) | **present** (in-repo path but git-invisible). |
| `secrets.env.age` | encrypted firm secrets bundle | yes | **git-TRACKED** (travels with the repo) — no separate transfer. |
| `~/.gemini/oauth_creds.json` + `google_accounts.json` + `projects.json` | Gemini CLI OAuth creds — Gemini second-seat handoff + ad-hoc transcription | yes | **present** (shared infra, not Nexostrat-owned; re-auth via `gemini` login if ever lost). |
| `operations/marketing/website-intro/` | **16 GB** video production assets (raw `.mov`/`.mp4`, edits/final `Intro V1–V5.mkv`) — gitignored via `operations/marketing/.gitignore: website-intro/*` | no | **present on desktop.** ⚠️ git-invisible, so git cannot prove the desktop copy is latest — **confirm with Ricardo no newer edit exists only on the laptop** (see §9). |
| `pipeline/clients/<slug>/transcripts/**/*.mkv` (e.g. trixx `video.mkv`, 47 MB) | client meeting recordings (plaintext per `feedback_no_vault_for_client_material`) | yes (client) | **present.** Now gitignored (this step added the rule). Raw AV stays on disk; only transcript text is committed. |
| `skills/06_client_deliverables/scripts/node_modules/` | Node deps | no | **REBUILD** via `npm ci` (do not copy). |

## 7. External dependencies / integrations
- **Git remotes:** GitHub (`github.com/nexostrat/nexostrat`), Codeberg
  (`codeberg.org/nexostrat/nexostrat`), Gitea (laptop-hosted, retiring). All reachable from
  desktop via SSH key `~/.ssh/nexostrat_ed25519`.
- **Anthropic / Google AI / xAI APIs** — keys are slots in `secrets.env.age`, **not yet
  provisioned** (Mode B Skills, Plan 05+). No live integration today.
- **GitHub/Codeberg mirror PATs** — `GITHUB_MIRROR_PAT`, `CODEBERG_MIRROR_PAT` in
  `secrets.env.age` (rotated 2026-05-16, no expiry). Only consumed by the dormant Plan 01b
  mirror services (not installed). Day-to-day pushes use the SSH key, not the PATs.
- **Telegram bot** — runs as a tenant of the Brain Bot Hub (`/srv/brain-hub/`, ADR-039); token
  slot `TELEGRAM_BOT_TOKEN` not yet provisioned. Bot *process* lives in shared hub infra, not
  here.
- **Google Drive (rclone)** — `RCLONE_DRIVE_TOKEN` slot, not yet provisioned (Plan 08+).
- No webhooks, tunnels, or DNS owned by Nexostrat at this stage.

## 8. Verification test (the gate before laptop is disabled)
Nexostrat's canonical output is the **document/deck deliverable toolchain** (the session-30
format trío + skill renderers). The gate has three parts, all run on the desktop:

```bash
cd /srv/Nexostrat

# (a) Python deliverable deps import cleanly (install the 3 missing first — see §4)
python3 -c "import docx, pptx, pandas, PIL, reportlab, lxml, defusedxml, jsonschema; print('PY DEPS OK')"

# (b) Node deliverable generator deps build + the renderer imports its libs
cd skills/06_client_deliverables/scripts && npm ci && \
  node -e "require('docx'); require('pptxgenjs'); console.log('NODE DEPS OK')"
cd /srv/Nexostrat

# (c) The skill-renderer + foss-stack helper test suite passes
python3 -m pytest tests/ -q
```

**Expected green result:** (a) prints `PY DEPS OK`; (b) prints `NODE DEPS OK`; (c) pytest
reports all tests in `tests/foss_stack/` passing (0 failed). LibreOffice (`soffice`) and
`pandoc` must be on PATH (both already present) for the docx/pptx office scripts to render.

**Bonus end-to-end (optional, manual):** generate one deliverable trío via the
`nexostrat-client-deliverables` skill against an existing refined diagnosis under
`pipeline/clients/` and confirm a valid `.pptx` + `.docx` + `.html` are produced.

## 9. Notes / gotchas
- **No move, no drain.** Desktop is already canonical at HEAD `91f4fcf`; laptop is strictly
  behind with no divergence. Do NOT re-pull or re-clone.
- **`origin` retargeting (action item for Stage D-adjacent cleanup):** `origin` = Gitea on the
  laptop (`100.64.121.80`). After the laptop goes cold, repoint `origin` → GitHub on the
  desktop, or this repo loses its `git push` default. The `github`/`codeberg` named remotes
  already work; simplest fix: `git remote set-url origin <github-url>` (or rename remotes).
- **16 GB media is git-invisible** → the only thing this audit cannot prove from git alone is
  whether `operations/marketing/website-intro/` on the desktop is the *latest* cut. The files
  are present and dated 2026-05-28; Ricardo edits/records on the desktop. **Confirm with
  Ricardo** that no newer website-intro edit lives only on the laptop before the laptop is
  retired. Everything else git-invisible (keys, creds) is identical-by-design.
- **NO brain-write path.** Nexostrat has no cron, no systemd, and no script that writes to
  `/srv/brain` or emits to a shared `events.jsonl`. The two `events.jsonl` mentions in
  `infra/scripts/{checkpoint-mtime-check,new-client}.sh` are forward-looking comments
  (Plan 03/07), not live writers. **No `~/.brain-migration-freeze` guard is needed** for
  Nexostrat — it is not one of the dual-writer paths.
- **Two untracked files handled:**
  1. `pipeline/clients/trixx-logistics/transcripts/2026-05-29/2026-05-29_10-57_pre-reunion/video.mkv`
     (47 MB meeting recording) → **gitignored** this step (heavy client media; transcript text
     is committed, raw AV is not). File stays on disk. Done.
  2. `skills/drive-download-20260529T184628Z-3-001.zip` (924 KB) → a Drive export bundle
     containing three `.skill` packages (`06 nexostrat-client-deliverables.skill`,
     `nexostrat-editorial-designer.skill`, `nexostrat-pptx-expert.skill`) whose source already
     lives in `skills/` / the installed Claude skills. **Recommend DELETE** (redundant export
     dumped at `skills/` root; not a recurring pattern, so no gitignore rule). **Flagged for
     Ricardo's explicit OK before removal** — not deleted by this step.
- **Secret rotation:** no leaked/overdue Nexostrat secret (unlike Brain's HF token). The two
  mirror PATs are uncompromised; rotation is optional hygiene, not required by this migration.
