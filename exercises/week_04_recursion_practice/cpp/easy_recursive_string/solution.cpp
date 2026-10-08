// Problem statement: problem.md
//
// The grader calls these through ctypes, so the symbols must be extern "C".
// All three must be written recursively: no for, no while.

#include <cctype>

// Delete this define and every `NOT_IMPLEMENTED` below once you start writing.
// The grader reads them as "not written yet"; anything else counts as a real answer.
#define NOT_IMPLEMENTED (-1000)

// s reversed into out. Returns the characters written, or -1 when out is too small.
extern "C" int reverse_string(const char *s, char *out, int out_capacity)
{
    return NOT_IMPLEMENTED;
}

// How many vowels (a e i o u, either case) s contains.
extern "C" int count_vowels(const char *s)
{
    return NOT_IMPLEMENTED;
}

// 1 when a is a subsequence of b, 0 otherwise.
extern "C" int is_subsequence(const char *a, const char *b)
{
    return NOT_IMPLEMENTED;
}
