# Week 05 — 분할 정복 (Divide and Conquer)

이번 주 토픽은 분할 정복입니다. 이름이 어려워 보이지만 뜻은 간단합니다.

> **큰 문제를 작게 쪼개서, 작은 문제를 풀고, 그걸로 큰 문제의 답을 낸다.**

Week 03 의 재귀와 같은 발상입니다. 다른 점은 이번에 **쪼개는 방법**에 집중한다는 것입니다.
어떻게 쪼개느냐에 따라 전혀 다른 알고리즘이 나옵니다.

| 과제 | 언어 | 난이도 | 내용 |
|---|---|---|---|
| [`c/medium_binary_search`](c/medium_binary_search/problem.md) | C | 중간 | 이진 탐색 |
| [`cpp/medium_quick_sort`](cpp/medium_quick_sort/problem.md) | C++ | 중간 | 퀵 소트 |
| [`python/medium_order_split`](python/medium_order_split/problem.md) | Python | 중간 | 분할 매도 |

## 채점하기

```sh
uv run runner.py test 5                        # 세 과제를 모두 채점합니다
uv run runner.py test 5 --task binary_search   # 한 과제만 채점합니다
```

## 세 과제가 각각 어떻게 쪼개나

**① C 이진 탐색 — 반으로 쪼개고 한쪽을 버린다**

정렬된 배열에서 값을 찾습니다. 가운데를 보면 찾는 값이 왼쪽에 있는지 오른쪽에 있는지
알 수 있으니, 나머지 절반은 아예 볼 필요가 없습니다.

```
[1  3  5  7  9]   7을 찾는다
       ^ 가운데는 5, 7보다 작다  ->  왼쪽은 버린다
      [7  9]
       ^ 찾았다
```

볼 때마다 후보가 절반이 되니 100만 개도 스무 번이면 끝납니다.

**② C++ 퀵 소트 — 기준값으로 가른다**

기준값 하나를 정하고, 그보다 작은 것은 왼쪽 큰 것은 오른쪽으로 몰아 둡니다.
그러면 기준값의 자리는 이미 정해졌으니 왼쪽과 오른쪽만 따로 정렬하면 됩니다.

```
[5  2  9  1  6]   기준값을 5로
[2  1][5][9  6]   가르고 나면 5는 제자리
 ^^^^     ^^^^    양쪽을 각각 정렬하면 끝
```

**③ Python 분할 매도 — 답의 범위를 쪼갠다**

여기가 이번 주의 가장 큰 도약입니다. 쪼갤 배열이 아예 없습니다.

하루 체결 한도를 얼마로 잡아야 기한 안에 주식을 다 팔 수 있는지 구하는 문제인데,
**한도를 정해 주면 가능한지 판정하기는 쉽습니다.** 그리고 한도를 올리면 한 번 가능해진
뒤로는 계속 가능하죠.

```
한도:      1    2    3    4    5    6
가능한가?  X    X    X    O    O    O
                       ^ 답
```

`X` 와 `O` 의 경계를 찾는 문제이고, 그건 정렬된 배열에서 값을 찾는 것과 똑같습니다.
그래서 **배열 대신 "가능한 답의 범위" 에서 이진 탐색**을 합니다.

## 이번 주의 핵심 한 가지

**①과 ③이 같은 기법입니다.** 이걸 알아차리는 게 이번 주의 가장 큰 수확입니다.

| | C 과제 | Python 과제 |
|---|---|---|
| 무엇을 반으로 쪼개나 | 배열의 인덱스 범위 | 가능한 답의 범위 |
| 가운데에서 무엇을 보나 | `values[mid]` 값 | `can_sell_all(mid)` 판정 |
| 그래서 하는 일 | 한쪽을 버린다 | 한쪽을 버린다 |

C 과제의 `lower_bound` 와 Python 과제의 `min_daily_limit` 은 **같은 코드 모양**입니다.
먼저 C 과제를 끝내고 Python 과제로 가시면 "어, 이거 아까 그거네" 하는 순간이 옵니다.

