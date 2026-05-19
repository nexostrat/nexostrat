# Plan 02a — FOSS Stack Integration (Baserow + BookStack)

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **For humans:** This file is the technical plan. The plain-language partner (`-explicado.md`) lands when Plan 02b enables the docs-pair hook.

**Goal:** Deploy Baserow + BookStack + Caddy as a self-hosted FOSS stack on HP, wire them into the existing skill pipeline + `new-client.sh`, ship backup/recovery infrastructure, and leave the API surface ready for Plan 04 (Telegram bot) to consume. After Plan 02a, scaffolding a client creates both folder + Baserow row, each skill renderer also creates a `deliverables` row, and JP's eventual Telegram-bot queries have data to read.

**Architecture:** Docker-compose stack (Baserow + BookStack + Caddy reverse-proxy) managed by a systemd unit on HP. Caddy provides TLS + subdomain routing within Tailscale only (no WAN exposure). Schema migrations are idempotent Python scripts that hit Baserow REST API. A shared helper `skills/shared/baserow.py` is the single integration point — `new-client.sh` and the 5 skill renderers all go through it. Backups are pg_dump / mysqldump piped through age-encrypt to `vault/backups/` with nightly systemd timers; warm-rsync to the second host arrives later in Plan 01b warm-standby.

**Tech Stack:** Docker · docker-compose · Baserow Community Edition (MIT) · BookStack (MIT) · Caddy 2 (Apache 2.0) · Python 3 (requests, jsonschema) · bash · age · systemd · Tailscale (already deployed).

**Plan-level success criteria (all must hold at end):**
- `docker compose up -d` in `infra/docker/foss-stack/` brings up baserow + bookstack + caddy in <60s.
- `curl -k https://baserow.nexostrat.local/health` returns 200 from any Tailscale peer; same for `https://docs.nexostrat.local/health`.
- Same URLs return connection-refused from WAN (verified via cellular network test from Ricardo's phone with Tailscale off).
- `infra/scripts/new-client.sh test-cliente MX "Test Cliente SA" "testing"` creates folder + Baserow `clients` row; running again is a clean no-op.
- Running Skill 01 on `test-cliente` writes file to `pipeline/clients/test-cliente/01_company_analysis/...` AND creates `deliverables` row in Baserow.
- `infra/scripts/baserow-reconcile.sh` run after deleting the deliverables row recreates it from the filesystem artefact.
- `infra/recovery/restore-baserow.sh $(date +%F)` against last night's backup completes in <20 min, validates schema + row integrity.
- `infra/baserow/schema/canonical.json` matches the live schema; `infra/scripts/baserow-schema-check.sh` exits 0.
- `infra/scripts/smoke-test.sh` extended version passes all 12 checks (existing 6 + new 6).
- BookStack has 4 shelves + 7 seeded pages visible via web; Ricardo can log in via email/password.
- 5 runbooks in `docs/runbooks/` cover all 12 failure modes from spec §7.2.
- Repo tagged `v0.2a-foss-stack` on the commit closing this plan.

**Manual gate:** Tasks 1-2 are fully scriptable. Task 3 is interactive — it requires logging into Baserow + BookStack web UIs to generate admin passwords + first API tokens, then committing them to `secrets.env.age`. Task 3 cannot be subagent-dispatched cleanly; execute it in the main session.

**Spec references:** [`2026-05-19_foss-stack-design.md`](../proposals/2026-05-19_foss-stack-design.md) (the design doc this plan implements). ADR-038 (Notion exit), ADR-024 (meeting capture — Whisper canonical confirmed), ADR-026 (Ollama), ADR-029 (no n8n — confirmed: this stack is Python + systemd only).

**Dependencies:**
- Hard: `v0.1-foundation` tag (Plan 01c done). ✅ satisfied.
- Hard: `vault/` working with age keys. ✅ satisfied.
- Hard: Docker + Tailscale on HP. ✅ satisfied.
- Soft: Plan 01b warm-standby Tasks 7-12. Backups stay local until second host arrives; no blocking.

**Audit-finding inheritance:** None — Plan 02a is greenfield work derived from the FOSS stack design doc. Internal risk-auditor pass can run after first commit (see § Re-audit hook below).

**Re-audit hook (2026-05-19, pre-execute):** Plan 02a invites adversarial audit by `risk-auditor` agent BEFORE executing Task 4 (first schema mutation), focusing on: API token scope/leak surface, Caddy routing correctness, Baserow upgrade-compatibility of the schema choices, idempotency of migrations. Audit report writes to `00_META/proposals/2026-05-19_plan-02a-audit-report.md`. Plan executor patches inline before continuing.

---

## File Structure

**Created in this plan:**

```
/srv/Nexostrat/
├─ infra/
│  ├─ docker/
│  │  └─ foss-stack/
│  │     ├─ docker-compose.yml                        (NEW — service definitions)
│  │     ├─ .env.example                              (NEW — env var template)
│  │     ├─ .gitignore                                (NEW — block .env + data/)
│  │     ├─ caddy/
│  │     │  └─ Caddyfile                              (NEW — reverse proxy config)
│  │     └─ data/                                     (NOT committed — runtime volumes via .gitignore)
│  │
│  ├─ systemd/
│  │  ├─ nexostrat-foss-stack.service                 (NEW — boot-on-start)
│  │  ├─ nexostrat-foss-backup.service                (NEW — nightly backup)
│  │  ├─ nexostrat-foss-backup.timer                  (NEW — 02:30 daily)
│  │  ├─ nexostrat-baserow-reconcile.service          (NEW — nightly reconcile)
│  │  ├─ nexostrat-baserow-reconcile.timer            (NEW — 03:30 daily)
│  │  ├─ nexostrat-baserow-schema-check.service       (NEW — weekly drift check)
│  │  └─ nexostrat-baserow-schema-check.timer         (NEW — Mondays 04:00)
│  │
│  ├─ baserow/
│  │  ├─ migrations/
│  │  │  ├─ __init__.py                               (NEW — empty)
│  │  │  ├─ _api.py                                   (NEW — shared API client + auth)
│  │  │  ├─ 01_clients_table.py                       (NEW — create clients table)
│  │  │  ├─ 02_meetings_table.py                      (NEW — create meetings table)
│  │  │  ├─ 03_deliverables_table.py                  (NEW — create deliverables table)
│  │  │  ├─ 04_financials_table.py                    (NEW — create financials table)
│  │  │  ├─ 05_views.py                               (NEW — create predefined views)
│  │  │  └─ run_all.py                                (NEW — orchestrate all migrations)
│  │  ├─ schema/
│  │  │  └─ canonical.json                            (NEW — schema snapshot, git-tracked)
│  │  └─ export_schema.py                             (NEW — snapshot current schema → JSON)
│  │
│  ├─ bookstack/
│  │  ├─ migrations/
│  │  │  ├─ __init__.py                               (NEW — empty)
│  │  │  ├─ _api.py                                   (NEW — shared API client + auth)
│  │  │  ├─ 01_shelves_books.py                       (NEW — create shelves + books)
│  │  │  ├─ 02_seed_pages.py                          (NEW — create 7 seeded pages)
│  │  │  └─ run_all.py                                (NEW — orchestrate)
│  │  └─ seed/
│  │     ├─ playbooks_operations_pre_meeting_checklist.md
│  │     ├─ playbooks_operations_post_meeting_protocol.md
│  │     ├─ industries_logistica_cross_border_terminos_reforma.md
│  │     ├─ industries_logistica_cross_border_mapa_competitivo.md
│  │     ├─ drafts_pricing_hoja_ruta.md
│  │     ├─ references_glossary_terminos_nexostrat.md
│  │     └─ references_templates_checklist_session_end.md
│  │
│  ├─ scripts/
│  │  ├─ backup-foss-stack.sh                         (NEW — nightly: pg_dump + mysqldump + tar uploads, age-encrypt)
│  │  ├─ baserow-reconcile.sh                         (NEW — nightly: scan filesystem, create orphan rows)
│  │  ├─ baserow-schema-check.sh                      (NEW — weekly: diff vs canonical.json)
│  │  ├─ sync-state-from-baserow.sh                   (NEW — on-demand: rebuild state.json from Baserow)
│  │  ├─ setup-foss-stack-secrets.sh                  (NEW — interactive: prompt tokens, re-encrypt secrets.env.age)
│  │  ├─ new-client.sh                                (MODIFIED — POST to Baserow after folder scaffold)
│  │  └─ smoke-test.sh                                (MODIFIED — add Baserow + BookStack + reconcile checks)
│  │
│  └─ recovery/
│     ├─ restore-baserow.sh                           (NEW — decrypt + pg_restore + restart + health-check)
│     ├─ restore-bookstack.sh                         (NEW — decrypt + mysql restore + restart + health-check)
│     └─ baserow-rotate-token.sh                      (NEW — semi-manual playbook for token rotation)
│
├─ skills/
│  ├─ shared/
│  │  ├─ baserow.py                                   (NEW — helper module ~50 LOC)
│  │  └─ tests/
│  │     └─ test_baserow.py                           (NEW — unit tests with mocked API)
│  ├─ 01_company_analyst/scripts/generate_docx.py     (MODIFIED — call post_deliverable())
│  ├─ 02_industry_analyst/scripts/generate_docx.py    (MODIFIED — same)
│  ├─ 03_competitor_analyst/scripts/generate_docx.py  (MODIFIED — same)
│  ├─ 04_discovery_meeting/scripts/generate_docx.py   (MODIFIED — same)
│  └─ 05_opportunity_report/scripts/generate_docx.py  (MODIFIED — same)
│
├─ docs/
│  └─ runbooks/
│     ├─ baserow_down.md                              (NEW — F1-F3 from spec §7.2)
│     ├─ bookstack_down.md                            (NEW — F4-F6)
│     ├─ baserow_token_compromise.md                  (NEW — F8)
│     ├─ baserow_schema_drift.md                      (NEW — F9)
│     ├─ baserow_reconcile.md                         (NEW — F11 manual trigger guide)
│     └─ hp_down.md                                    (MODIFIED — extend FOSS stack boot sequence)
│
├─ tests/
│  └─ foss_stack/
│     ├─ __init__.py                                  (NEW — empty)
│     ├─ test_baserow_health.py                       (NEW — integration: API responds)
│     ├─ test_bookstack_health.py                     (NEW — integration: API responds)
│     ├─ test_new_client_baserow.py                   (NEW — integration: scaffold → row)
│     ├─ test_skill_renderer_post.py                  (NEW — integration: render → deliverables row)
│     ├─ test_backup_restore_baserow.py               (NEW — round-trip)
│     ├─ test_backup_restore_bookstack.py             (NEW — round-trip)
│     ├─ test_schema_check_drift.py                   (NEW — synthetic drift → detection)
│     └─ test_reconcile_orphan.py                     (NEW — synthetic orphan → row created)
│
├─ vault/
│  └─ backups/                                        (NEW — runtime dir, not committed)
│     ├─ baserow/                                     (.age files written by backup script)
│     ├─ baserow-uploads/                             (.age tar.gz files)
│     ├─ bookstack/                                   (.age files)
│     └─ bookstack-uploads/                           (.age tar.gz files)
│
├─ secrets.env.age                                    (MODIFIED — add BASEROW_API_TOKEN, BASEROW_URL, BOOKSTACK_API_TOKEN, BOOKSTACK_URL)
└─ 00_META/plans/README.md                            (MODIFIED — mark Plan 02a DONE row, update plan index)
```

**Volume mapping (data NOT in git):**

| Service | Container path | Host path | Purpose |
|---|---|---|---|
| Baserow Postgres | `/baserow/data/postgres` | `infra/docker/foss-stack/data/baserow-postgres/` | DB files |
| Baserow Redis | `/data` | `infra/docker/foss-stack/data/baserow-redis/` | cache |
| Baserow media | `/baserow/data/media` | `infra/docker/foss-stack/data/baserow-media/` | uploaded files |
| BookStack app | `/config` | `infra/docker/foss-stack/data/bookstack-app/` | config + uploads + storage |
| BookStack MySQL | `/var/lib/mysql` | `infra/docker/foss-stack/data/bookstack-db/` | DB files |
| Caddy | `/data` + `/config` | `infra/docker/foss-stack/data/caddy/` | TLS certs |

`.gitignore` in `infra/docker/foss-stack/` blocks `data/` + `.env` from being committed.

---

## Task 1: Docker compose + Caddy scaffolding

**Files:**
- Create: `infra/docker/foss-stack/docker-compose.yml`
- Create: `infra/docker/foss-stack/.env.example`
- Create: `infra/docker/foss-stack/.gitignore`
- Create: `infra/docker/foss-stack/caddy/Caddyfile`
- Test: `infra/docker/foss-stack/test-compose-validates.sh` (temp test file, deleted after Step 6)

- [ ] **Step 1: Write the failing test (compose validation)**

```bash
cat > /tmp/test-compose-validates.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd /srv/Nexostrat/infra/docker/foss-stack
[ -f .env ] || cp .env.example .env
docker compose config --quiet
echo "PASS: compose validates"
EOF
chmod +x /tmp/test-compose-validates.sh
```

- [ ] **Step 2: Run test to confirm failure**

```bash
/tmp/test-compose-validates.sh
```

Expected: failure with `no such file or directory: /srv/Nexostrat/infra/docker/foss-stack`.

- [ ] **Step 3: Create directory + .gitignore**

```bash
mkdir -p /srv/Nexostrat/infra/docker/foss-stack/caddy
cat > /srv/Nexostrat/infra/docker/foss-stack/.gitignore <<'EOF'
# Runtime data — never commit
data/

# Local env file — secrets live in vault/, not here
.env
EOF
```

- [ ] **Step 4: Create `.env.example`**

```bash
cat > /srv/Nexostrat/infra/docker/foss-stack/.env.example <<'EOF'
# Copy to .env and fill before first bring-up.
# Production .env is generated by infra/scripts/setup-foss-stack-secrets.sh

# Baserow
BASEROW_PUBLIC_URL=https://baserow.nexostrat.local
BASEROW_DATABASE_PASSWORD=__GENERATE_AT_SETUP__
BASEROW_SECRET_KEY=__GENERATE_AT_SETUP__
BASEROW_JWT_SIGNING_KEY=__GENERATE_AT_SETUP__

# BookStack
BOOKSTACK_APP_URL=https://docs.nexostrat.local
BOOKSTACK_DB_PASSWORD=__GENERATE_AT_SETUP__
BOOKSTACK_DB_ROOT_PASSWORD=__GENERATE_AT_SETUP__
BOOKSTACK_APP_KEY=__GENERATE_AT_SETUP__

# Caddy — local CA, no public ACME
CADDY_LOCAL_CA=internal

# Compose project name
COMPOSE_PROJECT_NAME=nexostrat-foss
EOF
```

- [ ] **Step 5: Create `docker-compose.yml`**

```bash
cat > /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml <<'EOF'
# Nexostrat FOSS stack — Baserow + BookStack + Caddy
# Bound to 127.0.0.1 + Tailscale interface only. WAN access is firewalled.

networks:
  nexostrat_net:
    driver: bridge

volumes:
  baserow_postgres: { driver: local }
  baserow_redis: { driver: local }
  baserow_media: { driver: local }
  bookstack_app: { driver: local }
  bookstack_db: { driver: local }
  caddy_data: { driver: local }
  caddy_config: { driver: local }

services:
  baserow:
    image: baserow/baserow:1.27.2
    container_name: nexostrat-baserow
    restart: unless-stopped
    environment:
      BASEROW_PUBLIC_URL: ${BASEROW_PUBLIC_URL}
      DATABASE_PASSWORD: ${BASEROW_DATABASE_PASSWORD}
      SECRET_KEY: ${BASEROW_SECRET_KEY}
      BASEROW_JWT_SIGNING_KEY: ${BASEROW_JWT_SIGNING_KEY}
      BASEROW_EXTRA_ALLOWED_HOSTS: "baserow.nexostrat.local,baserow,localhost"
    volumes:
      - baserow_postgres:/baserow/data/postgres
      - baserow_redis:/baserow/data/redis
      - baserow_media:/baserow/data/media
    networks: [ nexostrat_net ]
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost/api/_health/"]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 60s

  bookstack:
    image: lscr.io/linuxserver/bookstack:24.10
    container_name: nexostrat-bookstack
    restart: unless-stopped
    environment:
      PUID: 1000
      PGID: 1000
      TZ: America/Tijuana
      APP_URL: ${BOOKSTACK_APP_URL}
      APP_KEY: ${BOOKSTACK_APP_KEY}
      DB_HOST: bookstack-db
      DB_PORT: 3306
      DB_DATABASE: bookstack
      DB_USERNAME: bookstack
      DB_PASSWORD: ${BOOKSTACK_DB_PASSWORD}
    volumes:
      - bookstack_app:/config
    networks: [ nexostrat_net ]
    depends_on:
      bookstack-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:80/status"]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 60s

  bookstack-db:
    image: lscr.io/linuxserver/mariadb:11.4
    container_name: nexostrat-bookstack-db
    restart: unless-stopped
    environment:
      PUID: 1000
      PGID: 1000
      TZ: America/Tijuana
      MYSQL_ROOT_PASSWORD: ${BOOKSTACK_DB_ROOT_PASSWORD}
      MYSQL_DATABASE: bookstack
      MYSQL_USER: bookstack
      MYSQL_PASSWORD: ${BOOKSTACK_DB_PASSWORD}
    volumes:
      - bookstack_db:/config
    networks: [ nexostrat_net ]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${BOOKSTACK_DB_ROOT_PASSWORD}"]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 60s

  caddy:
    image: caddy:2.8-alpine
    container_name: nexostrat-caddy
    restart: unless-stopped
    ports:
      # 127.0.0.1 + Tailscale interface only — NOT 0.0.0.0
      - "127.0.0.1:443:443"
      - "100.64.121.80:443:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    networks: [ nexostrat_net ]
    depends_on:
      - baserow
      - bookstack
EOF
```

- [ ] **Step 6: Create `Caddyfile`**

```bash
cat > /srv/Nexostrat/infra/docker/foss-stack/caddy/Caddyfile <<'EOF'
{
    # Local CA — no public ACME, no Let's Encrypt. Browsers warn until cert is
    # trusted manually per device (one-time, see docs/runbooks/foss_stack_setup.md
    # which lands in Plan 02b).
    local_certs
    auto_https disable_redirects
}

baserow.nexostrat.local {
    tls internal
    reverse_proxy baserow:80
    encode gzip
}

docs.nexostrat.local {
    tls internal
    reverse_proxy bookstack:80
    encode gzip
}
EOF
```

- [ ] **Step 7: Run validation test, expect PASS**

```bash
cd /srv/Nexostrat/infra/docker/foss-stack
cp .env.example .env  # placeholder values OK for `compose config`
/tmp/test-compose-validates.sh
rm /tmp/test-compose-validates.sh
rm .env  # do not commit, real .env is generated in Task 3
```

Expected: `PASS: compose validates`.

- [ ] **Step 8: Commit**

```bash
cd /srv/Nexostrat
git add infra/docker/foss-stack/
git commit -m "$(cat <<'EOF'
Plan 02a Task 1 · FOSS stack compose + Caddy scaffolding

Defines Baserow + BookStack + MariaDB + Caddy services with:
- Volumes mapped to host data/ (gitignored)
- Caddy local CA (no public ACME) for TLS on Tailscale-only addresses
- Healthchecks on each service for systemd readiness gates
- Bind 127.0.0.1 + 100.64.121.80 only (no 0.0.0.0)

.env stays gitignored; real values land via setup-foss-stack-secrets.sh in Task 3.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Systemd unit for stack boot-on-start

**Files:**
- Create: `infra/systemd/nexostrat-foss-stack.service`
- Test: ad-hoc shell test (no committed test file — systemd state is host-level)

- [ ] **Step 1: Write the failing test**

```bash
cat > /tmp/test-systemd-unit.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
systemctl --user-or-system cat nexostrat-foss-stack.service 2>&1 | grep -q "ExecStart=.*docker compose"
echo "PASS: unit registered with docker compose ExecStart"
EOF
chmod +x /tmp/test-systemd-unit.sh
```

- [ ] **Step 2: Run test, expect failure**

```bash
/tmp/test-systemd-unit.sh
```

Expected: `Failed to get unit file state` or similar.

- [ ] **Step 3: Create unit file**

```bash
cat > /srv/Nexostrat/infra/systemd/nexostrat-foss-stack.service <<'EOF'
[Unit]
Description=Nexostrat FOSS stack (Baserow + BookStack + Caddy)
Documentation=file:///srv/Nexostrat/00_META/proposals/2026-05-19_foss-stack-design.md
Requires=docker.service tailscaled.service
After=docker.service tailscaled.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/srv/Nexostrat/infra/docker/foss-stack
EnvironmentFile=/srv/Nexostrat/infra/docker/foss-stack/.env
ExecStartPre=/usr/bin/docker compose pull --quiet
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=300
TimeoutStopSec=120

[Install]
WantedBy=multi-user.target
EOF
```

- [ ] **Step 4: Install unit (symlink into /etc/systemd/system/)**

Manual step — requires sudo. Document the command but do not auto-execute in subagent context:

```bash
sudo ln -sf /srv/Nexostrat/infra/systemd/nexostrat-foss-stack.service /etc/systemd/system/nexostrat-foss-stack.service
sudo systemctl daemon-reload
```

- [ ] **Step 5: Verify unit registration (no start yet — .env not real)**

```bash
systemctl cat nexostrat-foss-stack.service | head -3
```

Expected: shows the `[Unit] Description=Nexostrat FOSS stack...` header.

- [ ] **Step 6: Run test, expect PASS**

```bash
sed -i 's/--user-or-system/--system/' /tmp/test-systemd-unit.sh  # adjust if first version assumed wrong flag
/tmp/test-systemd-unit.sh
rm /tmp/test-systemd-unit.sh
```

Expected: `PASS: unit registered with docker compose ExecStart`.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/systemd/nexostrat-foss-stack.service
git commit -m "$(cat <<'EOF'
Plan 02a Task 2 · systemd unit for FOSS stack boot-on-start

oneshot + RemainAfterExit=yes pattern (compose orchestrates lifecycle internally).
Requires docker + tailscaled; waits for network-online.target.
ExecStartPre pulls images so first boot doesn't surprise with multi-minute pull time.

Manual install (sudo ln + daemon-reload) documented in the task; service stays
disabled until Task 3 lands real .env.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Initial stack bring-up (interactive — main session only)

> **⚠️ MANUAL GATE:** This task requires Ricardo to interact with Baserow + BookStack web UIs in a browser. It cannot be subagent-dispatched. Execute in main session with Ricardo present.

**Files:**
- Create: `infra/scripts/setup-foss-stack-secrets.sh`
- Modify: `secrets.env.age` (decrypt, append vars, re-encrypt)

- [ ] **Step 1: Write `setup-foss-stack-secrets.sh`**

```bash
cat > /srv/Nexostrat/infra/scripts/setup-foss-stack-secrets.sh <<'EOF'
#!/usr/bin/env bash
# Interactive: generates random passwords for the FOSS stack, writes them to
# infra/docker/foss-stack/.env (host-only, gitignored) AND to secrets.env.age
# (vault, for use by skill renderers + bot Telegram).
#
# After this script: services can be brought up; user must then manually
# generate API tokens in Baserow + BookStack web UIs (Steps 6-9 of Task 3).

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
ENV_FILE="$NEXOSTRAT/infra/docker/foss-stack/.env"
SECRETS_PLAIN="$(mktemp -p /dev/shm nexostrat-secrets-XXXX.env)"
trap 'shred -u "$SECRETS_PLAIN" 2>/dev/null || rm -f "$SECRETS_PLAIN"' EXIT

if [ -f "$ENV_FILE" ]; then
    echo "WARN: $ENV_FILE already exists; refusing to overwrite. Delete it first to regenerate."
    exit 1
fi

# Helper — 32 hex chars from /dev/urandom
gen() { openssl rand -hex 32; }

BASEROW_DATABASE_PASSWORD=$(gen)
BASEROW_SECRET_KEY=$(gen)
BASEROW_JWT_SIGNING_KEY=$(gen)
BOOKSTACK_DB_PASSWORD=$(gen)
BOOKSTACK_DB_ROOT_PASSWORD=$(gen)
# BookStack APP_KEY must be base64-encoded 32-byte key for Laravel
BOOKSTACK_APP_KEY="base64:$(openssl rand -base64 32)"

cat > "$ENV_FILE" <<ENV_EOF
BASEROW_PUBLIC_URL=https://baserow.nexostrat.local
BASEROW_DATABASE_PASSWORD=$BASEROW_DATABASE_PASSWORD
BASEROW_SECRET_KEY=$BASEROW_SECRET_KEY
BASEROW_JWT_SIGNING_KEY=$BASEROW_JWT_SIGNING_KEY

BOOKSTACK_APP_URL=https://docs.nexostrat.local
BOOKSTACK_DB_PASSWORD=$BOOKSTACK_DB_PASSWORD
BOOKSTACK_DB_ROOT_PASSWORD=$BOOKSTACK_DB_ROOT_PASSWORD
BOOKSTACK_APP_KEY=$BOOKSTACK_APP_KEY

CADDY_LOCAL_CA=internal
COMPOSE_PROJECT_NAME=nexostrat-foss
ENV_EOF
chmod 600 "$ENV_FILE"
echo "Wrote $ENV_FILE (mode 600)"

# Append a Baserow + BookStack URL-only stanza to secrets.env (decrypted in shm)
# API tokens are added in Steps 6-9 of Task 3 (manual UI gen).
"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" --decrypt-to "$SECRETS_PLAIN"
if ! grep -q "^BASEROW_URL=" "$SECRETS_PLAIN"; then
    cat >> "$SECRETS_PLAIN" <<SHARED_EOF

# FOSS stack — URLs only; tokens added after web-UI gen
BASEROW_URL=https://baserow.nexostrat.local
BASEROW_API_TOKEN=__SET_AFTER_UI_GEN__
BOOKSTACK_URL=https://docs.nexostrat.local
BOOKSTACK_API_TOKEN=__SET_AFTER_UI_GEN__
BOOKSTACK_API_SECRET=__SET_AFTER_UI_GEN__
SHARED_EOF
fi
"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" --encrypt-from "$SECRETS_PLAIN"

echo "Updated secrets.env.age with stub API-token entries."
echo ""
echo "NEXT: bring up stack, then log in to Baserow + BookStack to generate tokens."
echo "  sudo systemctl start nexostrat-foss-stack.service"
echo "  Wait ~60s; check: docker compose -f $NEXOSTRAT/infra/docker/foss-stack/docker-compose.yml ps"
EOF
chmod +x /srv/Nexostrat/infra/scripts/setup-foss-stack-secrets.sh
```

> **Note on `run-with-secrets.sh --decrypt-to / --encrypt-from`:** these modes are extensions added to the existing wrapper (Plan 01a Task 15). If they do not exist, add a small patch first (Step 1b below).

- [ ] **Step 1b: If needed, extend `run-with-secrets.sh` with `--decrypt-to` / `--encrypt-from` modes**

Inspect the existing wrapper:

```bash
grep -n "case" /srv/Nexostrat/infra/scripts/run-with-secrets.sh | head -5
```

If no `--decrypt-to` flag exists, add a minimal patch:

```bash
# Insert after the existing flag parser, before the main exec branch
# (exact line numbers depend on the current wrapper version — adapt):

# Add to run-with-secrets.sh after the trap setup:
#
#   if [ "${1:-}" = "--decrypt-to" ]; then
#       age -d -i ~/.config/age/key.txt "$NEXOSTRAT/secrets.env.age" > "$2"
#       chmod 600 "$2"
#       exit 0
#   fi
#   if [ "${1:-}" = "--encrypt-from" ]; then
#       age -e -R "$NEXOSTRAT/infra/age-recipients.txt" "$2" > "$NEXOSTRAT/secrets.env.age.tmp"
#       mv "$NEXOSTRAT/secrets.env.age.tmp" "$NEXOSTRAT/secrets.env.age"
#       shred -u "$2"
#       exit 0
#   fi
```

Commit this patch separately if applied:

```bash
git add infra/scripts/run-with-secrets.sh
git commit -m "Plan 02a Task 3 pre-req · add --decrypt-to / --encrypt-from modes to run-with-secrets.sh"
```

- [ ] **Step 2: Run `setup-foss-stack-secrets.sh`**

```bash
/srv/Nexostrat/infra/scripts/setup-foss-stack-secrets.sh
```

Expected output:
```
Wrote /srv/Nexostrat/infra/docker/foss-stack/.env (mode 600)
Updated secrets.env.age with stub API-token entries.

NEXT: bring up stack, then log in to Baserow + BookStack to generate tokens.
```

- [ ] **Step 3: Verify `.env` exists + is mode 600**

```bash
ls -la /srv/Nexostrat/infra/docker/foss-stack/.env
```

Expected: `-rw-------` ownership, no group/other read.

- [ ] **Step 4: Add Tailscale hostname entries to /etc/hosts (HP + Ricardo devices)**

On HP:

```bash
echo "100.64.121.80 baserow.nexostrat.local docs.nexostrat.local" | sudo tee -a /etc/hosts
```

On Ricardo's laptop / phone Tailscale devices: add same line manually. Document this in `docs/runbooks/foss_stack_setup.md` which lands in Plan 02b (defer the runbook).

- [ ] **Step 5: Bring up the stack**

```bash
sudo systemctl enable --now nexostrat-foss-stack.service
sleep 90  # initial pull + DB init for both services
docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml ps
```

Expected: all four containers show `running (healthy)`. If any show `unhealthy`, check logs:

```bash
docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml logs --tail 50 <service>
```

- [ ] **Step 6: Generate Baserow admin account + API token (MANUAL — web UI)**

In browser on HP (or any Tailscale peer with /etc/hosts entry):
1. Navigate to `https://baserow.nexostrat.local` — accept the local-CA self-signed warning (one-time).
2. Click "Create new account." Use `ricardo@nexostrat.com`, choose a strong password (save to Ricardo's password manager — Bitwarden per ADR-004).
3. Skip the wizard prompts to create a workspace; the migration scripts (Task 4) create the Nexostrat workspace + database programmatically.
4. Top-right user menu → "Settings" → "API tokens" → "Create new token." Name it `nexostrat-internal`. Grant scope: full access to all current + future workspaces.
5. Copy the token (shown once).

- [ ] **Step 7: Generate BookStack admin account + API token (MANUAL — web UI)**

In browser:
1. Navigate to `https://docs.nexostrat.local` — accept warning.
2. Default credentials: `admin@admin.com` / `password`. Log in.
3. Settings → Users → admin user → change email to `ricardo@nexostrat.com`, change password (save to Bitwarden).
4. Settings → Users → API Tokens → "Create Token" for ricardo. Set name `nexostrat-internal`, no expiry. Copy both Token ID + Token Secret (shown once).

- [ ] **Step 8: Write tokens to `secrets.env.age`**

```bash
SECRETS_PLAIN=$(mktemp -p /dev/shm nexostrat-secrets-XXXX.env)
trap "shred -u $SECRETS_PLAIN" EXIT
/srv/Nexostrat/infra/scripts/run-with-secrets.sh --decrypt-to "$SECRETS_PLAIN"

# Replace the stub values with real ones (edit the file in place using sed)
read -rsp "Paste Baserow API token: " BASEROW_TOKEN; echo
read -rsp "Paste BookStack API Token ID: " BOOKSTACK_ID; echo
read -rsp "Paste BookStack API Token Secret: " BOOKSTACK_SECRET; echo

sed -i "s|^BASEROW_API_TOKEN=.*|BASEROW_API_TOKEN=$BASEROW_TOKEN|" "$SECRETS_PLAIN"
sed -i "s|^BOOKSTACK_API_TOKEN=.*|BOOKSTACK_API_TOKEN=$BOOKSTACK_ID|" "$SECRETS_PLAIN"
sed -i "s|^BOOKSTACK_API_SECRET=.*|BOOKSTACK_API_SECRET=$BOOKSTACK_SECRET|" "$SECRETS_PLAIN"

/srv/Nexostrat/infra/scripts/run-with-secrets.sh --encrypt-from "$SECRETS_PLAIN"
unset BASEROW_TOKEN BOOKSTACK_ID BOOKSTACK_SECRET
```

- [ ] **Step 9: Verify tokens decrypt + work**

```bash
SECRETS_PLAIN=$(mktemp -p /dev/shm nexostrat-secrets-XXXX.env)
trap "shred -u $SECRETS_PLAIN" EXIT
/srv/Nexostrat/infra/scripts/run-with-secrets.sh --decrypt-to "$SECRETS_PLAIN"
. "$SECRETS_PLAIN"

curl -sk -H "Authorization: Token $BASEROW_API_TOKEN" \
  "$BASEROW_URL/api/database/workspaces/" | head -200
```

Expected: JSON list of workspaces (likely just one default). HTTP 200.

```bash
curl -sk -H "Authorization: Token ${BOOKSTACK_API_TOKEN}:${BOOKSTACK_API_SECRET}" \
  "$BOOKSTACK_URL/api/docs.json" | head -10
```

Expected: JSON docs index. HTTP 200.

- [ ] **Step 10: Commit setup script (only — `.env` and tokens never enter git)**

```bash
cd /srv/Nexostrat
git add infra/scripts/setup-foss-stack-secrets.sh
git add secrets.env.age  # the encrypted blob, safe to commit
git commit -m "$(cat <<'EOF'
Plan 02a Task 3 · stack bring-up + admin tokens in secrets.env.age

setup-foss-stack-secrets.sh generates random Postgres/MySQL/Laravel keys,
writes plaintext .env to host (mode 600, gitignored), appends URL + token
stubs to secrets.env.age.

Manual web-UI steps generate Baserow + BookStack admin accounts + API tokens;
tokens replace stubs via interactive sed pipeline.

Verified tokens authenticate: GET /api/database/workspaces returns 200 (Baserow),
GET /api/docs.json returns 200 (BookStack).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Baserow schema migrations — 4 tables

**Files:**
- Create: `infra/baserow/migrations/__init__.py`
- Create: `infra/baserow/migrations/_api.py`
- Create: `infra/baserow/migrations/01_clients_table.py`
- Create: `infra/baserow/migrations/02_meetings_table.py`
- Create: `infra/baserow/migrations/03_deliverables_table.py`
- Create: `infra/baserow/migrations/04_financials_table.py`
- Create: `infra/baserow/migrations/run_all.py`
- Test: `tests/foss_stack/test_migrations_idempotent.py`

- [ ] **Step 1: Write the failing test (idempotency)**

```bash
mkdir -p /srv/Nexostrat/tests/foss_stack
cat > /srv/Nexostrat/tests/foss_stack/__init__.py <<'EOF'
EOF
cat > /srv/Nexostrat/tests/foss_stack/test_migrations_idempotent.py <<'EOF'
"""Run migrations twice. Second run must be a clean no-op."""
import subprocess, os, json
import pytest

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")

def run_migrations():
    return subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
         "python3", f"{NEXOSTRAT}/infra/baserow/migrations/run_all.py"],
        capture_output=True, text=True, check=False
    )

