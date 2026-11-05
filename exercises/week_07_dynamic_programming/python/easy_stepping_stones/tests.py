"""Grading tests for Week 07 / Python (easy): stepping stones."""

from __future__ import annotations

import copy

import pytest

from harness import within_seconds

from . import solution

TOO_SLOW = "{name} 이 2초 안에 끝나지 않았습니다. 돌마다 구한 답을 기억해 두고 다시 쓰고 있나요?"

# fib(301): every way to cross 300 stones with jumps of 1 and 2.
WAYS_300 = 359579325206583560961765665172189099052367214309267232255589801


# --- (a) count_ways --------------------------------------------------------


@pytest.mark.parametrize(
    ("n", "jumps", "broken", "expected"),
    [
        (4, (1, 2), (), 5),
        (4, (1, 2), {2}, 1),
        (5, (1, 3), (), 4),
        (10, (1, 2, 3), (), 274),
        (8, (2, 3), (), 4),
        (6, (2,), (), 1),
        (5, (2,), (), 0),
        (1, (2,), (), 0),
        (0, (1, 2), (), 1),
        (7, (1, 2), {3, 5}, 2),
        (7, (1, 2), {3, 4}, 0),
        (10, (1, 2), {5}, 25),
    ],
)
def test_count_ways(n, jumps, broken, expected):
    assert solution.count_ways(n, jumps, broken) == expected


def test_count_ways_without_broken_stones():
    assert solution.count_ways(4, (1, 2)) == 5


def test_count_ways_jump_order_does_not_matter():
    assert solution.count_ways(10, (3, 1, 2)) == 274


def test_count_ways_accepts_a_list_of_broken_stones():
    assert solution.count_ways(10, [1, 2], [5]) == 25


def test_count_ways_300_stones():
    too_slow = TOO_SLOW.format(name="count_ways(300, (1, 2))")
    assert within_seconds(2, lambda: solution.count_ways(300, (1, 2)), too_slow) == WAYS_300


# --- (b) min_cost ----------------------------------------------------------


@pytest.mark.parametrize(
    ("cost", "jumps", "broken", "expected"),
    [
        ([0, 5, 1, 7, 2], (1, 2), (), 3),
        ([0, 5, 1, 7, 2], (1, 2), {2}, 14),
        ([0, 10, 1, 1, 10, 1], (1, 2, 3), (), 2),
        ([0, 4, 4, 4], (1,), (), 12),
        ([0, 3, 2, 4], (2,), (), -1),
        ([0, 1, 1, 1], (1, 2), {1, 2}, -1),
        ([0], (1,), (), 0),
        ([0, 0, 0, 0], (1, 2), (), 0),
    ],
)
def test_min_cost(cost, jumps, broken, expected):
    assert solution.min_cost(cost, jumps, broken) == expected


def test_min_cost_without_broken_stones():
    assert solution.min_cost([0, 5, 1, 7, 2], (1, 2)) == 3


def test_min_cost_does_not_pay_for_the_first_stone():
    assert solution.min_cost([99, 1, 1], (1,)) == 2


def test_min_cost_300_stones():
    # Every stone costs 1, so the answer is the fewest landings to get 299 stones ahead.
    too_slow = TOO_SLOW.format(name="min_cost([1] * 300, (1, 2))")
    assert within_seconds(2, lambda: solution.min_cost([1] * 300, (1, 2)), too_slow) == 150


# --- 입력 -------------------------------------------------------------------


def test_inputs_are_not_modified():
    cost, jumps, broken = [0, 5, 1, 7, 2], [1, 2], {2}
    before = copy.deepcopy((cost, jumps, broken))
    solution.count_ways(4, jumps, broken)
    solution.min_cost(cost, jumps, broken)
    assert (cost, jumps, broken) == before, "입력을 바꿨습니다"
