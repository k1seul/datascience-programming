// Problem statement: problem.md

// Delete this define together with the `return NOT_IMPLEMENTED;` below once you start.
// The grader reads it as "not written yet"; anything else counts as a real answer.
#define NOT_IMPLEMENTED (-1000)

struct Node {  // given node type
    int value;
    Node *next;
};

// Build a list from values, reverse every group of k nodes and write the result to out.
// Returns the number of items written (n), or -1 when k < 1 or out_capacity is too small.
extern "C" int reverse_groups(const int *values, int n, int k, int *out, int out_capacity)
{
    return NOT_IMPLEMENTED;
}
