"""Problem statement: problem.md"""

from __future__ import annotations

from collections.abc import Iterable


class Node:
    """Given node type - do not modify."""

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: Node | None = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


def from_iterable(values: Iterable[int]) -> Node | None:
    """Return the head of a list linking the values in order, or None when empty."""
    raise NotImplementedError  # TODO


def to_list(head: Node | None) -> list[int]:
    """Flatten a linked list into a Python list."""
    raise NotImplementedError  # TODO


def reverse(head: Node | None) -> Node | None:
    """Relink the nodes in reverse and return the new head. Do not allocate new nodes."""
    raise NotImplementedError  # TODO
