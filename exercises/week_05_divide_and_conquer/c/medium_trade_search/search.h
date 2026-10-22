/* Week 05 / C - the functions to implement.
 *
 * Do not modify this header. Implement everything in solution.c.
 * ts is a trade log sorted in ascending order of timestamp; duplicates are allowed
 * because several trades can share the same timestamp. n >= 0.
 */

#ifndef WEEK05_SEARCH_H
#define WEEK05_SEARCH_H

/* Index of some trade whose timestamp is exactly t, or -1 when there is none.
 * With duplicates any matching index is accepted. */
int find_trade(const int *ts, int n, int t);

/* First index whose timestamp is >= t. Returns n when every timestamp is < t. */
int first_at_or_after(const int *ts, int n, int t);

/* First index whose timestamp is > t. Returns n when every timestamp is <= t. */
int first_after(const int *ts, int n, int t);

/* How many trades fall in the closed range [lo, hi]. Returns 0 when lo > hi. */
int count_in_range(const int *ts, int n, int lo, int hi);

#endif /* WEEK05_SEARCH_H */
