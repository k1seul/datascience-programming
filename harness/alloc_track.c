/* Counters behind alloc_track.h. Compiled into the same library as the solution. */

#include "alloc_track.h"

/* The forced include renamed these; this file needs the real ones. */
#undef malloc
#undef calloc
#undef realloc
#undef free

static int live = 0;
static int total = 0;

static void *count_new(void *ptr)
{
    if (ptr != NULL) {
        live++;
        total++;
    }
    return ptr;
}

void *harness_malloc(size_t size)
{
    return count_new(malloc(size));
}

void *harness_calloc(size_t count, size_t size)
{
    return count_new(calloc(count, size));
}

void *harness_realloc(void *ptr, size_t size)
{
    void *moved = realloc(ptr, size);
    if (ptr == NULL)
        return count_new(moved);
    if (moved == NULL && size == 0)
        live--;
    return moved;
}

void harness_free(void *ptr)
{
    if (ptr != NULL)
        live--;
    free(ptr);
}

int harness_live_allocations(void)
{
    return live;
}

int harness_total_allocations(void)
{
    return total;
}
