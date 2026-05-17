## Backup Posture

Per spec §1 + §3 (post-Plan-01b state):

```
HP working tree (live)
  ▼
Gitea origin (HP, Tailscale only)
  ▼ systemd .path-watcher (Plan 01b)
GitHub mirror (off-site, private)
  ▼ same .path-watcher pattern
Codeberg mirror (off-site, private, second-site)
  ▼ nightly rsync 03:00 America/Tijuana (Plan 01b)
Warm-standby clone (idle until failover; RTO 15-30 min)
  ▼
Drive 2TB (heavy assets only, age-encrypted before upload)
```

**Recovery RTO targets:**
- Single-machine failure: 15-30 min via warm-standby (`docs/runbooks/hp_down.md`).
- Single off-site loss (GitHub OR Codeberg): irrelevant; the other survives.
- Total HP loss + warm-standby unreachable: ~2-4 hours via off-site mirror restore + crypto recovery.

**Verification cadence:** integration smoke test (Plan 01c) does real decrypt round-trip + real `git push` + verify GitHub HEAD changed + warm-rsync trigger. Periodic verification per a yet-undefined schedule (Plan 10 territory).
