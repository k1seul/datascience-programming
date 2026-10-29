"""Grading tests for Week 06 / C (implementation): circular deque and round robin.

Test names start with the sub-part they grade, (a) to (d) in problem.md.
"""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, live_allocations, native_lib, native_stdout

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)


class DequeStruct(ctypes.Structure):
    """Mirror of Deque in deque.h."""

    _fields_ = [
        ("buf", INT_P),
        ("capacity", ctypes.c_int),
        ("size", ctypes.c_int),
        ("front", ctypes.c_int),
    ]


DEQUE_P = ctypes.POINTER(DequeStruct)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    """Mirror the signatures from deque.h onto the loaded library."""
    lib.deque_create.argtypes = [ctypes.c_int]
    lib.deque_create.restype = DEQUE_P
    lib.deque_free.argtypes = [DEQUE_P]
    lib.deque_free.restype = None
    for name in ("deque_is_empty", "deque_is_full"):
        getattr(lib, name).argtypes = [DEQUE_P]
        getattr(lib, name).restype = ctypes.c_int
    for name in ("deque_push_front", "deque_push_back"):
        getattr(lib, name).argtypes = [DEQUE_P, ctypes.c_int]
        getattr(lib, name).restype = ctypes.c_int
    for name in ("deque_pop_front", "deque_pop_back", "deque_peek_front", "deque_peek_back"):
        getattr(lib, name).argtypes = [DEQUE_P, INT_P]
        getattr(lib, name).restype = ctypes.c_int
    lib.deque_print.argtypes = [DEQUE_P]
    lib.deque_print.restype = None
    lib.round_robin.argtypes = [INT_P, ctypes.c_int, ctypes.c_int, INT_P]
    lib.round_robin.restype = ctypes.c_int
    return lib


def load() -> ctypes.CDLL:
    return _bind(native_lib(SRC, track_alloc=True))


class Deque:
    """Wraps a Deque * so the tests read like the C calls they make."""

    def __init__(self, lib: ctypes.CDLL, capacity: int) -> None:
        self.lib = lib
        self.ptr = lib.deque_create(capacity)
        if not self.ptr:
            # The untouched stub returns NULL here, so the grader reads this as "not
            # written yet" rather than as a wrong answer.
            raise NotImplementedError("deque_create() returned NULL")

    @property
    def raw(self) -> DequeStruct:
        return self.ptr.contents

    def contents(self) -> list[int]:
        """Elements front to back, read straight from buf using the layout in deque.h."""
        raw = self.raw
        return [raw.buf[(raw.front + i) % raw.capacity] for i in range(raw.size)]

    def check(self, result: int) -> int:
        if result == NOT_IMPLEMENTED:
            raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
        return result

    def is_empty(self) -> int:
        return self.check(self.lib.deque_is_empty(self.ptr))

    def is_full(self) -> int:
        return self.check(self.lib.deque_is_full(self.ptr))

    def push_front(self, value: int) -> int:
        return self.check(self.lib.deque_push_front(self.ptr, value))

    def push_back(self, value: int) -> int:
        return self.check(self.lib.deque_push_back(self.ptr, value))

    def _take(self, name: str) -> tuple[int, int]:
        out = ctypes.c_int(12345)
        ok = self.check(getattr(self.lib, name)(self.ptr, ctypes.byref(out)))
        return ok, out.value

    def pop_front(self) -> tuple[int, int]:
        return self._take("deque_pop_front")

    def pop_back(self) -> tuple[int, int]:
        return self._take("deque_pop_back")

    def peek_front(self) -> tuple[int, int]:
        return self._take("deque_peek_front")

    def peek_back(self) -> tuple[int, int]:
        return self._take("deque_peek_back")

    def push_all_back(self, values: list[int]) -> None:
        for value in values:
            assert self.push_back(value) == 1, f"deque_push_back({value}) 가 실패했습니다"

    def free(self) -> None:
        self.lib.deque_free(self.ptr)
        self.ptr = None


@pytest.fixture
def lib():
    return load()


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


def round_robin(lib: ctypes.CDLL, burst: list[int], quantum: int) -> tuple[int, list[int]]:
    n = len(burst)
    burst_buf = (ctypes.c_int * max(n, 1))(*burst)
    out = (ctypes.c_int * max(n, 1))(*([-7] * max(n, 1)))
    written = lib.round_robin(burst_buf, n, quantum, out)
    if written == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return written, list(out[: max(written, 0)])


# --- (a) deque_create / deque_free ------------------------------------------


