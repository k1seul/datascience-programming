"""Problem statement: problem.md"""
# hello!

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
    head: Node | None = None
    tail: Node | None = None
    for value in values:
        node = Node(value)
        if tail is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def to_list(head: Node | None) -> list[int]:
    """Flatten a linked list into a Python list."""
    values: list[int] = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values


def reverse(head: Node | None) -> Node | None:
    """Relink the nodes in reverse and return the new head. Do not allocate new nodes."""
    prev: Node | None = None
    while head is not None:
        # Remember the rest of the list before overwriting the link we are standing on.
        following = head.next
        head.next = prev
        prev = head
        head = following
    return prev
