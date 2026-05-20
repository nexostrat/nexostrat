#!/usr/bin/env bash
# baserow-reconcile.sh — Nexostrat (Plan 02a Task 10)
#
# Scan pipeline/clients/<slug>/<station>/runs/<date>/ for skill .md files.
# Cross-reference against Baserow `deliverables` table. Create rows for orphans
# (a .md written outside the renderer's post_deliverable hook). Already-synced
# rows are a no-op — the script is idempotent and safe to run on any cadence.
#
# Filesystem is source of truth; Baserow is the index. Reconcile heals drift.
#
# Dual-mode invocation (same pattern as new-client.sh, Task 8):
#   - If BASEROW_URL + BASEROW_API_TOKEN are already in env (we're invoked from
#     within run-with-secrets.sh, e.g., pytest under the wrapper), call the
#     python step directly.
#   - Else if secrets.env.age + run-with-secrets.sh are available, spawn the
#     wrapper.
#   - Else error out with a clear message.
#
# Nesting the wrapper would trigger a second age passphrase prompt in a
# subprocess that may have no usable TTY (relevant to the nightly systemd run).
#
# Normal manual invocation:
#   infra/scripts/run-with-secrets.sh infra/scripts/baserow-reconcile.sh
#
# Nightly systemd timer: nexostrat-baserow-reconcile.timer (03:30 local).

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}

reconcile_py() {
    python3 - <<'PY'
import os, sys, pathlib

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")
sys.path.insert(0, f"{NEXOSTRAT}/skills/shared")
import baserow

# Pipeline station folder name (filesystem, Spanish-facing for stations 04/05)
# → skill identifier used in Baserow `deliverables.skill` single_select.
# Verified against pipeline/clients/_template/ and the skill renderers'
# post_deliverable() calls at Task 10 write time.
STATION_TO_SKILL = {
    "01_company_analysis":    "company-analyst",
    "02_industry_analysis":   "industry-analyst",
    "03_competitor_analysis": "competitor-analyst",
    "04_prep_llamada":        "discovery-meeting",
    "05_opportunity_report":  "opportunity-report",
}

clients_dir = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients")
if not clients_dir.exists():
    print("No pipeline/clients/ folder; nothing to reconcile")
    sys.exit(0)

orphans = 0
synced = 0
for client_dir in sorted(clients_dir.iterdir()):
    if not client_dir.is_dir():
        continue
    # Skip _template and dotfolders.
    if client_dir.name.startswith(("_", ".")):
        continue
    slug = client_dir.name
    client = baserow._find_one("clients", "slug", slug)
    if not client:
        print(
            f"WARNING: client folder {slug!r} has no Baserow row; "
            f"skipping deliverables for this client",
            file=sys.stderr,
        )
        continue
    cid = client["id"]
    for station, skill_name in STATION_TO_SKILL.items():
        runs = client_dir / station / "runs"
        if not runs.exists():
            continue
        for run_dir in sorted(runs.iterdir()):
            if not run_dir.is_dir():
                continue
            mds = sorted(run_dir.glob("*.md"))
            if not mds:
                continue
            # Canonical: one .md per run dir (matches renderer convention).
            md = mds[0]
            docx = md.with_suffix(".docx")
            pdf = md.with_suffix(".pdf")
            existing = baserow._find_one("deliverables", "file_md", str(md))
            if existing:
                synced += 1
                continue
            baserow.post_deliverable(
                client_id=cid,
                skill=skill_name,
                file_md=str(md),
                file_docx=str(docx) if docx.exists() else "",
                file_pdf=str(pdf) if pdf.exists() else "",
            )
            orphans += 1

print(f"Reconcile complete: {orphans} orphan(s) added, {synced} already in sync")
PY
}

export NEXOSTRAT

if [[ -n "${BASEROW_URL:-}" && -n "${BASEROW_API_TOKEN:-}" ]]; then
    reconcile_py
elif [[ -f "$NEXOSTRAT/secrets.env.age" && -x "$NEXOSTRAT/infra/scripts/run-with-secrets.sh" ]]; then
    export -f reconcile_py
    "$NEXOSTRAT/infra/scripts/run-with-secrets.sh" bash -c reconcile_py
else
    echo "ERROR: secrets not available — set BASEROW_URL+BASEROW_API_TOKEN, or provide $NEXOSTRAT/secrets.env.age and run-with-secrets.sh" >&2
    exit 1
fi
