"""Ordinary ternary long division with structured explanations."""

from __future__ import annotations

from .explanation import ArithmeticResult, ExplanationStep, create_step
from .formatter import align_arithmetic_expression
from .multiplication import multiply_by_trit
from .subtraction import subtract_numbers
from .utils import (
    compare_magnitudes,
    strip_leading_zeros,
    validate_supported_base,
    validate_ternary_operand,
)

def divide_numbers(
    dividend: str,
    divisor: str,
    *,
    base: int = 3,
    explanation_mode: bool = False,
) -> ArithmeticResult:
    """Return the structured result for dividing two number strings.

    Args:
        dividend: The number being divided.
        divisor: The number used as the divisor.
        base: The number base used by the operation.
        explanation_mode: Whether to generate beginner-friendly steps.
    """
    validate_supported_base(base)
    dividend_operand = validate_ternary_operand(dividend, field_name="Dividend")
    divisor_operand = validate_ternary_operand(divisor, field_name="Divisor")

    if divisor_operand == "0":
        raise ValueError("Cannot divide by zero.")

    if dividend_operand == "0":
        steps = []
        if explanation_mode:
            steps.append(
                create_step(
                    "Setup",
                    "0 / " + divisor_operand,
                    "Zero divided by any non-zero number gives quotient 0 and remainder 0.",
                )
            )
        return ArithmeticResult(
            result="0",
            steps=steps,
            metadata={"quotient": "0", "remainder": "0", "intermediate_rows": []},
        )

    quotient_digits = []
    remainder = "0"
    intermediate_rows = []
    borrow_values = []
    borrow_records = []
    steps: list[ExplanationStep] = []

    if explanation_mode:
        steps.append(
            create_step(
                "Setup",
                align_arithmetic_expression(dividend_operand, divisor_operand, "/"),
                "Divide from left to right. Bring down one trit, choose a quotient trit, multiply, then subtract.",
            )
        )

    for position, digit in enumerate(dividend_operand, start=1):
        remainder = bring_down(remainder, digit)
        quotient_digit, product = choose_quotient_digit(
            remainder,
            divisor_operand,
            base=base,
        )
        quotient_digits.append(quotient_digit)

        if product == "0":
            new_remainder = remainder
            subtraction_result = ArithmeticResult(result=remainder)
        else:
            subtraction_result = subtract_numbers(
                remainder,
                product,
                base=base,
                explanation_mode=explanation_mode,
            )
            new_remainder = subtraction_result.result
            borrow_values.extend(subtraction_result.borrows)
            borrow_records.extend(subtraction_result.metadata["borrow_records"])

        row = {
            "position": position,
            "brought_down": digit,
            "current": remainder,
            "quotient_digit": quotient_digit,
            "product": product,
            "remainder": new_remainder,
        }
        intermediate_rows.append(row)

        if explanation_mode:
            steps.append(
                create_step(
                    f"Division Step {position}",
                    (
                        f"Bring down {digit}: {remainder}\n"
                        f"{divisor_operand} x {quotient_digit} = {product}\n"
                        f"{remainder} - {product} = {new_remainder}"
                    ),
                    "Use the largest ternary digit that does not make the product bigger than the current value.",
                )
            )
            steps.extend(subtraction_result.steps)

        remainder = new_remainder

    quotient = strip_leading_zeros("".join(quotient_digits))

    if explanation_mode:
        steps.append(
            create_step(
                "Result",
                f"Quotient {quotient}, Remainder {remainder}",
                "The quotient is built from the digits chosen at each step. The final leftover value is the remainder.",
            )
        )

    return ArithmeticResult(
        result=quotient,
        carries=[],
        borrows=borrow_values,
        steps=steps,
        metadata={
            "quotient": quotient,
            "remainder": remainder,
            "intermediate_rows": intermediate_rows,
            "borrow_records": borrow_records,
        },
    )


def bring_down(remainder: str, digit: str) -> str:
    """Append one dividend digit to the current long-division remainder."""
    if remainder == "0":
        return strip_leading_zeros(digit)

    return strip_leading_zeros(remainder + digit)


def choose_quotient_digit(
    current: str,
    divisor: str,
    *,
    base: int = 3,
) -> tuple[str, str]:
    """Choose the largest quotient trit whose product fits current."""
    for candidate in range(base - 1, -1, -1):
        product, _carries, _steps = multiply_by_trit(
            divisor,
            str(candidate),
            base=base,
        )

        if compare_magnitudes(product, current) <= 0:
            return str(candidate), product

    return "0", "0"
