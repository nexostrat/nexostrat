#!/usr/bin/env bash
# bootstrap-machine.sh — Nexostrat
#
# Reads infra/machines/<profile>.yaml and prepares the host accordingly.
# Plan 01a SCOPE: skeleton only — parses profile, logs intended actions,
# exits without performing them. Idempotent. Re-runnable.
#
# Full installer logic (apt install lists, docker setup, systemd unit
# enablement, Tailscale auth) lands in Plan 02 via the per-section work
# (apt task, docker task, systemd task).
#
# Usage: infra/scripts/bootstrap-machine.sh <profile>
#   profile = name of a file under infra/machines/ (without .yaml suffix)
#
# Exit codes:
#   0  = success (intent logged or actions completed)
#   1  = profile not found / parse error
#   2  = unsupported OS

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROFILE="${1:?usage: bootstrap-machine.sh <profile>}"
PROFILE_FILE="$REPO_ROOT/infra/machines/${PROFILE}.yaml"

if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "ERROR: profile not found: $PROFILE_FILE" >&2
  echo "Available profiles:" >&2
  ls "$REPO_ROOT/infra/machines/"*.yaml 2>/dev/null | xargs -n1 basename | sed 's/\.yaml$//' >&2
  exit 1
fi

# Parse profile via Python (PyYAML — already a Plan 01a prerequisite)
python3 - <<PYEOF
import sys, yaml, json
profile = yaml.safe_load(open("$PROFILE_FILE"))
if profile is None:
    sys.exit("ERROR: profile is empty")

# phones.yaml has a different shape (multi-user); handle both
if "$PROFILE" == "phones":
    print(f"=== Phones profile (multi-user) ===")
    for user, cfg in profile.get("phones", {}).items():
        print(f"\nUser: {user}")
        print(f"  platform: {cfg.get('platform', '<unset>')}")
        print(f"  apps: {', '.join(cfg.get('apps', []))}")
        print(f"  notes: {cfg.get('notes', '')}")
    sys.exit(0)

print(f"=== Bootstrap intent for profile: $PROFILE ===")
print(f"hostname:     {profile.get('hostname', '<unset>')}")
print(f"role:         {profile.get('role', '<unset>')}")
print(f"owner:        {profile.get('owner', '<unset>')}")
print(f"os:           {profile.get('os', '<unset>')} {profile.get('os_version', '')}")
print(f"tailscale_ip: {profile.get('tailscale_ip', '<unset>')}")

cli = profile.get("cli_tools") or []
if cli: print(f"cli_tools:    {', '.join(cli)}")

apps = profile.get("desktop_apps") or []
if apps: print(f"desktop_apps: {', '.join(apps)}")

dock = (profile.get("docker") or {}).get("services") or []
if dock: print(f"docker:       {', '.join(dock)}")

gpu = profile.get("gpu")
if gpu:
    print(f"gpu vendor:   {gpu.get('vendor', '<unset>')}")
    if gpu.get("models"): print(f"gpu models:   {', '.join(gpu['models'])}")

print()
print("[skeleton mode] No actions performed. Plan 02 implements the installer.")
PYEOF
