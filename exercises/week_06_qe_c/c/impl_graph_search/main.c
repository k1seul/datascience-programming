/* Self-check driver, like the main.c you get in the exam. Not used by the grader.
 *
 *     cc -Wall -Wextra -o main main.c solution.c && ./main
 *
 * Compare each line with the "Expected:" line under it.
 */

#include <stdio.h>

#include "graph.h"

static void print_ints(const char *label, const int *values, int n)
{
    printf("%s", label);
    for (int i = 0; i < n; i++)
        printf(i == 0 ? "%d" : " %d", values[i]);
    printf("\n");
}

int main(void)
{
    /*   0 -> 1 -> 3 -> 4
     *   0 -> 2 -> 3          5 has no edges */
    printf("== (a) graph_create / graph_add_edge ==\n");
    Graph *g = graph_create(6);
    if (g == NULL) {
        printf("graph_create(6) returned NULL. Start with (a).\n");
        return 1;
    }
    graph_add_edge(g, 0, 1);
    graph_add_edge(g, 0, 2);
    graph_add_edge(g, 1, 3);
    graph_add_edge(g, 2, 3);
    graph_add_edge(g, 3, 4);
    int bad = graph_add_edge(g, 0, 6);
    printf("n=%d add_edge(0, 6)=%d\n", g->n, bad);
    printf("Expected: n=6 add_edge(0, 6)=0\n\n");

    printf("== (b) graph_print ==\n");
    graph_print(g);
    printf("Expected:\n0: 1 2\n1: 3\n2: 3\n3: 4\n4:\n5:\n\n");

    printf("== (c) graph_bfs_distance ==\n");
    int dist[6] = {0};
    int reached = graph_bfs_distance(g, 0, dist);
    printf("reached=%d ", reached);
    print_ints("dist=", dist, 6);
    printf("Expected: reached=5 dist=0 1 1 2 3 -1\n\n");

    printf("== (d) graph_dfs_order ==\n");
    int order[6] = {0};
    int visited = graph_dfs_order(g, 0, order);
    printf("visited=%d ", visited);
    print_ints("order=", order, visited > 0 && visited <= 6 ? visited : 0);
    printf("Expected: visited=5 order=0 1 3 4 2\n\n");

    printf("== (e) graph_has_cycle ==\n");
    int before = graph_has_cycle(g);
    graph_add_edge(g, 4, 1);
    int after = graph_has_cycle(g);
    printf("before=%d after adding 4->1=%d\n", before, after);
    printf("Expected: before=0 after adding 4->1=1\n");

    graph_free(g);
    return 0;
}
