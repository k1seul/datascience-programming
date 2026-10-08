"""Grading tests for Week 04 / Python (easy)."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from . import solution

SRC = Path(__file__).resolve().parent / "solution.py"


def call(values, k, target):
    return sorted(solution.combinations_with_sum(values, k, target))


@pytest.mark.parametrize(
    ("values", "k", "target", "expected"),
    [
        ([1, 2, 3, 4], 2, 5, [[1, 4], [2, 3]]),
        ([1, 2, 3], 2, 4, [[1, 3]]),
        ([1, 2, 3], 3, 6, [[1, 2, 3]]),
        ([5], 1, 5, [[5]]),
        ([5], 1, 4, []),
        ([1, 2, 3], 1, 2, [[2]]),
        ([1, 2, 3, 4, 5], 2, 6, [[1, 5], [2, 4]]),
        ([-1, 1, 2], 2, 1, [[-1, 2]]),
        ([-3, -2, 5], 2, -5, [[-3, -2]]),
        ([1, 2, 3], 2, 100, []),
        ([10, 20, 30], 2, 50, [[20, 30]]),
    ],
)
def test_basic_cases(values, k, target, expected):
    assert call(values, k, target) == expected


def test_input_order_is_kept_inside_each_combination():
    # 입력이 [4, 1, 3, 2] 이므로 각 조합도 그 순서를 따릅니다: [4, 1] 과 [3, 2].
    assert call([4, 1, 3, 2], 2, 5) == [[3, 2], [4, 1]]


def test_every_matching_combination_is_found():
    assert call([1, 2, 3, 4, 5, 6], 3, 10) == [[1, 3, 6], [1, 4, 5], [2, 3, 5]]


# --- 경계 처리 -------------------------------------------------------------


def test_k_zero_with_target_zero_returns_one_empty_combination():
    assert call([1, 2, 3], 0, 0) == [[]]
    assert call([], 0, 0) == [[]]


def test_k_zero_with_nonzero_target_returns_nothing():
    assert call([1, 2, 3], 0, 5) == []


@pytest.mark.parametrize("k", [-1, -5])
def test_negative_k_returns_nothing(k):
    assert call([1, 2, 3], k, 0) == []


def test_k_larger_than_the_input_returns_nothing():
    assert call([1, 2], 3, 3) == []
    assert call([], 1, 0) == []


def test_k_equal_to_the_input_length():
    assert call([1, 2], 2, 3) == [[1, 2]]
    assert call([1, 2], 2, 4) == []


# --- 흔한 실수 ------------------------------------------------------------


def test_results_are_copies_not_shared_references():
    """답에 담을 때 리스트를 복사하지 않으면 여기서 걸립니다."""
    found = solution.combinations_with_sum([1, 2, 3, 4], 2, 5)
    assert sorted(found) == [[1, 4], [2, 3]], (
        "결과가 같은 리스트를 가리키고 있습니다. result.append(path[:]) 처럼 복사해 주세요"
    )
    assert len({id(c) for c in found}) == len(found), "같은 리스트 객체를 여러 번 담았습니다"


def test_values_are_not_reused():
    # 2 를 두 번 써서 4 를 만들면 안 됩니다.
    assert call([2, 3], 2, 4) == []


def test_input_is_not_modified():
    values = [1, 2, 3, 4]
    before = copy.deepcopy(values)
    solution.combinations_with_sum(values, 2, 5)
    assert values == before, "입력을 바꿨습니다"


def test_itertools_is_not_used():
    source = SRC.read_text(encoding="utf-8")
    assert "itertools" not in source, "itertools 대신 백트래킹을 직접 구현해 주세요"
