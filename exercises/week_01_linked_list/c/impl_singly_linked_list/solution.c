/* Problem statement: problem.md / function contract: list.h */

#include <stdlib.h>

#include "list.h"

/* Delete this define and every `NOT_IMPLEMENTED` below once you start writing.
 * The grader reads them as "not written yet"; anything else counts as a real answer.
 * list_create returning NULL carries the same meaning. */
#define NOT_IMPLEMENTED (-1000)

typedef struct Node {
    int value;
    struct Node *next;
} Node;

struct List {
    Node *head;
    /* Feel free to add fields such as tail or size. */
};

List *list_create(void)
{
    return NULL;
}

void list_destroy(List *list)
{
}

int list_size(const List *list)
{
    return NOT_IMPLEMENTED;
}

int list_push_front(List *list, int value)
{
    return NOT_IMPLEMENTED;
}

int list_push_back(List *list, int value)
{
    return NOT_IMPLEMENTED;
}

int list_insert(List *list, int index, int value)
{
    return NOT_IMPLEMENTED;
}

int list_remove(List *list, int index, int *out)
{
    return NOT_IMPLEMENTED;
}

int list_get(const List *list, int index, int *out)
{
    return NOT_IMPLEMENTED;
}

int list_index_of(const List *list, int value)
{
    return NOT_IMPLEMENTED;
}

void list_reverse(List *list)
{
}

int list_to_array(const List *list, int *out, int capacity)
{
    return NOT_IMPLEMENTED;
}
