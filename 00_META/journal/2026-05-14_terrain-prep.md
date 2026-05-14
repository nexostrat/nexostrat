# 2026-05-14 — Terrain prep before Batch 1

## Session shape

Started intending to execute Batch 1 spec amendments per the amendment plan. Pivoted within the first turn after Ricardo flagged: "Git commit is not working since contacto@nexostrat.com does not even have a git account. What lay work do we need to do before even starting the bases?"

That single observation surfaced a much wider set of latent prerequisites — git identity that maps to no actual account, no git remotes, no age key, no JP coordination kicked off, no SSH config, etc. The session became a deliberate "clean the terrain" pass before pouring foundation. Batch 1 deferred to next session.

## Architectural directives that emerged mid-session

These are now durable in memory + reflected in the rewrites:

1. **No `/srv/brain` references inside Nexostrat anywhere.** Ricardo's exact phrasing: "Nexostrat is a completely different entity than the brain. The brain should not even be mentioned in documentation or anywhere inside Nexostrat. They are two different entities with different objective." This drove (a) the choice to let Nexostrat fall out of the Brain SessionStart hook's brain-wide scan rather than patch the hook, (b) the late-session decision to do a full Nexostrat-native rewrite of CLAUDE.md/GEMINI.md/README.md instead of deferring to Plan 01c, (c) saving as feedback memory.
2. **No n8n.** Drop entirely from spec/plans/code; Python + systemd timers are the orchestration substrate (already in ADR-029, but Ricardo extended to "even peripheral mentions die"). F22 path verification becomes moot — n8n just disappears from the architecture.
3. **Notion via JP personal subscription** for Stage 1. Firm cost = $0. Reverses the F14 amendment direction (was about to add $10-30/mo to Stage 1 envelope; now stays at original $36-91/mo). Consistent with the existing cost-share agreement.

## What we built

Phase 0 (hygiene): landed prior session's uncommitted audit + walkthrough work as a single prelim commit, then added `.gitignore` (interim secret/key patterns) + `.gitattributes` (line endings + binary detection).

Phase 1 (identity + accounts): contacto@nexostrat.com mailbox provisioned at Hostinger, then `nexostrat`-username accounts created on GitHub, Codeberg, Gitea (org); Notion workspace created but cost absorbed by JP. SSH keypair `~/.ssh/nexostrat_ed25519` (no passphrase — disk encryption + daily-use friction tradeoff) registered on all 3 platforms. `~/.ssh/config` Host aliases set up so day-to-day clone URLs stay clean despite Gitea SSH on `:2222`. Verified all 3 platforms with `ssh -T` returning friendly auth greetings. Git remote `origin` added pointing at Gitea; pushed all 8 accumulated commits.

Phase 2 (crypto): age keypair generation hit a snag because `age -p` requires a real TTY and Claude Code's `!` prefix doesn't allocate one. Solved by Ricardo running the encrypt step in a separate terminal. Public key extracted BEFORE encryption (caught the "shred-then-extract" ordering bug in my first draft of the recipe; revised JP message accordingly). Backed up encrypted key + passphrase + sha256 to Bitwarden; Ricardo verified recovery roundtrip. `infra/age-recipients.txt` committed with Ricardo's pubkey + JP placeholder + comprehensive instructions.

Phase 3 (JP coordination): drafted Spanish Signal message bundling 6 asks (age pubkey with full age-keygen recipe, OS choice with Linux Mint recommendation, Telegram chat_id, Gitea username, Notion invite to JP's workspace, GitHub username decision). Ricardo sent via Signal. Drip-feed replies expected over next few days given JP's 10h/wk bandwidth.

Late-session pivot: Ricardo flagged that the inherited CLAUDE.md/GEMINI.md were heavily Brain-coupled and would influence every future session. Did substantial rewrites of CLAUDE.md, GEMINI.md, and README.md — stripped all `/srv/brain` references, inlined previously-pointered protocols (memo template paths, session output format, gemini handoff full spec, vault access policy, backup posture), updated brand from "Mejía IA & Cía" to Nexostrat throughout, reflected Ricardo + JP partnership, replaced "Cross-Folder Memo Protocol" with `events.jsonl` pointer (per ADR-013 + Plan 03), added explicit no-Brain + no-n8n + bilingual rules. Plan 01c can still do the canonical-shared-stanza restructure on top of Nexostrat-native files instead of Brain-coupled ones — cleaner starting point.

Also pre-empted Batch 1's planned `events.json → calendar.json` rename: did the `git mv` + updated `$schema` (`brain-events-v1` → `nexostrat-calendar-v1`) and `project` (`01_VENTURES/04_MejiaIACia` → `nexostrat`) fields. Same for `tasks.json` `$schema` (`brain-tasks-v1` → `nexostrat-tasks-v1`). Removes a residual Brain-reference in JSON-config land.

## Surface-area discoveries

- **Gitea port mismatch.** Spec says `:3000`; actual host port is `:3001` (the Docker container's internal `:3000` is published on host's `:3001`). This bit Ricardo's first login attempt. To fold into Batch 1 spec edit (single-line correction in §1).
- **Plaintext recipe ordering bug.** The age-keygen flow needs pubkey extracted BEFORE encrypt-and-shred. My first draft of the recipe shredded the plaintext before extracting pubkey, which would leave JP unable to share his pubkey. Caught it before sending; revised the JP Signal message.
- **`age -p` TTY requirement.** The `!` prefix in Claude Code is non-TTY; `age -p` insists on `/dev/tty` for passphrase input. Ricardo had to open a separate terminal for the encryption step. Worth remembering — same pattern will apply to other interactive secret-prompts (gpg, openssl rsa, etc.).
- **Existing local SSH key collision risk.** Ricardo's personal `~/.ssh/id_ed25519` is registered on his personal `ricardomejiacaicedo-del` GitHub. Used a separate key file (`nexostrat_ed25519`) for the firm to avoid the "key already in use on another account" rejection.

## What's queued for next session (Batch 1)

Batch 1 is now the next session's whole agenda. Three commits total:

1. Spec single-pass edit covering 14 amendments + 3 new ADR map rows + Brain-reference strip + n8n delete + port :3001 + F14 cost revert.
2. (Rename commit collapsed — already done in terrain prep.)
3. Master plan index update with Plan 01 → 01a/b/c entries + new realistic dates + mark old Plan 01 SUPERSEDED.

Time estimate: ~2-2.5h. No blockers — JP coordination is in flight but doesn't gate Batch 1 (it gates Batch 3 execution, weeks out).

## Memory

Saved to `/home/ricardo/.claude/projects/-srv-Nexostrat/memory/`:

- `user_role.md` — Ricardo profile (architect-operator, 50/50 with JP, direct communicator, deeply technical)
- `feedback_no_brain_references.md` — never reference `/srv/brain` from inside Nexostrat
- `feedback_drop_n8n_entirely.md` — Python + systemd; F22 by deletion not verification
- `project_notion_via_jp.md` — Stage 1 firm Notion cost = $0; F14 reverses

Indexed in `MEMORY.md`.

## Final state

Working tree clean after the final commit batch. `main` at `<commit-hash>` (filled in after commit). Next session: type "Start Session" → CHECKPOINT.md baton tells you exactly what Batch 1 looks like with all the terrain-prep corrections folded in.