def test_a_create_starts_empty_with_front_zero(make):
    dq = make(4)
    raw = dq.raw
    assert raw.capacity == 4
    assert raw.size == 0
    assert raw.front == 0
    assert raw.buf, "buf 가 NULL 입니다. capacity 칸짜리 배열을 할당해 주세요"


@pytest.mark.parametrize("capacity", [0, -1])
def test_a_create_rejects_capacity_below_one(lib, capacity):
    assert not lib.deque_create(capacity), "capacity 가 1 보다 작으면 NULL 을 반환해야 합니다"


def test_a_free_accepts_null(lib):
    lib.deque_free(None)


def test_a_free_releases_buf_and_deque(lib):
    before = live_allocations(lib)
    dq = Deque(lib, 5)
    dq.push_all_back([1, 2, 3])
    dq.free()
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"deque_free 뒤에 해제되지 않은 메모리가 {leaked}개 남았습니다"


# --- (b) push / pop / peek ---------------------------------------------------


def test_b_new_deque_is_empty_and_not_full(make):
    dq = make(3)
    assert dq.is_empty() == 1
    assert dq.is_full() == 0


def test_b_push_back_then_pop_front_keeps_order(make):
    dq = make(4)
    dq.push_all_back([1, 2, 3])
    assert dq.contents() == [1, 2, 3]
    assert [dq.pop_front() for _ in range(3)] == [(1, 1), (1, 2), (1, 3)]
    assert dq.is_empty() == 1


def test_b_push_front_then_pop_front_reverses_order(make):
    dq = make(4)
    for value in [1, 2, 3]:
        assert dq.push_front(value) == 1
    assert dq.contents() == [3, 2, 1]
    assert [dq.pop_front() for _ in range(3)] == [(1, 3), (1, 2), (1, 1)]


def test_b_push_back_then_pop_back_reverses_order(make):
    dq = make(4)
    dq.push_all_back([1, 2, 3])
    assert [dq.pop_back() for _ in range(3)] == [(1, 3), (1, 2), (1, 1)]


def test_b_peek_does_not_remove(make):
    dq = make(4)
    dq.push_all_back([7, 8])
    assert dq.peek_front() == (1, 7)
    assert dq.peek_back() == (1, 8)
    assert dq.peek_front() == (1, 7)
    assert dq.raw.size == 2
    assert dq.contents() == [7, 8]


def test_b_empty_deque_rejects_pop_and_peek_and_leaves_out_alone(make):
    dq = make(2)
    assert dq.pop_front() == (0, 12345)
    assert dq.pop_back() == (0, 12345)
    assert dq.peek_front() == (0, 12345)
    assert dq.peek_back() == (0, 12345)
    assert dq.raw.size == 0


def test_b_full_deque_rejects_push(make):
    dq = make(3)
    dq.push_all_back([1, 2, 3])
    assert dq.is_full() == 1
    assert dq.is_empty() == 0
    assert dq.push_back(4) == 0
    assert dq.push_front(0) == 0
    assert dq.contents() == [1, 2, 3]
    assert dq.raw.size == 3


def test_b_push_front_on_empty_wraps_front_to_last_slot(make):
    dq = make(4)
    assert dq.push_front(9) == 1
    raw = dq.raw
    assert raw.front == 3, "front 가 0 일 때 push_front 하면 front 는 capacity - 1 이 됩니다"
    assert raw.buf[3] == 9
    assert raw.size == 1


def test_b_elements_stay_in_place(make):
    dq = make(4)
    dq.push_all_back([1, 2])
    assert dq.push_front(0) == 1
    raw = dq.raw
    assert raw.front == 3
    moved = "원소를 옮기지 말고 front 만 움직이세요"
    assert [raw.buf[3], raw.buf[0], raw.buf[1]] == [0, 1, 2], moved
    assert dq.contents() == [0, 1, 2]


def test_b_push_back_wraps_past_the_end(make):
    dq = make(3)
    dq.push_all_back([1, 2, 3])
    assert dq.pop_front() == (1, 1)
    assert dq.pop_front() == (1, 2)
    assert dq.raw.front == 2
    dq.push_all_back([4, 5])
    raw = dq.raw
    assert [raw.buf[0], raw.buf[1], raw.buf[2]] == [4, 5, 3]
    assert dq.contents() == [3, 4, 5]
    assert dq.is_full() == 1
    assert [dq.pop_front() for _ in range(3)] == [(1, 3), (1, 4), (1, 5)]


def test_b_pop_back_across_the_wrap(make):
    dq = make(3)
    assert dq.push_front(1) == 1
    assert dq.push_front(2) == 1
    dq.push_all_back([3])
    assert dq.contents() == [2, 1, 3]
    assert dq.pop_back() == (1, 3)
    assert dq.pop_back() == (1, 1)
    assert dq.pop_back() == (1, 2)
    assert dq.pop_back() == (0, 12345)


