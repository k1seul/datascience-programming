"""Grading tests for Week 06 / C (implementation): recently viewed list.

Test names start with the sub-part they grade, (a) to (g) in problem.md. Every check
walks the list through the structs in recent.h, so a prev pointer that was not updated
fails even when next looks right.
"""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import (
    NOT_IMPLEMENTED,
    live_allocations,
    native_lib,
    native_stdout,
    total_allocations,
)

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

# The tests only build short lists. Walking further than this means next loops back.
MAX_WALK = 64


class ItemStruct(ctypes.Structure):
    """Mirror of Item in recent.h."""


ITEM_P = ctypes.POINTER(ItemStruct)
ItemStruct._fields_ = [("id", ctypes.c_int), ("prev", ITEM_P), ("next", ITEM_P)]


class RecentListStruct(ctypes.Structure):
    """Mirror of RecentList in recent.h."""

    _fields_ = [
        ("capacity", ctypes.c_int),
        ("size", ctypes.c_int),
        ("head", ITEM_P),
        ("tail", ITEM_P),
    ]


LIST_P = ctypes.POINTER(RecentListStruct)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    """Mirror the signatures from recent.h onto the loaded library."""
    lib.item_create.argtypes = [ctypes.c_int]
    lib.item_create.restype = ITEM_P
    lib.recent_create.argtypes = [ctypes.c_int]
    lib.recent_create.restype = LIST_P
    lib.recent_free.argtypes = [LIST_P]
    lib.recent_free.restype = None
    lib.recent_push_front.argtypes = [LIST_P, ITEM_P]
    lib.recent_push_front.restype = None
    lib.recent_detach.argtypes = [LIST_P, ITEM_P]
    lib.recent_detach.restype = None
    lib.recent_find.argtypes = [LIST_P, ctypes.c_int]
    lib.recent_find.restype = ITEM_P
    lib.recent_view.argtypes = [LIST_P, ctypes.c_int]
    lib.recent_view.restype = None
    lib.recent_remove.argtypes = [LIST_P, ctypes.c_int]
    lib.recent_remove.restype = ctypes.c_int
    lib.recent_print.argtypes = [LIST_P]
    lib.recent_print.restype = None
    # Items the tests detach are freed with the same counting free the solution uses.
    lib.harness_free.argtypes = [ctypes.c_void_p]
    lib.harness_free.restype = None
    return lib


def addr(ptr: ctypes._Pointer | None) -> int | None:
    """Address a pointer holds, None for NULL."""
    return ctypes.cast(ptr, ctypes.c_void_p).value if ptr else None


def walk(lst: RecentListStruct) -> list[int]:
    """Ids head to tail, checking every prev link, tail and size on the way."""
    ids: list[int] = []
    prev = None
    node = lst.head
    while node:
        assert len(ids) < MAX_WALK, "next 를 따라가도 끝나지 않습니다. 어딘가 고리가 생겼습니다"
        item = node.contents
        if prev is None:
            assert not item.prev, f"맨 앞 노드({item.id})의 prev 는 NULL 이어야 합니다"
        else:
            broken = f"노드 {item.id} 의 prev 가 바로 앞 노드를 가리키지 않습니다"
            assert addr(item.prev) == prev, broken
        ids.append(item.id)
        prev = addr(node)
        node = item.next
    assert addr(lst.tail) == prev, "tail 이 마지막 노드를 가리키지 않습니다"
    assert lst.size == len(ids), f"size 가 {lst.size} 인데 실제 노드는 {len(ids)}개입니다"
    return ids


class Recent:
    """Wraps a RecentList * so the tests read like the C calls they make."""

    def __init__(self, lib: ctypes.CDLL, capacity: int) -> None:
        self.lib = lib
        self.ptr = lib.recent_create(capacity)
        if not self.ptr:
            # The untouched stub returns NULL here, so the grader reads this as "not
            # written yet" rather than as a wrong answer.
            raise NotImplementedError("recent_create() returned NULL")

    @property
    def raw(self) -> RecentListStruct:
        return self.ptr.contents

    def ids(self) -> list[int]:
        return walk(self.raw)

    def push_front(self, *ids: int) -> list[ctypes._Pointer]:
        items = [new_item(self.lib, i) for i in ids]
        for item in items:
            self.lib.recent_push_front(self.ptr, item)
        return items

    def detach(self, item: ctypes._Pointer) -> None:
        self.lib.recent_detach(self.ptr, item)

    def find(self, id_: int) -> ctypes._Pointer:
        return self.lib.recent_find(self.ptr, id_)

    def view(self, *ids: int) -> None:
        for id_ in ids:
            self.lib.recent_view(self.ptr, id_)

    def remove(self, id_: int) -> int:
        result = self.lib.recent_remove(self.ptr, id_)
        if result == NOT_IMPLEMENTED:
            raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
        return result

    def free(self) -> None:
        self.lib.recent_free(self.ptr)
        self.ptr = None


