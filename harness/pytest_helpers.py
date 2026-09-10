"""pytest 안에서 네이티브 구현을 다룰 때 쓰는 어댑터."""

from __future__ import annotations

import ctypes
from collections.abc import Sequence
from pathlib import Path

import pytest

from harness.native import BuildFailed, CompilerMissing, load


def native_lib(src: Path) -> ctypes.CDLL:
    """소스를 빌드해 로드한다.

    컴파일러가 없으면 skip, 제출한 코드가 컴파일되지 않으면 컴파일러 출력과 함께 fail.
    """
    try:
        return load(src)
    except CompilerMissing as exc:
        pytest.skip(str(exc))
    except FileNotFoundError:
        pytest.skip(f"{src.name} 가 아직 없습니다")
    except BuildFailed as exc:
        pytest.fail(f"{src.name} 컴파일 실패:\n{exc}", pytrace=False)


def list_out_call(
    fn: ctypes._CFuncPtr,
    *args: Sequence[int] | int,
    capacity: int | None = None,
) -> list[int]:
    """`int f(... , int *out, int out_capacity)` 규약을 파이썬 호출로 감싼다.

    args 의 정수는 스칼라 인자로, 정수 시퀀스는 `(const int *ptr, int len)` 두 인자로 펼쳐진다.
    반환값이 음수면 오류 신호로 보고 ValueError 를 올리고, 0 이상이면 out 에 쓰인 개수로 본다.

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

    if written < 0:
        raise ValueError(f"네이티브 구현이 오류 코드 {written} 을 반환했습니다")
    if written > cap:
        raise AssertionError(f"버퍼 용량({cap})보다 큰 길이 {written} 를 반환했습니다")
    return list(out[:written])
