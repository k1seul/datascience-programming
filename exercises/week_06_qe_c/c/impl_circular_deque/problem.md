# Week 06 / C (구현) — 원형 덱과 작업 스케줄러

배열 하나로 **앞과 뒤 양쪽에서 넣고 뺄 수 있는 덱(deque)** 을 만들고,
그 덱으로 여러 작업을 돌아가며 처리하는 **스케줄러**를 만듭니다.

소문항이 네 개 있습니다. 앞에서 만든 함수를 뒤 소문항에서 그대로 씁니다.

| 소문항 | 함수 | 배점 |
|---|---|---|
| (a) | `deque_create`, `deque_free` | 10 |
| (b) | `deque_is_empty`, `deque_is_full`, `push` / `pop` / `peek` 여섯 개 | 40 |
| (c) | `deque_print` | 10 |
| (d) | `round_robin` | 40 |

## 구조체

`deque.h` 에 이미 정의되어 있습니다. **이 파일은 고치지 마세요.** 함수는 모두 `solution.c` 에 작성합니다.

```c
typedef struct {
    int *buf;       /* capacity 칸짜리 배열 */
    int capacity;   /* 최대 몇 개까지 들어가는지 */
    int size;       /* 지금 몇 개 들어 있는지 */
    int front;      /* 맨 앞 원소가 있는 인덱스 */
} Deque;
```

덱의 원소는 `buf[front]` 부터 시작해서 오른쪽으로 `size` 개입니다.
배열 끝을 넘어가면 **처음(인덱스 0)으로 돌아옵니다.** 그래서 "원형"입니다.

```
capacity = 4, front = 3, size = 3

인덱스    0     1     2     3
buf    [  1  |  2  |  ?  |  0  ]
                            ^ front

앞에서부터 읽으면 buf[3], buf[0], buf[1]  ->  0, 1, 2
```

`i` 번째 원소(맨 앞이 0번째)는 `buf[(front + i) % capacity]` 에 있습니다.

**원소는 `buf` 안에서 절대 옮기지 않습니다.** 넣고 뺄 때 바뀌는 것은 `front` 와 `size` 뿐입니다.

## (a) `deque_create`, `deque_free` — 10점

```c
Deque *deque_create(int capacity);
void deque_free(Deque *dq);
```

- `deque_create` 는 비어 있는 덱을 만들어 반환합니다. `buf` 는 `capacity` 칸을 할당하고,
  `size` 는 `0`, `front` 는 `0` 으로 둡니다.
- `capacity` 가 1 보다 작으면 아무것도 할당하지 말고 `NULL` 을 반환합니다.
- `deque_free` 는 `buf` 와 덱 자체를 모두 해제합니다. `NULL` 을 받으면 아무것도 하지 않습니다.

## (b) 넣기, 빼기, 들여다보기 — 40점

```c
int deque_is_empty(const Deque *dq);
int deque_is_full(const Deque *dq);

int deque_push_front(Deque *dq, int value);
int deque_push_back(Deque *dq, int value);
int deque_pop_front(Deque *dq, int *out);
int deque_pop_back(Deque *dq, int *out);
int deque_peek_front(const Deque *dq, int *out);
int deque_peek_back(const Deque *dq, int *out);
```

`deque_is_empty` 와 `deque_is_full` 은 맞으면 `1`, 아니면 `0` 을 반환합니다.
나머지 여섯 함수는 **성공하면 `1`, 실패하면 `0`** 을 반환합니다.

- 덱이 꽉 찼을 때 `push` 는 실패합니다. 덱은 그대로 둡니다.
- 덱이 비었을 때 `pop` 과 `peek` 은 실패합니다. 이때 `*out` 은 건드리지 않습니다.
- `pop` 은 꺼낸 값을 `*out` 에 쓰고 덱에서 지웁니다. `peek` 은 값만 `*out` 에 쓰고 덱은 그대로 둡니다.

각 함수가 `front` 와 `size` 를 이렇게 바꿉니다.

| 함수 | `front` | `size` | 값을 넣거나 읽는 자리 |
|---|---|---|---|
| `push_front` | 한 칸 왼쪽으로 (`0` 이면 `capacity - 1`) | +1 | 바뀐 `front` |
| `pop_front` | 한 칸 오른쪽으로 (`capacity - 1` 이면 `0`) | -1 | 바뀌기 전 `front` |
| `push_back` | 그대로 | +1 | `(front + size) % capacity` (`size` 를 늘리기 전) |
| `pop_back` | 그대로 | -1 | `(front + size - 1) % capacity` (`size` 를 줄이기 전) |

