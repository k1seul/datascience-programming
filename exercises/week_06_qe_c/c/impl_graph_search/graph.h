/* Week 06 / C - directed graph on adjacency lists, BFS, DFS and cycle detection.
 *
 * Do not modify this header. Implement every function in solution.c.
 * Vertices are numbered 0 .. n-1.
 */

#ifndef WEEK06_GRAPH_H
#define WEEK06_GRAPH_H

/* One out-edge in a vertex's adjacency list. */
typedef struct Edge {
    int to;
    struct Edge *next;
} Edge;

typedef struct {
    int n;
    Edge **adj; /* adj[v]: first out-edge of v, NULL when v has none */
} Graph;

/* (a) ------------------------------------------------------------------- */

/* A graph with n vertices and no edges: adj has n entries, all NULL.
 * Returns NULL when n < 1. */
Graph *graph_create(int n);

/* Add the edge from -> to at the END of adj[from], so each list keeps the order the
 * edges were added in. Adding the same edge twice adds it twice. Self-loops are fine.
 * Returns 1, or 0 when from or to is not a vertex (the graph stays unchanged). */
int graph_add_edge(Graph *g, int from, int to);

/* Free every edge, adj and the graph. Must be safe to call with NULL. */
void graph_free(Graph *g);

/* (b) ------------------------------------------------------------------- */

/* One line per vertex, 0 first: "v:" followed by " w" for each out-edge in list order.
 *     0: 1 2
 *     1:
 *     2: 0 */
void graph_print(const Graph *g);

/* (c) ------------------------------------------------------------------- */

/* dist has room for n entries. Set dist[v] to the fewest edges on a path from start
 * to v, or -1 when v cannot be reached. Returns how many vertices are reachable,
 * start included. Returns -1 when start is not a vertex, leaving dist untouched. */
int graph_bfs_distance(const Graph *g, int start, int *dist);

/* (d) ------------------------------------------------------------------- */

/* Depth-first search from start: visit a vertex, then go into each of its unvisited
 * out-neighbours in list order, finishing one before trying the next. order has room
 * for n entries; write the vertices in the order they are first visited.
 * Returns how many were visited, or -1 when start is not a vertex. */
int graph_dfs_order(const Graph *g, int start, int *order);

/* (e) ------------------------------------------------------------------- */

/* 1 when the graph has a directed cycle anywhere (a self-loop counts), 0 otherwise. */
int graph_has_cycle(const Graph *g);

#endif /* WEEK06_GRAPH_H */
