# Week 01 / C++ (쉬움) — 정렬된 리스트에서 중복 제거

오름차순으로 정렬된 값들이 주어진다. 이 값들로 **단일 연결 리스트를 만든 다음**,
같은 값이 이어지는 구간을 하나만 남기고 지운 결과를 반환한다.

```
[1, 1, 2, 3, 3, 3]  ->  [1, 2, 3]
[]                  ->  []
[2, 2, 2]           ->  [2]
```

## 시그니처

```cpp
extern "C" int dedup_sorted(const int *values, int n, int *out, int out_capacity);
```

- `values` / `n`: 정렬된 입력. `n >= 0`.
- `out` / `out_capacity`: 결과를 쓸 버퍼.
- 반환: `out` 에 쓴 개수. `out_capacity` 가 모자라면 아무것도 쓰지 않고 `-1`.

## 조건

- 입력 배열을 그대로 훑어서 답을 만들지 말고, 노드(`struct Node { int value; Node *next; }`)를
  이어 붙여 리스트를 만든 뒤 **링크를 끊는 방식**으로 지운다. 이번 주 토픽은 포인터 조작이다.
- 만든 노드는 반환 전에 전부 해제한다 (`delete`).
- 한 번의 순회로 끝낼 수 있다.

## 채점

```sh
uv run runner.py test 1 --task remove_duplicates
```

## 생각해 볼 것

- 지울 노드를 `delete` 하기 전에 `next` 를 어디에 저장해 두어야 하는가?
- 입력이 정렬되어 있지 않다면 이 방법은 왜 통하지 않는가?
