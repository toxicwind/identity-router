# Extending the router

The router is universal by construction — it is never welded to one
agent's six files. Two extension points, both runtime parameters.

## 1. A different identity file

```bash
IDENTITY_ROUTER_IDENTITY=/path/to/other/IDENTITY.md identity-router-identity --json
```

The parser reads the top bullet fields (`- **Name:** ...`) and the
section headers matching the posture markers (refusal, autonomy,
forensics, typo). Any markdown file shaped like that works.

## 2. A different corpus of target files

`recommend()` takes any keyword mapping — target filename to keyword
list. The six standing files are the default, not the definition:

```python
from identity_router import recommend

my_files = {
    "RUNBOOK.md": ["deploy", "rollback", "incident", "on-call"],
    "DECISIONS.md": ["adr", "chose", "tradeoff", "rejected"],
    "PEOPLE.md": ["met", "intro", "contact", "team"],
}

ranked = recommend("We chose Postgres over SQLite for the queue", file_keywords=my_files)
print(ranked[0][1])  # DECISIONS.md
```

This is also how you add a seventh standing file without touching the
tool: compose your own mapping and pass it in. The scoring semantics
(multi-word weighting, word-boundary phrase bonus, deterministic
alphabetical tie-break) apply to any corpus.

## 3. Tuning keywords

`identity_router.route.FILE_KEYWORDS` is a plain dict — read it,
copy it, extend it in your own code. Keyword design guidance:

- Prefer **multi-word phrases** ("standing order" beats "order") —
  they carry more weight in scoring and resist cross-file collisions.
- Name the **file's own concepts** ("memory" for MEMORY.md) so
  self-referential lessons ("this is a memory") route correctly.
- The phrase bonus is **word-boundary** matched: "terse" won't fire
  inside "petersen". Single tokens that are substrings of common words
  are safe.
- Keep keywords **orthogonal across files** where possible; when two
  files genuinely share a signal ("never ask" in SOUL.md and AGENTS.md),
  the denser file wins and the runner-up stays visible in the ranking.

## 4. The procedure around the tool

The router scores; the agent decides. The surrounding procedure —
extract the lesson dated and attributed, read the target file first,
replace don't stack, dedupe, verify on disk — lives in SKILL.md and
applies to any corpus you point the router at.
