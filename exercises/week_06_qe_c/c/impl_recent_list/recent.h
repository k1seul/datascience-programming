/* Week 06 / C - "recently viewed" list on a doubly linked list.
 *
 * Do not modify this header. Implement every function in solution.c.
 */

#ifndef WEEK06_RECENT_H
#define WEEK06_RECENT_H

typedef struct Item {
    int id;
    struct Item *prev; /* toward head: viewed more recently */
    struct Item *next; /* toward tail: viewed less recently */
} Item;

typedef struct {
    int capacity;
    int size;
    Item *head; /* most recently viewed, NULL when empty */
    Item *tail; /* least recently viewed, NULL when empty */
} RecentList;

/* (a) ------------------------------------------------------------------- */

/* A new item with prev and next set to NULL. Returns NULL on allocation failure. */
Item *item_create(int id);

/* An empty list. Returns NULL when capacity < 1. */
RecentList *recent_create(int capacity);

/* Free every item still in the list, then the list. Must be safe to call with NULL. */
void recent_free(RecentList *list);

/* (b) ------------------------------------------------------------------- */

/* Link item in as the new head and add 1 to size. item is not in any list.
 * Does not look at capacity. */
void recent_push_front(RecentList *list, Item *item);

/* (c) ------------------------------------------------------------------- */

/* Unlink item, which is in list, and subtract 1 from size.
 * Sets item->prev and item->next to NULL. Does not free item. */
void recent_detach(RecentList *list, Item *item);

/* (d) ------------------------------------------------------------------- */

/* The item with this id, or NULL when there is none. */
Item *recent_find(const RecentList *list, int id);

/* (e) ------------------------------------------------------------------- */

/* Record a view of id.
 * Already in the list: move that same item to the head (no new allocation).
 * Not in the list: create an item for it at the head. When that makes size exceed
 * capacity, remove the tail item and free it. */
void recent_view(RecentList *list, int id);

/* (f) ------------------------------------------------------------------- */

/* Remove the item with this id and free it. Returns 1 when removed, 0 when absent. */
int recent_remove(RecentList *list, int id);

/* (g) ------------------------------------------------------------------- */

/* Print the ids head to tail as "5 -> 2 -> 9" followed by a newline.
 * An empty list prints "(empty)". */
void recent_print(const RecentList *list);

#endif /* WEEK06_RECENT_H */
