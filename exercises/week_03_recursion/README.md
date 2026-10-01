# Week 03 — 재귀 (Recursion)

이번 주 토픽은 재귀입니다.
"문제를 같은 모양의 더 작은 문제로 바꾼다"는 하나의 발상이 어디까지 가는지 봅니다.

과제가 네 개입니다. 각각 재귀의 다른 얼굴을 다룹니다.

| 과제 | 언어 | 난이도 | 내용 | 재귀의 얼굴 |
|---|---|---|---|---|
| [`c/easy_hanoi`](c/easy_hanoi/problem.md) | C | 쉬움 | 하노이 탑 | 기본형 |
| [`cpp/medium_merge_sort`](cpp/medium_merge_sort/problem.md) | C++ | 중간 | 재귀 머지 소트 | 분할 정복 |
| [`python/easy_flatten`](python/easy_flatten/problem.md) | Python | 쉬움 | 중첩 리스트 펼치기 | 재귀적 구조 |
| [`python/medium_backtracking`](python/medium_backtracking/problem.md) | Python | 중간 | 순열과 부분집합 | 백트래킹 |

## 채점하기

```sh
uv run runner.py test 3                       # 네 과제를 모두 채점합니다
uv run runner.py test 3 --lang python         # 언어별로 골라서 채점합니다
uv run runner.py test 3 --task hanoi          # 한 과제만 채점합니다
```

## 재귀를 쓸 때 늘 같은 두 가지

어떤 재귀 함수를 짜든 물어볼 것은 두 개뿐입니다.

1. **언제 멈추는가** (기저 조건)
2. **어떻게 더 작은 같은 문제로 바꾸는가**

하노이 탑은 "원반이 0개면 멈춘다 / n-1개 문제로 바꾼다", 평탄화는 "정수를 만나면 멈춘다 /
리스트면 그 안을 각각 펼친다" 입니다. 네 과제를 풀면서 매번 이 두 가지를 먼저 적어 보세요.
코드보다 그게 먼저입니다.

## 재귀는 공짜가 아닙니다

호출마다 **스택**에 자리를 하나씩 씁니다. 깊이 들어가면 자리가 모자라고, 그때 터지는 방식이
언어마다 다릅니다.

| 언어 | 터지는 방식 |
|---|---|
| Python | `RecursionError`. 기본 한도 1000 (`sys.getrecursionlimit()`) |
| C / C++ | **세그폴트.** 경고 없이 죽습니다 |

이번 주 과제들은 깊이가 얕아서 터지지 않습니다. 하노이는 깊이가 `n`, 머지 소트는 `log n` 이고
순열·부분집합도 값의 개수만큼입니다. 하지만 `python/easy_flatten` 의 "생각해 볼 것" 에
직접 터뜨려 보는 방법을 적어 두었으니 한 번 해 보시길 권합니다.

**이동 횟수와 재귀 깊이는 다릅니다.** 하노이 탑은 `n = 20` 일 때 100만 수가 넘지만 깊이는 20밖에
안 됩니다. 이 차이를 구분하는 것이 이번 주의 중요한 감각입니다.

## 추천 읽을거리

- [Recursion in Programming — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/recursion/)
  기저 조건, 재귀 호출, 스택 동작을 그림과 함께 훑어 주는 글입니다.
- [Python Tutor](https://pythontutor.com/)
  이번 주에 특히 유용합니다. 재귀 호출이 쌓이고 풀리는 과정을 한 줄씩 볼 수 있습니다.
  `factorial(4)` 같은 짧은 코드를 붙여 넣고 끝까지 눌러 보세요.
- [VisuAlgo — Recursion Tree](https://visualgo.net/en/recursion)
  호출이 갈라지는 모양을 트리로 보여 줍니다. 백트래킹을 이해할 때 도움이 됩니다.
- [Python 공식 문서 — `sys.setrecursionlimit`](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)

## 이번 주에 익혀 두면 좋은 것

- 기저 조건을 **먼저** 적는 습관. 재귀가 안 멈추는 버그는 거의 다 여기서 옵니다
- 재귀 호출을 머릿속으로 다 따라가지 않는 연습.
  "작은 문제는 이미 풀렸다고 믿고" 지금 단계만 맞게 쓰는 것이 핵심입니다
- 호출 **횟수**와 호출 **깊이**를 구분하기
- 백트래킹에서 되돌리기(undo)를 빼먹지 않기, 그리고 답을 담을 때 복사하기
