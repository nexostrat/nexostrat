#!/usr/bin/env python3
"""inline_includes.py — Nexostrat (C3 fix)

Replace {{include: <path>}} markers in a template with the file contents at <path>.
Path is resolved relative to the template's own directory.

Usage:
  inline_includes.py --template <tmpl> --output <out>
      Generate <out> from <tmpl>.

  inline_includes.py --template <tmpl> --check <existing>
      Generate from <tmpl> and compare against <existing>.
      Exit 0 if identical; exit 1 with a unified diff if different.
"""
from __future__ import annotations
import argparse, difflib, pathlib, re, sys

MARKER = re.compile(r'^\{\{include:\s*([^}]+?)\s*\}\}\s*$', re.M)


MAX_DEPTH = 10  # Hard cap to defend against include-cycles; 10 is generous.


def render(template_path: pathlib.Path) -> str:
    text = template_path.read_text(encoding='utf-8')
    base = template_path.parent

    def sub(match: re.Match[str]) -> str:
        rel = match.group(1).strip()
        target = (base / rel).resolve()
        # Boundary is base.parent — the template's parent directory's parent. For the
        # 00_META/templates/ + 00_META/shared/ split this allows curated siblings via
        # ../shared/<stanza>.md while still blocking escapes to infra/, vault/, /etc/,
        # etc. Tighten if a template layout ever lands where this boundary is too lax.
        if not target.is_relative_to(base.parent.resolve()):
            sys.exit(f"ERROR: include path escapes allowed root: {rel} (resolved {target})")
        if not target.is_file():
            sys.exit(f"ERROR: include path not found: {rel} (resolved {target})")
        # Strip exactly one trailing newline (not all) so {{include}} on its own
        # line doesn't double-blank, while preserving any intentional blank lines
        # the included file ends with.
        content = target.read_text(encoding='utf-8')
        return content[:-1] if content.endswith('\n') else content

    # Iterate to a fixed point so nested {{include}} markers (an include whose
    # content itself contains an include) expand fully. Stanzas at 01c don't
    # nest today, but future stanzas may; the guard bounds depth so a cycle
    # fails loudly instead of looping forever.
    for _ in range(MAX_DEPTH):
        new_text = MARKER.sub(sub, text)
        if new_text == text:
            return text
        text = new_text
    sys.exit(f"ERROR: include depth exceeded {MAX_DEPTH} — possible cycle in {template_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True, type=pathlib.Path)
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument('--output', type=pathlib.Path)
    grp.add_argument('--check',  type=pathlib.Path)
    args = ap.parse_args()

    rendered = render(args.template)

    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
        return 0

    # --check
    existing = args.check.read_text(encoding='utf-8') if args.check.is_file() else ''
    if existing == rendered:
        return 0
    print(f"DRIFT: {args.check}")
    sys.stdout.writelines(difflib.unified_diff(
        existing.splitlines(keepends=True),
        rendered.splitlines(keepends=True),
        fromfile=str(args.check),
        tofile=str(args.template) + ' (rendered)',
    ))
    return 1


if __name__ == '__main__':
    sys.exit(main())
