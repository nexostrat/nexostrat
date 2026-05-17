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

for unit in "${units[@]}"; do
  base="$(basename "$unit")"
  systemctl enable "$base" >/dev/null 2>&1 || \
    { echo "WARN: enable $base — skipping (probably already enabled)"; continue; }
  echo "  enabled $base"
done

echo
echo "Installed and enabled. Use 'systemctl status <unit>' to inspect."
echo "Path units start watching as soon as they're started; .timer units"
echo "fire on their schedule. To start a .path unit now:"
echo "  sudo systemctl start nexostrat-mirror-github.path"
echo "  sudo systemctl start nexostrat-mirror-codeberg.path"
