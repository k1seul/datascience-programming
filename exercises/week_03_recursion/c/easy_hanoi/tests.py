"""Grading tests for Week 03 / C (easy)."""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)

# The minimal solution for the Tower of Hanoi is unique, so these are the only
# correct sequences. Written as (from peg, to peg) pairs.
MOVES = {
    0: [],
    1: [(1, 3)],
    2: [(1, 2), (1, 3), (2, 3)],
    3: [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)],
    4: [
        (1, 2),
        (1, 3),
        (2, 3),
        (1, 2),
        (3, 1),
        (3, 2),
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 1),
        (3, 1),
        (2, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ],
}


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.hanoi_count.argtypes = [ctypes.c_int]
    lib.hanoi_count.restype = ctypes.c_int
    lib.hanoi_moves.argtypes = [ctypes.c_int, INT_P, ctypes.c_int]
    lib.hanoi_moves.restype = ctypes.c_int
    return lib


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def count(self, n: int) -> int:
        return checked(self._lib.hanoi_count(n))

    def moves(self, n: int, capacity: int | None = None) -> tuple[int, list[tuple[int, int]]]:
        cap = capacity if capacity is not None else 64
        out = (ctypes.c_int * max(cap, 1))()
        got = checked(self._lib.hanoi_moves(n, out, cap))
        if got < 0:
            return got, []
        flat = list(out[: got * 2])
        return got, list(zip(flat[0::2], flat[1::2], strict=True))


@pytest.fixture
def api():
    return Api(_bind(native_lib(SRC)))


# --- hanoi_count -----------------------------------------------------------


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 1), (2, 3), (3, 7), (4, 15), (5, 31), (10, 1023), (16, 65535)],
)
def test_hanoi_count(api, n, expected):
    assert api.count(n) == expected


def test_hanoi_count_at_the_upper_limit(api):
    # 2**31 - 1 is the largest value an int can hold, so n = 31 is the last valid input.
    assert api.count(31) == 2147483647


@pytest.mark.parametrize("n", [-1, -10, 32, 100])
def test_hanoi_count_rejects_out_of_range(api, n):
    assert api.count(n) == -1


# --- hanoi_moves -----------------------------------------------------------


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4])
def test_hanoi_moves_returns_the_move_count(api, n):
    assert api.moves(n)[0] == len(MOVES[n])


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4])
def test_hanoi_moves_matches_the_unique_minimal_sequence(api, n):
    assert api.moves(n)[1] == MOVES[n]


def test_hanoi_moves_writes_two_ints_per_move(api):
    # n = 2 is three moves, so six ints: 1->2, 1->3, 2->3
    out = (ctypes.c_int * 6)()
    lib = _bind(native_lib(SRC))
    assert checked(lib.hanoi_moves(2, out, 6)) == 3
    assert list(out) == [1, 2, 1, 3, 2, 3]


@pytest.mark.parametrize("n", [-1, 32])
def test_hanoi_moves_rejects_out_of_range(api, n):
    assert api.moves(n)[0] == -1


def test_hanoi_moves_rejects_small_capacity(api):
    # Three moves need six ints; five is not enough.
    assert api.moves(2, capacity=5)[0] == -1


def test_hanoi_moves_accepts_exact_capacity(api):
    assert api.moves(3, capacity=14) == (7, MOVES[3])


# --- 규칙을 실제로 지키는지 ------------------------------------------------


def simulate(n: int, moves: list[tuple[int, int]]) -> None:
    """Replay the moves on real pegs and fail if any rule is broken."""
    pegs = {1: list(range(n, 0, -1)), 2: [], 3: []}
    for step, (src, dst) in enumerate(moves, 1):
        assert src in pegs and dst in pegs, f"{step}번째 이동의 기둥 번호가 1~3 이 아닙니다"
        assert src != dst, f"{step}번째 이동이 같은 기둥을 가리킵니다"
        assert pegs[src], f"{step}번째 이동: {src}번 기둥이 비어 있습니다"
        disk = pegs[src].pop()
        assert not pegs[dst] or pegs[dst][-1] > disk, (
            f"{step}번째 이동: 큰 원반 위에 작은 원반을 올렸습니다"
        )
        pegs[dst].append(disk)
    assert pegs[3] == list(range(n, 0, -1)), "마지막에 모든 원반이 3번 기둥에 쌓여 있지 않습니다"
    assert not pegs[1] and not pegs[2]


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_moves_obey_the_rules_and_finish_on_peg_three(api, n):
    count, moves = api.moves(n, capacity=2 * (2**n))
    assert count == 2**n - 1
    simulate(n, moves)
