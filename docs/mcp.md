# MCP server

`identity-router-mcp` (or `mcp/server.py`) exposes the router over MCP
stdio — stdlib only, no dependencies. Any MCP client can register it as
a custom connector:

```json
{
  "mcpServers": {
    "identity-router": {
      "command": "identity-router-mcp"
    }
  }
}
```

Without a pip install, point at the shim instead:

```json
{
  "mcpServers": {
    "identity-router": {
      "command": "/path/to/identity-router/mcp/server.py"
    }
  }
}
```

## Tools

### `current_identity`

"What's my current identity?" — name, character, vibe, emoji, and live
posture lines parsed from the identity file. Reports only; never edits.

Reads `IDENTITY_ROUTER_IDENTITY` if set, else `~/IDENTITY.md`.

### `route_lesson`

Score a durable lesson against the standing files. Returns the ranked
recommendation with matched keywords. **The caller decides; this tool
never writes to disk.**

```json
{
  "name": "route_lesson",
  "arguments": { "lesson": "Never ask before running idempotent cleanup" }
}
```

### `standing_files`

The ownership table: which standing file owns which kind of knowledge.

## Verify the server

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | identity-router-mcp
```

Expect an `initialize` result with `serverInfo.name: "identity-router"`
and a `tools/list` result with the three tools above.

## Design notes

- The server never dies on a bad frame: malformed JSON on stdin is
  logged to stderr and skipped.
- Notifications (`notifications/initialized`, `notifications/cancelled`)
  are accepted silently.
- Tool results are plain text — `route_lesson` returns the same ranked
  text the CLI prints, so an agent reading it gets the full scoring
  context, not just a winner.
