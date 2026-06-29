"""
Evaluates logic circuit network states and creates step-by-step signal
propagation traces for educational review.
"""

from __future__ import annotations

from dataclasses import dataclass

from exceptions import SimulationError
from logic_circuit_simulator.circuit import Circuit
from logic_circuit_simulator.components import (
    CircuitNode,
    GateNode,
    InputNode,
    OutputNode,
)


@dataclass(frozen=True, slots=True)
class PropagationStep:
    """Stores information about one signal propagation step."""

    step_number: int
    node_id: str
    label: str
    node_type: str
    assigned_value: int
    narrative_detail: str


@dataclass(frozen=True, slots=True)
class SimulationPayload:
    """Stores simulation results and the execution trace."""

    input_states: dict[str, int]
    output_states: dict[str, int]
    execution_trace: list[PropagationStep]


def run_circuit_simulation(
    circuit: Circuit,
    runtime_inputs: dict[str, int],
) -> SimulationPayload:
    """Run a complete ternary circuit simulation.

    Args:
        circuit: Circuit graph to evaluate.
        runtime_inputs: Mapping of input node IDs to ternary signal values.

    Returns:
        Final input states, output states, and propagation trace.

    Raises:
        InvalidCircuitError: If the circuit graph is incomplete or cyclic.
        SimulationError: If evaluation cannot assign a node value.
    """
    circuit.validate_integrity()
    _reset_computed_node_values(circuit)
    _apply_runtime_inputs(circuit, runtime_inputs)

    execution_trace = _record_input_assignments(circuit)
    step_counter = len(execution_trace) + 1

    for node in circuit.compile_topological_order():
        if isinstance(node, InputNode):
            continue

        execution_trace.append(_evaluate_traceable_node(node, step_counter))
        step_counter += 1

    return SimulationPayload(
        input_states=_collect_input_states(circuit),
        output_states=_collect_output_states(circuit),
        execution_trace=execution_trace,
    )


def _reset_computed_node_values(circuit: Circuit) -> None:
    """Clear cached gate and output values before a simulation run."""
    for node in [*circuit.gates.values(), *circuit.outputs.values()]:
        node.value = None


def _apply_runtime_inputs(circuit: Circuit, runtime_inputs: dict[str, int]) -> None:
    """Assign provided runtime values to declared input nodes."""
    declared_inputs = set(circuit.inputs)
    provided_inputs = set(runtime_inputs)

    unknown_inputs = sorted(provided_inputs - declared_inputs)
    if unknown_inputs:
        names = ", ".join(unknown_inputs)
        raise SimulationError(f"Runtime input(s) not declared in circuit: {names}.")

    missing_inputs = sorted(declared_inputs - provided_inputs)
    if missing_inputs:
        names = ", ".join(missing_inputs)
        raise SimulationError(f"Missing runtime input value(s): {names}.")

    for node_id in sorted(circuit.inputs):
        circuit.inputs[node_id].set_value(runtime_inputs[node_id])


def _record_input_assignments(circuit: Circuit) -> list[PropagationStep]:
    """Create trace entries for all primary input assignments."""
    execution_trace: list[PropagationStep] = []

    for node_id in sorted(circuit.inputs.keys()):
        inp = circuit.inputs[node_id]

        if inp.value is None:
            raise SimulationError(f"Input '{inp.node_id}' has no assigned value.")

        execution_trace.append(
            PropagationStep(
                step_number=len(execution_trace) + 1,
                node_id=inp.node_id,
                label=inp.label,
                node_type="TERNARY INPUT",
                assigned_value=int(inp.value),
                narrative_detail=(
                    f"Primary ternary input '{inp.label}' "
                    f"assigned signal value {inp.value}."
                ),
            )
        )

    return execution_trace


def _evaluate_traceable_node(node: CircuitNode, step_number: int) -> PropagationStep:
    """Evaluate one gate or output node and return its trace entry."""
    if isinstance(node, GateNode):
        return _evaluate_gate_node(node, step_number)
    if isinstance(node, OutputNode):
        return _evaluate_output_node(node, step_number)

    raise SimulationError(f"Unsupported circuit node type: {type(node).__name__}.")


def _evaluate_gate_node(node: GateNode, step_number: int) -> PropagationStep:
    """Evaluate one gate node and build its propagation trace step."""
    node.evaluate()
    if node.value is None:
        raise SimulationError(f"Gate '{node.node_id}' evaluation produced no value.")

    return PropagationStep(
        step_number=step_number,
        node_id=node.node_id,
        label=node.label,
        node_type=f"{node.gate_type} GATE",
        assigned_value=int(node.value),
        narrative_detail=node.get_educational_explanation().replace("\n", " "),
    )


def _evaluate_output_node(node: OutputNode, step_number: int) -> PropagationStep:
    """Evaluate one output node and build its propagation trace step."""
    node.evaluate()
    if node.value is None:
        raise SimulationError(f"Output '{node.node_id}' evaluation produced no value.")

    return PropagationStep(
        step_number=step_number,
        node_id=node.node_id,
        label=node.label,
        node_type="TERNARY OUTPUT",
        assigned_value=int(node.value),
        narrative_detail=(
            f"Output node '{node.label}' received signal value {node.value}."
        ),
    )


def _collect_input_states(circuit: Circuit) -> dict[str, int]:
    """Return final assigned input values."""
    return {
        node_id: int(node.value)
        for node_id, node in circuit.inputs.items()
        if node.value is not None
    }


def _collect_output_states(circuit: Circuit) -> dict[str, int]:
    """Return final output values."""
    return {
        node_id: int(node.value)
        for node_id, node in circuit.outputs.items()
        if node.value is not None
    }
