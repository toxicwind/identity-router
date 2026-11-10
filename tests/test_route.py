"""Tests for identity_router.route — the lesson recommendation engine.

These exercise the scoring math, ranking behavior, and CLI surface.
Lessons below are parameters (arbitrary strings), never behavior baked
into the tool — the router stays universal.
"""
import json

import pytest

from identity_router import cli, route


# ---------------------------------------------------------------- tokens

def test_tokens_lowercases_and_strips_stopwords():
    toks = route.tokens("The Agent never ASKS Chris to close a Gap")
    assert "the" not in toks
    assert "to" not in toks
    assert toks == ["agent", "never", "asks", "chris", "close", "gap"]


def test_tokens_handles_punctuation_and_numbers():
    assert route.tokens("git-push, x2!") == ["git", "push", "x2"]
    toks = route.tokens("build v0.21.9 on 2026-09-17")
    assert "v0" in toks and "21" in toks


# ------------------------------------------------------------- scoring

def test_score_lesson_multi_word_keywords_weigh_more():
    score_multi, hits_multi = route.score_lesson(
        "this is my right hand rule", ["right hand", "hand"]
    )
    # "right hand" (2 tokens) outweighs "hand" (1 token) on the same lesson
    assert hits_multi["right hand"] > hits_multi["hand"]
    assert score_multi > 0


def test_score_lesson_phrase_bonus():
    _, with_phrase = route.score_lesson("never ask chris for anything", ["never ask"])
    _, no_phrase = route.score_lesson("never questioned or asked chris", ["never ask"])
    # exact substring presence adds the phrase bonus on top
    assert with_phrase["never ask"] > no_phrase.get("never ask", 0)


def test_score_lesson_zero_on_no_signal():
    score, hits = route.score_lesson("bananas orbit purple", ["shell", "git"])
    assert score == 0
    assert hits == {}


# ------------------------------------------------------------ recommend

@pytest.mark.parametrize(
    "lesson,expected",
    [
        # each canonical lesson should recommend its natural home
        ("Change my vibe to warmer and pick a new emoji", "IDENTITY.md"),
        ("Never ask before running an idempotent maintenance cleanup", "SOUL.md"),
        ("Meeting with Michelle Petersen Thursday 2026-09-18 12:00 MDT", "MEMORY.md"),
        ("Chris works in America/Denver timezone with terse bursts", "USER.md"),
        ("Push everything straight to main, never a shared clone checkout", "AGENTS.md"),
        ("Headless Chromium needs proxy_fwd on 127.0.0.1:3129", "TOOLS.md"),
        # obtuse-angle cases: the unexpected-but-correct routing wins
        ("Paper citation graphs belong in memory, not as throwaway notes", "MEMORY.md"),
        ("A standing rule is a node in a knowledge graph with edges", "MEMORY.md"),
    ],
)
def test_recommend_routes_to_expected_file(lesson, expected):
    ranked = route.recommend(lesson)
    top = ranked[0][1]
    assert top == expected, (
        f"lesson {lesson!r} routed to {top}, expected {expected}\n"
        + route.render_recommendation(lesson, ranked)
    )


def test_recommend_empty_lesson_raises():
    with pytest.raises(ValueError):
        route.recommend("")
    with pytest.raises(ValueError):
        route.recommend("   ")


def test_recommend_covers_all_six_files():
    ranked = route.recommend("anything at all")
    assert [f for _, f, _ in ranked] == sorted(route.FILE_KEYWORDS)


def test_recommend_ties_break_alphabetically():
    ranked = route.recommend(
        "zzz nothing relevant",
        file_keywords={"B.md": ["x"], "A.md": ["x"]},
    )
    assert [f for _, f, _ in ranked] == ["A.md", "B.md"]


def test_recommend_accepts_custom_corpus():
    ranked = route.recommend(
        "ship the docker image through the ci pipeline",
        file_keywords={"DEPLOY.md": ["docker", "ci", "pipeline"], "DOCS.md": ["markdown"]},
    )
    assert ranked[0][1] == "DEPLOY.md"


def test_recommend_is_deterministic():
    a = route.recommend("autonomy delegation trust typo protocol")
    b = route.recommend("autonomy delegation trust typo protocol")
    assert [(s, f) for s, f, _ in a] == [(s, f) for s, f, _ in b]


def test_recommend_second_place_is_sensible():
    # "never ask" appears in both SOUL.md and AGENTS.md; SOUL's density wins
    ranked = route.recommend("Never ask Chris a question that tools can answer")
    files = [f for _, f, _ in ranked]
    assert files[0] == "SOUL.md"
    assert "AGENTS.md" in files[1:3]


# ------------------------------------------------------------- render

def test_render_marks_recommendation():
    ranked = route.recommend("update the typo protocol for chris")
    out = route.render_recommendation("update the typo protocol for chris", ranked)
    assert "<-- recommended" in out
    assert out.splitlines()[0] == "lesson: update the typo protocol for chris"


def test_render_no_signal_message():
    ranked = [(0, "A.md", {}), (0, "B.md", {})]
    out = route.render_recommendation("zzz", ranked)
    assert "no keyword signal" in out


# ------------------------------------------------------------------ CLI

def test_cli_route_missing_lesson_exits_2(capsys):
    assert cli.route_main([]) == 2
    assert cli.route_main(["   "]) == 2


def test_cli_route_files_lists_ownership(capsys):
    assert cli.route_main(["--files"]) == 0
    out = capsys.readouterr().out
    for fname in route.FILE_KEYWORDS:
        assert f"~/{fname}" in out


def test_cli_route_json_is_parseable(capsys):
    assert cli.route_main(["--json", "new vibe: colder"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert isinstance(data, list)
    assert data[0]["file"].endswith(".md")
    assert data[0]["score"] >= 0
    assert "matched_keywords" in data[0]


def test_cli_route_text_output(capsys):
    assert cli.route_main(["chromium headless proxy quirk on this machine"]) == 0
    out = capsys.readouterr().out
    assert "~/TOOLS.md <-- recommended" in out
