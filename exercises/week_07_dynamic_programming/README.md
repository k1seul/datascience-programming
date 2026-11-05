# Week 07 — 동적 계획법 (Dynamic Programming)

이번 주 과제는 다섯 개입니다. 앞의 세 개는 DP 에 익숙해지기 위한 쉬운 문제이고, 뒤의 두 개가 이번 주의 본 문제입니다.

| 순서 | 과제 | 언어 | 내용 | 예상 시간 |
|---|---|---|---|---|
| 1 | [`python/easy_fibonacci`](python/easy_fibonacci/problem.md) | Python | 피보나치를 빠르게 구하고, 느린 재귀가 몇 번 호출되는지 세기 | 30분 |
| 2 | [`c/easy_tiling`](c/easy_tiling/problem.md) | C | 2×n 판을 타일로 채우는 방법의 수 | 30~40분 |
| 3 | [`python/easy_stepping_stones`](python/easy_stepping_stones/problem.md) | Python | 징검다리를 건너는 방법의 수와 가장 적은 비용 | 1시간 |
| 4 | [`cpp/medium_edit_distance`](cpp/medium_edit_distance/problem.md) | C++ | 오타를 몇 번 고치면 같은 단어가 되는지, 가장 가까운 단어 찾기 | 1.5시간 |
| 5 | [`c/medium_knapsack`](c/medium_knapsack/problem.md) | C | 예산 안에서 효과가 가장 큰 광고 조합과, 무엇을 골랐는지 | 2시간 |

**순서대로 푸세요.** 뒤 문제가 앞 문제에서 익힌 것을 그대로 씁니다.

| 과제 | 익히는 것 |
|---|---|
| 1, 2 | 같은 계산을 두 번 하지 않는 두 가지 방법 (memoization, tabulation) |
| 3 | 점화식 바꿔 보기: 경우의 수(더하기)와 최솟값(min) |
| 4 | 두 문자열로 만드는 2차원 표 |
| 5 | 2차원 표, 그리고 표에서 "무엇을 골랐는지" 되짚기 |

각 문제 파일에는 문제 설명, 예시, 지켜야 할 것, 그리고 **접어 둔 힌트**가 있습니다.
먼저 혼자 풀어 보고 막힐 때 힌트를 하나씩 펼쳐 보세요.

## 채점하기

```sh
uv run runner.py test 7                            # 다섯 과제를 모두 채점합니다
uv run runner.py test 7 --task fibonacci           # 1번만
uv run runner.py test 7 --task tiling              # 2번만
uv run runner.py test 7 --task stepping_stones     # 3번만
uv run runner.py test 7 --task edit_distance       # 4번만
uv run runner.py test 7 --task knapsack            # 5번만
```

## 동적 계획법이란

Week 03 에서 피보나치를 재귀로 짜면 이렇게 됩니다.

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

`fib(5)` 하나를 구하려고 `fib(2)` 를 세 번, `fib(1)` 을 다섯 번 부릅니다. **이미 구한 답을 처음부터 다시 구하고 있습니다.**
`n` 이 1 커질 때마다 호출이 1.6배쯤 늘어서 `fib(50)` 은 끝나지 않습니다.

**동적 계획법(DP)은 작은 문제의 답을 한 번만 구해서 기억해 두고, 다시 필요하면 꺼내 쓰는 방법입니다.**
그러면 `fib(0)` 부터 `fib(n)` 까지 각각 한 번씩, 모두 `n + 1` 번만 계산하면 됩니다.
기억하는 방법은 두 가지가 있고, 1번 과제에서 둘 다 써 봅니다.

### Memoization (top-down)

재귀 모양은 그대로 두고, 구한 답을 dict 나 배열에 **적어 둡니다**. 같은 인자로 다시 불리면 계산하지 않고 적어 둔 값을 돌려줍니다.

### Tabulation (bottom-up)

재귀 없이, **작은 문제부터 표를 채웁니다.** `dp[0]`, `dp[1]` 을 먼저 채우고, 그것으로 `dp[2]`, 그다음 `dp[3]` … 순서로 올라갑니다.

| | Memoization | Tabulation |
|---|---|---|
| 모양 | 재귀 | 반복문 |
| 채우는 순서 | 재귀가 알아서 정합니다 | 직접 정해야 합니다 |
| 조심할 것 | 재귀 깊이 (파이썬은 1000 단계쯤에서 `RecursionError`) | 표 크기와 인덱스 |

두 방법 중 무엇을 써도 답은 같습니다. 이번 주 1번 과제만 방법을 정해 두었고, 나머지는 편한 쪽으로 푸세요.

## DP 문제를 푸는 4단계

새 문제를 만나면 코드를 쓰기 전에 아래 네 가지를 먼저 말로 적어 보세요. 2번 과제(타일 채우기)로 예를 들면 이렇습니다.

1. **상태**: 표의 한 칸이 무엇을 뜻하는지 정합니다.
   `dp[i]` = 가로 `i` 칸짜리 판을 채우는 방법의 수
2. **점화식**: 한 칸을 더 작은 칸들로 나타냅니다. **"마지막에 무엇을 했나"** 를 보면 대부분 나옵니다.
   맨 오른쪽이 세로 타일 하나이거나 가로 타일 두 개이므로 `dp[i] = dp[i-1] + dp[i-2]`
