"""Console-script entry points for the identity-router CLI.

- ``identity-router`` / ``identity-router-route`` — score a lesson and
  print the ranked routing recommendation. The script scores; you decide.
- ``identity-router-identity`` — answer "what's my current identity?"

The router routes. It never polices.
"""
import argparse
import sys

from .identity import identity_json, load_identity, render_identity
from .route import OWNERSHIP, recommend, render_recommendation

from . import __version__


def route_main(argv=None):
    parser = argparse.ArgumentParser(
        prog="identity-router",
        description=(
            "Route a durable lesson to the right standing file. "
            "Scores keyword overlap and prints a ranked recommendation — "
            "the script scores, the agent decides."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("lesson", nargs="?", help="the durable lesson text to route")
    parser.add_argument(
        "--json", action="store_true",
        help="print the ranked recommendation as JSON instead of text",
    )
    parser.add_argument(
        "--files", action="store_true",
        help="print the ownership table (which file owns what) and exit",
    )
    args = parser.parse_args(argv)

    if args.files:
        for fname, owns in OWNERSHIP.items():
            print(f"~/{fname}\n    {owns}\n")
        return 0

    if not args.lesson or not args.lesson.strip():
        parser.print_usage(sys.stderr)
        print('identity-router "<lesson text>"  (or: identity-router --files)', file=sys.stderr)
        return 2

    ranked = recommend(args.lesson)
    if args.json:
        import json as _json
        print(
            _json.dumps(
                [
                    {
                        "score": s,
                        "file": f"~/{fname}",
                        "matched_keywords": sorted(hits, key=hits.get, reverse=True),
                    }
                    for s, fname, hits in ranked
                ],
                indent=2,
            )
        )
        return 0

    sys.stdout.write(render_recommendation(args.lesson, ranked))
    return 0


def identity_main(argv=None):
    parser = argparse.ArgumentParser(
        prog="identity-router-identity",
        description="Answer 'what's my current identity?' from ~/IDENTITY.md. Reports only.",
    )
    parser.add_argument("--json", action="store_true", help="print identity as JSON")
    args = parser.parse_args(argv)
    try:
        core = load_identity()
    except FileNotFoundError:
        print("no identity file found (set IDENTITY_ROUTER_IDENTITY to point at one)", file=sys.stderr)
        return 1
    sys.stdout.write(identity_json(core) + "\n" if args.json else render_identity(core))
    return 0


def main(argv=None):
    """Alias: ``identity-router`` is the route command."""
    return route_main(argv)
