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
| ~~`NOTION_API_KEY`~~ | ~~Notion~~ | ~~Meeting transcription / `/note` plugin~~ | ~~every 6 mo~~ | **DEPRECATED 2026-05-16** | Per ADR-038: Notion exits firm-level. The variable will be physically stripped from `secrets.env.age` at next TTY-required re-encrypt (tracked in `t-plan-01a-jp-and-tty-deferred`). FOSS replacement for meeting capture decided in Plan 02 — no API key needed if self-hosted Whisper.cpp + Ollama. |
| `TELEGRAM_BOT_TOKEN` | Telegram | `nexostrat-bot` Docker service (Plan 04) | only on suspected leak | (not yet provisioned) | Allowlist enforced via `infra/telegram/allowlist.yaml` |
| `RCLONE_DRIVE_TOKEN` | Google Drive (OAuth via rclone) | Heavy-asset upload (Plan 08+) | every 12 mo or on token expiry | (not yet provisioned) | Drive 2TB account |

## Rotation procedure (per secret)

1. Generate new value at the provider.
2. Decrypt `secrets.env.age` to `/dev/shm` (age 1.1.0+ accepts passphrase-protected identity files directly via `-i`; one passphrase prompt, no subshell):
   ```bash
   age -d -i ~/.config/age/nexostrat.key.age secrets.env.age \
       > /dev/shm/secrets.env.tmp
   ```
3. Edit the value in place (e.g., via `nano /dev/shm/secrets.env.tmp`).
4. Re-encrypt to both recipients (`&&`-chained so a partial `age` write does NOT trigger `shred` of the only plaintext copy — see 2026-05-16 hardening in commit `ed9a596`):
   ```bash
   age -R infra/age-recipients.txt -o secrets.env.age /dev/shm/secrets.env.tmp \
       && shred -u /dev/shm/secrets.env.tmp
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
