import pytest

from exceptions import SimulationError
from logic_circuit_simulator.circuit import Circuit
from logic_circuit_simulator.evaluator import run_circuit_simulation


def test_circuit_simulation_min_gate() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_input("B", "Input B")
    circuit.add_gate("G1", "MIN")
    circuit.add_output("OUT", "Output")

    circuit.connect("A", "G1", 0)
    circuit.connect("B", "G1", 1)
    circuit.connect("G1", "OUT", 0)

    # Test cases: (A, B) -> Output
    test_cases = [
        ({"A": 0, "B": 2}, 0),
        ({"A": 1, "B": 2}, 1),
        ({"A": 2, "B": 2}, 2),
    ]

    for inputs, expected in test_cases:
        payload = run_circuit_simulation(circuit, inputs)
        assert payload.output_states["OUT"] == expected


def test_circuit_simulation_sum_gate() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_input("B", "Input B")
    circuit.add_gate("G1", "SUM")
    circuit.add_output("OUT", "Output")

    circuit.connect("A", "G1", 0)
    circuit.connect("B", "G1", 1)
    circuit.connect("G1", "OUT", 0)

    # Test cases: (A, B) -> Output
    test_cases = [
        ({"A": 1, "B": 1}, 2),
        ({"A": 2, "B": 1}, 0),
        ({"A": 2, "B": 2}, 1),
    ]

    for inputs, expected in test_cases:
        payload = run_circuit_simulation(circuit, inputs)
        assert payload.output_states["OUT"] == expected


def test_circuit_simulation_nmin_gate() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_input("B", "Input B")
    circuit.add_gate("G1", "NMIN")
    circuit.add_output("OUT", "Output")

    circuit.connect("A", "G1", 0)
    circuit.connect("B", "G1", 1)
    circuit.connect("G1", "OUT", 0)

    # Test cases: (A, B) -> Output
    test_cases = [
        ({"A": 2, "B": 2}, 0),  # NOT (2 MIN 2) = NOT 2 = 0
        ({"A": 1, "B": 2}, 1),  # NOT (1 MIN 2) = NOT 1 = 1
        ({"A": 0, "B": 0}, 2),  # NOT (0 MIN 0) = NOT 0 = 2
    ]

    for inputs, expected in test_cases:
        payload = run_circuit_simulation(circuit, inputs)
        assert payload.output_states["OUT"] == expected


def test_circuit_simulation_rejects_missing_runtime_input() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_input("B", "Input B")
    circuit.add_gate("G1", "MIN")
    circuit.add_output("OUT", "Output")

    circuit.connect("A", "G1", 0)
    circuit.connect("B", "G1", 1)
    circuit.connect("G1", "OUT", 0)

    with pytest.raises(SimulationError, match="Missing runtime input"):
        run_circuit_simulation(circuit, {"A": 1})


def test_circuit_simulation_rejects_unknown_runtime_input() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_output("OUT", "Output")
    circuit.connect("A", "OUT", 0)

    with pytest.raises(SimulationError, match="not declared"):
        run_circuit_simulation(circuit, {"A": 1, "B": 2})
