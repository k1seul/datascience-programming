"""Grading tests for Week 07 / Python (easy): Fibonacci."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from harness import within_seconds

from . import solution

SMALL = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
LARGE = {
    50: 12586269025,
    90: 2880067194370816120,
    100: 354224848179261915075,
    300: 222232244629420445529739893461909967206666939096499764990979600,
}

NAIVE_SMALL = [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177]


def quick(fn: Callable[[int], int], n: int) -> int:
    """Plain recursion takes years for these n; a remembered answer comes back at once."""
    too_slow = (
        f"{fn.__name__}({n}) 이 2초 안에 끝나지 않았습니다. "
        "한 번 구한 값을 기억해 두고 다시 쓰고 있나요?"
    )
    return within_seconds(2, lambda: fn(n), too_slow)


# --- (a) fib_memo ----------------------------------------------------------


@pytest.mark.parametrize(("n", "expected"), list(enumerate(SMALL)))
def test_fib_memo_small(n, expected):
    assert solution.fib_memo(n) == expected


@pytest.mark.parametrize(("n", "expected"), list(LARGE.items()))
def test_fib_memo_large(n, expected):
    assert quick(solution.fib_memo, n) == expected


def test_fib_memo_can_be_called_again():
    # A memo kept between calls must still give the right answer for a smaller n.
    assert quick(solution.fib_memo, 30) == 832040
    assert solution.fib_memo(10) == 55
    assert quick(solution.fib_memo, 31) == 1346269


# --- (b) fib_table ---------------------------------------------------------


@pytest.mark.parametrize(("n", "expected"), list(enumerate(SMALL)))
def test_fib_table_small(n, expected):
    assert solution.fib_table(n) == expected


@pytest.mark.parametrize(("n", "expected"), list(LARGE.items()))
def test_fib_table_large(n, expected):
    assert quick(solution.fib_table, n) == expected


def test_fib_table_goes_past_the_recursion_limit():
    """fib(5000) has 1045 digits. Recursion stops near depth 1000, a list does not."""
    try:
        value = quick(solution.fib_table, 5000)
    except RecursionError:
        pytest.fail(
            "RecursionError 가 났습니다. fib_table 은 재귀 없이 리스트를 앞에서부터 채워 주세요",
            pytrace=False,
        )
    assert len(str(value)) == 1045
    assert value % 10**9 == 382863125


def test_both_ways_agree():
    def first_mismatch() -> int | None:
        for n in range(0, 200):
            if solution.fib_table(n) != solution.fib_memo(n):
                return n
        return None

    too_slow = (
        "n = 0 부터 199 까지 두 함수를 비교하는 데 2초가 넘게 걸렸습니다. "
        "한 번 구한 값을 기억해 두고 다시 쓰고 있나요?"
    )
    n = within_seconds(2, first_mismatch, too_slow)
    assert n is None, f"n = {n} 에서 두 함수가 다릅니다"


# --- (c) naive_calls -------------------------------------------------------


@pytest.mark.parametrize(("n", "expected"), list(enumerate(NAIVE_SMALL)))
def test_naive_calls_small(n, expected):
    assert solution.naive_calls(n) == expected


def test_naive_calls_matches_a_real_count():
    calls = 0

    def fib(n: int) -> int:
        nonlocal calls
        calls += 1
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    for n in range(0, 16):
        calls = 0
        fib(n)
        assert solution.naive_calls(n) == calls, f"fib({n}) 은 실제로 {calls}번 호출됩니다"


def test_naive_calls_30():
    assert quick(solution.naive_calls, 30) == 2692537


def test_naive_calls_100():
    assert quick(solution.naive_calls, 100) == 1146295688027634168201
