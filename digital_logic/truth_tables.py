"""Truth table generation for supported ternary logic gates."""

from __future__ import annotations

from .logic_gates import evaluate_gate, get_gate
from .utils import ternary_combinations, input_labels

TruthTableRow = tuple[int, ...]


def generate_truth_table(gate_name: str) -> tuple[list[str], list[TruthTableRow]]:
    """Generate a complete truth table for a supported gate.

    Args:
        gate_name: Gate name such as MIN, MAX, SUM, NMIN, NMAX, or NOT.

    Returns:
        A pair of headers and rows. The final column is always Output.
    """
    gate = get_gate(gate_name)

    labels = list(input_labels(gate.arity))
    headers = [*labels, "Output"]

    rows = [
        (*inputs, evaluate_gate(gate.name, inputs))
        for inputs in ternary_combinations(gate.arity)
    ]

    return headers, rows


def explain_truth_table(gate_name: str) -> list[str]:
    """Return educational notes for a generated truth table."""
    gate = get_gate(gate_name)
    combinations = 3**gate.arity

    return [
        f"A truth table lists every possible input pattern for {gate.name}.",
        f"{gate.name} has {gate.arity} input value(s), so it has {combinations} row(s).",
        f"Ternary rule used: {gate.logic_rule}",
        (
            "Ternary computing systems are built by combining many "
            "of these three-level logic operations."
        ),
    ]
