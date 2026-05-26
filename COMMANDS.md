# Nexostrat — Commands

> **Pattern:** one `COMMANDS.md` per project folder, sections per PC. This file lives in the Nexostrat repo so it travels with the project. The per-PC aggregator (`~/Desktop/COMMANDS.md`) points to this file and adds OS-level commands + cross-project navigation.
>
> **PCs covered here:**
> - **Server PC** (`ricardo-hp-laptop`) — Tailscale `100.64.121.80`. Hosts the Nexostrat infra (Gitea origin, FOSS stack, mirror cluster, vault). All daily and periodic Nexostrat operations run here.
> - **Desktop PC** — Ricardo's more powerful machine. Used to host online meetings + record + transcribe. Does NOT host Nexostrat infra. Transcripts get transferred to the server PC for Skill 05 consumption.

---

# Server PC (`ricardo-hp-laptop`)

This is where the Nexostrat repo lives at `/srv/Nexostrat/` and all infra (Baserow, BookStack, Caddy, mirrors, timers) runs.

## Session lifecycle (Claude Code at `/srv/Nexostrat/`)

```
Start Session              # Claude reads CHECKPOINT, STATUS, tasks, calendar, journal, founder inbox
End Session                # Claude proposes summary + writes STATUS / tasks / journal / CHECKPOINT, commits, pushes
```

## Client lifecycle

```bash
# Scaffold a new client folder from the template
bash /srv/Nexostrat/infra/scripts/new-client.sh <slug> <CO|MX> '<Legal Name>' <sector> [--pilot]

# Example
bash /srv/Nexostrat/infra/scripts/new-client.sh trixx-logistics MX 'Grupo Trixx' logistica --pilot
```

After scaffolding, fill the two intake files inside `pipeline/clients/<slug>/00_intake/`:

| File | Content | Visible to |
|---|---|---|
| `research_input.md` | Facts (slices 1+2) — pasted to Skills 01–03 | Skills 01–03 |
| `our_hypotheses.md` | Judgment (slice 3) — SEALED during Skills 01–03 | Skills 04–05 only |

Then trigger the full discovery pipeline by typing this phrase in Claude Code:

```
Analiza <slug>
```

Runs Skills 01 → 02 → 03 → 04 serially, with human review between each step.

## Individual skills

| Slug | Folder | Purpose |
|---|---|---|
| `/company-analyst`   | `skills/01_company_analyst/`    | Análisis empresarial (CO/MX) |
| `/industry-analyst`  | `skills/02_industry_analyst/`   | Análisis sectorial (reusable per sector) |
| `/competitor-analyst`| `skills/03_competitor_analyst/` | Análisis competitivo (CO/MX) |
| `/discovery-meeting` | `skills/04_discovery_meeting/`  | PrepLlamada — guía pre-llamada |
| `/opportunity-report`| `skills/05_opportunity_report/` | Reporte de Oportunidades — entregable cliente (free, post-meeting) |

**Skill 05 is the FREE deliverable.** Consumes 4 prior reports + meeting transcript + notes. **Mandatory Ricardo+JP review** before delivery (Fase 5 — obligatoria).

## Memos (Founder inbox)

```bash
/srv/Nexostrat/infra/scripts/nexostrat-memos.py founder         # this persona's inbox
/srv/Nexostrat/infra/scripts/nexostrat-memos.py skills-master
/srv/Nexostrat/infra/scripts/nexostrat-memos.py client-owner
/srv/Nexostrat/infra/scripts/nexostrat-memos.py broadcast
```

Write a memo (manual until /memo Telegram plugin lands in Plan 04):

```
<target-scope>/00_META/inbox/YYYY-MM-DD_HHMM_<from>_<short-topic>.md
```

YAML frontmatter schema in `CLAUDE.md` § "Cross-Folder Memo Protocol".

## Git

```bash
git status                                         # check state
git diff                                           # uncommitted changes
git add -p                                         # stage interactively
git commit -m "concise message"
git push origin main                               # → Gitea, auto-mirrors to GitHub + Codeberg via path-watcher
git log --oneline -20                              # recent history
```

Mirror status:

```bash
systemctl status nexostrat-mirror-github
systemctl status nexostrat-mirror-codeberg
systemctl status nexostrat-mirror-github.path nexostrat-mirror-codeberg.path
sudo systemctl start nexostrat-mirror-github       # force a push out-of-cycle
sudo systemctl start nexostrat-mirror-codeberg
```

## FOSS stack — Baserow + BookStack + Caddy

