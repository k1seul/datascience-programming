"""Grading tests for Week 07 / C (easy): tiling a 2 x n board."""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib, within_seconds

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

TILING = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
WITH_SQUARE = [1, 1, 3, 5, 11, 21, 43, 85, 171, 341, 683]

# From n = 46 (tiling) and n = 32 (with squares) the counts no longer fit in an int.
TILING_LARGE = {50: 20365011074, 80: 37889062373143906, 90: 4660046610375530309}
WITH_SQUARE_LARGE = {40: 733007751851, 60: 768614336404564651}


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    for name in ("tiling", "tiling_with_square"):
        fn = getattr(lib, name)
        fn.argtypes = [ctypes.c_int]
        fn.restype = ctypes.c_longlong
    return lib


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


@pytest.fixture
def lib():
    return _bind(native_lib(SRC))


def quick(fn, n: int) -> int:
    """Plain recursion takes years for these n; a filled table answers at once."""
    too_slow = (
        f"{fn.__name__}({n}) 이 2초 안에 끝나지 않았습니다. "
        "재귀로만 풀면 n 이 커질 때 끝나지 않습니다. 배열을 앞에서부터 채워 보세요"
    )
    return checked(within_seconds(2, lambda: fn(n), too_slow))


def overflow_hint(n: int, got: int, expected: int) -> str:
    return f"n = {n} 에서 {got} 이 나왔습니다 (정답 {expected}). int 로 계산하다 넘치지 않았나요?"


# --- (a) tiling ------------------------------------------------------------


@pytest.mark.parametrize(("n", "expected"), list(enumerate(TILING)))
def test_tiling_small(lib, n, expected):
    assert checked(lib.tiling(n)) == expected


@pytest.mark.parametrize(("n", "expected"), list(TILING_LARGE.items()))
def test_tiling_large(lib, n, expected):
    got = quick(lib.tiling, n)
    assert got == expected, overflow_hint(n, got, expected)


@pytest.mark.parametrize("n", [-1, -5, 91, 100])
def test_tiling_out_of_range(lib, n):
    assert checked(lib.tiling(n)) == -1


# --- (b) tiling_with_square ------------------------------------------------


@pytest.mark.parametrize(("n", "expected"), list(enumerate(WITH_SQUARE)))
def test_with_square_small(lib, n, expected):
    assert checked(lib.tiling_with_square(n)) == expected


@pytest.mark.parametrize(("n", "expected"), list(WITH_SQUARE_LARGE.items()))
def test_with_square_large(lib, n, expected):
    got = quick(lib.tiling_with_square, n)
    assert got == expected, overflow_hint(n, got, expected)


@pytest.mark.parametrize("n", [-1, 61, 90])
def test_with_square_out_of_range(lib, n):
    assert checked(lib.tiling_with_square(n)) == -1
