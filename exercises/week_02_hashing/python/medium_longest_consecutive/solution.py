"""Problem statement: problem.md"""

from __future__ import annotations

from collections.abc import Sequence


def longest_consecutive(values: Sequence[int]) -> int:
    """Length of the longest run of consecutive integers, ignoring their positions."""
    raise NotImplementedError


def longest_consecutive_range(values: Sequence[int]) -> tuple[int, int] | None:
    """(start, end) of that run, lowest start on a tie, or None when the input is empty."""
    raise NotImplementedError
