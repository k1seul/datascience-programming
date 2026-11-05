"""Grading tests for Week 07 / C (medium): 0/1 knapsack.

knapsack_choose may return any optimal set, so its tests check the set itself: indices
in range, ascending, within budget, and worth the best value.
"""

from __future__ import annotations

import ctypes
from collections.abc import Sequence
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, live_allocations, native_lib, within_seconds

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)

# (cost, value, budget, best value)
CASES = [
    ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9),
    ([5, 4, 3], [11, 7, 6], 7, 13),
    ([10, 20, 30], [60, 100, 120], 50, 220),
    ([1, 1, 1, 1], [1, 2, 3, 4], 2, 7),
    ([2, 2, 2], [3, 3, 3], 5, 6),
    ([1, 2, 3], [2, 2, 2], 10, 6),
    ([3], [5], 3, 5),
    ([5, 6], [3, 4], 4, 0),
    ([4, 2, 3], [0, 0, 1], 9, 1),
    ([1, 3, 4, 5], [1, 4, 5, 7], 0, 0),
    ([], [], 10, 0),
]

# 40 items: trying every subset means 2^40 of them.
BIG_COST = [i % 7 + 1 for i in range(40)]
BIG_VALUE = [(i * 37) % 23 + 1 for i in range(40)]
BIG_BUDGET = 100
BIG_BEST = 416

TOO_SLOW = (
    "광고 40개짜리 입력이 2초 안에 끝나지 않았습니다. "
    "모든 조합을 다 해 보지 말고 (광고 수 + 1) x (예산 + 1) 표를 채워 주세요"
)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.knapsack_best.argtypes = [INT_P, INT_P, ctypes.c_int, ctypes.c_int]
    lib.knapsack_best.restype = ctypes.c_int
    lib.knapsack_choose.argtypes = [INT_P, INT_P, ctypes.c_int, ctypes.c_int, INT_P]
    lib.knapsack_choose.restype = ctypes.c_int
    return lib


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


def buffer(values: Sequence[int]) -> ctypes.Array:
    return (ctypes.c_int * max(len(values), 1))(*values)


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self.lib = lib

    def best(self, cost: Sequence[int], value: Sequence[int], budget: int) -> int:
        return checked(self.lib.knapsack_best(buffer(cost), buffer(value), len(cost), budget))

    def choose(self, cost: Sequence[int], value: Sequence[int], budget: int) -> list[int]:
        chosen = buffer([-1] * len(cost))
        count = checked(
            self.lib.knapsack_choose(buffer(cost), buffer(value), len(cost), budget, chosen)
        )
        assert 0 <= count <= len(cost), f"반환값 {count} 은 고른 개수가 될 수 없습니다"
        return list(chosen[:count])


@pytest.fixture
def api():
    return Api(_bind(native_lib(SRC, track_alloc=True)))


def check_choice(
    picked: list[int], cost: Sequence[int], value: Sequence[int], budget: int, best: int
) -> None:
    assert all(0 <= i < len(cost) for i in picked), f"없는 번호가 있습니다: {picked}"
    assert picked == sorted(set(picked)), f"번호는 겹치지 않게 오름차순으로 적어 주세요: {picked}"
    spent = sum(cost[i] for i in picked)
    assert spent <= budget, f"{picked} 의 비용 합 {spent} 이 예산 {budget} 을 넘습니다"
    worth = sum(value[i] for i in picked)
    assert worth == best, f"{picked} 의 효과 합은 {worth} 입니다. 가장 큰 값은 {best} 입니다"


# --- (a) knapsack_best -----------------------------------------------------


@pytest.mark.parametrize(("cost", "value", "budget", "best"), CASES)
def test_best(api, cost, value, budget, best):
    assert api.best(cost, value, budget) == best


def test_best_is_not_greedy(api):
    # Item 0 has the best value per cost (11 for 5), but items 1 and 2 together are worth more.
    assert api.best([5, 4, 3], [11, 7, 6], 7) == 13


def test_best_forty_items(api):
    best = within_seconds(2, lambda: api.best(BIG_COST, BIG_VALUE, BIG_BUDGET), TOO_SLOW)
    assert best == BIG_BEST


@pytest.mark.parametrize(("n", "budget"), [(-1, 5), (2, -1)])
def test_best_rejects_negative_sizes(api, n, budget):
    assert checked(api.lib.knapsack_best(buffer([1, 2]), buffer([1, 2]), n, budget)) == -1


def test_best_frees_its_table(api):
    before = live_allocations(api.lib)
    api.best([1, 3, 4, 5], [1, 4, 5, 7], 7)
    leaked = live_allocations(api.lib) - before
    assert leaked == 0, f"knapsack_best 가 끝난 뒤 해제하지 않은 메모리가 {leaked}개 남았습니다"


# --- (b) knapsack_choose ---------------------------------------------------


@pytest.mark.parametrize(("cost", "value", "budget", "best"), CASES)
def test_choose(api, cost, value, budget, best):
    check_choice(api.choose(cost, value, budget), cost, value, budget, best)


def test_choose_the_example(api):
    # Items 1 and 2 are the only way to reach 9 here, so the answer is fixed.
    assert api.choose([1, 3, 4, 5], [1, 4, 5, 7], 7) == [1, 2]


def test_choose_nothing_fits(api):
    assert api.choose([5, 6], [3, 4], 4) == []


def test_choose_everything_fits(api):
    assert api.choose([1, 2, 3], [2, 2, 2], 10) == [0, 1, 2]


def test_choose_forty_items(api):
    picked = within_seconds(2, lambda: api.choose(BIG_COST, BIG_VALUE, BIG_BUDGET), TOO_SLOW)
    check_choice(picked, BIG_COST, BIG_VALUE, BIG_BUDGET, BIG_BEST)


@pytest.mark.parametrize(("n", "budget"), [(-1, 5), (2, -1)])
def test_choose_rejects_negative_sizes(api, n, budget):
    chosen = buffer([0, 0])
    result = api.lib.knapsack_choose(buffer([1, 2]), buffer([1, 2]), n, budget, chosen)
    assert checked(result) == -1


def test_choose_frees_its_table(api):
    before = live_allocations(api.lib)
    api.choose([1, 3, 4, 5], [1, 4, 5, 7], 7)
    leaked = live_allocations(api.lib) - before
    assert leaked == 0, f"knapsack_choose 가 끝난 뒤 해제하지 않은 메모리가 {leaked}개 남았습니다"
