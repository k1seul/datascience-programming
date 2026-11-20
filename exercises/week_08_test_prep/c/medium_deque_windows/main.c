/* Self-check driver. Compile it together with your solution and compare each line
 * with the "Expected:" line under it:
 *
 *     cc -Wall -Wextra -o main main.c solution.c && ./main
 *
 * This file is yours: add any checks you like. The grader does not use it.
 */

#include <stdio.h>

#include "deque.h"

static void print_deque(const Deque *dq)
{
    printf("[");
    for (int i = 0; i < dq->size; i++)
        printf(i ? ", %d" : "%d", dq->buf[(dq->front + i) % dq->capacity]);
    printf("]  front=%d rear=%d size=%d\n", dq->front, dq->rear, dq->size);
}

static void print_array(const int *values, int n)
{
    for (int i = 0; i < n; i++)
        printf(i ? " %d" : "%d", values[i]);
    printf("\n");
}

int main(void)
{
    printf("== (a) circular deque ==\n");
    Deque *dq = dq_create(3);
    if (dq == NULL) {
        printf("dq_create returned NULL. Start with (a).\n");
        return 0;
    }
    dq_push_back(dq, 1);
    dq_push_back(dq, 2);
    dq_push_back(dq, 3);
    print_deque(dq);
    printf("Expected: [1, 2, 3]  front=0 rear=0 size=3\n");

    int full = dq_push_back(dq, 4);
    printf("push_back on a full deque returned %d\n", full);
    printf("Expected: push_back on a full deque returned 0\n");

    int v = 0;
    dq_pop_front(dq, &v);
    printf("pop_front -> %d\n", v);
    printf("Expected: pop_front -> 1\n");

    dq_push_back(dq, 4);
    print_deque(dq);
    printf("Expected: [2, 3, 4]  front=1 rear=1 size=3\n");

    dq_pop_back(dq, &v);
    dq_push_front(dq, 9);
    print_deque(dq);
    printf("Expected: [9, 2, 3]  front=0 rear=0 size=3\n");
    dq_free(dq);

    printf("\n== (b) days until a warmer day ==\n");
    int temps[] = {73, 74, 75, 71, 69, 72, 76, 73};
    int answer[8] = {0};
    int written = days_until_warmer(temps, 8, answer);
    printf("returned %d: ", written);
    print_array(answer, 8);
    printf("Expected: returned 8: 1 1 4 2 1 1 0 0\n");

    printf("\n== (c) first negative in every window ==\n");
    int nums[] = {12, -1, -7, 8, -15, 30, 16, 28};
    int result[6] = {0};
    written = first_negative(nums, 8, 3, result);
    printf("returned %d: ", written);
    print_array(result, 6);
    printf("Expected: returned 6: -1 -1 -7 -15 -15 0\n");
    return 0;
}
