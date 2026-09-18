"""Grading tests for Week 02 / C (easy)."""

from __future__ import annotations

import ctypes
import random
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.has_duplicate.argtypes = [INT_P, ctypes.c_int]
    lib.has_duplicate.restype = ctypes.c_int
    lib.first_duplicate.argtypes = [INT_P, ctypes.c_int]
    lib.first_duplicate.restype = ctypes.c_int
    lib.find_duplicates.argtypes = [INT_P, ctypes.c_int, INT_P, ctypes.c_int]
    lib.find_duplicates.restype = ctypes.c_int
    return lib


def buffer(values: list[int]) -> ctypes.Array:
    return (ctypes.c_int * max(len(values), 1))(*values)


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def has_duplicate(self, values: list[int]) -> int:
        return checked(self._lib.has_duplicate(buffer(values), len(values)))

    def first_duplicate(self, values: list[int]) -> int:
        return checked(self._lib.first_duplicate(buffer(values), len(values)))

    def find_duplicates(
        self, values: list[int], capacity: int | None = None
    ) -> tuple[int, list[int]]:
        cap = capacity if capacity is not None else 100
        out = (ctypes.c_int * max(cap, 1))()
        count = checked(self._lib.find_duplicates(buffer(values), len(values), out, cap))
        return count, list(out[: max(count, 0)])


@pytest.fixture
def api():
    return Api(_bind(native_lib(SRC)))


def reference(values: list[int]) -> list[int]:
    seen: dict[int, int] = {}
    for value in values:
        seen[value] = seen.get(value, 0) + 1
    return sorted(value for value, count in seen.items() if count > 1)


# --- has_duplicate ---------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([7], 0),
        ([1, 2, 3], 0),
        ([3, 1, 4, 1, 5], 1),
        ([0, 0], 1),
        ([99, 98, 99], 1),
        (list(range(100)), 0),
    ],
)
def test_has_duplicate(api, values, expected):
    assert api.has_duplicate(values) == expected


@pytest.mark.parametrize("bad", [-1, 100, 1000])
def test_has_duplicate_rejects_out_of_range(api, bad):
    assert api.has_duplicate([1, 2, bad]) == -1


# --- first_duplicate -------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], -1),
        ([1, 2, 3], -1),
        ([3, 1, 4, 1, 5], 1),
        ([5, 3, 5, 3], 5),
        ([3, 5, 3, 5], 3),
        ([9, 9], 9),
        ([0, 1, 2, 0], 0),
    ],
)
def test_first_duplicate(api, values, expected):
    assert api.first_duplicate(values) == expected


def test_first_duplicate_is_not_the_smallest_value(api):
    # 2 is smaller, but 8 repeats earlier.
    assert api.first_duplicate([8, 2, 8, 2]) == 8


@pytest.mark.parametrize("bad", [-1, 100])
def test_first_duplicate_rejects_out_of_range(api, bad):
    assert api.first_duplicate([1, bad, 1]) == -2


# --- find_duplicates -------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([1, 2, 3], []),
        ([3, 1, 4, 1, 5], [1]),
        ([7, 7, 2, 2, 2, 9], [2, 7]),
        ([0, 0, 99, 99], [0, 99]),
        ([5, 5, 5, 5], [5]),
    ],
)
def test_find_duplicates(api, values, expected):
    assert api.find_duplicates(values) == (len(expected), expected)


def test_find_duplicates_is_ascending_without_sorting(api):
    values = [9, 1, 9, 5, 1, 5, 3, 3]
    count, found = api.find_duplicates(values)
    assert found == sorted(found)
    assert (count, found) == (4, [1, 3, 5, 9])


def test_find_duplicates_rejects_small_capacity(api):
    assert api.find_duplicates([1, 1, 2, 2, 3, 3], capacity=2)[0] == -1


def test_find_duplicates_accepts_exact_capacity(api):
    assert api.find_duplicates([1, 1, 2, 2, 3, 3], capacity=3) == (3, [1, 2, 3])


@pytest.mark.parametrize("bad", [-5, 100])
def test_find_duplicates_rejects_out_of_range(api, bad):
    assert api.find_duplicates([1, 1, bad])[0] == -2


# --- 무작위 대조 -----------------------------------------------------------


def test_matches_reference_on_random_input(api):
    rng = random.Random(2)
    for _ in range(60):
        values = [rng.randint(0, 99) for _ in range(rng.randint(0, 200))]
        expected = reference(values)
        assert api.find_duplicates(values) == (len(expected), expected)
        assert api.has_duplicate(values) == (1 if expected else 0)
