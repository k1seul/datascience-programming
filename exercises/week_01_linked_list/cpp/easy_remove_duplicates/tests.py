"""Week 01 / C++ (쉬움) 채점 테스트."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from harness import list_out_call, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


@pytest.fixture
def dedup():
    lib = native_lib(SRC)

    def call(values: list[int], capacity: int | None = None) -> list[int]:
        return list_out_call(lib.dedup_sorted, values, capacity=capacity)

    return call


def reference(values: list[int]) -> list[int]:
    result: list[int] = []
    for value in values:
        if not result or result[-1] != value:
            result.append(value)
    return result


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([1], [1]),
        ([1, 1], [1]),
        ([1, 1, 2, 3, 3, 3], [1, 2, 3]),
        ([2, 2, 2], [2]),
        ([1, 2, 3], [1, 2, 3]),
        ([-5, -5, 0, 0, 0, 7], [-5, 0, 7]),
    ],
)
def test_기본_케이스(dedup, values, expected):
    assert dedup(values) == expected


def test_중복이_맨_끝에_몰려도_처리한다(dedup):
    assert dedup([1, 2, 3, 3, 3, 3]) == [1, 2, 3]


def test_중복이_맨_앞에_몰려도_처리한다(dedup):
    assert dedup([9, 9, 9, 9, 10]) == [9, 10]


def test_용량이_모자라면_오류를_반환한다(dedup):
    with pytest.raises(ValueError):
        dedup([1, 1, 2, 3], capacity=2)


def test_결과_길이와_딱_맞는_용량은_통과한다(dedup):
    assert dedup([1, 1, 2, 3], capacity=3) == [1, 2, 3]


def test_무작위_입력이_참조_구현과_같다(dedup):
    rng = random.Random(1)
    for _ in range(50):
        values = sorted(rng.choices(range(-10, 10), k=rng.randint(0, 40)))
        assert dedup(values) == reference(values)
