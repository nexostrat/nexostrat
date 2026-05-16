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
