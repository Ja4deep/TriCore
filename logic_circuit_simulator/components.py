"""
Defines individual circuit node components for the Logic Circuit Simulator,
reusing existing Digital Logic assets.
"""

from __future__ import annotations

from config import TERNARY_SIGNAL_VALUES
from digital_logic.logic_gates import evaluate_gate, explain_gate_result, get_gate
from exceptions import InvalidCircuitError


class CircuitNode:
    """Base structural node within a logic circuit graph network."""

    def __init__(self, node_id: str, label: str) -> None:
        self.node_id: str = node_id
        self.label: str = label
        self.inputs: list[CircuitNode | None] = []
        self.outputs: list[CircuitNode] = []
        self.value: int | None = None

    def add_output_connection(self, target_node: CircuitNode) -> None:
        """Appends a node target to the output collection."""
        if target_node not in self.outputs:
            self.outputs.append(target_node)


class InputNode(CircuitNode):
    """Represents a primary ternary input node."""

    def __init__(self, node_id: str, label: str) -> None:
        super().__init__(node_id, label)
        self.inputs = []  # Primary inputs have no source nodes
        self.value = 0

    def set_value(self, value: int) -> None:
        """Sets the ternary value of this input pin."""
        if value not in TERNARY_SIGNAL_VALUES:
            raise InvalidCircuitError("Input value must be 0, 1, or 2.")
        self.value = value


class OutputNode(CircuitNode):
    """Represents a primary ternary output node."""

    def __init__(self, node_id: str, label: str) -> None:
        super().__init__(node_id, label)
        self.inputs = [None]  # Single incoming driver connection slot

    def evaluate(self) -> int:
        """Passes through the computed signal from its driver node link."""
        driver = self.inputs[0]

        if driver is None:
            raise InvalidCircuitError(f"Output '{self.node_id}' is not connected.")

        if driver.value is None:
            raise InvalidCircuitError(
                f"Output '{self.node_id}' driver has not been evaluated."
            )

        value: int = driver.value

        self.value = value
        return value


class GateNode(CircuitNode):
    """Represents a ternary logic gate node."""

    def __init__(self, node_id: str, gate_type: str) -> None:
        gate_meta = get_gate(gate_type)
        super().__init__(node_id, gate_meta.name)
        self.gate_type: str = gate_meta.name
        self.inputs = [None] * gate_meta.arity

    def evaluate(self) -> int:
        """Computes the operational state by delegating to Phase 3 evaluators."""
        input_values = []

        for inp in self.inputs:
            if inp is None:
                raise InvalidCircuitError(
                    f"Gate '{self.node_id}' has an unconnected input."
                )

            if inp.value is None:
                raise InvalidCircuitError(
                    f"Input for gate '{self.node_id}' has not been evaluated."
                )

            input_values.append(inp.value)

        result = evaluate_gate(self.gate_type, tuple(input_values))

        self.value = result
        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id='{self.node_id}', "
            f"label='{self.label}')"
        )

    def get_educational_explanation(self) -> str:
        """Generates real-time architectural reasoning using original definitions."""
        input_values = []

        for inp in self.inputs:
            if inp is None:
                raise InvalidCircuitError(
                    f"Gate '{self.node_id}' has an unconnected input."
                )

            if inp.value is None:
                raise InvalidCircuitError(
                    f"Input for gate '{self.node_id}' has not been evaluated."
                )

            input_values.append(inp.value)

        current_out = self.value if self.value is not None else 0

        return explain_gate_result(self.gate_type, tuple(input_values), current_out)
