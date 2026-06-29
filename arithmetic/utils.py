"""Validation and alignment helpers shared by arithmetic modules."""

from __future__ import annotations

from typing import Iterable, Sequence

from config import (
    BALANCED_TERNARY_DIGITS,
    BOM_CHARACTERS,
    ORDINARY_TERNARY_DIGITS,
    SUPPORTED_BASE,
    TERNARY_SIGNAL_VALUES,
)
from exceptions import InvalidBaseError, InvalidNumberError


def clean_input(raw_input_value: str) -> str:
    """Return input with outer whitespace and hidden BOM characters removed."""
    cleaned_value = raw_input_value.strip()

    for character in BOM_CHARACTERS:
        cleaned_value = cleaned_value.replace(character, "")

    return cleaned_value


def has_outer_whitespace(value: str) -> bool:
    """Return whether value contains leading or trailing whitespace."""
    return value != value.strip()


def validate_not_empty(value: str, *, field_name: str = "Input") -> str:
    """Validate that a string is not empty."""
    if value == "":
        raise InvalidNumberError(f"{field_name} cannot be empty.")

    return value


def validate_no_outer_whitespace(value: str, *, field_name: str = "Input") -> str:
    """Validate that a string has no leading or trailing whitespace."""
    if has_outer_whitespace(value):
        raise InvalidNumberError(
            f"{field_name} cannot contain leading or trailing whitespace."
        )

    return value


def validate_digits(
    value: str,
    allowed_digits: Iterable[str],
    *,
    field_name: str = "Input",
) -> str:
    """Validate that a string only contains allowed digits."""
    allowed_digit_set = set(allowed_digits)
    invalid_digits = [digit for digit in value if digit not in allowed_digit_set]

    if invalid_digits:
        allowed_display = ", ".join(sorted(allowed_digit_set))
        raise InvalidNumberError(f"{field_name} can only contain {allowed_display}.")

    return value


def validate_no_leading_zeros(
    value: str,
    *,
    field_name: str = "Input",
    allow_leading_zeros: bool = False,
) -> str:
    """Validate that a number string does not contain unnecessary leading zeros."""
    if allow_leading_zeros:
        return value

    sign, digits = split_sign(value)

    if len(digits) > 1 and digits.startswith("0"):
        raise InvalidNumberError(f"{field_name} cannot contain leading zeros.")

    return sign + digits


def validate_number_string(
    value: str,
    allowed_digits: Iterable[str],
    *,
    field_name: str = "Input",
    allow_leading_zeros: bool = False,
    allow_negative_sign: bool = False,
    allow_outer_whitespace: bool = False,
    uppercase: bool = False,
) -> str:
    """Validate an arbitrary-length number string without converting to int.

    Args:
        value: Raw number text.
        allowed_digits: Digits allowed after any sign is removed.
        field_name: Name used in error messages.
        allow_leading_zeros: Whether values such as 001 are allowed.
        allow_negative_sign: Whether a leading minus sign is allowed.
        allow_outer_whitespace: Whether leading/trailing whitespace is allowed.
        uppercase: Whether to uppercase the normalized value before digit checks.

    Returns:
        A normalized string that keeps arbitrary length intact.
    """
    if not allow_outer_whitespace:
        validate_no_outer_whitespace(value, field_name=field_name)

    normalized_value = clean_input(value)
    if uppercase:
        normalized_value = normalized_value.upper()

    validate_not_empty(normalized_value, field_name=field_name)

    sign, digits = split_sign(normalized_value)
    if sign and not allow_negative_sign:
        raise InvalidNumberError(f"{field_name} cannot contain a negative sign.")

    validate_not_empty(digits, field_name=field_name)
    validate_digits(digits, allowed_digits, field_name=field_name)
    validate_no_leading_zeros(
        sign + digits,
        field_name=field_name,
        allow_leading_zeros=allow_leading_zeros,
    )

    return sign + digits


def validate_ordinary_ternary(
    value: str,
    *,
    field_name: str = "Ordinary ternary input",
    allow_leading_zeros: bool = False,
    allow_negative_sign: bool = True,
    allow_outer_whitespace: bool = False,
) -> str:
    """Validate an arbitrary-length ordinary ternary number."""
    return validate_number_string(
        value,
        ORDINARY_TERNARY_DIGITS,
        field_name=field_name,
        allow_leading_zeros=allow_leading_zeros,
        allow_negative_sign=allow_negative_sign,
        allow_outer_whitespace=allow_outer_whitespace,
    )


