"""Problem statement: problem.md"""

from __future__ import annotations

from collections.abc import Sequence


def can_sell_all(holdings: Sequence[int], days: int, limit: int) -> bool:
    """Whether a daily cap of `limit` shares per account clears everything within days."""
    raise NotImplementedError


def min_daily_limit(holdings: Sequence[int], days: int) -> int:
    """The smallest daily cap that still clears everything within days.

    Must decide with can_sell_all; the grader counts how often it is called.
    """
    raise NotImplementedError
