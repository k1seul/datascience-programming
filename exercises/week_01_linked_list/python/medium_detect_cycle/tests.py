"""Week 01 / Python (중간) 채점 테스트."""

from __future__ import annotations

import pytest

from . import solution
from .solution import Node


def build(values: list[int], cycle_at: int | None = None) -> tuple[Node | None, Node | None]:
    """리스트를 만들고 (머리, 사이클 시작 노드) 를 돌려준다.

    cycle_at 이 None 이면 사이클 없음. 아니면 꼬리의 next 를 그 인덱스 노드로 잇는다.
    """
    nodes = [Node(value) for value in values]
    for left, right in zip(nodes, nodes[1:], strict=False):
        left.next = right
    if cycle_at is None or not nodes:
        return (nodes[0] if nodes else None), None
    start = nodes[cycle_at]
    nodes[-1].next = start
    return nodes[0], start


@pytest.mark.parametrize("values", [[], [1], [1, 2, 3], list(range(50))])
def test_사이클이_없으면_None(values):
    head, _ = build(values)
    assert solution.detect_cycle(head) is None
    assert solution.cycle_length(head) == 0


@pytest.mark.parametrize("cycle_at", [0, 1, 2, 3])
def test_사이클_시작_노드를_찾는다(cycle_at):
    head, start = build([10, 20, 30, 40], cycle_at=cycle_at)
    assert solution.detect_cycle(head) is start


@pytest.mark.parametrize(
    ("cycle_at", "expected"),
    [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1)],
)
def test_사이클_길이(cycle_at, expected):
    head, _ = build([1, 2, 3, 4, 5], cycle_at=cycle_at)
    assert solution.cycle_length(head) == expected


def test_자기_자신을_가리키는_노드_하나():
    head, start = build([7], cycle_at=0)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 1


def test_리스트_전체가_사이클이면_머리가_시작점이다():
    head, start = build([1, 2, 3, 4], cycle_at=0)
    assert solution.detect_cycle(head) is head
    assert start is head


def test_꼬리만_자기_자신을_가리키는_경우():
    head, start = build([1, 2, 3], cycle_at=2)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 1


def test_같은_값이_반복돼도_노드_동일성으로_판단한다():
    head, start = build([1, 1, 1, 1], cycle_at=2)
    assert solution.detect_cycle(head) is start


def test_긴_꼬리와_짧은_사이클():
    head, start = build(list(range(1000)), cycle_at=997)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 3


def test_방문_집합을_쓰지_않는다(monkeypatch):
    """상수 메모리 조건에 대한 최선의 확인.

    solution 모듈에서 set/dict 이름을 가로채 둔다. `seen = set()` 같은 흔한 풀이는 여기서 걸린다.
    (`{}` 나 집합 컴프리헨션 같은 리터럴까지는 잡지 못한다 — 조건 자체는 problem.md 가 기준이다.)
    """

    def banned(*args, **kwargs):
        raise AssertionError(
            "추가 자료구조 없이(상수 메모리) 풀어야 합니다 — 느린/빠른 포인터를 쓰세요"
        )

    monkeypatch.setattr(solution, "set", banned, raising=False)
    monkeypatch.setattr(solution, "dict", banned, raising=False)

    head, start = build([1, 2, 3, 4, 5], cycle_at=1)
    assert solution.detect_cycle(head) is start
    assert solution.cycle_length(head) == 4