def validate_supported_base(base: int) -> int:
    """Validate that an arithmetic operation is using ordinary ternary."""
    if base != SUPPORTED_BASE:
        raise InvalidBaseError("TriCore arithmetic currently supports base 3 only.")

    return base


def validate_ternary_operand(value: str, *, field_name: str = "Operand") -> str:
    """Validate a non-negative ordinary ternary operand for arithmetic."""
    return validate_ordinary_ternary(
        value,
        field_name=field_name,
        allow_negative_sign=False,
    )


def validate_balanced_ternary(
    value: str,
    *,
    field_name: str = "Balanced ternary input",
    allow_leading_zeros: bool = False,
    allow_negative_sign: bool = False,
    allow_outer_whitespace: bool = False,
) -> str:
    """Validate an arbitrary-length balanced ternary number."""
    return validate_number_string(
        value,
        BALANCED_TERNARY_DIGITS,
        field_name=field_name,
        allow_leading_zeros=allow_leading_zeros,
        allow_negative_sign=allow_negative_sign,
        allow_outer_whitespace=allow_outer_whitespace,
        uppercase=True,
    )


def split_sign(value: str) -> tuple[str, str]:
    """Split an optional leading minus sign from a number string."""
    if value.startswith("-"):
        return "-", value[1:]

    return "", value


def strip_leading_zeros(value: str) -> str:
    """Return a number string with unnecessary leading zeros removed."""
    sign, digits = split_sign(value)
    stripped_digits = digits.lstrip("0") or "0"

    if stripped_digits == "0":
        return stripped_digits

    return sign + stripped_digits


def compare_magnitudes(left: str, right: str) -> int:
    """Compare two non-negative number strings by magnitude.

    Returns:
        1 if left is larger, -1 if right is larger, and 0 if they are equal.
    """
    left_digits = strip_leading_zeros(split_sign(left)[1])
    right_digits = strip_leading_zeros(split_sign(right)[1])

    if len(left_digits) > len(right_digits):
        return 1
    if len(left_digits) < len(right_digits):
        return -1
    if left_digits > right_digits:
        return 1
    if left_digits < right_digits:
        return -1

    return 0


def trit_to_int(trit: str) -> int:
    """Convert one ordinary ternary digit to an integer."""
    validate_digits(trit, ORDINARY_TERNARY_DIGITS, field_name="Trit")
    if len(trit) != 1:
        raise InvalidNumberError("Trit must be exactly one digit.")

    return int(trit)


def int_to_trit(value: int) -> str:
    """Convert a one-digit integer value to an ordinary ternary digit."""
    if value not in TERNARY_SIGNAL_VALUES:
        raise InvalidNumberError("Trit value must be 0, 1, or 2.")

    return str(value)


def split_digits(value: str) -> list[str]:
    """Return a number string as a list of digits without its sign."""
    _sign, digits = split_sign(value)
    return list(digits)


def align_numbers(*numbers: str, fill: str = "0") -> tuple[str, ...]:
    """Left-pad numbers so their digit strings have the same length."""
    if len(fill) != 1:
        raise InvalidNumberError("Fill must be a single character.")
    if not numbers:
        return ()

    signless_numbers = [split_sign(number)[1] for number in numbers]
    width = max(len(number) for number in signless_numbers)

    return tuple(number.rjust(width, fill) for number in signless_numbers)


def iter_digits_from_right(value: str) -> list[str]:
    """Return digits from right to left for column-based operations."""
    return list(reversed(split_digits(value)))


def chunk_from_right(value: str, chunk_size: int) -> list[str]:
    """Split a number string into chunks from right to left."""
    if chunk_size < 1:
        raise InvalidNumberError("Chunk size must be at least 1.")

    digits = split_sign(value)[1]
    chunks = []

    while digits:
        chunks.append(digits[-chunk_size:])
        digits = digits[:-chunk_size]

    return chunks


def ensure_same_length(values: Sequence[str]) -> tuple[str, ...]:
    """Return values unchanged if they already have equal digit lengths."""
    if not values:
        return ()

    lengths = {len(split_sign(value)[1]) for value in values}
    if len(lengths) != 1:
        raise InvalidNumberError("Values must have the same digit length.")

    return tuple(values)