```bash
# Service control
systemctl status nexostrat-foss-stack
sudo systemctl start nexostrat-foss-stack
sudo systemctl stop nexostrat-foss-stack
sudo systemctl restart nexostrat-foss-stack

# Container-level
cd /srv/Nexostrat/infra/docker/foss-stack
docker compose ps
docker compose logs --tail=50 baserow
docker compose logs --tail=50 bookstack
docker compose logs --tail=50 caddy
```

Web access (Tailscale-only — accept Caddy CA cert warning once per device):

- Baserow:   https://baserow.nexostrat.local/
- BookStack: https://docs.nexostrat.local/

## Periodic operations

**Schema drift check** (timer currently masked — run manually):

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
    /srv/Nexostrat/infra/scripts/baserow-schema-check.sh
```

Exit codes: `0` clean · `1` drift detected · `2` script error.

**Reconcile orphan deliverables → Baserow rows** (timer currently masked):

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
    /srv/Nexostrat/infra/scripts/baserow-reconcile.sh
```

**Foundation smoke test:**

```bash
/srv/Nexostrat/infra/scripts/smoke-test-foundation.sh
```

6 sub-tests; crypto + leak SKIPs are TTY-related and normal in non-interactive runs.

## Calendar cache refresh (`calendar_cache.json`)

The hub's pre-meeting brief loop (Brain Bot Platform §9, master plan Phase 5) reads `/srv/Nexostrat/calendar_cache.json` every 15 min. The cache is **human-in-the-loop**: the hub never holds Google OAuth, so a Claude session running on a PC with the Google Calendar MCP authenticated populates it.

**Source of truth:**
- Filter rule: [`00_META/calendar_filter.md`](00_META/calendar_filter.md) (Nexostrat-side audit B7 ratification)
- Filter implementation: `/home/ricardo/brain-hub/hub/google/calendar_filter_nexostrat.py::nexostrat_filter()` (constant `FILTER_VERSION = "nexostrat-v1"`)
- Cache schema is contracted in master plan §6.2 P-H2 and hub contribution doc §3 P-H2.

**Cache schema** (top-level keys):

| Field | Type | Notes |
|---|---|---|
| `generated_at` | ISO-8601 UTC | timestamp the session wrote the cache |
| `generated_by` | string | identifier of the session that wrote it (e.g. `claude@desktop`) |
| `filter_applied` | string | must equal the imported `FILTER_VERSION` — drift sentinel |
| `stale_after_hours` | int | `24` (hub renders the "⚠ cache stale" footer past this) |
| `events` | array | upstream fields `id, summary, start, end, attendees, location, description` + injected `source_calendar` + `match` rationale |

**Refresh procedure** (run any time Ricardo wants the cache < 24h fresh, ahead of Phase 5 dispatch loops, or after a non-trivial calendar change):

1. Open Claude Code on a PC where the Google Calendar MCP is authenticated to `ricardomejiacaicedo@gmail.com` (currently: desktop).
2. From `/srv/Nexostrat/`, ask:
   > Refresh `calendar_cache.json` per master plan §6.2 P-H2 — fetch next 30 days across all calendars, apply `calendar_filter_nexostrat.nexostrat_filter` with JP's email (`jpasistentepersonal@gmail.com`), write the cache.
3. Claude calls `list_calendars` + `list_events` (per calendar, `startTime=now`, `endTime=now+30d`), annotates each event with `source_calendar = <calendar summary>`, applies the filter, persists with the schema above, and commits + pushes.
4. Verify:
   ```bash
   jq -r '.filter_applied, .generated_at, .stale_after_hours, (.events | length)' /srv/Nexostrat/calendar_cache.json
   ```
   First line MUST equal the constant in `calendar_filter_nexostrat.py::FILTER_VERSION` (drift sentinel).

**Fallback (demo only, NOT production):** hand-author the cache with one synthetic event. The hub's stale-cache messaging path won't exercise. Per hub contribution doc §3 P-H2 "Defer option."

**Migration trigger:** when the firm-owned Google account (e.g. `ops@nexostrat.com`) lands, the whole-account-is-Nexostrat assumption removes the filter; `filter_applied` bumps to `nexostrat-noop-firm-account-v1` per `00_META/calendar_filter.md` § Migration trigger.

## Vault (age-encrypted secrets)

```bash
# Decrypt one-off to RAM (tmpfs — never hits disk)
age -d -i ~/.config/age/nexostrat.key.age vault/<path>.age > /dev/shm/<filename>
# ... use the plaintext ...
shred -u /dev/shm/<filename>

# Decrypt env file + run a command with those vars set (preferred — handles cleanup)
/srv/Nexostrat/infra/scripts/run-with-secrets.sh <command>
```

## Key file locations (Server PC)

