"""Grading tests for Week 03 / C++ (medium)."""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def merge_sort():
    lib = native_lib(SRC)

    def call(values: list[int], capacity: int | None = None) -> list[int]:
        return list_out_call(lib.merge_sort, values, capacity=capacity)

    return call


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([3], [3]),
        ([2, 1], [1, 2]),
        ([1, 2], [1, 2]),
        ([5, 2, 9, 1, 5, 6], [1, 2, 5, 5, 6, 9]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([7, 7, 7], [7, 7, 7]),
        ([0, -1, 3, -2], [-2, -1, 0, 3]),
        ([-5, -5, -1, -9], [-9, -5, -5, -1]),
        ([10, 1, 10, 1], [1, 1, 10, 10]),
        ([4, 1, 3, 9, 7], [1, 3, 4, 7, 9]),
        ([2, 8, 5, 3, 9, 4, 1, 7, 6], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ],
)
def test_basic_cases(merge_sort, values, expected):
    assert merge_sort(values) == expected


def test_odd_and_even_lengths_both_work(merge_sort):
    assert merge_sort([3, 1, 2]) == [1, 2, 3]
    assert merge_sort([4, 3, 1, 2]) == [1, 2, 3, 4]


def test_input_is_not_modified(merge_sort):
    lib = native_lib(SRC)
    values = [5, 2, 9, 1]
    buf = (ctypes.c_int * 4)(*values)
    out = (ctypes.c_int * 4)()
    lib.merge_sort.argtypes = [
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
    ]
    lib.merge_sort.restype = ctypes.c_int
    lib.merge_sort(buf, 4, out, 4)
    assert list(buf) == values, "const 인 입력 배열을 바꿨습니다"


def test_reports_error_when_capacity_is_too_small(merge_sort):
    with pytest.raises(ValueError):
        merge_sort([3, 1, 2], capacity=2)


def test_exact_capacity_is_enough(merge_sort):
    assert merge_sort([3, 1, 2], capacity=3) == [1, 2, 3]


def test_standard_sort_is_not_used():
    """The point of this task is writing merge sort, not calling a library sort."""
    source = SRC.read_text(encoding="utf-8")
    for banned in ("std::sort", "std::stable_sort", "qsort", "std::partial_sort"):
        assert banned not in source, f"{banned} 대신 머지 소트를 직접 구현해 주세요"
