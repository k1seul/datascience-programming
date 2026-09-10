/* Week 01 / C - public API of the singly linked list.
 *
 * Do not modify this header. Define List in solution.c and implement every function
 * below. The convention is 0 on success and a negative value on failure, except for
 * list_size, list_index_of and list_to_array.
 */

#ifndef WEEK01_LIST_H
#define WEEK01_LIST_H

/* Opaque type: only solution.c knows the layout. */
typedef struct List List;

/* Create an empty list. Returns NULL on failure. */
List *list_create(void);

/* Free every node and the list itself. Must be safe to call with NULL. */
void list_destroy(List *list);

/* Number of elements. */
int list_size(const List *list);

/* Prepend / append a value. Returns 0 on success, -1 on failure. */
int list_push_front(List *list, int value);
int list_push_back(List *list, int value);

/* Insert at index. Returns 0 when 0 <= index <= size, -1 otherwise. */
int list_insert(List *list, int index, int value);

/* Remove the element at index and write its value to *out.
 * Returns 0 on success, -1 when the index is out of range.
 * When out is NULL the value is discarded. */
int list_remove(List *list, int index, int *out);

/* Write the value at index to *out. Returns 0 on success, -1 when out of range. */
int list_get(const List *list, int index, int *out);

/* Index of the first occurrence of value, or -1 when absent. */
int list_index_of(const List *list, int value);

/* Reverse the links in place. */
void list_reverse(List *list);

/* Copy the values into out from the front and return how many were copied.
 * When capacity is smaller than size, write nothing and return -1. */
int list_to_array(const List *list, int *out, int capacity);

#endif /* WEEK01_LIST_H */
