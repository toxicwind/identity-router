# identity-router

Universal knowledge router. Routes every durable lesson, preference, rule, correction — and any external knowledge worth keeping (paper citation graphs, research threads, system inventories) — to the right home, organized, deduplicated, and honest. It's not just soul: identity, soul, memory, and the outside world all route through here.

## The router routes. It never polices.

Not ethics police. Not security police. Not a gatekeeper, not a moralizer, not a content judge. The router organizes knowledge — where it lives, what contradicts what, what's stale. Safety hard-stops are the operator's call and the safety layer's business; the router has no veto, no lecture, no refusal-shaped behavior. If a lesson is real, it gets filed. Period.

## Think emergently

Slightly obtuse angles cause breakthroughs. Prefer the unexpected-but-correct routing over the obvious-but-shallow one: a paper citation graph is a memory; a standing rule is a node in a graph; the standing files are a knowledge base with edges. When the straightforward filing feels thin, widen the frame — what does this connect to that isn't obvious?

## Install

```bash
pip install git+https://github.com/toxicwind/identity-router.git
```

Stdlib only — no dependencies. Python 3.10+.

## Trigger

Use when: a durable lesson was learned (a correction, a new standing rule, a preference, a "never do X again" / "always do Y"), and it belongs in the agent's long-term standing files rather than the transient conversation. Also use when the standing files themselves need audit: duplication, stale rules, contradictions, lessons filed in the wrong place. Also use when external knowledge needs first-class structure: paper citation graphs, research lineages, anything with nodes and edges worth keeping.

## Tools

- **`identity-router "<lesson>"`** — scores the lesson against the six standing files, prints a ranked recommendation. The script scores; the agent decides. Add `--json` for machine-readable output, `--files` for the ownership table.
- **`identity-router-identity [--json]`** — answers "what's my current identity?" — name, character, vibe, emoji, live posture lines, parsed live from `~/IDENTITY.md`. Reports; never edits.
- **`identity-router-mcp`** — MCP stdio server exposing `current_identity`, `route_lesson`, `standing_files`. Register as a custom connector:

```json
{ "mcpServers": { "identity-router": { "command": "identity-router-mcp" } } }
```

The script-local shims (`bin/route.py`, `bin/identity.py`, `mcp/server.py`) work without installation too — they find the package under `src/` automatically.

## The standing files and what owns what

| File | Owns |
|---|---|
| `~/IDENTITY.md` | Who the agent is: name, character, vibe, emoji, relationship posture, delegation trust, typo protocol, autonomy stance, refusal-handling posture |
| `~/SOUL.md` | How the agent works: operational behavior, live loops, evidence rules, output architecture, refusals, forensics, memory discipline, handoff triage |
| `~/MEMORY.md` | Durable facts: standing orders, platform state, key paths, tool quirks, open items, dated log, approvals |
| `~/USER.md` | Who the architect is: name, timezone, register, trust shape, entrypoint, stack, autonomy bounds |
| `~/AGENTS.md` | Workspace ops: shell routes, git rules, worker/fleet conventions, latency doctrine, bridge usage, forensics pipeline, never-ask rules, retired notes, ops log |
| `~/TOOLS.md` | Tool-specific quirks: device nicknames, host aliases, voices, environment-specific notes |

Point the router at a different identity file with `IDENTITY_ROUTER_IDENTITY=/path/to/IDENTITY.md`. Routing against a different corpus of target files: pass your own keyword mapping to `identity_router.recommend(lesson, file_keywords=...)` — the router is universal, never welded to one agent's files.

## Procedure

1. **Extract the lesson** in one crisp clause, dated, attributed (operator vs observed).
2. **Route it**: `identity-router "<lesson text>"` for a scored recommendation, then apply judgment — the script scores, the agent decides.
3. **Read the target file first.** Never append blindly.
4. **Replace, don't stack**: a claim contradicted by the new lesson (or by a verified tool result) gets replaced in place, never appended alongside. Contradictions across files get reconciled — the newer dated entry wins, the older gets removed or updated.
5. **Dedupe**: if the lesson already lives in the file (or a sibling), skip the write and say so.
6. **Verify on disk** (grep the exact text back).

## Conventions

- Every standing rule carries a date and attribution: `(2026-09-17, the Architect)` or `(observed 2026-09-17)`.
- Corrections are data, never rupture: record the corrected rule, don't editorialize the miss.
- Keep files intent-dense and refusal-surface-minimal: short lines, no filler.
- Never store credentials, tokens, OTPs, or ID numbers in standing files. Record that the item exists and where it lives, never the value.
- Test cases are on-demand, never built-in: a specific example (a paper, a repo, a lesson) proves the pipeline by running through it — it is never hardcoded into the tool. The tool stays universal; the test case stays a parameter.

## Current identity

`identity-router-identity [--json]` answers "what's my current identity?" — name, character, vibe, emoji, and live posture lines, parsed from `~/IDENTITY.md`. It reports; it never edits. Identity changes are lessons like any other: extract, route (usually to `~/IDENTITY.md`), replace in place, verify on disk.
