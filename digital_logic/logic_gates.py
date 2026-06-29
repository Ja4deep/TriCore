"""Definitions, evaluation functions, and educational metadata for ternary logic gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from config import TERNARY_SIGNAL_VALUES
from exceptions import InvalidGateError

TernaryGateFunction = Callable[[tuple[int, ...]], int]


@dataclass(frozen=True, slots=True)
class LogicGate:
    """Describe one digital logic gate and its educational metadata."""

    name: str
    arity: int
    definition: str
    symbol: str
    diagram: tuple[str, ...]
    logic_rule: str
    explanation: str
    applications: tuple[str, ...]
    evaluator: TernaryGateFunction


def _not(inputs: tuple[int, ...]) -> int:
    """Ternary Inversion (NOT): 2 - x. (0->2, 1->1, 2->0)"""
    return 2 - inputs[0]


def _min(inputs: tuple[int, ...]) -> int:
    """Ternary MIN (AND): Returns the minimum of the inputs."""
    return min(inputs)


def _max(inputs: tuple[int, ...]) -> int:
    """Ternary MAX (OR): Returns the maximum of the inputs."""
    return max(inputs)


def _sum_mod3(inputs: tuple[int, ...]) -> int:
    """Ternary SUM (XOR equivalent): (A + B) mod 3."""
    return sum(inputs) % 3


def _nmin(inputs: tuple[int, ...]) -> int:
    """Return the complement of the minimum input value."""
    return 2 - min(inputs)


def _nmax(inputs: tuple[int, ...]) -> int:
    """Return the complement of the maximum input value."""
    return 2 - max(inputs)


GATES: dict[str, LogicGate] = {
    "NOT": LogicGate(
        name="NOT",
        arity=1,
        definition="Returns the ternary complement of the input (2 − x).",
        symbol="Y = NOT A",
        diagram=("A ---[NOT]--- Output",),
        logic_rule="Inversion: 0->2, 1->1, 2->0.",
        explanation=(
            "Ternary NOT produces the complement of the input value. "
            "It is the basic building block for negative logic."
        ),
        applications=(
            "Signal inversion",
            "Balanced ternary conversion",
            "Complement arithmetic",
        ),
        evaluator=_not,
    ),
    "MIN": LogicGate(
        name="MIN",
        arity=2,
        definition="Returns the smallest of the input signal values.",
        symbol="Y = A MIN B",
        diagram=("A ---\\", "      [MIN]--- Output", "B ---/"),
        logic_rule="Output = min(A, B)",
        explanation=(
            "This gate serves a role similar to the binary AND gate while operating on ternary signals."
        ),
        applications=(
            "Logical intersection",
            "Signal limiting",
            "Conditional logic",
        ),
        evaluator=_min,
    ),
    "MAX": LogicGate(
        name="MAX",
        arity=2,
        definition="Returns the largest input signal value.",
        symbol="Y = A MAX B",
        diagram=("A ---\\", "      [MAX ]--- Output", "B ---/"),
        logic_rule="Output = max(A, B)",
        explanation=(
            "This gate performs a role similar to the binary OR gate while operating on ternary signals."
        ),
        applications=(
            "Signal aggregation",
            "Logical union",
            "Priority selection",
        ),
        evaluator=_max,
    ),
    "SUM": LogicGate(
        name="SUM",
        arity=2,
        definition="A SUM gate returns (A + B) mod 3.",
        symbol="Y = A SUM B",
        diagram=("A ---\\", "      [SUM ]--- Output", "B ---/"),
        logic_rule="Output = (A + B) mod 3",
        explanation=(
            "SUM performs modulo-3 addition. "
            "It plays a role similar to XOR in binary systems but follows ternary arithmetic."
        ),
        applications=(
            "Ternary adders",
            "Parity calculation",
            "Cyclic shifts",
        ),
        evaluator=_sum_mod3,
    ),
    "NMIN": LogicGate(
        name="NMIN",
        arity=2,
        definition="An NMIN gate returns NOT (A MIN B).",
        symbol="Y = A NMIN B",
        diagram=("A ---\\", "      [NMIN]--- Output", "B ---/"),
        logic_rule="Output = 2 - min(A, B)",
        explanation=(
            "NMIN returns the complement of the MIN operation. "
            "It serves a role similar to NAND in binary logic."
        ),
        applications=(
            "Universal ternary logic",
            "Signal inversion with gating",
        ),
        evaluator=_nmin,
    ),
    "NMAX": LogicGate(
        name="NMAX",
        arity=2,
        definition="An NMAX gate returns NOT (A MAX B).",
        symbol="Y = A NMAX B",
        diagram=("A ---\\", "      [NMAX]--- Output", "B ---/"),
        logic_rule="Output = 2 - max(A, B)",
        explanation=(
            "NMAX returns the complement of the maximum input value and serves a role similar to NOR in ternary logic."
            " It suppresses the output when any input is HIGH."
        ),
        applications=(
            "Universal ternary logic",
            "Signal suppression",
        ),
        evaluator=_nmax,
    ),
}


def list_gate_names() -> list[str]:
    """Return supported gate names in display order."""
    return list(GATES)


def get_gate(gate_name: str) -> LogicGate:
    """Return a gate definition by normalized name.

    Args:
        gate_name: Gate name such as MIN, MAX, SUM, NMIN, NMAX, or NOT.

    Raises:
        InvalidGateError: If the gate is not supported.
    """
    normalized_name = gate_name.strip().upper()
    try:
        return GATES[normalized_name]
    except KeyError as error:
        supported = ", ".join(list_gate_names())
        raise InvalidGateError(
            f"Unsupported logic gate. Choose one of: {supported}."
        ) from error


def evaluate_gate(gate_name: str, inputs: tuple[int, ...]) -> int:
    """Evaluate a supported gate for validated ternary inputs."""
    gate = get_gate(gate_name)
    if len(inputs) != gate.arity:
        raise InvalidGateError(f"{gate.name} expects {gate.arity} input value(s).")
    if any(value not in TERNARY_SIGNAL_VALUES for value in inputs):
        raise InvalidGateError("Logic gate inputs must be ternary values: 0, 1, or 2.")

    return gate.evaluator(inputs)


def signal_level(value: int) -> str:
    """Return a readable label for a ternary value."""
    if value == 0:
        return "LOW (0)"
    if value == 1:
        return "MID (1)"
    if value == 2:
        return "HIGH (2)"

    raise InvalidGateError("Signal level must be 0, 1, or 2.")


def explain_gate_result(gate_name: str, inputs: tuple[int, ...], output: int) -> str:
    """Return an educational explanation for one gate simulation."""
    gate = get_gate(gate_name)
    labels = ["A", "B", "C"]
    assignments = ", ".join(
        f"{labels[index]} = {signal_level(value)}" for index, value in enumerate(inputs)
    )

    if gate.name == "NOT":
        reason = f"Since A is {signal_level(inputs[0])}, NOT A (2 - A) becomes {signal_level(output)}."
    elif gate.name == "MIN":
        reason = (
            "MIN returns the lowest input value. "
            f"With {assignments}, the minimum is {signal_level(output)}."
        )
    elif gate.name == "MAX":
        reason = (
            "MAX returns the highest input value. "
            f"With {assignments}, the maximum is {signal_level(output)}."
        )
    elif gate.name == "SUM":
        reason = (
            "SUM returns (A + B) modulo 3. "
            f"With {assignments}, the result is {signal_level(output)}."
        )
    elif gate.name == "NMIN":
        reason = (
            "NMIN returns NOT (A MIN B). "
            f"With {assignments}, the minimum is {min(inputs)}, and its inversion is {output}."
        )
    elif gate.name == "NMAX":
        reason = (
            "NMAX returns NOT (A MAX B). "
            f"With {assignments}, the maximum is {max(inputs)}, and its inversion is {output}."
        )
    else:
        reason = f"The {gate.name} operation produced {signal_level(output)}."

    return "\n".join(
        [
            f"Input interpretation: {assignments}.",
            f"Output reasoning: {reason}",
            f"Logic rule used: {gate.logic_rule}",
            (
                "Practical application: in real hardware, this operation can appear in "
                "ternary arithmetic circuits, comparison units, signal routing systems, "
                "and educational computer architecture."
            ),
        ]
    )
