"""Grading tests for Week 08 / C++ (medium): Fraction and a Shape hierarchy.

The classes live in solution.hpp. shim.cpp includes it and exposes plain C functions,
which is what ctypes can call; it is built instead of a solution.cpp.
"""

from __future__ import annotations

import ctypes
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, native_lib

HERE = Path(__file__).resolve().parent
SRC = HERE / "shim.cpp"

INT_P = ctypes.POINTER(ctypes.c_int)
STUB_TEXT = "NOT_IMPLEMENTED"

RECTANGLE, SQUARE = 0, 1
ADD, MUL = 0, 1


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    lib.fraction_make.argtypes = [ctypes.c_int, ctypes.c_int, INT_P, INT_P]
    lib.fraction_make.restype = None
    lib.fraction_op.argtypes = [ctypes.c_int] * 5 + [INT_P, INT_P]
    lib.fraction_op.restype = None
    lib.fraction_equal.argtypes = [ctypes.c_int] * 4
    lib.fraction_equal.restype = ctypes.c_int
    lib.fraction_text.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    lib.fraction_text.restype = ctypes.c_int
    for name in ("shape_area", "shape_area_via_base"):
        getattr(lib, name).argtypes = [ctypes.c_int] * 3
        getattr(lib, name).restype = ctypes.c_double
    for name in ("shape_name", "shape_name_via_base", "shape_text"):
        getattr(lib, name).argtypes = [ctypes.c_int] * 3 + [ctypes.c_char_p, ctypes.c_int]
        getattr(lib, name).restype = ctypes.c_int
    lib.square_sides.argtypes = [ctypes.c_int, INT_P, INT_P]
    lib.square_sides.restype = None
    return lib


def text_of(fn, *args: int) -> str:
    buf = ctypes.create_string_buffer(256)
    fn(*args, buf, len(buf))
    return buf.value.decode()


def not_written(value: object) -> bool:
    return value in (NOT_IMPLEMENTED, STUB_TEXT)