def new_item(lib: ctypes.CDLL, id_: int) -> ctypes._Pointer:
    item = lib.item_create(id_)
    if not item:
        raise NotImplementedError("item_create() returned NULL")
    return item


def free_item(lib: ctypes.CDLL, item: ctypes._Pointer) -> None:
    lib.harness_free(ctypes.cast(item, ctypes.c_void_p))


@pytest.fixture
def lib():
    return _bind(native_lib(SRC, track_alloc=True))


@pytest.fixture
def make(lib):
    made: list[Recent] = []

    def factory(capacity: int) -> Recent:
        lst = Recent(lib, capacity)
        made.append(lst)
        return lst

    yield factory
    for lst in made:
        if lst.ptr:
            lst.free()


def printed(capfd, lst: Recent) -> str:
    _, out = native_stdout(capfd, lambda: lst.lib.recent_print(lst.ptr))
    if out.strip() == "NOT_IMPLEMENTED":
        raise NotImplementedError("recent_print is still the stub")
    return out


# --- (a) item_create / recent_create / recent_free ---------------------------


def test_a_item_create_sets_id_and_clears_links(lib):
    item = new_item(lib, 5)
    assert item.contents.id == 5
    assert not item.contents.prev, "새 노드의 prev 는 NULL 이어야 합니다"
    assert not item.contents.next, "새 노드의 next 는 NULL 이어야 합니다"
    free_item(lib, item)


def test_a_recent_create_starts_empty(make):
    lst = make(3)
    assert lst.raw.capacity == 3
    assert lst.raw.size == 0
    assert not lst.raw.head
    assert not lst.raw.tail


@pytest.mark.parametrize("capacity", [0, -2])
def test_a_recent_create_rejects_capacity_below_one(lib, capacity):
    assert not lib.recent_create(capacity), "capacity 가 1 보다 작으면 NULL 을 반환해야 합니다"


def test_a_free_accepts_null(lib):
    lib.recent_free(None)


def test_a_free_releases_an_empty_list(lib):
    before = live_allocations(lib)
    Recent(lib, 3).free()
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"recent_free 뒤에 해제되지 않은 메모리가 {leaked}개 남았습니다"


def test_a_free_releases_every_item(lib):
    before = live_allocations(lib)
    lst = Recent(lib, 3)
    lst.push_front(1, 2, 3)
    lst.free()
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"recent_free 뒤에 해제되지 않은 메모리가 {leaked}개 남았습니다"


# --- (b) recent_push_front ---------------------------------------------------


def test_b_push_front_on_empty_list(make):
    lst = make(3)
    (item,) = lst.push_front(7)
    assert addr(lst.raw.head) == addr(item)
    assert addr(lst.raw.tail) == addr(item), "노드가 하나뿐이면 head 와 tail 이 같은 노드입니다"
    assert lst.ids() == [7]


def test_b_push_front_puts_newest_first(make):
    lst = make(3)
    lst.push_front(1, 2, 3)
    assert lst.ids() == [3, 2, 1]


def test_b_push_front_ignores_capacity(make):
    lst = make(1)
    lst.push_front(1, 2)
    assert lst.ids() == [2, 1]


# --- (c) recent_detach -------------------------------------------------------


def test_c_detach_middle(lib, make):
    lst = make(3)
    _, two, _ = lst.push_front(1, 2, 3)
    lst.detach(two)
    assert lst.ids() == [3, 1]
    assert not two.contents.prev and not two.contents.next, "떼어 낸 노드의 prev, next 는 NULL 로"
    free_item(lib, two)


def test_c_detach_head(lib, make):
    lst = make(3)
    _, _, three = lst.push_front(1, 2, 3)
    lst.detach(three)
    assert lst.ids() == [2, 1]
    free_item(lib, three)


def test_c_detach_tail(lib, make):
    lst = make(3)
    one, _, _ = lst.push_front(1, 2, 3)
    lst.detach(one)
    assert lst.ids() == [3, 2]
    free_item(lib, one)


def test_c_detach_only_item_empties_the_list(lib, make):
    lst = make(3)
    (only,) = lst.push_front(4)
    lst.detach(only)
    assert lst.ids() == []
    assert not lst.raw.head and not lst.raw.tail
    free_item(lib, only)


def test_c_detach_does_not_free(lib, make):
    lst = make(3)
    _, two, _ = lst.push_front(1, 2, 3)
    before = live_allocations(lib)
    lst.detach(two)
    freed = "recent_detach 는 노드를 떼어 내기만 하고 해제하지 않습니다"
    assert live_allocations(lib) == before, freed
    free_item(lib, two)


def test_c_detached_item_can_go_back_to_the_front(make):
    lst = make(3)
    _, two, _ = lst.push_front(1, 2, 3)
    lst.detach(two)
    lst.lib.recent_push_front(lst.ptr, two)
    assert lst.ids() == [2, 3, 1]


# --- (d) recent_find ---------------------------------------------------------


