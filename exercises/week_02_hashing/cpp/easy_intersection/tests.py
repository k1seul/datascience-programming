"""Grading tests for Week 02 / C++ (easy)."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def intersection():
    lib = native_lib(SRC)

    def call(a: list[int], b: list[int], capacity: int | None = None) -> list[int]:
        # The order is up to the implementation, so compare as a sorted list.
        return sorted(list_out_call(lib.intersection, a, b, capacity=capacity))

    return call


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 2, 2, 1], [2, 2], [2]),
        ([4, 9, 5], [9, 4, 9, 8], [4, 9]),
        ([1, 2, 3], [4, 5], []),
        ([], [1, 2], []),
        ([1, 2], [], []),
        ([], [], []),
        ([7], [7], [7]),
        ([-3, 0, 3], [3, 0, -3], [-3, 0, 3]),
    ],
)
def test_basic_cases(intersection, a, b, expected):
    assert intersection(a, b) == expected


def test_each_value_appears_once(intersection):
    assert intersection([5, 5, 5, 5], [5, 5, 5]) == [5]


def test_handles_negatives_and_large_values(intersection):
    a = [-1_000_000, 0, 1_000_000]
    b = [1_000_000, -1_000_000]
    assert intersection(a, b) == [-1_000_000, 1_000_000]


def test_reports_error_when_capacity_is_too_small(intersection):
    with pytest.raises(ValueError):
        intersection([1, 2, 3], [1, 2, 3], capacity=2)


def test_exact_capacity_is_enough(intersection):
    assert intersection([1, 2, 3], [1, 2, 3], capacity=3) == [1, 2, 3]


def test_matches_reference_on_random_input(intersection):
    rng = random.Random(3)
    for _ in range(60):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 40))]
        b = [rng.randint(-20, 20) for _ in range(rng.randint(0, 40))]
        assert intersection(a, b) == sorted(set(a) & set(b))
