"""Ordinary ternary long multiplication with structured explanations."""

from __future__ import annotations

from dataclasses import dataclass

from .addition import add_many
from .carry import CarryRecord, calculate_carry, create_carry, describe_carry
from .explanation import ArithmeticResult, ExplanationStep, create_step
from .formatter import align_arithmetic_expression
from .utils import (
    iter_digits_from_right,
    strip_leading_zeros,
    trit_to_int,
    validate_supported_base,
    validate_ternary_operand,
)


@dataclass(frozen=True, slots=True)
class _MultiplicationRows:
    """Internal container for partial-row multiplication output."""

    partial_rows: list[str]
    carry_records: list[CarryRecord]
    steps: list[ExplanationStep]


def multiply_numbers(
    left: str,
    right: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> ArithmeticResult:
    """Return the structured result for multiplying two number strings.

    Args:
        left: The left operand.
        right: The right operand.
        base: The number base used by the operation.
        explanation_mode: Whether to generate beginner-friendly steps.

    Returns:
        Structured multiplication result and educational metadata.

    Raises:
        InvalidBaseError: If ``base`` is unsupported.
        InvalidNumberError: If either operand is malformed.
    """
    left_operand, right_operand = _validate_multiplication_operands(left, right, base)

    if left_operand == "0" or right_operand == "0":
        return _zero_multiplication_result(
            left_operand,
            right_operand,
            explanation_mode=explanation_mode,
        )

    rows = _build_partial_rows(
        left_operand,
        right_operand,
        base=base,
        explanation_mode=explanation_mode,
    )

    addition_result = add_many(
        rows.partial_rows,
        base=base,
        explanation_mode=explanation_mode,
    )
    carry_records = [
        *rows.carry_records,
        *addition_result.metadata["carry_records"],
    ]
    steps = _build_multiplication_steps(
        left_operand,
        right_operand,
        rows,
        addition_result,
        explanation_mode=explanation_mode,
    )

    return ArithmeticResult(
        result=addition_result.result,
        carries=[record.value for record in carry_records],
        borrows=[],
        steps=steps,
        metadata={
            "partial_rows": rows.partial_rows,
            "carry_records": carry_records,
        },
    )


def multiply_by_trit(
    multiplicand: str,
    multiplier_digit: str,
    *,
    shift: int = 0,
    base: int = 3,
    explanation_mode: bool = False,
) -> tuple[str, list[CarryRecord], list[ExplanationStep]]:
    """Multiply a validated ternary number by one trit and shift the row.

    Args:
        multiplicand: Validated non-negative ordinary ternary number.
        multiplier_digit: Single ordinary ternary digit.
        shift: Number of zero trits to append for place value.
        base: Arithmetic base.
        explanation_mode: Whether to emit educational steps.

    Returns:
        Partial product, carry records, and explanation steps.
    """
    multiplier = trit_to_int(multiplier_digit)
    result_digits, carry_records, steps, carry = _multiply_trit_columns(
        multiplicand,
        multiplier_digit,
        multiplier,
        shift=shift,
        base=base,
        explanation_mode=explanation_mode,
    )
    _append_remaining_carry(result_digits, carry, base=base)

    partial_product = _shift_partial_product(result_digits, shift)

    if explanation_mode and shift:
        steps.append(_create_shift_step(partial_product, shift))

    return partial_product, carry_records, steps


def _validate_multiplication_operands(
    left: str,
    right: str,
    base: int,
) -> tuple[str, str]:
    """Validate multiplication inputs and return normalized operands."""
    validate_supported_base(base)
    return (
        validate_ternary_operand(left, field_name="Left operand"),
        validate_ternary_operand(right, field_name="Right operand"),
    )


def _zero_multiplication_result(
    left_operand: str,
    right_operand: str,
    *,
    explanation_mode: bool,
) -> ArithmeticResult:
    """Build the multiplication result for any zero operand case."""
    steps = []
    if explanation_mode:
        steps.append(
            create_step(
                "Setup",
                align_arithmetic_expression(left_operand, right_operand, "x", "0"),
                "Any number multiplied by 0 is 0.",
            )
        )

    return ArithmeticResult(
        result="0",
        steps=steps,
        metadata={"partial_rows": ["0"], "carry_records": []},
    )


def _build_partial_rows(
    left_operand: str,
    right_operand: str,
    *,
    base: int,
    explanation_mode: bool,
) -> _MultiplicationRows:
    """Create all shifted partial rows for long multiplication."""
    partial_rows = []
    carry_records: list[CarryRecord] = []
    steps: list[ExplanationStep] = []

    for position, multiplier_digit in enumerate(iter_digits_from_right(right_operand)):
        partial_product, row_carries, row_steps = multiply_by_trit(
            left_operand,
            multiplier_digit,
            shift=position,
            base=base,
            explanation_mode=explanation_mode,
        )
        partial_rows.append(partial_product)
        carry_records.extend(row_carries)
        steps.extend(row_steps)

    return _MultiplicationRows(partial_rows, carry_records, steps)


def _build_multiplication_steps(
    left_operand: str,
    right_operand: str,
    rows: _MultiplicationRows,
    addition_result: ArithmeticResult,
    *,
    explanation_mode: bool,
) -> list[ExplanationStep]:
    """Build the ordered educational steps for multiplication."""
    if not explanation_mode:
        return []

    steps = [
        create_step(
            "Setup",
            align_arithmetic_expression(left_operand, right_operand, "x"),
            (
                "Multiply each trit in the bottom number by the top number, "
                "then add the shifted rows."
            ),
        )
    ]
    steps.extend(rows.steps)
    steps.append(
        create_step(
            "Add Partial Rows",
            "\n".join(rows.partial_rows),
            f"Add the partial rows to get {addition_result.result}.",
        )
    )
    steps.extend(addition_result.steps)
    return steps


def _multiply_trit_columns(
    multiplicand: str,
    multiplier_digit: str,
    multiplier: int,
    *,
    shift: int,
    base: int,
    explanation_mode: bool,
) -> tuple[list[str], list[CarryRecord], list[ExplanationStep], int]:
    """Multiply each multiplicand column by one trit."""
    carry = 0
    result_digits = []
    carry_records = []
    steps = []

    for position, digit in enumerate(iter_digits_from_right(multiplicand)):
        operand = trit_to_int(digit)
        column_total = (operand * multiplier) + carry
        written_digit, carry_out = calculate_carry(column_total, base=base)

        result_digits.append(written_digit)

        if carry_out:
            carry_records.append(
                create_carry(
                    position + shift,
                    carry_out,
                    source=f"{digit} x {multiplier_digit} with carry {carry}",
                )
            )

        if explanation_mode:
            steps.append(
                create_step(
                    f"Partial Row {shift + 1}, Column {position + 1}",
                    describe_carry(
                        position,
                        [operand * multiplier],
                        carry,
                        written_digit,
                        carry_out,
                        base=base,
                    ),
                    f"Multiply {digit} by {multiplier_digit}, write {written_digit}, and carry {carry_out}.",
                )
            )

        carry = carry_out

    return result_digits, carry_records, steps, carry


def _append_remaining_carry(
    result_digits: list[str],
    carry: int,
    *,
    base: int,
) -> None:
    """Append carry digits left after column multiplication."""
    while carry:
        written_digit, carry = calculate_carry(carry, base=base)
        result_digits.append(written_digit)


def _shift_partial_product(result_digits: list[str], shift: int) -> str:
    """Reverse result digits, strip leading zeroes, and apply place shift."""
    partial_product = strip_leading_zeros("".join(reversed(result_digits)))

    if partial_product != "0":
        partial_product += "0" * shift

    return partial_product


def _create_shift_step(partial_product: str, shift: int) -> ExplanationStep:
    """Create the place-shift explanation for one partial row."""
    return create_step(
        f"Shift Partial Row {shift + 1}",
        partial_product,
        (
            f"Append {shift} zero trit(s) because this multiplier digit is "
            f"{shift} place(s) from the right."
        ),
    )