def test_b_queue_keeps_working_after_many_laps(make):
    dq = make(2)
    for value in range(10):
        assert dq.push_back(value) == 1
        assert dq.pop_front() == (1, value)
    dq.push_all_back([10, 11])
    assert dq.contents() == [10, 11]
    assert dq.pop_front() == (1, 10)


def test_b_mixed_operations(make):
    dq = make(5)
    dq.push_all_back([1, 2])
    dq.push_front(0)
    dq.push_back(3)
    assert dq.pop_back() == (1, 3)
    dq.push_front(-1)
    assert dq.pop_front() == (1, -1)
    dq.push_back(4)
    assert dq.contents() == [0, 1, 2, 4]
    assert dq.raw.size == 4


# --- (c) deque_print ---------------------------------------------------------


def test_c_print_lists_front_to_back(capfd, make):
    dq = make(3)
    dq.push_all_back([1, 4])
    dq.push_front(3)
    _, out = native_stdout(capfd, lambda: dq.lib.deque_print(dq.ptr))
    if out.strip() == "NOT_IMPLEMENTED":
        raise NotImplementedError("deque_print is still the stub")
    assert out == "[3, 1, 4]\n"


def test_c_print_after_wrap(capfd, make):
    dq = make(3)
    dq.push_all_back([1, 2, 3])
    dq.pop_front()
    dq.push_back(4)
    _, out = native_stdout(capfd, lambda: dq.lib.deque_print(dq.ptr))
    assert out == "[2, 3, 4]\n"


@pytest.mark.parametrize(("values", "expected"), [([], "[]\n"), ([7], "[7]\n")])
def test_c_print_empty_and_single(capfd, make, values, expected):
    dq = make(2)
    dq.push_all_back(values)
    _, out = native_stdout(capfd, lambda: dq.lib.deque_print(dq.ptr))
    assert out == expected


def test_c_print_does_not_change_the_deque(capfd, make):
    dq = make(3)
    dq.push_all_back([5, 6])
    native_stdout(capfd, lambda: dq.lib.deque_print(dq.ptr))
    assert dq.contents() == [5, 6]


# --- (d) round_robin ---------------------------------------------------------


@pytest.mark.parametrize(
    ("burst", "quantum", "expected"),
    [
        ([5, 2, 4], 2, [1, 2, 0]),
        ([3, 1, 2], 1, [1, 2, 0]),
        ([6, 1, 3, 2], 2, [1, 3, 2, 0]),
        ([4, 3, 5], 10, [0, 1, 2]),
        ([2, 2, 2], 2, [0, 1, 2]),
        ([1, 3, 1, 3], 2, [0, 2, 1, 3]),
        ([1], 3, [0]),
    ],
)
def test_d_round_robin(lib, burst, quantum, expected):
    assert round_robin(lib, burst, quantum) == (len(burst), expected)


def test_d_round_robin_with_no_tasks(lib):
    assert round_robin(lib, [], 2) == (0, [])


@pytest.mark.parametrize("quantum", [0, -2])
def test_d_round_robin_rejects_quantum_below_one(lib, quantum):
    written, _ = round_robin(lib, [3, 1], quantum)
    assert written == -1


def test_d_round_robin_does_not_change_burst(lib):
    burst = (ctypes.c_int * 3)(5, 2, 4)
    out = (ctypes.c_int * 3)()
    written = lib.round_robin(burst, 3, 2, out)
    if written == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    assert list(burst) == [5, 2, 4], "burst 는 const 입니다. 남은 시간은 따로 저장해 주세요"


def test_d_round_robin_frees_what_it_allocates(lib):
    before = live_allocations(lib)
    round_robin(lib, [5, 2, 4], 2)
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"round_robin 이 끝난 뒤 해제되지 않은 메모리가 {leaked}개 남았습니다"


# --- no debug output ---------------------------------------------------------


def test_only_deque_print_prints(capfd, lib):
    def run() -> None:
        dq = Deque(lib, 3)
        dq.push_all_back([1, 2])
        dq.push_front(0)
        dq.is_full()
        dq.is_empty()
        dq.peek_front()
        dq.peek_back()
        dq.pop_front()
        dq.pop_back()
        dq.free()
        round_robin(lib, [5, 2, 4], 2)

    _, out = native_stdout(capfd, run)
    assert out == "", f"deque_print 말고는 아무것도 출력하면 안 됩니다. 출력된 내용:\n{out}"
