"""Grading tests for Week 01 / C++ (easy)."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def dedup():
    lib = native_lib(SRC)

    def call(values: list[int], capacity: int | None = None) -> list[int]:
        return list_out_call(lib.dedup_sorted, values, capacity=capacity)

    return call


def reference(values: list[int]) -> list[int]:
    result: list[int] = []
    for value in values:
        if not result or result[-1] != value:
            result.append(value)
    return result


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([1], [1]),
        ([1, 1], [1]),
        ([1, 1, 2, 3, 3, 3], [1, 2, 3]),
        ([2, 2, 2], [2]),
        ([1, 2, 3], [1, 2, 3]),
        ([-5, -5, 0, 0, 0, 7], [-5, 0, 7]),
    ],
)
def test_basic_cases(dedup, values, expected):
    assert dedup(values) == expected


def test_duplicates_at_the_end(dedup):
    assert dedup([1, 2, 3, 3, 3, 3]) == [1, 2, 3]


def test_duplicates_at_the_front(dedup):
    assert dedup([9, 9, 9, 9, 10]) == [9, 10]


def test_reports_error_when_capacity_is_too_small(dedup):
    with pytest.raises(ValueError):
        dedup([1, 1, 2, 3], capacity=2)


def test_exact_capacity_is_enough(dedup):
    assert dedup([1, 1, 2, 3], capacity=3) == [1, 2, 3]


def test_matches_reference_on_random_input(dedup):
    rng = random.Random(1)
    for _ in range(50):
        values = sorted(rng.choices(range(-10, 10), k=rng.randint(0, 40)))
        assert dedup(values) == reference(values)
