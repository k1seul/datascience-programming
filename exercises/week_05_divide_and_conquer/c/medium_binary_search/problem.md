# Week 05 / C (중간) — 이진 탐색

오름차순으로 정렬된 정수 배열에서 값을 찾는 함수 네 개를 작성하세요.

## 문제

정수 배열 `values` 와 그 길이 `n` 이 주어집니다.

- `values` 는 **오름차순으로 정렬**되어 있습니다.
- **같은 값이 여러 번** 들어 있을 수 있습니다.
- `n` 은 0일 수도 있습니다 (빈 배열).

네 함수는 각각 다음 값을 반환합니다.

| 함수 | 반환값 |
|---|---|
| `binary_search(values, n, target)` | `target` 과 같은 원소의 인덱스. 없으면 `-1` |
| `lower_bound(values, n, target)` | 값이 `target` **이상**인 원소가 처음 나오는 인덱스 |
| `upper_bound(values, n, target)` | 값이 `target` **초과**인 원소가 처음 나오는 인덱스 |
| `count_equal(values, n, target)` | `target` 과 같은 원소의 개수 |

두 가지 규칙이 더 있습니다.

- `binary_search` 는 같은 값이 여러 개면 **그중 어느 인덱스를 반환해도** 정답입니다.
- `lower_bound` 와 `upper_bound` 는 조건을 만족하는 원소가 없으면 **`n`** 을 반환합니다.

## 예시

```
values = [1, 2, 2, 2, 5]     (n = 5)
인덱스     0  1  2  3  4
```

| `target` | `binary_search` | `lower_bound` | `upper_bound` | `count_equal` |
|---|---|---|---|---|
| `0` | `-1` | `0` | `0` | `0` |
| `1` | `0` | `0` | `1` | `1` |
| `2` | `1`, `2`, `3` 중 하나 | `1` | `4` | `3` |
| `3` | `-1` | `4` | `4` | `0` |
| `5` | `4` | `4` | `5` | `1` |
| `6` | `-1` | `5` | `5` | `0` |

몇 줄만 풀어서 보면 이렇습니다.

- **`target = 2`** : 2 이상인 첫 원소는 인덱스 1의 `2` 입니다. 2보다 큰 첫 원소는 인덱스 4의 `5` 입니다.
  2는 인덱스 1, 2, 3에 세 개 있습니다.
- **`target = 3`** : 3은 배열에 없습니다. 그래도 `lower_bound` 는 3 이상인 첫 원소(인덱스 4의 `5`)를
  가리킵니다. "3을 넣는다면 들어갈 자리"라고 생각하면 됩니다.
- **`target = 6`** : 6 이상인 원소가 하나도 없습니다. 그래서 `lower_bound` 와 `upper_bound` 모두
  `n` 인 `5` 를 반환합니다.

빈 배열(`n = 0`)이면 `binary_search` 는 `-1`, 나머지 세 함수는 `0` 을 반환합니다.

## 구현할 함수

`search.h` 에 선언되어 있습니다. `solution.c` 에 작성하세요.

```c
int binary_search(const int *values, int n, int target);
int lower_bound(const int *values, int n, int target);
int upper_bound(const int *values, int n, int target);
int count_equal(const int *values, int n, int target);
```

## 지켜야 할 것

- **`O(log n)` 으로 작성하세요.** 배열을 처음부터 하나씩 확인하는 방식은 안 됩니다.
  한 번 비교할 때마다 남은 탐색 범위를 절반으로 줄여야 합니다.
- C 표준 라이브러리의 `bsearch` 는 쓰지 마세요. 채점기가 소스를 확인합니다.
- 배열을 정렬하거나 수정하지 마세요. 이미 정렬되어 있습니다.
- 반복문과 재귀 중 편한 쪽을 쓰면 됩니다.

## 채점

```sh
uv run runner.py test 5 --task binary_search
```

## 힌트

막힐 때 하나씩 펼쳐 보세요.

<details>
<summary>힌트 1 — 이진 탐색은 어떻게 동작하나요?</summary>

정렬된 배열의 **가운데 원소**를 봅니다.

- 가운데 원소가 `target` 보다 작으면, `target` 은 오른쪽 절반에만 있을 수 있습니다. 왼쪽 절반은 버립니다.
- 가운데 원소가 `target` 보다 크면, 반대로 오른쪽 절반을 버립니다.

남은 절반에서 같은 일을 반복합니다. 범위가 매번 절반이 되니 100만 개짜리 배열도 20번 정도면 끝납니다.

```
[1  3  5  7  9]    7을 찾는다
       ^           가운데는 5. 7보다 작으니 왼쪽은 버린다
          [7  9]
           ^       찾았다
```

</details>

<details>
<summary>힌트 2 — lower_bound 의 기본 틀</summary>

아래 틀을 그대로 쓰면 경계 실수를 거의 피할 수 있습니다.

```c
int lo = 0, hi = n;                /* 답은 [lo, hi] 범위 안에 있다 */
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (values[mid] >= target)
        hi = mid;                  /* mid 가 답일 수도 있으니 남긴다 */
    else
        lo = mid + 1;              /* mid 는 확실히 답이 아니다 */
}
return lo;                         /* 반복이 끝나면 lo == hi 가 답 */
```

`hi` 를 `n - 1` 이 아니라 **`n`** 으로 시작하는 점을 눈여겨보세요. 답이 `n` 일 수 있기 때문입니다.

</details>

<details>
<summary>힌트 3 — upper_bound 는 무엇이 다른가요?</summary>

힌트 2의 코드에서 **조건 하나만** 바꾸면 됩니다. `>=` 를 `>` 로요.

`lower_bound` 는 "`target` 이상이 처음 나오는 곳", `upper_bound` 는 "`target` 초과가 처음 나오는 곳"이니까요.

</details>

<details>
<summary>힌트 4 — count_equal 과 binary_search</summary>

예시 표에서 `upper_bound` 열의 값에서 `lower_bound` 열의 값을 빼 보세요.

`binary_search` 는 `lower_bound` 가 가리키는 자리에 정말 `target` 이 있는지만 확인하면 됩니다.
그 자리가 `n` 일 수도 있으니 배열 밖을 읽지 않도록 조심하세요.

</details>

## 자주 하는 실수

**가운데 인덱스를 `(lo + hi) / 2` 로 구하기**

```c
int mid = (lo + hi) / 2;          /* lo + hi 가 int 범위를 넘으면 음수가 됩니다 */
int mid = lo + (hi - lo) / 2;     /* 이렇게 쓰세요 */
```

이번 테스트에서는 드러나지 않지만, 배열이 아주 크면 실제로 터지는 버그입니다.

**경계를 섞어 쓰기**

`hi = n` 으로 시작했다면 `while (lo < hi)` 와 `hi = mid` 를 함께 써야 합니다.
`hi = n - 1` 로 시작했다면 `while (lo <= hi)` 와 `hi = mid - 1` 이 짝입니다.
두 방식을 섞으면 무한 루프에 빠지거나 답을 한 칸 지나칩니다. 한 가지만 골라 쓰세요.

**없을 때 `-1` 을 반환하기**

`lower_bound` 와 `upper_bound` 는 찾는 값보다 큰 원소가 없을 때 `-1` 이 아니라 `n` 을 반환해야 합니다.

## 더 생각해 볼 것

- 힌트 2의 코드에서 `while (lo <= hi)` 로 바꾸면 어떤 입력에서 문제가 생길까요?
- 배열이 정렬되어 있지 않으면 이진 탐색을 쓸 수 없는 이유는 무엇일까요?
