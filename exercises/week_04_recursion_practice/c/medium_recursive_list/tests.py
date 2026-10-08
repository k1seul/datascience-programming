"""Grading tests for Week 04 / C (medium)."""

from __future__ import annotations

import ctypes
import re
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"


class Node(ctypes.Structure):
    pass


Node._fields_ = [("value", ctypes.c_int), ("next", ctypes.POINTER(Node))]
NodeP = ctypes.POINTER(Node)
INT_P = ctypes.POINTER(ctypes.c_int)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.sum_values.argtypes = [NodeP]
    lib.sum_values.restype = ctypes.c_int
    lib.max_value.argtypes = [NodeP, INT_P]
    lib.max_value.restype = ctypes.c_int
    lib.to_string_reverse.argtypes = [NodeP, ctypes.c_char_p, ctypes.c_int]
    lib.to_string_reverse.restype = ctypes.c_int
    lib.drop_value.argtypes = [NodeP, ctypes.c_int]
    lib.drop_value.restype = NodeP
    return lib


def build(values: list[int]) -> tuple[NodeP, list[Node]]:
    """Build a list in Python-owned memory. The node list must stay referenced."""
    nodes = [Node(value, None) for value in values]
    for current, following in zip(nodes, nodes[1:], strict=False):
        current.next = ctypes.pointer(following)
    head = ctypes.pointer(nodes[0]) if nodes else NodeP()
    return head, nodes


def walk(head: NodeP) -> list[int]:
    values = []
    node = head
    while node:
        values.append(node.contents.value)
        node = node.contents.next
    return values


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self._lib = lib

    def sum_values(self, values: list[int]) -> int:
        head, _keep = build(values)
        return self._lib.sum_values(head)

    def max_value(self, values: list[int]) -> tuple[int, int]:
        head, _keep = build(values)
        out = ctypes.c_int(0)
        code = self._lib.max_value(head, ctypes.byref(out))
        return code, out.value

    def to_string_reverse(self, values: list[int], capacity: int | None = None):
        head, _keep = build(values)
        cap = capacity if capacity is not None else 256
        buf = ctypes.create_string_buffer(max(cap, 1))
        written = self._lib.to_string_reverse(head, buf, cap)
        if written < 0:
            return written, ""
        return written, buf.raw[:written].decode()

    def drop_value(self, values: list[int], x: int) -> list[int]:
        head, _keep = build(values)
        return walk(self._lib.drop_value(head, x))

    def unchanged_after_to_string(self, values: list[int]) -> list[int]:
        head, _keep = build(values)
        buf = ctypes.create_string_buffer(256)
        self._lib.to_string_reverse(head, buf, 256)
        return walk(head)


@pytest.fixture
def api():
    lib = _bind(native_lib(SRC))
    # An untouched stub returns the sentinel here, which marks the task "not written yet".
    if lib.sum_values(NodeP()) == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return Api(lib)


# --- sum_values ------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([5], 5),
        ([1, 2, 3], 6),
        ([-1, 1], 0),
        ([-5, -3, -2], -10),
        ([10, 20, 30, 40], 100),
    ],
)
def test_sum_values(api, values, expected):
    assert api.sum_values(values) == expected


# --- max_value -------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([7], 7),
        ([1, 5, 2], 5),
        ([5, 1, 2], 5),
        ([1, 2, 5], 5),
        ([-5, -1, -3], -1),
        ([4, 4, 4], 4),
    ],
)
def test_max_value(api, values, expected):
    assert api.max_value(values) == (0, expected)


def test_max_value_rejects_an_empty_list(api):
    assert api.max_value([])[0] == -1


# --- to_string_reverse -----------------------------------------------------


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], ""),
        ([1], "1 "),
        ([1, 2], "2 1 "),
        ([1, 2, 3], "3 2 1 "),
        ([-1, 2], "2 -1 "),
        ([10, -20, 30], "30 -20 10 "),
        ([7, 7], "7 7 "),
    ],
)
def test_to_string_reverse(api, values, expected):
    assert api.to_string_reverse(values) == (len(expected), expected)


def test_to_string_reverse_has_a_trailing_space_and_no_newline(api):
    _, text = api.to_string_reverse([1, 2, 3])
    assert text.endswith(" "), "값마다 뒤에 공백 하나가 붙어야 합니다"
    assert "\n" not in text, "개행을 넣지 마세요"


def test_to_string_reverse_rejects_small_capacity(api):
    # "3 2 1 " 는 6글자이므로 NUL 까지 7칸이 필요합니다.
    assert api.to_string_reverse([1, 2, 3], capacity=6)[0] == -1


def test_to_string_reverse_accepts_exact_capacity(api):
    assert api.to_string_reverse([1, 2, 3], capacity=7) == (6, "3 2 1 ")


def test_to_string_reverse_does_not_change_the_list(api):
    assert api.unchanged_after_to_string([1, 2, 3]) == [1, 2, 3]


# --- drop_value ------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "x", "expected"),
    [
        ([], 1, []),
        ([1, 2, 3], 9, [1, 2, 3]),
        ([1, 2, 3], 2, [1, 3]),
        ([1, 2, 3], 1, [2, 3]),
        ([1, 2, 3], 3, [1, 2]),
        ([2, 2, 2], 2, []),
        ([1, 2, 1, 3, 1], 1, [2, 3]),
        ([5, 5, 1, 5], 5, [1]),
        ([1, 1], 1, []),
    ],
)
def test_drop_value(api, values, x, expected):
    assert api.drop_value(values, x) == expected


def test_drop_value_can_remove_the_head(api):
    assert api.drop_value([9, 1, 2], 9) == [1, 2]


# --- 재귀로 썼는지 ---------------------------------------------------------


def test_loops_are_not_used():
    """네 함수 모두 재귀로 써야 합니다."""
    source = SRC.read_text(encoding="utf-8")
    for keyword in ("for", "while", "goto"):
        found = re.search(rf"\b{keyword}\s*[(;]", source)
        assert found is None, f"{keyword} 대신 재귀로 작성해 주세요"
