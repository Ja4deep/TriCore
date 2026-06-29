"""Validation helpers for ternary digital logic input."""

from __future__ import annotations

from arithmetic.utils import clean_input, validate_not_empty

from .logic_gates import get_gate
from .utils import TERNARY_TEXT


def normalize_gate_name(gate_name: str) -> str:
    """Validate and return a supported ternary gate name in uppercase."""
    normalized_name = clean_input(gate_name).upper()
    validate_not_empty(normalized_name, field_name="Gate name")
    return get_gate(normalized_name).name


def validate_ternary_value(value: str, *, field_name: str = "Input") -> int:
    """Validate a single ternary value and return it as an integer."""
    normalized_value = clean_input(value)
    validate_not_empty(normalized_value, field_name=field_name)

    if normalized_value not in TERNARY_TEXT:
        raise ValueError(f"{field_name} must be a ternary value: 0, 1, or 2.")

    return int(normalized_value)


def validate_ternary_values(
    values: list[str] | tuple[str, ...],
    *,
    expected_count: int,
    field_name: str = "Input",
) -> tuple[int, ...]:
    """Validate multiple ternary values for gate simulation."""
    if len(values) != expected_count:
        raise ValueError(f"{field_name} requires {expected_count} ternary value(s).")

    return tuple(
        validate_ternary_value(value, field_name=f"{field_name} {index}")
        for index, value in enumerate(values, start=1)
    )


def validate_expression_text(expression: str) -> str:
    """Validate that a ternary logic expression is not empty."""
    normalized_expression = clean_input(expression)
    validate_not_empty(normalized_expression, field_name="Logic expression")
    return normalized_expression
