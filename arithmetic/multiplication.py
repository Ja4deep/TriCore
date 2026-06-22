"""Ordinary ternary long multiplication with structured explanations."""

from __future__ import annotations

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
    """
    validate_supported_base(base)
    left_operand = validate_ternary_operand(left, field_name="Left operand")
    right_operand = validate_ternary_operand(right, field_name="Right operand")

    if left_operand == "0" or right_operand == "0":
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

    partial_rows = []
    carry_records: list[CarryRecord] = []
    steps: list[ExplanationStep] = []

    if explanation_mode:
        steps.append(
            create_step(
                "Setup",
                align_arithmetic_expression(left_operand, right_operand, "x"),
                "Multiply each trit in the bottom number by the top number, then add the shifted rows.",
            )
        )

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

    addition_result = add_many(
        partial_rows,
        base=base,
        explanation_mode=explanation_mode,
    )
    result = addition_result.result
    carry_records.extend(addition_result.metadata["carry_records"])

    if explanation_mode:
        steps.append(
            create_step(
                "Add Partial Rows",
                "\n".join(partial_rows),
                f"Add the partial rows to get {result}.",
            )
        )
        steps.extend(addition_result.steps)

    return ArithmeticResult(
        result=result,
        carries=[record.value for record in carry_records],
        borrows=[],
        steps=steps,
        metadata={
            "partial_rows": partial_rows,
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
    """Multiply a validated ternary number by one trit and shift the row."""
    multiplier = trit_to_int(multiplier_digit)
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

    while carry:
        written_digit, carry = calculate_carry(carry, base=base)
        result_digits.append(written_digit)

    partial_product = strip_leading_zeros("".join(reversed(result_digits)))

    if partial_product != "0":
        partial_product += "0" * shift

    if explanation_mode and shift:
        steps.append(
            create_step(
                f"Shift Partial Row {shift + 1}",
                partial_product,
                f"Append {shift} zero trit(s) because this multiplier digit is {shift} place(s) from the right.",
            )
        )

    return partial_product, carry_records, steps
