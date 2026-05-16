# System map — Nexostrat infrastructure

> **Updated:** 2026-05-16 (Plan 01b Task 1)
> **Owner:** Founder
> **Purpose:** Single source of truth for "where things live" across hosts,
> containers, and the systemd surface. Consult before adding any new unit,
> service, or scheduled job.

## Hosts

| Hostname | Tailscale IP | OS | Role | Notes |
|---|---|---|---|---|
| `ricardo-hp-laptop` | `100.64.121.80` | Linux Mint 22.2 | hp-server | Primary host; runs Gitea, bot, shadow stack |
| `<warm-standby-tbd>` | `<TBD>` | Linux Mint 22.2 | hp-standby | Filled at standby provisioning (Plan 01b Tasks 7-9) |
| `ricardo-desktop`     | `<TBD>` | Linux Mint 22.2 | ricardo-desktop | GPU host (Ollama); wake-on-LAN target |

> **OS pinning:** Linux Mint 22.2 LTS across all hosts at Stage 1. Bump this
> column (here and in `infra/machines/*.yaml`) when any host is upgraded.

## Docker stack on hp-server

Compose file: `/srv/Nexostrat/docker-compose.yml` (Plan 02 lands the actual compose; Plan 01b uses what already exists for Gitea).

| Container | Image (pinned) | Host port | Bound to | Purpose |
|---|---|---|---|---|
| `gitea`     | `gitea/gitea:1.22` | `3001` | Tailscale `100.64.121.80` | Git origin, web UI |
| `nexostrat-bot` | (custom — Plan 04) | (none) | n/a | Telegram bot service |
| (others)    | (Plan 02-08 add) | | | |

## Gitea on-disk paths

| What | Host-side path |
|---|---|
| Gitea data root (bind-mount of `/data` in container) | `/srv/gitea/data` |
| `nexostrat/nexostrat` bare repo | `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git` |
| `refs/heads/main` (the watch target) | `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main` |
| Host-side owner of bare repo | `ricardo:ricardo` (verified Plan 01b Task 1 pre-flight) |

**Path-watcher access:** The mirror systemd units (Tasks 4-5) watch the
`refs/heads/main` file. The host-side bare repo is owned by `ricardo:ricardo`,
so the mirror service (running as `ricardo`) reads it directly — no chmod or
elevated privilege needed.

## SSH config

`~/.ssh/config` aliases for git operations:

| Host alias | Real host | Port | Identity |
|---|---|---|---|
| `gitea-nexostrat` | `100.64.121.80` (Tailscale) | `2222` | `~/.ssh/nexostrat_ed25519` |
| `github.com` | (default) | `22` | `~/.ssh/nexostrat_ed25519` |
| `codeberg.org` | (default) | `22` | `~/.ssh/nexostrat_ed25519` |

## Mirrors (populated by Tasks 4-5)

> **Asymmetric topology note (2026-05-16):** Codeberg uses the firm-identity
> namespace `nexostrat/nexostrat`. GitHub uses Ricardo's personal namespace
> `ricardomejiacaicedo-del/nexostrat` because the existing `nexostrat_ed25519`
> SSH key authenticates as `ricardomejiacaicedo-del` on github.com (registered
> during 2026-05-14 terrain prep). Re-aligning to a firm-identity GitHub
> namespace is deferred to a Stage 2 cleanup.

| Mirror | Remote URL | Trigger | Service |
|---|---|---|---|
| GitHub | `git@github.com:ricardomejiacaicedo-del/nexostrat.git` | systemd `.path` watching Gitea bare-repo `refs/heads/main` | `nexostrat-mirror-github.service` |
| Codeberg | `git@codeberg.org:nexostrat/nexostrat.git` | same | `nexostrat-mirror-codeberg.service` |

## Warm-standby (populated by Tasks 7-12)

| Field | Value |
|---|---|
| Hostname | `<TBD-at-provisioning>` |
| Tailscale IP | `<TBD>` |
| Clone path | `/srv/Nexostrat/` (mirror of HP) |
| Rsync source | `ricardo@hp-server:/srv/Nexostrat/` |
| Rsync schedule | nightly 03:00 America/Tijuana |
| Service status at rest | All Docker services pulled but stopped |
| Failover RTO target | 15-30 min |

## Systemd units (populated by Tasks 4-5, 9, 12)

System-level units at `/etc/systemd/system/`:

| Unit | Type | Trigger | Purpose |
|---|---|---|---|
| (filled by Plan 01b execution) | | | |

## Cross-cutting notes

- All mirror PATs (`GITHUB_MIRROR_PAT`, `CODEBERG_MIRROR_PAT`) live in
  `secrets.env.age` per `infra/secrets/MANIFEST.md`. The mirror service
  reads them via `infra/scripts/run-with-secrets.sh`.
- The age key for decryption is `~/.config/age/nexostrat.key.age` for
  `ricardo`. JP's same-named file on his machine has the same purpose.
- The mirror `.service` units are NOT triggered by Gitea internals (per
  C4 fix — Gitea hooks can't decrypt). They are triggered by `.path` units
  on the host that watch the bare-repo file.

## What this map is NOT

- Not a runbook (those live in `docs/runbooks/`).
- Not a credentials store (those live in `secrets.env.age`).
- Not auto-generated — humans update this when they touch infrastructure.
  Stale entries trigger a quarterly review (`00_PARTNERSHIP/reviews/`).
