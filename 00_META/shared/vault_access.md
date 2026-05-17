## Vault / Sensitive Discipline

Per ADR-003 + ADR-004 + F10:

| Subfolder | Owner |
|---|---|
| `vault/partnership/` | Founder |
| `vault/legal/`, `vault/accounting/`, `vault/keys/` | Founder |
| `vault/clients/<slug>/` | Client-Owner |

Skills-Master owns no vault content.

**Discipline:**
- NEVER commit plaintext secrets to git. The `.gitignore` blocks `*.env`, `*.key`, `*secrets*`, `*.pem`. The pre-commit hook (`infra/hooks/pre-commit-secret-scan.sh`) catches secret prefixes.
- Decrypt to `/dev/shm` (RAM tmpfs) at use time → use → shred. No persistent mounted plaintext.
- Heavy assets (audio, large PDFs) age-encrypted before Drive upload; index in `vault/sensitive_index.md`.
- Secrets loaded into services via `infra/scripts/run-with-secrets.sh` (per CRITICAL 1 fix: explicit cleanup, no `exec` leak).
- The `vault/` folder accepts only `.age` files; `infra/hooks/pre-commit-vault-age-only.sh` enforces.

**Recovery scenarios:** see `docs/runbooks/key_compromise.md` (Plan 02) and `docs/runbooks/total_outage.md` (Plan 10). Short version: each holder's encrypted private key is backed up in their cloud password vault (Bitwarden); recipients file (`infra/age-recipients.txt`) is the canonical "who can decrypt" list.
