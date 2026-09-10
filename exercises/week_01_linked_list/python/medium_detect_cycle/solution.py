"""Problem statement: problem.md"""

from __future__ import annotations


class Node:
    """Given node type - do not modify."""

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: Node | None = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        # Never print next, so that a cyclic list stays safe to repr.
        return f"Node({self.value})"


def detect_cycle(head: Node | None) -> Node | None:
    """Return the node where the cycle starts, or None when there is no cycle."""
    raise NotImplementedError


def cycle_length(head: Node | None) -> int:
    """Return the number of nodes in the cycle, or 0 when there is no cycle."""
    raise NotImplementedError
