"""Grading tests for Week 08 / C (medium): circular deque and two window problems.

Test names start with the sub-part they grade, (a) to (c) in problem.md.
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

# (b) 200,000 days that only get colder, then one hot day. Scanning ahead from every day
# takes about 2 * 10^10 comparisons; a deque of waiting days takes 2 * 10^5.
FALLING_DAYS = 200_000
FALLING = [FALLING_DAYS - i for i in range(FALLING_DAYS - 1)] + [10 * FALLING_DAYS]

# (c) Negatives only at both ends, so most windows have none. Scanning every window from
# its start takes about 10^10 steps.
SPARSE_N, SPARSE_K = 200_000, 100_000
SPARSE = [i % 7 + 1 for i in range(SPARSE_N)]
SPARSE[0], SPARSE[-1] = -5, -9

TOO_SLOW = (
    "{what} 이 2초 안에 끝나지 않았습니다. 날마다(창마다) 처음부터 다시 훑지 말고 "
    "덱에 인덱스를 넣고 빼면서 한 번만 지나가세요"
)

# Small inputs finish at once; getting stuck means a loop that never ends, which usually
# comes from a broken deque. Failing here keeps the rest of the run going.
STUCK = (
    "작은 입력인데 2초 안에 끝나지 않았습니다. 무한 루프에 빠졌을 수 있습니다. "
    "(a) 의 덱 테스트부터 모두 통과시키세요"
)


class DequeStruct(ctypes.Structure):
    """Mirror of Deque in deque.h."""

    _fields_ = [
        ("buf", INT_P),
        ("capacity", ctypes.c_int),
        ("size", ctypes.c_int),
        ("front", ctypes.c_int),
        ("rear", ctypes.c_int),
    ]


DEQUE_P = ctypes.POINTER(DequeStruct)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    """Mirror the signatures from deque.h onto the loaded library."""
    lib.dq_create.argtypes = [ctypes.c_int]
    lib.dq_create.restype = DEQUE_P
    lib.dq_free.argtypes = [DEQUE_P]
    lib.dq_free.restype = None
    for name in ("dq_is_empty", "dq_is_full"):
        getattr(lib, name).argtypes = [DEQUE_P]
        getattr(lib, name).restype = ctypes.c_int
    for name in ("dq_push_front", "dq_push_back"):
        getattr(lib, name).argtypes = [DEQUE_P, ctypes.c_int]
        getattr(lib, name).restype = ctypes.c_int
    for name in ("dq_pop_front", "dq_pop_back", "dq_peek_front", "dq_peek_back"):
        getattr(lib, name).argtypes = [DEQUE_P, INT_P]
        getattr(lib, name).restype = ctypes.c_int
    lib.days_until_warmer.argtypes = [INT_P, ctypes.c_int, INT_P]
    lib.days_until_warmer.restype = ctypes.c_int
    lib.first_negative.argtypes = [INT_P, ctypes.c_int, ctypes.c_int, INT_P]
    lib.first_negative.restype = ctypes.c_int
    return lib


def checked(result: int) -> int:
    """Turn the untouched stub's sentinel into the marker the grader looks for."""
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


@pytest.fixture
def lib():
    return _bind(native_lib(SRC, track_alloc=True))


class Deque:
    """Wraps a Deque * so the tests read like the C calls they make."""

    def __init__(self, lib: ctypes.CDLL, capacity: int) -> None:
        self.lib = lib
        self.ptr = lib.dq_create(capacity)
        if not self.ptr:
            # The untouched stub returns NULL here, so the grader reads this as "not
            # written yet" rather than as a wrong answer.
            raise NotImplementedError("dq_create() returned NULL")

    @property
    def raw(self) -> DequeStruct:
        return self.ptr.contents

    def contents(self) -> list[int]:
        """Values front to back, read straight from buf using the layout in deque.h."""
        raw = self.raw
        return [raw.buf[(raw.front + i) % raw.capacity] for i in range(raw.size)]

    def check_rear(self) -> None:
        raw = self.raw
        expected = (raw.front + raw.size) % raw.capacity
        assert raw.rear == expected, (
            f"rear 가 {raw.rear} 입니다. front {raw.front}, size {raw.size} 이면 "
            f"(front + size) % capacity = {expected} 이어야 합니다"
        )

    def push_back(self, *values: int) -> list[int]:
        return [checked(self.lib.dq_push_back(self.ptr, v)) for v in values]

    def push_front(self, *values: int) -> list[int]:
        return [checked(self.lib.dq_push_front(self.ptr, v)) for v in values]

    def _take(self, name: str) -> tuple[int, int]:
        out = ctypes.c_int(-777)
        ok = checked(getattr(self.lib, name)(self.ptr, ctypes.byref(out)))
        return ok, out.value

    def pop_front(self) -> tuple[int, int]:
        return self._take("dq_pop_front")

    def pop_back(self) -> tuple[int, int]:
        return self._take("dq_pop_back")

    def peek_front(self) -> tuple[int, int]:
        return self._take("dq_peek_front")

    def peek_back(self) -> tuple[int, int]:
        return self._take("dq_peek_back")

    def is_empty(self) -> int:
        return checked(self.lib.dq_is_empty(self.ptr))

    def is_full(self) -> int:
        return checked(self.lib.dq_is_full(self.ptr))

    def free(self) -> None:
        self.lib.dq_free(self.ptr)
        self.ptr = None


