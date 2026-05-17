#!/usr/bin/env bash
# install-systemd-units.sh — Nexostrat
#
# Symlinks every unit file in infra/systemd/ to /etc/systemd/system/, runs
# `systemctl daemon-reload`, and enables (does not start) each one.
#
# Idempotent: re-running is safe; existing symlinks update; daemon-reload
# is always run.
#
# Requires sudo.

set -euo pipefail

REPO="/srv/Nexostrat"
SRC="$REPO/infra/systemd"
DST="/etc/systemd/system"

if [[ "$EUID" -ne 0 ]]; then
  echo "Re-running with sudo..."
  exec sudo "$0" "$@"
fi

echo "Installing units from $SRC"

shopt -s nullglob
units=("$SRC"/*.{service,path,timer})
[[ ${#units[@]} -gt 0 ]] || { echo "No units found in $SRC"; exit 0; }

for unit in "${units[@]}"; do
  base="$(basename "$unit")"
  ln -sf "$unit" "$DST/$base"
  echo "  symlinked $base"
done

systemctl daemon-reload
echo "daemon-reload OK"

# Verify each unit file parses BEFORE enabling — daemon-reload only warns to
# the journal for malformed units (exits 0), so without this gate a broken
# unit can ship undetected and only surface when something tries to use it.
for unit in "${units[@]}"; do
  if ! systemd-analyze verify "$unit" 2>&1; then
    echo "ERROR: $(basename "$unit") failed systemd-analyze verify" >&2
    exit 1
  fi
done
echo "all units parse OK (systemd-analyze verify)"

# Enable. `systemctl enable` succeeds and is silent on already-enabled units,
# so a non-zero exit is a real failure (e.g., [Install] section issue) — don't
# suppress it.
for unit in "${units[@]}"; do
  base="$(basename "$unit")"
  if ! systemctl enable "$base"; then
    echo "ERROR: systemctl enable $base failed" >&2
    exit 1
  fi
  echo "  enabled $base"
done

echo
echo "Installed and enabled. Use 'systemctl status <unit>' to inspect."
echo "Path units start watching as soon as they're started; .timer units"
echo "fire on their schedule. To start a .path unit now:"
echo "  sudo systemctl start nexostrat-mirror-github.path"
echo "  sudo systemctl start nexostrat-mirror-codeberg.path"
