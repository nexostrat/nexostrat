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
