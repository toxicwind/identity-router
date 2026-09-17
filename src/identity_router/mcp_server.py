"""identity-router MCP server (stdio, stdlib only).

Exposes the identity-router package as MCP tools so any MCP client can
add it as a custom connector:

    { "mcpServers": { "identity-router": {
        "command": "identity-router-mcp" } } }

(``identity-router-mcp`` is installed by ``pip install``; run this
module directly with ``python -m identity_router.mcp_server`` too.)

Tools:
  current_identity  - what's my current identity? (name, character, vibe,
                      emoji, posture from the identity file)
  route_lesson      - score a durable lesson against the standing files;
                      returns the ranked routing recommendation. The caller
                      decides; this tool never writes.
  standing_files    - ownership table: which standing file owns what.
"""
import json
import sys

from .identity import identity_json, load_identity
from .route import OWNERSHIP, recommend, render_recommendation

TOOLS = [
    {
        "name": "current_identity",
        "description": (
            "Answer 'what's my current identity?' — the agent's name, "
            "character, vibe, emoji, and live posture lines. Reports only; "
            "never edits."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "route_lesson",
        "description": (
            "Score a durable lesson (correction, standing rule, preference) "
            "against the standing files and return the ranked routing "
            "recommendation with matched keywords. The caller decides the "
            "target; this tool never writes to disk."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lesson": {"type": "string", "description": "The durable lesson text to route"}
            },
            "required": ["lesson"],
            "additionalProperties": False,
        },
    },
    {
        "name": "standing_files",
        "description": "The ownership table: which standing file owns which kind of knowledge.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


def call_tool(name, args):
    if name == "current_identity":
        try:
            core = load_identity()
        except FileNotFoundError:
            return "error: no identity file found (set IDENTITY_ROUTER_IDENTITY)"
        return identity_json(core)
    if name == "route_lesson":
        lesson = (args or {}).get("lesson", "")
        if not lesson.strip():
            return "error: 'lesson' must be a non-empty string"
        return render_recommendation(lesson, recommend(lesson))
    if name == "standing_files":
        return json.dumps(OWNERSHIP, indent=2)
    return f"error: unknown tool '{name}'"


def respond(req_id, result):
    sys.stdout.write(
        json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n"
    )
    sys.stdout.flush()


def handle(msg):
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params", {}) or {}
    if method == "initialize":
        respond(
            req_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "identity-router", "version": "1.0.0"},
            },
        )
    elif method in ("notifications/initialized", "notifications/cancelled"):
        pass
    elif method == "tools/list":
        respond(req_id, {"tools": TOOLS})
    elif method == "tools/call":
        text = call_tool(params.get("name"), params.get("arguments"))
        respond(req_id, {"content": [{"type": "text", "text": text}]})
    elif req_id is not None:
        sys.stdout.write(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"unknown method {method}"},
                }
            )
            + "\n"
        )
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            handle(json.loads(line))
        except Exception as e:  # never die on a bad frame
            sys.stderr.write(f"frame error: {e}\n")


if __name__ == "__main__":
    main()
