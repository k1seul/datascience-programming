"""Grading tests for Week 02 / C++ (medium)."""

from __future__ import annotations

import ctypes
import random
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"

INT_P = ctypes.POINTER(ctypes.c_int)


@pytest.fixture
def subarray_sum():
    lib = native_lib(SRC)
    lib.subarray_sum.argtypes = [INT_P, ctypes.c_int, ctypes.c_int]
    lib.subarray_sum.restype = ctypes.c_int

    def call(values: list[int], k: int) -> int:
        buf = (ctypes.c_int * max(len(values), 1))(*values)
        result = lib.subarray_sum(buf, len(values), k)
        if result == NOT_IMPLEMENTED:
            raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
        return result

    return call


def reference(values: list[int], k: int) -> int:
    total = 0
    seen = {0: 1}
    running = 0
    for value in values:
        running += value
        total += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return total


@pytest.mark.parametrize(
    ("values", "k", "expected"),
    [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([], 0, 0),
        ([], 5, 0),
        ([5], 5, 1),
        ([5], 3, 0),
        ([0, 0, 0], 0, 6),
        ([-1, -1, 1], -2, 1),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ],
)
def test_basic_cases(subarray_sum, values, k, expected):
    assert subarray_sum(values, k) == expected


def test_counts_the_whole_array(subarray_sum):
    assert subarray_sum([2, 3, 5], 10) == 1


def test_negative_values_break_sliding_windows(subarray_sum):
    # A sliding window would miss these, because growing the window can lower the sum.
    assert subarray_sum([1, 2, -2, 2, 1], 3) == 4


def test_matches_reference_on_random_input(subarray_sum):
    rng = random.Random(4)
    for _ in range(60):
        values = [rng.randint(-5, 5) for _ in range(rng.randint(0, 60))]
        k = rng.randint(-8, 8)
        assert subarray_sum(values, k) == reference(values, k)


def test_large_input_needs_linear_time(subarray_sum):
    # One million elements. An O(n) answer finishes in milliseconds; checking every
    # subarray is roughly 5e11 steps, which the 20s per-test timeout stops long before.
    rng = random.Random(5)
    values = [rng.randint(-3, 3) for _ in range(1_000_000)]
    assert subarray_sum(values, 2) == reference(values, 2)
