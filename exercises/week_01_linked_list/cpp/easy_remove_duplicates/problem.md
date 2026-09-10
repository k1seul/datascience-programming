# Week 01 / C++ (쉬움) — 정렬된 리스트에서 중복 제거

오름차순으로 정렬된 값들이 주어집니다.
이 값들로 **단일 연결 리스트를 만든 다음**, 같은 값이 이어지는 구간을 하나만 남기고
지운 결과를 반환하면 됩니다.

```
[1, 1, 2, 3, 3, 3]  ->  [1, 2, 3]
[]                  ->  []
[2, 2, 2]           ->  [2]
```

## 시그니처

```cpp
extern "C" int dedup_sorted(const int *values, int n, int *out, int out_capacity);
```

- `values` 와 `n` 은 정렬된 입력입니다 (`n >= 0`).
- `out` 과 `out_capacity` 는 결과를 쓸 버퍼입니다.
- 반환값은 `out` 에 쓴 개수입니다. `out_capacity` 가 부족하면 아무것도 쓰지 않고 `-1` 을 반환합니다.

## 조건

- 입력 배열을 그대로 훑어서 답을 만들지 마시고, 노드(`struct Node { int value; Node *next; }`)를
  이어 붙여 리스트를 만든 뒤 **링크를 끊는 방식**으로 지워 주세요.
  이번 주 토픽이 포인터 조작이기 때문입니다.
- 만든 노드는 반환하기 전에 모두 `delete` 로 해제해 주세요.
- 스텁의 `#define NOT_IMPLEMENTED` 와 `return NOT_IMPLEMENTED;` 는 구현을 시작할 때 지워 주세요.
  채점기가 이 값을 "아직 풀지 않음" 표시로 읽습니다.
- 한 번만 순회하면 끝낼 수 있습니다.

## 채점

```sh
uv run runner.py test 1 --task remove_duplicates
```

## 생각해 볼 것

- 지울 노드를 `delete` 하기 전에 `next` 를 어디에 저장해 두어야 할까요?
- 입력이 정렬되어 있지 않다면 이 방법이 왜 통하지 않을까요?
