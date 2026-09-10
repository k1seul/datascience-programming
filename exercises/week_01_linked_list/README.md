# Week 01 — 연결 리스트 (Linked List)

이번 주 토픽은 단일 연결 리스트다. C 로 자료구조를 직접 만들어 보고,
C++ 와 Python 에서는 그 위에서 도는 알고리즘을 쉬움 / 중간 한 문제씩 푼다.

| 과제 | 언어 | 난이도 | 내용 |
|---|---|---|---|
| [`c/impl_singly_linked_list`](c/impl_singly_linked_list/problem.md) | C | 구현 | 단일 연결 리스트 자료구조 전체 |
| [`cpp/easy_remove_duplicates`](cpp/easy_remove_duplicates/problem.md) | C++ | 쉬움 | 정렬된 리스트에서 중복 제거 |
| [`cpp/medium_reverse_in_k_groups`](cpp/medium_reverse_in_k_groups/problem.md) | C++ | 중간 | k개씩 뒤집기 |
| [`python/easy_reverse_list`](python/easy_reverse_list/problem.md) | Python | 쉬움 | 리스트 뒤집기와 변환 |
| [`python/medium_detect_cycle`](python/medium_detect_cycle/problem.md) | Python | 중간 | 사이클 탐지 (플로이드) |

## 채점

```sh
uv run runner.py test 1                      # 5개 과제 전부
uv run runner.py test 1 --lang cpp           # 언어별
uv run runner.py test 1 --task detect_cycle  # 과제 하나
```

## 이번 주에 붙잡을 감각

- 포인터를 옮길 때 **어떤 순서로** 옮겨야 링크가 끊기지 않는가 (`next` 를 먼저 저장한다)
- 머리(head)가 바뀌는 연산에서 더미 노드(dummy head)가 왜 편한가
- 한 번의 순회로 끝낼 수 있는 일을 두 번 순회하고 있지는 않은가
