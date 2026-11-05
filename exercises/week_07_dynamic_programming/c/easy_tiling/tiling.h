/* Week 07 / C - the functions to implement.
 *
 * Do not modify this header. Implement everything in solution.c.
 * The board is 2 rows high and n columns wide.
 */

#ifndef WEEK07_TILING_H
#define WEEK07_TILING_H

/* Ways to cover the board with 1 x 2 tiles, laid either way.
 * n is 0..90; returns -1 outside that range. tiling(0) is 1 (the empty board). */
long long tiling(int n);

/* Same board, but 2 x 2 tiles may be used as well.
 * n is 0..60; returns -1 outside that range. */
long long tiling_with_square(int n);

#endif /* WEEK07_TILING_H */