`capacity = 4` 인 덱으로 따라가 보면 이렇습니다.

| 호출 | 반환 | `front` | `size` | 앞 → 뒤 |
|---|---|---|---|---|
| `deque_create(4)` | | 0 | 0 | `[]` |
| `push_back(1)` | 1 | 0 | 1 | `[1]` |
| `push_back(2)` | 1 | 0 | 2 | `[1, 2]` |
| `push_front(0)` | 1 | **3** | 3 | `[0, 1, 2]` |
| `pop_back` → `2` | 1 | 3 | 2 | `[0, 1]` |
| `pop_front` → `0` | 1 | **0** | 1 | `[1]` |

`push_front(0)` 에서 `front` 가 `0` 이었으니 `3` 으로 넘어갔고, `0` 은 `buf[3]` 에 들어갔습니다.
`1` 과 `2` 는 처음 넣은 `buf[0]`, `buf[1]` 에 그대로 있습니다.

## (c) `deque_print` — 10점

```c
void deque_print(const Deque *dq);
```

원소를 앞에서부터 아래 형식으로 출력하고 줄을 바꿉니다. 채점기가 **글자 하나까지** 비교합니다.

| 덱 (앞 → 뒤) | 출력 |
|---|---|
| `3, 1, 4` | `[3, 1, 4]` |
| `7` | `[7]` |
| 비어 있음 | `[]` |

쉼표 뒤에 공백이 하나 있고, 마지막 원소 뒤에는 쉼표가 없습니다.

## (d) `round_robin` — 40점

```c
int round_robin(const int *burst, int n, int quantum, int *finish_order);
```

작업이 `n` 개 있고, 작업 `i` 를 끝내려면 `burst[i]` 만큼 시간이 필요합니다.
CPU 하나로 이 작업들을 **돌아가며 조금씩** 처리합니다.

1. 처음에는 작업 `0, 1, ..., n-1` 이 순서대로 줄을 섭니다.
2. 줄 맨 앞의 작업을 꺼내서 `quantum` 만큼 실행합니다. 남은 시간이 `quantum` 보다 적으면 남은 만큼만 실행합니다.
3. 그 작업이 끝났으면 `finish_order` 에 적습니다. 아직 남았으면 줄 맨 뒤로 보냅니다.
4. 줄이 빌 때까지 2~3을 반복합니다.

`finish_order` 에는 작업이 **끝난 순서대로** 작업 번호를 적고, `n` 을 반환합니다.

`burst = [5, 2, 4]`, `quantum = 2` 이면 이렇게 진행됩니다.

| 차례 | 꺼낸 작업 | 실행한 시간 | 그 작업에 남은 시간 | 줄 (앞 → 뒤) | `finish_order` |
|---|---|---|---|---|---|
| 시작 | | | | `0, 1, 2` | |
| 1 | 0 | 2 | 3 | `1, 2, 0` | |
| 2 | 1 | 2 | 0 → 끝 | `2, 0` | `1` |
| 3 | 2 | 2 | 2 | `0, 2` | `1` |
| 4 | 0 | 2 | 1 | `2, 0` | `1` |
| 5 | 2 | 2 | 0 → 끝 | `0` | `1, 2` |
| 6 | 0 | 1 | 0 → 끝 | | `1, 2, 0` |

그래서 `finish_order` 는 `[1, 2, 0]` 이고 반환값은 `3` 입니다.

| `burst` | `quantum` | `finish_order` |
|---|---|---|
| `[3, 1, 2]` | `1` | `[1, 2, 0]` |
| `[6, 1, 3, 2]` | `2` | `[1, 3, 2, 0]` |
| `[4, 3, 5]` | `10` | `[0, 1, 2]` (`quantum` 이 크면 들어온 순서대로 끝납니다) |
| `[]` | `2` | `[]`, 반환값 `0` |

- `burst` 의 각 값은 1 이상입니다. `finish_order` 에는 `n` 칸이 있습니다.
- `quantum` 이 1 보다 작으면 `-1` 을 반환합니다.
- **줄은 (a), (b) 에서 만든 덱으로 만드세요.** 작업 번호를 덱에 넣고 빼면 됩니다.
- `burst` 는 `const` 라서 바꿀 수 없습니다. 남은 시간은 따로 저장해야 합니다.

## 지켜야 할 것

