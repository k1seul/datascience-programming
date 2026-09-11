# Week 01 — 연결 리스트 (Linked List)

이번 주 토픽은 단일 연결 리스트입니다.
C 에서는 자료구조를 처음부터 직접 만들어 보고, C++ 와 Python 에서는 그 위에서 도는
알고리즘을 쉬움과 중간 난이도로 한 문제씩 풉니다.

| 과제 | 언어 | 난이도 | 내용 |
|---|---|---|---|
| [`c/impl_singly_linked_list`](c/impl_singly_linked_list/problem.md) | C | 구현 | 단일 연결 리스트 자료구조 전체 |
| [`cpp/easy_remove_duplicates`](cpp/easy_remove_duplicates/problem.md) | C++ | 쉬움 | 정렬된 리스트에서 중복 제거하기 |
| [`cpp/medium_reverse_in_k_groups`](cpp/medium_reverse_in_k_groups/problem.md) | C++ | 중간 | k개씩 묶어서 뒤집기 |
| [`python/easy_reverse_list`](python/easy_reverse_list/problem.md) | Python | 쉬움 | 리스트 뒤집기와 변환 |
| [`python/medium_detect_cycle`](python/medium_detect_cycle/problem.md) | Python | 중간 | 사이클 찾기 (플로이드 알고리즘) |

## 채점하기

```sh
uv run runner.py test 1                      # 다섯 과제를 모두 채점합니다
uv run runner.py test 1 --lang cpp           # 언어별로 골라서 채점합니다
uv run runner.py test 1 --task detect_cycle  # 한 과제만 채점합니다
```

## 추천 읽을거리

- [Linked List Data Structure — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/linked-list-data-structure/)
  이번 주 내용을 전체적으로 훑어 주는 글입니다. 리스트의 종류(단일, 이중, 원형)와 기본 연산,
  배열과 비교했을 때의 장단점까지 한 페이지에 정리되어 있습니다.
- [Python Tutor](https://pythontutor.com/)
  짧은 리스트를 만들어 뒤집는 코드를 붙여 넣고 한 줄씩 실행해 보세요.
  `next` 를 언제 저장해 두어야 하는지가 그림으로 보입니다. C, C++, Python 모두 지원합니다.
- [VisuAlgo — Linked List](https://visualgo.net/en/list)
  삽입, 삭제, 뒤집기를 애니메이션으로 확인할 수 있습니다.

기초가 아직 흔들린다면 [Week 00 — 기초 다지기](../week_00_basics/README.md) 를 먼저 보고 오셔도 좋습니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶으시면 아래 문제들을 권합니다.
꼭 다 풀어야 하는 것은 아니고, 약한 유형을 골라 두세 문제만 해 보셔도 충분합니다.

### 느린 포인터와 빠른 포인터

| | 문제 | 난이도 |
|---|---|---|
| 2095 | [Delete the Middle Node of a Linked List](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/) | Medium |
| 19 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium |
| 82 | [Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) | Medium |
| 1721 | [Swapping Nodes in a Linked List](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/) | Medium |

### 리스트 뒤집기

| | 문제 | 난이도 |
|---|---|---|
| 234 | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | Easy |
| 2074 | [Reverse Nodes in Even Length Groups](https://leetcode.com/problems/reverse-nodes-in-even-length-groups/) | Medium |
| 2130 | [Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/) | Medium |

### 그 밖에

| | 문제 | 난이도 |
|---|---|---|
| 203 | [Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) | Easy |
| 1290 | [Convert Binary Number in a Linked List to Integer](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/) | Easy |
| 328 | [Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/) | Medium |
| 707 | [Design Linked List](https://leetcode.com/problems/design-linked-list/) | Medium |

이번 주 과제와 짝이 되는 문제들이 있습니다. 707번은 C 구현 과제와 거의 같은 내용이고,
82번은 `cpp/easy_remove_duplicates` 에서 한 걸음 더 나간 문제(중복된 값을 아예 다 지웁니다)입니다.
2074번은 `cpp/medium_reverse_in_k_groups` 와 같은 묶음 뒤집기이고,
234번과 2130번은 느린/빠른 포인터로 중간을 찾은 다음 뒤집는, 두 과제를 합친 형태입니다.

## 이번 주에 익혀 두면 좋은 것

- 포인터를 옮길 때 **어떤 순서로** 옮겨야 링크가 끊기지 않는지 (`next` 를 먼저 저장해 두는 습관)
- 머리(head)가 바뀌는 연산에서 더미 노드(dummy head)를 두면 왜 코드가 간단해지는지
- 한 번만 순회하면 되는 일을 두 번 순회하고 있지는 않은지
