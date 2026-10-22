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

A = [100, 200, 200, 200, 500]
B = [10, 20, 30]
C = [7]
D: list[int] = []
E = [5, 5, 5, 5]


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.find_trade.argtypes = [INT_P, ctypes.c_int, ctypes.c_int]
    lib.find_trade.restype = ctypes.c_int
    lib.first_at_or_after.argtypes = [INT_P, ctypes.c_int, ctypes.c_int]
    lib.first_at_or_after.restype = ctypes.c_int
    lib.first_after.argtypes = [INT_P, ctypes.c_int, ctypes.c_int]
    lib.first_after.restype = ctypes.c_int
    lib.count_in_range.argtypes = [INT_P, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    lib.count_in_range.restype = ctypes.c_int
    return lib


def buffer(values: list[int]) -> ctypes.Array:
    return (ctypes.c_int * max(len(values), 1))(*values)


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def find_trade(self, ts: list[int], t: int) -> int:
        return self._lib.find_trade(buffer(ts), len(ts), t)

    def first_at_or_after(self, ts: list[int], t: int) -> int:
        return self._lib.first_at_or_after(buffer(ts), len(ts), t)

    def first_after(self, ts: list[int], t: int) -> int:
        return self._lib.first_after(buffer(ts), len(ts), t)

    def count_in_range(self, ts: list[int], lo: int, hi: int) -> int:
        return self._lib.count_in_range(buffer(ts), len(ts), lo, hi)


@pytest.fixture
def api():
    lib = _bind(native_lib(SRC))
    # An empty log has nothing at or after anything, so the answer is 0.
    # An untouched stub returns the sentinel, which marks the task "not written yet".
    if lib.first_at_or_after(buffer(D), 0, 0) == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return Api(lib)


# --- find_trade ------------------------------------------------------------


@pytest.mark.parametrize(
    ("ts", "t"),
    [(A, 100), (A, 200), (A, 500), (B, 10), (B, 20), (B, 30), (C, 7), (E, 5)],
)
def test_find_trade_lands_on_a_matching_timestamp(api, ts, t):
    index = api.find_trade(ts, t)
    assert 0 <= index < len(ts), f"인덱스 {index} 가 범위를 벗어났습니다"
    assert ts[index] == t


@pytest.mark.parametrize(
    ("ts", "t"),
    [(A, 0), (A, 150), (A, 300), (A, 600), (B, 15), (C, 1), (C, 8), (D, 0), (E, 4), (E, 6)],
)
def test_find_trade_returns_minus_one_when_absent(api, ts, t):
    assert api.find_trade(ts, t) == -1


# --- first_at_or_after -----------------------------------------------------


@pytest.mark.parametrize(
    ("ts", "t", "expected"),
    [
        (A, 0, 0),
        (A, 100, 0),
        (A, 150, 1),
        (A, 200, 1),
        (A, 300, 4),
        (A, 500, 4),
        (A, 600, 5),
        (B, 15, 1),
        (B, 20, 1),
        (B, 31, 3),
        (C, 1, 0),
        (C, 7, 0),
        (C, 8, 1),
        (D, 0, 0),
        (E, 4, 0),
        (E, 5, 0),
        (E, 6, 4),
    ],
)
def test_first_at_or_after(api, ts, t, expected):
    assert api.first_at_or_after(ts, t) == expected


# --- first_after -----------------------------------------------------------


@pytest.mark.parametrize(
    ("ts", "t", "expected"),
    [
        (A, 0, 0),
        (A, 100, 1),
        (A, 150, 1),
        (A, 200, 4),
        (A, 300, 4),
        (A, 500, 5),
        (A, 600, 5),
        (B, 15, 1),
        (B, 20, 2),
        (B, 30, 3),
        (C, 1, 0),
        (C, 7, 1),
        (D, 0, 0),
        (E, 4, 0),
        (E, 5, 4),
    ],
)
def test_first_after(api, ts, t, expected):
    assert api.first_after(ts, t) == expected


def test_the_two_bounds_differ_by_the_number_of_matches(api):
    for t in (0, 100, 150, 200, 300, 500, 600):
        matches = sum(1 for v in A if v == t)
        assert api.first_after(A, t) - api.first_at_or_after(A, t) == matches


# --- count_in_range --------------------------------------------------------


@pytest.mark.parametrize(
    ("ts", "lo", "hi", "expected"),
    [
        (A, 200, 200, 3),
        (A, 100, 200, 4),
        (A, 100, 500, 5),
        (A, 150, 450, 3),
        (A, 0, 50, 0),
        (A, 600, 700, 0),
        (A, 0, 1000, 5),
        (B, 10, 30, 3),
        (B, 21, 29, 0),
        (B, 20, 20, 1),
        (C, 7, 7, 1),
        (D, 0, 10, 0),
        (E, 5, 5, 4),
        (E, 0, 4, 0),
    ],
)
def test_count_in_range(api, ts, lo, hi, expected):
    assert api.count_in_range(ts, lo, hi) == expected


def test_count_in_range_returns_zero_when_lo_is_above_hi(api):
    assert api.count_in_range(A, 300, 200) == 0
    assert api.count_in_range(B, 30, 10) == 0


# --- 라이브러리 금지 -------------------------------------------------------


def test_bsearch_is_not_used():
    source = SRC.read_text(encoding="utf-8")
    assert not re.search(r"\bbsearch\s*\(", source), "bsearch 대신 직접 이진 탐색을 구현해 주세요"
