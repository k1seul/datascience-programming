"""Adapters for calling native implementations from inside pytest."""

from __future__ import annotations

import ctypes
from collections.abc import Sequence
from pathlib import Path

import pytest

from harness.native import BuildFailed, CompilerMissing, load

# Untouched C / C++ stubs return this instead of a plausible error code, so the grader
# can tell "not written yet" apart from "written and wrong". Keep it in sync with the
# NOT_IMPLEMENTED define in the stub files.
NOT_IMPLEMENTED = -1000


def native_lib(src: Path) -> ctypes.CDLL:
    """Build and load a source.

    Skips the test when no compiler is available, and fails it with the compiler
    output when the submitted code does not compile.
    """
    try:
        return load(src)
    except CompilerMissing as exc:
        pytest.skip(str(exc))
    except FileNotFoundError:
        pytest.skip(f"{src.name} does not exist yet")
    except BuildFailed as exc:
        pytest.fail(f"{src.name} failed to compile:\n{exc}", pytrace=False)


def list_out_call(
    fn: ctypes._CFuncPtr,
    *args: Sequence[int] | int,
    capacity: int | None = None,
) -> list[int]:
    """Wrap the `int f(..., int *out, int out_capacity)` convention as a Python call.

    Integers in `args` are passed as scalars; integer sequences expand into a
    `(const int *ptr, int len)` pair. A negative return value is treated as an error
    signal and raises ValueError; otherwise it is the number of items written to out.

        list_out_call(lib.reverse_groups, [1, 2, 3, 4], 2)
        # -> int reverse_groups(const int *values, int n, int k, int *out, int cap)
    """
    argtypes: list[type] = []
    values: list[object] = []
    total = 0

    for arg in args:
        if isinstance(arg, int):
            argtypes.append(ctypes.c_int)
            values.append(arg)
            continue
        buf = (ctypes.c_int * len(arg))(*arg)
        argtypes += [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        values += [buf, len(arg)]
        total += len(arg)

    cap = capacity if capacity is not None else max(16, total + 8)
    out = (ctypes.c_int * cap)()
    argtypes += [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

    fn.argtypes = argtypes
    fn.restype = ctypes.c_int
    written = fn(*values, out, cap)

    if written == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    if written < 0:
        raise ValueError(f"the native implementation returned error code {written}")
    if written > cap:
        raise AssertionError(f"returned length {written} exceeds the buffer capacity {cap}")
    return list(out[:written])
