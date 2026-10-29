"""Grading tests for Week 06 / C (implementation): graph search.

Test names start with the sub-part they grade, (a) to (e) in problem.md.
"""

from __future__ import annotations

import ctypes
from collections.abc import Sequence
from pathlib import Path

import pytest

from harness import NOT_IMPLEMENTED, live_allocations, native_lib, native_stdout

HERE = Path(__file__).resolve().parent
SRC = HERE / "solution.c"

INT_P = ctypes.POINTER(ctypes.c_int)

# The tests only build small graphs. A list longer than this means next loops back.
MAX_WALK = 64

# Six vertices, 5 is on its own:
#     0 -> 1 -> 3 -> 4
#     0 -> 2 -> 3
G1_N = 6
G1 = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
TRIANGLE = [(0, 1), (1, 2), (2, 0)]
DIAMOND = [(0, 1), (0, 2), (1, 3), (2, 3)]


class EdgeStruct(ctypes.Structure):
    """Mirror of Edge in graph.h."""


EDGE_P = ctypes.POINTER(EdgeStruct)
EdgeStruct._fields_ = [("to", ctypes.c_int), ("next", EDGE_P)]


class GraphStruct(ctypes.Structure):
    """Mirror of Graph in graph.h."""

    _fields_ = [("n", ctypes.c_int), ("adj", ctypes.POINTER(EDGE_P))]


GRAPH_P = ctypes.POINTER(GraphStruct)


def _bind(lib: ctypes.CDLL) -> ctypes.CDLL:
    """Mirror the signatures from graph.h onto the loaded library."""
    lib.graph_create.argtypes = [ctypes.c_int]
    lib.graph_create.restype = GRAPH_P
    lib.graph_add_edge.argtypes = [GRAPH_P, ctypes.c_int, ctypes.c_int]
    lib.graph_add_edge.restype = ctypes.c_int
    lib.graph_free.argtypes = [GRAPH_P]
    lib.graph_free.restype = None
    lib.graph_print.argtypes = [GRAPH_P]
    lib.graph_print.restype = None
    for name in ("graph_bfs_distance", "graph_dfs_order"):
        getattr(lib, name).argtypes = [GRAPH_P, ctypes.c_int, INT_P]
        getattr(lib, name).restype = ctypes.c_int
    lib.graph_has_cycle.argtypes = [GRAPH_P]
    lib.graph_has_cycle.restype = ctypes.c_int
    return lib


def check(result: int) -> int:
    if result == NOT_IMPLEMENTED:
        raise NotImplementedError("the stub is still returning NOT_IMPLEMENTED")
    return result


class Graph:
    """Wraps a Graph * so the tests read like the C calls they make."""

    def __init__(self, lib: ctypes.CDLL, n: int, edges: Sequence[tuple[int, int]] = ()) -> None:
        self.lib = lib
        self.ptr = lib.graph_create(n)
        if not self.ptr:
            # The untouched stub returns NULL here, so the grader reads this as "not
            # written yet" rather than as a wrong answer.
            raise NotImplementedError("graph_create() returned NULL")
        for u, v in edges:
            assert self.add_edge(u, v) == 1, f"graph_add_edge({u}, {v}) 가 실패했습니다"

    @property
    def raw(self) -> GraphStruct:
        return self.ptr.contents

    def add_edge(self, u: int, v: int) -> int:
        return check(self.lib.graph_add_edge(self.ptr, u, v))

    def adjacency(self) -> list[list[int]]:
        """Every vertex's out-neighbours, read straight from the Edge lists."""
        raw = self.raw
        lists = []
        for v in range(raw.n):
            targets = []
            edge = raw.adj[v]
            while edge:
                assert len(targets) < MAX_WALK, f"adj[{v}] 의 next 를 따라가도 끝나지 않습니다"
                targets.append(edge.contents.to)
                edge = edge.contents.next
            lists.append(targets)
        return lists

    def bfs(self, start: int) -> tuple[int, list[int]]:
        dist = (ctypes.c_int * self.raw.n)(*([77] * self.raw.n))
        reached = check(self.lib.graph_bfs_distance(self.ptr, start, dist))
        return reached, list(dist)

    def dfs(self, start: int) -> tuple[int, list[int]]:
        order = (ctypes.c_int * self.raw.n)(*([77] * self.raw.n))
        visited = check(self.lib.graph_dfs_order(self.ptr, start, order))
        return visited, list(order[: max(visited, 0)])

    def has_cycle(self) -> int:
        return check(self.lib.graph_has_cycle(self.ptr))

    def free(self) -> None:
        self.lib.graph_free(self.ptr)
        self.ptr = None


