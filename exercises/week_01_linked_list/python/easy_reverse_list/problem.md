# Week 01 / Python (쉬움) — 리스트 뒤집기와 변환

`Node` 클래스는 이미 주어져 있다. 파이썬 리스트와 연결 리스트를 오가는 변환 두 개와,
뒤집기 하나를 구현한다.

```python
head = from_iterable([1, 2, 3])   # 1 -> 2 -> 3
to_list(head)                     # [1, 2, 3]
to_list(reverse(head))            # [3, 2, 1]
```

## 구현할 함수

```python
def from_iterable(values: Iterable[int]) -> Node | None: ...
def to_list(head: Node | None) -> list[int]: ...
def reverse(head: Node | None) -> Node | None: ...
```

- 빈 리스트는 `None` 으로 표현한다. 세 함수 모두 빈 입력을 처리해야 한다.
- `reverse` 는 **새 노드를 만들지 않는다.** 기존 노드의 `next` 를 다시 이어서 뒤집고,
  새로운 머리 노드를 반환한다. (채점기가 노드 객체의 동일성으로 이걸 확인한다.)
- 재귀 없이 반복문으로 푼다. 입력이 10만 개여도 터지지 않아야 한다.

## 채점

```sh
uv run runner.py test 1 --task reverse_list
```

## 생각해 볼 것

- `reverse` 안에서 `node.next` 를 바꾸기 **전에** 무엇을 먼저 저장해야 하는가?
- 뒤집기가 끝났을 때 원래 머리 노드의 `next` 는 무엇을 가리켜야 하는가?
- `to_list` 를 재귀로 짜면 몇 개짜리 입력에서 `RecursionError` 가 나는가? 직접 확인해 보라.
