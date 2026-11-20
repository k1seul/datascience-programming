# Week 08 / C (중간) — 덱으로 푸는 두 문제

배열로 **원형 덱**을 만들고, 그 덱을 두 가지 방식으로 써 봅니다.

- **뒤쪽만** 쓰면 스택이 됩니다. (b) "며칠 뒤에 따뜻해지나"
- **뒤에 넣고 앞에서 빼면** 큐가 됩니다. (c) "창마다 첫 음수"

| 소문항 | 함수 | 배점 |
|---|---|---|
| (a) | `dq_create`, `dq_free`, `dq_is_empty`, `dq_is_full`, `push` / `pop` / `peek` 여섯 개 | 40 |
| (b) | `days_until_warmer` | 30 |
| (c) | `first_negative` | 30 |

## 구조체

`deque.h` 에 이미 정의되어 있습니다. **이 파일은 고치지 마세요.** 함수는 모두 `solution.c` 에 작성합니다.

```c
typedef struct {
    int *buf;       /* capacity 칸짜리 배열 */
    int capacity;   /* 최대 몇 개까지 들어가는지 */
    int size;       /* 지금 몇 개 들어 있는지 */
    int front;      /* 맨 앞 원소가 있는 인덱스 */
    int rear;       /* 맨 뒤 원소 바로 다음 칸: push_back 이 다음에 쓸 자리 */
} Deque;
```

Week 06 의 덱에 **`rear` 가 하나 더** 있습니다. 언제나 `rear == (front + size) % capacity` 가 되도록 유지하세요.

```
capacity = 4, front = 3, size = 3, rear = 2

인덱스    0     1     2     3
buf    [  1  |  2  |  ?  |  0  ]
                      ^     ^
                    rear  front

앞에서부터 읽으면 buf[3], buf[0], buf[1]  ->  0, 1, 2
```

## (a) 원형 덱 — 40점

```c
Deque *dq_create(int capacity);
void dq_free(Deque *dq);
int dq_is_empty(const Deque *dq);
int dq_is_full(const Deque *dq);
int dq_push_front(Deque *dq, int value);
int dq_push_back(Deque *dq, int value);
int dq_pop_front(Deque *dq, int *out);
int dq_pop_back(Deque *dq, int *out);
int dq_peek_front(const Deque *dq, int *out);
int dq_peek_back(const Deque *dq, int *out);
```

- `dq_create` 는 `front`, `rear`, `size` 를 모두 `0` 으로 둡니다. `capacity` 가 1 보다 작으면 `NULL` 을 반환합니다.
- `dq_free` 는 `buf` 와 덱을 해제합니다. `NULL` 을 받으면 아무것도 하지 않습니다.
- `push`, `pop`, `peek` 은 **성공하면 `1`, 실패하면 `0`** 입니다. 꽉 찼을 때 `push`, 비었을 때 `pop` / `peek` 이 실패합니다.
  실패하면 덱과 `*out` 을 건드리지 않습니다.

각 함수가 바꾸는 값입니다.

| 함수 | 읽거나 쓰는 자리 | 바뀌는 것 |
|---|---|---|
| `push_back` | `buf[rear]` 에 쓰기 | `rear` 한 칸 오른쪽, `size + 1` |
| `push_front` | `front` 를 한 칸 왼쪽으로 옮긴 뒤 `buf[front]` 에 쓰기 | `size + 1` |
| `pop_front` | `buf[front]` 읽기 | `front` 한 칸 오른쪽, `size - 1` |
| `pop_back` | `rear` 를 한 칸 왼쪽으로 옮긴 뒤 `buf[rear]` 읽기 | `size - 1` |
| `peek_back` | `rear` 바로 왼쪽 칸 읽기 | 없음 |

## (b) `days_until_warmer` — 30점

```c
int days_until_warmer(const int *temps, int n, int *answer);
```

`temps[i]` 는 `i` 일의 기온입니다. `answer[i]` 에 "**며칠 뒤에 처음으로 더 따뜻한 날이 오는지**"를 쓰고,
그런 날이 없으면 `0` 을 씁니다. `n` 을 반환합니다. 같은 기온은 더 따뜻한 날이 아닙니다.

```
temps    73  74  75  71  69  72  76  73
answer    1   1   4   2   1   1   0   0
```

`75` 도인 2일은 4일 뒤인 6일(`76`)에 처음으로 더 따뜻해지니 `4` 입니다.

**덱을 스택처럼 쓰세요.** 아직 더 따뜻한 날을 만나지 못한 날의 번호를 뒤에 쌓아 둡니다.
새 날이 오면 그날보다 추운 날들을 뒤에서부터 꺼내면서 답을 적고, 새 날의 번호를 넣습니다.
덱은 `dq_create(n)` 으로 만들고 반환하기 전에 해제하세요.

## (c) `first_negative` — 30점

```c
int first_negative(const int *nums, int n, int k, int *result);
```

길이 `k` 인 창을 한 칸씩 밀면서, **창 안의 첫 번째 음수**를 `result` 에 씁니다. 창에 음수가 없으면 `0` 입니다.
창은 `n - k + 1` 개이고 그 수를 반환합니다. `k` 가 1 보다 작거나 `n` 보다 크면 `-1` 을 반환합니다.

