"""identity-router — the universal knowledge router for durable agent memory.

The router routes. It never polices. No veto, no lecture, no
refusal-shaped behavior. If a lesson is real, it gets filed. Period.

Think emergently: slightly obtuse angles cause breakthroughs. The router
prefers the unexpected-but-correct routing over the obvious-but-shallow
one — a paper citation graph is a memory, a standing rule is a node in a
graph, the standing files are a knowledge base with edges.

Stdlib only — no third-party dependencies.
"""

from .identity import parse_identity
from .route import (
    FILE_KEYWORDS,
    OWNERSHIP,
    recommend,
    render_recommendation,
    score_lesson,
)

__version__ = "1.0.0"

__all__ = [
    "FILE_KEYWORDS",
    "OWNERSHIP",
    "parse_identity",
    "recommend",
    "render_recommendation",
    "score_lesson",
]