- `deque.h` 는 고치지 마세요.
- **`deque_print` 말고는 아무것도 출력하지 마세요.** 디버그용 `printf` 가 남아 있으면 채점기가 실패로 처리합니다.
- **`malloc` 한 것은 모두 `free` 하세요.** 채점기가 `malloc` 과 `free` 횟수를 세어서,
  `deque_free` 뒤나 `round_robin` 이 끝난 뒤에 남은 메모리가 있으면 실패로 처리합니다.
- 원소를 `buf` 안에서 옮기지 마세요. 채점기가 `front` 와 `buf` 를 직접 읽어서 확인합니다.

## 직접 확인하기

시험장에는 채점기가 없고 `main.c` 만 주어집니다. 같은 방식으로 확인해 보세요.

```sh
cd exercises/week_06_qe_c/c/impl_circular_deque
cc -Wall -Wextra -o main main.c solution.c && ./main
```

각 줄 아래의 `Expected:` 줄과 똑같이 나오면 됩니다.
아직 안 쓴 함수가 있으면 `unused parameter` 경고가 나오는데, 다 쓰고 나면 사라집니다.

## 채점

```sh
uv run runner.py test 6 --task circular_deque
```

테스트 이름이 `test_a_`, `test_b_` 처럼 소문항으로 시작하니, 어느 소문항이 틀렸는지 바로 알 수 있습니다.

## 힌트

막힐 때 하나씩 펼쳐 보세요.

<details>
<summary>힌트 1 — 한 칸 왼쪽, 한 칸 오른쪽</summary>

오른쪽으로 한 칸은 `(front + 1) % capacity` 입니다. `capacity - 1` 다음이 `0` 이 됩니다.

왼쪽으로 한 칸은 `(front - 1 + capacity) % capacity` 입니다. `+ capacity` 를 빼면 안 됩니다.
C 에서 `-1 % 4` 는 `3` 이 아니라 **`-1`** 이기 때문입니다.

</details>

<details>
<summary>힌트 2 — deque_create 에서 할당은 두 번</summary>

덱 구조체 하나, `buf` 배열 하나를 따로 `malloc` 합니다.

```c
Deque *dq = malloc(sizeof(Deque));
dq->buf = malloc(sizeof(int) * capacity);
```

두 번째 `malloc` 이 실패하면 첫 번째로 받은 `dq` 를 `free` 하고 `NULL` 을 반환하세요.
해제할 때는 반대 순서입니다. `dq->buf` 를 먼저, `dq` 를 나중에 해제합니다.

</details>

<details>
<summary>힌트 3 — round_robin 의 뼈대</summary>

1. 남은 시간을 담을 배열 `left` 를 `malloc` 하고 `burst` 를 복사합니다.
2. `deque_create(n)` 으로 줄을 만들고 `0` 부터 `n - 1` 까지 `push_back` 합니다.
3. `pop_front` 가 성공하는 동안 반복합니다. 꺼낸 작업의 `left` 를 줄이고,
   `0` 이 되면 `finish_order` 에 적고, 아니면 다시 `push_back` 합니다.
4. `left` 와 덱을 해제합니다.

줄에는 작업이 많아야 `n` 개 들어 있으니 덱이 꽉 차서 `push_back` 이 실패하는 일은 없습니다.

</details>

## 자주 하는 실수

**`push_front` 에서 `front - 1` 을 그냥 쓰기**

`front` 가 `0` 일 때 `-1` 이 되어 배열 밖에 씁니다. 힌트 1을 보세요.

**`pop_back` 에서 `front` 를 바꾸기**

뒤에서 꺼낼 때는 `size` 만 줄이면 됩니다. 맨 앞 원소는 그대로이니 `front` 도 그대로입니다.

**`deque_free` 에서 하나만 해제하기**

`free(dq)` 만 하면 `buf` 가 남고, `free(dq->buf)` 만 하면 구조체가 남습니다.
`free(dq)` 를 먼저 하면 그 뒤에 `dq->buf` 를 읽을 수 없습니다.

**`round_robin` 에서 `left` 나 덱을 해제하지 않기**

함수 안에서 만든 것은 반환하기 전에 모두 해제해야 합니다.

## 더 생각해 볼 것

- `size` 없이 `front` 와 `rear` 만으로 덱을 만들면, 꽉 찬 덱과 빈 덱을 어떻게 구별할 수 있을까요?
- `round_robin` 에서 각 작업이 **끝난 시각**도 구하려면 무엇을 더 저장해야 할까요?
