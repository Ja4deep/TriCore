"""
Educational blueprint repository containing pre-built template configurations,
practical applications, and functional diagrams.
"""

from __future__ import annotations

from dataclasses import dataclass

from logic_circuit_simulator.circuit import Circuit


@dataclass(frozen=True, slots=True)
class CircuitExampleCard:
    """Bundles architectural configuration templates along with educational explanations."""

    key: str
    title: str
    purpose: str
    real_world_application: str
    diagram_key: str
    setup_inputs: list[tuple[str, str]]
    setup_gates: list[tuple[str, str]]
    setup_outputs: list[tuple[str, str]]
    setup_wires: list[tuple[str, str, int]]


EXAMPLES_REPOSITORY: dict[str, CircuitExampleCard] = {
    "1": CircuitExampleCard(
        key="SIGNAL",
        title="Ternary Signal Combiner",
        purpose="Combines two ternary signals and takes the strongest (highest) level.",
        real_world_application="Signal priority selection in multi-sensor arrays.",
        diagram_key="SIGNAL",
        setup_inputs=[("A", "Sensor A Level"), ("B", "Sensor B Level")],
        setup_gates=[("G1", "MAX")],
        setup_outputs=[("OUT", "Priority Output")],
        setup_wires=[("A", "G1", 0), ("B", "G1", 1), ("G1", "OUT", 0)],
    ),
    "2": CircuitExampleCard(
        key="LIMITER",
        title="Ternary Signal Limiter",
        purpose="Ensures the output signal does not exceed a certain threshold (MID level).",
        real_world_application="Voltage regulation and safety clamping in ternary processors.",
        diagram_key="LIMITER",
        setup_inputs=[("A", "Raw Input Signal"), ("B", "MID Threshold (Set to 1)")],
        setup_gates=[("G1", "MIN")],
        setup_outputs=[("OUT", "Clamped Signal")],
        setup_wires=[("A", "G1", 0), ("B", "G1", 1), ("G1", "OUT", 0)],
    ),
    "3": CircuitExampleCard(
        key="ADDER",
        title="Ternary Half-Adder (Sum Only)",
        purpose="Computes the ternary sum of two trits using modulo-3 addition.",
        real_world_application="Demonstrates the sum stage used in ternary arithmetic units.",
        diagram_key="ADDER",
        setup_inputs=[("A", "Trit A"), ("B", "Trit B")],
        setup_gates=[("G1", "SUM")],
        setup_outputs=[("OUT", "Ternary Sum Result")],
        setup_wires=[("A", "G1", 0), ("B", "G1", 1), ("G1", "OUT", 0)],
    ),
}


def load_example_into_circuit(
    example: CircuitExampleCard, target_circuit: Circuit
) -> None:
    """Loads a predefined example circuit into the current workspace."""
    target_circuit.clear()

    for nid, lbl in example.setup_inputs:
        target_circuit.add_input(nid, lbl)

    for nid, gtype in example.setup_gates:
        target_circuit.add_gate(nid, gtype)

    for nid, lbl in example.setup_outputs:
        target_circuit.add_output(nid, lbl)

    for src, tgt, slot in example.setup_wires:
        target_circuit.connect(src, tgt, slot)
