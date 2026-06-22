"""Ordinary ternary subtraction with structured explanations."""

from __future__ import annotations

from .borrow import BorrowRecord, calculate_borrow, create_borrow, describe_borrow
from .explanation import ArithmeticResult, ExplanationStep, create_step
from .formatter import align_arithmetic_expression
from .utils import (
    align_numbers,
    compare_magnitudes,
    iter_digits_from_right,
    strip_leading_zeros,
    trit_to_int,
    validate_supported_base,
    validate_ternary_operand,
)

def subtract_numbers(
    left: str,
    right: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> ArithmeticResult:
    """Return the structured result for subtracting two number strings.

    Args:
        left: The left operand.
        right: The right operand.
        base: The number base used by the operation.
        explanation_mode: Whether to generate beginner-friendly steps.
    """
    validate_supported_base(base)
    left_operand = validate_ternary_operand(left, field_name="Left operand")
    right_operand = validate_ternary_operand(right, field_name="Right operand")
    comparison = compare_magnitudes(left_operand, right_operand)

    if comparison == 0:
        steps = []
        if explanation_mode:
            steps.append(
                create_step(
                    "Setup",
                    align_arithmetic_expression(left_operand, right_operand, "-", "0"),
                    "Both operands have the same value, so the difference is 0.",
                )
            )
        return ArithmeticResult(result="0", steps=steps, metadata={"borrow_records": []})

    negative_result = comparison < 0
    minuend = right_operand if negative_result else left_operand
    subtrahend = left_operand if negative_result else right_operand

    result, borrow_records, steps = subtract_unsigned(
        minuend,
        subtrahend,
        base=base,
        explanation_mode=explanation_mode,
    )

    if negative_result:
        result = "-" + result

    if explanation_mode:
        setup_explanation = (
            "The right operand is larger, so subtract the smaller magnitude first "
            "and mark the final answer as negative."
            if negative_result
            else "Line up the ternary numbers by place value and subtract from right to left."
        )
        steps.insert(
            0,
            create_step(
                "Setup",
                align_arithmetic_expression(left_operand, right_operand, "-", result),
                setup_explanation,
            ),
        )

    return ArithmeticResult(
        result=result,
        carries=[],
        borrows=[record.value for record in borrow_records],
        steps=steps,
        metadata={
            "borrow_records": borrow_records,
            "negative_result": negative_result,
        },
    )


def subtract_unsigned(
    left: str,
    right: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> tuple[str, list[BorrowRecord], list[ExplanationStep]]:
    """Subtract two validated non-negative ternary numbers where left >= right."""
    if compare_magnitudes(left, right) < 0:
        raise ValueError("Unsigned subtraction requires left to be greater than right.")

    left_aligned, right_aligned = align_numbers(left, right)
    borrow = 0
    result_digits = []
    borrow_records = []
    steps = []

    for position, (left_digit, right_digit) in enumerate(
        zip(iter_digits_from_right(left_aligned), iter_digits_from_right(right_aligned))
    ):
        top_digit = trit_to_int(left_digit)
        bottom_digit = trit_to_int(right_digit)
        written_digit, borrow_out, _adjusted_top = calculate_borrow(
            top_digit,
            bottom_digit,
            borrow,
            base=base,
        )

        result_digits.append(written_digit)

        if borrow_out:
            borrow_records.append(
                create_borrow(
                    position,
                    borrow_out,
                    source=f"{left_digit} - {right_digit} with borrow {borrow}",
                )
            )

        if explanation_mode:
            steps.append(
                create_step(
                    f"Column {position + 1}",
                    describe_borrow(
                        position,
                        top_digit,
                        bottom_digit,
                        borrow,
                        written_digit,
                        borrow_out,
                        base=base,
                    ),
                    "Move one column to the left and account for any borrowed trit.",
                )
            )

        borrow = borrow_out

    result = strip_leading_zeros("".join(reversed(result_digits)))
    return result, borrow_records, steps
