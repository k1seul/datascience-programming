"""Grading tests for Week 07 / C++ (medium): edit distance."""

from __future__ import annotations

import ctypes
from collections.abc import Sequence
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib, within_seconds

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"

CITIES = ["seoul", "busan", "daegu", "incheon", "gwangju", "daejeon", "ulsan", "suwon"]


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.edit_distance.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.edit_distance.restype = ctypes.c_int
    lib.closest_word.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int]
    lib.closest_word.restype = ctypes.c_int
    return lib


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def edit_distance(self, a: str, b: str) -> int:
        return checked(self._lib.edit_distance(a.encode(), b.encode()))

    def closest_word(self, word: str, words: Sequence[str]) -> int:
        array = (ctypes.c_char_p * max(len(words), 1))(*[w.encode() for w in words])
        return checked(self._lib.closest_word(word.encode(), array, len(words)))


@pytest.fixture
def api():
    return Api(_bind(native_lib(SRC)))


# --- (a) edit_distance -----------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("kitten", "sitting", 3),
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("sunday", "saturday", 3),
        ("flaw", "lawn", 2),
        ("algorithm", "altruistic", 6),
        ("data", "date", 1),
        ("science", "silence", 2),
        ("pyhton", "python", 2),
        ("ab", "ba", 2),
        ("a", "b", 1),
        ("abc", "xyz", 3),
        ("abc", "abc", 0),
    ],
)
def test_edit_distance(api, a, b, expected):
    assert api.edit_distance(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [("", "", 0), ("", "abc", 3), ("abc", "", 3), ("", "a", 1)],
)
def test_edit_distance_with_an_empty_word(api, a, b, expected):
    assert api.edit_distance(a, b) == expected


def test_edit_distance_is_symmetric(api):
    for a, b in [("kitten", "sitting"), ("horse", "ros"), ("flaw", "lawn"), ("", "abc")]:
        assert api.edit_distance(a, b) == api.edit_distance(b, a), f"{a!r} 와 {b!r}"


def quick_distance(api: Api, a: str, b: str) -> int:
    """Plain recursion branches three ways per letter, so 30-letter words never finish."""
    too_slow = (
        f"{len(a)}글자와 {len(b)}글자 단어의 편집 거리가 2초 안에 나오지 않았습니다. "
        "재귀로만 풀지 말고 표를 채워 주세요"
    )
    return within_seconds(2, lambda: api.edit_distance(a, b), too_slow)


def test_edit_distance_long_words(api):
    assert quick_distance(api, "dynamicprogramming" * 2, "dynamiteprogrammer" * 2) == 10


def test_edit_distance_shifted_words(api):
    assert quick_distance(api, "abcdefghij" * 3, "bcdefghijk" * 3) == 4


# --- (b) closest_word ------------------------------------------------------


@pytest.mark.parametrize(
    ("typo", "expected"),
    [
        ("seuol", "seoul"),
        ("pusan", "busan"),
        ("deajeon", "daejeon"),
        ("inchon", "incheon"),
        ("kwangju", "gwangju"),
        ("daegoo", "daegu"),
        ("ulsn", "ulsan"),
        ("sowon", "suwon"),
    ],
)
def test_closest_word_fixes_city_names(api, typo, expected):
    assert CITIES[api.closest_word(typo, CITIES)] == expected


def test_closest_word_exact_match(api):
    assert api.closest_word("daegu", CITIES) == CITIES.index("daegu")


def test_closest_word_tie_goes_to_the_smaller_index(api):
    # "bat", "cut" and "cart" are all one edit away from "cat".
    tie = "거리가 같은 단어가 여럿이면 번호가 가장 작은 단어를 골라 주세요"
    assert api.closest_word("cat", ["bat", "cut", "cart"]) == 0, tie
    assert api.closest_word("cat", ["cart", "cut", "bat"]) == 0, tie
    assert api.closest_word("cat", ["dog", "cut", "bat"]) == 1, tie


def test_closest_word_single_word(api):
    assert api.closest_word("anything", ["seoul"]) == 0


def test_closest_word_empty_dictionary(api):
    assert api.closest_word("seoul", []) == -1
