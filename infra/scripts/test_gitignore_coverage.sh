#!/usr/bin/env bash
# Test: .gitignore covers every Plan 01a F23 required pattern category.
set -u
PASS=0
FAIL=0
GITIGNORE="/srv/Nexostrat/.gitignore"

check() {
  local label="$1"; local pattern="$2"
  if grep -qE "$pattern" "$GITIGNORE"; then
    echo "PASS  $label  ($pattern)"; PASS=$((PASS+1))
  else
    echo "FAIL  $label  ($pattern)"; FAIL=$((FAIL+1))
  fi
}

check "Python __pycache__"    '^__pycache__/?$|/__pycache__/?$|^\*?__pycache__'
check "Python .pyc"           '\*\.pyc$|\.pyc$'
check "Python .venv"          '\.venv/?$|^venv/?$'
check "Python egg-info"       '\*\.egg-info/?$|egg-info'
check "Node modules"          'node_modules/?$'
check "Node npm-debug"        'npm-debug\.log|\*\.log'
check "IDE JetBrains"         '\.idea/?'
check "IDE VSCode"            '\.vscode/?'
check "Editor swap"           '\*\.swp|\*~'
check "OS macOS"              '\.DS_Store'
check "OS Windows"            'Thumbs\.db'
check "Docker override"       'docker-compose\.override\.yml'
check "Age private keys"      '\*\.key|^\*\.key$'
check "Age password files"    'secrets\.env$|\*\*/secrets\.env|\*\.secrets\.json'
check "Allowlist secrets.env.age"      '^!secrets\.env\.age'
check "Allowlist secrets MANIFEST.md"  '^!infra/secrets/MANIFEST\.md'
check "shm tmpfs dumps"       '/dev/shm|nexostrat-secrets-'
check "Log dumps"             '\*\.log$'
check "PEM/PFX certs"         '\*\.pem|\*\.pfx|\*\.p12'
check "Brainstorming wd"      '\.superpowers/?'

echo
echo "Result: ${PASS} pass, ${FAIL} fail"
[ "$FAIL" -eq 0 ] || exit 1