참고로 Week 03 의 머지 소트까지 합치면 분할 정복의 네 가지 모양이 모입니다.
머지 소트는 "쪼갠 뒤 **합치는**" 쪽이고, 이번 주 퀵 소트는 "**가른 뒤** 각각 푸는" 쪽입니다.

## 가장 많이 틀리는 것: 경계

이진 탐색은 아이디어가 쉬운데 **한 칸씩 어긋나는 실수**가 유명할 만큼 잦습니다.
원인은 거의 항상 `lo` 와 `hi` 를 어디서 시작하고 언제 멈추는지를 섞어 쓰기 때문입니다.

**한 가지 조합만 골라서 통째로 외워 두세요.**

```c
int lo = 0, hi = n;                  /* hi 는 "아직 모르는 구간의 끝 다음" */
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (조건) hi = mid;              /* mid 도 후보로 남긴다 */
    else      lo = mid + 1;          /* mid 는 확실히 아니다 */
}
return lo;
```

`hi = n` 으로 시작했으면 `while (lo < hi)` 와 `hi = mid` 가 짝입니다.
`hi = n - 1` 로 시작했으면 `while (lo <= hi)` 와 `hi = mid - 1` 이 짝입니다.
둘을 섞으면 무한 루프가 나거나 답을 지나칩니다.

그리고 가운데는 항상 이렇게 구합니다.

```c
int mid = lo + (hi - lo) / 2;   /* (lo + hi) / 2 는 큰 값에서 넘칩니다 */
```

## 소재는 금융 데이터입니다

Python 과제는 "시장 충격을 줄이려고 주문을 며칠에 나눠 체결한다" 는 상황으로 감쌌습니다.
C++ 과제도 일별 수익률 분포를 보려면 정렬이 필요하다는 동기에서 출발합니다.

알고리즘은 교과서와 똑같습니다. 다만 이런 일에 실제로 쓰인다는 걸 보아 두면
나중에 비슷한 문제를 만났을 때 알아보기 쉽습니다.

## 추천 읽을거리

- [Binary Search — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/binary-search/)
  반복문과 재귀 두 버전, 경계 처리까지 정리되어 있습니다.
- [QuickSort — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/)
  가르는 과정을 그림으로 보여 줍니다.
- [VisuAlgo — Sorting](https://visualgo.net/en/sorting)
  머지 소트와 퀵 소트를 나란히 애니메이션으로 비교할 수 있습니다. 이번 주에 특히 유용합니다.
- [Python Tutor](https://pythontutor.com/)
  이진 탐색의 `lo` 와 `hi` 가 어떻게 좁혀지는지 한 줄씩 따라가 보세요.

## 더 풀어 볼 문제 (LeetCode)

여섯 문제만 골랐습니다. 위에서 아래로 내려가며 푸시면 난이도가 올라갑니다.

| | 문제 | 난이도 | 어디에 해당하나 |
|---|---|---|---|
| 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | C 과제의 `binary_search` |
| 35 | [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Easy | `lower_bound` 그 자체 |
| 34 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | 두 경계를 함께 쓰는 문제 |
| 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | 퀵 소트의 가르기를 선택에 쓰기 |
| 1011 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Python 과제와 같은 패턴, 다른 옷 |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | 정렬이 한 번 끊긴 배열에서의 이진 탐색 |

215번은 퀵 소트를 짜고 나서 보면 쉽습니다. **정렬을 끝까지 하지 않고** 한쪽만 더 파고들면
k번째 값을 평균 `O(n)` 에 찾을 수 있습니다.
1011번은 Python 과제와 판정 함수만 다릅니다. 두 문제를 나란히 보면 패턴이 굳습니다.
더 도전하고 싶으시면 **410 Split Array Largest Sum**(Hard)이 같은 패턴의 상급판입니다.
