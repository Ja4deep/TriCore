"""Shared carry-tracking helpers for arithmetic operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .utils import int_to_trit


@dataclass(frozen=True, slots=True)
class CarryRecord:
    """Describe a carry created during a column-based operation.

    Attributes:
        position: Zero-based position from the rightmost digit.
        value: The carried value.
        source: Optional human-readable source for explanation output.
    """

    position: int
    value: int
    source: str = ""


def create_carry(position: int, value: int, source: str = "") -> CarryRecord:
    """Create a validated carry record.

    Args:
        position: Zero-based position from the rightmost digit.
        value: The carried value.
        source: Optional human-readable source for explanation output.

    Returns:
        A validated carry record.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("Carry position cannot be negative.")

    return CarryRecord(position=position, value=value, source=source)


def normalize_carries(carries: Sequence[int | CarryRecord]) -> list[CarryRecord]:
    """Return carries as records with stable positions.

    Args:
        carries: Carry values or existing carry records.

    Returns:
        Carry records in the same order as the input.
    """
    normalized_carries = []

    for position, carry in enumerate(carries):
        if isinstance(carry, CarryRecord):
            normalized_carries.append(carry)
        else:
            normalized_carries.append(create_carry(position, carry))

    return normalized_carries


def calculate_carry(total: int, *, base: int = 3) -> tuple[str, int]:
    """Return the written digit and carry for a column total.

    Args:
        total: Sum or product total for the current column.
        base: Number base used by the operation.

    Returns:
        A tuple containing the digit to write and the carry to propagate.
    """
    if total < 0:
        raise ValueError("Carry total cannot be negative.")
    if base < 2:
        raise ValueError("Base must be at least 2.")

    return int_to_trit(total % base), total // base


def describe_carry(
    position: int,
    operands: Sequence[int],
    carry_in: int,
    written_digit: str,
    carry_out: int,
    *,
    base: int = 3,
) -> str:
    """Build a beginner-friendly carry explanation for one column."""
    expression_parts = [str(operand) for operand in operands]
    if carry_in:
        expression_parts.append(f"carry {carry_in}")

    total = sum(operands) + carry_in
    lines = [
        f"Column {position + 1}",
        " + ".join(expression_parts),
        f"= {to_base_text(total, base)}",
        f"Write {written_digit}",
    ]

    if carry_out:
        lines.append(f"Carry {carry_out}")
    else:
        lines.append("Carry 0")

    return "\n".join(lines)


def to_base_text(value: int, base: int = 3) -> str:
    """Return a small non-negative integer as base text for explanations."""
    if value < 0:
        raise ValueError("Value cannot be negative.")
    if base < 2:
        raise ValueError("Base must be at least 2.")
    if value == 0:
        return "0_3" if base == 3 else "0"

    digits = []
    working_value = value

    while working_value:
        digits.append(str(working_value % base))
        working_value //= base

    suffix = "_3" if base == 3 else f"_{base}"
    return "".join(reversed(digits)) + suffix
