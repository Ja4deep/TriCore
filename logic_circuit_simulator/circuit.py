"""
Manages topological graph compilation, node mapping, and validation checks
for the active logic circuit instance.
"""

from __future__ import annotations

from exceptions import InvalidCircuitError
from logic_circuit_simulator.components import (
    CircuitNode,
    GateNode,
    InputNode,
    OutputNode,
)


class Circuit:
    """Represents a ternary logic circuit consisting of inputs, gates, and outputs."""

    def __init__(self) -> None:
        self.inputs: dict[str, InputNode] = {}
        self.gates: dict[str, GateNode] = {}
        self.outputs: dict[str, OutputNode] = {}

    def clear(self) -> None:
        """Resets the circuit graph container to a blank slate state."""
        self.inputs.clear()
        self.gates.clear()
        self.outputs.clear()

    def add_input(self, node_id: str, label: str) -> None:
        """Creates a unique input node parameter."""
        self._validate_unique_node_id(node_id)
        self.inputs[node_id] = InputNode(node_id, label)

    def add_gate(self, node_id: str, gate_type: str) -> None:
        """Registers an operational gate type configuration."""
        self._validate_unique_node_id(node_id)
        self.gates[node_id] = GateNode(node_id, gate_type)

    def add_output(self, node_id: str, label: str) -> None:
        """Adds an output node to the circuit."""
        self._validate_unique_node_id(node_id)
        self.outputs[node_id] = OutputNode(node_id, label)

    def connect(self, source_id: str, target_id: str, input_slot: int = 0) -> None:
        """Connects a source node to a target input slot."""
        source = self.get_node(source_id)
        target = self.get_node(target_id)

        if source_id == target_id:
            raise InvalidCircuitError("A node cannot be connected to itself.")

        if isinstance(source, OutputNode):
            raise InvalidCircuitError(
                "An Output port cannot act as a source driver signal."
            )
        if isinstance(target, InputNode):
            raise InvalidCircuitError(
                "An Input pin connection port cannot receive an entry line signal."
            )

        if input_slot < 0 or input_slot >= len(target.inputs):
            raise InvalidCircuitError(
                f"Target '{target_id}' has no matching input socket slot: {input_slot}"
            )

        if target.inputs[input_slot] is not None:
            raise InvalidCircuitError(
                f"Input slot {input_slot} of '{target_id}' is already connected."
            )

        target.inputs[input_slot] = source
        source.add_output_connection(target)

    def get_node(self, node_id: str) -> CircuitNode:
        """Locates any registered node instance within the tracking scopes."""
        if node_id in self.inputs:
            return self.inputs[node_id]
        if node_id in self.gates:
            return self.gates[node_id]
        if node_id in self.outputs:
            return self.outputs[node_id]
        raise InvalidCircuitError(
            f"Target node lookup identifier '{node_id}' not found."
        )

    def compile_topological_order(self) -> list[CircuitNode]:
        """Validates graph connectivity constraints and structures evaluation sequencing."""
        visited: set[str] = set()
        stack: set[str] = set()
        order: list[CircuitNode] = []

        def dfs(node: CircuitNode) -> None:
            if node.node_id in stack:
                raise InvalidCircuitError(
                    "Circular structural dependency feedback loop detected in circuit layout."
                )
            if node.node_id not in visited:
                stack.add(node.node_id)
                for out in node.outputs:
                    dfs(out)
                stack.remove(node.node_id)
                visited.add(node.node_id)
                order.insert(0, node)

        # Initialize tracking maps through input sources
        for input_node in self.inputs.values():
            dfs(input_node)

        # Trap floating/unconnected internal sub-graph elements
        for gate_node in self.gates.values():
            if gate_node.node_id not in visited:
                dfs(gate_node)

        return order

    def validate_integrity(self) -> None:
        """Guarantees circuit validation constraints match expected design maps."""
        if not self.inputs and not self.gates and not self.outputs:
            raise InvalidCircuitError("Circuit topology is currently empty.")

        for name, gate in self.gates.items():
            for idx, src in enumerate(gate.inputs):
                if src is None:
                    raise InvalidCircuitError(
                        f"Gate component '{name}' contains a disconnected tracking input terminal line at index [{idx}]."
                    )

        for name, out in self.outputs.items():
            if out.inputs[0] is None:
                raise InvalidCircuitError(
                    f"Output port element '{name}' has no incoming driving connection linked."
                )

        # Execute topological compilation pass to guarantee loop clearance
        self.compile_topological_order()

    def _validate_unique_node_id(self, node_id: str) -> None:
        """Ensure a node identifier is unused across all circuit collections."""
        if node_id in self.inputs or node_id in self.gates or node_id in self.outputs:
            raise InvalidCircuitError(
                f"Node identifier '{node_id}' already assigned in graph."
            )
