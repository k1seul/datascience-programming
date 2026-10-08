/* Week 04 / C - the node type and the functions to implement.
 *
 * Do not modify this header. Implement every function in solution.c, and write
 * all four recursively: no for, no while. The grader builds the lists and owns
 * their memory, so never call free().
 */

#ifndef WEEK04_LIST_H
#define WEEK04_LIST_H

typedef struct Node {
    int value;
    struct Node *next;
} Node;

/* Sum of every value. An empty list sums to 0. */
int sum_values(const Node *head);

/* Writes the largest value to *out. Returns 0 on success, -1 for an empty list. */
int max_value(const Node *head, int *out);

/* Writes the values in reverse order into out as text: each value followed by a
 * single space, no trailing newline, NUL-terminated.
 *     1 -> 2 -> 3   becomes   "3 2 1 "
 * Returns the number of characters written (not counting the NUL),
 * or -1 when out_capacity is too small. The list itself must not change. */
int to_string_reverse(const Node *head, char *out, int out_capacity);

/* Removes every node whose value equals x and returns the new head.
 * Do not free anything; just relink. */
Node *drop_value(Node *head, int x);

#endif /* WEEK04_LIST_H */
