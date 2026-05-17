#!/usr/bin/env bash
# smoke-test.sh — Nexostrat (R2)
#
# End-to-end integration smoke test for the foundation milestone.
# Runs 6 sub-tests; each prints a clear PASS/FAIL line. Exit 0 only if all green.

set -uo pipefail

REPO="/srv/Nexostrat"
PASS=0; FAIL=0
echo "============================================================"
echo "Nexostrat smoke test  ($(date -Iseconds))"
echo "============================================================"

ok()  { echo "  PASS  $1"; PASS=$((PASS+1)); }
no()  { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

# ---- 1. Crypto round-trip -------------------------------------------------
# Both decrypt invocations use `age -d -i <encrypted-identity>` which prompts
# for the passphrase on /dev/tty. Under TTY-less execution (subagent-driven,
# CI, scripted runs) age fails with "could not read passphrase". TTY-gate the
# whole sub-test and surface a SKIP rather than two FAILs. Companion task:
# t-plan-01a-jp-and-tty-deferred tracks the interactive rerun.
echo
echo "[1/6] Decrypt round-trip on secrets.env.age"
if [ ! -t 0 ] || [ ! -t 1 ]; then
  echo "  SKIP  no TTY; crypto round-trip needs interactive passphrase entry"
  echo "        (run via t-plan-01a-jp-and-tty-deferred TTY-side rerun)"
else
  TMP=/dev/shm/smoke-test-secrets-$$
  if age -d -i "$HOME/.config/age/nexostrat.key.age" \
          "$REPO/secrets.env.age" > "$TMP" 2>/dev/null \
     && grep -q 'ANTHROPIC_API_KEY' "$TMP"; then
    ok "secrets.env.age decrypts and contains expected key"
  else
    no "secrets.env.age decrypt failed"
  fi
  shred -u "$TMP" 2>/dev/null || rm -f "$TMP"

  # Re-encrypt round-trip to confirm both recipients still work
  TMP_PT=/dev/shm/smoke-pt-$$.txt
  TMP_CT=/dev/shm/smoke-ct-$$.age
  TMP_DEC=/dev/shm/smoke-dec-$$.txt
  echo "smoke-test $(date -Iseconds)" > "$TMP_PT"
  if age -R "$REPO/infra/age-recipients.txt" -o "$TMP_CT" "$TMP_PT" \
     && age -d -i "$HOME/.config/age/nexostrat.key.age" "$TMP_CT" > "$TMP_DEC" \
     && diff -q "$TMP_PT" "$TMP_DEC" >/dev/null; then
    ok "encrypt-to-recipients + decrypt-with-Ricardo-key round-trip"
  else
    no "round-trip failed"
  fi
  shred -u "$TMP_PT" "$TMP_CT" "$TMP_DEC" 2>/dev/null || rm -f "$TMP_PT" "$TMP_CT" "$TMP_DEC"
fi

# ---- 2. Mirror HEAD parity (no-commit; uses current state) ---------------
# Earlier draft pushed a smoke-test commit to verify convergence; that
# (a) polluted main history with a permanent smoke-test <ts> commit per
# run, and (b) silently false-positived when the pre-commit hook refused
# the commit (HEAD unchanged → convergence loop trivially succeeded).
# Plan 01b already proved end-to-end convergence (3 s GitHub / 8 s
# Codeberg at d38e865). This sub-test just asserts the mirrors are at
# current HEAD — if the path-watchers fell behind, this catches it
# without mutating main.
echo
echo "[2/6] GitHub + Codeberg mirror HEAD parity"
cd "$REPO"
LOCAL=$(git rev-parse HEAD)
GH=$(git ls-remote github main 2>/dev/null | awk '{print $1}')
CB=$(git ls-remote codeberg main 2>/dev/null | awk '{print $1}')
if [[ "$GH" == "$LOCAL" && "$CB" == "$LOCAL" ]]; then
  ok "GitHub + Codeberg at HEAD ($LOCAL) without intervention"
else
  no "mirror not in sync: GH=$GH CB=$CB local=$LOCAL"
fi

# ---- 3. Warm-rsync real-trigger ------------------------------------------
# Plan 01b Tasks 7-12 (warm-standby cluster, including this unit) were
# DEFERRED 2026-05-16; tag landed v0.1b-mirrors-only. The warm-rsync
# unit doesn't exist until t-plan-01b-execute-warm-standby completes
# (gated on physical second host; due 2026-06-30). Gate this sub-test
# on unit presence and SKIP-not-FAIL when absent — v0.1-foundation can
# tag at 5-PASS + 1-SKIP. The SKIP becomes PASS once the warm-standby
# cluster lands.
echo
echo "[3/6] warm-rsync real trigger"
if ! systemctl cat nexostrat-warm-rsync.service >/dev/null 2>&1; then
  echo "  SKIP  nexostrat-warm-rsync.service not installed"
  echo "        (Plan 01b Tasks 7-12 deferred to t-plan-01b-execute-warm-standby;"
  echo "         gates on physical second host; due 2026-06-30)"
else
  sudo systemctl start nexostrat-warm-rsync.service 2>/dev/null
  sleep 5
  RES=$(sudo systemctl show nexostrat-warm-rsync.service --property=Result --value 2>/dev/null)
  RC=$(sudo systemctl show nexostrat-warm-rsync.service --property=ExecMainStatus --value 2>/dev/null)
  if [[ "$RES" == "success" && "$RC" == "0" ]]; then
    ok "warm-rsync.service Result=success ExecMainStatus=0"
  else
    no "warm-rsync.service Result=$RES ExecMainStatus=$RC"
  fi
fi

# ---- 4. run-with-secrets.sh leak check -----------------------------------
# The wrapper calls `age -d -i $PRIV_KEY_AGE` which prompts on /dev/tty.
# Under TTY-less execution (subagent-driven-development, scripted runs)
# the wrapper hangs at the prompt and never decrypts — INTRA stays 0,
# POST stays 0, the test silently false-positives. TTY-gate the check
# and assert INTRA>0 before declaring PASS so the leak path is actually
# exercised. Companion item tracked in t-plan-01a-jp-and-tty-deferred.
echo
echo "[4/6] run-with-secrets.sh /dev/shm leak check"
if [ ! -t 0 ] || [ ! -t 1 ]; then
  echo "  SKIP  no TTY; leak check requires interactive passphrase entry"
  echo "        (run via t-plan-01a-jp-and-tty-deferred TTY-side rerun)"
else
  "$REPO/infra/scripts/run-with-secrets.sh" sh -c 'sleep 60' &
  WPID=$!
  sleep 5
  INTRA=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | wc -l)
  kill $WPID 2>/dev/null
  pkill -P $WPID 2>/dev/null
  sleep 1
  POST=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | wc -l)
  if [[ $INTRA -eq 0 ]]; then
    no "wrapper never decrypted — INTRA=0 (passphrase not entered or wrapper broken)"
  elif [[ $POST -eq 0 ]]; then
    ok "no /dev/shm leak after wrapper exit (intra-run had $INTRA as expected)"
  else
    no "leftover plaintext in /dev/shm: $POST file(s)"
    rm -f /dev/shm/nexostrat-secrets-*
  fi
