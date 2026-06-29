"""Ordinary ternary subtraction with structured explanations."""

from __future__ import annotations

from dataclasses import dataclass

from exceptions import InvalidNumberError

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


@dataclass(frozen=True, slots=True)
class _SubtractionOperands:
    """Internal operand arrangement for signed subtraction."""

    left: str
    right: str
    minuend: str
    subtrahend: str
    negative_result: bool


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

    Returns:
        Structured subtraction result and educational metadata.

    Raises:
        InvalidBaseError: If ``base`` is unsupported.
        InvalidNumberError: If either operand is malformed.
    """
    validate_supported_base(base)
    left_operand = validate_ternary_operand(left, field_name="Left operand")
    right_operand = validate_ternary_operand(right, field_name="Right operand")
    comparison = compare_magnitudes(left_operand, right_operand)

    if comparison == 0:
        return _equal_operands_result(
            left_operand,
            right_operand,
            explanation_mode=explanation_mode,
        )

    operands = _arrange_subtraction_operands(left_operand, right_operand, comparison)
    result, borrow_records, steps = subtract_unsigned(
        operands.minuend,
        operands.subtrahend,
        base=base,
        explanation_mode=explanation_mode,
    )

    if operands.negative_result:
        result = "-" + result

    _prepend_subtraction_setup_step(
        steps,
        operands,
        result,
        explanation_mode=explanation_mode,
    )

    return _build_subtraction_result(
        result,
        borrow_records,
        steps,
        negative_result=operands.negative_result,
    )


def _equal_operands_result(
    left_operand: str,
    right_operand: str,
    *,
    explanation_mode: bool,
) -> ArithmeticResult:
    """Build the subtraction result for equal operands."""
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


def _arrange_subtraction_operands(
    left_operand: str,
    right_operand: str,
    comparison: int,
) -> _SubtractionOperands:
    """Choose minuend and subtrahend while preserving result sign."""
    negative_result = comparison < 0
    return _SubtractionOperands(
        left=left_operand,
        right=right_operand,
        minuend=right_operand if negative_result else left_operand,
        subtrahend=left_operand if negative_result else right_operand,
        negative_result=negative_result,
    )


def _prepend_subtraction_setup_step(
    steps: list[ExplanationStep],
    operands: _SubtractionOperands,
    result: str,
    *,
    explanation_mode: bool,
) -> None:
    """Add the leading educational setup step for subtraction."""
    if not explanation_mode:
        return

    setup_explanation = (
        "The right operand is larger, so subtract the smaller magnitude first "
        "and mark the final answer as negative."
        if operands.negative_result
        else "Line up the ternary numbers by place value and subtract from right to left."
    )
    steps.insert(
        0,
        create_step(
            "Setup",
            align_arithmetic_expression(operands.left, operands.right, "-", result),
            setup_explanation,
        ),
    )


def _build_subtraction_result(
    result: str,
    borrow_records: list[BorrowRecord],
    steps: list[ExplanationStep],
    *,
    negative_result: bool,
) -> ArithmeticResult:
    """Build the public subtraction result payload."""
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
    """Subtract two validated non-negative ternary numbers where left >= right.

    Args:
        left: Validated minuend.
        right: Validated subtrahend.
        base: Arithmetic base.
        explanation_mode: Whether to emit educational column steps.

    Returns:
        Difference, borrow records, and explanation steps.

    Raises:
        InvalidNumberError: If ``left`` is smaller than ``right``.
    """
    if compare_magnitudes(left, right) < 0:
        raise InvalidNumberError(
            "Unsigned subtraction requires left to be greater than right."
        )

    left_aligned, right_aligned = align_numbers(left, right)
    borrow = 0
    result_digits = []
    borrow_records = []
    steps = []

    for position, (left_digit, right_digit) in enumerate(
        zip(
            iter_digits_from_right(left_aligned),
            iter_digits_from_right(right_aligned),
            strict=True,
        )
    ):
        written_digit, borrow_out, step = _subtract_column(
            position,
            left_digit,
            right_digit,
            borrow,
            base=base,
            explanation_mode=explanation_mode,
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

        if step is not None:
            steps.append(step)

        borrow = borrow_out

    result = strip_leading_zeros("".join(reversed(result_digits)))
    return result, borrow_records, steps


def _subtract_column(
    position: int,
    left_digit: str,
    right_digit: str,
    borrow: int,
    *,
    base: int,
    explanation_mode: bool,
) -> tuple[str, int, ExplanationStep | None]:
    """Subtract one aligned column and optionally create an explanation step."""
    top_digit = trit_to_int(left_digit)
    bottom_digit = trit_to_int(right_digit)
    written_digit, borrow_out, _adjusted_top = calculate_borrow(
        top_digit,
        bottom_digit,
        borrow,
        base=base,
    )
    step = None

    if explanation_mode:
        step = create_step(
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

    return written_digit, borrow_out, step
