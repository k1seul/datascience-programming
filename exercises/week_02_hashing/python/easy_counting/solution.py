"""Problem statement: problem.md"""

from __future__ import annotations

from collections.abc import Iterable


def count_values(values: Iterable[int]) -> dict[int, int]:
    """How many times each value appears, keyed by the value."""
    raise NotImplementedError


def first_unique(text: str) -> str | None:
    """The first character that appears exactly once, or None when there is none."""
    raise NotImplementedError


def is_anagram(left: str, right: str) -> bool:
    """Whether both strings use the same characters the same number of times."""
    raise NotImplementedError