@pytest.fixture
def lib():
    return _bind(native_lib(SRC, track_alloc=True))


@pytest.fixture
def make(lib):
    made: list[Graph] = []

    def factory(n: int, edges: Sequence[tuple[int, int]] = ()) -> Graph:
        g = Graph(lib, n, edges)
        made.append(g)
        return g

    yield factory
    for g in made:
        if g.ptr:
            g.free()


def printed(capfd, g: Graph) -> str:
    _, out = native_stdout(capfd, lambda: g.lib.graph_print(g.ptr))
    if out.strip() == "NOT_IMPLEMENTED":
        raise NotImplementedError("graph_print is still the stub")
    return out


def assert_no_leak(lib: ctypes.CDLL, before: int, what: str) -> None:
    leaked = live_allocations(lib) - before
    assert leaked == 0, f"{what} 뒤에 해제되지 않은 메모리가 {leaked}개 남았습니다"


# --- (a) graph_create / graph_add_edge / graph_free --------------------------


def test_a_create_has_no_edges(make):
    g = make(4)
    raw = g.raw
    assert raw.n == 4
    assert raw.adj, "adj 가 NULL 입니다. n 칸짜리 포인터 배열을 할당해 주세요"
    assert g.adjacency() == [[], [], [], []], "처음에는 adj[v] 가 모두 NULL 이어야 합니다"


@pytest.mark.parametrize("n", [0, -1])
def test_a_create_rejects_n_below_one(lib, n):
    assert not lib.graph_create(n), "n 이 1 보다 작으면 NULL 을 반환해야 합니다"


def test_a_add_edge_appends_in_order(make):
    g = make(4, [(0, 2), (0, 1), (0, 3), (2, 0)])
    assert g.adjacency() == [[2, 1, 3], [], [0], []], "간선은 목록의 맨 뒤에 붙여야 합니다"


@pytest.mark.parametrize(("u", "v"), [(-1, 0), (0, -1), (4, 0), (0, 4)])
def test_a_add_edge_rejects_missing_vertices(make, u, v):
    g = make(4)
    assert g.add_edge(u, v) == 0
    assert g.adjacency() == [[], [], [], []]


def test_a_add_edge_keeps_self_loops_and_repeats(make):
    g = make(2, [(1, 1), (1, 0), (1, 1)])
    assert g.adjacency() == [[], [1, 0, 1]]


def test_a_free_accepts_null(lib):
    lib.graph_free(None)


def test_a_free_releases_everything(lib):
    before = live_allocations(lib)
    Graph(lib, 3).free()
    assert_no_leak(lib, before, "간선 없는 그래프의 graph_free")

    before = live_allocations(lib)
    Graph(lib, G1_N, G1).free()
    assert_no_leak(lib, before, "graph_free")


# --- (b) graph_print ---------------------------------------------------------


def test_b_print_one_line_per_vertex(capfd, make):
    g = make(4, [(0, 1), (0, 2), (2, 3)])
    assert printed(capfd, g) == "0: 1 2\n1:\n2: 3\n3:\n"


def test_b_print_single_vertex(capfd, make):
    g = make(1)
    assert printed(capfd, g) == "0:\n"


def test_b_print_keeps_list_order(capfd, make):
    g = make(3, [(1, 1), (1, 0), (2, 1), (0, 2)])
    assert printed(capfd, g) == "0: 2\n1: 1 0\n2: 1\n"


# --- (c) graph_bfs_distance --------------------------------------------------


@pytest.mark.parametrize(
    ("start", "expected"),
    [
        (0, (5, [0, 1, 1, 2, 3, -1])),
        (3, (2, [-1, -1, -1, 0, 1, -1])),
        (5, (1, [-1, -1, -1, -1, -1, 0])),
    ],
)
def test_c_bfs_distance(make, start, expected):
    g = make(G1_N, G1)
    assert g.bfs(start) == expected


def test_c_bfs_takes_the_fewest_edges(make):
    g = make(4, [(0, 1), (1, 2), (2, 3), (0, 3)])
    assert g.bfs(0) == (4, [0, 1, 2, 1]), "0 -> 3 은 간선 하나로 갈 수 있습니다"


def test_c_bfs_around_a_cycle(make):
    g = make(3, TRIANGLE)
    assert g.bfs(1) == (3, [2, 0, 1])


