#!/usr/bin/env python3
"""nexostrat-memos.py — Nexostrat (F8)

Scan **/00_META/inbox/*.md across the repo, parse YAML-style frontmatter,
filter by `to:` field, print a formatted summary.

Usage:
  nexostrat-memos.py <persona>
      persona ∈ {founder, skills-master, client-owner, broadcast, all}

Output: one line per memo, sorted by priority then created.

Frontmatter expected:
    ---
    status: open | resolved | deferred
    from: founder | skills-master | client-owner | telegram-<id>
    to: founder | skills-master | client-owner | broadcast
    type: question | request | observation | decision | note
    priority: critical | high | medium | low
    subject: <one-line>
    created: <ISO-8601>
    related: [<paths>]
    due: <ISO-8601>
    ---
"""
from __future__ import annotations
import pathlib, re, sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PRIORITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, '': 4}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return a flat dict of frontmatter fields. Values stay as strings."""
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end < 0:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*?)\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def collect(persona: str) -> list[tuple[str, dict[str, str], pathlib.Path]]:
    out = []
    for inbox in REPO_ROOT.glob('**/00_META/inbox'):
        for memo in sorted(inbox.glob('*.md')):
            if memo.name == '.gitkeep':
                continue
            try:
                text = memo.read_text(encoding='utf-8')
            except Exception:
                continue
            fm = parse_frontmatter(text)
            if not fm:
                continue
            if fm.get('status', 'open') != 'open':
                continue
            to_field = fm.get('to', '')
            # Note: Python `and` binds tighter than `or`, so the `broadcast` clause is parenthesized
            # explicitly to spare future readers a parse step.
            if persona == 'all' or to_field == persona or (to_field == 'broadcast' and persona != 'all'):
                out.append((to_field, fm, memo))
    out.sort(key=lambda t: (PRIORITY_ORDER.get(t[1].get('priority', ''), 4),
                            t[1].get('created', '')))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    persona = sys.argv[1]
    items = collect(persona)
    if not items:
        print(f"  (no open memos for: {persona})")
        return 0
    print(f"  Open memos for: {persona}  ({len(items)} total)\n")
    for _to, fm, memo in items:
        rel = memo.relative_to(REPO_ROOT)
        prio = fm.get('priority', '?')
        typ = fm.get('type', '?')
        frm = fm.get('from', '?')
        subj = fm.get('subject', '<no subject>')
        due = f" due={fm['due']}" if fm.get('due') else ''
        print(f"  [{prio:8}] {typ:10}  from {frm}  →  {subj}{due}")
        print(f"             ({rel})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
