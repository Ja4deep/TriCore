"""Educational decimal-to-ordinary-ternary conversion helpers."""

from arithmetic.utils import clean_input
from ui.terminal import (
    error_screen,
    explanation_screen,
    input_screen,
    key_value_lines,
    print_screen,
    prompt,
    result_screen,
)


def decimal_to_ternary(n: int) -> str:
    """Convert a decimal integer to ordinary ternary.

    Args:
        n: The decimal integer to convert.

    Returns:
        The base-3 representation using digits 0, 1, and 2.
    """

    # Handle the special case where the input is 0
    if n == 0:
        return "0"

    if n < 0:
        return "-" + decimal_to_ternary(-n)

    # Store ternary digits as they are generated
    digits = []

    # Repeatedly divide by 3 because ternary is a base-3 number system
    while n > 0:
        # The remainder becomes the next ternary digit
        digits.append(str(n % 3))

        # Move to the next digit position
        n //= 3

    # Digits are generated in reverse order, so reverse them
    return "".join(reversed(digits))


def get_decimal_input() -> int:
    """Ask for a decimal integer until the input is valid."""
    while True:
        print_screen(
            input_screen(
                "Input",
                "Enter a decimal number",
                "Whole numbers are supported, including negatives.",
            )
        )
        raw_input_value = clean_input(prompt("Enter a decimal number"))

        try:
            return int(raw_input_value)
        except ValueError:
            print_screen(error_screen("Please enter a whole number, such as 8 or -11."))


def display_header() -> None:
    """Display the ordinary ternary converter title."""
    print_screen(
        explanation_screen(
            "Decimal to Ordinary Ternary",
            ["Convert a decimal integer into base 3."],
        )
    )


def explain_conversion() -> None:
    """Print the idea behind ordinary ternary conversion."""
    print_screen(
        explanation_screen(
            "How Ordinary Ternary Works",
            [
                "Ternary is base 3, so every place is a power of 3.",
                "The allowed digits are 0, 1, and 2.",
                "Repeated division by 3 gives the digits from right to left.",
            ],
        )
    )


def get_conversion_steps(number: int) -> list[tuple[int, int, int]]:
    """Return division steps for decimal to ternary conversion.

    Args:
        number: The decimal integer to trace.

    Returns:
        Tuples in the form (current_number, quotient, remainder).
    """
    number = abs(number)

    if number == 0:
        return [(0, 0, 0)]

    steps = []

    while number > 0:
        quotient = number // 3
        remainder = number % 3
        steps.append((number, quotient, remainder))
        number = quotient

    return steps


def display_step_by_step_conversion(number: int) -> None:
    """Display every division step used to produce ternary digits."""
    lines = []

    if number < 0:
        lines.extend(
            [
                f"Convert the magnitude {abs(number)} first.",
                "Then add the minus sign to the final ternary value.",
                "",
            ]
        )

    for current_number, quotient, remainder in get_conversion_steps(number):
        lines.append(f"{current_number} / 3 = {quotient} remainder {remainder}")
        lines.append(f"Write {remainder}")
        lines.append("")

    print_screen(explanation_screen("Step-by-Step Conversion", lines))


def ternary_to_decimal_value(ternary: str) -> int:
    """Evaluate an ordinary ternary string as decimal."""
    sign = -1 if ternary.startswith("-") else 1
    digits = ternary.lstrip("-")
    total = 0

    for power, digit in enumerate(reversed(digits)):
        total += int(digit) * (3**power)

    return sign * total


def verify_conversion(number: int, ternary: str) -> str:
    """Build a mathematical verification for a ternary result."""
    sign = -1 if ternary.startswith("-") else 1
    digits = ternary.lstrip("-")
    highest_power = len(digits) - 1
    evaluated_terms = []
    lines = ["Verification", ""]

    for index, digit in enumerate(digits):
        power = highest_power - index
        place_value = 3**power
        contribution = int(digit) * place_value
        evaluated_terms.append(contribution)
        lines.append(f"({digit} x {place_value}) = {contribution}")

    total = sum(evaluated_terms) * sign
    expression = " + ".join(str(value) for value in evaluated_terms)

    if sign == -1:
        lines.append("")
        lines.append(f"-({expression}) = {total}")
    else:
        lines.append("")
        lines.append(f"{expression} = {total}")

    if total == number:
        lines.append("[OK] Verification Successful")
    else:
        lines.append("[X] Verification Failed")

    return "\n".join(lines)


def display_results(number: int) -> None:
    """Display ternary output with steps and verification."""
    ternary = decimal_to_ternary(number)

    print_screen(
        result_screen(
            "Conversion Result",
            key_value_lines(
                [
                    ("Decimal Number", number),
                    ("Ordinary Ternary", ternary),
                ]
            ),
        )
    )

    display_step_by_step_conversion(number)

    print_screen(
        explanation_screen(
            "Verification", verify_conversion(number, ternary).splitlines()
        )
    )

    print_screen(
        explanation_screen(
            "Learning Summary",
            [
                "Decimal to ternary uses repeated division by 3.",
                "The remainders form the ternary answer from right to left.",
            ],
        )
    )


def main() -> None:
    """Run the educational ordinary ternary converter."""
    display_header()
    explain_conversion()
    display_results(get_decimal_input())


if __name__ == "__main__":
    main()
