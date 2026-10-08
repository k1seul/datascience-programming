# Week 04 — 재귀 연습 (시험 대비)

다음 주 시험 범위에 맞춘 연습 주차입니다. 새로운 개념은 없습니다.
Week 01(연결 리스트), Week 03(재귀)에서 배운 것을 **시험에 나오는 형태로** 한 번씩 써 봅니다.

| 과제 | 언어 | 난이도 | 내용 | 연습하는 것 |
|---|---|---|---|---|
| [`c/medium_recursive_list`](c/medium_recursive_list/problem.md) | C | 중간 | 연결 리스트를 재귀로 | 재귀 × 연결 리스트 |
| [`cpp/easy_recursive_string`](cpp/easy_recursive_string/problem.md) | C++ | 쉬움 | 문자열을 재귀로 | 인덱스 좁히기, 문자 필터 |
| [`python/easy_combinations_sum`](python/easy_combinations_sum/problem.md) | Python | 쉬움 | 합이 정해진 조합 | 백트래킹, 경계 처리 |

## 채점하기

```sh
uv run runner.py test 4                            # 세 과제를 모두 채점합니다
uv run runner.py test 4 --task recursive_list      # 한 과제만 채점합니다
```

## C 과제가 이번 주의 중심입니다

Week 01 에서 연결 리스트를 **반복문으로** 다뤘고, Week 03 에서 재귀를 배웠습니다.
그런데 **그 둘을 합쳐 본 적이 없습니다.** 이번 주에 그 빈자리를 채웁니다.

연결 리스트는 구조 자체가 재귀적입니다.

```
head -> [1] -> [2] -> [3] -> NULL
         ^      ^^^^^^^^^^^^^^^^^
         노드    나머지 리스트 (이것도 연결 리스트)
```

"노드 하나 + 나머지 리스트" 로 보는 순간 재귀가 자연스럽게 맞아 들어갑니다.
반복문으로 쓸 때 필요했던 `prev` 포인터 같은 것이 사라지는 경우도 많습니다.

## 이번 주에 꼭 손에 익혀야 할 세 가지

**① 재귀의 "돌아오는 길"에서 일하기.**
값을 역순으로 다루려면 재귀를 먼저 부르고, 돌아온 다음에 자기 일을 합니다.

```
순서대로 처리:              역순으로 처리:
  자기 일을 한다;             나머지를 처리한다;
  나머지를 처리한다;           자기 일을 한다;
```

C 과제의 `to_string_reverse` 와 C++ 과제의 `reverse_string` 이 같은 이야기입니다.

**② 출력 형식을 정확히 맞추기.**
"값마다 뒤에 공백 하나, 마지막 개행 없음" 같은 조건은 한 글자만 틀려도 오답입니다.
구현이 맞는데 형식 때문에 점수를 잃는 일이 가장 아깝습니다. 과제에서 미리 겪어 두세요.

**③ 경계 조건.**
빈 리스트, 빈 문자열, `k = 0`, `k > len(values)` 같은 경우를 빠뜨리지 않는 것.
Python 과제의 `[[]]` 와 `[]` 차이가 대표적입니다. 헷갈리면 통째로 틀립니다.

## 백트래킹 골격은 이미 익혔습니다

Python 과제는 Week 03 의 순열·부분집합과 **같은 골격**입니다. 조건 하나가 붙었을 뿐이죠.

```
고른다 -> 더 들어간다 -> 되돌린다
```

그리고 답을 담을 때 **복사**하는 것을 잊지 마세요. `result.append(path)` 가 아니라
`result.append(path[:])` 입니다. Week 03 에서 이미 한 번 걸러진 내용이지만,
가장 자주 나오는 실수라 이번에도 테스트가 확인합니다.

## 추천 읽을거리

이번 주는 새 개념이 없으니 지난 주차 자료를 다시 보시는 편이 낫습니다.

- [Week 01 — 연결 리스트](../week_01_linked_list/README.md)
- [Week 03 — 재귀](../week_03_recursion/README.md)
- [Python Tutor](https://pythontutor.com/) — 재귀 호출이 쌓이고 풀리는 과정을 한 줄씩 볼 수 있습니다.
  C 과제의 `to_string_reverse` 를 짧은 리스트로 돌려 보면 "돌아오는 길"이 눈에 보입니다.

## 더 풀어 볼 문제 (LeetCode)

시험 유형과 같은 모양의 문제만 네 개 골랐습니다.

| | 문제 | 난이도 | 어디에 해당하나 |
|---|---|---|---|
| 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | 연결 리스트 재귀 |
| 203 | [Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) | Easy | 재귀로 노드 빼기 |
| 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | 문자열 양쪽 좁히기 + 문자 필터 |
| 77 | [Combinations](https://leetcode.com/problems/combinations/) | Medium | 백트래킹 조합 |

203번은 C 과제의 `drop_value` 와 같은 문제입니다. **재귀로** 풀어 보세요.
125번은 영숫자만 보고 대소문자를 무시하는 조건이 붙어 있어 문자 필터 연습이 됩니다.
77번은 Python 과제에서 `target` 조건만 뺀 형태입니다.