| What | Path |
|---|---|
| Repo root | `/srv/Nexostrat/` |
| Skills | `/srv/Nexostrat/skills/0[1-5]_*/` |
| Client pipelines | `/srv/Nexostrat/pipeline/clients/<slug>/` |
| Scripts | `/srv/Nexostrat/infra/scripts/` |
| Docker stack | `/srv/Nexostrat/infra/docker/foss-stack/` |
| Vault | `/srv/Nexostrat/vault/` |
| Age private key | `~/.config/age/nexostrat.key.age` (passphrase-protected) |
| Plans | `/srv/Nexostrat/00_META/plans/` |
| Journal | `/srv/Nexostrat/00_META/journal/` |
| Founder inbox | `/srv/Nexostrat/00_META/inbox/` |

---

# Desktop PC

**Role for Nexostrat:** records online client meetings + produces transcripts → transfers transcripts back to the server PC for Skill 05 consumption. Does NOT host Nexostrat infra.

## One-time install (fresh Linux Mint machine)

Run top-to-bottom on the desktop PC. ~15–30 min plus model download time.

### 1. OS packages

```bash
sudo apt update
sudo apt install -y \
    obs-studio pavucontrol ffmpeg \
    build-essential cmake git \
    pulseaudio-utils
```

### 2. Build whisper.cpp at `/opt/whisper.cpp`

```bash
sudo mkdir -p /opt
cd /opt
sudo git clone https://github.com/ggerganov/whisper.cpp.git
sudo chown -R $USER:$USER /opt/whisper.cpp
cd /opt/whisper.cpp
cmake -B build
cmake --build build -j --config Release
```

Verify: `/opt/whisper.cpp/build/bin/whisper-cli --help`

### 3. Download Spanish models

```bash
cd /opt/whisper.cpp
./models/download-ggml-model.sh small        # ~466 MB, fast, ~85-90% accuracy
./models/download-ggml-model.sh large-v3     # ~3 GB, best, ~95-97% accuracy
```

### 4. Install `~/bin/transcribe.sh`

```bash
mkdir -p ~/bin
```

Then create `~/bin/transcribe.sh` with this content and `chmod +x` it:

```bash
#!/usr/bin/env bash
# transcribe.sh — extract audio from a recording, then transcribe via whisper.cpp.
# Output: <input-basename>.txt next to the input file.

set -euo pipefail

WHISPER_BIN=/opt/whisper.cpp/build/bin/whisper-cli
MODELS_DIR=/opt/whisper.cpp/models

if [[ -n "${WHISPER_MODEL:-}" ]]; then
    MODEL="$WHISPER_MODEL"
elif [[ -f "$MODELS_DIR/ggml-large-v3.bin" ]]; then
    MODEL="$MODELS_DIR/ggml-large-v3.bin"
elif [[ -f "$MODELS_DIR/ggml-medium.bin" ]]; then
    MODEL="$MODELS_DIR/ggml-medium.bin"
elif [[ -f "$MODELS_DIR/ggml-small.bin" ]]; then
    MODEL="$MODELS_DIR/ggml-small.bin"
else
    echo "error: no whisper model found in $MODELS_DIR" >&2
    exit 1
fi

if [[ $# -lt 1 ]]; then
    echo "usage: $(basename "$0") <recording-file> [language]" >&2
    exit 2
fi

INPUT="$1"; LANG="${2:-es}"
[[ -f "$INPUT" ]]      || { echo "error: file not found: $INPUT" >&2; exit 1; }
[[ -x "$WHISPER_BIN" ]] || { echo "error: whisper-cli not found at $WHISPER_BIN" >&2; exit 1; }

BASE="${INPUT%.*}"
WAV="${BASE}.tmp.wav"

echo ">> model:  $(basename "$MODEL")"
echo ">> input:  $INPUT"
echo ">> lang:   $LANG"
echo ">> extracting 16 kHz mono WAV..."
ffmpeg -hide_banner -loglevel error -y -i "$INPUT" -vn -ac 1 -ar 16000 "$WAV"

echo ">> transcribing..."
"$WHISPER_BIN" -m "$MODEL" -l "$LANG" -f "$WAV" -otxt -of "$BASE"

rm -f "$WAV"
echo ">> transcript: ${BASE}.txt"
```

