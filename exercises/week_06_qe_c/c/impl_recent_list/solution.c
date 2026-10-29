/* Problem statement: problem.md / function contract: recent.h */

#include <stdio.h>
#include <stdlib.h>

#include "recent.h"

/* Delete this define and every `NOT_IMPLEMENTED` below once you start writing.
 * The grader reads them as "not written yet"; anything else counts as a real answer.
 * item_create and recent_create returning NULL carry the same meaning. */
#define NOT_IMPLEMENTED (-1000)

/* (a) */

Item *item_create(int id)
{
    return NULL;
}

RecentList *recent_create(int capacity)
{
    return NULL;
}

void recent_free(RecentList *list)
{
}

/* (b) */

void recent_push_front(RecentList *list, Item *item)
{
}

/* (c) */

void recent_detach(RecentList *list, Item *item)
{
}

/* (d) */

Item *recent_find(const RecentList *list, int id)
{
    return NULL;
}

/* (e) */

void recent_view(RecentList *list, int id)
{
}

/* (f) */

int recent_remove(RecentList *list, int id)
{
    return NOT_IMPLEMENTED;
}

/* (g) */

void recent_print(const RecentList *list)
{
    printf("NOT_IMPLEMENTED\n");
}
