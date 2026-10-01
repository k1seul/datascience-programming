"""Grading tests for Week 03 / Python (easy)."""

from __future__ import annotations

import copy

import pytest

from . import solution


@pytest.mark.parametrize(
    ("nested", "expected"),
    [
        ([], []),
        ([1], [1]),
        ([1, 2, 3], [1, 2, 3]),
        ([[1], [2]], [1, 2]),
        ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
        ([[1, 2], [3], 4], [1, 2, 3, 4]),
        ([[], [[]]], []),
        ([[[[5]]]], [5]),
        ([1, [], 2], [1, 2]),
        ([[1, [2]], 3, [[4], 5]], [1, 2, 3, 4, 5]),
        ([0, [-1, [-2]]], [0, -1, -2]),
    ],
)
def test_flatten(nested, expected):
    assert solution.flatten(nested) == expected


def test_flatten_keeps_the_original_order():
    assert solution.flatten([[3, 1], [2], [[5, 4]]]) == [3, 1, 2, 5, 4]


def test_flatten_does_not_modify_the_input():
    nested = [1, [2, [3]], 4]
    before = copy.deepcopy(nested)
    solution.flatten(nested)
    assert nested == before, "입력 리스트를 바꿨습니다"


def test_flatten_returns_a_new_list():
    nested = [1, 2, 3]
    assert solution.flatten(nested) is not nested


@pytest.mark.parametrize(
    ("nested", "expected"),
    [
        ([], 1),
        ([1, 2], 1),
        ([1, [2]], 2),
        ([[], []], 2),
        ([1, [2, [3]]], 3),
        ([1, [2, [3, [4]]]], 4),
        ([[1], [[2]]], 3),
        ([[[[5]]]], 4),
        ([[], [[]]], 3),
        ([1, [2], [[3]], [[[4]]]], 4),
    ],
)
def test_depth(nested, expected):
    assert solution.depth(nested) == expected


def test_depth_takes_the_deepest_branch():
    # 왼쪽 가지는 2겹, 오른쪽 가지는 4겹
    assert solution.depth([[1], [[[2]]]]) == 4


def test_depth_does_not_modify_the_input():
    nested = [1, [2, [3]]]
    before = copy.deepcopy(nested)
    solution.depth(nested)
    assert nested == before, "입력 리스트를 바꿨습니다"
