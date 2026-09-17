"""Core lesson-routing logic.

Scores a durable lesson against the standing files by keyword overlap
(plus a phrase bonus for exact multi-word matches) and returns a ranked
recommendation. The script scores; the agent decides.

Pure functions here — no filesystem reads except in ``load_identity`` —
so this module is trivially testable. Examples/tests are runtime
parameters; nothing is hardcoded to a specific lesson, agent, or
identity file.
"""
import os
import re
from collections import Counter

#: Human-readable ownership table: which standing file owns what.
#: The six names below match the skill's convention (~/IDENTITY.md etc.),
#: but the module never assumes them — pass ``file_keywords`` to
#: :func:`recommend` to route against any corpus of target files.
OWNERSHIP = {
    "IDENTITY.md": (
        "Who the agent is: name, character, vibe, emoji, relationship "
        "posture, delegation trust, typo protocol, autonomy stance, "
        "refusal-handling posture"
    ),
    "SOUL.md": (
        "How the agent works: operational behavior, live loops, evidence "
        "rules, output architecture, refusals, forensics, memory "
        "discipline, handoff triage"
    ),
    "MEMORY.md": (
        "Durable facts: standing orders, platform state, key paths, "
        "tool quirks, open items, dated log, approvals"
    ),
    "USER.md": (
        "Who the user is: name, timezone, register, trust shape, "
        "entrypoint, stack, autonomy bounds"
    ),
    "AGENTS.md": (
        "Workspace ops: shell routes, git rules, worker/fleet conventions, "
        "latency doctrine, bridge usage, forensics pipeline, never-ask "
        "rules, retired notes, ops log"
    ),
    "TOOLS.md": (
        "Tool-specific quirks: device nicknames, host aliases, voices, "
        "environment-specific notes"
    ),
}

#: Keyword signals per standing file. These are the canonical defaults;
#: :func:`recommend` accepts any ``file_keywords`` mapping so the router
#: stays universal rather than welded to one agent's files.
FILE_KEYWORDS = {
    "IDENTITY.md": [
        "identity", "who i am", "character", "vibe", "emoji", "persona",
        "tone", "relationship", "trust", "delegation", "typo", "autonomy",
        "right hand", "familiar", "refusal posture", "co-owner", "yolo",
        "question", "clarify", "branch", "gate", "blocking", "answer",
    ],
    "SOUL.md": [
        "soul", "how i work", "workflow", "operational", "behavior",
        "evidence", "verify", "live loop", "react", "ooda", "act don't ask",
        "closed loop", "forensics", "parquet", "output", "sections",
        "triage", "handoff", "attention", "maintenance", "destruction",
        "never ask", "race", "forward only",
    ],
    "MEMORY.md": [
        "memory", "standing order", "fact", "deadline", "due", "appointment",
        "meeting", "scheduled", "schedule", "open item", "platform state",
        "key path", "tool quirk", "approval", "commitment", "remember",
        "log", "status", "graph", "citation", "research",
    ],
    "USER.md": [
        "chris", "user", "timezone", "register", "terse", "bursts",
        "entry", "android", "main chat", "stack", "awrawr", "cell",
    ],
    "AGENTS.md": [
        "shell", "git", "push", "worker", "fleet", "subagent", "bridge",
        "exec.py", "taskhook", "latency", "cron", "hook", "pitchfork",
        "worktree", "never ask", "directive",
    ],
    "TOOLS.md": [
        "device", "nickname", "host alias", "voice", "chromium",
        "headless", "proxy", "quirk", "environment",
    ],
}

STOP = frozenset(
    "the a an and or of to in on for with is are was were be been it its "
    "this that these those as at by from i you he she we they my your his "
    "her our their me him us them do does did not no yes so but if then "
    "than too very can will just should would could there here what when "
    "where which who how why".split()
)

TOKEN_RE = re.compile(r"[a-z0-9']+")


def tokens(text):
    """Lowercased token list with stopwords removed."""
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOP]


def score_lesson(lesson, keywords):
    """Score one target's keyword set against the lesson.

    Returns ``(score, hits)`` where ``hits`` maps matched keywords to
    their weight. Token overlap is weighted by keyword length
    (multi-word signals count more); an exact phrase occurrence adds a
    bonus on top.
    """
    lt = tokens(lesson)
    hits = Counter()
    for kw in keywords:
        kwt = tokens(kw)
        n = sum(1 for t in lt if t in kwt)
        if n:
            # multi-word keyword matches weigh more
            hits[kw] = n * len(kwt)
    # phrase bonus: exact keyword occurrence as a whole word/phrase.
    # Word-boundary matching on purpose — a raw substring check misfires
    # (e.g. "terse" inside "petersen"); boundaries keep the bonus honest.
    low = lesson.lower()
    for kw in keywords:
        if re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", low):
            hits[kw] += 3
    return sum(hits.values()), dict(hits)


def recommend(lesson, file_keywords=None):
    """Rank standing files for a lesson.

    Returns a list of ``(score, filename, hits)`` tuples, highest first.
    ``hits`` maps each matched keyword to its weight. ``file_keywords``
    defaults to :data:`FILE_KEYWORDS`; pass your own mapping to route
    against any corpus — the router stays universal.
    """
    if not lesson or not lesson.strip():
        raise ValueError("lesson must be a non-empty string")
    file_keywords = FILE_KEYWORDS if file_keywords is None else file_keywords
    ranked = []
    for fname, kws in file_keywords.items():
        s, hits = score_lesson(lesson, kws)
        ranked.append((s, fname, hits))
    # highest score first; ties break alphabetically for determinism
    ranked.sort(key=lambda r: (-r[0], r[1]))
    return ranked


def render_recommendation(lesson, ranked):
    """Render a ranked recommendation as the CLI's human-readable text."""
    lines = [f"lesson: {lesson}", ""]
    for i, (s, fname, hits) in enumerate(ranked):
        mark = " <-- recommended" if i == 0 and s > 0 else ""
        lines.append(f"{s:3d}  ~/{fname}{mark}")
        top = ", ".join(sorted(hits, key=hits.get, reverse=True)[:4])
        if top:
            lines.append(f"      matched: {top}")
    if ranked and ranked[0][0] == 0:
        lines.append("")
        lines.append("no keyword signal — read the files and decide by ownership table.")
    return "\n".join(lines) + "\n"


def identity_path():
    """Where the agent's identity file lives.

    Defaults to ``~/IDENTITY.md``; override with
    ``IDENTITY_ROUTER_IDENTITY`` for tests, demos, or alternate agents.
    """
    return os.environ.get("IDENTITY_ROUTER_IDENTITY", os.path.join(os.path.expanduser("~"), "IDENTITY.md"))
