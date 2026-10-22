"""Grading tests for Week 05 / C++ (medium)."""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def quick_sort():
    lib = native_lib(SRC)

    def call(values: list[int], capacity: int | None = None) -> list[int]:
        return list_out_call(lib.quick_sort, values, capacity=capacity)

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
        ([3, 1, 2], [1, 2, 3]),
        ([4, 3, 1, 2], [1, 2, 3, 4]),
    ],
)
def test_basic_cases(quick_sort, values, expected):
    assert quick_sort(values) == expected


def test_already_sorted_input_still_works(quick_sort):
    # 첫 원소를 피벗으로 쓰면 가장 느려지는 입력입니다. 답은 맞아야 합니다.
    assert quick_sort([1, 2, 3, 4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]


def test_all_equal_values(quick_sort):
    assert quick_sort([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]


def test_input_is_not_modified(quick_sort):
    lib = native_lib(SRC)
    values = [5, 2, 9, 1]
    buf = (ctypes.c_int * 4)(*values)
    out = (ctypes.c_int * 4)()
    lib.quick_sort.argtypes = [
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
    ]
    lib.quick_sort.restype = ctypes.c_int
    lib.quick_sort(buf, 4, out, 4)
    assert list(buf) == values, "const 인 입력 배열을 바꿨습니다"


def test_reports_error_when_capacity_is_too_small(quick_sort):
    with pytest.raises(ValueError):
        quick_sort([3, 1, 2], capacity=2)


def test_exact_capacity_is_enough(quick_sort):
    assert quick_sort([3, 1, 2], capacity=3) == [1, 2, 3]


def test_standard_sort_is_not_used():
    """The point of this task is writing quick sort, not calling a library sort."""
    source = SRC.read_text(encoding="utf-8")
    for banned in (
        "std::sort",
        "std::stable_sort",
        "std::nth_element",
        "std::partial_sort",
        "qsort",
    ):
        assert banned not in source, f"{banned} 대신 퀵 소트를 직접 구현해 주세요"
