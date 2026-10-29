/* Week 06 / C - circular deque and a round-robin scheduler.
 *
 * Do not modify this header. Implement every function in solution.c.
 * Functions that succeed or fail return 1 on success and 0 on failure.
 */

#ifndef WEEK06_DEQUE_H
#define WEEK06_DEQUE_H

/* The elements, front to back, are
 *     buf[front], buf[(front + 1) % capacity], ..., buf[(front + size - 1) % capacity]
 * Elements never move inside buf. Only front and size change. */
typedef struct {
    int *buf;
    int capacity;
    int size;
    int front;
} Deque;

/* (a) ------------------------------------------------------------------- */

/* An empty deque with room for capacity elements and front = 0.
 * Returns NULL when capacity < 1. */
Deque *deque_create(int capacity);

/* Free buf and the deque itself. Must be safe to call with NULL. */
void deque_free(Deque *dq);

/* (b) ------------------------------------------------------------------- */

int deque_is_empty(const Deque *dq);
int deque_is_full(const Deque *dq);

/* Add value at the front / back. Returns 0 when the deque is full. */
int deque_push_front(Deque *dq, int value);
int deque_push_back(Deque *dq, int value);

/* Remove the front / back element and write it to *out.
 * Returns 0 when the deque is empty, leaving *out untouched. */
int deque_pop_front(Deque *dq, int *out);
int deque_pop_back(Deque *dq, int *out);

/* Same as pop, but the element stays in the deque. */
int deque_peek_front(const Deque *dq, int *out);
int deque_peek_back(const Deque *dq, int *out);

/* (c) ------------------------------------------------------------------- */

/* Print the elements front to back as "[3, 1, 4]" followed by a newline.
 * An empty deque prints "[]". */
void deque_print(const Deque *dq);

/* (d) ------------------------------------------------------------------- */

/* Task i needs burst[i] units of time (burst[i] >= 1). Tasks wait in a queue in
 * index order. Repeatedly take the task at the front and run it for
 * min(quantum, time it still needs). A task that is done is written to
 * finish_order; one that is not goes to the back of the queue.
 *
 * finish_order has room for n entries. Returns n, or -1 when quantum < 1. */
int round_robin(const int *burst, int n, int quantum, int *finish_order);

#endif /* WEEK06_DEQUE_H */