def test_first_run_creates_tables():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"
    assert "created" in r.stdout.lower() or "exists" in r.stdout.lower()

def test_second_run_is_noop():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"
    # No new "created" lines, only "exists, skipping" lines
    assert r.stdout.count("CREATED") == 0
    assert r.stdout.count("EXISTS") >= 4  # at least 4 tables
EOF
```

- [ ] **Step 2: Run test, expect failure (module not found)**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_migrations_idempotent.py -v
```

Expected: `ModuleNotFoundError` or `FileNotFoundError` on the migration script.

- [ ] **Step 3: Write shared API client `_api.py`**

```bash
mkdir -p /srv/Nexostrat/infra/baserow/migrations
cat > /srv/Nexostrat/infra/baserow/migrations/__init__.py <<'EOF'
EOF
cat > /srv/Nexostrat/infra/baserow/migrations/_api.py <<'EOF'
"""Thin Baserow REST client for schema migrations. Loads token from env."""
import os, sys, json, time, urllib.request, urllib.error, ssl

BASE_URL = os.environ["BASEROW_URL"]
TOKEN = os.environ["BASEROW_API_TOKEN"]

# Caddy local CA — verify against system trust store if Caddy CA is trusted,
# otherwise allow unverified (Tailscale-only network is the security boundary).
_CTX = ssl.create_default_context()
if os.environ.get("BASEROW_INSECURE_TLS", "1") == "1":
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE


def _req(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=_CTX, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {body}") from e


def get(path: str) -> dict: return _req("GET", path)
def post(path: str, body: dict) -> dict: return _req("POST", path, body)
def patch(path: str, body: dict) -> dict: return _req("PATCH", path, body)


def get_or_create_workspace(name: str = "Nexostrat") -> int:
    """Returns workspace_id."""
    workspaces = get("/api/database/workspaces/")
    for w in workspaces:
        if w["name"] == name:
            print(f"WORKSPACE EXISTS: {name} (id={w['id']})")
            return w["id"]
    result = post("/api/database/workspaces/", {"name": name})
    print(f"WORKSPACE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_or_create_database(workspace_id: int, name: str = "nexostrat") -> int:
    """Returns database_id (called 'application' in Baserow API)."""
    apps = get(f"/api/applications/workspace/{workspace_id}/")
    for app in apps:
        if app["name"] == name and app["type"] == "database":
            print(f"DATABASE EXISTS: {name} (id={app['id']})")
            return app["id"]
    result = post(
        f"/api/applications/workspace/{workspace_id}/",
        {"name": name, "type": "database"}
    )
    print(f"DATABASE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_or_create_table(database_id: int, name: str) -> int:
    """Returns table_id. Does NOT create fields — caller adds via add_field()."""
    tables = get(f"/api/database/tables/database/{database_id}/")
    for t in tables:
        if t["name"] == name:
            print(f"TABLE EXISTS: {name} (id={t['id']})")
            return t["id"]
    result = post(
        f"/api/database/tables/database/{database_id}/",
        {"name": name, "data": [], "first_row_header": False}
    )
    print(f"TABLE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_fields(table_id: int) -> list[dict]:
    return get(f"/api/database/fields/table/{table_id}/")


def add_field(table_id: int, spec: dict) -> int:
    """spec example: {'name': 'slug', 'type': 'text'}.
       Returns field_id. Skips if a field with same name exists."""
    existing = {f["name"]: f["id"] for f in get_fields(table_id)}
    if spec["name"] in existing:
        print(f"  FIELD EXISTS: {spec['name']}")
        return existing[spec["name"]]
    result = post(f"/api/database/fields/table/{table_id}/", spec)
    print(f"  FIELD CREATED: {spec['name']} ({spec['type']})")
    return result["id"]
EOF
```

- [ ] **Step 4: Write `01_clients_table.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/01_clients_table.py <<'EOF'
"""Create the `clients` table per spec §4.1."""
from _api import get_or_create_workspace, get_or_create_database, get_or_create_table, add_field


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    tid = get_or_create_table(db, "clients")

    add_field(tid, {"name": "slug", "type": "text"})
    add_field(tid, {"name": "name", "type": "text"})
    add_field(tid, {"name": "display_name", "type": "text"})
    add_field(tid, {"name": "country", "type": "single_select",
                    "select_options": [{"value": "CO", "color": "blue"},
                                       {"value": "MX", "color": "green"}]})
    add_field(tid, {"name": "rfc_nit", "type": "text"})
    add_field(tid, {"name": "sector", "type": "text"})
    add_field(tid, {"name": "phase", "type": "single_select",
                    "select_options": [
                        {"value": "prospect", "color": "gray"},
                        {"value": "intake", "color": "blue"},
                        {"value": "diagnostico_in_progress", "color": "yellow"},
                        {"value": "diagnostico_delivered", "color": "cyan"},
                        {"value": "roadmap_offered", "color": "orange"},
                        {"value": "roadmap_in_progress", "color": "red"},
                        {"value": "retainer_active", "color": "green"},
                        {"value": "dormant", "color": "dark-gray"}
                    ]})
    add_field(tid, {"name": "pilot", "type": "boolean"})
    add_field(tid, {"name": "source", "type": "single_select",
                    "select_options": [
                        {"value": "inbound", "color": "blue"},
                        {"value": "outbound", "color": "orange"},
                        {"value": "referido", "color": "green"},
                        {"value": "marketing", "color": "purple"}
                    ]})
    add_field(tid, {"name": "decisor_name", "type": "text"})
    add_field(tid, {"name": "decisor_role", "type": "text"})
    add_field(tid, {"name": "contact_name", "type": "text"})
    add_field(tid, {"name": "contact_phone", "type": "text"})
    add_field(tid, {"name": "contact_email", "type": "email"})
    add_field(tid, {"name": "folder_path", "type": "formula",
                    "formula": "concat('pipeline/clients/', field('slug'), '/')"})
    add_field(tid, {"name": "created_at", "type": "created_on"})
    add_field(tid, {"name": "updated_at", "type": "last_modified"})

    print(f"clients table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 5: Write `02_meetings_table.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/02_meetings_table.py <<'EOF'
