# Claude → Gemini Handoff

> **Status:** TEMPLATE
> **Created:** <YYYY-MM-DD>
> **Raised by:** <Claude | Ricardo>
> **Task type:** <search | audit | review | brainstorm | verify>

## Context

<Why we're asking — what Ricardo is working on, what decisions led here, what makes this a handoff-worthy question.>

## The ask

<One clear question or task. Be specific.>

## Constraints / Scope

- <What Gemini should and shouldn't do>
- <Files or data to consult>
- <Expected output format & length>

## Relevant files

- <path> — <why>

## Output expectations

Write your response to `00_META/handoff/gemini_to_claude.md` using the response template. Change the status of this file from `IN_PROGRESS` to `RESOLVED` when done.

## Not in scope

- <Things Gemini should explicitly skip>

---

> **How to use this file:**
> When Claude raises a real handoff, it overwrites this template with real values and changes `Status` to `OPEN`. When Gemini picks it up, it changes `Status` to `IN_PROGRESS`. When Gemini finishes, it changes `Status` to `RESOLVED` and writes the companion response file. When Claude integrates, it moves both files to `archive/YYYY-MM-DD_<slug>.md` and restores this template.
