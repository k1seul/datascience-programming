# Week 06 / C (구현) — 최근 본 상품 목록

쇼핑몰의 "최근 본 상품" 목록을 **이중 연결 리스트**로 만듭니다.

- 가장 최근에 본 상품이 맨 앞에 옵니다.
- 이미 목록에 있는 상품을 다시 보면 맨 앞으로 올라옵니다.
- 정해진 개수(`capacity`)를 넘으면 가장 오래전에 본 상품이 빠집니다.

소문항이 일곱 개 있습니다. 작은 함수부터 만들고, 뒤 소문항에서 앞의 함수를 조합해서 씁니다.

| 소문항 | 함수 | 하는 일 | 배점 |
|---|---|---|---|
| (a) | `item_create`, `recent_create`, `recent_free` | 만들기, 해제하기 | 10 |
| (b) | `recent_push_front` | 노드를 맨 앞에 붙이기 | 15 |
| (c) | `recent_detach` | 노드를 목록에서 떼어 내기 | 20 |
| (d) | `recent_find` | id 로 노드 찾기 | 10 |
| (e) | `recent_view` | 상품을 봤을 때 목록 갱신하기 | 25 |
| (f) | `recent_remove` | 상품 지우기 | 10 |
| (g) | `recent_print` | 목록 출력하기 | 10 |

## 구조체

`recent.h` 에 이미 정의되어 있습니다. **이 파일은 고치지 마세요.** 함수는 모두 `solution.c` 에 작성합니다.

```c
typedef struct Item {
    int id;
    struct Item *prev;   /* 앞쪽 노드 (더 최근에 본 상품) */
    struct Item *next;   /* 뒤쪽 노드 (더 오래전에 본 상품) */
} Item;

typedef struct {
    int capacity;   /* 최대 몇 개까지 기억하는지 */
    int size;       /* 지금 몇 개 들어 있는지 */
    Item *head;     /* 가장 최근에 본 상품. 비었으면 NULL */
    Item *tail;     /* 가장 오래전에 본 상품. 비었으면 NULL */
} RecentList;
```

상품 9, 2, 5 를 이 순서로 최근에 봤다면 이렇게 이어져 있습니다.

```
            head                           tail
             v                              v
  NULL <-- [ 9 ] <-----> [ 2 ] <-----> [ 5 ] --> NULL
           가장 최근                    가장 오래전
```

노드마다 화살표가 **두 개**(`prev`, `next`)입니다. 목록을 바꿀 때마다 아래 네 가지가 지켜져야 합니다.

1. `head->prev` 와 `tail->next` 는 `NULL` 입니다. 목록이 비었으면 `head` 와 `tail` 이 모두 `NULL` 입니다.
2. `a->next` 가 `b` 이면 `b->prev` 는 `a` 입니다. 반대도 마찬가지입니다.
3. `head` 에서 `next` 를 따라가면 `tail` 에서 끝납니다.
4. `size` 는 실제 노드 수와 같습니다.

**채점기는 매번 구조체를 직접 읽어서 이 네 가지를 확인합니다.** `next` 만 맞고 `prev` 를 깜빡하면 바로 걸립니다.

## (a) `item_create`, `recent_create`, `recent_free` — 10점

```c
Item *item_create(int id);
RecentList *recent_create(int capacity);
void recent_free(RecentList *list);
```

- `item_create` 는 노드 하나를 `malloc` 해서 `id` 를 넣고, `prev` 와 `next` 는 `NULL` 로 둡니다.
- `recent_create` 는 빈 목록을 만듭니다. `size` 는 `0`, `head` 와 `tail` 은 `NULL` 입니다.
  `capacity` 가 1 보다 작으면 `NULL` 을 반환합니다.
- `recent_free` 는 목록에 남은 노드를 모두 해제하고, 목록 자체도 해제합니다. `NULL` 을 받으면 아무것도 하지 않습니다.

## (b) `recent_push_front` — 15점

```c
void recent_push_front(RecentList *list, Item *item);
```

다른 목록에 들어 있지 않은 노드 `item` 을 **맨 앞(`head`)** 에 붙이고 `size` 를 1 늘립니다.
`capacity` 는 보지 않습니다. 넘치는 것은 (e)에서 처리합니다.

```
붙이기 전:   head -> [ 2 ] <-> [ 5 ]          item = [ 9 ]

붙인 뒤:     head -> [ 9 ] <-> [ 2 ] <-> [ 5 ]
```

바꿔야 할 포인터는 `item->prev`, `item->next`, 원래 맨 앞 노드의 `prev`, 그리고 `list->head` 입니다.
목록이 비어 있었다면 원래 맨 앞 노드가 없으니, 대신 `list->tail` 도 `item` 이 됩니다.

