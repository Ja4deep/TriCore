"""Small helpers shared by the Digital Logic Laboratory."""

from __future__ import annotations

from itertools import product

TERNARY_TEXT = frozenset({"0", "1", "2"})


def input_labels(arity: int) -> tuple[str, ...]:
    """Return conventional signal labels for a gate arity."""
    if arity < 1:
        raise ValueError("Arity must be at least 1.")

    return tuple(chr(ord("A") + index) for index in range(arity))


def ternary_combinations(arity: int) -> list[tuple[int, ...]]:
    """Return every ternary input combination for the requested arity."""
    if arity < 1:
        raise ValueError("Arity must be at least 1.")

    return [tuple(values) for values in product((0, 1, 2), repeat=arity)]
