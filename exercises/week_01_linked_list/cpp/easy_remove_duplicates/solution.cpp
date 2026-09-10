// Problem statement: problem.md

// Delete this define together with the `return NOT_IMPLEMENTED;` below once you start.
// The grader reads it as "not written yet"; anything else counts as a real answer.
#define NOT_IMPLEMENTED (-1000)

struct Node {  // given node type
    int value;
    Node *next;
};

// Build a list from the sorted values, drop the duplicates and write the result to out.
// Returns the number of items written, or -1 when out_capacity is too small.
extern "C" int dedup_sorted(const int *values, int n, int *out, int out_capacity)
{
    return NOT_IMPLEMENTED;
}
