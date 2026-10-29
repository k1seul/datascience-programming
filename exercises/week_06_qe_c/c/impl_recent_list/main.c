/* Self-check driver, like the main.c you get in the exam. Not used by the grader.
 *
 *     cc -Wall -Wextra -o main main.c solution.c && ./main
 *
 * Compare each line with the "Expected:" line under it.
 */

#include <stdio.h>

#include "recent.h"

/* Stop walking after this many nodes, in case a link points back into the list. */
#define MAX_WALK 20

/* Head to tail, then tail to head, so a missing prev link shows up too. */
static void show_both_ways(const RecentList *list)
{
    int steps = 0;
    printf("size=%d  head->tail:", list->size);
    for (const Item *node = list->head; node != NULL && steps < MAX_WALK; node = node->next) {
        printf(" %d", node->id);
        steps++;
    }
    steps = 0;
    printf("  tail->head:");
    for (const Item *node = list->tail; node != NULL && steps < MAX_WALK; node = node->prev) {
        printf(" %d", node->id);
        steps++;
    }
    printf("\n");
}

int main(void)
{
    printf("== (a) item_create / recent_create ==\n");
    Item *item = item_create(5);
    RecentList *list = recent_create(3);
    if (item == NULL || list == NULL) {
        printf("item_create or recent_create returned NULL. Start with (a).\n");
        return 1;
    }
    printf("id=%d prev=%s next=%s\n", item->id, item->prev ? "set" : "NULL",
           item->next ? "set" : "NULL");
    printf("Expected: id=5 prev=NULL next=NULL\n");
    printf("capacity=%d size=%d head=%s\n", list->capacity, list->size,
           list->head ? "set" : "NULL");
    printf("Expected: capacity=3 size=0 head=NULL\n\n");

    printf("== (b) recent_push_front ==\n");
    recent_push_front(list, item);
    recent_push_front(list, item_create(2));
    recent_push_front(list, item_create(9));
    show_both_ways(list);
    printf("Expected: size=3  head->tail: 9 2 5  tail->head: 5 2 9\n\n");

    printf("== (c) recent_detach ==\n");
    Item *middle = list->head->next;
    recent_detach(list, middle);
    show_both_ways(list);
    printf("Expected: size=2  head->tail: 9 5  tail->head: 5 9\n");
    recent_push_front(list, middle);
    show_both_ways(list);
    printf("Expected: size=3  head->tail: 2 9 5  tail->head: 5 9 2\n\n");

    printf("== (d) recent_find ==\n");
    Item *found = recent_find(list, 9);
    printf("find(9)=%d find(7)=%s\n", found ? found->id : -1,
           recent_find(list, 7) ? "set" : "NULL");
    printf("Expected: find(9)=9 find(7)=NULL\n\n");

    printf("== (e) recent_view ==\n");
    recent_view(list, 5);
    show_both_ways(list);
    printf("Expected: size=3  head->tail: 5 2 9  tail->head: 9 2 5\n");
    recent_view(list, 4);
    show_both_ways(list);
    printf("Expected: size=3  head->tail: 4 5 2  tail->head: 2 5 4\n\n");

    printf("== (f) recent_remove ==\n");
    int removed = recent_remove(list, 5);
    int missing = recent_remove(list, 5);
    printf("remove(5)=%d remove(5) again=%d\n", removed, missing);
    printf("Expected: remove(5)=1 remove(5) again=0\n");
    show_both_ways(list);
    printf("Expected: size=2  head->tail: 4 2  tail->head: 2 4\n\n");

    printf("== (g) recent_print ==\n");
    recent_print(list);
    printf("Expected: 4 -> 2\n");

    recent_free(list);
    return 0;
}