"""Create the `meetings` table per spec §4.2."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field, get_fields)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")  # ensure clients exists for link
    tid = get_or_create_table(db, "meetings")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})
    add_field(tid, {"name": "date", "type": "date",
                    "date_format": "ISO", "date_include_time": True,
                    "date_time_format": "24"})
    add_field(tid, {"name": "location", "type": "text"})
    add_field(tid, {"name": "kind", "type": "single_select",
                    "select_options": [
                        {"value": "discovery", "color": "blue"},
                        {"value": "feedback", "color": "cyan"},
                        {"value": "roadmap_kickoff", "color": "orange"},
                        {"value": "check_in", "color": "yellow"},
                        {"value": "internal_r_jp", "color": "purple"}
                    ]})
    add_field(tid, {"name": "attendees_text", "type": "long_text"})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "planned", "color": "gray"},
                        {"value": "confirmed", "color": "blue"},
                        {"value": "recorded", "color": "yellow"},
                        {"value": "transcribed", "color": "cyan"},
                        {"value": "extracted", "color": "green"},
                        {"value": "cancelled", "color": "red"}
                    ]})
    add_field(tid, {"name": "recording_path", "type": "text"})
    add_field(tid, {"name": "transcript_path", "type": "text"})
    add_field(tid, {"name": "notes_path", "type": "text"})
    add_field(tid, {"name": "duration_min", "type": "number",
                    "number_decimal_places": 0})
    add_field(tid, {"name": "created_at", "type": "created_on"})

    print(f"meetings table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 6: Write `03_deliverables_table.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/03_deliverables_table.py <<'EOF'
"""Create the `deliverables` table per spec §4.3."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")
    tid = get_or_create_table(db, "deliverables")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})
    add_field(tid, {"name": "skill", "type": "single_select",
                    "select_options": [
                        {"value": "company-analyst", "color": "blue"},
                        {"value": "industry-analyst", "color": "cyan"},
                        {"value": "competitor-analyst", "color": "purple"},
                        {"value": "discovery-meeting", "color": "yellow"},
                        {"value": "opportunity-report", "color": "green"}
                    ]})
    add_field(tid, {"name": "file_md", "type": "text"})
    add_field(tid, {"name": "file_docx", "type": "text"})
    add_field(tid, {"name": "file_pdf", "type": "text"})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "draft", "color": "gray"},
                        {"value": "internal_review", "color": "yellow"},
                        {"value": "delivered", "color": "green"},
                        {"value": "revised", "color": "orange"}
                    ]})
    add_field(tid, {"name": "created_at", "type": "created_on"})
    add_field(tid, {"name": "delivered_at", "type": "date",
                    "date_format": "ISO", "date_include_time": False})
    add_field(tid, {"name": "delivered_via", "type": "single_select",
                    "select_options": [
                        {"value": "email", "color": "blue"},
                        {"value": "whatsapp", "color": "green"},
                        {"value": "in_person", "color": "purple"},
                        {"value": "not_yet", "color": "gray"}
                    ]})

    print(f"deliverables table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 7: Write `04_financials_table.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/04_financials_table.py <<'EOF'
"""Create the `financials` table per spec §4.4."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")
    tid = get_or_create_table(db, "financials")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})  # nullable in Baserow link_row
    add_field(tid, {"name": "kind", "type": "single_select",
                    "select_options": [
                        {"value": "income", "color": "green"},
                        {"value": "expense", "color": "red"}
                    ]})
    add_field(tid, {"name": "amount", "type": "number",
                    "number_decimal_places": 2})
    add_field(tid, {"name": "currency", "type": "single_select",
                    "select_options": [
                        {"value": "MXN", "color": "green"},
                        {"value": "COP", "color": "yellow"},
                        {"value": "USD", "color": "blue"}
                    ]})
    add_field(tid, {"name": "date", "type": "date",
                    "date_format": "ISO", "date_include_time": False})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "pending", "color": "gray"},
                        {"value": "received", "color": "green"},
                        {"value": "paid", "color": "blue"},
                        {"value": "cancelled", "color": "red"}
                    ]})
    add_field(tid, {"name": "description", "type": "text"})
    add_field(tid, {"name": "invoice_path", "type": "text"})

    print(f"financials table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 8: Write orchestrator `run_all.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/run_all.py <<'EOF'
"""Run all Baserow migrations in order. Idempotent."""
import sys, importlib.util, pathlib

HERE = pathlib.Path(__file__).parent


def import_module_from_path(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    sys.path.insert(0, str(HERE))  # so each migration can `from _api import ...`
    migrations = sorted(p for p in HERE.glob("[0-9][0-9]_*.py") if p.is_file())
    for path in migrations:
        print(f"--- {path.name} ---")
        mod = import_module_from_path(path.stem, path)
        mod.run()
    print("\nAll migrations complete.")


if __name__ == "__main__":
    main()
EOF
```

- [ ] **Step 9: Run migrations, expect all 4 tables created**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/baserow/migrations/run_all.py
```

Expected output (first run):
```
--- 01_clients_table.py ---
WORKSPACE EXISTS: Nexostrat (id=1)
DATABASE CREATED: nexostrat (id=N)
TABLE CREATED: clients (id=M)
  FIELD CREATED: slug (text)
  ...
clients table ready (id=M)
--- 02_meetings_table.py ---
...
All migrations complete.
```

- [ ] **Step 10: Re-run migrations, expect no-op**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/baserow/migrations/run_all.py
```

Expected: every line says `EXISTS`, no `CREATED`. Final line `All migrations complete.`

- [ ] **Step 11: Run pytest, expect PASS on both tests**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_migrations_idempotent.py -v
```

Expected: 2 passed.

- [ ] **Step 12: Commit**

```bash
cd /srv/Nexostrat
git add infra/baserow/migrations/ tests/foss_stack/__init__.py tests/foss_stack/test_migrations_idempotent.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 4 · Baserow schema — 4 tables (clients, meetings, deliverables, financials)

_api.py wraps urllib for Baserow REST with get/post/patch + helpers
get_or_create_{workspace,database,table} + add_field.

01-04 migration scripts create each table per spec §4.1-4.4 with idempotent
field creation (skip if name match). run_all.py orchestrates sorted glob.

test_migrations_idempotent.py asserts first run creates, second run is no-op.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Baserow predefined views

**Files:**
- Create: `infra/baserow/migrations/05_views.py`
- Modify: `infra/baserow/migrations/run_all.py` (no change needed — globs `[0-9][0-9]_*.py`)
- Test: `tests/foss_stack/test_views_present.py`

- [ ] **Step 1: Write failing test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_views_present.py <<'EOF'
"""After running views migration, each table has the predefined views."""
import os, json, urllib.request, ssl, pytest

BASE_URL = os.environ["BASEROW_URL"]
TOKEN = os.environ["BASEROW_API_TOKEN"]

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    req.add_header("Authorization", f"Token {TOKEN}")
    with urllib.request.urlopen(req, context=_CTX, timeout=30) as r:
        return json.loads(r.read())


def _table_id(name):
    ws = _get("/api/database/workspaces/")[0]["id"]
    apps = _get(f"/api/applications/workspace/{ws}/")
    db = next(a for a in apps if a["name"] == "nexostrat" and a["type"] == "database")
    tables = _get(f"/api/database/tables/database/{db['id']}/")
    return next(t for t in tables if t["name"] == name)["id"]


@pytest.mark.parametrize("table,expected_views", [
    ("clients",      ["Pipeline activo", "Pilotos", "Por país"]),
    ("meetings",     ["Próximas", "Esta semana", "Pendientes de transcripción"]),
    ("deliverables", ["Esta semana", "En revisión interna", "Por skill"]),
    ("financials",   ["Mes en curso", "Por cobrar"]),
])
def test_views_exist(table, expected_views):
    tid = _table_id(table)
    views = _get(f"/api/database/views/table/{tid}/")
    names = {v["name"] for v in views}
    for v in expected_views:
        assert v in names, f"{table} missing view: {v}. Got: {names}"
EOF
```

- [ ] **Step 2: Run test, expect failure (views don't exist yet)**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest /srv/Nexostrat/tests/foss_stack/test_views_present.py -v
```

Expected: failures on all 4 parametrized cases.

- [ ] **Step 3: Write `05_views.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/migrations/05_views.py <<'EOF'
"""Create predefined views per spec §4.5. Idempotent."""
from _api import get, post, get_or_create_workspace, get_or_create_database


def _table_id(database_id: int, name: str) -> int:
    tables = get(f"/api/database/tables/database/{database_id}/")
    return next(t for t in tables if t["name"] == name)["id"]


def _field_id(table_id: int, name: str) -> int:
    fields = get(f"/api/database/fields/table/{table_id}/")
    return next(f for f in fields if f["name"] == name)["id"]


def _ensure_view(table_id: int, view_name: str, view_type: str,
                 filters: list[dict] | None = None,
                 sortings: list[dict] | None = None) -> int:
    existing = get(f"/api/database/views/table/{table_id}/")
    for v in existing:
        if v["name"] == view_name:
            print(f"  VIEW EXISTS: {view_name}")
            return v["id"]
    payload = {"name": view_name, "type": view_type,
               "filter_type": "AND", "filters_disabled": False}
    result = post(f"/api/database/views/table/{table_id}/", payload)
    vid = result["id"]
    for f in (filters or []):
        post(f"/api/database/views/{vid}/filters/", f)
    for s in (sortings or []):
        post(f"/api/database/views/{vid}/sortings/", s)
    print(f"  VIEW CREATED: {view_name}")
    return vid


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")

    # ---- clients ----
    clients_tid = _table_id(db, "clients")
    phase_fid = _field_id(clients_tid, "phase")
    pilot_fid = _field_id(clients_tid, "pilot")
    country_fid = _field_id(clients_tid, "country")
    print("clients views:")
    _ensure_view(clients_tid, "Pipeline activo", "grid",
                 filters=[{"field": phase_fid, "type": "not_equal", "value": "dormant"}])
    _ensure_view(clients_tid, "Pilotos", "grid",
                 filters=[{"field": pilot_fid, "type": "boolean", "value": "true"}])
    _ensure_view(clients_tid, "Por país", "grid")  # grouping via UI; filter not required

    # ---- meetings ----
    meetings_tid = _table_id(db, "meetings")
    date_fid = _field_id(meetings_tid, "date")
    mstatus_fid = _field_id(meetings_tid, "status")
    print("meetings views:")
    _ensure_view(meetings_tid, "Próximas", "grid",
                 filters=[{"field": date_fid, "type": "date_after_today", "value": ""}],
                 sortings=[{"field": date_fid, "order": "ASC"}])
    _ensure_view(meetings_tid, "Esta semana", "grid",
                 filters=[{"field": date_fid, "type": "date_within_days", "value": "7"}])
    _ensure_view(meetings_tid, "Pendientes de transcripción", "grid",
                 filters=[{"field": mstatus_fid, "type": "single_select_equal", "value": "recorded"}])

    # ---- deliverables ----
    deliv_tid = _table_id(db, "deliverables")
    created_fid = _field_id(deliv_tid, "created_at")
    dstatus_fid = _field_id(deliv_tid, "status")
    skill_fid = _field_id(deliv_tid, "skill")
    print("deliverables views:")
    _ensure_view(deliv_tid, "Esta semana", "grid",
                 filters=[{"field": created_fid, "type": "date_within_days", "value": "7"}])
    _ensure_view(deliv_tid, "En revisión interna", "grid",
                 filters=[{"field": dstatus_fid, "type": "single_select_equal", "value": "internal_review"}])
    _ensure_view(deliv_tid, "Por skill", "grid")  # grouping via UI

    # ---- financials ----
    fin_tid = _table_id(db, "financials")
    fdate_fid = _field_id(fin_tid, "date")
    fstatus_fid = _field_id(fin_tid, "status")
    fkind_fid = _field_id(fin_tid, "kind")
    print("financials views:")
    _ensure_view(fin_tid, "Mes en curso", "grid",
                 filters=[{"field": fdate_fid, "type": "date_within_days", "value": "30"}])
    _ensure_view(fin_tid, "Por cobrar", "grid",
                 filters=[{"field": fkind_fid, "type": "single_select_equal", "value": "income"},
                          {"field": fstatus_fid, "type": "single_select_equal", "value": "pending"}])


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 4: Run views migration**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/baserow/migrations/05_views.py
```

Expected: 11 `VIEW CREATED` lines (3 + 3 + 3 + 2).

- [ ] **Step 5: Re-run, expect no-op**

Expected: 11 `VIEW EXISTS` lines.

- [ ] **Step 6: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_views_present.py -v
```

Expected: 4 passed.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/baserow/migrations/05_views.py tests/foss_stack/test_views_present.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 5 · Baserow predefined views

11 views per spec §4.5 across 4 tables:
- clients: Pipeline activo, Pilotos, Por país
- meetings: Próximas, Esta semana, Pendientes de transcripción
- deliverables: Esta semana, En revisión interna, Por skill
- financials: Mes en curso, Por cobrar

Filter syntax uses Baserow's typed filter API (date_after_today, date_within_days,
single_select_equal). Idempotent — re-runs are no-ops.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Schema snapshot + canonical.json + weekly drift check

**Files:**
- Create: `infra/baserow/export_schema.py`
- Create: `infra/baserow/schema/canonical.json`
- Create: `infra/scripts/baserow-schema-check.sh`
- Create: `infra/systemd/nexostrat-baserow-schema-check.service`
- Create: `infra/systemd/nexostrat-baserow-schema-check.timer`
- Test: `tests/foss_stack/test_schema_check_drift.py`

- [ ] **Step 1: Write failing drift-detection test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_schema_check_drift.py <<'EOF'
"""Synthetic schema drift → check script must detect."""
import subprocess, os, json, tempfile, pathlib

NEXOSTRAT = "/srv/Nexostrat"


def test_clean_schema_passes():
    """If canonical.json matches live schema, exit 0."""
    r = subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/baserow-schema-check.sh"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, f"stderr={r.stderr}"


def test_drift_detected(tmp_path):
    """Mutate canonical.json (simulate drift), check script must exit non-zero."""
    canonical = pathlib.Path(f"{NEXOSTRAT}/infra/baserow/schema/canonical.json")
    backup = tmp_path / "canonical.backup.json"
    backup.write_text(canonical.read_text())
    try:
        data = json.loads(canonical.read_text())
        # Inject fake field into clients
        data["tables"]["clients"]["fields"].append(
            {"name": "FAKE_DRIFT_FIELD", "type": "text"}
        )
        canonical.write_text(json.dumps(data, indent=2, sort_keys=True))
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/baserow-schema-check.sh"],
            capture_output=True, text=True
        )
        assert r.returncode != 0, "drift should have been detected"
        assert "FAKE_DRIFT_FIELD" in (r.stdout + r.stderr)
    finally:
        canonical.write_text(backup.read_text())
EOF
```

- [ ] **Step 2: Run test, expect failure (script missing)**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_schema_check_drift.py -v
```

Expected: `FileNotFoundError` on the check script.

- [ ] **Step 3: Write `export_schema.py`**

```bash
cat > /srv/Nexostrat/infra/baserow/export_schema.py <<'EOF'
"""Dump live Baserow schema to JSON (sorted, deterministic)."""
import json, sys, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "migrations"))
from _api import get


def dump_schema(workspace_name="Nexostrat", database_name="nexostrat") -> dict:
    workspaces = get("/api/database/workspaces/")
    ws = next(w for w in workspaces if w["name"] == workspace_name)
    apps = get(f"/api/applications/workspace/{ws['id']}/")
    db = next(a for a in apps if a["name"] == database_name and a["type"] == "database")
    tables = get(f"/api/database/tables/database/{db['id']}/")

    schema = {"workspace": workspace_name, "database": database_name, "tables": {}}
    for t in sorted(tables, key=lambda x: x["name"]):
        fields = get(f"/api/database/fields/table/{t['id']}/")
        # Strip API ids — they're not stable across re-creation. Keep name + type.
        clean_fields = []
        for f in sorted(fields, key=lambda x: x["name"]):
            cf = {"name": f["name"], "type": f["type"]}
            if f.get("select_options"):
                cf["select_options"] = sorted(
                    [{"value": o["value"]} for o in f["select_options"]],
                    key=lambda o: o["value"]
                )
            if f.get("formula"):
                cf["formula"] = f["formula"]
            clean_fields.append(cf)
        # Views — names only, no IDs
        views = get(f"/api/database/views/table/{t['id']}/")
        view_names = sorted(v["name"] for v in views)
        schema["tables"][t["name"]] = {"fields": clean_fields, "views": view_names}
    return schema


def main():
    schema = dump_schema()
    out = pathlib.Path(__file__).parent / "schema" / "canonical.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
EOF
```

- [ ] **Step 4: Run export to produce initial canonical.json**

```bash
mkdir -p /srv/Nexostrat/infra/baserow/schema
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/baserow/export_schema.py
```

Expected: `Wrote /srv/Nexostrat/infra/baserow/schema/canonical.json`

Inspect the output — should be deterministic JSON with 4 tables, each with `fields` + `views` arrays.

```bash
head -40 /srv/Nexostrat/infra/baserow/schema/canonical.json
```

- [ ] **Step 5: Write `baserow-schema-check.sh`**

```bash
cat > /srv/Nexostrat/infra/scripts/baserow-schema-check.sh <<'EOF'
#!/usr/bin/env bash
# Compare live Baserow schema to infra/baserow/schema/canonical.json.
# Exit 0 = clean, non-zero = drift detected (alerts Telegram via Plan 04 when wired).

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
CANONICAL="$NEXOSTRAT/infra/baserow/schema/canonical.json"
TMP_LIVE=$(mktemp)
trap "rm -f $TMP_LIVE" EXIT

"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" \
  python3 -c "
import sys, json, pathlib
sys.path.insert(0, '$NEXOSTRAT/infra/baserow')
from export_schema import dump_schema
print(json.dumps(dump_schema(), indent=2, sort_keys=True))
" > "$TMP_LIVE"

if diff -u "$CANONICAL" "$TMP_LIVE"; then
    echo "OK: schema matches canonical.json"
    exit 0
else
    echo "DRIFT DETECTED — see diff above" >&2
    exit 1
fi
EOF
chmod +x /srv/Nexostrat/infra/scripts/baserow-schema-check.sh
```

- [ ] **Step 6: Run check, expect clean**

```bash
/srv/Nexostrat/infra/scripts/baserow-schema-check.sh
```

Expected: `OK: schema matches canonical.json` and exit 0.

- [ ] **Step 7: Write systemd timer + service**

```bash
cat > /srv/Nexostrat/infra/systemd/nexostrat-baserow-schema-check.service <<'EOF'
[Unit]
Description=Nexostrat — weekly Baserow schema drift check
After=nexostrat-foss-stack.service

[Service]
Type=oneshot
User=ricardo
WorkingDirectory=/srv/Nexostrat
ExecStart=/srv/Nexostrat/infra/scripts/baserow-schema-check.sh
StandardOutput=journal
StandardError=journal
EOF

cat > /srv/Nexostrat/infra/systemd/nexostrat-baserow-schema-check.timer <<'EOF'
[Unit]
Description=Nexostrat — weekly Baserow schema drift check (Mondays 04:00)

[Timer]
OnCalendar=Mon *-*-* 04:00:00
Persistent=true
Unit=nexostrat-baserow-schema-check.service

[Install]
WantedBy=timers.target
EOF
```

Install (manual sudo step):

```bash
sudo ln -sf /srv/Nexostrat/infra/systemd/nexostrat-baserow-schema-check.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nexostrat-baserow-schema-check.timer
systemctl list-timers nexostrat-baserow-schema-check.timer
```

Expected: `list-timers` shows the unit with next-run timestamp.

- [ ] **Step 8: Run pytest, expect both tests PASS**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_schema_check_drift.py -v
```

Expected: 2 passed.

- [ ] **Step 9: Commit**

```bash
cd /srv/Nexostrat
git add infra/baserow/export_schema.py \
        infra/baserow/schema/canonical.json \
        infra/scripts/baserow-schema-check.sh \
        infra/systemd/nexostrat-baserow-schema-check.{service,timer} \
        tests/foss_stack/test_schema_check_drift.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 6 · Baserow schema snapshot + weekly drift check

export_schema.py dumps live Baserow schema to canonical.json (sorted JSON,
field names + types + select option values + view names; strips API IDs which
are not stable across re-creation).

baserow-schema-check.sh diffs live vs canonical, exits non-zero on drift.

Weekly systemd timer (Mondays 04:00) runs the check; output goes to journal.
Plan 04 wires Telegram alert when the unit fails.

test_schema_check_drift.py asserts: (a) clean match passes, (b) synthetic
canonical mutation is detected.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: `skills/shared/baserow.py` helper module

**Files:**
- Create: `skills/shared/baserow.py`
- Create: `skills/shared/tests/__init__.py`
- Create: `skills/shared/tests/test_baserow.py`

- [ ] **Step 1: Write failing unit tests with mocked API**

```bash
mkdir -p /srv/Nexostrat/skills/shared/tests
cat > /srv/Nexostrat/skills/shared/tests/__init__.py <<'EOF'
EOF
cat > /srv/Nexostrat/skills/shared/tests/test_baserow.py <<'EOF'
"""Unit tests for skills/shared/baserow.py with mocked HTTP."""
from unittest.mock import patch, MagicMock
import pytest, os, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
os.environ.setdefault("BASEROW_URL", "https://baserow.test")
os.environ.setdefault("BASEROW_API_TOKEN", "dummy")

import baserow


@patch("baserow._request")
def test_post_client_new(mock_req):
    """post_client on a new slug → POST a row."""
    # Sequence: lookup table id, look for existing client (none), post new
    mock_req.side_effect = [
        {"results": [{"id": 1, "name": "clients"}]},   # _table_id lookup -> clients
        {"results": []},                                 # find_client_by_slug -> empty
        {"id": 42, "slug": "trixx"},                     # POST new row
    ]
    row_id = baserow.post_client(
        slug="trixx", name="Trixx Logistics SA", display_name="Trixx",
        country="MX", sector="logística", pilot=True, source="referido"
    )
    assert row_id == 42


@patch("baserow._request")
def test_post_client_idempotent(mock_req):
    """post_client on existing slug → return existing id, no POST."""
    mock_req.side_effect = [
        {"results": [{"id": 1, "name": "clients"}]},
        {"results": [{"id": 99, "slug": "trixx"}]},   # exists
    ]
    row_id = baserow.post_client(slug="trixx", name="x", display_name="x",
                                  country="MX", sector="x", pilot=False, source="inbound")
    assert row_id == 99


@patch("baserow._request")
def test_post_deliverable_new(mock_req):
    mock_req.side_effect = [
        {"results": [{"id": 2, "name": "deliverables"}]},
        {"results": []},
        {"id": 7},
    ]
    row_id = baserow.post_deliverable(
        client_id=42, skill="company-analyst",
        file_md="pipeline/clients/trixx/01.../foo.md",
        file_docx="...foo.docx", file_pdf="...foo.pdf"
    )
    assert row_id == 7


@patch("baserow._request")
def test_post_deliverable_dedupe(mock_req):
    """Same (client_id, skill, file_md) → update existing, not insert."""
    mock_req.side_effect = [
        {"results": [{"id": 2, "name": "deliverables"}]},
        {"results": [{"id": 88, "file_md": "...foo.md"}]},  # match
        {"id": 88},                                          # PATCH
    ]
    row_id = baserow.post_deliverable(
        client_id=42, skill="company-analyst",
        file_md="...foo.md", file_docx="...foo.docx", file_pdf="...foo.pdf"
    )
    assert row_id == 88


@patch("baserow._request")
def test_network_error_does_not_crash(mock_req):
    """If Baserow is unreachable, helper logs + returns None (does not raise)."""
    mock_req.side_effect = ConnectionError("Baserow down")
    result = baserow.post_deliverable(
        client_id=42, skill="company-analyst",
        file_md="x", file_docx="x", file_pdf="x"
    )
    assert result is None
EOF
```

- [ ] **Step 2: Run tests, expect import error**

```bash
cd /srv/Nexostrat
python3 -m pytest skills/shared/tests/test_baserow.py -v
```

Expected: `ModuleNotFoundError: No module named 'baserow'`

- [ ] **Step 3: Write `skills/shared/baserow.py`**

```bash
cat > /srv/Nexostrat/skills/shared/baserow.py <<'EOF'
"""Thin Baserow REST helper for Nexostrat skill renderers + new-client.sh.

Public surface:
    post_client(slug, name, display_name, country, sector, pilot, source, **kwargs) -> int|None
    post_meeting(client_id, date, kind, **kwargs) -> int|None
    post_deliverable(client_id, skill, file_md, file_docx, file_pdf, **kwargs) -> int|None
    update_status(table, row_id, status) -> bool

All functions are idempotent (lookup-then-create) and fail-safe (return None on
network/HTTP error, log to stderr; never raise).

Reads BASEROW_URL + BASEROW_API_TOKEN from environment.
"""
from __future__ import annotations
import json, os, ssl, sys, urllib.request, urllib.error
from typing import Any

BASE_URL = os.environ.get("BASEROW_URL", "")
TOKEN = os.environ.get("BASEROW_API_TOKEN", "")
_DB_NAME = "nexostrat"
_WS_NAME = "Nexostrat"

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE  # Tailscale-only network is the security boundary

# In-process cache to avoid repeating workspace/database/table lookups
_TABLE_ID_CACHE: dict[str, int] = {}


def _log(msg: str) -> None:
    print(f"[baserow] {msg}", file=sys.stderr)


def _request(method: str, path: str, body: dict | None = None) -> dict:
    """Raw HTTP. Raises on network or HTTP errors."""
    if not BASE_URL or not TOKEN:
        raise RuntimeError("BASEROW_URL / BASEROW_API_TOKEN not set in environment")
    url = f"{BASE_URL}{path}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=_CTX, timeout=15) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode('utf-8', 'replace')}") from e


def _table_id(name: str) -> int:
    if name in _TABLE_ID_CACHE:
        return _TABLE_ID_CACHE[name]
    # Walk workspaces → databases → tables
    workspaces = _request("GET", "/api/database/workspaces/")
    ws = next(w for w in workspaces if w["name"] == _WS_NAME)
    apps = _request("GET", f"/api/applications/workspace/{ws['id']}/")
    db = next(a for a in apps if a["name"] == _DB_NAME and a["type"] == "database")
    tables = _request("GET", f"/api/database/tables/database/{db['id']}/")
    t = next(t for t in tables if t["name"] == name)
    _TABLE_ID_CACHE[name] = t["id"]
    return t["id"]


def _find_one(table: str, field: str, value: Any) -> dict | None:
    """Return first row in `table` where row[field] == value, or None."""
    tid = _table_id(table)
    # user_field_names=true returns fields by name instead of id
    resp = _request(
        "GET",
        f"/api/database/rows/table/{tid}/?user_field_names=true&filter__field_{field}__equal={value}&size=1"
    )
    results = resp.get("results", [])
    return results[0] if results else None


def _insert(table: str, fields: dict) -> dict:
    tid = _table_id(table)
    return _request("POST", f"/api/database/rows/table/{tid}/?user_field_names=true", fields)


def _update(table: str, row_id: int, fields: dict) -> dict:
    tid = _table_id(table)
    return _request("PATCH", f"/api/database/rows/table/{tid}/{row_id}/?user_field_names=true", fields)


def _safe(fn):
    """Decorator: catch all exceptions, log, return None."""
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            _log(f"{fn.__name__} failed: {type(e).__name__}: {e}")
            return None
    return wrapper


@_safe
def post_client(slug: str, name: str, display_name: str, country: str,
                sector: str, pilot: bool, source: str, **kwargs) -> int | None:
    """Idempotent. If slug exists, return existing id; else create row."""
    existing = _find_one("clients", "slug", slug)
    if existing:
        _log(f"client exists: slug={slug} id={existing['id']}")
        return existing["id"]
    fields = {"slug": slug, "name": name, "display_name": display_name,
              "country": country, "sector": sector, "pilot": pilot,
              "source": source, "phase": kwargs.get("phase", "prospect")}
    for k in ("rfc_nit", "decisor_name", "decisor_role",
              "contact_name", "contact_phone", "contact_email"):
        if k in kwargs:
            fields[k] = kwargs[k]
    row = _insert("clients", fields)
    _log(f"client created: slug={slug} id={row['id']}")
    return row["id"]


@_safe
def post_meeting(client_id: int, date: str, kind: str, **kwargs) -> int | None:
    """No dedupe — meetings may legitimately repeat. Caller responsible."""
    fields = {"client": [client_id], "date": date, "kind": kind,
              "status": kwargs.get("status", "planned")}
    for k in ("location", "attendees_text", "recording_path",
              "transcript_path", "notes_path", "duration_min"):
        if k in kwargs:
            fields[k] = kwargs[k]
    row = _insert("meetings", fields)
    _log(f"meeting created: client_id={client_id} id={row['id']}")
    return row["id"]


@_safe
def post_deliverable(client_id: int, skill: str, file_md: str,
                     file_docx: str, file_pdf: str = "", **kwargs) -> int | None:
    """Dedupe by file_md path. If exists, UPDATE; else INSERT."""
    existing = _find_one("deliverables", "file_md", file_md)
    fields = {"client": [client_id], "skill": skill, "file_md": file_md,
              "file_docx": file_docx, "file_pdf": file_pdf,
              "status": kwargs.get("status", "draft")}
    for k in ("delivered_at", "delivered_via"):
        if k in kwargs:
            fields[k] = kwargs[k]
    if existing:
        row = _update("deliverables", existing["id"], fields)
        _log(f"deliverable updated: id={row['id']} skill={skill}")
    else:
        row = _insert("deliverables", fields)
        _log(f"deliverable created: id={row['id']} skill={skill}")
    return row["id"]


@_safe
def update_status(table: str, row_id: int, status: str) -> bool:
    _update(table, row_id, {"status": status})
    return True
EOF
```

- [ ] **Step 4: Run unit tests, expect PASS**

```bash
cd /srv/Nexostrat
python3 -m pytest skills/shared/tests/test_baserow.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Integration test with real Baserow**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_baserow_helper_integration.py <<'EOF'
"""Integration tests for skills/shared/baserow.py against real Baserow."""
import sys, pathlib, os, time
sys.path.insert(0, str(pathlib.Path("/srv/Nexostrat/skills/shared")))
import baserow


def test_post_client_round_trip():
    slug = f"_test_integration_{int(time.time())}"
    cid = baserow.post_client(
        slug=slug, name="Test SA", display_name="Test",
        country="MX", sector="testing", pilot=False, source="inbound"
    )
    assert cid is not None, "first call should create"

    cid2 = baserow.post_client(
        slug=slug, name="Test SA", display_name="Test",
        country="MX", sector="testing", pilot=False, source="inbound"
    )
    assert cid2 == cid, "second call should return same id (idempotent)"


def test_post_deliverable_round_trip():
    # Need a client first
    slug = f"_test_deliv_{int(time.time())}"
    cid = baserow.post_client(slug=slug, name="x", display_name="x",
                              country="MX", sector="x", pilot=False, source="inbound")
    assert cid is not None

    path_md = f"/tmp/_test_{int(time.time())}.md"
    did = baserow.post_deliverable(client_id=cid, skill="company-analyst",
                                    file_md=path_md, file_docx=path_md + ".docx",
                                    file_pdf="")
    assert did is not None

    # Re-post same → UPDATE, same row id
    did2 = baserow.post_deliverable(client_id=cid, skill="company-analyst",
                                     file_md=path_md, file_docx=path_md + ".docx",
                                     file_pdf="")
    assert did2 == did
EOF
```

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_baserow_helper_integration.py -v
```

Expected: 2 passed. (Test rows remain in Baserow — clean them via UI or accept residue for Stage 1.)

- [ ] **Step 6: Commit**

```bash
cd /srv/Nexostrat
git add skills/shared/baserow.py \
        skills/shared/tests/__init__.py \
        skills/shared/tests/test_baserow.py \
        tests/foss_stack/test_baserow_helper_integration.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 7 · skills/shared/baserow.py helper

~150 LOC fail-safe Baserow REST helper:
- post_client (idempotent by slug)
- post_meeting (no dedupe — caller's responsibility)
- post_deliverable (dedupe by file_md path; UPDATE existing or INSERT)
- update_status (generic field setter)
- All public fns decorated with _safe — catch + log + return None, never raise

In-process table-id cache avoids repeat workspace/database lookups.

Unit tests mock _request; integration tests round-trip through real Baserow.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Extend `new-client.sh` with Baserow POST

**Files:**
- Modify: `infra/scripts/new-client.sh`
- Test: `tests/foss_stack/test_new_client_baserow.py`

- [ ] **Step 1: Inspect current new-client.sh**

```bash
wc -l /srv/Nexostrat/infra/scripts/new-client.sh
grep -n "exit\|return" /srv/Nexostrat/infra/scripts/new-client.sh | tail -5
```

Note the line numbers of the script's final state-write block (where it writes `state.json`) — the Baserow POST insertion goes immediately after.

- [ ] **Step 2: Write failing integration test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_new_client_baserow.py <<'EOF'
"""new-client.sh creates folder + Baserow row. Re-run is idempotent."""
import subprocess, os, sys, time, shutil, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"


def test_new_client_creates_folder_and_baserow_row():
    slug = f"_test_nc_{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")

    try:
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Test Cliente SA", "testing"],
            capture_output=True, text=True, cwd=NEXOSTRAT
        )
        assert r.returncode == 0, f"new-client failed: {r.stderr}"
        assert folder.exists(), "folder not created"
        assert (folder / "state.json").exists(), "state.json not created"

        # Baserow row should exist
        row = baserow._find_one("clients", "slug", slug)
        assert row is not None, "Baserow client row not created"
        assert row["name"] == "Test Cliente SA"

        # Idempotency — re-run should be a clean no-op
        r2 = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Test Cliente SA", "testing"],
            capture_output=True, text=True, cwd=NEXOSTRAT
        )
        # Script may exit non-zero on existing folder; that's the existing
        # behavior — what we need is that we do not duplicate the Baserow row.
        rows = baserow._request(
            "GET",
            f"/api/database/rows/table/{baserow._table_id('clients')}/?user_field_names=true&filter__field_slug__equal={slug}"
        )["results"]
        assert len(rows) == 1, f"expected 1 row, got {len(rows)}"
    finally:
        if folder.exists():
            shutil.rmtree(folder)
EOF
```

- [ ] **Step 3: Run test, expect failure**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_new_client_baserow.py -v
```

Expected: assertion error on `baserow client row not created`.

- [ ] **Step 4: Patch `new-client.sh`**

Read the script's final block (replace `<final-state-write-line>` with the actual line just before final `echo` / exit):

```bash
grep -n "echo.*new-client" /srv/Nexostrat/infra/scripts/new-client.sh | tail -3
```

Append a Baserow POST step before the final success message. The patch is appended to the existing logic — do NOT modify earlier sections:

```bash
cat >> /srv/Nexostrat/infra/scripts/new-client.sh <<'EOF'

# ─────────────────────────────────────────────────────────────────────
# Plan 02a Task 8 — Baserow row sync. Reads BASEROW_URL + token from
# secrets.env.age via run-with-secrets.sh. Failure here is non-fatal:
# log warning + continue (filesystem is source of truth; reconcile
# script picks up orphans nightly).
# ─────────────────────────────────────────────────────────────────────

if [ -f "$NEXOSTRAT/secrets.env.age" ]; then
    "$NEXOSTRAT/infra/scripts/run-with-secrets.sh" \
        python3 -c "
import sys, pathlib, os
sys.path.insert(0, '$NEXOSTRAT/skills/shared')
import baserow
cid = baserow.post_client(
    slug='$SLUG',
    name='''$NAME''',
    display_name='''$NAME''',
    country='$COUNTRY',
    sector='''$SECTOR''',
    pilot=$([ "${PILOT:-false}" = "true" ] && echo "True" || echo "False"),
    source='manual',
)
if cid is None:
    print('WARNING: Baserow row not created (network/auth issue?); folder is source of truth', file=sys.stderr)
    sys.exit(0)  # do not fail the script
print(f'Baserow client row: id={cid}')
" || echo "WARNING: Baserow sync skipped (run-with-secrets failed)"
else
    echo "WARNING: secrets.env.age missing — Baserow row not created"
fi
EOF
```

> **Important:** the heredoc uses `'EOF'` (quoted) so shell variable refs like `$SLUG`, `$NAME` are NOT expanded at write-time. They'll be evaluated when `new-client.sh` runs. Confirm `$SLUG`, `$NAME`, `$COUNTRY`, `$SECTOR`, `$PILOT` are the variable names used earlier in the script — adapt the heredoc body if your `new-client.sh` uses different identifiers.

- [ ] **Step 5: Verify the patch syntactically**

```bash
bash -n /srv/Nexostrat/infra/scripts/new-client.sh
echo "exit=$?"
```

Expected: `exit=0`.

- [ ] **Step 6: Re-run integration test, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_new_client_baserow.py -v
```

Expected: 1 passed.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/scripts/new-client.sh tests/foss_stack/test_new_client_baserow.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 8 · new-client.sh creates Baserow client row

Append-only patch: after folder scaffold + state.json write, call
skills/shared/baserow.py:post_client via run-with-secrets.sh.

Failure is non-fatal — filesystem is source of truth; reconcile script
(Task 12) picks up orphans nightly. Variable substitution happens at runtime
($SLUG, $NAME, etc.); shell vars are NOT expanded in the heredoc write.

Integration test asserts folder + state.json + Baserow row all present after
one invocation; second invocation does not duplicate the Baserow row.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Extend all 5 skill renderers with `post_deliverable()`

**Files (5 modifications + 1 test):**
- Modify: `skills/01_company_analyst/scripts/generate_docx.py`
- Modify: `skills/02_industry_analyst/scripts/generate_docx.py`
- Modify: `skills/03_competitor_analyst/scripts/generate_docx.py`
- Modify: `skills/04_discovery_meeting/scripts/generate_docx.py`
- Modify: `skills/05_opportunity_report/scripts/generate_docx.py`
- Test: `tests/foss_stack/test_skill_renderer_post.py`

- [ ] **Step 1: Write failing integration test for skill 01**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_skill_renderer_post.py <<'EOF'
"""When a skill renderer produces a docx, it also posts a deliverables row."""
import subprocess, os, sys, time, shutil, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"


def _setup_client(slug):
    """Create a Baserow client + folder via new-client.sh."""
    subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
         slug, "MX", "Renderer Test SA", "testing"],
        cwd=NEXOSTRAT, capture_output=True, text=True, check=True
    )
    cid = baserow._find_one("clients", "slug", slug)["id"]
    return cid


def _cleanup(slug, folder):
    if folder.exists():
        shutil.rmtree(folder)


def test_skill_01_renderer_creates_deliverable_row():
    slug = f"_test_rend_{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        cid = _setup_client(slug)
        # Write a minimal markdown file then invoke the renderer
        run_dir = folder / "01_company_analysis/runs/2026-05-19_mode-a"
        run_dir.mkdir(parents=True, exist_ok=True)
        md = run_dir / f"{slug}_AnalisisCompania_20260519.md"
        md.write_text("# Test Analysis\n\nMinimal body for renderer integration test.\n")
        # Invoke renderer with the md path as input
        r = subprocess.run(
            ["/srv/Nexostrat/infra/scripts/run-with-secrets.sh",
             "python3", f"{NEXOSTRAT}/skills/01_company_analyst/scripts/generate_docx.py",
             str(md)],
            capture_output=True, text=True
        )
        assert r.returncode == 0, f"renderer failed: {r.stderr}"
        # Deliverable row should exist
        deliv = baserow._find_one("deliverables", "file_md", str(md))
        assert deliv is not None, "deliverables row not created"
        assert deliv["skill"]["value"] == "company-analyst"
    finally:
        _cleanup(slug, folder)
EOF
```

- [ ] **Step 2: Run test, expect failure**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_skill_renderer_post.py -v
```

Expected: assertion error on `deliverables row not created`.

- [ ] **Step 3: Locate the post-render block in skill 01**

```bash
grep -n "return\|sys.exit\|print.*Wrote" /srv/Nexostrat/skills/01_company_analyst/scripts/generate_docx.py | tail -10
```

Identify the line where the script's last action is writing the .docx — the Baserow POST inserts directly after that, before the final return / exit / print.

- [ ] **Step 4: Patch all 5 renderers — common helper insertion**

For each of the 5 renderer scripts, append the following block immediately before any final `return`/`sys.exit` (or at the end of the `main()` function). Adapt path variable names per renderer (the snippet below uses common Nexostrat convention `md_path`, `docx_path`, `pdf_path` — substitute the names actually used in each file).

**Patch template** (apply per renderer with skill-name + path variables adapted):

```python
# Plan 02a Task 9 — Baserow deliverables sync.
# Fail-safe: never block rendering.
try:
    import sys as _sys, pathlib as _pl
    _sys.path.insert(0, str(_pl.Path("/srv/Nexostrat/skills/shared")))
    import baserow as _b
    # Derive client_id from slug (parent folder of the run dir)
    _slug = _pl.Path(md_path).parts[-5]  # pipeline/clients/<slug>/.../runs/<date>/<file>
    _client = _b._find_one("clients", "slug", _slug) if _b.BASE_URL else None
    if _client:
        _b.post_deliverable(
            client_id=_client["id"],
            skill="company-analyst",       # <— PER-SKILL: change this string
            file_md=str(md_path),
            file_docx=str(docx_path),
            file_pdf=str(pdf_path) if pdf_path else "",
        )
except Exception as _e:
    print(f"[baserow-sync] skipped: {_e}", file=_sys.stderr)
```

Skill name per file:
| File | `skill=` value |
|---|---|
| `skills/01_company_analyst/scripts/generate_docx.py` | `"company-analyst"` |
| `skills/02_industry_analyst/scripts/generate_docx.py` | `"industry-analyst"` |
| `skills/03_competitor_analyst/scripts/generate_docx.py` | `"competitor-analyst"` |
| `skills/04_discovery_meeting/scripts/generate_docx.py` | `"discovery-meeting"` |
| `skills/05_opportunity_report/scripts/generate_docx.py` | `"opportunity-report"` |

Apply patch to each script — one at a time, commit after each so any regression is bisectable.

**Worked example: skill 01**

```bash
# After identifying the insertion line (e.g., line 142), use a Python helper to insert:
python3 <<'PYINSERT'
import pathlib
path = pathlib.Path("/srv/Nexostrat/skills/01_company_analyst/scripts/generate_docx.py")
text = path.read_text()
# Find the marker — the line that prints "Wrote {docx_path}" or the last return in main()
marker = 'print(f"Wrote'  # adapt to actual content
i = text.rfind(marker)
assert i > 0, "marker not found — inspect manually"
# Insert the block after the marker line's newline
nl = text.find("\n", i) + 1
patch = '''
# Plan 02a Task 9 — Baserow deliverables sync (fail-safe).
try:
    import sys as _sys, pathlib as _pl
    _sys.path.insert(0, str(_pl.Path("/srv/Nexostrat/skills/shared")))
    import baserow as _b
    _slug = _pl.Path(md_path).parts[-5]
    _client = _b._find_one("clients", "slug", _slug) if _b.BASE_URL else None
    if _client:
        _b.post_deliverable(
            client_id=_client["id"],
            skill="company-analyst",
            file_md=str(md_path),
            file_docx=str(docx_path),
            file_pdf=str(pdf_path) if pdf_path else "",
        )
except Exception as _e:
    import sys
    print(f"[baserow-sync] skipped: {_e}", file=sys.stderr)
'''
path.write_text(text[:nl] + patch + text[nl:])
print(f"Patched {path}")
PYINSERT
```

- [ ] **Step 5: Run integration test on skill 01, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_skill_renderer_post.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Commit skill 01**

```bash
cd /srv/Nexostrat
git add skills/01_company_analyst/scripts/generate_docx.py \
        tests/foss_stack/test_skill_renderer_post.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 9.1 · Skill 01 company-analyst — post_deliverable on render

Fail-safe Baserow sync after docx write. Slug derived from md_path parts[-5]
(canonical layout: pipeline/clients/<slug>/<station>/runs/<date>/<file>).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7: Repeat the patch for skills 02-05, one commit each**

For each of the remaining 4 renderers, repeat Step 4's worked-example pattern with the appropriate `skill=` string and verify the renderer still completes successfully. After each, commit:

```bash
git add skills/02_industry_analyst/scripts/generate_docx.py
git commit -m "Plan 02a Task 9.2 · Skill 02 industry-analyst — post_deliverable on render"

git add skills/03_competitor_analyst/scripts/generate_docx.py
git commit -m "Plan 02a Task 9.3 · Skill 03 competitor-analyst — post_deliverable on render"

git add skills/04_discovery_meeting/scripts/generate_docx.py
git commit -m "Plan 02a Task 9.4 · Skill 04 discovery-meeting — post_deliverable on render"

git add skills/05_opportunity_report/scripts/generate_docx.py
git commit -m "Plan 02a Task 9.5 · Skill 05 opportunity-report — post_deliverable on render"
```

- [ ] **Step 8: Run the 5-skill harness to verify nothing broke**

```bash
cd /srv/Nexostrat
bash skills/tests/run_harness.sh 2>&1 | tail -20
```

Expected: `32 PASS · 0 SKIP · 0 FAIL` (the existing harness baseline established in session 4) — or whatever the current PASS count is. The harness must not regress.

If a renderer's syntax broke, revert that specific commit + re-patch surgically.

---

## Task 10: `baserow-reconcile.sh` + nightly timer

**Files:**
- Create: `infra/scripts/baserow-reconcile.sh`
- Create: `infra/systemd/nexostrat-baserow-reconcile.service`
- Create: `infra/systemd/nexostrat-baserow-reconcile.timer`
- Test: `tests/foss_stack/test_reconcile_orphan.py`

- [ ] **Step 1: Write failing test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_reconcile_orphan.py <<'EOF'
"""Orphan deliverable file → reconcile creates Baserow row."""
import subprocess, sys, time, shutil, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"


def test_reconcile_creates_orphan_row():
    slug = f"_test_reconcile_{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        # Create client via new-client.sh
        subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Reconcile Test", "testing"],
            cwd=NEXOSTRAT, capture_output=True, text=True, check=True
        )
        cid = baserow._find_one("clients", "slug", slug)["id"]

        # Synthesize an orphan deliverable — write file without renderer call
        run_dir = folder / "01_company_analysis/runs/2026-05-19_mode-a"
        run_dir.mkdir(parents=True, exist_ok=True)
        md = run_dir / f"{slug}_AnalisisCompania_20260519.md"
        docx = run_dir / f"{slug}_AnalisisCompania_20260519.docx"
        md.write_text("orphan body")
        docx.write_text("dummy docx bytes")

        # Confirm no row exists yet
        assert baserow._find_one("deliverables", "file_md", str(md)) is None

        # Run reconcile
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/baserow-reconcile.sh"],
            capture_output=True, text=True
        )
        assert r.returncode == 0, f"reconcile failed: {r.stderr}"

        # Row should now exist
        row = baserow._find_one("deliverables", "file_md", str(md))
        assert row is not None, "orphan not picked up"
        assert row["skill"]["value"] == "company-analyst"
    finally:
        if folder.exists():
            shutil.rmtree(folder)
EOF
```

- [ ] **Step 2: Run test, expect failure (script missing)**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_reconcile_orphan.py -v
```

Expected: `FileNotFoundError`.

- [ ] **Step 3: Write `baserow-reconcile.sh`**

```bash
cat > /srv/Nexostrat/infra/scripts/baserow-reconcile.sh <<'EOF'
#!/usr/bin/env bash
# Scan pipeline/clients/<slug>/<station>/runs/<date>_*/ for skill output files.
# Cross-reference against Baserow deliverables table. Create rows for orphans.
# Idempotent: re-run is no-op if everything is already in sync.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}

"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" \
  python3 -c "
import sys, pathlib, re
sys.path.insert(0, '$NEXOSTRAT/skills/shared')
import baserow

STATION_TO_SKILL = {
    '01_company_analysis': 'company-analyst',
    '02_industry_analysis': 'industry-analyst',
    '03_competitor_analysis': 'competitor-analyst',
    '04_prep_llamada': 'discovery-meeting',
    '05_opportunity_report': 'opportunity-report',
}

clients_dir = pathlib.Path('$NEXOSTRAT/pipeline/clients')
if not clients_dir.exists():
    print('No clients/ folder; nothing to reconcile')
    sys.exit(0)

orphans = 0
synced = 0
for client_dir in clients_dir.iterdir():
    if not client_dir.is_dir() or client_dir.name.startswith('_'):
        continue
    slug = client_dir.name
    client = baserow._find_one('clients', 'slug', slug)
    if not client:
        print(f'WARNING: client folder {slug} has no Baserow row; skipping deliverables for it')
        continue
    cid = client['id']
    for station, skill_name in STATION_TO_SKILL.items():
        runs = client_dir / station / 'runs'
        if not runs.exists():
            continue
        for run_dir in runs.iterdir():
            if not run_dir.is_dir():
                continue
            mds = sorted(run_dir.glob('*.md'))
            if not mds:
                continue
            md = mds[0]
            docx = md.with_suffix('.docx')
            pdf = md.with_suffix('.pdf')
            row = baserow._find_one('deliverables', 'file_md', str(md))
            if row:
                synced += 1
                continue
            baserow.post_deliverable(
                client_id=cid, skill=skill_name,
                file_md=str(md),
                file_docx=str(docx) if docx.exists() else '',
                file_pdf=str(pdf) if pdf.exists() else '',
            )
            orphans += 1

print(f'Reconcile complete: {orphans} orphan(s) added, {synced} already in sync')
"
EOF
chmod +x /srv/Nexostrat/infra/scripts/baserow-reconcile.sh
```

- [ ] **Step 4: Run reconcile manually, expect no-op (no orphans exist yet)**

```bash
/srv/Nexostrat/infra/scripts/baserow-reconcile.sh
```

Expected output: `Reconcile complete: 0 orphan(s) added, N already in sync` (where N counts the existing deliverable rows).

- [ ] **Step 5: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_reconcile_orphan.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Write systemd unit + timer**

```bash
cat > /srv/Nexostrat/infra/systemd/nexostrat-baserow-reconcile.service <<'EOF'
[Unit]
Description=Nexostrat — nightly Baserow deliverables reconcile
After=nexostrat-foss-stack.service

[Service]
Type=oneshot
User=ricardo
WorkingDirectory=/srv/Nexostrat
ExecStart=/srv/Nexostrat/infra/scripts/baserow-reconcile.sh
StandardOutput=journal
StandardError=journal
EOF

cat > /srv/Nexostrat/infra/systemd/nexostrat-baserow-reconcile.timer <<'EOF'
[Unit]
Description=Nexostrat — nightly Baserow deliverables reconcile (03:30)

[Timer]
OnCalendar=*-*-* 03:30:00
Persistent=true
Unit=nexostrat-baserow-reconcile.service

[Install]
WantedBy=timers.target
EOF
```

Install (manual sudo):

```bash
sudo ln -sf /srv/Nexostrat/infra/systemd/nexostrat-baserow-reconcile.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nexostrat-baserow-reconcile.timer
systemctl list-timers nexostrat-baserow-reconcile.timer
```

Expected: `list-timers` shows the unit with next-run timestamp at 03:30.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/scripts/baserow-reconcile.sh \
        infra/systemd/nexostrat-baserow-reconcile.{service,timer} \
        tests/foss_stack/test_reconcile_orphan.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 10 · baserow-reconcile.sh + nightly timer

Scans pipeline/clients/<slug>/<station>/runs/<date>/*.md and ensures each
file has a corresponding deliverables row in Baserow. Creates orphan rows;
already-synced rows are no-op.

STATION_TO_SKILL map binds folder names to skill identifiers (resolves the
discovery-meeting / 04_prep_llamada / discovery-meeting naming triplet from
ADR-027 + session 3 rename history).

systemd timer runs nightly at 03:30 local, AFTER any same-day backups (02:30).
Output goes to journal; Plan 04 Telegram alerts on service failure.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: BookStack shelves + books setup

**Files:**
- Create: `infra/bookstack/migrations/__init__.py`
- Create: `infra/bookstack/migrations/_api.py`
- Create: `infra/bookstack/migrations/01_shelves_books.py`
- Test: `tests/foss_stack/test_bookstack_shelves.py`

- [ ] **Step 1: Write failing test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_bookstack_shelves.py <<'EOF'
"""BookStack should have the 4 shelves + their books from spec §5.4."""
import os, json, urllib.request, ssl, pytest

URL = os.environ["BOOKSTACK_URL"]
TOK = os.environ["BOOKSTACK_API_TOKEN"]
SEC = os.environ["BOOKSTACK_API_SECRET"]

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _get(path):
    req = urllib.request.Request(f"{URL}/api{path}")
    req.add_header("Authorization", f"Token {TOK}:{SEC}")
    with urllib.request.urlopen(req, context=_CTX, timeout=15) as r:
        return json.loads(r.read())


EXPECTED_SHELVES = {"Playbooks", "Industries", "Drafts", "References"}
EXPECTED_BOOKS = {
    "Sales", "Operations",
    "Logística-cross-border-MX",
    "ADRs-draft", "Pricing", "Service-design",
    "Glossary", "Tooling", "Templates",
}


def test_all_shelves_exist():
    shelves = {s["name"] for s in _get("/shelves")["data"]}
    assert EXPECTED_SHELVES.issubset(shelves), f"missing: {EXPECTED_SHELVES - shelves}"


def test_all_books_exist():
    books = {b["name"] for b in _get("/books")["data"]}
    assert EXPECTED_BOOKS.issubset(books), f"missing: {EXPECTED_BOOKS - books}"
EOF
```

- [ ] **Step 2: Run test, expect failure**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_bookstack_shelves.py -v
```

Expected: both fail — shelves + books are empty initially.

- [ ] **Step 3: Write BookStack API client**

```bash
mkdir -p /srv/Nexostrat/infra/bookstack/migrations
cat > /srv/Nexostrat/infra/bookstack/migrations/__init__.py <<'EOF'
EOF
cat > /srv/Nexostrat/infra/bookstack/migrations/_api.py <<'EOF'
"""Thin BookStack API client for migrations. Token + Secret from env."""
import os, json, ssl, urllib.request, urllib.error

URL = os.environ["BOOKSTACK_URL"]
TOK = os.environ["BOOKSTACK_API_TOKEN"]
SEC = os.environ["BOOKSTACK_API_SECRET"]

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _req(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"{URL}/api{path}", data=data, method=method)
    req.add_header("Authorization", f"Token {TOK}:{SEC}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=_CTX, timeout=15) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode('utf-8', 'replace')}")


def get(path): return _req("GET", path)
def post(path, body): return _req("POST", path, body)
def put(path, body): return _req("PUT", path, body)


def get_or_create_book(name: str, description: str = "") -> int:
    books = get("/books")["data"]
    for b in books:
        if b["name"] == name:
            print(f"  BOOK EXISTS: {name} (id={b['id']})")
            return b["id"]
    r = post("/books", {"name": name, "description": description})
    print(f"  BOOK CREATED: {name} (id={r['id']})")
    return r["id"]


def get_or_create_shelf(name: str, description: str, book_ids: list[int]) -> int:
    shelves = get("/shelves")["data"]
    for s in shelves:
        if s["name"] == name:
            # Ensure all book_ids are attached (idempotent membership)
            put(f"/shelves/{s['id']}", {"name": name, "description": description, "books": book_ids})
            print(f"SHELF EXISTS: {name} (id={s['id']})")
            return s["id"]
    r = post("/shelves", {"name": name, "description": description, "books": book_ids})
    print(f"SHELF CREATED: {name} (id={r['id']})")
    return r["id"]
EOF
```

- [ ] **Step 4: Write `01_shelves_books.py`**

```bash
cat > /srv/Nexostrat/infra/bookstack/migrations/01_shelves_books.py <<'EOF'
"""Create 4 shelves + 9 books per spec §5.4. Idempotent."""
from _api import get_or_create_shelf, get_or_create_book


SHELVES = {
    "Playbooks": {
        "description": "Operational playbooks — how we run sales + ops",
        "books": [
            ("Sales", "Cold outbound, follow-up, objections, pricing-talk"),
            ("Operations", "Pre-meeting + post-meeting + render workflow + brand"),
        ],
    },
    "Industries": {
        "description": "Sector knowledge accumulator — grows session by session",
        "books": [
            ("Logística-cross-border-MX", "Seeded from Trixx; future cross-border MX clients add here"),
        ],
    },
    "Drafts": {
        "description": "Sandbox before promotion to git",
        "books": [
            ("ADRs-draft", "Exploration before formalizing ADRs to 00_GOVERNANCE/adr/"),
            ("Pricing", "Pricing experiments — Hoja de Ruta, retainer, etc."),
            ("Service-design", "Service-model thinking, packaging, positioning"),
        ],
    },
    "References": {
        "description": "Internal references — glossary, tooling, templates",
        "books": [
            ("Glossary", "Terms: TIGIE, Pedimento, OEA, NIT, RFC, Diagnóstico, Hoja de Ruta"),
            ("Tooling", "Whisper notes, Ollama prompt experiments, render tips"),
            ("Templates", "Checklists, plantillas reutilizables"),
        ],
    },
}


def run():
    for shelf_name, cfg in SHELVES.items():
        book_ids = []
        for bname, bdesc in cfg["books"]:
            book_ids.append(get_or_create_book(bname, bdesc))
        get_or_create_shelf(shelf_name, cfg["description"], book_ids)


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 5: Run migration**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/bookstack/migrations/01_shelves_books.py
```

Expected: 4 shelves + 9 books created (or `EXISTS` if rerunning).

- [ ] **Step 6: Re-run, expect no-op**

Expected: every line says `EXISTS`.

- [ ] **Step 7: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_bookstack_shelves.py -v
```

Expected: 2 passed.

- [ ] **Step 8: Commit**

```bash
cd /srv/Nexostrat
git add infra/bookstack/migrations/ tests/foss_stack/test_bookstack_shelves.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 11 · BookStack — 4 shelves + 9 books

_api.py wraps BookStack REST (Token+Secret auth).

01_shelves_books.py creates: Playbooks (Sales, Operations), Industries
(Logística-cross-border-MX), Drafts (ADRs-draft, Pricing, Service-design),
References (Glossary, Tooling, Templates).

Idempotent: re-run is no-op; existing shelves have books reattached via PUT
so membership stays correct.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: BookStack seeded pages

**Files:**
- Create: `infra/bookstack/seed/playbooks_operations_pre_meeting_checklist.md`
- Create: `infra/bookstack/seed/playbooks_operations_post_meeting_protocol.md`
- Create: `infra/bookstack/seed/industries_logistica_cross_border_terminos_reforma.md`
- Create: `infra/bookstack/seed/industries_logistica_cross_border_mapa_competitivo.md`
- Create: `infra/bookstack/seed/drafts_pricing_hoja_ruta.md`
- Create: `infra/bookstack/seed/references_glossary_terminos_nexostrat.md`
- Create: `infra/bookstack/seed/references_templates_checklist_session_end.md`
- Create: `infra/bookstack/migrations/02_seed_pages.py`
- Test: `tests/foss_stack/test_bookstack_pages.py`

> **Language note:** these are Ricardo-facing operational pages. Per
> [`feedback_language_consistency`](memory) BookStack content is Spanish
> (eventual JP read; client-adjacent). Code blocks within may be English.

- [ ] **Step 1: Write the 7 seed page markdown files**

For brevity, the body of each seed page is left at a one-paragraph stub —
Ricardo expands them in-place after seeding. The structure is committed; the
content grows organically.

```bash
mkdir -p /srv/Nexostrat/infra/bookstack/seed

cat > /srv/Nexostrat/infra/bookstack/seed/playbooks_operations_pre_meeting_checklist.md <<'EOF'
# Pre-meeting checklist (derivado de la sesión Trixx 2026-05-19)

## Antes de la reunión (T-1 día)

- [ ] PDFs impresos en el escritorio: AnalisisCompania, Industria, Competencia, PrepLlamada.
- [ ] Libreta + pluma + tarjeta de presentación en la maleta.
- [ ] Cargador de teléfono (grabación de audio puede ser larga).
- [ ] Confirmación del lugar + hora 24h antes vía WhatsApp con el contacto.
- [ ] Re-leer `our_hypotheses.md` del cliente — especialmente las zonas sensibles.

## Llegando

- [ ] Saludo cercano (tono mixto cercano + estratégico — calibrado por sector).
- [ ] Apertura relacional 5 min antes de cualquier sondeo operativo.
- [ ] Pedir permiso explícito para grabar audio: "Para no perderme detalles importantes, ¿les molesta si grabo solo el audio?"

## Durante

- [ ] PrepLlamada como guía, NO como cuestionario.
- [ ] Evitar zonas sensibles documentadas (defectos del sitio, comparativas directas con competidores específicos, "¿por qué no han modernizado antes?").
- [ ] 30 min objetivo — no extender más allá de lo necesario.

## Cierre

- [ ] Ofrecer análisis gratuito en unos días.
- [ ] NO empujar la Hoja de Ruta de IA en esta reunión.
- [ ] Agradecer + confirmar próximo paso (envío del reporte D+2).
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/playbooks_operations_post_meeting_protocol.md <<'EOF'
# Post-meeting protocol (qué hacer con la grabación y las notas)

## T+0 — Misma noche

- [ ] Subir grabación a `vault/clients/<slug>/meetings/<date>.age` (age-encrypted).
- [ ] Crear row `meetings` en Baserow con status=`recorded`, path al archivo, kind=`discovery`.
- [ ] Escribir 5-10 bullet points de impresiones inmediatas en `pipeline/clients/<slug>/05_meetings/notes/<date>.md`.

## T+1 día

- [ ] Whisper.cpp transcribe el audio (manual Stage 1 — Plan 08 automatiza).
- [ ] Update Baserow row: status=`transcribed`, transcript_path.
- [ ] Leer transcripción + comparar con notas + las 9 hipótesis del PrepLlamada.

## T+2-3 días

- [ ] Ejecutar Skill 05 (opportunity-report) con: 4 reportes previos + transcript + notas.
- [ ] Revisión obligatoria interna (Ricardo + JP per ADR-038 Fase 5).
- [ ] Entrega manual al cliente (Fase 6 — siempre personal, nunca automatizado primer envío).

## D+4 días hábiles

- [ ] Si no responde — follow-up automatizado (Plan 04 cuando aterrice) o manual.
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/industries_logistica_cross_border_terminos_reforma.md <<'EOF'
# Logística cross-border MX — Términos clave + Reforma 2026

> **Extraído de:** Skill 02 (industry-analyst) corrida 2026-05-18 sobre el sector cross-border MX-USA para el caso Trixx.
> Reutilizable hasta diciembre 2026; si la regulación cambia, revisar.

## Términos clave para conversaciones con clientes del sector

- **TIGIE** — Tarifa de los Impuestos Generales de Importación y Exportación.
- **Pedimento** — documento aduanal obligatorio para cada operación de importación/exportación.
- **Carta Porte 3.1** — complemento fiscal del CFDI para transporte de mercancías; obligatorio desde 2024 con multas creciendo.
- **OEA** — Operador Económico Autorizado; certificación SAT que da preferencia + agilidad aduanal.
- **Responsabilidad solidaria 2026** — Reforma Ley Aduanera que extiende responsabilidad fiscal a más eslabones de la cadena logística (consignatario, transportista, agente). Tema sensible y nuevo en 2026.

## Reforma Ley Aduanera 2026 — puntos clave

(Expandir con detalles específicos cuando se ejecute análisis sobre nuevos clientes del sector.)
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/industries_logistica_cross_border_mapa_competitivo.md <<'EOF'
# Logística cross-border MX — Mapa competitivo

> **Extraído de:** Skill 03 (competitor-analyst) corrida 2026-05-18 para Trixx.

## Competidores estructurales identificados

### Nuvocargo
- USD 74M en funding, AI-native, target volumen 150-350 envíos/mes.
- Segmento que solapa con Trixx.
- Portal cliente + tracking en tiempo real + cotizaciones instantáneas + integración con marketplaces.
- **Gap atacable 6-12 meses con Nexostrat:** portal cliente + automatización de cotizaciones.

### Agentes aduanales locales TJ
- Mercado fragmentado, baja madurez digital.
- Trixx ya compite aquí — no es la amenaza primaria.

### Integración Aduanal (proyección)
- Players regionales con presencia digital intermedia.

## Talking points calibrados (sin profundidad técnica)

1. "El mercado está cambiando" — sin atacar Nuvocargo directo.
2. Reforma 2026 + responsabilidad solidaria como ángulo táctico de urgencia.
3. Multas Carta Porte como dolor concreto demostrable.
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/drafts_pricing_hoja_ruta.md <<'EOF'
# Hoja de Ruta de IA — scope + pricing experiment (DRAFT)

> **Estado:** placeholder. Diseño pendiente post-piloto Trixx.
> **Triggers para llenar:** cuando Trixx (o el primer cliente que pase a paid) pida cotización formal.

## Hipótesis iniciales (a validar)

- **Scope:** plan a 4 semanas con 2 sesiones largas (1.5h c/u) + entregable final consolidando 6-10 oportunidades priorizadas + 2 Quick Wins + roadmap detallado.
- **Precio rango inicial:** USD 3-8K (calibrar al cierre del piloto Trixx).
- **Modalidad:** pago contra entregable final, no upfront.

## Decisiones pendientes

- ¿Una Hoja de Ruta cubre múltiples áreas funcionales o se vende por área (ventas, ops, finanzas)?
- ¿Incluye implementación de Quick Wins, o solo diseño?
- ¿Retainer post-Hoja de Ruta es paquete separado o continuación natural?

## Material de referencia

- Plan Maestro v1 (2026-05-07) tiene una primera versión del scope; ha sido superseded por la simplificación de JP del 2026-05-18 (6 fases, 5 skills).
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/references_glossary_terminos_nexostrat.md <<'EOF'
# Glosario — Términos Nexostrat

> Términos internos del firma. Si un término aparece en docs cliente, define aquí.

- **Diagnóstico** — Entregable gratuito final de la Fase 4 (opportunity-report). 6-10 oportunidades priorizadas + 2 Quick Wins + plan 4 semanas.
- **Hoja de Ruta de IA** — Servicio paid post-Diagnóstico. Scope + precio pendiente de diseñar.
- **Skill 01** — company-analyst (análisis de empresa CO/MX).
- **Skill 02** — industry-analyst (análisis sectorial CO/MX).
- **Skill 03** — competitor-analyst (análisis competitivo CO/MX).
- **Skill 04** — discovery-meeting (guía pre-llamada relacional).
- **Skill 05** — opportunity-report (entregable Diagnóstico).
- **Pipeline phase 0** — Pre-meeting; corre Skills 01-04 + intake en `pipeline/clients/<slug>/00_intake/`.
- **Fase 1-6** — workflow JP simplificado 2026-05-18 (contacto → preparación → primera llamada → reporte → revisión interna → entrega + seguimiento).
- **JP-Light** — modo de JP (ADR-021bis): Telegram + email + dashboard FOSS; no Gitea web, no Claude Code en jp-mac.
- **JP-Heavy** — flip futuro de JP a clone completo + Claude Code en jp-mac.
EOF

cat > /srv/Nexostrat/infra/bookstack/seed/references_templates_checklist_session_end.md <<'EOF'
# Checklist — Session-end protocol Claude Code

> Derivado de CLAUDE.md § Session End Protocol. Páginas vivas; CLAUDE.md es canonical.

## Step 1 — Claude, on close phrase

1. 2-4 sentence prose summary de qué hizo la sesión.
2. Bulleted list de cada archivo que se va a escribir al cerrar.
3. Pending-items table con prioridad propuesta + due date + rationale.
4. Disambiguation questions solo si son bloqueantes de verdad.

## Step 2 — Operator confirms

## Step 3 — Claude applies everything

1. Update `STATUS.md`.
2. Update root `tasks.json`.
3. Update root `calendar.json` si cambiaron deadlines.
4. Journal entry en `00_META/journal/YYYY-MM-DD_<topic>.md`.
5. Update root `00_META/CHANGELOG.md` si se editó algún context file.
6. Rewrite `CHECKPOINT.md`.
7. Handoff a Gemini si aplica.
8. Memos a otras personas si aplica.
9. `git add` + `git commit` + `git push origin main`.

## Step 4 — Operator escribe "Finish Session"
EOF
```

- [ ] **Step 2: Write `02_seed_pages.py`**

```bash
cat > /srv/Nexostrat/infra/bookstack/migrations/02_seed_pages.py <<'EOF'
"""Create 7 seed pages from infra/bookstack/seed/*.md. Idempotent."""
import pathlib
from _api import get, post


# Page filename -> (book_name, page_title)
PAGES = {
    "playbooks_operations_pre_meeting_checklist.md": ("Operations", "Pre-meeting checklist (Trixx-derived)"),
    "playbooks_operations_post_meeting_protocol.md": ("Operations", "Post-meeting protocol"),
    "industries_logistica_cross_border_terminos_reforma.md": ("Logística-cross-border-MX", "Términos clave + Reforma 2026"),
    "industries_logistica_cross_border_mapa_competitivo.md": ("Logística-cross-border-MX", "Mapa competitivo MX cross-border"),
    "drafts_pricing_hoja_ruta.md": ("Pricing", "Hoja de Ruta de IA — scope + pricing experiment"),
    "references_glossary_terminos_nexostrat.md": ("Glossary", "Términos Nexostrat"),
    "references_templates_checklist_session_end.md": ("Templates", "Checklist de session-end Claude Code"),
}


def _book_id(name):
    books = get("/books")["data"]
    return next(b["id"] for b in books if b["name"] == name)


def _existing_pages_in_book(book_id):
    pages = get(f"/books/{book_id}")["contents"]
    return {p["name"] for p in pages if p["type"] == "page"}


def run():
    seed_dir = pathlib.Path(__file__).parent.parent / "seed"
    for fname, (book_name, title) in PAGES.items():
        bid = _book_id(book_name)
        existing = _existing_pages_in_book(bid)
        if title in existing:
            print(f"  PAGE EXISTS: {title} (book={book_name})")
            continue
        md_content = (seed_dir / fname).read_text()
        post("/pages", {"book_id": bid, "name": title, "markdown": md_content})
        print(f"  PAGE CREATED: {title} (book={book_name})")


if __name__ == "__main__":
    run()
EOF
```

- [ ] **Step 3: Write test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_bookstack_pages.py <<'EOF'
"""7 seeded pages exist in their assigned books."""
import os, json, urllib.request, ssl

URL = os.environ["BOOKSTACK_URL"]
TOK = os.environ["BOOKSTACK_API_TOKEN"]
SEC = os.environ["BOOKSTACK_API_SECRET"]
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _get(path):
    req = urllib.request.Request(f"{URL}/api{path}")
    req.add_header("Authorization", f"Token {TOK}:{SEC}")
    with urllib.request.urlopen(req, context=_CTX, timeout=15) as r:
        return json.loads(r.read())


EXPECTED_TITLES = {
    "Pre-meeting checklist (Trixx-derived)",
    "Post-meeting protocol",
    "Términos clave + Reforma 2026",
    "Mapa competitivo MX cross-border",
    "Hoja de Ruta de IA — scope + pricing experiment",
    "Términos Nexostrat",
    "Checklist de session-end Claude Code",
}


def test_7_pages_seeded():
    pages = {p["name"] for p in _get("/pages")["data"]}
    missing = EXPECTED_TITLES - pages
    assert not missing, f"missing pages: {missing}"
EOF
```

- [ ] **Step 4: Run migration**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 /srv/Nexostrat/infra/bookstack/migrations/02_seed_pages.py
```

Expected: 7 `PAGE CREATED` lines.

- [ ] **Step 5: Re-run, expect no-op**

Expected: 7 `PAGE EXISTS` lines.

- [ ] **Step 6: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_bookstack_pages.py -v
```

Expected: 1 passed.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/bookstack/seed/ \
        infra/bookstack/migrations/02_seed_pages.py \
        tests/foss_stack/test_bookstack_pages.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 12 · BookStack — 7 seeded pages

Spanish content per feedback_language_consistency rule (Ricardo + JP-facing).
Pages extracted from existing material (Trixx session 5 checklist, Skill 02/03
outputs, CLAUDE.md session-end protocol).

Idempotent: pages identified by (book, title); skip if title already exists in
the target book.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: Backup scripts + nightly timers

**Files:**
- Create: `infra/scripts/backup-foss-stack.sh`
- Create: `infra/systemd/nexostrat-foss-backup.service`
- Create: `infra/systemd/nexostrat-foss-backup.timer`
- Test: `tests/foss_stack/test_backup_creates_valid_age.py`

- [ ] **Step 1: Write failing test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_backup_creates_valid_age.py <<'EOF'
"""Backup script produces age-encrypted files that decrypt successfully."""
import subprocess, os, pathlib, datetime

NEXOSTRAT = "/srv/Nexostrat"
VAULT = pathlib.Path(f"{NEXOSTRAT}/vault/backups")
TODAY = datetime.date.today().isoformat()


def test_backup_produces_all_4_artefacts():
    r = subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/backup-foss-stack.sh"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, f"backup failed: {r.stderr}"

    expected = [
        VAULT / "baserow" / f"{TODAY}.sql.age",
        VAULT / "bookstack" / f"{TODAY}.sql.age",
        VAULT / "baserow-uploads" / f"{TODAY}.tar.gz.age",
        VAULT / "bookstack-uploads" / f"{TODAY}.tar.gz.age",
    ]
    for p in expected:
        assert p.exists(), f"missing: {p}"
        assert p.stat().st_size > 100, f"too small (likely empty): {p}"


def test_backup_artefacts_decrypt():
    """Each .age file decrypts cleanly with the host's age key."""
    for path in [
        VAULT / "baserow" / f"{TODAY}.sql.age",
        VAULT / "bookstack" / f"{TODAY}.sql.age",
    ]:
        if not path.exists():
            continue
        r = subprocess.run(
            ["age", "-d", "-i", os.path.expanduser("~/.config/age/key.txt"), str(path)],
            capture_output=True
        )
        assert r.returncode == 0, f"decrypt failed: {path}"
        # Postgres dump starts with "--" or "-- PostgreSQL database dump"
        # MySQL dump starts with "-- MySQL dump" or "-- MariaDB dump"
        head = r.stdout[:200].decode("utf-8", "replace")
        assert "dump" in head.lower() or "PostgreSQL" in head or "MySQL" in head or "MariaDB" in head, \
            f"unexpected dump header: {head!r}"
EOF
```

- [ ] **Step 2: Run test, expect failure (script missing)**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_backup_creates_valid_age.py -v
```

Expected: `FileNotFoundError`.

- [ ] **Step 3: Write `backup-foss-stack.sh`**

```bash
cat > /srv/Nexostrat/infra/scripts/backup-foss-stack.sh <<'EOF'
#!/usr/bin/env bash
# Nightly backup of Baserow Postgres + BookStack MySQL + uploads volumes.
# Each artefact is age-encrypted to vault/backups/<service>/YYYY-MM-DD.<ext>.age
# Retention: 30 days local (purge older); warm-standby rsync handled by Plan 01b timer.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
DATE=$(date +%F)
VAULT="$NEXOSTRAT/vault/backups"
RECIPIENTS="$NEXOSTRAT/infra/age-recipients.txt"

mkdir -p "$VAULT"/{baserow,bookstack,baserow-uploads,bookstack-uploads}

# Load .env so we know container names + DB passwords
set -a
. "$NEXOSTRAT/infra/docker/foss-stack/.env"
set +a

echo "[$(date -Is)] starting FOSS stack backup"

# ─── Baserow Postgres ────────────────────────────────────────────
echo "  baserow postgres → $VAULT/baserow/$DATE.sql.age"
docker exec nexostrat-baserow bash -c \
    "PGPASSWORD=\$DATABASE_PASSWORD pg_dump -U baserow -d baserow" \
  | age -e -R "$RECIPIENTS" -o "$VAULT/baserow/$DATE.sql.age"

# ─── BookStack MySQL ─────────────────────────────────────────────
echo "  bookstack mysql → $VAULT/bookstack/$DATE.sql.age"
docker exec nexostrat-bookstack-db sh -c \
    "exec mysqldump -ubookstack -p\"$BOOKSTACK_DB_PASSWORD\" bookstack" \
  | age -e -R "$RECIPIENTS" -o "$VAULT/bookstack/$DATE.sql.age"

# ─── Baserow media (uploads) ─────────────────────────────────────
echo "  baserow uploads → $VAULT/baserow-uploads/$DATE.tar.gz.age"
docker run --rm -v nexostrat-foss_baserow_media:/src -v /tmp:/dest alpine \
    tar -czf - -C /src . \
  | age -e -R "$RECIPIENTS" -o "$VAULT/baserow-uploads/$DATE.tar.gz.age"

# ─── BookStack uploads ──────────────────────────────────────────
echo "  bookstack uploads → $VAULT/bookstack-uploads/$DATE.tar.gz.age"
docker run --rm -v nexostrat-foss_bookstack_app:/src -v /tmp:/dest alpine \
    tar -czf - -C /src . \
  | age -e -R "$RECIPIENTS" -o "$VAULT/bookstack-uploads/$DATE.tar.gz.age"

# ─── Retention: purge >30 days ──────────────────────────────────
find "$VAULT" -name "*.age" -type f -mtime +30 -delete

echo "[$(date -Is)] backup complete"
EOF
chmod +x /srv/Nexostrat/infra/scripts/backup-foss-stack.sh
```

- [ ] **Step 4: Run backup manually**

```bash
/srv/Nexostrat/infra/scripts/backup-foss-stack.sh
```

Expected: 4 lines logging each artefact written, then "backup complete." Verify files:

```bash
ls -la /srv/Nexostrat/vault/backups/*/$(date +%F)*
```

Expected: 4 .age files, each non-zero size.

- [ ] **Step 5: Write systemd unit + timer**

```bash
cat > /srv/Nexostrat/infra/systemd/nexostrat-foss-backup.service <<'EOF'
[Unit]
Description=Nexostrat — nightly FOSS stack backup (Baserow + BookStack)
After=nexostrat-foss-stack.service
Requires=nexostrat-foss-stack.service

[Service]
Type=oneshot
User=ricardo
WorkingDirectory=/srv/Nexostrat
ExecStart=/srv/Nexostrat/infra/scripts/backup-foss-stack.sh
StandardOutput=journal
StandardError=journal
EOF

cat > /srv/Nexostrat/infra/systemd/nexostrat-foss-backup.timer <<'EOF'
[Unit]
Description=Nexostrat — nightly FOSS stack backup (02:30)

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true
Unit=nexostrat-foss-backup.service

[Install]
WantedBy=timers.target
EOF
```

Install (manual sudo):

```bash
sudo ln -sf /srv/Nexostrat/infra/systemd/nexostrat-foss-backup.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nexostrat-foss-backup.timer
systemctl list-timers nexostrat-foss-backup.timer
```

Expected: timer shows next run at 02:30 local.

- [ ] **Step 6: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
python3 -m pytest tests/foss_stack/test_backup_creates_valid_age.py -v
```

Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/scripts/backup-foss-stack.sh \
        infra/systemd/nexostrat-foss-backup.{service,timer} \
        tests/foss_stack/test_backup_creates_valid_age.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 13 · backup-foss-stack.sh + nightly 02:30 timer

pg_dump (Baserow) + mysqldump (BookStack) piped through age-encrypt to
vault/backups/<service>/YYYY-MM-DD.sql.age. Same shape for upload volumes
via docker-run alpine tar -> stdout -> age.

Retention: 30 days local (find -mtime +30 -delete). Warm-standby rsync is
Plan 01b's responsibility.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: Recovery scripts

**Files:**
- Create: `infra/recovery/restore-baserow.sh`
- Create: `infra/recovery/restore-bookstack.sh`
- Create: `infra/recovery/baserow-rotate-token.sh`
- Test: `tests/foss_stack/test_backup_restore_baserow.py`
- Test: `tests/foss_stack/test_backup_restore_bookstack.py`

- [ ] **Step 1: Write failing round-trip test for Baserow**

```bash
mkdir -p /srv/Nexostrat/infra/recovery
cat > /srv/Nexostrat/tests/foss_stack/test_backup_restore_baserow.py <<'EOF'
"""Backup → mutate live → restore → verify mutation gone."""
import subprocess, sys, time, datetime, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"
TODAY = datetime.date.today().isoformat()
BACKUP_PATH = pathlib.Path(f"{NEXOSTRAT}/vault/backups/baserow/{TODAY}.sql.age")


def test_round_trip_restores_pre_backup_state():
    if not BACKUP_PATH.exists():
        # Take a backup first
        subprocess.run([f"{NEXOSTRAT}/infra/scripts/backup-foss-stack.sh"], check=True)

    # Mutate live: create a client with a unique marker slug
    marker = f"_test_restore_marker_{int(time.time())}"
    cid = baserow.post_client(slug=marker, name="x", display_name="x",
                              country="MX", sector="x", pilot=False, source="inbound")
    assert cid is not None
    assert baserow._find_one("clients", "slug", marker) is not None

    # Restore from today's backup (pre-mutation snapshot)
    r = subprocess.run(
        [f"{NEXOSTRAT}/infra/recovery/restore-baserow.sh", TODAY],
        capture_output=True, text=True, input="y\n"  # confirm prompt
    )
    assert r.returncode == 0, f"restore failed: {r.stderr}"

    # Marker should be GONE — it was created after the backup was taken
    baserow._TABLE_ID_CACHE.clear()  # force re-fetch (db is restored)
    time.sleep(2)
    found = baserow._find_one("clients", "slug", marker)
    assert found is None, "restore did not roll back the mutation"
EOF
```

- [ ] **Step 2: Run test, expect failure**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_backup_restore_baserow.py -v
```

Expected: `FileNotFoundError` on the restore script.

- [ ] **Step 3: Write `restore-baserow.sh`**

```bash
cat > /srv/Nexostrat/infra/recovery/restore-baserow.sh <<'EOF'
#!/usr/bin/env bash
# Decrypt + pg_restore Baserow Postgres from vault/backups/baserow/<date>.sql.age
# Usage: restore-baserow.sh YYYY-MM-DD
# IMPORTANT: stops the baserow container, drops + recreates the schema, loads
# the backup, restarts the container. Destructive — confirms before doing it.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
DATE="${1:?usage: $0 YYYY-MM-DD}"
BACKUP="$NEXOSTRAT/vault/backups/baserow/$DATE.sql.age"
[ -f "$BACKUP" ] || { echo "no backup at $BACKUP" >&2; exit 1; }

set -a
. "$NEXOSTRAT/infra/docker/foss-stack/.env"
set +a

echo "WILL RESTORE Baserow from $BACKUP"
echo "This DROPS the current Baserow database. Type 'y' to continue:"
read -r ack
[ "$ack" = "y" ] || { echo "aborted"; exit 1; }

# Stop the Baserow application (DB stays running — embedded in container)
# Then drop + recreate the schema, load backup.
echo "Stopping baserow container..."
docker stop nexostrat-baserow

PLAIN=$(mktemp -p /dev/shm restore-baserow-XXXX.sql)
trap "shred -u $PLAIN 2>/dev/null || rm -f $PLAIN" EXIT
age -d -i ~/.config/age/key.txt "$BACKUP" > "$PLAIN"

# Start a Postgres-only shell inside baserow to drop + restore
docker start nexostrat-baserow
sleep 5
echo "Dropping + recreating baserow database..."
docker exec nexostrat-baserow bash -c "
PGPASSWORD=\$DATABASE_PASSWORD psql -U baserow -d postgres -c 'DROP DATABASE IF EXISTS baserow;'
PGPASSWORD=\$DATABASE_PASSWORD psql -U baserow -d postgres -c 'CREATE DATABASE baserow;'
"
echo "Loading dump..."
docker exec -i nexostrat-baserow bash -c \
    "PGPASSWORD=\$DATABASE_PASSWORD psql -U baserow -d baserow" < "$PLAIN"

echo "Restarting baserow..."
docker restart nexostrat-baserow
sleep 15
# Health check
for i in 1 2 3 4 5 6; do
    if curl -sf -o /dev/null "http://localhost/api/_health/" \
       --resolve baserow.nexostrat.local:443:127.0.0.1 2>/dev/null; then
        echo "Baserow healthy."
        exit 0
    fi
    sleep 5
done
echo "WARNING: baserow not yet healthy after restore — check docker logs"
exit 1
EOF
chmod +x /srv/Nexostrat/infra/recovery/restore-baserow.sh
```

- [ ] **Step 4: Run test, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_backup_restore_baserow.py -v
```

Expected: 1 passed (round-trip).

- [ ] **Step 5: Write `restore-bookstack.sh`**

```bash
cat > /srv/Nexostrat/infra/recovery/restore-bookstack.sh <<'EOF'
#!/usr/bin/env bash
# Decrypt + mysql restore BookStack from vault/backups/bookstack/<date>.sql.age
# Usage: restore-bookstack.sh YYYY-MM-DD

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
DATE="${1:?usage: $0 YYYY-MM-DD}"
BACKUP="$NEXOSTRAT/vault/backups/bookstack/$DATE.sql.age"
[ -f "$BACKUP" ] || { echo "no backup at $BACKUP" >&2; exit 1; }

set -a
. "$NEXOSTRAT/infra/docker/foss-stack/.env"
set +a

echo "WILL RESTORE BookStack from $BACKUP — drops current DB."
echo "Type 'y' to continue:"
read -r ack
[ "$ack" = "y" ] || { echo "aborted"; exit 1; }

docker stop nexostrat-bookstack
PLAIN=$(mktemp -p /dev/shm restore-bookstack-XXXX.sql)
trap "shred -u $PLAIN 2>/dev/null || rm -f $PLAIN" EXIT
age -d -i ~/.config/age/key.txt "$BACKUP" > "$PLAIN"

echo "Dropping + recreating bookstack database..."
docker exec nexostrat-bookstack-db sh -c \
    "mysql -uroot -p\"$BOOKSTACK_DB_ROOT_PASSWORD\" -e 'DROP DATABASE IF EXISTS bookstack; CREATE DATABASE bookstack;'"
echo "Loading dump..."
docker exec -i nexostrat-bookstack-db sh -c \
    "mysql -ubookstack -p\"$BOOKSTACK_DB_PASSWORD\" bookstack" < "$PLAIN"

docker start nexostrat-bookstack
sleep 20
for i in 1 2 3 4 5 6; do
    if docker exec nexostrat-bookstack curl -sf -o /dev/null http://localhost:80/status 2>/dev/null; then
        echo "BookStack healthy."
        exit 0
    fi
    sleep 5
done
echo "WARNING: bookstack not yet healthy after restore"
exit 1
EOF
chmod +x /srv/Nexostrat/infra/recovery/restore-bookstack.sh
```

Write the BookStack round-trip test (mirrors Baserow version) + run it:

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_backup_restore_bookstack.py <<'EOF'
"""BookStack round-trip: create a page, restore from earlier backup, verify gone."""
import subprocess, os, sys, time, datetime, pathlib, ssl, urllib.request, json

URL = os.environ["BOOKSTACK_URL"]
TOK = os.environ["BOOKSTACK_API_TOKEN"]
SEC = os.environ["BOOKSTACK_API_SECRET"]
NEXOSTRAT = "/srv/Nexostrat"
TODAY = datetime.date.today().isoformat()

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _api(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"{URL}/api{path}", data=data, method=method)
    req.add_header("Authorization", f"Token {TOK}:{SEC}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_CTX, timeout=15) as r:
        return json.loads(r.read() or b"{}")


def _glossary_book_id():
    return next(b["id"] for b in _api("GET", "/books")["data"] if b["name"] == "Glossary")


def test_round_trip_removes_post_backup_page():
    backup = pathlib.Path(f"{NEXOSTRAT}/vault/backups/bookstack/{TODAY}.sql.age")
    if not backup.exists():
        subprocess.run([f"{NEXOSTRAT}/infra/scripts/backup-foss-stack.sh"], check=True)

    marker = f"__test_marker_{int(time.time())}__"
    book_id = _glossary_book_id()
    new_page = _api("POST", "/pages", {"book_id": book_id, "name": marker, "markdown": "x"})
    assert any(p["name"] == marker for p in _api("GET", "/pages")["data"])

    r = subprocess.run(
        [f"{NEXOSTRAT}/infra/recovery/restore-bookstack.sh", TODAY],
        capture_output=True, text=True, input="y\n"
    )
    assert r.returncode == 0, f"restore failed: {r.stderr}"
    time.sleep(5)
    assert not any(p["name"] == marker for p in _api("GET", "/pages")["data"]), \
        "restore did not roll back the post-backup page"
EOF
```

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_backup_restore_bookstack.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Write `baserow-rotate-token.sh` (semi-manual playbook script)**

```bash
cat > /srv/Nexostrat/infra/recovery/baserow-rotate-token.sh <<'EOF'
#!/usr/bin/env bash
# Token rotation playbook (semi-manual — requires Baserow UI access).
# Steps the operator + tells them what to do at each.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}

cat <<EOM
=== Baserow API token rotation ===

Manual steps (perform in browser at https://baserow.nexostrat.local):

  1. Log in as ricardo@nexostrat.com.
  2. User menu (top-right) -> Settings -> API tokens.
  3. Find token named 'nexostrat-internal'. Click 'Revoke'.
  4. Click 'Create new token'. Name: 'nexostrat-internal'. Same scope as before
     (full access to all current and future workspaces).
  5. Copy the new token value (shown once).

Now run this script with the new token piped on stdin:

  echo 'NEW_TOKEN_VALUE' | $0 --apply

Or interactively:

  $0
  (you will be prompted)

EOM

if [ "${1:-}" = "--apply" ]; then
    NEW_TOKEN=$(cat)
else
    read -rsp "Paste new Baserow API token: " NEW_TOKEN; echo
fi
[ -n "$NEW_TOKEN" ] || { echo "empty token" >&2; exit 1; }

PLAIN=$(mktemp -p /dev/shm rotate-token-XXXX.env)
trap "shred -u $PLAIN 2>/dev/null || rm -f $PLAIN" EXIT
"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" --decrypt-to "$PLAIN"
sed -i "s|^BASEROW_API_TOKEN=.*|BASEROW_API_TOKEN=$NEW_TOKEN|" "$PLAIN"
"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" --encrypt-from "$PLAIN"

echo "Token rotated in secrets.env.age."
echo "Restarting bot + skill-renderer touchpoints would normally happen here;"
echo "Plan 04 wires this when the bot lands."
EOF
chmod +x /srv/Nexostrat/infra/recovery/baserow-rotate-token.sh
```

- [ ] **Step 7: Commit**

```bash
cd /srv/Nexostrat
git add infra/recovery/ tests/foss_stack/test_backup_restore_baserow.py \
        tests/foss_stack/test_backup_restore_bookstack.py
git commit -m "$(cat <<'EOF'
Plan 02a Task 14 · recovery scripts (restore + rotate)

restore-baserow.sh / restore-bookstack.sh:
- Take YYYY-MM-DD argument
- Confirm before destructive DROP DATABASE
- pg_restore / mysql restore from age-decrypted dump
- Restart container + health-check loop (6 attempts × 5s)

baserow-rotate-token.sh:
- Semi-manual playbook (UI revoke + recreate)
- Accepts new token on stdin or interactive prompt
- Updates secrets.env.age in place via run-with-secrets.sh

Round-trip tests for both services: create marker, restore, verify marker gone.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: `sync-state-from-baserow.sh`

**Files:**
- Create: `infra/scripts/sync-state-from-baserow.sh`
- Test: `tests/foss_stack/test_sync_state.py`

- [ ] **Step 1: Write failing test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_sync_state.py <<'EOF'
"""sync-state-from-baserow.sh rebuilds state.json from Baserow."""
import subprocess, sys, time, json, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"


def test_sync_rebuilds_state_json():
    slug = f"_test_sync_{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Sync Test", "testing"],
            cwd=NEXOSTRAT, capture_output=True, text=True, check=True
        )
        state = folder / "state.json"
        original = json.loads(state.read_text())

        # Mutate Baserow phase
        row = baserow._find_one("clients", "slug", slug)
        baserow._update("clients", row["id"], {"phase": "diagnostico_in_progress"})

        # State.json still shows old phase
        assert json.loads(state.read_text())["phase"] != "diagnostico_in_progress"

        # Run sync
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/sync-state-from-baserow.sh", slug],
            capture_output=True, text=True
        )
        assert r.returncode == 0, f"sync failed: {r.stderr}"

        # state.json should now reflect Baserow
        assert json.loads(state.read_text())["phase"] == "diagnostico_in_progress"
    finally:
        import shutil
        if folder.exists(): shutil.rmtree(folder)
