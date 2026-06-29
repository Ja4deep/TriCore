"""
ASCII visualization layout generators and structural terminal presentation helpers
matching original interface templates.
"""

from __future__ import annotations

from logic_circuit_simulator.circuit import Circuit


def generate_static_ascii_layout(circuit: Circuit) -> list[str]:
    """Generates a structured ASCII visualization diagram showing active node mappings."""
    lines: list[str] = []
    lines.append("─" * 60)
    lines.append(" CIRCUIT ARCHITECTURE ".center(60, "■"))
    lines.append("─" * 60)

    lines.append("\n[INPUTS]")
    for inp_id, inp in sorted(circuit.inputs.items()):
        lines.append(
            f"  ID: {inp_id:5} ── [ {inp.label} ] ── Signal: {inp.value if inp.value is not None else 'UNSET'}"
        )

    lines.append("\n[LOGIC GATES]")
    for gate_id, gate in sorted(circuit.gates.items()):
        input_connections = []
        for idx, src in enumerate(gate.inputs):
            src_str = f"{src.node_id} ({src.label})" if src else "DISCONNECTED"
            input_connections.append(f"Slot {idx}: {src_str}")
        conn_lbl = ", ".join(input_connections)
        lines.append(
            f"  ID: {gate_id:5} ── [ {gate.gate_type} ] ── {conn_lbl} ── Result: {gate.value if gate.value is not None else 'UNEVALUATED'}"
        )
    lines.append("\n[OUTPUTS]")
    for out_id, out in sorted(circuit.outputs.items()):
        source_node = out.inputs[0]

        if source_node is None:
            src_str = "DISCONNECTED"
        else:
            src_str = f"{source_node.node_id} ({source_node.label})"
        lines.append(
            f"  ID: {out_id:5} ── [ {out.label} ] ── From: {src_str} ── Result: {out.value if out.value is not None else 'UNSET'}"
        )

    lines.append("─" * 60)
    return lines


def format_custom_flow_diagram(example_key: str) -> list[str]:
    """Provides high-fidelity, explicit educational path sketches for pre-baked functional circuits."""
    diagrams: dict[str, list[str]] = {
        "SIGNAL": [
            "  Input_A (Sensor A Level) ─────┐",
            "                                ├───────► [MAX GATE] ─────► Output (Priority Output)",
            "  Input_B (Sensor B Level) ─────┘",
        ],
        "LIMITER": [
            "  Input_A (Raw Input Signal) ───┐",
            "                                ├───────► [MIN GATE] ─────► Output (Clamped Signal)",
            "  Input_B (MID Threshold) ──────┘",
        ],
        "ADDER": [
            "  Input_A (Trit A) ─────────────┐",
            "                                ├───────► [SUM GATE] ─────► Output (Ternary Sum Result)",
            "  Input_B (Trit B) ─────────────┘",
        ],
    }
    return diagrams.get(
        example_key,
        ["  [Custom Layout Graph Topology - Dynamic Structural Data Link Extant]"],
    )
