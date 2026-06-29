import pytest

from arithmetic.division import divide_numbers
from arithmetic.utils import validate_supported_base, validate_ternary_operand
from digital_logic.logic_gates import evaluate_gate
from exceptions import (
    DivisionByZeroError,
    InvalidBaseError,
    InvalidGateError,
    InvalidNumberError,
)
from logic_circuit_simulator.circuit import Circuit
from logic_circuit_simulator.evaluator import run_circuit_simulation


def test_invalid_number_errors_remain_value_error_compatible() -> None:
    with pytest.raises(ValueError) as exc_info:
        validate_ternary_operand("12A")

    assert isinstance(exc_info.value, InvalidNumberError)


def test_invalid_base_uses_domain_exception() -> None:
    with pytest.raises(InvalidBaseError):
        validate_supported_base(10)


def test_division_by_zero_uses_domain_exception() -> None:
    with pytest.raises(DivisionByZeroError):
        divide_numbers("1", "0")


def test_invalid_gate_uses_domain_exception() -> None:
    with pytest.raises(InvalidGateError):
        evaluate_gate("UNKNOWN", (1,))


def test_invalid_runtime_signal_is_reported() -> None:
    circuit = Circuit()
    circuit.add_input("A", "Input A")
    circuit.add_output("OUT", "Output")
    circuit.connect("A", "OUT", 0)

    with pytest.raises(ValueError, match="Input value must be 0, 1, or 2"):
        run_circuit_simulation(circuit, {"A": 3})