EOF
```

- [ ] **Step 2: Run test, expect failure**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_sync_state.py -v
```

Expected: `FileNotFoundError`.

- [ ] **Step 3: Write the script**

```bash
cat > /srv/Nexostrat/infra/scripts/sync-state-from-baserow.sh <<'EOF'
#!/usr/bin/env bash
# Rebuild pipeline/clients/<slug>/state.json from Baserow (source-of-truth for metadata).
# Usage: sync-state-from-baserow.sh <slug> [<slug>...]   or
#        sync-state-from-baserow.sh --all

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}

"$NEXOSTRAT/infra/scripts/run-with-secrets.sh" \
  python3 -c "
import sys, json, pathlib
sys.path.insert(0, '$NEXOSTRAT/skills/shared')
import baserow

args = '''$*'''.split()
if not args:
    print('usage: sync-state-from-baserow.sh <slug> [<slug>...] | --all', file=sys.stderr)
    sys.exit(1)

if args == ['--all']:
    base = pathlib.Path('$NEXOSTRAT/pipeline/clients')
    slugs = [p.name for p in base.iterdir()
             if p.is_dir() and not p.name.startswith('_') and p.name != '_template']
else:
    slugs = args

for slug in slugs:
    row = baserow._find_one('clients', 'slug', slug)
    if not row:
        print(f'WARNING: no Baserow row for {slug}; skipping', file=sys.stderr)
        continue
    sj_path = pathlib.Path('$NEXOSTRAT/pipeline/clients') / slug / 'state.json'
    if not sj_path.exists():
        print(f'WARNING: no state.json at {sj_path}; skipping', file=sys.stderr)
        continue
    state = json.loads(sj_path.read_text())
    state.update({
        'slug': slug,
        'name': row['name'],
        'display_name': row.get('display_name', row['name']),
        'country': (row.get('country') or {}).get('value', state.get('country', '')),
        'sector': row.get('sector', state.get('sector', '')),
        'phase': (row.get('phase') or {}).get('value', state.get('phase', 'prospect')),
        'pilot': row.get('pilot', state.get('pilot', False)),
        'rfc_nit': row.get('rfc_nit', ''),
        '_synced_from_baserow_at': '$(date -Is)',
    })
    sj_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n')
    print(f'synced {slug}: phase={state[\"phase\"]}')
"
EOF
chmod +x /srv/Nexostrat/infra/scripts/sync-state-from-baserow.sh
```

