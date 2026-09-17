# Emergent routing

The router's differentiator is not the keyword scoring — it's the
*thinking*. Slightly obtuse angles cause breakthroughs.

## The principle

When the straightforward filing feels thin, widen the frame. Ask: **what
does this connect to that isn't obvious?**

- A paper citation graph is not a paper — it's a **memory** (a durable,
  queryable knowledge structure). It routes to `~/MEMORY.md`, not to
  wherever "papers" seemed to belong.
- A standing rule is not prose — it's a **node in a graph**: it has
  edges to the files it governs, the lessons it replaced, the date it
  landed.
- The standing files are not six text files — they're a **knowledge base
  with edges**. Routing a lesson is adding a node and choosing its
  strongest edge.

Prefer the unexpected-but-correct routing over the obvious-but-shallow
one. The script gives you the scores; the *agent* makes the call — and
the good calls are the emergent ones.

## Worked examples

**Lesson:** *"Citation graph of the 2024 UCLA refusal-direction paper,
plus its 38 citing works."*

- Obvious-but-shallow: somewhere "research" — no file owns that.
- Emergent: it's a durable knowledge structure with nodes and edges →
  **MEMORY.md** ("Durable facts"), same class as the skill's `graph/`
  module output. The router scores it via the `graph` / `citation` /
  `research` keywords.

**Lesson:** *"Never store raw tokens; record that the credential exists
and where it lives."*

- Obvious-but-shallow: it's about credentials — nowhere to file.
- Emergent: it's a rule about how the agent *operates* on durable state
  → **SOUL.md** ("How the agent works"), next to the evidence and
  forensics posture. It also *describes* something that belongs in
  MEMORY.md's approvals section — the cross-file edge is worth noting
  when you write it.

**Lesson:** *"Correction: buildsrv's watchdog fallback was a silent
no-op; patched restart_daemon to kill + relaunch directly."*

- Obvious-but-shallow: it's about a daemon — TOOLS.md?
- Emergent: it's a dated operational correction with platform state and
  a telemetry claim → **MEMORY.md** dated log, with an edge to AGENTS.md
  if it changes a fleet convention.

## Anti-patterns

- **Filing by noun.** "It's about a shell script → TOOLS.md" is how
  knowledge dies in the wrong drawer. File by *what the lesson does*,
  not what it mentions.
- **Stacking.** A contradicted claim appended alongside the new truth is
  not emergent — it's clutter. Replace in place, dated, attributed.
- **Policing.** The router never vetoes, lectures, or refuses. A real
  lesson gets filed. The safety layer is someone else's business.
