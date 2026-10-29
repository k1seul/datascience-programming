/* Problem statement: problem.md / function contract: deque.h */

#include <stdio.h>
#include <stdlib.h>

#include "deque.h"

/* Delete this define and every `NOT_IMPLEMENTED` below once you start writing.
 * The grader reads them as "not written yet"; anything else counts as a real answer.
 * deque_create returning NULL carries the same meaning. */
#define NOT_IMPLEMENTED (-1000)

/* (a) */

Deque *deque_create(int capacity)
{
    return NULL;
}

void deque_free(Deque *dq)
{
}

/* (b) */

int deque_is_empty(const Deque *dq)
{
    return NOT_IMPLEMENTED;
}

int deque_is_full(const Deque *dq)
{
    return NOT_IMPLEMENTED;
}

int deque_push_front(Deque *dq, int value)
{
    return NOT_IMPLEMENTED;
}

int deque_push_back(Deque *dq, int value)
{
    return NOT_IMPLEMENTED;
}

int deque_pop_front(Deque *dq, int *out)
{
    return NOT_IMPLEMENTED;
}

int deque_pop_back(Deque *dq, int *out)
{
    return NOT_IMPLEMENTED;
}

int deque_peek_front(const Deque *dq, int *out)
{
    return NOT_IMPLEMENTED;
}

int deque_peek_back(const Deque *dq, int *out)
{
    return NOT_IMPLEMENTED;
}

/* (c) */

void deque_print(const Deque *dq)
{
    printf("NOT_IMPLEMENTED\n");
}

/* (d) */

int round_robin(const int *burst, int n, int quantum, int *finish_order)
{
    return NOT_IMPLEMENTED;
}
