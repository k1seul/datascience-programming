"""Grading tests for Week 05 / C (medium)."""

from __future__ import annotations

import ctypes
import re
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)

ODD = [1, 3, 5, 7, 9]
DUP = [1, 2, 2, 2, 5]
ONE = [4]
EMPTY: list[int] = []
SAME = [2, 2, 2, 2]


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    for name in ("binary_search", "lower_bound", "upper_bound", "count_equal"):
        fn = getattr(lib, name)
        fn.argtypes = [INT_P, ctypes.c_int, ctypes.c_int]
        fn.restype = ctypes.c_int
    return lib


def buffer(values: list[int]) -> ctypes.Array:
    return (ctypes.c_int * max(len(values), 1))(*values)


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def binary_search(self, values: list[int], target: int) -> int:
        return self._lib.binary_search(buffer(values), len(values), target)

    def lower_bound(self, values: list[int], target: int) -> int:
        return self._lib.lower_bound(buffer(values), len(values), target)

    def upper_bound(self, values: list[int], target: int) -> int:
        return self._lib.upper_bound(buffer(values), len(values), target)

    def count_equal(self, values: list[int], target: int) -> int:
        return self._lib.count_equal(buffer(values), len(values), target)


@pytest.fixture
def api():
    lib = _bind(native_lib(SRC))
    # An empty array has nothing at or after anything, so lower_bound is 0.
    # An untouched stub returns the sentinel, which marks the task "not written yet".
    if lib.lower_bound(buffer(EMPTY), 0, 0) == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return Api(lib)


# --- binary_search ---------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "target"),
    [
        (ODD, 1),
        (ODD, 5),
        (ODD, 9),
        (DUP, 1),
        (DUP, 2),
        (DUP, 5),
        (ONE, 4),
        (SAME, 2),
    ],
)
def test_binary_search_lands_on_a_matching_value(api, values, target):
    index = api.binary_search(values, target)
    assert 0 <= index < len(values), f"인덱스 {index} 가 범위를 벗어났습니다"
    assert values[index] == target


@pytest.mark.parametrize(
    ("values", "target"),
    [
        (ODD, 0),
        (ODD, 4),
        (ODD, 10),
        (DUP, 0),
        (DUP, 3),
        (DUP, 6),
        (ONE, 3),
        (ONE, 5),
        (EMPTY, 0),
        (SAME, 1),
        (SAME, 3),
    ],
)
def test_binary_search_returns_minus_one_when_absent(api, values, target):
    assert api.binary_search(values, target) == -1


# --- lower_bound -----------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "target", "expected"),
    [
        (ODD, 0, 0),
        (ODD, 1, 0),
        (ODD, 4, 2),
        (ODD, 5, 2),
        (ODD, 9, 4),
        (ODD, 10, 5),
        (DUP, 0, 0),
        (DUP, 1, 0),
        (DUP, 2, 1),
        (DUP, 3, 4),
        (DUP, 5, 4),
        (DUP, 6, 5),
        (ONE, 3, 0),
        (ONE, 4, 0),
        (ONE, 5, 1),
        (EMPTY, 0, 0),
        (SAME, 1, 0),
        (SAME, 2, 0),
        (SAME, 3, 4),
    ],
)
def test_lower_bound(api, values, target, expected):
    assert api.lower_bound(values, target) == expected


# --- upper_bound -----------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "target", "expected"),
    [
        (ODD, 0, 0),
        (ODD, 1, 1),
        (ODD, 4, 2),
        (ODD, 5, 3),
        (ODD, 9, 5),
        (ODD, 10, 5),
        (DUP, 0, 0),
        (DUP, 1, 1),
        (DUP, 2, 4),
        (DUP, 3, 4),
        (DUP, 5, 5),
        (DUP, 6, 5),
        (ONE, 3, 0),
        (ONE, 4, 1),
        (ONE, 5, 1),
        (EMPTY, 0, 0),
        (SAME, 1, 0),
        (SAME, 2, 4),
        (SAME, 3, 4),
    ],
)
def test_upper_bound(api, values, target, expected):
    assert api.upper_bound(values, target) == expected


def test_bounds_return_n_when_every_value_is_smaller(api):
    assert api.lower_bound(DUP, 6) == len(DUP)
    assert api.upper_bound(DUP, 6) == len(DUP)
    assert api.lower_bound(ONE, 5) == len(ONE)


# --- count_equal -----------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "target", "expected"),
    [
        (ODD, 5, 1),
        (ODD, 1, 1),
        (ODD, 9, 1),
        (ODD, 4, 0),
        (ODD, 0, 0),
        (ODD, 10, 0),
        (DUP, 2, 3),
        (DUP, 1, 1),
        (DUP, 5, 1),
        (DUP, 3, 0),
        (DUP, 0, 0),
        (DUP, 6, 0),
        (ONE, 4, 1),
        (ONE, 3, 0),
        (EMPTY, 0, 0),
        (SAME, 2, 4),
        (SAME, 1, 0),
        (SAME, 3, 0),
    ],
)
def test_count_equal(api, values, target, expected):
    assert api.count_equal(values, target) == expected


def test_count_equal_is_the_gap_between_the_two_bounds(api):
    for values in (ODD, DUP, ONE, SAME):
        for target in range(0, 11):
            gap = api.upper_bound(values, target) - api.lower_bound(values, target)
            assert api.count_equal(values, target) == gap


# --- 라이브러리 금지 -------------------------------------------------------


def test_bsearch_is_not_used():
    source = SRC.read_text(encoding="utf-8")
    assert not re.search(r"\bbsearch\s*\(", source), "bsearch 대신 직접 이진 탐색을 구현해 주세요"
