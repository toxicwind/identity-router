#!/usr/bin/env python3
"""Route a durable lesson to the right standing file.

Usage: bin/route.py "<lesson text>"
Scores the standing files by keyword overlap and prints a ranked
recommendation. The script scores; the agent decides.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from identity_router.cli import route_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(route_main())
