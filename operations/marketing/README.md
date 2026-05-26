# Marketing Assets

Working folder for Nexostrat's marketing and brand-image production. Everything here is **gitignored** except this README — the assets are heavy, regenerable, and have no merge value. Backups go to Drive 2TB per the backup posture (see root CLAUDE.md § Backup Posture).

## Structure

```
operations/marketing/
├── README.md                  # this file (tracked)
├── .gitignore                 # ignores everything except README
│
├── brand/                     # long-lived brand identity (outlives campaigns)
│   └── logos/                 # PNG/SVG variants — fondo, transparente, mono, iconos
│
└── <campaign-slug>/           # one folder per campaign / deliverable
    ├── raw/                   # source footage / source images, unedited
    ├── edits/                 # editing project files (.kdenlive, .blend, .psd, .fcp)
    └── final/                 # exported deliverables ready to ship
```

## Conventions

- **One subfolder per campaign or deliverable.** Examples: `website-intro/`, `linkedin-launch-2026q3/`, `pitch-deck-investors/`.
- **`raw/ → edits/ → final/`** is the production pipeline inside each campaign. Source → working files → exports.
- **Filename pattern for dated takes:** `YYYY-MM-DD_<short-slug>_take-NN.<ext>` — sorts chronologically, capture order preserved.
- **Brand assets go in `brand/`**, not in any campaign — they're shared.
- **No client-facing assets here.** Client deliverables live under `pipeline/clients/<slug>/` per the pipeline convention.

## Video pipeline — DaVinci Resolve on Linux

**Problem:** Modern phones (Pixel, iPhone) record video in HEVC (H.265), often 10-bit HDR. DaVinci Resolve **Free** on Linux **cannot decode HEVC** — the timeline shows a green/blank track with audio only. This is a Studio-only codec on Linux; not a config bug.

**Fix:** Transcode raw camera files to **DNxHR HQ in a MOV container** before importing. DNxHR is DaVinci's preferred editing codec — visually lossless, intra-frame (frame-accurate scrubbing), and supported by the free Linux build.

**Convention:** keep originals in `raw/` (untouched archive), put transcoded edit-ready files in `raw/transcoded/`.

**Command** (one-shot for a single file):

```bash
ffmpeg -i raw/INPUT.mp4 \
    -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p \
    -c:a pcm_s16le -map_metadata 0 \
    raw/transcoded/INPUT.mov
```

**Command** (batch, all `.mp4` in `raw/` → `raw/transcoded/`, run from inside the campaign folder):

```bash
mkdir -p raw/transcoded
for f in raw/*.mp4; do
    base=$(basename "$f" .mp4)
    ffmpeg -hide_banner -loglevel warning -stats -i "$f" \
        -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p \
        -c:a pcm_s16le -map_metadata 0 \
        "raw/transcoded/${base}.mov"
done
```

**Expected output size:** DNxHR HQ runs ~700–900 Mbps at 3.6K — roughly 3 GB per minute. Source HEVC at 30 Mbps is ~10× smaller. Plan disk accordingly; gitignored anyway.

**If DNxHR HQ is too heavy** for very long clips, fall back to DNxHR SQ (`-profile:v dnxhr_sq`, ~half the bitrate, still edit-grade) or DNxHR LB (proxy-grade, ~quarter).

## Current campaigns

| Slug | Status | Notes |
|---|---|---|
| `website-intro/` | raw footage staged 2026-05-22 | 3 takes from 2026-05-21 phone capture; editing TBD |

## Heavy-asset discipline

If an asset is irreplaceable (one-shot interview, original footage that was deleted from source) and large, age-encrypt and upload to Drive following the heavy-assets pattern in CLAUDE.md § Vault / Sensitive Discipline. Index in `vault/sensitive_index.md`. Day-to-day working files (re-renderable, regenerable) don't need this — losing them costs time, not data.
