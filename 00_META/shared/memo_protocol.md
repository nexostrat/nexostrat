## Cross-Folder Memo Protocol

Per ADR-013 + spec §4.7. Each persona has an inbox at `<scope>/00_META/inbox/` and an `archive/`. Each memo is one .md file with YAML frontmatter:

```
---
status: open | resolved | deferred
from: founder | skills-master | client-owner | telegram-<userid>
to: founder | skills-master | client-owner | broadcast
type: question | request | observation | decision | note
priority: critical | high | medium | low
subject: <one-line>
created: <ISO-8601 timestamp>
related: [<paths or task ids>]
due: <ISO-8601 date if applicable>
---

<body>
```

**Operator-driven scope (per Strict Rule 1):** when Ricardo or JP is driving, memos are not required for cross-folder edits — they're a paper trail mechanism for specialist requests, async coordination, and autonomous-agent communication.

**At session start**, this persona reads its inbox via `infra/scripts/nexostrat-memos.py <persona>` which prints a formatted summary filtered by `to:`.

**Resolution lifecycle:** open → resolved (move file to `archive/`) OR deferred (update `due:`, keep in inbox). Telegram `/inbox`, `/resolve <id>`, `/defer <id>` plugins (Plan 04) wrap this.
