"""Week 01 / Python (쉬움) 채점 테스트."""

from __future__ import annotations

import pytest

from . import solution
from .solution import Node


def build(values: list[int]) -> Node | None:
    """학습자의 from_iterable 에 기대지 않고 테스트가 직접 리스트를 만든다."""
    head: Node | None = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def walk(head: Node | None) -> list[int]:
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values


def nodes_of(head: Node | None) -> list[Node]:
    result = []
    while head is not None:
        result.append(head)
        head = head.next
    return result


@pytest.mark.parametrize("values", [[], [1], [1, 2], [3, 1, 4, 1, 5, 9]])
def test_from_iterable(values):
    assert walk(solution.from_iterable(values)) == values


def test_from_iterable_은_제너레이터도_받는다():
    assert walk(solution.from_iterable(x * x for x in range(4))) == [0, 1, 4, 9]


@pytest.mark.parametrize("values", [[], [1], [1, 2], [3, 1, 4, 1, 5, 9]])
def test_to_list(values):
    assert solution.to_list(build(values)) == values


@pytest.mark.parametrize(
    ("values", "expected"),
    [([], []), ([1], [1]), ([1, 2], [2, 1]), ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])],
)
def test_reverse(values, expected):
    assert walk(solution.reverse(build(values))) == expected


def test_reverse_는_새_노드를_만들지_않는다():
    head = build([1, 2, 3, 4])
    before = set(map(id, nodes_of(head)))
    after = set(map(id, nodes_of(solution.reverse(head))))
    assert after == before, "기존 노드의 링크를 다시 잇는 대신 새 노드를 만들었습니다"


def test_reverse_후_원래_머리는_마지막_노드가_된다():
    head = build([1, 2, 3])
    new_head = solution.reverse(head)
    assert new_head.value == 3
    assert head.next is None


def test_세_함수를_이어_써도_맞는다():
    values = [5, 3, 8, 1]
    assert solution.to_list(solution.reverse(solution.from_iterable(values))) == values[::-1]


def test_긴_입력에서도_재귀로_터지지_않는다():
    values = list(range(100_000))
    head = solution.from_iterable(values)
    assert solution.to_list(solution.reverse(head)) == values[::-1]
