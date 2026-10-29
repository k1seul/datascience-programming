/* Self-check driver, like the main.c you get in the exam. Not used by the grader.
 *
 *     cc -Wall -Wextra -o main main.c solution.c && ./main
 *
 * Compare each line with the "Expected:" line under it.
 */

#include <stdio.h>

#include "deque.h"

static void print_take(const char *label, int ok, int value)
{
    if (ok == 1)
        printf("%s -> %d\n", label, value);
    else
        printf("%s -> fail (%d)\n", label, ok);
}

int main(void)
{
    printf("== (a) deque_create ==\n");
    Deque *dq = deque_create(4);
    if (dq == NULL) {
        printf("deque_create(4) returned NULL. Start with (a).\n");
        return 1;
    }
    printf("capacity=%d size=%d front=%d\n", dq->capacity, dq->size, dq->front);
    printf("Expected: capacity=4 size=0 front=0\n\n");

    printf("== (b) push / pop / peek ==\n");
    deque_push_back(dq, 1);
    deque_push_back(dq, 2);
    deque_push_front(dq, 0);
    printf("front=%d buf[3]=%d buf[0]=%d buf[1]=%d\n", dq->front, dq->buf[3], dq->buf[0],
           dq->buf[1]);
    printf("Expected: front=3 buf[3]=0 buf[0]=1 buf[1]=2\n");

    int value = 0;
    int ok = deque_peek_front(dq, &value);
    print_take("peek_front", ok, value);
    printf("Expected: peek_front -> 0\n");
    ok = deque_peek_back(dq, &value);
    print_take("peek_back", ok, value);
    printf("Expected: peek_back -> 2\n");

    deque_push_back(dq, 3);
    int full = deque_is_full(dq);
    int pushed = deque_push_back(dq, 4);
    printf("is_full=%d push_back(4)=%d\n", full, pushed);
    printf("Expected: is_full=1 push_back(4)=0\n");

    ok = deque_pop_front(dq, &value);
    print_take("pop_front", ok, value);
    printf("Expected: pop_front -> 0\n");
    ok = deque_pop_back(dq, &value);
    print_take("pop_back", ok, value);
    printf("Expected: pop_back -> 3\n\n");

    printf("== (c) deque_print ==\n");
    deque_print(dq);
    printf("Expected: [1, 2]\n\n");
    deque_free(dq);

    printf("== (d) round_robin ==\n");
    int burst[] = {5, 2, 4};
    int order[3] = {0};
    int written = round_robin(burst, 3, 2, order);
    printf("written=%d order=", written);
    for (int i = 0; i < written && i < 3; i++)
        printf(i == 0 ? "%d" : " %d", order[i]);
    printf("\nExpected: written=3 order=1 2 0\n");
    return 0;
}