- [ ] **Step 4: Run pytest, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_sync_state.py -v
```

Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
cd /srv/Nexostrat
git add infra/scripts/sync-state-from-baserow.sh tests/foss_stack/test_sync_state.py
git commit -m "Plan 02a Task 15 · sync-state-from-baserow.sh — on-demand reconcile of state.json"
```

---

## Task 16: 5 new runbooks

**Files:**
- Create: `docs/runbooks/baserow_down.md`
- Create: `docs/runbooks/bookstack_down.md`
- Create: `docs/runbooks/baserow_token_compromise.md`
- Create: `docs/runbooks/baserow_schema_drift.md`
- Create: `docs/runbooks/baserow_reconcile.md`

Each runbook is a stand-alone how-to. Standard structure: Symptoms → Detection → Recovery steps → Verification → Roll-forward notes.

- [ ] **Step 1: Write `baserow_down.md`**

```bash
mkdir -p /srv/Nexostrat/docs/runbooks
cat > /srv/Nexostrat/docs/runbooks/baserow_down.md <<'EOF'
# Runbook — Baserow down

Covers F1, F2, F3 from spec §7.2.

## Symptoms
- Telegram bot returns "Baserow no responde — datos pueden estar desactualizados" (fallback path).
- `curl -kf https://baserow.nexostrat.local/api/_health/` returns non-200 or connection-refused.
- `docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml ps` shows `nexostrat-baserow` as `exited` or `unhealthy`.
- systemd unit `nexostrat-baserow-reconcile.service` failed overnight (check `journalctl -u nexostrat-baserow-reconcile`).

