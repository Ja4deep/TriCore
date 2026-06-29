"""
Input data scrubbers and graph integrity validation guards.
"""

from __future__ import annotations
from config import TERNARY_SIGNAL_DIGITS
from exceptions import InvalidCircuitError

from arithmetic.utils import clean_input, validate_not_empty


def parse_and_validate_slot_index(raw_entry: str) -> int:
    """Parses a text index entry to guarantee it resolves to a valid integer boundary."""
    cleaned = clean_input(raw_entry)
    validate_not_empty(cleaned, field_name="Input Target Pin Slot Identifier")
    if not cleaned.isdigit():
        raise InvalidCircuitError(
            "Input socket selection parameter must be a non-negative integer numeric digit."
        )
    return int(cleaned)


def parse_and_validate_ternary_state(raw_entry: str) -> int:
    """Ensures incoming signals match expected ternary values (0, 1, or 2)."""
    cleaned = clean_input(raw_entry)
    validate_not_empty(cleaned, field_name="Signal Level Value")
    if cleaned not in TERNARY_SIGNAL_DIGITS:
        raise InvalidCircuitError("Signal state must be a ternary value: 0, 1, or 2.")
    return int(cleaned)
