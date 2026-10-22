"""Grading tests for Week 05 / Python (medium)."""

from __future__ import annotations

import copy
import math

import pytest

from . import solution


def reference_days(holdings, limit):
    return sum(math.ceil(h / limit) for h in holdings)


# --- can_sell_all ----------------------------------------------------------


@pytest.mark.parametrize(
    ("holdings", "days", "limit", "expected"),
    [
        ([3, 6, 7, 11], 8, 4, True),
        ([3, 6, 7, 11], 8, 3, False),
        ([3, 6, 7, 11], 8, 5, True),
        ([5], 5, 1, True),
        ([5], 4, 1, False),
        ([30, 11, 23, 4, 20], 6, 23, True),
        ([30, 11, 23, 4, 20], 6, 22, False),
        ([30, 11, 23, 4, 20], 5, 30, True),
        ([1], 1, 1, True),
        ([10, 10], 4, 5, True),
        ([10, 10], 4, 4, False),
        ([7], 2, 4, True),
        ([7], 2, 3, False),
    ],
)
def test_can_sell_all(holdings, days, limit, expected):
    assert solution.can_sell_all(holdings, days, limit) is expected


@pytest.mark.parametrize("limit", [0, -1, -10])
def test_can_sell_all_rejects_a_non_positive_limit(limit):
    assert solution.can_sell_all([1, 2, 3], 10, limit) is False


def test_can_sell_all_matches_the_day_count():
    holdings = [3, 6, 7, 11]
    for limit in range(1, 12):
        needed = reference_days(holdings, limit)
        assert solution.can_sell_all(holdings, needed, limit) is True
        assert solution.can_sell_all(holdings, needed - 1, limit) is False


# --- min_daily_limit -------------------------------------------------------


@pytest.mark.parametrize(
    ("holdings", "days", "expected"),
    [
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([5], 5, 1),
        ([1], 1, 1),
        ([1000], 1, 1000),
        ([1, 1, 1], 3, 1),
        ([4, 4, 4], 3, 4),
        ([10, 10], 4, 5),
        ([7], 2, 4),
        ([100, 100, 100], 3, 100),
        ([2, 3], 5, 1),
    ],
)
def test_min_daily_limit(holdings, days, expected):
    assert solution.min_daily_limit(holdings, days) == expected


def test_the_answer_is_the_smallest_that_works():
    holdings, days = [3, 6, 7, 11], 8
    answer = solution.min_daily_limit(holdings, days)
    assert reference_days(holdings, answer) <= days, "이 한도로는 기한을 못 맞춥니다"
    assert reference_days(holdings, answer - 1) > days, "더 작은 한도로도 가능합니다"


def test_days_equal_to_the_account_count_needs_the_largest_account():
    assert solution.min_daily_limit([30, 11, 23, 4, 20], 5) == 30
    assert solution.min_daily_limit([8, 2], 2) == 8


def test_plenty_of_days_allows_the_smallest_limit():
    assert solution.min_daily_limit([5, 5], 10) == 1


# --- O(log) 인지 ----------------------------------------------------------


def test_search_is_logarithmic(monkeypatch):
    """can_sell_all 호출 횟수로 이진 탐색인지 확인합니다.

    한도 후보가 1~1000 이므로 이진 탐색이면 10여 번, 1부터 하나씩 올려 보면 수백 번입니다.
    """
    real = solution.can_sell_all
    calls = 0

    def counted(holdings, days, limit):
        nonlocal calls
        calls += 1
        return real(holdings, days, limit)

    monkeypatch.setattr(solution, "can_sell_all", counted)

    assert solution.min_daily_limit([1000, 500, 250], 6) == 334
    assert calls > 0, "min_daily_limit 이 can_sell_all 을 호출해야 합니다"
    assert calls <= 20, (
        f"can_sell_all 을 {calls}번 불렀습니다. "
        "한도를 하나씩 올려 보지 말고 이진 탐색으로 풀어 주세요"
    )


def test_input_is_not_modified():
    holdings = [3, 6, 7, 11]
    before = copy.deepcopy(holdings)
    solution.min_daily_limit(holdings, 8)
    solution.can_sell_all(holdings, 8, 4)
    assert holdings == before, "입력을 바꿨습니다"