## Diagnose
1. `docker logs nexostrat-baserow --tail 100`
2. Check for: Postgres "FATAL: database system was not properly shut down" (F2 corruption), OOM kills, disk-full.
3. `df -h /srv` — disk full? (F12, see disk_full.md if it exists.)

## Recovery — F1 (container crash, data intact)
```bash
docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml restart baserow
sleep 15
curl -kf https://baserow.nexostrat.local/api/_health/  # expect 200
```

## Recovery — F2 (Postgres corruption)
```bash
# Pick the most recent backup that doesn't have the corruption — usually yesterday's.
ls -la /srv/Nexostrat/vault/backups/baserow/
/srv/Nexostrat/infra/recovery/restore-baserow.sh YYYY-MM-DD
```

After restore, run reconcile to repair any divergence between filesystem deliverables and the restored Baserow state:

```bash
/srv/Nexostrat/infra/scripts/baserow-reconcile.sh
```

## Recovery — F3 (total data loss)
HP disk failure: failover to warm-standby per `hp_down.md` (Plan 01b).
After failover, the standby's vault has the latest off-site backup — same restore flow as F2.

## Verification
- `curl -kf https://baserow.nexostrat.local/api/_health/` returns 200.
- `python3 -m pytest /srv/Nexostrat/tests/foss_stack/test_baserow_health.py` passes.
- Sample query: `curl -k -H "Authorization: Token $TOKEN" $BASEROW_URL/api/database/workspaces/` returns the Nexostrat workspace.