def test_d_find_returns_the_item_itself(make):
    lst = make(3)
    one, two, three = lst.push_front(1, 2, 3)
    assert addr(lst.find(1)) == addr(one)
    assert addr(lst.find(2)) == addr(two)
    assert addr(lst.find(3)) == addr(three)


def test_d_find_returns_null_when_absent(make):
    lst = make(3)
    assert not lst.find(1), "빈 목록에서는 NULL 입니다"
    lst.push_front(1, 2)
    assert not lst.find(9)


# --- (e) recent_view ---------------------------------------------------------


def test_e_view_new_ids_go_to_the_front(make):
    lst = make(3)
    lst.view(1, 2, 3)
    assert lst.ids() == [3, 2, 1]


def test_e_view_moves_an_existing_id_to_the_front(make):
    lst = make(3)
    lst.view(1, 2, 3)
    lst.view(2)
    assert lst.ids() == [2, 3, 1]
    lst.view(1)
    assert lst.ids() == [1, 2, 3]
    lst.view(1)
    assert lst.ids() == [1, 2, 3]


def test_e_view_reuses_the_existing_item(lib, make):
    lst = make(3)
    lst.view(1, 2, 3)
    item = addr(lst.find(2))
    before = total_allocations(lib)
    lst.view(2)
    # free + malloc can hand back the very same address, so count allocations instead.
    recreated = "이미 있는 상품은 새 노드를 만들지 말고 그 노드를 옮기세요"
    assert total_allocations(lib) == before, recreated
    assert addr(lst.find(2)) == item


def test_e_view_evicts_the_oldest(make):
    lst = make(3)
    lst.view(1, 2, 3, 4)
    assert lst.ids() == [4, 3, 2]
    assert not lst.find(1)


def test_e_view_frees_the_evicted_item(lib, make):
    lst = make(3)
    lst.view(1, 2, 3)
    full = live_allocations(lib)
    lst.view(4, 5, 6, 7)
    leaked = live_allocations(lib) - full
    assert leaked == 0, f"밀려난 노드 {leaked}개를 해제하지 않았습니다"
    assert lst.ids() == [7, 6, 5]


def test_e_view_existing_id_in_a_full_list_evicts_nothing(make):
    lst = make(3)
    lst.view(1, 2, 3)
    lst.view(1)
    assert lst.ids() == [1, 3, 2]


def test_e_view_with_capacity_one(make):
    lst = make(1)
    lst.view(5)
    assert lst.ids() == [5]
    lst.view(6)
    assert lst.ids() == [6]
    lst.view(6)
    assert lst.ids() == [6]


def test_e_view_sequence(make):
    lst = make(4)
    lst.view(1, 2, 3, 2, 4, 5, 1)
    assert lst.ids() == [1, 5, 4, 2]


# --- (f) recent_remove -------------------------------------------------------


def test_f_remove_from_middle_head_and_tail(make):
    lst = make(4)
    lst.view(1, 2, 3, 4)
    assert lst.remove(2) == 1
    assert lst.ids() == [4, 3, 1]
    assert lst.remove(4) == 1
    assert lst.ids() == [3, 1]
    assert lst.remove(1) == 1
    assert lst.ids() == [3]
    assert lst.remove(3) == 1
    assert lst.ids() == []


def test_f_remove_absent_id(make):
    lst = make(3)
    assert lst.remove(1) == 0
    lst.view(1, 2)
    assert lst.remove(9) == 0
    assert lst.ids() == [2, 1]


def test_f_remove_frees_the_item(lib, make):
    lst = make(3)
    lst.view(1, 2, 3)
    before = live_allocations(lib)
    lst.remove(2)
    assert live_allocations(lib) == before - 1, "지운 노드를 해제해 주세요"


def test_f_removing_makes_room(make):
    lst = make(3)
    lst.view(1, 2, 3)
    lst.remove(1)
    lst.view(4)
    assert lst.ids() == [4, 3, 2]


# --- (g) recent_print --------------------------------------------------------


def test_g_print_head_to_tail(capfd, make):
    lst = make(3)
    lst.view(9, 2, 5)
    assert printed(capfd, lst) == "5 -> 2 -> 9\n"


def test_g_print_single_item(capfd, make):
    lst = make(3)
    lst.view(7)
    assert printed(capfd, lst) == "7\n"


def test_g_print_empty(capfd, make):
    lst = make(3)
    assert printed(capfd, lst) == "(empty)\n"


def test_g_print_after_moves_and_removal(capfd, make):
    lst = make(3)
    lst.view(1, 2, 3, 1)
    lst.remove(2)
    assert printed(capfd, lst) == "1 -> 3\n"
    assert lst.ids() == [1, 3]


# --- no debug output ---------------------------------------------------------


def test_only_recent_print_prints(capfd, lib):
    def run() -> None:
        lst = Recent(lib, 2)
        lst.view(1, 2, 1, 3)
        lst.find(1)
        lst.remove(3)
        lst.free()

    _, out = native_stdout(capfd, run)
    assert out == "", f"recent_print 말고는 아무것도 출력하면 안 됩니다. 출력된 내용:\n{out}"
