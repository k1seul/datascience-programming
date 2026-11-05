// Problem statement: problem.md
//
// The grader calls these through ctypes, so the symbols must be extern "C".
// Inside, use std::string and std::vector as much as you like.

#include <string>
#include <vector>

// Delete this define together with every `return NOT_IMPLEMENTED;` below once you start.
// The grader reads it as "not written yet"; anything else counts as a real answer.
#define NOT_IMPLEMENTED (-1000)

// Fewest single-letter insertions, deletions and replacements that turn a into b.
extern "C" int edit_distance(const char *a, const char *b)
{
    return NOT_IMPLEMENTED;
}

// Index of the word in dict with the smallest edit distance to word. On a tie the
// smaller index wins. Returns -1 when n < 1.
extern "C" int closest_word(const char *word, const char *const *dict, int n)
{
    return NOT_IMPLEMENTED;
}
