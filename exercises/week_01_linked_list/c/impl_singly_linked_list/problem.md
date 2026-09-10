# Week 01 / C (구현) — 단일 연결 리스트

`list.h` 에 선언된 함수들을 `solution.c` 에 모두 구현합니다.
배열로 흉내 내지 마시고, 노드를 `malloc` 으로 하나씩 잡아서 `next` 포인터로 이어 주세요.

## 규약

- 반환값은 성공이면 `0`, 실패면 `-1` 입니다.
  다만 `list_size` 는 원소 개수를, `list_index_of` 는 위치(없으면 `-1`)를,
  `list_to_array` 는 복사한 개수(용량이 부족하면 `-1`)를 반환합니다.
- `list_destroy(NULL)` 은 아무 일도 하지 않고 그냥 넘어가야 합니다.
- 스텁의 `NOT_IMPLEMENTED` 와 `list_create` 의 `return NULL` 은 "아직 풀지 않음" 표시입니다.
  구현을 시작하면 자연스럽게 사라집니다.
- 인덱스는 0부터 셉니다. `list_insert` 만 `index == size` (맨 뒤에 붙이기)를 허용합니다.
- `list_size` 는 매번 세어도 되고 필드로 들고 있어도 됩니다.
  어느 쪽이든 모든 연산이 끝난 뒤에 값이 맞기만 하면 됩니다.

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

각 함수가 정확히 무엇을 해야 하는지는 `list.h` 의 주석에 적어 두었습니다.

## 채점

```sh
uv run runner.py test 1 --task singly_linked_list
```

테스트가 `solution.c` 를 공유 라이브러리로 빌드한 다음 ctypes 로 직접 호출합니다.
`-Wall -Wextra` 경고는 실패로 치지 않지만, 경고가 남아 있다면 대개 진짜 버그의 신호이니
한 번 확인해 보시는 편이 좋습니다.

## 생각해 볼 것

- `list_push_back` 을 매번 끝까지 순회해서 구현하면 원소를 n번 넣을 때 비용이 얼마나 될까요?
  꼬리 포인터를 따로 들고 있으면 어떻게 달라질까요?
- `list_remove` 에서 지울 노드의 이전 노드를 어떻게 잡으면 좋을까요?
  더미 헤드를 쓰면 머리를 지우는 경우를 따로 처리하지 않아도 되는지 확인해 보세요.
- 메모리 누수가 걱정된다면 `valgrind --leak-check=full` 로 테스트를 돌려 볼 수 있습니다.
