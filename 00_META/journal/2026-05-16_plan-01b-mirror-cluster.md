# 2026-05-16 — Plan 01b mirror cluster (Tasks 1-6) executed end-to-end

> **Topic:** Plan 01b mirror cluster · 8 commits · v0.1b-mirrors-only tagged · C4 + F7 closed
> **Persona:** Founder
> **Session length:** ~3h
> **Method:** `superpowers:subagent-driven-development`
> **Outcome:** Mirror cluster live + validated end-to-end; tag `v0.1b-mirrors-only` on `d38e865`

## The arc

This session executed Tasks 1-6 of Plan 01b (the mirror cluster) via the subagent-driven-development pattern proven during Plan 01a Tasks 1-11 (2026-05-15) and Tasks 12-18 (2026-05-16 morning). Eight commits landed between `beff92a..d38e865`. Audit findings **C4 + F7 are fully closed end-to-end**. The warm-standby cluster (Tasks 7-12) remains gated on a physical second host and is now tracked separately in `t-plan-01b-execute-warm-standby` (created this session).

The session opened with a pre-flight check that revealed two issues the locked plan did not anticipate:
1. The GitHub firm repo did not exist yet (terrain-prep "verified" the friendly-greeting auth, but the destination repo had never been created).
2. `ssh -T git@github.com` (bare domain) authenticated as `ricardomejiacaicedo-del` — Ricardo's personal account, not `nexostrat`. The two AskUserQuestion turns at session start chose to push to the personal namespace (`Push to personal namespace`) and generate PATs now (`Generate PATs now`).

