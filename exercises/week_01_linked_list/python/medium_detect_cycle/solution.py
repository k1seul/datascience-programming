"""문제 설명: problem.md"""

from __future__ import annotations


class Node:
    """주어진 노드 타입 — 고치지 않는다."""

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: Node | None = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        # 사이클이 있어도 안전하도록 next 는 찍지 않는다.
        return f"Node({self.value})"


def detect_cycle(head: Node | None) -> Node | None:
    """사이클이 시작되는 노드. 없으면 None."""
    raise NotImplementedError  # TODO


def cycle_length(head: Node | None) -> int:
    """사이클에 속한 노드 개수. 없으면 0."""
    raise NotImplementedError  # TODO
