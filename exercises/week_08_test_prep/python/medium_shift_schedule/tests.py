"""Grading tests for Week 08 / Python (medium): part-time shift schedule.

work_days may return any best schedule, so its tests check the schedule itself: days in
range, ascending, never three in a row, and worth max_pay.
"""

from __future__ import annotations

import copy
from collections.abc import Sequence

import pytest

from harness import within_seconds

from . import solution

# 500 days: trying every schedule means 2^500 of them.
BIG = [(i * 53 + 17) % 97 for i in range(500)]
BIG_BEST = 19114

TOO_SLOW = (
    "{name} 이 2초 안에 끝나지 않았습니다. 날짜마다 구한 답을 표에 적어 두고 다시 쓰고 있나요?"
)

CASES = [
    ([3, 2, 5, 10, 7], 22),
    ([1, 2, 3], 5),
    ([10, 10, 1, 10, 10], 40),
    ([100, 1, 1, 100], 201),
    ([4, 7, 2, 9, 3, 8, 6], 34),
    ([6, 7, 1, 30, 8, 2, 4], 55),
    ([5, 5, 5, 5], 15),
    ([1, 1], 2),
    ([7], 7),
    ([0, 0, 0], 0),
    ([], 0),
]


def check_schedule(pay: Sequence[int], days: object, best: int) -> None:
    assert isinstance(days, list), f"리스트를 반환해 주세요. 받은 값: {days!r}"
    in_range = all(isinstance(d, int) and 0 <= d < len(pay) for d in days)
    assert in_range, f"없는 날이 있습니다: {days}"
    assert days == sorted(set(days)), f"날짜는 겹치지 않게 오름차순으로 적어 주세요: {days}"
    worked = set(days)
    for d in days:
        assert not {d + 1, d + 2} <= worked, f"{d}, {d + 1}, {d + 2}일 사흘을 연달아 일합니다"
    earned = sum(pay[d] for d in days)
    short = f"{days} 로 버는 돈은 {earned} 입니다. 가장 많이 벌 수 있는 돈은 {best} 입니다"
    assert earned == best, short


# --- (a) max_pay -----------------------------------------------------------


@pytest.mark.parametrize(("pay", "best"), CASES)
def test_max_pay(pay, best):
    assert solution.max_pay(pay) == best


def test_max_pay_beats_every_other_day():
    # Working every other day earns 3 + 5 + 7 = 15; two days on, one off earns more.
    assert solution.max_pay([3, 2, 5, 10, 7]) == 22


def test_max_pay_500_days():
    too_slow = TOO_SLOW.format(name="max_pay (500일)")
    assert within_seconds(2, lambda: solution.max_pay(BIG), too_slow) == BIG_BEST


# --- (b) work_days ---------------------------------------------------------


@pytest.mark.parametrize(("pay", "best"), CASES)
def test_work_days(pay, best):
    check_schedule(pay, solution.work_days(pay), best)


def test_work_days_the_example():
    # Only one schedule earns 22 here, so the answer is fixed.
    assert solution.work_days([3, 2, 5, 10, 7]) == [0, 1, 3, 4]


def test_work_days_nothing_to_earn():
    assert solution.work_days([]) == []


def test_work_days_500_days():
    too_slow = TOO_SLOW.format(name="work_days (500일)")
    days = within_seconds(2, lambda: solution.work_days(BIG), too_slow)
    check_schedule(BIG, days, BIG_BEST)


# --- 입력 -------------------------------------------------------------------


def test_input_is_not_modified():
    pay = [3, 2, 5, 10, 7]
    before = copy.deepcopy(pay)
    solution.max_pay(pay)
    solution.work_days(pay)
    assert pay == before, "입력을 바꿨습니다"