That asymmetric-topology decision was reversed two commits later (`4dd9301`) after the code-quality reviewer flagged that the SSH config has explicit `*-nexostrat` aliases (`github-nexostrat`, `codeberg-nexostrat`, `gitea-nexostrat`) and `ssh -T git@github-nexostrat` returns `Hi nexostrat!`. The firm key IS registered on the firm GitHub user. The earlier pre-flight had probed using the bare domain (which falls back to Ricardo's default identity). Both mirrors now live at firm namespace `nexostrat/nexostrat`.

## The 8 commits (in order)

| # | Commit | Substance |
|---|---|---|
| 1 | `615372a` | **Task 1 original** — `00_GOVERNANCE/system_map.md` (single source of truth) + `00_GOVERNANCE/incidents/.gitkeep` scaffold + Gitea bare-repo path verified (`/srv/gitea/data/git/repositories/nexostrat/nexostrat.git`, owner `ricardo:ricardo` host-side). |
| 2 | `314ada6` | **Task 1 fixup-1** — code-quality review found controller-template factual errors. Patched: gitea image (`1.22` → `latest`, running 1.25.5), port binding (`Tailscale 100.64.121.80` → `0.0.0.0`), SSH aliases (real names `gitea-nexostrat`/`github-nexostrat`/`codeberg-nexostrat`), rsync source (`hp-server` → Tailscale IP). Added two hygiene-gap callouts (image-pinning + network-binding) for Plan 02 follow-up. |
| 3 | `4dd9301` | **Task 1 fixup-2** — reversed the asymmetric-topology decision. Mirrors table now uses firm-namespace `git@github-nexostrat:nexostrat/nexostrat.git`. Identity caveat added warning against bare-domain SSH for firm git ops. |
| 4 | `f1fc501` | **Tasks 2+3 bundle** — both mirror remotes added with alias URLs; both PATs (GITHUB_MIRROR_PAT + CODEBERG_MIRROR_PAT) injected into `secrets.env.age` in a single atomic age decrypt-encrypt cycle (one TTY prompt, one plaintext-in-RAM moment — better hygiene than the plan's two-task two-cycle split); MANIFEST.md rotation dates filled. Closes F7 (Codeberg mirror missing from original Plan 01). |
| 5 | `d9cdf3a` | **Tasks 4+5 artifacts** — `mirror-push.sh` (DRY: one script, remote-name arg) + `install-systemd-units.sh` (idempotent symlink installer, self-elevates to sudo) + 4 systemd unit files (`.path` + `.service` per mirror, with hardening: `ProtectSystem=strict`, `ReadWritePaths=/srv/Nexostrat`, `ProtectHome=read-only`, `BindReadOnlyPaths=/home/ricardo/.ssh`, `Environment=SSH_AUTH_SOCK=`). system_map.md Systemd-units table populated. |
| 6 | `260dc75` | **Tasks 4+5 pre-install patch** — code-quality review found 3 Important issues. Patched: phantom `After=gitea.service` removed (gitea runs as Docker container, not a systemd unit, AND the mirror service doesn't depend on gitea being up — it pushes from local working tree to GitHub/Codeberg); `systemctl enable` error suppression replaced with `systemd-analyze verify` gate + propagated errors (avoids silent broken-unit ship); cross-cutting note corrected to reflect SSH-only design (not `run-with-secrets.sh`-mediated). |
| 7 | `d04191d` | **Test sentinel** — trivial `infra/systemd/.last-mirror-test` write to provoke the path-watcher. |
| 8 | `d38e865` | **Tasks 4+5+6 post-validation** — Mirrors table populated with measured 60-second window: **GitHub 3 s, Codeberg 8 s** (both well inside the 60 s success criterion). Validation commit + post-validation update commit. |

## End-to-end validation — recursive proof

After the post-validation commit was pushed, the harness tried to do a redundant `git push github main` to keep the manual record consistent. GitHub rejected: `cannot lock ref 'refs/heads/main': is at d38e865 but expected d04191d`. The mirror service had ALREADY pushed `d38e865` to GitHub before the explicit redundant push could land. That race-loss is recursive proof: the wire-up works in production, end-to-end, including for its own validation commit.

All four SHAs converged at `d38e865`: local HEAD, origin/main, github/main, codeberg/main.

## Decisions locked this session

1. **GitHub firm-namespace topology.** Reversed the 2026-05-16 "asymmetric" detour. Both mirrors live at `nexostrat/nexostrat`. The empty repo created earlier at `ricardomejiacaicedo-del/nexostrat` was deleted (Ricardo, via `gh repo delete` after refresh-with-`delete_repo`-scope).

2. **Mirror authentication is SSH-only at Stage 1.** PATs are stored in `secrets.env.age` for a future HTTPS-fallback path (Plan 02+), but the mirror services never read them at runtime. The cross-cutting note in `system_map.md` was corrected to reflect this; `mirror-push.sh` comments are consistent.

3. **`After=gitea.service` is incorrect.** The mirror service pushes from the local working tree TO remote git providers — it does not depend on Gitea being up. Removed from both `.service` files. `network-online.target` is the only real boot-time dependency.

4. **`systemctl enable` errors must not be suppressed.** The old `|| { echo WARN; continue; }` pattern collapsed real failures (typo in `[Install]`, missing `WantedBy`) into the same "probably already enabled" message. Replaced with `systemd-analyze verify` as a parse gate + propagated errors from `systemctl enable`.

5. **Bundling decisions for atomic operations.** Tasks 2+3 (single age decrypt-encrypt cycle for both PATs) and Tasks 4+5 (structurally identical units) were bundled into one commit each. Tasks 4+5+6 closed with one post-validation commit covering both the wire-up and the 60s window measurement. Plan-as-written had these as separate commits; bundling matched operational rhythm better.

6. **Interim tag `v0.1b-mirrors-only`.** Full `v0.1b-mirrors` reserved for warm-standby completion. The interim tag is annotated, lists what's in/not-in, references the audit closures, and points to the new `t-plan-01b-execute-warm-standby` task.

7. **Plan 01c re-audit unblocked.** Per Ricardo's session-end call: warm-standby learnings are unlikely to affect Plan 01c's persona/hooks design, so no need to wait. `blocked_by` removed from `t-plan-01c-reaudit`.

## Cross-cutting drift caught by reviewers

- **Three controller-template factual errors** (Task 1 fixup-1) — I gave the implementer a template with wrong gitea version / wrong port binding / wrong SSH alias names. The implementer faithfully copied. Code-quality reviewer caught it. Fix landed same task.

- **Asymmetric-topology decision** based on misread of `ssh -T` output (Task 1 fixup-2) — the pre-flight used the bare domain (`git@github.com`) which falls back to the default identity. Code-quality reviewer caught the inconsistency between Codeberg (alias auth → `Hi nexostrat!`) and GitHub (bare auth → `Hi ricardomejiacaicedo-del!`). Verified the firm key DOES auth as `nexostrat` via the alias, then reversed the decision.

- **Three design issues** (Tasks 4+5 pre-install patch) — phantom dependency, error suppression, doc drift. All caught by code-quality review BEFORE the sudo install ran, so the live system was never misconfigured.

## TTY-deferred items (carried forward)

The mirror cluster is fully operational, but two TTY-required items remain deferred:

- **Item (8) in `t-plan-01a-jp-and-tty-deferred`** — `run-with-secrets.sh sh -c 'echo "GITHUB len: ${#GITHUB_MIRROR_PAT}; CODEBERG len: ${#CODEBERG_MIRROR_PAT}"'`. Not blocking the mirror today (services are SSH-only); becomes a gate if Plan 02+ wires an HTTPS-fallback path. Added to the deferred-task notes this session.

- **JP-side roundtrip from Plan 01a** (items 1-4, 6-7 of `t-plan-01a-jp-and-tty-deferred`) — unchanged, JP coordination on his own schedule per `defer-jp-until-test-phase` memory.

## Hygiene gaps logged for post-Plan-01c polish

(all VERY LOW severity per the final cross-cutting reviewer)

- `infra/systemd/.last-mirror-test` is tracked in git; should be `.gitignore`'d (sentinel role belongs in `system_map.md` and journal, not as a volatile-but-tracked file).
- Plan 01b plan text has 3 stale design items vs. implementation (PAT auth claim, `After=gitea.service`, suppressed-enable pattern). Audit-trail artifact; accept divergence.
- MANIFEST.md row-style asymmetry between GitHub (has `ghp_…` token-format hint) and Codeberg (no hint) rows. Cosmetic.
- `mirror-push.sh` `cd` safety-net comment, orphan-symlink cleanup in installer, system_map.md "invoked by .path" precision. All pure polish.

## Session metrics

- **Wall-time:** ~3 hours (matches the Plan 01a Tasks 1-11 shape; faster per-task than Plan 01a's 6h because Plan 01b is smaller scope)
- **Commits:** 8 + bookkeeping = 9
- **Subagent dispatches:** 5 (Task 1 implementer + spec + 2 code-quality reviewers / Tasks 2+3 implementer + spec + code-quality / Tasks 4+5 artifact implementer + spec + code-quality / final cross-cutting reviewer)
- **Reviewer findings closed mid-arc:** 3 Critical (Task 1 facts) + 3 Important (Tasks 4+5 design issues) + 1 Important (Tasks 2+3 tracking gap, fixed in `tasks.json`)
- **TTY-blocked steps handled out-of-band by Ricardo:** age decrypt-encrypt cycle for PATs (single one-shot script written to /dev/shm, self-shredding) + sudo install of systemd units. Both worked first-try.

## What's next (next session opens at)

**Default next-session work: Plan 01c re-audit.** Unblocked this session. Same audit pattern as the 4 priors (5th audit at this discipline). Plan 01c is `00_META/plans/2026-05-14_plan-01c-personas.md` (11 tasks, ~2050 lines). Dispatch `general-purpose` Opus agent with risk-auditor persona inlined.

**Parallel non-blocking:**
- `t-plan-01b-execute-warm-standby` — when physical second host (Linux Mint 22.2 + Tailscale-joined) is available. Tasks 7-12 of Plan 01b. ~2-3h. Tag `v0.1b-mirrors` on completion.
- `t-presentation-refresh-post-adr-038` — due 2026-06-01. Full regeneration from current spec.
- `t-plan-01a-jp-and-tty-deferred` items 1-4 + 6-8 — JP coordination on his own schedule.

---

*Session journal compiled at session end. Tag `v0.1b-mirrors-only` lives on `d38e865`. Bookkeeping commit lands after this journal entry.*
