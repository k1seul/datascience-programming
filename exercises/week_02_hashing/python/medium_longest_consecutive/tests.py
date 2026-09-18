"""Grading tests for Week 02 / Python (medium)."""

from __future__ import annotations

import random

import pytest

from . import solution


def reference(values: list[int]) -> tuple[int, int] | None:
    pool = set(values)
    best: tuple[int, int] | None = None
    best_length = 0
    for value in sorted(pool):
        if value - 1 in pool:
            continue
        end = value
        while end + 1 in pool:
            end += 1
        length = end - value + 1
        if length > best_length:
            best_length, best = length, (value, end)
    return best


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([5], 1),
        ([1, 1, 1], 1),
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([1, 2, 0, 1], 3),
        ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),
        ([-5, -4, -3], 3),
    ],
)
def test_longest_consecutive(values, expected):
    assert solution.longest_consecutive(values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], None),
        ([5], (5, 5)),
        ([100, 4, 200, 1, 3, 2], (1, 4)),
        ([-5, -4, -3], (-5, -3)),
        ([1, 1, 2], (1, 2)),
    ],
)
def test_longest_consecutive_range(values, expected):
    assert solution.longest_consecutive_range(values) == expected


def test_ties_pick_the_lowest_start():
    # 1-2 and 8-9 are both length 2; the answer starts at 1.
    assert solution.longest_consecutive_range([8, 9, 1, 2]) == (1, 2)


def test_duplicates_count_once():
    assert solution.longest_consecutive([3, 3, 3, 4, 4]) == 2


def test_matches_reference_on_random_input():
    rng = random.Random(7)
    for _ in range(60):
        values = [rng.randint(-15, 15) for _ in range(rng.randint(0, 50))]
        expected = reference(values)
        length = 0 if expected is None else expected[1] - expected[0] + 1
        assert solution.longest_consecutive_range(values) == expected
        assert solution.longest_consecutive(values) == length


def test_sorting_is_not_used(monkeypatch):
    """Best-effort check of the O(n) rule.

    Shadows sorted inside the solution module, which catches the usual sort-first shape.
    A `values.sort()` call on a list would slip through, but the input is a Sequence you
    are not meant to mutate.
    """

    def banned(*args, **kwargs):
        raise AssertionError("solve this in O(n) with a set, not by sorting")

    monkeypatch.setattr(solution, "sorted", banned, raising=False)

    assert solution.longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert solution.longest_consecutive_range([100, 4, 200, 1, 3, 2]) == (1, 4)


def test_large_input_needs_linear_time():
    # One long run plus noise: quadratic scanning would not finish inside the timeout.
    rng = random.Random(8)
    values = list(range(100_000))
    rng.shuffle(values)
    assert solution.longest_consecutive(values) == 100_000
