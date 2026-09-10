"""문제 설명: problem.md"""

from __future__ import annotations

from collections.abc import Iterable


class Node:
    """주어진 노드 타입 — 고치지 않는다."""

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: Node | None = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


def from_iterable(values: Iterable[int]) -> Node | None:
    """값들을 순서대로 이은 리스트의 머리. 비어 있으면 None."""
    raise NotImplementedError  # TODO


def to_list(head: Node | None) -> list[int]:
    """연결 리스트를 파이썬 리스트로 펼친다."""
    raise NotImplementedError  # TODO


def reverse(head: Node | None) -> Node | None:
    """링크를 다시 이어 뒤집고 새 머리를 반환한다. 새 노드를 만들지 않는다."""
    raise NotImplementedError  # TODO