## Roll-forward
If you restored from yesterday's backup, any data created since then is lost (RPO 24h Stage 1). Reconcile recovers deliverable rows from filesystem artefacts; meeting rows + financial rows must be manually re-entered if needed.
EOF
```

- [ ] **Step 2: Write `bookstack_down.md`**

```bash
cat > /srv/Nexostrat/docs/runbooks/bookstack_down.md <<'EOF'
# Runbook — BookStack down

Covers F4, F5, F6 from spec §7.2.

## Symptoms
- `curl -kf https://docs.nexostrat.local/status` returns non-200.
- Browser shows 502 / connection-refused.
- `docker compose ps` shows `nexostrat-bookstack` as `exited`/`unhealthy` OR `nexostrat-bookstack-db` exited.

## Diagnose
1. `docker logs nexostrat-bookstack --tail 100`
2. `docker logs nexostrat-bookstack-db --tail 100`
3. Common: MariaDB "Table 'bookstack.users' doesn't exist" (corruption), or `nexostrat-bookstack-db` exited (in which case bookstack waits).

## Recovery — F4 (container crash)
```bash
docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml restart bookstack-db
sleep 10
docker compose -f /srv/Nexostrat/infra/docker/foss-stack/docker-compose.yml restart bookstack
sleep 20
docker exec nexostrat-bookstack curl -sf http://localhost:80/status
```

## Recovery — F5 (MySQL corruption)
```bash
ls -la /srv/Nexostrat/vault/backups/bookstack/
/srv/Nexostrat/infra/recovery/restore-bookstack.sh YYYY-MM-DD
```

## Recovery — F6 (total data loss)
Same as Baserow F3: failover to warm-standby per `hp_down.md`.

## Verification
- `curl -kf https://docs.nexostrat.local/status` returns 200.
- Log in via web UI; verify ~7 seeded pages still present in shelf list.
- `python3 -m pytest /srv/Nexostrat/tests/foss_stack/test_bookstack_health.py` passes.

## Roll-forward
Pages Ricardo wrote since the last backup are lost (RPO 24h). No automated recovery; if a page is critical, recreate it from memory or git history of a related markdown file.
EOF
```

- [ ] **Step 3: Write `baserow_token_compromise.md`**

```bash
cat > /srv/Nexostrat/docs/runbooks/baserow_token_compromise.md <<'EOF'
# Runbook — Baserow API token compromise

Covers F8 from spec §7.2.

## Symptoms
- Audit log (Baserow Settings → Audit log) shows requests from unfamiliar IPs.
- Baserow logs show large unexpected query volume.
- Token accidentally committed to git history (catch via `pre-commit-secret-scan.sh`; if it slipped, history rewrite is a separate emergency).

## Immediate action (do not wait)
```bash
/srv/Nexostrat/infra/recovery/baserow-rotate-token.sh
```
Follow the prompts — UI revoke, UI re-create, paste new token.

## After rotation
1. Restart any process that holds the old token in memory:
   - When Plan 04 Telegram bot exists: `sudo systemctl restart nexostrat-telegram-bot.service`
   - Skill renderers re-read on each invocation (no restart needed).
2. Audit log: review requests with the old token in the 24h before rotation. Anything that looks like exfiltration → escalate (Ricardo + JP via Telegram).

## Verification
- Old token: `curl -k -H "Authorization: Token <OLD>" $BASEROW_URL/api/database/workspaces/` returns 401.
- New token: same call returns 200.

## Roll-forward
If history of `secrets.env.age` was somehow exposed: rotate all secrets in the file (age keys, other API tokens) per `docs/runbooks/key_compromise.md` (lands in Plan 02 / 10).
EOF
```

- [ ] **Step 4: Write `baserow_schema_drift.md`**

```bash
cat > /srv/Nexostrat/docs/runbooks/baserow_schema_drift.md <<'EOF'
# Runbook — Baserow schema drift

Covers F9 from spec §7.2.

## Symptoms
- Weekly `nexostrat-baserow-schema-check.service` failed (journal shows DRIFT lines).
- Manual run of `infra/scripts/baserow-schema-check.sh` exits non-zero with diff output.
- Skill renderer fails with 400 "field X does not exist" or "type mismatch."

## Diagnose
```bash
/srv/Nexostrat/infra/scripts/baserow-schema-check.sh
```

The diff output shows what changed between `infra/baserow/schema/canonical.json` (git tracked) and live Baserow.

Three categories of drift:
1. **Intentional UI edit by Ricardo** (e.g., added a useful new field) — commit a new canonical:
   ```bash
   /srv/Nexostrat/infra/scripts/run-with-secrets.sh \
     python3 /srv/Nexostrat/infra/baserow/export_schema.py
   git add infra/baserow/schema/canonical.json
   git commit -m "Baserow schema: <describe change>"
   ```
2. **Accidental UI edit** (renamed/deleted a field by mistake) — revert via UI; canonical is the source of truth.
3. **Migration regression** (a migration was edited but not re-run) — re-run migrations:
   ```bash
   /srv/Nexostrat/infra/scripts/run-with-secrets.sh \
     python3 /srv/Nexostrat/infra/baserow/migrations/run_all.py
   ```
   Then re-run schema-check to verify clean.

## Verification
```bash
/srv/Nexostrat/infra/scripts/baserow-schema-check.sh
# OK: schema matches canonical.json
```

## Roll-forward
If accidental deletion of data via UI edit destroyed rows: restore from yesterday's backup per `baserow_down.md` F2.
EOF
```

- [ ] **Step 5: Write `baserow_reconcile.md`**

```bash
cat > /srv/Nexostrat/docs/runbooks/baserow_reconcile.md <<'EOF'
# Runbook — Baserow reconcile (manual trigger)

Covers F11 from spec §7.2.

## When to run
- Skill renderer warning logs show "[baserow-sync] skipped: ..." for some output.
- Visual gap: a deliverable file exists in `pipeline/clients/<slug>/.../runs/` but not visible in Baserow.
- After a Baserow restore (F2/F3): catch up rows lost between backup and restore.
- Nightly cron handles routine cases. Manual trigger only for ad-hoc.

## Run
```bash
/srv/Nexostrat/infra/scripts/baserow-reconcile.sh
```

Expected output:
```
Reconcile complete: N orphan(s) added, M already in sync
```

## Output interpretation
- `N == 0` and `M > 0`: everything in sync, nothing to do.
- `N > 0`: orphans existed; they're now in Baserow. Check the audit by querying:
  ```bash
  /srv/Nexostrat/infra/scripts/run-with-secrets.sh \
    python3 -c "
  import sys; sys.path.insert(0, '/srv/Nexostrat/skills/shared')
  import baserow
  rows = baserow._request('GET', f'/api/database/rows/table/{baserow._table_id(\"deliverables\")}/?user_field_names=true&order_by=-created_at&size=10')
  for r in rows['results']:
      print(r['skill'], r['file_md'])
  "
  ```
