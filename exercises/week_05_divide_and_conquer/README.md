# Week 05 — 분할 정복 (Divide and Conquer)

이번 주 토픽은 분할 정복입니다.
"문제를 쪼개서 작은 문제로 만든다"는 Week 03 의 재귀와 같은 발상인데, 이번에는
**쪼개는 방식**에 집중합니다. 쪼개는 방법이 달라지면 알고리즘이 달라집니다.

| 과제 | 언어 | 난이도 | 내용 | 쪼개는 방식 |
|---|---|---|---|---|
| [`c/medium_trade_search`](c/medium_trade_search/problem.md) | C | 중간 | 체결 기록에서 구간 찾기 | 반으로 쪼개 **한쪽만** |
| [`cpp/medium_quick_sort`](cpp/medium_quick_sort/problem.md) | C++ | 중간 | 퀵 소트 | **기준값으로 가르기** |
| [`python/medium_order_split`](python/medium_order_split/problem.md) | Python | 중간 | 분할 매도 | 탐색 공간을 **답으로** |

## 채점하기

```sh
uv run runner.py test 5                        # 세 과제를 모두 채점합니다
uv run runner.py test 5 --task trade_search    # 한 과제만 채점합니다
```

## 세 가지 쪼개는 방식

Week 03 의 머지 소트까지 합치면 분할 정복의 네 모양이 모입니다.

```
① 쪼개서 각각 풀고 합친다        머지 소트 (Week 03)
   [■■■■■■■■] -> [■■■■][■■■■] -> 정렬된 둘을 합친다

② 반으로 쪼개 한쪽만 본다        이진 탐색 (이번 주 C)
   [■■■■■■■■] -> 가운데를 보고 한쪽을 버린다 -> [■■■■]

③ 기준값으로 가른다              퀵 소트 (이번 주 C++)
   [■■■■■■■■] -> [작은 것][기준][큰 것] -> 양쪽을 각각 정렬

④ 탐색 공간을 답으로 바꾼다      분할 매도 (이번 주 Python)
   배열이 아니라 "가능한 답의 범위" 에서 이진 탐색
```

②와 ④가 같은 기법이라는 것을 알아차리는 게 이번 주의 가장 큰 수확입니다.
C 과제의 `first_at_or_after` 와 Python 과제의 `min_daily_limit` 은 **같은 일**을 합니다.
찾을 배열이 있는지 없는지만 다릅니다.

## 소재는 금융 데이터입니다

이 수업의 성격에 맞춰 세 과제 모두 실제로 할 만한 작업으로 감쌌습니다.

- 시각 순으로 정렬된 **체결 기록**에서 구간을 잘라 내기 (C)
- **일별 수익률**을 정렬해서 분포를 보기 (C++)
- 시장 충격을 줄이려고 **주문을 며칠에 나눠** 체결하기 (Python)

알고리즘은 교과서와 같습니다. 다만 이런 일에 실제로 쓰인다는 것을 보아 두면
나중에 비슷한 문제를 만났을 때 알아보기 쉽습니다.

## 이번 주에 가장 많이 틀리는 것

**경계입니다.** 이진 탐색은 아이디어가 쉬운데 한 칸씩 어긋나는 실수가 유명할 만큼 잦습니다.

| 섞어 쓰면 안 되는 짝 | |
|---|---|
| `hi = n` 으로 시작 | `while (lo < hi)`, `hi = mid` |
| `hi = n - 1` 로 시작 | `while (lo <= hi)`, `hi = mid - 1` |

둘을 섞으면 무한 루프가 나거나 답을 한 칸 지나칩니다. 한 가지를 골라 **짝으로 외워 두세요.**
그리고 가운데는 항상 이렇게 구합니다.

```c
int mid = lo + (hi - lo) / 2;   /* (lo + hi) / 2 는 큰 값에서 넘칩니다 */
```

## 추천 읽을거리

- [Binary Search — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/binary-search/)
  반복문과 재귀 두 버전, 경계 처리까지 정리되어 있습니다.
- [QuickSort — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/)
  partition 과정을 그림으로 보여 줍니다.
- [VisuAlgo — Sorting](https://visualgo.net/en/sorting)
  머지 소트와 퀵 소트를 나란히 애니메이션으로 비교할 수 있습니다. 이번 주에 특히 유용합니다.
- [Python Tutor](https://pythontutor.com/)
  이진 탐색의 `lo` 와 `hi` 가 어떻게 좁혀지는지 한 줄씩 따라가 보세요.

## 더 풀어 볼 문제 (LeetCode)

여섯 문제만 골랐습니다. 위에서 아래로 내려가며 푸시면 난이도가 올라갑니다.

| | 문제 | 난이도 | 어디에 해당하나 |
|---|---|---|---|
| 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | C 과제의 `find_trade` |
| 35 | [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Easy | `first_at_or_after` 그 자체 |
| 34 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | 두 경계를 함께 쓰는 문제 |
| 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | 퀵 소트의 partition 을 선택에 쓰기 |
| 1011 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Python 과제와 같은 패턴, 다른 옷 |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | 정렬이 한 번 끊긴 배열에서의 이진 탐색 |

215번은 퀵 소트를 짜고 나서 보면 쉽습니다. **정렬을 끝까지 하지 않고** 한쪽만 더 파고들면
k번째 값을 평균 `O(n)` 에 찾을 수 있습니다.
1011번은 Python 과제와 판정 함수만 다릅니다. 두 문제를 나란히 보면 패턴이 굳습니다.
더 도전하고 싶으시면 **410 Split Array Largest Sum**(Hard)이 같은 패턴의 상급판입니다.