Ensure `~/bin/` is on PATH (Linux Mint's `~/.profile` adds it automatically when the dir exists; new shells pick it up).

### 5. OBS one-time configuration

1. Launch `obs` → choose **"Optimize just for recording, I will not be streaming"** in the auto-config wizard.
2. **Profile → New → `audio-meeting`** (active profile name shows in title bar).
3. **Settings → Video:** Output Resolution `640×360`, FPS `10`.
4. **Settings → Output:** Mode `Simple` · Recording Path `~/Videos` · Quality `High Quality, Medium File Size` · Format `MKV` · **Encoder `Software (x264)`** (avoid NVENC unless you've installed the proprietary NVIDIA driver).
5. **Settings → Audio → Global Audio Devices:** Desktop Audio `Default` · Mic/Auxiliary Audio `Default`.

**⚠ Critical rule:** Do NOT add anything in the Sources panel. OBS captures audio via Global Audio Devices, not via Sources. Adding "Application Audio Capture" or "Audio Output Capture" sources creates PipeWire loopback nodes that hijack system audio.

### 6. Verify

In OBS main window, speak + play a YouTube video → both `Desktop Audio` and `Mic/Aux` bars should bounce in the Audio Mixer. Start Recording → 20 s test → Stop. File at `~/Videos/<timestamp>.mkv`. Run `transcribe.sh ~/Videos/<file>.mkv es`. Read the resulting `.txt`.

## Per-meeting workflow

```
1. Open OBS → confirm Profile audio-meeting is active
2. Mixer test: speak + play any audio, both bars bounce
3. Start Recording
4. Hold meeting (audio in/out works normally — recording is transparent)
5. Stop Recording → file at ~/Videos/<timestamp>.mkv
6. transcribe.sh ~/Videos/<file>.mkv              # produces <file>.txt
7. Transfer .txt + .mkv to the server PC for Skill 05 input
```

## Transfer to server PC

Server PC is at Tailscale `100.64.121.80`. Easiest is scp into the right station folder:

```bash
# From desktop PC, to server PC's client station
scp ~/Videos/2026-MM-DD\ HH-MM-SS.{mkv,txt} \
    ricardo@100.64.121.80:/srv/Nexostrat/pipeline/clients/<slug>/transcripts/
```

Or use Telegram self-send / Drive / USB depending on file size.

Naming convention on the server PC: `pipeline/clients/<slug>/transcripts/YYYY-MM-DD_<short-topic>.{mkv,txt}`.

## In-person meetings

OBS does not apply. Use a phone voice recorder, get explicit consent (*"¿Les molesta si grabo solo el audio?"*), then transfer the audio file to either PC for transcription via `transcribe.sh`.

---

# Other PCs

(Placeholder — add a new section when Nexostrat starts being touched from another machine, e.g., JP's `jp-mac` if he flips to Heavy mode per ADR-021bis.)

---

# Model selection (Whisper.cpp)

Applies anywhere `transcribe.sh` runs.

| Model | Size | Spanish accuracy | Speed (laptop CPU) | When to use |
|---|---|---|---|---|
| `tiny` | 75 MB | ~70% | ~10× real-time | Never — too inaccurate |
| `base` | 142 MB | ~78% | ~7× real-time | Quick rough-cut only |
| `small` | 466 MB | ~85-90% | ~3× real-time | Non-critical recordings |
| `medium` | 1.5 GB | ~92-95% | ~1× real-time | Specialist terms (TIGIE, Carta Porte) |
| `large-v3` | 3 GB | ~95-97% | ~0.5× real-time | Client meetings, final transcripts |

`transcribe.sh` auto-prefers `large-v3` if downloaded. Desktop PC will run `large-v3` faster than the server PC because more horsepower.

---

# Appendix — Flat command list (server PC)

```
# Session lifecycle
Start Session
End Session

# Client lifecycle
bash infra/scripts/new-client.sh <slug> <CO|MX> '<Name>' <sector> [--pilot]
Analiza <slug>

# Individual skills
/company-analyst
/industry-analyst
/competitor-analyst
/discovery-meeting
/opportunity-report

# Memos
infra/scripts/nexostrat-memos.py founder
infra/scripts/nexostrat-memos.py skills-master
infra/scripts/nexostrat-memos.py client-owner

# Git
git status / git diff / git add -p / git commit -m '...' / git push origin main
systemctl status nexostrat-mirror-github
systemctl status nexostrat-mirror-codeberg

# FOSS stack
systemctl status nexostrat-foss-stack
docker compose -f infra/docker/foss-stack/docker-compose.yml ps

# Periodic
infra/scripts/run-with-secrets.sh infra/scripts/baserow-schema-check.sh
infra/scripts/run-with-secrets.sh infra/scripts/baserow-reconcile.sh
infra/scripts/smoke-test-foundation.sh

# Secrets
age -d -i ~/.config/age/nexostrat.key.age <file>.age
infra/scripts/run-with-secrets.sh <command>
```