def test_c_bfs_follows_edge_direction(make):
    g = make(2, [(1, 0)])
    assert g.bfs(0) == (1, [0, -1])
    assert g.bfs(1) == (2, [1, 0])


@pytest.mark.parametrize("start", [-1, 6])
def test_c_bfs_rejects_missing_start(make, start):
    g = make(G1_N, G1)
    assert g.bfs(start) == (-1, [77] * G1_N), "start 가 없는 정점이면 dist 를 건드리지 마세요"


def test_c_bfs_frees_its_queue(lib, make):
    g = make(G1_N, G1)
    before = live_allocations(lib)
    g.bfs(0)
    assert_no_leak(lib, before, "graph_bfs_distance")


# --- (d) graph_dfs_order -----------------------------------------------------


@pytest.mark.parametrize(
    ("edges", "start", "expected"),
    [
        (G1, 0, [0, 1, 3, 4, 2]),
        ([(0, 2), (0, 1), (1, 3), (2, 3), (3, 4)], 0, [0, 2, 3, 4, 1]),
        (G1, 2, [2, 3, 4]),
        (G1, 5, [5]),
    ],
)
def test_d_dfs_order(make, edges, start, expected):
    g = make(G1_N, edges)
    assert g.dfs(start) == (len(expected), expected)


def test_d_dfs_goes_deep_before_wide(make):
    g = make(G1_N, G1)
    _, order = g.dfs(0)
    assert order != [0, 1, 2, 3, 4], "가까운 정점부터 방문했습니다. 그건 BFS 순서입니다"
    assert order == [0, 1, 3, 4, 2]


def test_d_dfs_around_a_cycle(make):
    g = make(3, TRIANGLE)
    assert g.dfs(1) == (3, [1, 2, 0])


def test_d_dfs_skips_self_loop(make):
    g = make(2, [(0, 0), (0, 1)])
    assert g.dfs(0) == (2, [0, 1])


@pytest.mark.parametrize("start", [-1, 6])
def test_d_dfs_rejects_missing_start(make, start):
    g = make(G1_N, G1)
    visited, _ = g.dfs(start)
    assert visited == -1


def test_d_dfs_frees_what_it_allocates(lib, make):
    g = make(G1_N, G1)
    before = live_allocations(lib)
    g.dfs(0)
    assert_no_leak(lib, before, "graph_dfs_order")


# --- (e) graph_has_cycle -----------------------------------------------------


@pytest.mark.parametrize(
    ("n", "edges", "expected"),
    [
        (G1_N, G1, 0),
        (3, TRIANGLE, 1),
        (1, [(0, 0)], 1),
        (2, [(0, 1), (1, 0)], 1),
        (4, [(0, 1), (1, 2), (2, 3), (3, 1)], 1),
        (3, [], 0),
        (3, [(0, 1), (2, 1)], 0),
    ],
)
def test_e_has_cycle(make, n, edges, expected):
    g = make(n, edges)
    assert g.has_cycle() == expected


def test_e_meeting_a_vertex_twice_is_not_a_cycle(make):
    g = make(4, DIAMOND)
    assert g.has_cycle() == 0, "0->1->3 과 0->2->3 으로 3 을 두 번 만나지만 사이클은 아닙니다"


def test_e_edge_into_an_already_finished_part_is_not_a_cycle(make):
    g = make(4, [(0, 1), (2, 1), (2, 3), (3, 0)])
    assert g.has_cycle() == 0, "이미 탐색이 끝난 정점으로 가는 간선은 사이클이 아닙니다"


def test_e_cycle_not_reachable_from_vertex_zero(make):
    g = make(4, [(0, 1), (2, 3), (3, 2)])
    assert g.has_cycle() == 1, "0 에서 갈 수 없는 곳의 사이클도 찾아야 합니다"


def test_e_has_cycle_frees_what_it_allocates(lib, make):
    g = make(4, DIAMOND)
    before = live_allocations(lib)
    g.has_cycle()
    assert_no_leak(lib, before, "graph_has_cycle")


# --- no debug output ---------------------------------------------------------


def test_only_graph_print_prints(capfd, lib):
    def run() -> None:
        g = Graph(lib, G1_N, G1)
        g.add_edge(9, 0)
        g.bfs(0)
        g.dfs(0)
        g.has_cycle()
        g.free()

    _, out = native_stdout(capfd, run)
    assert out == "", f"graph_print 말고는 아무것도 출력하면 안 됩니다. 출력된 내용:\n{out}"
