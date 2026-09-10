"""Grading tests for Week 01 / Python (easy)."""

from __future__ import annotations

import pytest

from . import solution
from .solution import Node


def build(values: list[int]) -> Node | None:
    """Build a list here rather than relying on the submitted from_iterable."""
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


def test_from_iterable_accepts_a_generator():
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


def test_reverse_does_not_allocate_new_nodes():
    head = build([1, 2, 3, 4])
    before = set(map(id, nodes_of(head)))
    after = set(map(id, nodes_of(solution.reverse(head))))
    assert after == before, "new nodes were allocated instead of relinking the existing ones"


def test_old_head_becomes_the_last_node():
    head = build([1, 2, 3])
    new_head = solution.reverse(head)
    assert new_head.value == 3
    assert head.next is None


def test_the_three_functions_compose():
    values = [5, 3, 8, 1]
    assert solution.to_list(solution.reverse(solution.from_iterable(values))) == values[::-1]


def test_long_input_does_not_blow_the_stack():
    values = list(range(100_000))
    head = solution.from_iterable(values)
    assert solution.to_list(solution.reverse(head)) == values[::-1]
