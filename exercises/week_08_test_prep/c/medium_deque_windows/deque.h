/* Week 08 / C - the functions to implement.
 *
 * Do not modify this header. Implement everything in solution.c.
 */

#ifndef WEEK08_DEQUE_H
#define WEEK08_DEQUE_H

typedef struct {
    int *buf;       /* capacity slots */
    int capacity;   /* how many values fit */
    int size;       /* how many values are stored now */
    int front;      /* index of the first value */
    int rear;       /* index right after the last value: where push_back writes next */
} Deque;

/* Always true: rear == (front + size) % capacity. */

/* ---- (a) circular deque ---------------------------------------------- */

/* Empty deque with room for capacity values; front and rear start at 0.
 * Returns NULL when capacity < 1. */
Deque *dq_create(int capacity);

/* Frees buf and the deque. Does nothing for NULL. */
void dq_free(Deque *dq);

int dq_is_empty(const Deque *dq);
int dq_is_full(const Deque *dq);

/* Return 1 on success. Return 0 and change nothing when the deque is full. */
int dq_push_front(Deque *dq, int value);
int dq_push_back(Deque *dq, int value);

/* Store the first / last value in *out and return 1 (pop also removes it).
 * Return 0 and leave *out alone when the deque is empty. */
int dq_pop_front(Deque *dq, int *out);
int dq_pop_back(Deque *dq, int *out);
int dq_peek_front(const Deque *dq, int *out);
int dq_peek_back(const Deque *dq, int *out);

/* ---- (b) days until a warmer day -------------------------------------- */

/* answer[i] = how many days after day i the first strictly warmer day comes,
 * or 0 when no later day is warmer. Returns n. Uses a deque of day indices. */
int days_until_warmer(const int *temps, int n, int *answer);

/* ---- (c) first negative in every window ------------------------------- */

/* result[i] = the first negative value among nums[i .. i + k - 1], or 0 when that
 * window has none, for i = 0 .. n - k. Returns n - k + 1, or -1 when k < 1 or k > n.
 * Uses a deque of indices of negative values. */
int first_negative(const int *nums, int n, int k, int *result);

#endif /* WEEK08_DEQUE_H */