## (c) `recent_detach` — 20점

```c
void recent_detach(RecentList *list, Item *item);
```

목록 안의 노드 `item` 을 **떼어 내고** `size` 를 1 줄입니다. 떼어 낸 노드의 `prev` 와 `next` 는 `NULL` 로 바꿉니다.
**해제(`free`)는 하지 않습니다.** 떼어 낸 노드를 다른 곳에 다시 붙일 수 있어야 하기 때문입니다.

`item` 이 어디에 있느냐에 따라 바꿀 곳이 다릅니다.

| `item` 위치 | 예 (`[9, 2, 5]` 에서) | 결과 | 바뀌는 것 |
|---|---|---|---|
| 가운데 | `2` 를 떼기 | `[9, 5]` | `9->next` 는 `5`, `5->prev` 는 `9` |
| 맨 앞 | `9` 를 떼기 | `[2, 5]` | `head` 는 `2`, `2->prev` 는 `NULL` |
| 맨 뒤 | `5` 를 떼기 | `[9, 2]` | `tail` 은 `2`, `2->next` 는 `NULL` |
| 하나뿐 | `[7]` 에서 `7` 을 떼기 | `[]` | `head` 와 `tail` 이 모두 `NULL` |

## (d) `recent_find` — 10점

```c
Item *recent_find(const RecentList *list, int id);
```

`id` 가 같은 노드를 찾아서 **그 노드의 포인터**를 반환합니다. 없으면 `NULL` 입니다.
복사본이 아니라 목록 안에 있는 노드 자체를 반환해야 합니다.

## (e) `recent_view` — 25점

```c
void recent_view(RecentList *list, int id);
```

상품 `id` 를 봤을 때 목록을 갱신합니다. 경우가 셋입니다.

1. **이미 목록에 있으면** 그 노드를 맨 앞으로 옮깁니다. **노드를 새로 만들지 마세요.**
2. **목록에 없으면** 새 노드를 만들어 맨 앞에 붙입니다.
3. 2번 때문에 `size` 가 `capacity` 를 넘으면, 맨 뒤(가장 오래전에 본) 노드를 떼어 내고 **해제합니다.**

`capacity = 3` 으로 따라가 보면 이렇습니다.

| 호출 | 목록 (`head` → `tail`) | |
|---|---|---|
| `view(1)`, `view(2)`, `view(3)` | `[3, 2, 1]` | 새 상품은 맨 앞에 붙습니다 |
| `view(2)` | `[2, 3, 1]` | 이미 있으니 맨 앞으로 옮깁니다 |
| `view(4)` | `[4, 2, 3]` | 4를 붙이니 네 개가 되어, 맨 뒤의 1이 빠집니다 |
| `view(3)` | `[3, 4, 2]` | 이미 있으니 옮기기만 합니다. 아무것도 빠지지 않습니다 |

(b), (c), (d)의 함수로 모두 만들 수 있습니다.

## (f) `recent_remove` — 10점

```c
int recent_remove(RecentList *list, int id);
```

상품 `id` 의 노드를 목록에서 떼어 내고 **해제합니다.** 지웠으면 `1`, 목록에 없었으면 `0` 을 반환합니다.

## (g) `recent_print` — 10점

```c
void recent_print(const RecentList *list);
```

`head` 부터 `tail` 까지 `id` 를 아래 형식으로 출력하고 줄을 바꿉니다. 채점기가 **글자 하나까지** 비교합니다.

| 목록 | 출력 |
|---|---|
| `[5, 2, 9]` | `5 -> 2 -> 9` |
| `[7]` | `7` |
| 비어 있음 | `(empty)` |

## 지켜야 할 것

- `recent.h` 는 고치지 마세요.
- **`recent_print` 말고는 아무것도 출력하지 마세요.** 디버그용 `printf` 가 남아 있으면 채점기가 실패로 처리합니다.
- **`malloc` 한 것은 모두 `free` 하세요.** 채점기가 `malloc` 과 `free` 횟수를 셉니다.
  `recent_free` 뒤에 남은 노드가 있거나, (e)에서 밀려난 노드나 (f)에서 지운 노드를 해제하지 않으면 실패입니다.
- (e)에서 이미 있는 상품을 다시 볼 때 `malloc` 이 한 번이라도 불리면 실패입니다. 있던 노드를 옮기세요.

## 직접 확인하기

```sh
cd exercises/week_06_qe_c/c/impl_recent_list
cc -Wall -Wextra -o main main.c solution.c && ./main
```

