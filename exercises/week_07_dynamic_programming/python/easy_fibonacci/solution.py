"""Problem statement: problem.md"""

from __future__ import annotations


def fib_memo(n: int) -> int:
    """The n-th Fibonacci number, by recursion that remembers what it has computed."""
    raise NotImplementedError


def fib_table(n: int) -> int:
    """The n-th Fibonacci number, by filling a list from the front. No recursion."""
    raise NotImplementedError


def naive_calls(n: int) -> int:
    """How many times the memo-less recursive fib is called to compute fib(n)."""
    raise NotImplementedError
