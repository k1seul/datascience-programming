"""Grading tests for Week 01 / Python (medium)."""

from __future__ import annotations

import pytest

from . import solution
from .solution import Node


def build(values: list[int], cycle_at: int | None = None) -> tuple[Node | None, Node | None]:
    """Build a list and return (head, node where the cycle starts).

    cycle_at None means no cycle; otherwise the tail is linked back to that index.
    """
    nodes = [Node(value) for value in values]
    for left, right in zip(nodes, nodes[1:], strict=False):
        left.next = right
    if cycle_at is None or not nodes:
        return (nodes[0] if nodes else None), None
    start = nodes[cycle_at]
    nodes[-1].next = start
    return nodes[0], start


@pytest.mark.parametrize("values", [[], [1], [1, 2, 3], list(range(50))])
def test_returns_none_without_a_cycle(values):
    head, _ = build(values)
    assert solution.detect_cycle(head) is None
    assert solution.cycle_length(head) == 0


@pytest.mark.parametrize("cycle_at", [0, 1, 2, 3])
def test_finds_the_node_where_the_cycle_starts(cycle_at):
    head, start = build([10, 20, 30, 40], cycle_at=cycle_at)
    assert solution.detect_cycle(head) is start


@pytest.mark.parametrize(
    ("cycle_at", "expected"),
    [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1)],
)
def test_cycle_length(cycle_at, expected):
    head, _ = build([1, 2, 3, 4, 5], cycle_at=cycle_at)
    assert solution.cycle_length(head) == expected


def test_single_node_pointing_at_itself():
    head, start = build([7], cycle_at=0)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 1


def test_whole_list_is_the_cycle():
    head, start = build([1, 2, 3, 4], cycle_at=0)
    assert solution.detect_cycle(head) is head
    assert start is head


def test_only_the_tail_points_at_itself():
    head, start = build([1, 2, 3], cycle_at=2)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 1


def test_identity_not_value_decides():
    head, start = build([1, 1, 1, 1], cycle_at=2)
    assert solution.detect_cycle(head) is start


def test_long_tail_with_a_short_cycle():
    head, start = build(list(range(1000)), cycle_at=997)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 3


def test_no_visited_set(monkeypatch):
    """Best-effort check of the constant-memory rule.

    Shadows set/dict inside the solution module, which catches the common
    `seen = set()` shape. Literals such as `{}` or set comprehensions slip through;
    problem.md remains the authority on the rule.
    """

    def banned(*args, **kwargs):
        raise AssertionError(
            "solve this in constant memory with slow/fast pointers, not a visited set"
        )

    monkeypatch.setattr(solution, "set", banned, raising=False)
    monkeypatch.setattr(solution, "dict", banned, raising=False)

    head, start = build([1, 2, 3, 4, 5], cycle_at=1)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 4
