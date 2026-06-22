"""Shared borrow-tracking helpers for arithmetic operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class BorrowRecord:
    """Describe a borrow created during a column-based operation.

    Attributes:
        position: Zero-based position from the rightmost digit.
        value: The borrowed value.
        source: Optional human-readable source for explanation output.
    """

    position: int
    value: int
    source: str = ""


def create_borrow(position: int, value: int, source: str = "") -> BorrowRecord:
    """Create a validated borrow record.

    Args:
        position: Zero-based position from the rightmost digit.
        value: The borrowed value.
        source: Optional human-readable source for explanation output.

    Returns:
        A validated borrow record.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("Borrow position cannot be negative.")

    return BorrowRecord(position=position, value=value, source=source)


def normalize_borrows(borrows: Sequence[int | BorrowRecord]) -> list[BorrowRecord]:
    """Return borrows as records with stable positions.

    Args:
        borrows: Borrow values or existing borrow records.

    Returns:
        Borrow records in the same order as the input.
    """
    normalized_borrows = []

    for position, borrow in enumerate(borrows):
        if isinstance(borrow, BorrowRecord):
            normalized_borrows.append(borrow)
        else:
            normalized_borrows.append(create_borrow(position, borrow))

    return normalized_borrows


def calculate_borrow(
    top_digit: int,
    bottom_digit: int,
    borrow_in: int,
    *,
    base: int = 3,
) -> tuple[str, int, int]:
    """Return written digit, borrow out, and adjusted top digit.

    Args:
        top_digit: Digit from the minuend column.
        bottom_digit: Digit from the subtrahend column.
        borrow_in: Borrow already owed from the previous lower column.
        base: Number base used by the operation.

    Returns:
        A tuple containing the written digit, outgoing borrow, and adjusted
        top digit after any incoming and outgoing borrow changes.
    """
    if base < 2:
        raise ValueError("Base must be at least 2.")
    if borrow_in not in {0, 1}:
        raise ValueError("Borrow input must be 0 or 1.")

    adjusted_top_digit = top_digit - borrow_in
    borrow_out = 0

    if adjusted_top_digit < bottom_digit:
        adjusted_top_digit += base
        borrow_out = 1

    return str(adjusted_top_digit - bottom_digit), borrow_out, adjusted_top_digit


def describe_borrow(
    position: int,
    top_digit: int,
    bottom_digit: int,
    borrow_in: int,
    written_digit: str,
    borrow_out: int,
    *,
    base: int = 3,
) -> str:
    """Build a beginner-friendly borrow explanation for one column."""
    adjusted_top_digit = top_digit - borrow_in

    if borrow_out:
        borrowed_value = adjusted_top_digit + base
        return "\n".join(
            [
                f"Column {position + 1}",
                f"Cannot subtract {bottom_digit} from {adjusted_top_digit}.",
                "Borrow one trit from the next column.",
                f"After borrowing, the column has {borrowed_value}.",
                f"{borrowed_value} - {bottom_digit} = {written_digit}",
                f"Write {written_digit}",
            ]
        )

    return "\n".join(
        [
            f"Column {position + 1}",
            f"{adjusted_top_digit} - {bottom_digit} = {written_digit}",
            f"Write {written_digit}",
        ]
    )
