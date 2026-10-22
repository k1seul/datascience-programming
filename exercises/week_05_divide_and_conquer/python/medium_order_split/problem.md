# Week 05 / Python (중간) — 분할 매도

여러 계좌에 주식이 나뉘어 있습니다. 한 번에 전량을 시장에 던지면 가격이 밀리니까
**하루 체결 한도**를 정해 두고 며칠에 걸쳐 나눠 팝니다.

하루에 **계좌 하나당 최대 `limit` 주**까지 체결할 수 있습니다. 한 계좌를 그날 다 털지
못하면 다음 날 이어서 팔고, 한 날에 두 계좌를 걸쳐 파는 일은 없습니다.

```python
holdings = [3, 6, 7, 11]   # 계좌 4개의 보유 수량
days = 8

# limit = 4 라면
#   계좌 3주  -> 1일 (3주를 한 번에)
#   계좌 6주  -> 2일 (4주 + 2주)
#   계좌 7주  -> 2일 (4주 + 3주)
#   계좌 11주 -> 3일 (4주 + 4주 + 3주)
#   합 8일  <= 8  OK

min_daily_limit([3, 6, 7, 11], 8)   # 4
```

`days` 일 안에 전량을 처분할 수 있는 **가장 작은 한도**를 구합니다.
한도가 작을수록 시장 충격이 적으니 최소값을 찾는 것이 목표입니다.

## 구현할 함수

```python
def can_sell_all(holdings: Sequence[int], days: int, limit: int) -> bool: ...
def min_daily_limit(holdings: Sequence[int], days: int) -> int: ...
```

| 함수 | 하는 일 |
|---|---|
| `can_sell_all` | 한도가 `limit` 일 때 `days` 일 안에 전량 처분이 가능한가 |
| `min_daily_limit` | 가능한 **최소 한도** |

함수를 두 개로 나눈 것이 이 과제의 핵심입니다. 이유는 아래에 있습니다.

## 조건

- `holdings` 의 각 값은 1 이상이고, `days >= len(holdings)` 가 보장됩니다.
  하루에 한 계좌는 최소 1주씩이라도 팔 수 있으니 답은 항상 존재합니다.
- 답의 최소값은 `1`, 최대값은 `max(holdings)` 입니다.
- `limit <= 0` 이면 `can_sell_all` 은 `False` 입니다.
- **`min_daily_limit` 은 반드시 `can_sell_all` 을 호출해서 판정해야 합니다.**
  채점기가 호출 횟수를 셉니다.
- **`O(log)` 로 풀어 주세요.** `1` 부터 하나씩 올려 보면 안 됩니다.
- 입력을 바꾸지 마세요.

## 왜 이진 탐색인가

이 문제의 모양을 보세요.

```
한도:        1    2    3    4    5    6   ...
가능한가?    X    X    X    O    O    O   ...
                        ^
                     답은 여기
```

한도를 올리면 **한 번 가능해진 뒤로는 계속 가능합니다.** 그러니까 `X` 와 `O` 의 경계를
찾는 문제이고, 그건 정렬된 배열에서 값을 찾는 것과 똑같습니다.
Week 05 의 C 과제에서 만든 `first_at_or_after` 와 **같은 일**입니다.

다른 점은 **찾을 배열이 없다**는 것입니다. 배열 대신 "가능한 답의 범위" 안에서 찾습니다.
그 범위의 각 지점이 `O` 인지 `X` 인지는 `can_sell_all` 이 알려 줍니다.

```
lo = 1, hi = max(holdings)
반복: mid 를 잡고 can_sell_all(mid) 이면 더 작게, 아니면 더 크게
```

판정은 쉬운데 최솟값 찾기는 어려운 문제를 보면 이 패턴을 떠올리면 됩니다.
한 번 손으로 써 보면 계속 쓰게 됩니다.

## 한 계좌에 며칠이 걸리나

`pile` 주를 한도 `limit` 으로 팔면 `ceil(pile / limit)` 일이 걸립니다.

```python
import math
days_needed = math.ceil(pile / limit)
# 또는 정수만으로:  (pile + limit - 1) // limit
```

## 예시 몇 개 더

```python
min_daily_limit([30, 11, 23, 4, 20], 5)   # 30  (계좌 수와 날짜가 같으면 하루에 한 계좌씩)
min_daily_limit([30, 11, 23, 4, 20], 6)   # 23
min_daily_limit([5], 5)                   # 1
min_daily_limit([1000], 1)                # 1000
min_daily_limit([10, 10], 4)              # 5
min_daily_limit([7], 2)                   # 4
```

## 채점

```sh
uv run runner.py test 5 --task order_split
```

## 생각해 볼 것

- `can_sell_all` 을 몇 번 부르게 되나요? 한도의 최대값이 1000 이라면 이진 탐색은 10여 번,
  하나씩 올려 보면 최대 1000 번입니다. 채점기가 이 차이로 `O(log)` 를 확인합니다.
- `while lo < hi` 로 쓸 때, `can_sell_all(mid)` 이 참이면 `hi = mid` 이고 거짓이면
  `lo = mid + 1` 입니다. **왜 `hi = mid - 1` 이 아닌가요?** 한 칸만 틀려도 답을 지나칩니다.
- `days == len(holdings)` 인 경우의 답이 왜 `max(holdings)` 인지 설명해 보세요.
- 이 패턴을 쓸 수 있는 조건은 "한도를 올리면 계속 가능하다"는 **단조성**입니다.
  만약 한도를 올렸는데 다시 불가능해지는 문제라면 이진 탐색을 쓸 수 있을까요?
