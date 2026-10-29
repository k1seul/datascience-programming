"""Build C / C++ sources into shared libraries and load them with ctypes.

A task's tests only need this module; compilation, caching and rebuild decisions all
happen here. Build artifacts land in build/native/ and a source is only recompiled
when it is newer than the library built from it.
"""

from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build" / "native"
ALLOC_TRACK_HEADER = ROOT / "harness" / "alloc_track.h"
ALLOC_TRACK_SOURCE = ROOT / "harness" / "alloc_track.c"

# suffix -> (environment variable, default compiler, standard flags)
_TOOLCHAIN = {
    ".c": ("CC", "cc", ["-std=c17"]),
    ".cpp": ("CXX", "c++", ["-std=c++17"]),
}

_COMMON_FLAGS = ["-shared", "-fPIC", "-O2", "-Wall", "-Wextra"]

_loaded: dict[Path, ctypes.CDLL] = {}


class CompilerMissing(RuntimeError):
    """The required compiler was not found on PATH."""


class BuildFailed(RuntimeError):
    """Compilation failed. Carries the compiler output verbatim."""


def compiler_for(suffix: str) -> str:
    env_var, default, _ = _TOOLCHAIN[suffix]
    return os.environ.get(env_var) or default


def library_path(src: Path, track_alloc: bool = False) -> Path:
    """One shared library per source, named after its task and suffix to avoid clashes."""
    tag = "_tracked" if track_alloc else ""
    return BUILD_DIR / f"{src.parent.name}_{src.stem}_{src.suffix.lstrip('.')}{tag}.so"


def build(src: Path, track_alloc: bool = False) -> Path:
    """Compile the source if needed and return the path to the shared library.

    With track_alloc, the solution's malloc / calloc / realloc / free are routed through
    alloc_track.c so tests can call harness_live_allocations(). C sources only.
    """
    src = src.resolve()
    if src.suffix not in _TOOLCHAIN:
        raise ValueError(f"unsupported source suffix: {src.suffix}")
    if track_alloc and src.suffix != ".c":
        raise ValueError("allocation tracking is only wired up for C sources")
    if not src.exists():
        raise FileNotFoundError(src)

    compiler = compiler_for(src.suffix)
    if shutil.which(compiler) is None:
        raise CompilerMissing(f"{compiler} was not found on PATH")

    inputs = [src, ALLOC_TRACK_HEADER, ALLOC_TRACK_SOURCE] if track_alloc else [src]
    lib = library_path(src, track_alloc)
    if lib.exists() and lib.stat().st_mtime >= max(p.stat().st_mtime for p in inputs):
        return lib

    lib.parent.mkdir(parents=True, exist_ok=True)
    _, _, std_flags = _TOOLCHAIN[src.suffix]
    cmd = [compiler, *std_flags, *_COMMON_FLAGS]
    if track_alloc:
        cmd += ["-include", str(ALLOC_TRACK_HEADER), str(ALLOC_TRACK_SOURCE)]
    cmd += [str(src), "-o", str(lib)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise BuildFailed(f"$ {' '.join(cmd)}\n{proc.stdout}{proc.stderr}".rstrip())
    return lib


def load(src: Path, track_alloc: bool = False) -> ctypes.CDLL:
    """Build and load a source. Each source is loaded at most once per process."""
    src = src.resolve()
    lib_path = build(src, track_alloc)
    cached = _loaded.get(lib_path)
    if cached is not None:
        return cached
    lib = ctypes.CDLL(str(lib_path))
    _loaded[lib_path] = lib
    return lib
