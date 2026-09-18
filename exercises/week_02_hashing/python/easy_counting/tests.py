"""Grading tests for Week 02 / Python (easy)."""

from __future__ import annotations

import random

import pytest

from . import solution


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], {}),
        ([1], {1: 1}),
        ([3, 1, 3, 3, 1], {3: 3, 1: 2}),
        ([0, 0, 0], {0: 3}),
        ([-1, -1, 2], {-1: 2, 2: 1}),
    ],
)
def test_count_values(values, expected):
    assert solution.count_values(values) == expected


def test_count_values_accepts_a_generator():
    assert solution.count_values(x % 3 for x in range(10)) == {0: 4, 1: 3, 2: 3}


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", None),
        ("a", "a"),
        ("aabb", None),
        ("leetcode", "l"),
        ("loveleetcode", "v"),
        ("aabbc", "c"),
        ("abcabd", "c"),
    ],
)
def test_first_unique(text, expected):
    assert solution.first_unique(text) == expected


def test_first_unique_returns_the_earliest_not_the_smallest():
    # Both "z" and "a" appear once; "z" comes first.
    assert solution.first_unique("zbba") == "z"


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("", "", True),
        ("a", "a", True),
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "ab", False),
        ("ab", "a", False),
        ("aabb", "abab", True),
        ("aab", "abb", False),
    ],
)
def test_is_anagram(left, right, expected):
    assert solution.is_anagram(left, right) is expected


def test_is_anagram_on_random_pairs():
    rng = random.Random(6)
    for _ in range(50):
        word = [rng.choice("abcde") for _ in range(rng.randint(0, 8))]
        shuffled = word[:]
        rng.shuffle(shuffled)
        assert solution.is_anagram("".join(word), "".join(shuffled)) is True


def test_counter_is_not_used(monkeypatch):
    """Best-effort check of the "no Counter" rule.

    Shadows Counter inside the solution module, which catches the usual
    `from collections import Counter` shape.
    """

    def banned(*args, **kwargs):
        raise AssertionError("count with a dict of your own, not collections.Counter")

    monkeypatch.setattr(solution, "Counter", banned, raising=False)

    assert solution.count_values([1, 1, 2]) == {1: 2, 2: 1}
    assert solution.first_unique("aabbc") == "c"
    assert solution.is_anagram("abc", "cab") is True
