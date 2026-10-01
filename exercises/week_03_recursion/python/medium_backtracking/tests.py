"""Grading tests for Week 03 / Python (medium)."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from . import solution

SRC = Path(__file__).resolve().parent / "solution.py"


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], [[]]),
        ([1], [[1]]),
        ([1, 2], [[1, 2], [2, 1]]),
        (
            [1, 2, 3],
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
        ),
        (
            [3, 1, 2],
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
        ),
    ],
)
def test_permutations(values, expected):
    assert sorted(solution.permutations(values)) == expected


@pytest.mark.parametrize(("n", "expected"), [(1, 1), (2, 2), (3, 6), (4, 24), (5, 120)])
def test_permutation_count_is_n_factorial(n, expected):
    assert len(solution.permutations(list(range(1, n + 1)))) == expected


def test_permutations_are_all_different():
    found = solution.permutations([1, 2, 3, 4])
    unique = {tuple(p) for p in found}
    assert len(unique) == 24, "같은 순열이 여러 번 들어 있거나 빠진 것이 있습니다"


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], [[]]),
        ([1], [[], [1]]),
        ([1, 2], [[], [1], [1, 2], [2]]),
        ([1, 2, 3], [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]),
    ],
)
def test_subsets(values, expected):
    assert sorted(solution.subsets(values)) == expected


def test_subsets_keep_the_input_order():
    # 입력이 [2, 1] 이면 부분집합도 2 가 1 보다 앞입니다.
    assert sorted(solution.subsets([2, 1])) == [[], [1], [2], [2, 1]]


@pytest.mark.parametrize(("n", "expected"), [(1, 2), (2, 4), (3, 8), (4, 16), (5, 32)])
def test_subset_count_is_two_to_the_n(n, expected):
    assert len(solution.subsets(list(range(1, n + 1)))) == expected


def test_subsets_are_all_different():
    found = solution.subsets([1, 2, 3, 4])
    unique = {tuple(s) for s in found}
    assert len(unique) == 16, "같은 부분집합이 여러 번 들어 있거나 빠진 것이 있습니다"


# --- 흔한 실수 ------------------------------------------------------------


def test_results_are_copies_not_shared_references():
    """답에 담을 때 리스트를 복사하지 않으면 여기서 걸립니다."""
    found = solution.subsets([1, 2])
    assert [] in found and [1, 2] in found, (
        "결과가 전부 같은 리스트를 가리키고 있습니다. result.append(path[:]) 처럼 복사해 주세요"
    )
    ids = {id(s) for s in found}
    assert len(ids) == len(found), "같은 리스트 객체를 여러 번 담았습니다"


def test_input_is_not_modified():
    values = [1, 2, 3]
    before = copy.deepcopy(values)
    solution.permutations(values)
    solution.subsets(values)
    assert values == before, "입력을 바꿨습니다"


def test_itertools_is_not_used():
    source = SRC.read_text(encoding="utf-8")
    assert "itertools" not in source, "itertools 대신 백트래킹을 직접 구현해 주세요"
