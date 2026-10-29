/* Allocation counting for C tasks built with track_alloc=True.
 *
 * native.py force-includes this header ahead of the solution (cc -include), so every
 * malloc / calloc / realloc / free in the solution goes through the counters in
 * alloc_track.c. Tests read harness_live_allocations() before and after a call to see
 * whether the solution freed what it allocated.
 */

#ifndef HARNESS_ALLOC_TRACK_H
#define HARNESS_ALLOC_TRACK_H

/* Pull in the real declarations first so the macros below never rename them. */
#include <stdlib.h>

void *harness_malloc(size_t size);
void *harness_calloc(size_t count, size_t size);
void *harness_realloc(void *ptr, size_t size);
void harness_free(void *ptr);

/* Blocks handed out and not yet freed. */
int harness_live_allocations(void);

/* Blocks handed out so far, freed or not. Tells "moved a node" apart from "freed it
 * and allocated a new one", which can land on the same address. */
int harness_total_allocations(void);

#define malloc(size) harness_malloc(size)
#define calloc(count, size) harness_calloc(count, size)
#define realloc(ptr, size) harness_realloc(ptr, size)
#define free(ptr) harness_free(ptr)

#endif /* HARNESS_ALLOC_TRACK_H */
