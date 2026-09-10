"""Grading tests for Week 01 / C++ (medium)."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def reverse_groups():
    lib = native_lib(SRC)

    def call(values: list[int], k: int, capacity: int | None = None) -> list[int]:
        return list_out_call(lib.reverse_groups, values, k, capacity=capacity)

    return call


def reference(values: list[int], k: int) -> list[int]:
    result: list[int] = []
    for start in range(0, len(values), k):
        chunk = values[start : start + k]
        result += reversed(chunk) if len(chunk) == k else chunk
    return result


@pytest.mark.parametrize(
    ("values", "k", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 5, [5, 4, 3, 2, 1]),
        ([1, 2, 3], 9, [1, 2, 3]),
        ([], 3, []),
        ([1], 1, [1]),
        ([1, 2, 3, 4], 2, [2, 1, 4, 3]),
    ],
)
def test_basic_cases(reverse_groups, values, k, expected):
    assert reverse_groups(values, k) == expected


@pytest.mark.parametrize("k", [0, -1, -7])
def test_k_below_one_is_an_error(reverse_groups, k):
    with pytest.raises(ValueError):
        reverse_groups([1, 2, 3], k)


def test_reports_error_when_capacity_is_too_small(reverse_groups):
    with pytest.raises(ValueError):
        reverse_groups([1, 2, 3, 4], 2, capacity=3)


def test_exact_capacity_is_enough(reverse_groups):
    assert reverse_groups([1, 2, 3, 4], 2, capacity=4) == [2, 1, 4, 3]


def test_matches_reference_on_random_input(reverse_groups):
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(0, 30)
        values = [rng.randint(-50, 50) for _ in range(n)]
        k = rng.randint(1, 8)
        assert reverse_groups(values, k) == reference(values, k)
