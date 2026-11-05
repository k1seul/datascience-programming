"""Problem statement: problem.md"""

from __future__ import annotations

from collections.abc import Collection, Sequence


def count_ways(n: int, jumps: Sequence[int], broken: Collection[int] = ()) -> int:
    """Ways to get from stone 0 to stone n, jumping by one of jumps each time and
    never landing on a broken stone."""
    raise NotImplementedError


def min_cost(cost: Sequence[int], jumps: Sequence[int], broken: Collection[int] = ()) -> int:
    """Smallest total cost of the stones landed on from stone 0 to the last stone.

    -1 when the last stone cannot be reached.
    """
    raise NotImplementedError