`main.c` 는 목록을 `head` → `tail` 방향과 `tail` → `head` 방향으로 **두 번** 출력합니다.
`prev` 를 잘못 이었으면 두 번째 줄이 이상하게 나오니, `Expected:` 줄과 비교해 보세요.

## 채점

```sh
uv run runner.py test 6 --task recent_list
```

포인터를 잘못 이으면 해제된 메모리를 읽다가 테스트 전체가 멈출 수 있습니다(💥 중단됨).
그럴 때는 `-x` 를 붙여서 처음 실패한 테스트에서 멈추게 하면 원인을 찾기 쉽습니다.

```sh
uv run pytest exercises/week_06_qe_c/c/impl_recent_list -x
```

## 힌트

막힐 때 하나씩 펼쳐 보세요.

<details>
<summary>힌트 1 — push_front 는 순서가 중요합니다</summary>

`list->head` 를 먼저 바꾸면 원래 맨 앞 노드를 잃어버립니다. 원래 맨 앞 노드와 먼저 연결하세요.

```c
item->prev = NULL;
item->next = list->head;          /* 원래 맨 앞 노드 (없으면 NULL) */
if (list->head != NULL)
    list->head->prev = item;
else
    list->tail = item;            /* 빈 목록이었으면 item 이 맨 뒤이기도 합니다 */
list->head = item;
list->size++;
```

</details>

<details>
<summary>힌트 2 — detach 는 앞쪽 한 번, 뒤쪽 한 번</summary>

(c)의 네 가지 경우를 따로 쓰지 않아도 됩니다. **앞쪽**과 **뒤쪽**을 따로 처리하면 네 경우가 모두 됩니다.

- 앞쪽: `item->prev` 가 있으면 그 노드의 `next` 를 `item->next` 로 바꿉니다. 없으면 `item` 이 맨 앞이었으니 `list->head` 를 `item->next` 로 바꿉니다.
- 뒤쪽: `item->next` 가 있으면 그 노드의 `prev` 를 `item->prev` 로 바꿉니다. 없으면 `list->tail` 을 `item->prev` 로 바꿉니다.

마지막으로 `item` 의 두 포인터를 `NULL` 로 두고 `size` 를 줄입니다.

</details>

<details>
<summary>힌트 3 — view 와 remove 는 조립만 하면 됩니다</summary>

```
view(id):
    item = find(id)
    있으면:  detach(item), push_front(item)
    없으면:  push_front(item_create(id))
             size > capacity 이면  tail 을 detach 하고 free

remove(id):
    item = find(id)
    없으면 0
    있으면 detach(item), free(item), 1
```

tail 을 해제할 때는 `detach` 하기 **전에** `list->tail` 을 변수에 저장해 두세요. 떼어 내면 `list->tail` 이 바뀝니다.

</details>

<details>
<summary>힌트 4 — recent_free 에서 다음 노드 먼저 챙기기</summary>

`free(node)` 를 한 다음에는 `node->next` 를 읽으면 안 됩니다. 해제하기 전에 다음 노드를 저장하세요.

```c
Item *next = node->next;
free(node);
node = next;
```

</details>

## 자주 하는 실수

**한쪽 방향 포인터만 고치기**

`next` 만 고치고 `prev` 를 그대로 두면 `head` 에서 출발할 때는 멀쩡해 보입니다.
`tail` 에서 거꾸로 따라가 보면 틀린 게 보입니다. `main.c` 가 두 방향으로 다 출력하는 이유입니다.

**빈 목록에 붙이거나, 마지막 하나를 뗄 때 `tail` 을 잊기**

노드가 0개 ↔ 1개로 바뀔 때는 `head` 와 `tail` 을 **둘 다** 바꿔야 합니다.

**해제한 노드를 읽기**

`free` 한 노드의 `next` 나 `id` 를 읽으면 그때그때 다른 값이 나옵니다. 테스트가 어떤 때는 통과하고 어떤 때는
멈춘다면 이것부터 의심하세요.

**이미 있는 상품을 지우고 새로 만들기**

결과 목록은 같아 보여도 (e)의 조건을 어깁니다. 채점기는 `malloc` 횟수로 확인합니다.

## 더 생각해 볼 것

- 지금 `recent_find` 는 목록을 처음부터 훑어서 `O(n)` 입니다. Week 02 의 해시 테이블을 함께 쓰면
  `recent_view` 전체를 `O(1)` 로 만들 수 있습니다. 이것이 **LRU 캐시**입니다 (LeetCode 146).
- 단일 연결 리스트(Week 01)로 같은 기능을 만들면 `recent_detach` 가 왜 어려워질까요?
