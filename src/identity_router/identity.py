"""Answer "what's my current identity?" from the agent's IDENTITY.md.

Parses the file's top bullet fields (``- **Name:** ...``) plus the
section headers that carry live posture (autonomy, refusal handling,
forensics, typo protocol). Reports only — never edits, never polices.

The identity file path defaults to ``~/IDENTITY.md`` and is overridable
via the ``IDENTITY_ROUTER_IDENTITY`` environment variable (used by the
tests and demos so no real agent file is ever required).
"""
import json
import re

from .route import identity_path

#: Section-header substrings that count as "live posture" markers.
POSTURE_MARKERS = ("refusal", "autonom", "forensic", "typo")

TOP_FIELD_RE = re.compile(r"^- \*\*(\w[\w ]*):\*\*\s*(.+)$", re.M)
SECTION_RE = re.compile(r"^## (.+)$", re.M)


def parse_identity(text):
    """Parse IDENTITY.md text into a dict of fields + posture sections.

    ``text`` is raw markdown. Returns keys ``name``, ``character``,
    ``vibe``, ``emoji`` (lowercased field names) and ``_posture_sections``
    (section headers matching :data:`POSTURE_MARKERS`).
    """
    ident = {}
    for m in TOP_FIELD_RE.finditer(text):
        ident[m.group(1).strip().lower()] = m.group(2).strip()
    sections = SECTION_RE.findall(text)
    ident["_posture_sections"] = [
        s for s in sections if any(marker in s.lower() for marker in POSTURE_MARKERS)
    ]
    return ident


def load_identity(path=None):
    """Parse the identity file into a core dict.

    Returns ``{"name", "character", "vibe", "emoji", "posture", "source"}``
    with ``"?"`` for any missing field. Raises ``FileNotFoundError`` if
    the identity file does not exist.
    """
    path = path or identity_path()
    text = open(path, encoding="utf-8").read()
    ident = parse_identity(text)
    return {
        "name": ident.get("name", "?"),
        "character": ident.get("character", "?"),
        "vibe": ident.get("vibe", "?"),
        "emoji": ident.get("emoji", "?"),
        "posture": ident.get("_posture_sections", []),
        "source": path,
    }


def render_identity(core):
    """Render the human-readable identity summary."""
    lines = [
        f"{core['emoji']}  {core['name']}",
        f"character: {core['character']}",
        f"vibe: {core['vibe']}",
    ]
    if core.get("posture"):
        lines.append("posture: " + "; ".join(core["posture"]))
    lines.append(f"(source: {core['source']})")
    return "\n".join(lines) + "\n"


def identity_json(core):
    """Render the identity as JSON (for ``--json`` / MCP)."""
    return json.dumps(
        {
            "name": core["name"],
            "character": core["character"],
            "vibe": core["vibe"],
            "emoji": core["emoji"],
            "posture": core.get("posture", []),
            "source": core["source"],
        },
        indent=2,
    )
