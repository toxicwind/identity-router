#!/usr/bin/env python3
"""Answer "what's my current identity?" from ~/IDENTITY.md.

Usage: bin/identity.py [--json]
Reports only — never edits, never polices.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from identity_router.cli import identity_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(identity_main())
