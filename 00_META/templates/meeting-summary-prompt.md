# Meeting summary PDF template — Nexostrat

  Goal: produce a Nexostrat-branded PDF from any `summary.md` in
  `/srv/meetings/nexostrat/<date>/<slug>/` via pandoc + weasyprint.

  Files to create in this folder (`/srv/Nexostrat/00_META/templates/`):
  1. `meeting-summary.html.j2` — pandoc HTML5 template containing
     `$title$`, `$body$`, `$date$` placeholders; wrap `$body$` in
     `<main class="document">` for CSS targeting.
  2. `meeting-summary.css` — print CSS for weasyprint with brand colors
     as `:root` CSS vars and `@page` rules for header + footer.
  3. `assets/logo.png` — if Ricardo hasn't dropped one, use a text
     word-mark in the header instead.

  Before writing files, ask Ricardo for:
  - Logo file (or "use placeholder")
  - 4 brand colors (primary / secondary / text / background) — accept
    "use defaults" → navy `#0F2A4A` / teal `#1F8FBF` / `#1A1A1A` / white
  - Heading font + body font (defaults: Inter / Source Serif Pro via
    Google Fonts CDN — embed via `<link>` in the HTML template)
  - Footer line (default: `Nexostrat — Confidencial · página $page$`)
  - Paper size: A4 (default) or Letter

  After files exist, verify with:

      LATEST=$(ls -dt /srv/meetings/nexostrat/*/* | head -1)
      pandoc "$LATEST/summary.md" \
        --template=/srv/Nexostrat/00_META/templates/meeting-summary.html.j2 \
        --css=/srv/Nexostrat/00_META/templates/meeting-summary.css \
        --pdf-engine=weasyprint \
        -V title="$(basename $LATEST)" \
        -o /tmp/test-summary.pdf
      xdg-open /tmp/test-summary.pdf

  Then update `00_META/templates/README.md` (append a "Meeting summary
  PDF template" section listing the pandoc command). Commit + push:

      cd /srv/Nexostrat
      git add 00_META/templates/meeting-summary.* \
              00_META/templates/assets \
              00_META/templates/README.md
      git commit -m "templates: meeting-summary PDF template + brand assets"
      git push origin main && git push github main && git push codeberg main

  Until `meeting-pipeline.sh` is extended (a Phase 7 follow-up), the PDF
  is generated manually after each `meeting finish` run. The hub's
  `/resumen completo` still sends `summary.md` for now.

  Quickest way to save it:

  cat > /srv/Nexostrat/00_META/templates/meeting-summary-prompt.md <<'EOF'
  [paste the content above, ending with EOF]
  EOF