class Api:
    def __init__(self, lib: ctypes.CDLL) -> None:
        self.lib = lib

    # ---- Fraction ----

    def make(self, num: int, den: int) -> tuple[int, int]:
        n, d = ctypes.c_int(), ctypes.c_int()
        self.lib.fraction_make(num, den, ctypes.byref(n), ctypes.byref(d))
        if not_written(n.value):
            raise NotImplementedError("the Fraction constructor is still the stub")
        return n.value, d.value

    def op(self, op: int, a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        self.make(*a)
        n, d = ctypes.c_int(), ctypes.c_int()
        self.lib.fraction_op(op, *a, *b, ctypes.byref(n), ctypes.byref(d))
        if not_written(n.value):
            raise NotImplementedError("this Fraction operator is still the stub")
        return n.value, d.value

    def equal(self, a: tuple[int, int], b: tuple[int, int]) -> bool:
        self.make(*a)
        return bool(self.lib.fraction_equal(*a, *b))

    def text(self, num: int, den: int) -> str:
        out = text_of(self.lib.fraction_text, num, den)
        if not_written(out):
            raise NotImplementedError("operator<< for Fraction is still the stub")
        return out

    # ---- Shapes ----

    def area(self, kind: int, a: int, b: int = 0) -> float:
        value = self.lib.shape_area(kind, a, b)
        if not_written(value):
            raise NotImplementedError("area() is still the stub")
        return value

    def area_via_base(self, kind: int, a: int, b: int = 0) -> float:
        direct = self.area(kind, a, b)
        value = self.lib.shape_area_via_base(kind, a, b)
        assert not not_written(value), (
            f"Shape & 로 부르니 {direct} 가 아니라 Shape 의 area() 가 불렸습니다. "
            "Shape 의 area() 를 virtual 로 만들었나요?"
        )
        return value

    def name(self, kind: int, a: int, b: int = 0) -> str:
        out = text_of(self.lib.shape_name, kind, a, b)
        if not_written(out):
            raise NotImplementedError("name() is still the stub")
        return out

    def name_via_base(self, kind: int, a: int, b: int = 0) -> str:
        direct = self.name(kind, a, b)
        out = text_of(self.lib.shape_name_via_base, kind, a, b)
        assert not not_written(out), (
            f"Shape & 로 부르니 {direct!r} 가 아니라 Shape 의 name() 이 불렸습니다. "
            "Shape 의 name() 을 virtual 로 만들었나요?"
        )
        return out

    def text_shape(self, kind: int, a: int, b: int = 0) -> str:
        out = text_of(self.lib.shape_text, kind, a, b)
        if not_written(out):
            raise NotImplementedError("operator<< for Shape is still the stub")
        return out


@pytest.fixture
def api():
    return Api(_bind(native_lib(SRC)))


# --- (a) Fraction ----------------------------------------------------------


@pytest.mark.parametrize(
    ("num", "den", "expected"),
    [
        (1, 2, (1, 2)),
        (2, 4, (1, 2)),
        (6, 3, (2, 1)),
        (1, -2, (-1, 2)),
        (-3, -9, (1, 3)),
        (0, 5, (0, 1)),
        (-4, 6, (-2, 3)),
    ],
)
def test_a_constructor_reduces(api, num, den, expected):
    assert api.make(num, den) == expected


@pytest.mark.parametrize(
    ("op", "a", "b", "expected"),
    [
        (ADD, (1, 2), (1, 3), (5, 6)),
        (ADD, (1, 4), (1, 4), (1, 2)),
        (ADD, (1, 2), (-1, 2), (0, 1)),
        (ADD, (-1, 3), (1, 6), (-1, 6)),
        (MUL, (2, 3), (3, 4), (1, 2)),
        (MUL, (-1, 2), (2, 5), (-1, 5)),
        (MUL, (5, 7), (0, 1), (0, 1)),
    ],
)
def test_a_operators(api, op, a, b, expected):
    assert api.op(op, a, b) == expected


def test_a_equality_compares_values(api):
    assert api.equal((1, 2), (2, 4)) is True
    assert api.equal((1, 2), (1, 3)) is False
    assert api.equal((-1, 2), (1, -2)) is True
    assert api.equal((1, 2), (2, 1)) is False


@pytest.mark.parametrize(
    ("num", "den", "expected"),
    [(1, 2, "1/2"), (-3, 4, "-3/4"), (3, -4, "-3/4"), (4, 2, "2"), (0, 7, "0"), (-6, 3, "-2")],
)
def test_a_print(api, num, den, expected):
    assert api.text(num, den) == expected


# --- (b) Shapes ------------------------------------------------------------


@pytest.mark.parametrize(
    ("shape", "expected"),
    [((RECTANGLE, 3, 4), 12.0), ((RECTANGLE, 5, 1), 5.0), ((SQUARE, 3), 9.0)],
)
def test_b_area(api, shape, expected):
    assert api.area(*shape) == expected


@pytest.mark.parametrize(
    ("shape", "expected"),
    [((RECTANGLE, 3, 4), "Rectangle"), ((SQUARE, 3), "Square")],
)
def test_b_name(api, shape, expected):
    assert api.name(*shape) == expected


def test_b_square_calls_the_rectangle_constructor(api):
    api.area(SQUARE, 3)
    width, height = ctypes.c_int(), ctypes.c_int()
    api.lib.square_sides(5, ctypes.byref(width), ctypes.byref(height))
    sides = "Square(5) 의 width 와 height 는 둘 다 5 여야 합니다"
    assert (width.value, height.value) == (5, 5), sides


@pytest.mark.parametrize(
    ("shape", "area", "name"),
    [((RECTANGLE, 3, 4), 12.0, "Rectangle"), ((SQUARE, 3), 9.0, "Square")],
)
def test_b_virtual_through_shape(api, shape, area, name):
    assert api.area_via_base(*shape) == area
    assert api.name_via_base(*shape) == name


@pytest.mark.parametrize(
    ("shape", "expected"),
    [
        ((RECTANGLE, 3, 4), "Rectangle(12.0)"),
        ((SQUARE, 3), "Square(9.0)"),
        ((RECTANGLE, 1, 1), "Rectangle(1.0)"),
    ],
)
def test_b_print(api, shape, expected):
    assert api.text_shape(*shape) == expected
