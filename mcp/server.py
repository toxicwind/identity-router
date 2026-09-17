#!/usr/bin/env python3
"""identity-router MCP server (stdio, stdlib only).

Usage: mcp/server.py
See src/identity_router/mcp_server.py for the tool definitions.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from identity_router.mcp_server import main  # noqa: E402

if __name__ == "__main__":
    main()