@pytest.fixture
def make(lib):
    made: list[Deque] = []

    def factory(capacity: int) -> Deque:
        dq = Deque(lib, capacity)
        made.append(dq)
        return dq

    yield factory
    for dq in made:
        if dq.ptr:
            dq.free()


def buffer(values: Sequence[int]) -> ctypes.Array:
    return (ctypes.c_int * max(len(values), 1))(*values)


def warmer(lib: ctypes.CDLL, temps: Sequence[int], too_slow: str = STUCK) -> list[int]:
    answer = buffer([-777] * len(temps))

    def run() -> int:
        return lib.days_until_warmer(buffer(temps), len(temps), answer)

    count = checked(within_seconds(2, run, too_slow))
    assert count == len(temps), f"반환값은 {len(temps)} 이어야 합니다 (받은 값 {count})"
    return list(answer[: len(temps)])


def negatives(lib: ctypes.CDLL, nums: Sequence[int], k: int, too_slow: str = STUCK) -> list[int]:
    count_expected = len(nums) - k + 1
    result = buffer([-777] * max(count_expected, 1))

    def run() -> int:
        return lib.first_negative(buffer(nums), len(nums), k, result)

    count = checked(within_seconds(2, run, too_slow))
    assert count == count_expected, f"반환값은 {count_expected} 이어야 합니다 (받은 값 {count})"
    return list(result[:count])


# --- (a) circular deque ----------------------------------------------------


def test_a_create_starts_empty(make):
    dq = make(4)
    raw = dq.raw
    assert (raw.capacity, raw.size, raw.front, raw.rear) == (4, 0, 0, 0)
    assert dq.is_empty() == 1
    assert dq.is_full() == 0


@pytest.mark.parametrize("capacity", [0, -3])
def test_a_create_rejects_capacity_below_one(lib, capacity):
    assert not lib.dq_create(capacity), "capacity 가 1 보다 작으면 NULL 을 반환해야 합니다"


def test_a_free_accepts_null(lib):
    lib.dq_free(None)


def test_a_free_releases_everything(lib):
    before = live_allocations(lib)
    dq = Deque(lib, 3)
    dq.push_back(1, 2)
    dq.free()
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"dq_free 뒤에 해제되지 않은 메모리가 {leaked}개 남았습니다"


def test_a_push_back_and_pop_front_keep_order(make):
    dq = make(4)
    assert dq.push_back(10, 20, 30) == [1, 1, 1]
    assert dq.contents() == [10, 20, 30]
    dq.check_rear()
    assert dq.pop_front() == (1, 10)
    assert dq.pop_front() == (1, 20)
    assert dq.contents() == [30]
    dq.check_rear()


def test_a_push_front_and_pop_back(make):
    dq = make(4)
    dq.push_front(1)
    raw = dq.raw
    assert raw.front == 3, "빈 덱에 push_front 하면 front 는 0 에서 capacity - 1 로 넘어갑니다"
    assert raw.rear == 0, "push_front 는 rear 를 바꾸지 않습니다"
    dq.push_front(2)
    dq.push_back(3)
    assert dq.contents() == [2, 1, 3]
    assert dq.pop_back() == (1, 3)
    assert dq.pop_back() == (1, 1)
    assert dq.contents() == [2]
    dq.check_rear()


def test_a_peek_does_not_remove(make):
    dq = make(3)
    dq.push_back(4, 5, 6)
    assert dq.peek_front() == (1, 4)
    assert dq.peek_back() == (1, 6)
    assert dq.contents() == [4, 5, 6]