fi

# ---- 5. Inliner drift across all 6 persona files -------------------------
echo
echo "[5/6] inline_includes.py drift check across 6 persona files"
DRIFT=0
for pair in \
  "00_META/templates/CLAUDE.md.tmpl  CLAUDE.md" \
  "00_META/templates/GEMINI.md.tmpl  GEMINI.md" \
  "00_META/templates/skills_CLAUDE.md.tmpl  skills/CLAUDE.md" \
  "00_META/templates/skills_GEMINI.md.tmpl  skills/GEMINI.md" \
  "00_META/templates/pipeline_CLAUDE.md.tmpl  pipeline/CLAUDE.md" \
  "00_META/templates/pipeline_GEMINI.md.tmpl  pipeline/GEMINI.md"
do
  read -r tmpl out <<<"$pair"
  if ! python3 "$REPO/infra/scripts/inline_includes.py" \
        --template "$REPO/$tmpl" --check "$REPO/$out" >/dev/null 2>&1; then
    DRIFT=$((DRIFT+1))
    echo "    DRIFT: $out vs $tmpl"
  fi
done
if [[ $DRIFT -eq 0 ]]; then
  ok "all 6 persona files in sync with templates"
else
  no "$DRIFT persona file(s) drifted"
fi

# ---- 6. JSON schema validation -------------------------------------------
echo
echo "[6/6] tasks.json + calendar.json schema validation"
if bash "$REPO/infra/scripts/validate_schemas.sh" >/dev/null 2>&1; then
  ok "both files validate against their schemas"
else
  no "schema validation failed"
fi

# ---- Summary --------------------------------------------------------------
echo
echo "============================================================"
echo "  Result: $PASS pass, $FAIL fail"
echo "============================================================"
[[ $FAIL -eq 0 ]] || exit 1
