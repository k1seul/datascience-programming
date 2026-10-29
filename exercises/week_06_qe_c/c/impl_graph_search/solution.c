/* Problem statement: problem.md / function contract: graph.h */

#include <stdio.h>
#include <stdlib.h>

#include "graph.h"

/* Delete this define and every `NOT_IMPLEMENTED` below once you start writing.
 * The grader reads them as "not written yet"; anything else counts as a real answer.
 * graph_create returning NULL carries the same meaning. */
#define NOT_IMPLEMENTED (-1000)

/* (a) */

Graph *graph_create(int n)
{
    return NULL;
}

int graph_add_edge(Graph *g, int from, int to)
{
    return NOT_IMPLEMENTED;
}

void graph_free(Graph *g)
{
}

/* (b) */

void graph_print(const Graph *g)
{
    printf("NOT_IMPLEMENTED\n");
}

/* (c) */

int graph_bfs_distance(const Graph *g, int start, int *dist)
{
    return NOT_IMPLEMENTED;
}

/* (d) */

int graph_dfs_order(const Graph *g, int start, int *order)
{
    return NOT_IMPLEMENTED;
}

/* (e) */

int graph_has_cycle(const Graph *g)
{
    return NOT_IMPLEMENTED;
}
