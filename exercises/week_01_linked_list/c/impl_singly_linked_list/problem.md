# Week 01 / C (구현) — 단일 연결 리스트

`list.h` 에 선언된 API 를 `solution.c` 에 전부 구현한다. 배열로 흉내내지 말고
노드를 `malloc` 으로 잡아 `next` 포인터로 잇는다.

## 규약

- 반환값 규약: 성공 `0`, 실패 `-1`. 단 `list_size` 는 개수, `list_index_of` 는 위치(없으면 -1),
  `list_to_array` 는 복사한 개수(용량 부족이면 -1)를 반환한다.
- `list_destroy(NULL)` 은 아무 일도 하지 않아야 한다.
- 인덱스는 0부터 센다. `list_insert` 만 `index == size`(맨 뒤 붙이기)를 허용한다.
- `list_size` 는 매번 세도 되고 필드로 들고 있어도 된다. 다만 모든 연산 후 값이 맞아야 한다.

## 구현할 함수

```c
List *list_create(void);
void  list_destroy(List *list);
int   list_size(const List *list);
int   list_push_front(List *list, int value);
int   list_push_back(List *list, int value);
int   list_insert(List *list, int index, int value);
int   list_remove(List *list, int index, int *out);
int   list_get(const List *list, int index, int *out);
int   list_index_of(const List *list, int value);
void  list_reverse(List *list);
int   list_to_array(const List *list, int *out, int capacity);
```

## 채점

```sh
uv run runner.py test 1 --task singly_linked_list
```

테스트는 `solution.c` 를 공유 라이브러리로 빌드해 ctypes 로 직접 호출한다.
`-Wall -Wextra` 경고는 실패로 치지 않지만, 남았다면 대개 진짜 버그의 신호다.

## 생각해 볼 것

- `list_push_back` 을 매번 끝까지 순회해서 구현하면 n번 넣을 때 비용이 얼마인가? 꼬리 포인터를 들면?
- `list_remove` 에서 이전 노드를 어떻게 잡을 것인가. 더미 헤드를 쓰면 머리 삭제 분기가 사라지는가?
- 메모리 누수를 눈으로 확인하려면: `valgrind --leak-check=full` 로 테스트를 돌려 볼 수 있다.
