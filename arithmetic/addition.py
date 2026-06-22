"""Ordinary ternary addition with structured explanations."""

from __future__ import annotations

from typing import Sequence

from .carry import CarryRecord, calculate_carry, create_carry, describe_carry
from .explanation import ArithmeticResult, ExplanationStep, create_step
from .formatter import align_arithmetic_expression
from .utils import (
    align_numbers,
    iter_digits_from_right,
    strip_leading_zeros,
    trit_to_int,
    validate_supported_base,
    validate_ternary_operand,
)


def add_numbers(
    left: str,
    right: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> ArithmeticResult:
    """Return the structured result for adding two number strings.

    Args:
        left: The left operand.
        right: The right operand.
        base: The number base used by the operation.
        explanation_mode: Whether to generate beginner-friendly steps.
    """
    validate_supported_base(base)
    left_operand = validate_ternary_operand(left, field_name="Left operand")
    right_operand = validate_ternary_operand(right, field_name="Right operand")

    result, carry_records, steps = add_unsigned(
        left_operand,
        right_operand,
        base=base,
        explanation_mode=explanation_mode,
    )

    if explanation_mode:
        steps.insert(
            0,
            create_step(
                "Setup",
                align_arithmetic_expression(left_operand, right_operand, "+", result),
                "Line up the ternary numbers by place value and add from right to left.",
            ),
        )

    return ArithmeticResult(
        result=result,
        carries=[record.value for record in carry_records],
        borrows=[],
        steps=steps,
        metadata={"carry_records": carry_records},
    )


def add_many(
    operands: Sequence[str],
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> ArithmeticResult:
    """Return the structured result for adding several ternary operands."""
    validate_supported_base(base)

    if not operands:
        raise ValueError("At least one operand is required.")

    running_total = "0"
    all_steps: list[ExplanationStep] = []
    all_carry_records: list[CarryRecord] = []

    for index, operand in enumerate(operands, start=1):
        validated_operand = validate_ternary_operand(
            operand,
            field_name=f"Operand {index}",
        )
        partial = add_numbers(
            running_total,
            validated_operand,
            base=base,
            explanation_mode=explanation_mode,
        )
        running_total = partial.result
        all_steps.extend(partial.steps)
        all_carry_records.extend(partial.metadata["carry_records"])

    return ArithmeticResult(
        result=running_total,
        carries=[record.value for record in all_carry_records],
        borrows=[],
        steps=all_steps,
        metadata={"carry_records": all_carry_records},
    )


def add_unsigned(
    left: str,
    right: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> tuple[str, list[CarryRecord], list[ExplanationStep]]:
    """Add two validated non-negative ternary numbers."""
    left_aligned, right_aligned = align_numbers(left, right)
    carry = 0
    result_digits = []
    carry_records = []
    steps = []

    for position, (left_digit, right_digit) in enumerate(
        zip(iter_digits_from_right(left_aligned), iter_digits_from_right(right_aligned))
    ):
        operands = [trit_to_int(left_digit), trit_to_int(right_digit)]
        column_total = sum(operands) + carry
        written_digit, carry_out = calculate_carry(column_total, base=base)

        result_digits.append(written_digit)

        if carry_out:
            carry_records.append(
                create_carry(
                    position,
                    carry_out,
                    source=f"{left_digit} + {right_digit} with carry {carry}",
                )
            )

        if explanation_mode:
            steps.append(
                create_step(
                    f"Column {position + 1}",
                    describe_carry(
                        position,
                        operands,
                        carry,
                        written_digit,
                        carry_out,
                        base=base,
                    ),
                    "Move one column to the left and include the carry there.",
                )
            )

        carry = carry_out

    if carry:
        result_digits.append(str(carry))
        if explanation_mode:
            steps.append(
                create_step(
                    "Final Carry",
                    f"Carry {carry}",
                    "No columns remain, so write the final carry at the front.",
                )
            )

    result = strip_leading_zeros("".join(reversed(result_digits)))
    return result, carry_records, steps