def test_a_full_deque_rejects_pushes(make):
    dq = make(2)
    dq.push_back(1, 2)
    assert dq.is_full() == 1
    assert dq.push_back(3) == [0]
    assert dq.push_front(0) == [0]
    assert dq.contents() == [1, 2], "꽉 찬 덱에 넣으려다 실패하면 덱은 그대로여야 합니다"
    dq.check_rear()


def test_a_empty_deque_leaves_out_alone(make):
    dq = make(2)
    for take in (dq.pop_front, dq.pop_back, dq.peek_front, dq.peek_back):
        assert take() == (0, -777), "빈 덱에서는 0 을 반환하고 *out 은 건드리지 않습니다"


def test_a_indices_wrap_around(make):
    dq = make(3)
    dq.push_back(1, 2, 3)
    assert dq.raw.rear == 0, "마지막 칸에 쓰고 나면 rear 는 0 으로 돌아옵니다"
    dq.pop_front()
    dq.push_back(4)
    assert dq.raw.buf[0] == 4, "rear 가 0 이었으니 4 는 buf[0] 에 들어가야 합니다"
    assert dq.contents() == [2, 3, 4]
    dq.pop_front()
    dq.pop_front()
    dq.push_back(5, 6)
    assert dq.contents() == [4, 5, 6]
    dq.check_rear()


def test_a_mixed_sequence(make):
    dq = make(5)
    dq.push_back(3)
    dq.push_front(2)
    dq.push_back(4)
    dq.push_front(1)
    dq.pop_back()
    dq.push_back(9)
    dq.pop_front()
    assert dq.contents() == [2, 3, 9]
    dq.check_rear()


# --- (b) days_until_warmer -------------------------------------------------


@pytest.mark.parametrize(
    ("temps", "expected"),
    [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([50, 40, 30], [0, 0, 0]),
        ([5, 5, 5], [0, 0, 0]),
        ([3], [0]),
        ([-2, -5, -1], [2, 1, 0]),
    ],
)
def test_b_days_until_warmer(lib, temps, expected):
    assert warmer(lib, temps) == expected


def test_b_equal_is_not_warmer(lib):
    assert warmer(lib, [20, 20, 21]) == [2, 1, 0], "같은 온도는 더 따뜻한 날이 아닙니다"


def test_b_no_days(lib):
    assert checked(lib.days_until_warmer(buffer([]), 0, buffer([]))) == 0


def test_b_long_cold_spell(lib):
    answer = warmer(lib, FALLING, TOO_SLOW.format(what="20만 일"))
    assert answer[0] == FALLING_DAYS - 1
    assert answer[-2] == 1
    assert answer[-1] == 0
    assert sum(answer) == (FALLING_DAYS - 1) * FALLING_DAYS // 2


def test_b_frees_its_deque(lib):
    before = live_allocations(lib)
    warmer(lib, [73, 74, 75, 71, 69, 72, 76, 73])
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"days_until_warmer 가 끝난 뒤 해제하지 않은 메모리가 {leaked}개 남았습니다"


# --- (c) first_negative ----------------------------------------------------


@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([12, -1, -7, 8, -15, 30, 16, 28], 3, [-1, -1, -7, -15, -15, 0]),
        ([-8, 2, 3, -6, 10], 2, [-8, 0, -6, -6]),
        ([1, 2, 3], 2, [0, 0]),
        ([-1, -2, -3], 1, [-1, -2, -3]),
        ([4, -2, 5], 3, [-2]),
    ],
)
def test_c_first_negative(lib, nums, k, expected):
    assert negatives(lib, nums, k) == expected


@pytest.mark.parametrize("k", [0, -1, 4])
def test_c_rejects_bad_window(lib, k):
    result = buffer([0, 0, 0])
    assert checked(lib.first_negative(buffer([1, -2, 3]), 3, k, result)) == -1


def test_c_mostly_positive(lib):
    result = negatives(lib, SPARSE, SPARSE_K, TOO_SLOW.format(what="길이 20만, 창 10만"))
    assert len(result) == SPARSE_N - SPARSE_K + 1
    assert result[0] == -5
    assert result[-1] == -9
    assert result[1:-1] == [0] * (len(result) - 2)


def test_c_frees_its_deque(lib):
    before = live_allocations(lib)
    negatives(lib, [12, -1, -7, 8, -15, 30, 16, 28], 3)
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"first_negative 가 끝난 뒤 해제하지 않은 메모리가 {leaked}개 남았습니다"
