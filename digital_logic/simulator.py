"""Interactive and testable gate simulation helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .logic_gates import evaluate_gate, explain_gate_result, get_gate


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Structured result from simulating one logic gate."""

    gate_name: str
    inputs: tuple[int, ...]
    output: int
    explanation: str


def simulate_gate(gate_name: str, inputs: tuple[int, ...]) -> SimulationResult:
    """Simulate a gate and return the output with an explanation."""
    gate = get_gate(gate_name)
    output = evaluate_gate(gate.name, inputs)
    explanation = explain_gate_result(gate.name, inputs, output)

    return SimulationResult(
        gate_name=gate.name,
        inputs=inputs,
        output=output,
        explanation=explanation,
    )
