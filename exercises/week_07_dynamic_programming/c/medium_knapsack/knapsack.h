/* Week 07 / C - the functions to implement.
 *
 * Do not modify this header. Implement everything in solution.c.
 * Item i costs cost[i] (>= 1) and is worth value[i] (>= 0). An item is either taken
 * whole or left out, and can be taken at most once.
 */

#ifndef WEEK07_KNAPSACK_H
#define WEEK07_KNAPSACK_H

/* Largest total value of items whose total cost is at most budget.
 * Returns -1 when n < 0 or budget < 0. */
int knapsack_best(const int *cost, const int *value, int n, int budget);

/* Solves the same problem and writes the indices of the items to take into chosen,
 * in ascending order. chosen has room for n ints. Returns how many indices were
 * written. Any optimal choice is accepted. Returns -1 when n < 0 or budget < 0. */
int knapsack_choose(const int *cost, const int *value, int n, int budget, int *chosen);

#endif /* WEEK07_KNAPSACK_H */
