# Week 01 / Python (쉬움) — 리스트 뒤집기와 변환

`Node` 클래스는 이미 만들어져 있습니다.
파이썬 리스트와 연결 리스트를 서로 오가는 변환 함수 두 개와, 뒤집기 하나를 구현하시면 됩니다.

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

- 빈 리스트는 `None` 으로 표현합니다. 세 함수 모두 빈 입력을 처리할 수 있어야 합니다.
- `reverse` 는 **새 노드를 만들지 않습니다.**
  기존 노드의 `next` 를 다시 이어서 뒤집고, 새로운 머리 노드를 반환해 주세요.
  채점기가 노드 객체의 동일성으로 이 부분을 확인합니다.
- 재귀 대신 반복문으로 풀어 주세요. 입력이 10만 개여도 문제없이 돌아가야 합니다.

## 채점

```sh
uv run runner.py test 1 --task reverse_list
```

## 생각해 볼 것

- `reverse` 안에서 `node.next` 를 바꾸기 **전에** 무엇을 먼저 저장해 두어야 할까요?
- 뒤집기가 끝났을 때 원래 머리 노드의 `next` 는 무엇을 가리키고 있어야 할까요?
- `to_list` 를 재귀로 짜면 몇 개짜리 입력에서 `RecursionError` 가 날까요? 직접 확인해 보셔도 좋습니다.
