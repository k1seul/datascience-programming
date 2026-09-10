/* Week 01 / C — 단일 연결 리스트 공개 API.
 *
 * 이 헤더는 고치지 않는다. solution.c 에서 List 를 정의하고 아래 함수를 전부 구현한다.
 * 성공은 0, 실패는 음수를 반환하는 규약을 따른다 (list_index_of, list_size, list_to_array 예외).
 */

#ifndef WEEK01_LIST_H
#define WEEK01_LIST_H

/* 내부 구조는 solution.c 안에서만 안다 (불투명 타입). */
typedef struct List List;

/* 빈 리스트를 만든다. 실패하면 NULL. */
List *list_create(void);

/* 모든 노드와 리스트 자체를 해제한다. NULL 을 넘겨도 안전해야 한다. */
void list_destroy(List *list);

/* 원소 개수. */
int list_size(const List *list);

/* 맨 앞 / 맨 뒤에 추가. 성공 0, 실패 -1. */
int list_push_front(List *list, int value);
int list_push_back(List *list, int value);

/* index 위치에 삽입한다. 0 <= index <= size 이면 성공 0, 아니면 -1. */
int list_insert(List *list, int index, int value);

/* index 의 원소를 제거하고 그 값을 *out 에 쓴다. 성공 0, 범위 밖이면 -1.
 * out 이 NULL 이면 값은 버린다. */
int list_remove(List *list, int index, int *out);

/* index 의 값을 *out 에 쓴다. 성공 0, 범위 밖이면 -1. */
int list_get(const List *list, int index, int *out);

/* value 가 처음 나오는 위치. 없으면 -1. */
int list_index_of(const List *list, int value);

/* 링크를 제자리에서 뒤집는다. */
void list_reverse(List *list);

/* 앞에서부터 out 에 복사하고 복사한 개수를 반환한다.
 * capacity 가 size 보다 작으면 아무것도 쓰지 않고 -1. */
int list_to_array(const List *list, int *out, int capacity);

#endif /* WEEK01_LIST_H */
