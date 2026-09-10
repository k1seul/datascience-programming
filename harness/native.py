"""C / C++ 소스를 공유 라이브러리로 빌드해 ctypes로 불러오는 헬퍼.

각 주차의 tests.py는 이 모듈만 쓰면 되고, 컴파일·캐싱·재빌드 판단은 전부 여기서 처리한다.
빌드 산출물은 build/native/ 아래에 모이며 소스가 바뀌었을 때만 다시 컴파일한다.
"""

from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build" / "native"

# (컴파일러 환경변수, 기본 실행파일, 표준 플래그)
_TOOLCHAIN = {
    ".c": ("CC", "cc", ["-std=c17"]),
    ".cpp": ("CXX", "c++", ["-std=c++17"]),
}

_COMMON_FLAGS = ["-shared", "-fPIC", "-O2", "-Wall", "-Wextra"]

_loaded: dict[Path, ctypes.CDLL] = {}


class CompilerMissing(RuntimeError):
    """요구되는 컴파일러를 PATH에서 찾지 못했을 때."""


class BuildFailed(RuntimeError):
    """컴파일이 실패했을 때. 컴파일러 출력을 그대로 담는다."""


def compiler_for(suffix: str) -> str:
    env_var, default, _ = _TOOLCHAIN[suffix]
    return os.environ.get(env_var) or default


def library_path(src: Path) -> Path:
    """소스 하나당 하나의 .so 경로. 주차와 확장자를 이름에 넣어 충돌을 막는다."""
    return BUILD_DIR / f"{src.parent.name}_{src.stem}_{src.suffix.lstrip('.')}.so"


def build(src: Path) -> Path:
    """필요할 때만 컴파일하고 공유 라이브러리 경로를 돌려준다."""
    src = src.resolve()
    if src.suffix not in _TOOLCHAIN:
        raise ValueError(f"지원하지 않는 소스 확장자: {src.suffix}")
    if not src.exists():
        raise FileNotFoundError(src)

    compiler = compiler_for(src.suffix)
    if shutil.which(compiler) is None:
        raise CompilerMissing(f"{compiler} 를 PATH에서 찾을 수 없습니다")

    lib = library_path(src)
    if lib.exists() and lib.stat().st_mtime >= src.stat().st_mtime:
        return lib

    lib.parent.mkdir(parents=True, exist_ok=True)
    _, _, std_flags = _TOOLCHAIN[src.suffix]
    cmd = [compiler, *std_flags, *_COMMON_FLAGS, str(src), "-o", str(lib)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise BuildFailed(f"$ {' '.join(cmd)}\n{proc.stdout}{proc.stderr}".rstrip())
    return lib


def load(src: Path) -> ctypes.CDLL:
    """소스를 빌드해서 로드한다. 같은 소스는 프로세스 안에서 한 번만 로드한다."""
    src = src.resolve()
    lib_path = build(src)
    cached = _loaded.get(src)
    if cached is not None:
        return cached
    lib = ctypes.CDLL(str(lib_path))
    _loaded[src] = lib
    return lib
