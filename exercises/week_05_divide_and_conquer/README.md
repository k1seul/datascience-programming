# Week 05 — 분할 정복 (Divide and Conquer)

이번 주 과제는 세 개입니다. 아래 순서대로 푸는 것을 권합니다.

| 순서 | 과제 | 언어 | 내용 | 예상 시간 |
|---|---|---|---|---|
| 1 | [`c/medium_binary_search`](c/medium_binary_search/problem.md) | C | 정렬된 배열에서 값 찾기 | 1.5~2시간 |
| 2 | [`python/medium_order_split`](python/medium_order_split/problem.md) | Python | 기한 안에 주식을 다 팔 수 있는 최소 한도 찾기 | 1~1.5시간 |
| 3 | [`cpp/medium_quick_sort`](cpp/medium_quick_sort/problem.md) | C++ | 배열 정렬하기 | 1~1.5시간 |

**C 문제를 먼저 푸세요.** Python 문제는 C 문제에서 만드는 `lower_bound` 와 같은 방법으로 풀립니다.
C++ 문제는 앞의 두 문제와 상관없이 언제 풀어도 됩니다.

각 문제 파일에는 문제 설명, 예시, 지켜야 할 것, 그리고 **접어 둔 힌트**가 있습니다.
먼저 혼자 풀어 보고 막힐 때 힌트를 하나씩 펼쳐 보세요.

## 채점하기

```sh
uv run runner.py test 5                        # 세 과제를 모두 채점합니다
uv run runner.py test 5 --task binary_search   # C 과제만
uv run runner.py test 5 --task order_split     # Python 과제만
uv run runner.py test 5 --task quick_sort      # C++ 과제만
```

## 분할 정복이란

**큰 문제를 작은 부분으로 나누고, 작은 부분의 답으로 전체의 답을 구하는 방법**입니다.
이번 주 세 문제는 각각 이렇게 나눕니다.

**C — 이진 탐색: 가운데를 보고, 답이 없는 절반을 버린다**

```
[1  3  5  7  9]    7을 찾는다
       ^           가운데는 5. 7보다 작으니 왼쪽 절반은 볼 필요가 없다
          [7  9]   남은 절반에서 다시 가운데를 본다
```

한 번 볼 때마다 후보가 절반으로 줄어서, 100만 개짜리 배열도 20번 정도면 끝납니다.

**Python — 분할 매도: 가능한 답의 범위를 절반씩 줄인다**

이 문제에는 뒤질 배열이 없습니다. 대신 "한도가 몇이면 될까?"의 **후보 범위**(1부터 가장 큰 계좌까지)를
절반씩 줄여 갑니다. 한도를 하나 정해 주면 가능한지 확인하기는 쉽기 때문에 이 방법이 통합니다.

**C++ — 퀵 소트: 기준값으로 나눈 뒤 양쪽을 각각 정렬한다**

```
[5  2  9  1  6]    기준값으로 5를 고른다
[2  1] 5 [9  6]    5보다 작은 것은 왼쪽, 큰 것은 오른쪽. 이제 5는 제자리다
                   왼쪽과 오른쪽을 같은 방법으로 정렬하면 끝
```

## 이번 주에 가장 많이 틀리는 것

**이진 탐색의 경계입니다.** 아이디어는 쉬운데 한 칸씩 어긋나는 실수가 아주 흔합니다.
C 문제와 Python 문제 모두 해당되니, 두 문제를 풀기 전에 이것만 기억해 두세요.

```c
int lo = 0, hi = n;                  /* hi 는 n - 1 이 아니라 n 에서 시작 */
while (lo < hi) {                    /* <= 가 아니라 < */
    int mid = lo + (hi - lo) / 2;    /* (lo + hi) / 2 는 큰 값에서 넘친다 */
    if (조건) hi = mid;              /* mid - 1 이 아니라 mid */
    else      lo = mid + 1;
}
return lo;
```

주석에 적은 네 가지를 섞어 쓰면 무한 루프에 빠지거나 답을 한 칸 지나칩니다.
더 자세한 설명은 C 문제의 힌트 2에 있습니다.

## 참고 자료

- [Binary Search — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/binary-search/)
  반복문과 재귀 두 버전, 경계 처리까지 정리되어 있습니다.
- [QuickSort — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/)
  분할(partition) 과정을 그림으로 보여 줍니다.
- [VisuAlgo — Sorting](https://visualgo.net/en/sorting)
  퀵 소트가 동작하는 모습을 애니메이션으로 볼 수 있습니다. Week 03 의 머지 소트와 나란히 비교해 보세요.
- [Python Tutor](https://pythontutor.com/)
  이진 탐색에서 `lo` 와 `hi` 가 어떻게 좁혀지는지 한 줄씩 따라가 볼 수 있습니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶다면 아래 문제를 풀어 보세요. 위에서 아래로 갈수록 어려워집니다.

| | 문제 | 난이도 | 이번 주 과제와의 관계 |
|---|---|---|---|
| 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | C 과제의 `binary_search` 와 같습니다 |
| 35 | [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Easy | C 과제의 `lower_bound` 와 같습니다 |
| 34 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | `lower_bound` 와 `upper_bound` 를 함께 씁니다 |
| 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | 퀵 소트의 분할을 써서, 정렬하지 않고 k번째 값을 찾습니다 |
| 1011 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Python 과제와 같은 방법으로 풉니다 |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | 정렬이 중간에 한 번 끊긴 배열에서 이진 탐색을 합니다 |

더 어려운 문제를 원하면 **410 Split Array Largest Sum** (Hard)을 풀어 보세요. Python 과제와 같은 방법을 씁니다.