3. **시작값**: 점화식으로 구할 수 없는 가장 작은 칸을 직접 채웁니다.
   `dp[0] = 1` (빈 판은 아무것도 안 놓는 1가지), `dp[1] = 1`
4. **채우는 순서**: 각 칸이 쓰는 칸이 먼저 채워지도록 순서를 정합니다.
   `dp[i]` 가 `dp[i-1]`, `dp[i-2]` 를 쓰므로 작은 `i` 부터

이번 주 다섯 문제의 **상태**는 이렇습니다. 점화식은 각 문제의 힌트에 있으니 직접 세워 보고 확인하세요.

| 과제 | 상태 |
|---|---|
| 피보나치 | `F(n)` |
| 타일 | `dp[i]` = 가로 `i` 칸짜리 판을 채우는 방법의 수 |
| 징검다리 | `ways[i]` = `i` 번 돌까지 오는 방법의 수, `best[i]` = `i` 번 돌까지 오는 가장 적은 비용 |
| 편집 거리 | `dp[i][j]` = `a` 의 앞 `i` 글자를 `b` 의 앞 `j` 글자로 바꾸는 가장 적은 횟수 |
| 배낭 | `dp[i][b]` = 앞의 `i` 개 캠페인만 보고 예산이 `b` 일 때 얻는 가장 큰 효과 |

## 느린 풀이는 채점기가 알려 줍니다

이번 주에는 **큰 입력을 2초 안에 풀어야 하는 테스트**가 과제마다 있습니다. `fib_memo(300)`, `tiling(90)`, 돌 300개, 36글자 단어, 캠페인 40개 같은 입력입니다.
기억하지 않는 재귀로 풀면 이 테스트들이 "2초 안에 끝나지 않았습니다" 로 실패합니다.
그 테스트만 실패하고 **나머지 채점은 그대로 진행되니**, 작은 입력은 맞는데 큰 입력만 실패한다면 기억하는 부분을 확인하세요.

## 이번 주에 가장 많이 틀리는 것

**표의 크기와 0번 칸입니다.** 다섯 문제 모두 해당되니 풀기 전에 이것만 기억해 두세요.

- **표는 `n` 칸이 아니라 `n + 1` 칸입니다.** `dp[0]` 부터 `dp[n]` 까지 쓰기 때문입니다.
  2차원 표도 마찬가지로 `(n + 1) × (m + 1)` 입니다.
- **0번 칸은 "아무것도 없을 때"입니다.** 빈 판을 채우는 방법은 1가지, 빈 문자열을 만드는 데 드는 횟수는 0, 캠페인이 없을 때의 효과는 0 입니다.
  이 값을 잘못 넣으면 표 전체가 틀립니다.
- **`n` 이 0 이나 1 일 때를 따로 확인하세요.** 길이 1짜리 표에 `dp[1] = 1` 을 쓰면 표 밖입니다.

## 참고 자료

- [Dynamic Programming (DP) Introduction — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/)
  memoization 과 tabulation 을 피보나치로 비교합니다.
- [VisuAlgo — Recursion Tree and DAG](https://visualgo.net/en/recursion)
  재귀 호출 트리를 그려 줍니다. 피보나치를 골라 보면 같은 호출이 몇 번 반복되는지, 기억해 두면 트리가 어떻게 줄어드는지 볼 수 있습니다.
- [Edit Distance — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/edit-distance-dp-5/)
  4번 과제. 재귀 풀이부터 memoization, 표 채우기까지 차례로 설명합니다.
- [0/1 Knapsack Problem — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/0-1-knapsack-problem-dp-10/)
  5번 과제. 재귀, memoization, tabulation 세 가지 풀이를 나란히 보여 줍니다.
- [functools.cache — Python 문서](https://docs.python.org/3/library/functools.html#functools.cache)
  파이썬에서 memoization 을 한 줄로 해 주는 데코레이터입니다. 1번 과제를 직접 푼 다음에 써 보세요.
- [Python Tutor](https://pythontutor.com/)
  memo dict 에 값이 어떤 순서로 채워지는지 한 줄씩 따라가 볼 수 있습니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶다면 아래 문제를 풀어 보세요. 위에서 아래로 갈수록 어려워집니다.

| | 문제 | 난이도 | 이번 주 과제와의 관계 |
|---|---|---|---|
| 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | 3번 과제의 `count_ways` 에서 `jumps = (1, 2)` 인 경우입니다 |
| 746 | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | Easy | 3번 과제의 `min_cost` 와 비슷합니다. 비용을 내는 계단과 출발점이 조금 다르니 문제를 잘 읽어 보세요 |
| 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | 동전이 `jumps`, 금액이 도착할 돌 번호이고 모든 돌의 비용이 1 인 `min_cost` 입니다 |
| 1143 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | 4번 과제와 같은 2차원 표를 다른 점화식으로 채웁니다 |
| 72 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | 4번 과제의 `edit_distance` 와 같습니다 |
| 416 | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | 5번 과제의 배낭 문제로 풉니다. 예산이 "전체 합의 절반"입니다 |
