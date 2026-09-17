#!/usr/bin/env python3
"""Hello, identity-router.

A 20-second tour: who am I, and where does this lesson belong?
Runs anywhere — uses the bundled example identity so it needs no
~/IDENTITY.md and no pip install.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from identity_router import recommend, render_recommendation  # noqa: E402
from identity_router.identity import load_identity, render_identity  # noqa: E402

os.environ.setdefault(
    "IDENTITY_ROUTER_IDENTITY",
    os.path.join(ROOT, "examples", "identity-example.md"),
)

print("== who am I? ==")
print(render_identity(load_identity()))

lesson = "Verify every claim against a tool result before reporting progress"
print("== where does this lesson belong? ==")
print(render_recommendation(lesson, recommend(lesson)))

print("== as data ==")
score, fname, hits = recommend(
    "Never store tokens in standing files; record where they live instead"
)[0]
print(json.dumps({"recommended": f"~/{fname}", "score": score}, indent=2))
print("\nThe router routes. It never polices. 🧊")