```
nums     12  -1  -7   8 -15  30  16  28       k = 3

창 [12 -1 -7]  [-1 -7 8]  [-7 8 -15]  [8 -15 30]  [-15 30 16]  [30 16 28]
결과    -1         -1          -7         -15          -15           0
```

**덱을 큐처럼 쓰세요.** 음수의 **인덱스**만 뒤에 넣습니다. 맨 앞 인덱스가 창을 벗어나면 앞에서 꺼냅니다.
그러면 덱의 맨 앞이 언제나 창 안의 첫 음수입니다. 덱은 `dq_create(k)` 로 만들면 충분합니다.

## 지켜야 할 것

- `deque.h` 는 고치지 마세요.
- **`malloc` 한 것은 모두 `free` 하세요.** 채점기가 `malloc` 과 `free` 횟수를 셉니다. (b), (c) 안에서 만든 덱도 해제해야 합니다.
- **(b), (c) 는 큰 입력도 2초 안에 끝나야 합니다.** 채점기가 길이 20만짜리 입력을 넣습니다.
  날마다(창마다) 처음부터 다시 훑으면 10¹⁰ 번이 넘게 비교해서 끝나지 않습니다.
- 원소를 `buf` 안에서 옮기지 마세요. 채점기가 `front`, `rear` 와 `buf` 를 직접 읽어서 확인합니다.

## 직접 확인하기

시험장처럼 `main.c` 로 확인해 보세요. 각 줄 아래의 `Expected:` 줄과 똑같이 나오면 됩니다.

```sh
cd exercises/week_08_test_prep/c/medium_deque_windows
cc -Wall -Wextra -o main main.c solution.c && ./main
```

## 채점

```sh
uv run runner.py test 8 --task deque_windows
```

(a) 의 덱이 틀리면 (b), (c) 가 배열 밖에 쓰다가 테스트 전체가 멈출 수 있습니다(💥 중단됨).
그럴 때는 (a) 만 먼저 채점해서 덱부터 고치세요.

```sh
uv run runner.py test 8 --task deque_windows -k test_a
```

## 힌트

막힐 때 하나씩 펼쳐 보세요.

<details>
<summary>힌트 1 — 한 칸 왼쪽, 한 칸 오른쪽</summary>

오른쪽으로 한 칸은 `(i + 1) % capacity`, 왼쪽으로 한 칸은 `(i - 1 + capacity) % capacity` 입니다.
C 에서 `-1 % 4` 는 `3` 이 아니라 `-1` 이라서 `+ capacity` 가 꼭 필요합니다.

`pop_back` 과 `peek_back` 이 읽는 칸은 `rear` 가 아니라 **`rear` 의 한 칸 왼쪽**입니다.

</details>

<details>
<summary>힌트 2 — days_until_warmer 의 뼈대</summary>

```c
Deque *waiting = dq_create(n);     /* 아직 답을 못 정한 날들 */
int day;
for (int i = 0; i < n; i++) {
    answer[i] = 0;
    while (dq_peek_back(waiting, &day) && temps[day] < temps[i]) {
        /* day 는 i 일에 처음으로 더 따뜻한 날을 만났습니다 */
        ...
    }
    dq_push_back(waiting, i);
}
dq_free(waiting);
```

덱에 남은 날들은 뒤로 갈수록 기온이 낮거나 같습니다. 그래서 맨 뒤 날이 새 날보다 따뜻하면 그 앞은 더 볼 필요가 없습니다.

</details>

<details>
<summary>힌트 3 — first_negative 의 뼈대</summary>

`i` 번째 값을 볼 때 네 가지를 차례로 합니다.

1. 맨 앞 인덱스가 `i - k` 이하이면 창을 벗어났으니 앞에서 꺼냅니다.
2. `nums[i]` 가 음수이면 `i` 를 뒤에 넣습니다.
3. `i >= k - 1` 이면 창 하나가 완성된 것입니다.
4. 덱이 비어 있지 않으면 `result[i - k + 1] = nums[맨 앞 인덱스]`, 비어 있으면 `0` 입니다.

</details>

## 자주 하는 실수

**`rear` 를 갱신하지 않기**

`push_back` 에서 `size` 만 늘리고 `rear` 를 옮기지 않으면, 다음 `push_back` 이 같은 칸에 덮어씁니다.

**`push_front` 와 `pop_back` 에서 `-1` 을 그냥 쓰기**

`front` 나 `rear` 가 `0` 일 때 `-1` 이 되어 배열 밖을 읽고 씁니다. 힌트 1을 보세요.

**값을 덱에 넣기**

(b), (c) 모두 **인덱스**를 넣어야 합니다. 값만 있으면 며칠 차이인지, 창을 벗어났는지 알 수 없습니다.

**덱을 해제하지 않기**

(b), (c) 안에서 `dq_create` 로 만든 덱은 반환하기 전에 `dq_free` 해야 합니다.

## 더 생각해 볼 것

- (b) 에서 덱의 크기는 왜 `n` 이어야 할까요? 기온이 계속 떨어지는 날들을 떠올려 보세요.
- (c) 를 "창마다 **가장 작은** 값"으로 바꾸면 무엇을 더 해야 할까요? (b) 에서 뒤쪽 원소를 꺼내던 방법이 필요합니다.
