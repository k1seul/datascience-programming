"""Week 01 / C (구현) 채점 테스트.

solution.c 를 공유 라이브러리로 빌드해 ctypes 로 직접 호출한다.
"""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    """헤더의 시그니처를 ctypes 에 그대로 알려 준다."""
    lib.list_create.argtypes = []
    lib.list_create.restype = ctypes.c_void_p
    lib.list_destroy.argtypes = [ctypes.c_void_p]
    lib.list_destroy.restype = None
    lib.list_size.argtypes = [ctypes.c_void_p]
    lib.list_size.restype = ctypes.c_int
    lib.list_push_front.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.list_push_front.restype = ctypes.c_int
    lib.list_push_back.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.list_push_back.restype = ctypes.c_int
    lib.list_insert.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    lib.list_insert.restype = ctypes.c_int
    lib.list_remove.argtypes = [ctypes.c_void_p, ctypes.c_int, INT_P]
    lib.list_remove.restype = ctypes.c_int
    lib.list_get.argtypes = [ctypes.c_void_p, ctypes.c_int, INT_P]
    lib.list_get.restype = ctypes.c_int
    lib.list_index_of.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.list_index_of.restype = ctypes.c_int
    lib.list_reverse.argtypes = [ctypes.c_void_p]
    lib.list_reverse.restype = None
    lib.list_to_array.argtypes = [ctypes.c_void_p, INT_P, ctypes.c_int]
    lib.list_to_array.restype = ctypes.c_int
    return lib


class List:
    """C 리스트 핸들을 파이썬에서 편하게 두드리기 위한 얇은 래퍼."""

    def __init__(self, lib: ctypes.CDLL, handle: int) -> None:
        self._lib = lib
        self._handle = handle

    def size(self) -> int:
        return self._lib.list_size(self._handle)

    def push_front(self, value: int) -> int:
        return self._lib.list_push_front(self._handle, value)

    def push_back(self, value: int) -> int:
        return self._lib.list_push_back(self._handle, value)

    def insert(self, index: int, value: int) -> int:
        return self._lib.list_insert(self._handle, index, value)

    def remove(self, index: int) -> tuple[int, int]:
        """(반환코드, 제거된 값) 을 돌려준다."""
        out = ctypes.c_int(0)
        code = self._lib.list_remove(self._handle, index, ctypes.byref(out))
        return code, out.value

    def get(self, index: int) -> tuple[int, int]:
        out = ctypes.c_int(0)
        code = self._lib.list_get(self._handle, index, ctypes.byref(out))
        return code, out.value

    def index_of(self, value: int) -> int:
        return self._lib.list_index_of(self._handle, value)

    def reverse(self) -> None:
        self._lib.list_reverse(self._handle)

    def to_array(self, capacity: int | None = None) -> tuple[int, list[int]]:
        size = self.size()
        cap = capacity if capacity is not None else max(size, 0) + 8
        buf = (ctypes.c_int * max(cap, 1))()
        count = self._lib.list_to_array(self._handle, buf, cap)
        return count, list(buf[: max(count, 0)])

    def to_list(self) -> list[int]:
        count, values = self.to_array()
        assert count >= 0, "list_to_array 가 충분한 용량에도 -1 을 반환했습니다"
        return values

    def extend(self, values: list[int]) -> None:
        for value in values:
            assert self.push_back(value) == 0, f"list_push_back({value}) 이 실패했습니다"


@pytest.fixture
def lst():
    lib = _bind(native_lib(SRC))
    handle = lib.list_create()
    if not handle:
        pytest.fail("list_create() 가 NULL 을 반환했습니다", pytrace=False)
    wrapper = List(lib, handle)
    yield wrapper
    lib.list_destroy(handle)


def test_새_리스트는_비어_있다(lst):
    assert lst.size() == 0
    assert lst.to_list() == []


def test_destroy_는_NULL_을_받아도_안전하다():
    lib = _bind(native_lib(SRC))
    lib.list_destroy(None)


def test_push_back_은_뒤에_붙인다(lst):
    lst.extend([1, 2, 3])
    assert lst.to_list() == [1, 2, 3]
    assert lst.size() == 3


def test_push_front_는_앞에_붙인다(lst):
    for value in [1, 2, 3]:
        assert lst.push_front(value) == 0
    assert lst.to_list() == [3, 2, 1]


def test_insert_는_앞_중간_끝에_모두_들어간다(lst):
    lst.extend([10, 30])
    assert lst.insert(1, 20) == 0
    assert lst.insert(0, 5) == 0
    assert lst.insert(lst.size(), 40) == 0
    assert lst.to_list() == [5, 10, 20, 30, 40]


def test_insert_는_범위를_벗어나면_실패한다(lst):
    lst.extend([1, 2])
    assert lst.insert(3, 99) == -1
    assert lst.insert(-1, 99) == -1
    assert lst.to_list() == [1, 2]


def test_remove_는_값을_돌려주고_링크를_잇는다(lst):
    lst.extend([1, 2, 3, 4])

    assert lst.remove(0) == (0, 1)
    assert lst.to_list() == [2, 3, 4]

    assert lst.remove(1) == (0, 3)
    assert lst.to_list() == [2, 4]

    assert lst.remove(lst.size() - 1) == (0, 4)
    assert lst.to_list() == [2]
    assert lst.size() == 1


def test_remove_는_범위를_벗어나면_실패한다(lst):
    lst.extend([1])
    assert lst.remove(1)[0] == -1
    assert lst.remove(-1)[0] == -1
    assert lst.to_list() == [1]


def test_get(lst):
    lst.extend([7, 8, 9])
    assert lst.get(0) == (0, 7)
    assert lst.get(2) == (0, 9)
    assert lst.get(3)[0] == -1
    assert lst.get(-1)[0] == -1


def test_index_of_는_처음_나온_위치를_준다(lst):
    lst.extend([5, 6, 5, 7])
    assert lst.index_of(5) == 0
    assert lst.index_of(7) == 3
    assert lst.index_of(99) == -1


@pytest.mark.parametrize(
    ("values", "expected"),
    [([], []), ([1], [1]), ([1, 2], [2, 1]), ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])],
)
def test_reverse(lst, values, expected):
    lst.extend(values)
    lst.reverse()
    assert lst.to_list() == expected
    assert lst.size() == len(values)


def test_reverse_후에도_뒤에_계속_붙일_수_있다(lst):
    lst.extend([1, 2, 3])
    lst.reverse()
    lst.push_back(0)
    assert lst.to_list() == [3, 2, 1, 0]


def test_to_array_는_용량이_모자라면_실패한다(lst):
    lst.extend([1, 2, 3])
    count, _ = lst.to_array(capacity=2)
    assert count == -1
    assert lst.to_array(capacity=3) == (3, [1, 2, 3])


def test_섞어서_써도_상태가_유지된다(lst):
    lst.extend([1, 2, 3])
    lst.push_front(0)
    lst.insert(2, 99)
    lst.remove(0)
    lst.reverse()
    assert lst.to_list() == [3, 2, 99, 1]
    assert lst.size() == 4
    assert lst.index_of(99) == 2
