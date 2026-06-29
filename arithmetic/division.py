"""Ordinary ternary long division with structured explanations."""

from __future__ import annotations

from dataclasses import dataclass, field

from exceptions import DivisionByZeroError

from .borrow import BorrowRecord
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


@dataclass(slots=True)
class _DivisionAccumulator:
    """Internal state accumulated during long division."""

    quotient_digits: list[str] = field(default_factory=list)
    remainder: str = "0"
    intermediate_rows: list[dict[str, str | int]] = field(default_factory=list)
    borrow_values: list[int] = field(default_factory=list)
    borrow_records: list[BorrowRecord] = field(default_factory=list)
    steps: list[ExplanationStep] = field(default_factory=list)


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

    Returns:
        Structured quotient, remainder, borrow data, and optional explanations.

    Raises:
        InvalidBaseError: If ``base`` is unsupported.
        InvalidNumberError: If either operand is malformed.
        DivisionByZeroError: If the divisor is zero.
    """
    dividend_operand, divisor_operand = _validate_division_operands(
        dividend,
        divisor,
        base,
    )

    if dividend_operand == "0":
        return _zero_dividend_result(divisor_operand, explanation_mode=explanation_mode)

    accumulator = _DivisionAccumulator(
        steps=_initial_division_steps(
            dividend_operand,
            divisor_operand,
            explanation_mode=explanation_mode,
        )
    )
    for position, digit in enumerate(dividend_operand, start=1):
        _process_dividend_digit(
            accumulator,
            position,
            digit,
            divisor_operand,
            base=base,
            explanation_mode=explanation_mode,
        )

    return _build_division_result(accumulator, explanation_mode=explanation_mode)


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


def _validate_division_operands(
    dividend: str,
    divisor: str,
    base: int,
) -> tuple[str, str]:
    """Validate division inputs and return normalized operands."""
    validate_supported_base(base)
    dividend_operand = validate_ternary_operand(dividend, field_name="Dividend")
    divisor_operand = validate_ternary_operand(divisor, field_name="Divisor")

    if divisor_operand == "0":
        raise DivisionByZeroError("Cannot divide by zero.")

    return dividend_operand, divisor_operand


def _zero_dividend_result(
    divisor_operand: str,
    *,
    explanation_mode: bool,
) -> ArithmeticResult:
    """Build the result for zero divided by a non-zero divisor."""
    steps = []
    if explanation_mode:
        steps.append(
            create_step(
                "Setup",
                "0 / " + divisor_operand,
                (
                    "Zero divided by any non-zero number gives quotient 0 "
                    "and remainder 0."
                ),
            )
        )

    return ArithmeticResult(
        result="0",
        steps=steps,
        metadata={"quotient": "0", "remainder": "0", "intermediate_rows": []},
    )


def _initial_division_steps(
    dividend_operand: str,
    divisor_operand: str,
    *,
    explanation_mode: bool,
) -> list[ExplanationStep]:
    """Create setup steps for long division."""
    if not explanation_mode:
        return []

    return [
        create_step(
            "Setup",
            align_arithmetic_expression(dividend_operand, divisor_operand, "/"),
            (
                "Divide from left to right. Bring down one trit, choose a "
                "quotient trit, multiply, then subtract."
            ),
        )
    ]


def _process_dividend_digit(
    accumulator: _DivisionAccumulator,
    position: int,
    digit: str,
    divisor_operand: str,
    *,
    base: int,
    explanation_mode: bool,
) -> None:
    """Process one dividend digit in the long-division algorithm."""
    current = bring_down(accumulator.remainder, digit)
    quotient_digit, product = choose_quotient_digit(
        current,
        divisor_operand,
        base=base,
    )
    subtraction_result, new_remainder = _subtract_product(
        current,
        product,
        base=base,
        explanation_mode=explanation_mode,
    )

    accumulator.quotient_digits.append(quotient_digit)
    accumulator.borrow_values.extend(subtraction_result.borrows)
    accumulator.borrow_records.extend(
        subtraction_result.metadata.get("borrow_records", [])
    )
    accumulator.intermediate_rows.append(
        {
            "position": position,
            "brought_down": digit,
            "current": current,
            "quotient_digit": quotient_digit,
            "product": product,
            "remainder": new_remainder,
        }
    )
    _append_division_step(
        accumulator,
        position,
        digit,
        current,
        divisor_operand,
        quotient_digit,
        product,
        new_remainder,
        subtraction_result,
        explanation_mode=explanation_mode,
    )
    accumulator.remainder = new_remainder


def _subtract_product(
    current: str,
    product: str,
    *,
    base: int,
    explanation_mode: bool,
) -> tuple[ArithmeticResult, str]:
    """Subtract a quotient-digit product from the current remainder."""
    if product == "0":
        return ArithmeticResult(result=current), current

    subtraction_result = subtract_numbers(
        current,
        product,
        base=base,
        explanation_mode=explanation_mode,
    )
    return subtraction_result, subtraction_result.result


def _append_division_step(
    accumulator: _DivisionAccumulator,
    position: int,
    digit: str,
    current: str,
    divisor_operand: str,
    quotient_digit: str,
    product: str,
    new_remainder: str,
    subtraction_result: ArithmeticResult,
    *,
    explanation_mode: bool,
) -> None:
    """Append educational explanation for one division row."""
    if not explanation_mode:
        return

    accumulator.steps.append(
        create_step(
            f"Division Step {position}",
            (
                f"Bring down {digit}: {current}\n"
                f"{divisor_operand} x {quotient_digit} = {product}\n"
                f"{current} - {product} = {new_remainder}"
            ),
            (
                "Use the largest ternary digit that does not make the product "
                "bigger than the current value."
            ),
        )
    )
    accumulator.steps.extend(subtraction_result.steps)


def _build_division_result(
    accumulator: _DivisionAccumulator,
    *,
    explanation_mode: bool,
) -> ArithmeticResult:
    """Build the public division result payload."""
    quotient = strip_leading_zeros("".join(accumulator.quotient_digits))

    if explanation_mode:
        accumulator.steps.append(
            create_step(
                "Result",
                f"Quotient {quotient}, Remainder {accumulator.remainder}",
                (
                    "The quotient is built from the digits chosen at each step. "
                    "The final leftover value is the remainder."
                ),
            )
        )

    return ArithmeticResult(
        result=quotient,
        carries=[],
        borrows=accumulator.borrow_values,
        steps=accumulator.steps,
        metadata={
            "quotient": quotient,
            "remainder": accumulator.remainder,
            "intermediate_rows": accumulator.intermediate_rows,
            "borrow_records": accumulator.borrow_records,
        },
    )