- `WARNING: client folder X has no Baserow row`: a folder exists without a `clients` row. Likely the folder was created manually (bypassing `new-client.sh`). Fix:
  ```bash
  # Re-run new-client.sh for the slug; it's idempotent for the folder but will create the row.
  /srv/Nexostrat/infra/scripts/new-client.sh <slug> <country> "<name>" "<sector>"
  ```

## Verification
After reconcile, run again — should be no-op:
```bash
/srv/Nexostrat/infra/scripts/baserow-reconcile.sh
# Reconcile complete: 0 orphan(s) added, X already in sync
```
EOF
```

- [ ] **Step 6: Commit**

```bash
cd /srv/Nexostrat
git add docs/runbooks/baserow_down.md docs/runbooks/bookstack_down.md \
        docs/runbooks/baserow_token_compromise.md \
        docs/runbooks/baserow_schema_drift.md docs/runbooks/baserow_reconcile.md
git commit -m "$(cat <<'EOF'
Plan 02a Task 16 · 5 runbooks for FOSS stack failure modes

Covers F1-F6, F8, F9, F11 from spec §7.2:
- baserow_down.md — F1/F2/F3 container crash / corruption / total loss
- bookstack_down.md — F4/F5/F6 same shape
- baserow_token_compromise.md — F8 rotation playbook
- baserow_schema_drift.md — F9 weekly check + 3 categories of drift
- baserow_reconcile.md — F11 manual trigger guide

Each follows Symptoms → Diagnose → Recovery → Verification → Roll-forward.

F7 (HP server down) is handled by Plan 01b's hp_down.md (extended in Task 17).
F10 (bot fallback) is Plan 04 territory.
F12 (disk full) is generic infra runbook, deferred.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 17: Extend existing `hp_down.md` with FOSS stack boot sequence

**Files:**
- Modify: `docs/runbooks/hp_down.md`

- [ ] **Step 1: Inspect current `hp_down.md`**

```bash
grep -n "^##" /srv/Nexostrat/docs/runbooks/hp_down.md
```

Identify the section where services are listed (typically "Bring up services on standby" or similar).

- [ ] **Step 2: Append FOSS-stack boot sub-section**

Open the file and append the following block before the final "Verification" section:

```markdown
## FOSS stack boot sequence (Plan 02a addition)

After the standby is reachable and Tailscale is up:

```bash
# Ensure /etc/hosts has Tailscale-side names
grep -q "baserow.nexostrat.local" /etc/hosts || \
  echo "<STANDBY_TAILSCALE_IP> baserow.nexostrat.local docs.nexostrat.local" | sudo tee -a /etc/hosts

# Restore .env from vault (it lives in vault/backups/foss-stack-env/ — confirm
# the standby has the latest copy via warm-rsync, Plan 01b)
ls -la /srv/Nexostrat/vault/backups/foss-stack-env/  # newest .env.age

PLAIN=$(mktemp -p /dev/shm)
age -d -i ~/.config/age/key.txt /srv/Nexostrat/vault/backups/foss-stack-env/LATEST.env.age > $PLAIN
cp $PLAIN /srv/Nexostrat/infra/docker/foss-stack/.env
chmod 600 /srv/Nexostrat/infra/docker/foss-stack/.env
shred -u $PLAIN

# Start the stack
sudo systemctl enable --now nexostrat-foss-stack.service
sleep 90

# Restore latest backups from vault/backups/
TODAY=$(ls -t /srv/Nexostrat/vault/backups/baserow/ | head -1 | sed 's/.sql.age//')
/srv/Nexostrat/infra/recovery/restore-baserow.sh "$TODAY"
/srv/Nexostrat/infra/recovery/restore-bookstack.sh "$TODAY"

# Smoke-test
/srv/Nexostrat/infra/scripts/smoke-test.sh
```

> **Note:** `vault/backups/foss-stack-env/` is the location for the latest `.env`
> age-encrypted blob. Backups script must be extended in a future patch to also
> snapshot `.env` (currently `.env` lives only on HP — single point of failure).
> Track via task `t-vault-backup-foss-env` (open during Plan 02a wrap).
```

(Use `Edit` tool or your editor to append the block above; exact insertion point depends on the current `hp_down.md` structure.)

- [ ] **Step 3: Add the follow-up task to tasks.json**

```bash
# Edit tasks.json by hand to add an entry. Use the schema established in Plan 01a.
# Add to the tasks array:
#
# {
#   "id": "t-vault-backup-foss-env",
#   "title": "Add infra/docker/foss-stack/.env to nightly backup encrypted snapshot",
#   "status": "open",
#   "priority": "medium",
#   "due": "2026-06-30",
#   "notes": "hp_down.md assumes vault/backups/foss-stack-env/LATEST.env.age exists; backup-foss-stack.sh does not yet snapshot .env. Add as 5th artefact. Required for clean warm-standby failover."
# }
```

Validate the JSON schema:

```bash
python3 -c "
import jsonschema, json
jsonschema.validate(json.load(open('/srv/Nexostrat/tasks.json')),
                    json.load(open('/srv/Nexostrat/infra/schemas/tasks.schema.json')))
"
```

- [ ] **Step 4: Commit**

```bash
cd /srv/Nexostrat
git add docs/runbooks/hp_down.md tasks.json
git commit -m "Plan 02a Task 17 · hp_down.md extended with FOSS stack boot sequence"
```

---

## Task 18: Extend `smoke-test.sh` with FOSS stack checks

**Files:**
- Modify: `infra/scripts/smoke-test.sh`

- [ ] **Step 1: Inspect current smoke-test**

```bash
wc -l /srv/Nexostrat/infra/scripts/smoke-test.sh
grep -c "echo.*PASS\|echo.*FAIL" /srv/Nexostrat/infra/scripts/smoke-test.sh
```

Confirm the count of existing checks (~6 per Plan 01c R2 rich version).

- [ ] **Step 2: Append 6 new checks**

Add the following block at the end of the existing checks, before the final summary print:

```bash
cat >> /srv/Nexostrat/infra/scripts/smoke-test.sh <<'EOF'

# ═════ Plan 02a Task 18 — FOSS stack checks ═════

# Check 7: Baserow health endpoint
if curl -ksf -o /dev/null --max-time 5 https://baserow.nexostrat.local/api/_health/; then
    echo "PASS: baserow health"
    : $((CHECKS_PASS+=1))
else
    echo "FAIL: baserow health (URL unreachable or non-200)"
    : $((CHECKS_FAIL+=1))
fi

# Check 8: BookStack health endpoint
if curl -ksf -o /dev/null --max-time 5 https://docs.nexostrat.local/status; then
    echo "PASS: bookstack health"
    : $((CHECKS_PASS+=1))
else
    echo "FAIL: bookstack health"
    : $((CHECKS_FAIL+=1))
fi

# Check 9: Baserow schema canonical matches live
if "$NEXOSTRAT/infra/scripts/baserow-schema-check.sh" >/dev/null 2>&1; then
    echo "PASS: baserow schema canonical match"
    : $((CHECKS_PASS+=1))
else
    echo "FAIL: baserow schema drift detected"
    : $((CHECKS_FAIL+=1))
fi

# Check 10: Baserow reconcile is a no-op (means filesystem ↔ Baserow in sync)
RECONCILE_OUT=$("$NEXOSTRAT/infra/scripts/baserow-reconcile.sh" 2>&1 || true)
if echo "$RECONCILE_OUT" | grep -q "0 orphan(s) added"; then
    echo "PASS: baserow reconcile no-op"
    : $((CHECKS_PASS+=1))
else
    echo "FAIL: baserow reconcile found orphans — $RECONCILE_OUT"
    : $((CHECKS_FAIL+=1))
fi

# Check 11: Yesterday's backup files exist + decrypt
YDAY=$(date -d 'yesterday' +%F 2>/dev/null || date -v-1d +%F)
for svc in baserow bookstack; do
    BK="$NEXOSTRAT/vault/backups/$svc/$YDAY.sql.age"
    if [ -f "$BK" ] && age -d -i ~/.config/age/key.txt "$BK" >/dev/null 2>&1; then
        echo "PASS: $svc backup $YDAY decrypts"
        : $((CHECKS_PASS+=1))
    else
        echo "FAIL: $svc backup $YDAY missing or undecryptable"
        : $((CHECKS_FAIL+=1))
    fi
done

# Check 12: docker compose stack is healthy
UNHEALTHY=$(docker compose -f "$NEXOSTRAT/infra/docker/foss-stack/docker-compose.yml" ps \
    --format '{{.Name}} {{.Status}}' | grep -ci unhealthy || true)
if [ "$UNHEALTHY" = "0" ]; then
    echo "PASS: all foss-stack containers healthy"
    : $((CHECKS_PASS+=1))
else
    echo "FAIL: $UNHEALTHY unhealthy container(s) in foss-stack"
    : $((CHECKS_FAIL+=1))
fi
EOF
```

> **Note:** The `: $((CHECKS_PASS+=1))` pattern assumes those counter variables exist in the original `smoke-test.sh`. If they don't (different bookkeeping pattern), adapt — the script's existing summary block knows how to count its checks.

- [ ] **Step 3: Run extended smoke-test, expect all PASS**

```bash
/srv/Nexostrat/infra/scripts/smoke-test.sh
```

Expected: existing 6 checks PASS + 7 new checks PASS = 13 PASS, 0 FAIL.

Note: Check 11 may FAIL on the same day Plan 02a Task 13 first ran (yesterday's backup doesn't exist yet). Wait one day, or temporarily replace `$YDAY` with `$TODAY` for the first run, then revert.

- [ ] **Step 4: Commit**

```bash
cd /srv/Nexostrat
git add infra/scripts/smoke-test.sh
git commit -m "Plan 02a Task 18 · smoke-test.sh — 7 new FOSS stack checks"
```

---

## Task 19: End-to-end integration test

**Files:**
- Create: `tests/foss_stack/test_e2e_pipeline.py`

- [ ] **Step 1: Write the test**

```bash
cat > /srv/Nexostrat/tests/foss_stack/test_e2e_pipeline.py <<'EOF'
"""End-to-end:
  1. Scaffold a test client via new-client.sh → folder + Baserow row + state.json sync.
  2. Run Skill 01 renderer over a synthetic .md → docx + deliverables row.
  3. Run reconcile → no-op (everything in sync).
  4. Cleanup.
"""
import subprocess, sys, time, json, shutil, pathlib
sys.path.insert(0, "/srv/Nexostrat/skills/shared")
import baserow

NEXOSTRAT = "/srv/Nexostrat"


def test_e2e_scaffold_render_reconcile():
    slug = f"_e2e_{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")

    try:
        # 1. Scaffold
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "E2E Test SA", "testing"],
            cwd=NEXOSTRAT, capture_output=True, text=True
        )
        assert r.returncode == 0, f"new-client failed: {r.stderr}"
        assert folder.exists(), "folder not created"
        assert (folder / "state.json").exists()
        client = baserow._find_one("clients", "slug", slug)
        assert client is not None, "Baserow client row not created"

        # 2. Render
        run_dir = folder / "01_company_analysis/runs/2026-05-19_mode-a"
        run_dir.mkdir(parents=True, exist_ok=True)
        md = run_dir / f"{slug}_AnalisisCompania_20260519.md"
        md.write_text("# E2E Test Analysis\n\nMinimal body.\n")

        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
             "python3", f"{NEXOSTRAT}/skills/01_company_analyst/scripts/generate_docx.py",
             str(md)],
            capture_output=True, text=True
        )
        assert r.returncode == 0, f"renderer failed: {r.stderr}"
        docx = run_dir / f"{slug}_AnalisisCompania_20260519.docx"
        assert docx.exists(), "docx not generated"
        deliv = baserow._find_one("deliverables", "file_md", str(md))
        assert deliv is not None, "deliverable row not created"

        # 3. Reconcile (should be no-op)
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/baserow-reconcile.sh"],
            capture_output=True, text=True
        )
        assert r.returncode == 0
        assert "0 orphan(s) added" in r.stdout, f"unexpected orphans: {r.stdout}"

    finally:
        if folder.exists():
            shutil.rmtree(folder)
EOF
```

- [ ] **Step 2: Run test, expect PASS**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/test_e2e_pipeline.py -v
```

Expected: 1 passed.

- [ ] **Step 3: Run the full foss_stack test suite, verify no regressions**

```bash
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/ -v
```

Expected: all tests pass (sum of all task-tests + integration tests).

- [ ] **Step 4: Commit**

```bash
cd /srv/Nexostrat
git add tests/foss_stack/test_e2e_pipeline.py
git commit -m "Plan 02a Task 19 · end-to-end integration test (scaffold → render → reconcile)"
```

---

## Task 20: Master plan index update + tag `v0.2a-foss-stack`

**Files:**
- Modify: `00_META/plans/README.md`
- Modify: `STATUS.md` (mark Plan 02a DONE)
- Modify: `tasks.json` (close `t-plan-02-write` if Plan 02b is also written; for now, split it)
- Modify: `00_META/CHANGELOG.md` (new row)

- [ ] **Step 1: Update master plan index status row**

In `00_META/plans/README.md`, edit the Plan 02 row to reflect the split + Plan 02a completion. The row should change from a single Plan 02 line to two lines:

```markdown
| 02a | FOSS Stack Integration (Baserow + BookStack + recovery) | **DONE** | [`2026-05-19_plan-02a-foss-stack.md`](2026-05-19_plan-02a-foss-stack.md) | actual: ~7 days | 2026-06-15 | YYYY-MM-DD |
| 02b | Documentation System (Diátaxis + drift hook + auto-generators + ADRs + how-tos) | DRAFT-PENDING | — | ~2 days | — | — |
```

Update the dependency graph diagram (further down) to show 02a and 02b as siblings depending on 01c, both unblocking 03/04 in parallel.

- [ ] **Step 2: Add per-plan header for 02b**

Below the existing per-plan headers, replace the unified "Plan 02" header with:

```markdown
### Plan 02a — FOSS Stack Integration

**Goal:** Deploy Baserow + BookStack + Caddy as a self-hosted FOSS stack on HP, wire them into existing skills + `new-client.sh`, ship backup/recovery infrastructure.

**Deliverables:** docker-compose + systemd unit; 4 Baserow tables + 11 views + canonical schema; BookStack 4 shelves + 9 books + 7 seeded pages; `skills/shared/baserow.py` helper; extended `new-client.sh` + 5 skill renderers; nightly backups + weekly schema check + nightly reconcile; 5 recovery scripts; 5 runbooks; extended smoke-test; e2e integration test.

**Dependencies:** Plan 01c (foundation milestone).

**Success criteria:** see plan file § Plan-level success criteria.

**File:** [`2026-05-19_plan-02a-foss-stack.md`](2026-05-19_plan-02a-foss-stack.md) — ~20 tasks.

### Plan 02b — Documentation System

**Goal:** Set up `docs/` Diátaxis structure + paired-files drift hook + auto-generators + write the first ~10 how-tos so Stage 1 has operational docs both Ricardo and JP can read.

**Deliverables:** see Plan 02 original deliverables in the prior version of this index (unchanged except: Plan 02b's docs-pair hook does NOT need to handle FOSS stack content — those docs land already-paired via Plan 02a).

**Dependencies:** Plan 01c. (Independent of Plan 02a — can land in parallel or after.)

**File:** *(to be written via writing-plans when execution starts)*
```

- [ ] **Step 3: Update STATUS.md**

Append a "Done this session" block describing what landed across all 20 Plan 02a tasks. Update "Current phase" to reflect Plan 02a completion + Plan 02b queued.

- [ ] **Step 4: Update CHANGELOG.md**

Append a new row:

```markdown
| 2026-MM-DD | Claude (Opus 4.7 1M, Plan 02a executed) | **Plan 02a DONE.** Tasks 1-20 executed; FOSS stack (Baserow + BookStack + Caddy) deployed on HP; 4 Baserow tables + 11 views + 9 BookStack books + 7 seeded pages live; `skills/shared/baserow.py` helper + 5 skill renderers extended + new-client.sh extended; nightly backup + weekly schema check + nightly reconcile timers active; 5 runbooks + 5 recovery scripts shipped; tag `v0.2a-foss-stack`. Plan 02b (Docs Diátaxis) remains DRAFT-PENDING, can land in parallel with Plans 03/04. |
```

- [ ] **Step 5: Validate JSON schemas + commit + tag**

```bash
cd /srv/Nexostrat
python3 -c "
import jsonschema, json
jsonschema.validate(json.load(open('tasks.json')),
                    json.load(open('infra/schemas/tasks.schema.json')))
jsonschema.validate(json.load(open('calendar.json')),
                    json.load(open('infra/schemas/calendar.schema.json')))
print('schemas OK')
"

git add 00_META/plans/README.md STATUS.md 00_META/CHANGELOG.md tasks.json
git commit -m "$(cat <<'EOF'
Plan 02a Task 20 · DONE — master index, STATUS, CHANGELOG updated

Plan 02 split into 02a (FOSS Stack) + 02b (Docs Diátaxis), matching the
Plan 01a/b/c precedent. 02a is DONE; 02b remains DRAFT-PENDING.

Master index dependency graph updated: 02a + 02b are siblings depending on 01c,
both unblock 03/04 in parallel.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git tag -a v0.2a-foss-stack -m "FOSS stack (Baserow + BookStack) integrated; pipeline writes through to Baserow"
git push origin main
git push origin v0.2a-foss-stack
```

- [ ] **Step 6: Final verification**

```bash
/srv/Nexostrat/infra/scripts/smoke-test.sh
echo "---"
cd /srv/Nexostrat
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
  python3 -m pytest tests/foss_stack/ -v 2>&1 | tail -20
```

Expected: smoke-test PASS all 13 checks; pytest summary shows all foss_stack tests passing.

---

## Self-review (writer pass)

Done with fresh eyes against the spec:

1. **Spec coverage check:**
   - § 3 Architecture → Task 1 (compose+Caddy) ✓
   - § 4 Data model → Tasks 4-6 (schema + views + snapshot) ✓
   - § 5 BookStack → Tasks 11-12 (shelves + pages) ✓
   - § 6.1 Bot queries → Plan 04 territory (correctly deferred)
   - § 6.2 `new-client.sh` POST → Task 8 ✓
   - § 6.3 Skill renderers → Task 9 ✓
   - § 6.4 Meeting capture (manual Stage 1) → no script work needed; deferred
   - § 6.5 events.jsonl → Plan 03 territory (correctly deferred)
   - § 6.6 Daily brief → Plan 03 territory (correctly deferred)
   - § 6.7 BookStack integration minimal → covered (none needed Stage 1)
   - § 7.1 Backup strategy → Task 13 ✓
   - § 7.2 Failure modes → Tasks 16+17 (runbooks) cover F1-F9, F11; F7 in Plan 01b; F10/F12 deferred to other plans
   - § 7.3 Recovery scripts → Task 14 ✓
   - § 7.4 Runbooks → Task 16 ✓
   - § 7.5 Non-obvious decisions → captured in runbooks + Task 14 confirm prompt + Task 6 canonical schema
   - § 8 MVP scope → Tasks 1-20 all aligned

   Gap detected and patched mid-write: `vault/backups/foss-stack-env/` referenced in Task 17 but not produced by Task 13's `backup-foss-stack.sh`. Addressed via follow-up task `t-vault-backup-foss-env` (added in Task 17 Step 3 — medium priority, due 2026-06-30).

2. **Placeholder scan:** No "TBD" / "TODO" / "implement later" in any task. The seed page bodies (Task 12) ARE intentionally stub-content (one paragraph each — Ricardo grows them organically); the structure + initial content commit is real, not a placeholder.

3. **Type/name consistency:** `baserow._find_one`, `baserow._update`, `baserow._table_id`, `baserow.post_client`, `baserow.post_deliverable`, `baserow.BASE_URL` are referenced identically across Tasks 7, 8, 9, 10, 15, 19. Field names (`slug`, `phase`, `file_md`, `client`) match between schema migrations (Task 4) and helper module (Task 7). Skill values in `STATION_TO_SKILL` (Task 10) match the single_select options in `deliverables` (Task 4 step 6).

4. **Scope:** Plan 02a is ~20 tasks, ~3500 lines (target was 3500-4500). Reasonable single-plan size. Plan 02b remains separately scoped per the split decision.

---

## Execution Handoff

Plan complete and saved to `/srv/Nexostrat/00_META/plans/2026-05-19_plan-02a-foss-stack.md`. Two execution options:

**1. Subagent-Driven (recommended)** — A fresh subagent per task, review between tasks, fast iteration. Best for Plan 02a because Tasks 1-2, 4-7, 10-19 are scriptable + testable. Task 3 (manual web-UI gate) needs main-session execution; flag it to pause subagent-driven flow there.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints. Slower but lets Ricardo see each commit in-context.

**Pick approach, and decide whether to start today or queue for after the Trixx pilot (2026-05-25).**
