/* 문제 설명: problem.md / 함수 규약: list.h */

#include <stdlib.h>

#include "list.h"

typedef struct Node {
    int value;
    struct Node *next;
} Node;

struct List {
    Node *head;
    /* TODO: tail, size 같은 필드를 더해도 된다 */
};

List *list_create(void)
{
    return NULL; /* TODO */
}

void list_destroy(List *list)
{
    /* TODO */
}

int list_size(const List *list)
{
    return -1; /* TODO */
}

int list_push_front(List *list, int value)
{
    return -1; /* TODO */
}

int list_push_back(List *list, int value)
{
    return -1; /* TODO */
}

int list_insert(List *list, int index, int value)
{
    return -1; /* TODO */
}

int list_remove(List *list, int index, int *out)
{
    return -1; /* TODO */
}

int list_get(const List *list, int index, int *out)
{
    return -1; /* TODO */
}

int list_index_of(const List *list, int value)
{
    return -1; /* TODO */
}

void list_reverse(List *list)
{
    /* TODO */
}

int list_to_array(const List *list, int *out, int capacity)
{
    return -1; /* TODO */
}
