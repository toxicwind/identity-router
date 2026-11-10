"""Tests for identity_router.identity — the "who am I?" query path.

The identity file is a runtime parameter: tests point
``IDENTITY_ROUTER_IDENTITY`` at fixture markdown so no real agent file
is ever required.
"""
import json

import pytest

from identity_router import cli, identity
from identity_router.mcp_server import call_tool


FIXTURE = """# IDENTITY.md

- **Name:** Hatch
- **Character:** Chris's right hand and keeper of the long game
- **Vibe:** Warm, dry, direct
- **Emoji:** 🧊

## Autonomous continuation (2026-09-16, Chris)

Some posture text.

## Typo protocol (2026-09-16, Chris)

More posture text.

## Unrelated section

Not posture.
"""


@pytest.fixture()
def identity_file(tmp_path, monkeypatch):
    p = tmp_path / "IDENTITY.md"
    p.write_text(FIXTURE, encoding="utf-8")
    monkeypatch.setenv("IDENTITY_ROUTER_IDENTITY", str(p))
    return str(p)


# ---------------------------------------------------------------- parse

def test_parse_identity_fields():
    ident = identity.parse_identity(FIXTURE)
    assert ident["name"] == "Hatch"
    assert ident["character"] == "Chris's right hand and keeper of the long game"
    assert ident["vibe"] == "Warm, dry, direct"
    assert ident["emoji"] == "🧊"


def test_parse_identity_posture_sections():
    ident = identity.parse_identity(FIXTURE)
    assert any("Autonomous" in s for s in ident["_posture_sections"])
    assert any("Typo" in s for s in ident["_posture_sections"])
    assert not any("Unrelated" in s for s in ident["_posture_sections"])


def test_parse_identity_missing_fields_absent():
    ident = identity.parse_identity("# empty\n\nnothing here\n")
    assert ident.get("name") is None
    assert ident["_posture_sections"] == []


# ------------------------------------------------------------------ load

def test_load_identity_reads_env_path(identity_file):
    core = identity.load_identity()
    assert core["name"] == "Hatch"
    assert core["source"] == identity_file
    assert len(core["posture"]) == 2


def test_load_identity_missing_fields_become_unknown(tmp_path, monkeypatch):
    p = tmp_path / "IDENTITY.md"
    p.write_text("# empty\n", encoding="utf-8")
    monkeypatch.setenv("IDENTITY_ROUTER_IDENTITY", str(p))
    core = identity.load_identity()
    assert core["name"] == "?"
    assert core["emoji"] == "?"


def test_load_identity_missing_file_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("IDENTITY_ROUTER_IDENTITY", str(tmp_path / "nope.md"))
    with pytest.raises(FileNotFoundError):
        identity.load_identity()


# --------------------------------------------------------------- render

def test_render_identity_text(identity_file):
    out = identity.render_identity(identity.load_identity())
    assert out.startswith("🧊  Hatch")
    assert "character:" in out
    assert "posture:" in out


def test_identity_json_shape(identity_file):
    data = json.loads(identity.identity_json(identity.load_identity()))
    assert set(data) == {"name", "character", "vibe", "emoji", "posture", "source"}
    assert data["emoji"] == "🧊"


# ------------------------------------------------------------------ CLI

def test_cli_identity_json(identity_file, capsys):
    assert cli.identity_main(["--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["name"] == "Hatch"


def test_cli_identity_text(identity_file, capsys):
    assert cli.identity_main([]) == 0
    out = capsys.readouterr().out
    assert "Hatch" in out and "🧊" in out


def test_cli_identity_missing_file_exits_1(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("IDENTITY_ROUTER_IDENTITY", str(tmp_path / "nope.md"))
    assert cli.identity_main([]) == 1


# ------------------------------------------------------------------ MCP

def test_mcp_current_identity(identity_file):
    data = json.loads(call_tool("current_identity", {}))
    assert data["name"] == "Hatch"
    assert data["emoji"] == "🧊"


def test_mcp_route_lesson_recommends():
    text = call_tool("route_lesson", {"lesson": "headless chromium proxy quirk"})
    assert "~/TOOLS.md <-- recommended" in text


def test_mcp_route_lesson_rejects_empty():
    assert "error" in call_tool("route_lesson", {"lesson": "   "})


def test_mcp_standing_files_lists_ownership():
    from identity_router.route import OWNERSHIP
    data = json.loads(call_tool("standing_files", {}))
    assert set(data) == set(OWNERSHIP)


def test_mcp_unknown_tool_errors():
    assert "error" in call_tool("nope", {})
