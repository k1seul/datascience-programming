/* Week 05 / C - the functions to implement.
 *
 * Do not modify this header. Implement everything in solution.c.
 * values is sorted in ascending order and may contain duplicates. n >= 0.
 */

#ifndef WEEK05_SEARCH_H
#define WEEK05_SEARCH_H

/* Index of some element equal to target, or -1 when there is none.
 * With duplicates any matching index is accepted. */
int binary_search(const int *values, int n, int target);

/* First index whose value is >= target. Returns n when every value is < target. */
int lower_bound(const int *values, int n, int target);

/* First index whose value is > target. Returns n when every value is <= target. */
int upper_bound(const int *values, int n, int target);

/* How many elements equal target. */
int count_equal(const int *values, int n, int target);

#endif /* WEEK05_SEARCH_H */
