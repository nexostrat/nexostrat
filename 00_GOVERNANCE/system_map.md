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

| Container | Image | Host port | Bound to | Purpose |
|---|---|---|---|---|
| `gitea`     | `gitea/gitea:latest` (running 1.25.5) | `3001` (web), `2222` (SSH) | `0.0.0.0` (all interfaces) | Git origin, web UI |
| `nexostrat-bot` | (custom — Plan 04) | (none) | n/a | Telegram bot service |
| (others)    | (Plan 02-08 add) | | | |

> **Image-pinning gap:** `gitea/gitea:latest` is NOT a pinned tag — Gitea
> could float to a new minor version on container restart. Plan 02 owns the
> compose file landing; the fix is to pin to `gitea/gitea:1.25.5` (the version
> currently running) or to a content digest, then update this row.
>
> **Network-binding gap:** Gitea listens on `0.0.0.0`, not the Tailscale IP.
> Access control is currently host-level: Tailscale ACLs + LAN trust. If the
> host ever joins an untrusted LAN, port 3001/2222 are exposed. Plan 02 may
> rebind to `127.0.0.1:3001:3000` and route Tailscale-only via reverse proxy.

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
| `gitea-nexostrat`     | `100.64.121.80` (Tailscale) | `2222` | `~/.ssh/nexostrat_ed25519` |
| `github-nexostrat`    | `github.com`                | `22`   | `~/.ssh/nexostrat_ed25519` |
| `codeberg-nexostrat`  | `codeberg.org`              | `22`   | `~/.ssh/nexostrat_ed25519` |

All three aliases set `IdentitiesOnly yes` so the firm key never leaks into
generic git operations (e.g., `ssh -T git@github.com` without an alias hits a
DIFFERENT identity — typically Ricardo's personal-account key).

## Mirrors

Both mirrors live in the firm-identity namespace `nexostrat/nexostrat`. The
`nexostrat_ed25519` key is registered on the firm GitHub user (`Hi nexostrat!`
on `ssh -T git@github-nexostrat`) and on the firm Codeberg user.

> **Identity caveat — DO NOT use bare-domain SSH for firm git ops:** Running
> `ssh -T git@github.com` (no alias) hits Ricardo's default identity and reports
> `Hi ricardomejiacaicedo-del!` — that's the personal account, NOT the firm.
> Always use the alias (`git@github-nexostrat:...`) to force the firm key. The
> mirror service uses the alias form; manual debugging should too.

| Mirror | Remote URL | Trigger | Service | Last validated 60s window |
|---|---|---|---|---|
| GitHub   | `git@github-nexostrat:nexostrat/nexostrat.git`   | systemd `.path` watching Gitea bare-repo `refs/heads/main` | `nexostrat-mirror-github.service`   | 2026-05-16 — **3 s** (push → github/main matches) |
| Codeberg | `git@codeberg-nexostrat:nexostrat/nexostrat.git` | same                                                       | `nexostrat-mirror-codeberg.service` | 2026-05-16 — **8 s** (push → codeberg/main matches) |

The remote URLs use the SSH-config aliases (not the bare domain), which forces
the `nexostrat_ed25519` identity via `IdentitiesOnly yes`. This is the same
pattern as the `gitea-nexostrat` origin already in use.

End-to-end validated 2026-05-16 (commit `d04191d`): a single `git push origin
main` propagated to both mirrors within the 60-second success window. The
sentinel `infra/systemd/.last-mirror-test` carries the timestamp of the most
recent end-to-end test and gets overwritten on each future validation pass.

## Warm-standby (populated by Tasks 7-12)

| Field | Value |
|---|---|
| Hostname | `<TBD-at-provisioning>` |
| Tailscale IP | `<TBD>` |
| Clone path | `/srv/Nexostrat/` (mirror of HP) |
| Rsync source | `ricardo@100.64.121.80:/srv/Nexostrat/` (Tailscale IP of `ricardo-hp-laptop`) |
| Rsync schedule | nightly 03:00 America/Tijuana |
| Service status at rest | All Docker services pulled but stopped |
| Failover RTO target | 15-30 min |

## Systemd units (populated by Tasks 4-5, 9, 12)

System-level units at `/etc/systemd/system/`:

| Unit | Type | Trigger | Purpose |
|---|---|---|---|
| `nexostrat-mirror-github.path`     | path-watcher | gitea bare-repo `refs/heads/main` change | Triggers `nexostrat-mirror-github.service`     |
| `nexostrat-mirror-github.service`  | oneshot      | invoked by .path                         | Pushes HP origin → GitHub via SSH alias        |
| `nexostrat-mirror-codeberg.path`   | path-watcher | gitea bare-repo `refs/heads/main` change | Triggers `nexostrat-mirror-codeberg.service`   |
| `nexostrat-mirror-codeberg.service`| oneshot      | invoked by .path                         | Pushes HP origin → Codeberg via SSH alias      |

## Cross-cutting notes

- The mirror services use **SSH only** (via the `~/.ssh/config` aliases set
  in the `.service` units' git push command). They do NOT read the PATs at
  runtime. SSH-only is the Stage-1 design (one identity surface, no token
  expiration mid-mirror).
- The PATs (`GITHUB_MIRROR_PAT`, `CODEBERG_MIRROR_PAT`) live in
  `secrets.env.age` per `infra/secrets/MANIFEST.md` and are reserved for
  a future HTTPS-fallback path (Plan 02+, not yet wired). Until that wiring
  lands, `infra/scripts/run-with-secrets.sh` is not called by these
  mirror services.
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
