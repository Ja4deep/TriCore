"""Formatting helpers for Digital Logic Laboratory screens."""

from __future__ import annotations

from ui.terminal import key_value_lines, table_lines

from .logic_gates import LogicGate, get_gate
from .simulator import SimulationResult
from .truth_tables import generate_truth_table
from .utils import input_labels


def gate_detail_lines(gate: LogicGate) -> list[str]:
    """Return display lines describing one logic gate."""
    lines = [
        "Definition",
        gate.definition,
        "",
        "Symbol",
        gate.symbol,
        "",
        "Circuit Diagram",
        *gate.diagram,
        "",
        "Logic Rule",
        gate.logic_rule,
        "",
        "Educational Explanation",
        gate.explanation,
        "",
        "Real-World Applications",
    ]
    lines.extend(f"- {application}" for application in gate.applications)
    return lines


def truth_table_lines(gate_name: str) -> list[str]:
    """Return formatted truth table lines for a supported gate."""
    headers, rows = generate_truth_table(gate_name)
    return table_lines(headers, rows)


def simulation_result_lines(result: SimulationResult) -> list[str]:
    """Return key-value lines for a simulation result."""
    labels = input_labels(len(result.inputs))
    input_items = [
        (f"Input {label}", value)
        for label, value in zip(labels, result.inputs, strict=True)
    ]
    return key_value_lines(
        [
            ("Gate", result.gate_name),
            *input_items,
            ("Output", result.output),
        ]
    )


def simulation_diagram_lines(result: SimulationResult) -> list[str]:
    """Return an annotated circuit diagram for a simulation result."""
    gate = get_gate(result.gate_name)
    return [
        *gate.diagram,
        "",
        f"Output = {result.output}",
    ]


def gate_reference_lines(gate_name: str) -> list[str]:
    """Return a compact reference card for a gate and its truth table."""
    gate = get_gate(gate_name)
    return [
        *gate_detail_lines(gate),
        "",
        "Truth Table",
        *truth_table_lines(gate.name),
    ]
