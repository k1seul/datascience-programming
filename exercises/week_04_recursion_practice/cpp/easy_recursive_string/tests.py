"""Grading tests for Week 04 / C++ (easy)."""

from __future__ import annotations

import ctypes
import re
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.cpp"


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.reverse_string.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    lib.reverse_string.restype = ctypes.c_int
    lib.count_vowels.argtypes = [ctypes.c_char_p]
    lib.count_vowels.restype = ctypes.c_int
    lib.is_subsequence.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.is_subsequence.restype = ctypes.c_int
    return lib


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def reverse_string(self, text: str, capacity: int | None = None) -> tuple[int, str]:
        cap = capacity if capacity is not None else 256
        buf = ctypes.create_string_buffer(max(cap, 1))
        written = self._lib.reverse_string(text.encode(), buf, cap)
        if written < 0:
            return written, ""
        return written, buf.raw[:written].decode()

    def count_vowels(self, text: str) -> int:
        return self._lib.count_vowels(text.encode())

    def is_subsequence(self, a: str, b: str) -> int:
        return self._lib.is_subsequence(a.encode(), b.encode())


@pytest.fixture
def api():
    lib = _bind(native_lib(SRC))
    # An untouched stub returns the sentinel here, which marks the task "not written yet".
    if lib.count_vowels(b"") == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return Api(lib)


# --- reverse_string --------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ba"),
        ("hello", "olleh"),
        ("abcde", "edcba"),
        ("aa", "aa"),
        ("Hello World", "dlroW olleH"),
        ("12 34", "43 21"),
    ],
)
def test_reverse_string(api, text, expected):
    assert api.reverse_string(text) == (len(expected), expected)


def test_reverse_string_rejects_small_capacity(api):
    # "olleh" 는 5글자이므로 NUL 까지 6칸이 필요합니다.
    assert api.reverse_string("hello", capacity=5)[0] == -1


def test_reverse_string_accepts_exact_capacity(api):
    assert api.reverse_string("hello", capacity=6) == (5, "olleh")


def test_reverse_string_handles_an_empty_string(api):
    assert api.reverse_string("", capacity=1) == (0, "")


# --- count_vowels ----------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("a", 1),
        ("b", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("Programming", 3),
        ("rhythm", 0),
        ("AaEeIiOoUu", 10),
        ("Hello World", 3),
        ("xyz", 0),
    ],
)
def test_count_vowels(api, text, expected):
    assert api.count_vowels(text) == expected


def test_count_vowels_ignores_case(api):
    assert api.count_vowels("APPLE") == api.count_vowels("apple")


def test_count_vowels_does_not_count_y(api):
    assert api.count_vowels("myth") == 0


# --- is_subsequence --------------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("", "", 1),
        ("", "abc", 1),
        ("a", "", 0),
        ("a", "a", 1),
        ("a", "b", 0),
        ("ace", "abcde", 1),
        ("aec", "abcde", 0),
        ("abc", "abc", 1),
        ("abcd", "abc", 0),
        ("axc", "abcde", 0),
        ("ade", "abcde", 1),
        ("bd", "abcde", 1),
        ("aa", "ab", 0),
        ("aa", "aba", 1),
    ],
)
def test_is_subsequence(api, a, b, expected):
    assert api.is_subsequence(a, b) == expected


def test_empty_string_is_a_subsequence_of_anything(api):
    assert api.is_subsequence("", "xyz") == 1
    assert api.is_subsequence("", "") == 1


def test_a_longer_string_cannot_be_a_subsequence(api):
    assert api.is_subsequence("abcdef", "abc") == 0


# --- 재귀로 썼는지 ---------------------------------------------------------


def test_loops_are_not_used():
    """세 함수 모두 재귀로 써야 합니다."""
    source = SRC.read_text(encoding="utf-8")
    for keyword in ("for", "while", "goto"):
        found = re.search(rf"\b{keyword}\s*[(;]", source)
        assert found is None, f"{keyword} 대신 재귀로 작성해 주세요"
