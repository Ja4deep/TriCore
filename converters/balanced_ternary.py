import sys

try:
    from converters.decimal_to_ternary import decimal_to_ternary
except ModuleNotFoundError:
    from decimal_to_ternary import decimal_to_ternary

from ui.terminal import (
    error_screen,
    explanation_screen,
    input_screen,
    key_value_lines,
    menu_screen,
    print_screen,
    prompt,
    result_screen,
    success_message,
    table_lines,
)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


BALANCED_DIGIT_VALUES = {
    "T": -1,
    "0": 0,
    "1": 1,
}

def display_header() -> None:
    """Display the balanced ternary module title."""
    print_screen(
        explanation_screen(
            "Balanced Ternary Converter",
            ["Study base 3 with digit values -1, 0, and +1."],
        )
    )


def clean_input(raw_input_value: str) -> str:
    """Return user input with whitespace and hidden BOM characters removed."""
    return raw_input_value.strip().replace("\ufeff", "").replace("\xef\xbb\xbf", "")


def get_decimal_input() -> int:
    """Ask the user for a decimal integer until the input is valid."""
    while True:
        print_screen(
            input_screen(
                "Input",
                "Enter a decimal integer",
                "Whole numbers are supported, including negatives.",
            )
        )
        raw_input_value = clean_input(prompt("Enter a decimal integer"))

        try:
            return int(raw_input_value)
        except ValueError:
            print_screen(error_screen("Please enter a whole number, such as 8 or -11."))


def validate_balanced_ternary(balanced_ternary: str) -> str:
    """Validate and normalize a balanced ternary string.

    Args:
        balanced_ternary: Text entered by the user.

    Returns:
        The normalized uppercase balanced ternary string.

    Raises:
        ValueError: If the input is empty or contains characters other than
            T, 0, and 1.
    """
    normalized_value = clean_input(balanced_ternary).upper()

    if not normalized_value:
        raise ValueError("Balanced ternary input cannot be empty.")

    invalid_digits = [
        digit for digit in normalized_value if digit not in BALANCED_DIGIT_VALUES
    ]
    if invalid_digits:
        raise ValueError("Balanced ternary can only contain T, 0, and 1.")

    return normalized_value


def get_balanced_ternary_input() -> str:
    """Ask the user for balanced ternary until the input is valid."""
    while True:
        print_screen(
            input_screen(
                "Input",
                "Enter a balanced ternary number",
                "Use T for -1, 0 for zero, and 1 for +1.",
            )
        )
        try:
            return validate_balanced_ternary(prompt("Enter a balanced ternary number"))
        except ValueError as error:
            print_screen(error_screen(str(error)))


def get_conversion_mode() -> str:
    """Ask the user which balanced ternary conversion mode to run."""
    while True:
        print_screen(
            menu_screen(
                "Balanced Ternary",
                [
                    ("1", "Decimal to Balanced Ternary"),
                    ("2", "Balanced Ternary to Decimal"),
                    ("3", "Back"),
                ],
            )
        )

        choice = clean_input(prompt())

        if choice in {"1", "2", "3"}:
            return choice

        print_screen(error_screen("Please enter 1, 2, or 3."))


def balanced_digit_from_remainder(remainder: int) -> tuple[str, int]:
    """Convert a base-3 remainder into a balanced ternary digit and carry.

    Args:
        remainder: The remainder from division by 3.

    Returns:
        A tuple containing the balanced digit and the carry for the next
        higher place.

    Raises:
        ValueError: If remainder is not 0, 1, or 2.

    Notes:
        A remainder of 2 cannot be written directly because balanced ternary
        only allows -1, 0, and +1. Since 2 = -1 + 3, we write T and carry 1.
    """
    if remainder == 0:
        return "0", 0
    if remainder == 1:
        return "1", 0
    if remainder == 2:
        return "T", 1

    raise ValueError("Remainder must be 0, 1, or 2.")


def invert_balanced_ternary(balanced_ternary: str) -> str:
    """Return the balanced ternary representation of the opposite value.

    Args:
        balanced_ternary: A valid balanced ternary string.

    Returns:
        The representation of the negative of the input value.
    """
    inverted_digits = []

    for digit in balanced_ternary:
        if digit == "1":
            inverted_digits.append("T")
        elif digit == "T":
            inverted_digits.append("1")
        else:
            inverted_digits.append("0")

    return "".join(inverted_digits)


def decimal_to_balanced_ternary(number: int) -> str:
    """Convert a decimal integer to balanced ternary.

    Args:
        number: The decimal integer to convert.

    Returns:
        The balanced ternary representation using T, 0, and 1.
    """
    if number == 0:
        return "0"

    if number < 0:
        return invert_balanced_ternary(decimal_to_balanced_ternary(-number))

    digits = []

    while number > 0:
        remainder = number % 3
        digit, carry = balanced_digit_from_remainder(remainder)

        digits.append(digit)
        number = (number // 3) + carry

    return "".join(reversed(digits))


def balanced_ternary_to_decimal(balanced_ternary: str) -> int:
    """Convert a balanced ternary string back to decimal.

    Args:
        balanced_ternary: Balanced ternary text using T, 0, and 1.

    Returns:
        The decimal integer represented by the balanced ternary input.

    Raises:
        ValueError: If the input is empty or contains invalid characters.
    """
    normalized_value = validate_balanced_ternary(balanced_ternary)
    total = 0

    for power, digit in enumerate(reversed(normalized_value)):
        total += BALANCED_DIGIT_VALUES[digit] * (3 ** power)

    return total


def get_conversion_steps(number: int) -> list[dict[str, int | str]]:
    """Return division steps used to convert a non-negative integer.

    Args:
        number: The non-negative decimal integer to trace.

    Returns:
        A list of dictionaries containing quotient, remainder, digit, carry,
        and next number values for each step.
    """
    if number < 0:
        number = abs(number)

    steps = []

    while number > 0:
        quotient = number // 3
        remainder = number % 3
        digit, carry = balanced_digit_from_remainder(remainder)
        next_number = quotient + carry

        steps.append(
            {
                "number": number,
                "quotient": quotient,
                "remainder": remainder,
                "digit": digit,
                "carry": carry,
                "next_number": next_number,
            }
        )

        number = next_number

    return steps


def superscript_power(power: int) -> str:
    """Return a power value formatted in a terminal-friendly way."""
    return "^" + str(power)


def format_signed_sum(values: list[int]) -> str:
    """Format a list of integers as a readable signed sum."""
    if not values:
        return "0"

    expression = str(values[0])

    for value in values[1:]:
        if value < 0:
            expression += f" - {abs(value)}"
        else:
            expression += f" + {value}"

    return expression


def explain_conversion() -> None:
    """Print an educational explanation of balanced ternary."""
    print_screen(
        explanation_screen(
            "How Balanced Ternary Works",
            [
                "Ordinary ternary is base 3 and uses digits 0, 1, and 2.",
                "Balanced ternary is still base 3, but its digits are T, 0, and 1.",
                "T represents -1, so each digit can mean -1, 0, or +1.",
                "",
                "Balanced ternary removes the digit 2 by rewriting it as:",
                "2 = -1 + 3",
                "",
                "That is why remainder 2 becomes T with a carry of 1.",
                "The T supplies -1 in the current place.",
                "The carry supplies +3 in the next higher place.",
                "",
                "One advantage is symmetry: negation swaps 1 and T.",
            ],
        )
    )


def explain_examples() -> None:
    """Print small reference examples for common balanced ternary values."""
    rows = [(number, decimal_to_balanced_ternary(number)) for number in [2, 5, 8, 11]]
    print_screen(
        explanation_screen(
            "Small Examples",
            table_lines(["Decimal", "Balanced"], rows),
        )
    )


def display_step_by_step_conversion(number: int, balanced_ternary: str) -> None:
    """Display each division step used for decimal to balanced conversion."""
    lines = []

    if number == 0:
        print_screen(
            explanation_screen(
                "Step-by-Step Conversion",
                ["0 is represented as 0 in balanced ternary."],
            )
        )
        return

    working_number = abs(number)

    if number < 0:
        lines.extend(
            [
                f"First convert the magnitude {working_number}.",
                "Then invert the digits because the original number is negative.",
                "1 becomes T, T becomes 1, and 0 stays 0.",
                "",
            ]
        )

    for step in get_conversion_steps(working_number):
        current_number = step["number"]
        quotient = step["quotient"]
        remainder = step["remainder"]
        digit = step["digit"]
        carry = step["carry"]
        next_number = step["next_number"]

        lines.append(f"{current_number} / 3 = {quotient} remainder {remainder}")

        if remainder == 2:
            lines.append("remainder 2 -> write T, carry 1 because 2 = -1 + 3")
            lines.append(f"{quotient} + carry = {next_number}")
        else:
            lines.append(f"remainder {remainder} -> write {digit}, carry {carry}")

        lines.append("")

    lines.append(f"Balanced Ternary = {balanced_ternary}")
    print_screen(explanation_screen("Step-by-Step Conversion", lines))


def build_place_value_rows(
    balanced_ternary: str,
) -> list[tuple[str, int, int, int, int]]:
    """Build rows for the balanced ternary place-value table."""
    normalized_value = validate_balanced_ternary(balanced_ternary)
    highest_power = len(normalized_value) - 1
    rows = []

    for index, digit in enumerate(normalized_value):
        power = highest_power - index
        digit_value = BALANCED_DIGIT_VALUES[digit]
        place_value = 3 ** power
        contribution = digit_value * place_value
        rows.append((digit, digit_value, power, place_value, contribution))

    return rows


def display_place_value_table(balanced_ternary: str) -> None:
    """Display the place-value table for a balanced ternary number."""
    rows = [
        (digit, digit_value, f"3{superscript_power(power)}", place_value, contribution)
        for digit, digit_value, power, place_value, contribution in build_place_value_rows(
            balanced_ternary
        )
    ]
    print_screen(
        explanation_screen(
            "Place-Value Table",
            table_lines(["Digit", "Value", "Power", "Place", "Contribution"], rows),
        )
    )


def verify_conversion(balanced_ternary: str) -> str:
    """Build a symbolic and evaluated verification for balanced ternary.

    Args:
        balanced_ternary: The balanced ternary string to verify.

    Returns:
        A multi-line explanation showing how the representation evaluates.
    """
    rows = build_place_value_rows(balanced_ternary)
    contributions = [row[4] for row in rows]
    decimal_value = balanced_ternary_to_decimal(balanced_ternary)

    lines = ["Verification", "", balanced_ternary, ""]

    for _digit, digit_value, _power, place_value, contribution in rows:
        lines.append(f"({digit_value} x {place_value}) = {contribution}")

    lines.append("")
    lines.append(f"{format_signed_sum(contributions)} = {decimal_value}")

    return "\n".join(lines)


def verify_round_trip(original_decimal: int, balanced_ternary: str) -> bool:
    """Return whether balanced ternary converts back to the original decimal."""
    return balanced_ternary_to_decimal(balanced_ternary) == original_decimal


def display_round_trip_verification(
    original_decimal: int, balanced_ternary: str
) -> None:
    """Display whether the conversion passes round-trip verification."""
    converted_decimal = balanced_ternary_to_decimal(balanced_ternary)
    status = (
        "[OK] Verification Successful"
        if converted_decimal == original_decimal
        else "[X] Verification Failed"
    )

    print_screen(
        result_screen(
            "Round-Trip Verification",
            [
                f"Balanced -> Decimal : {converted_decimal}",
                status,
            ],
        )
    )


def display_results(number: int) -> None:
    """Display decimal, ordinary ternary, balanced ternary, and verification."""
    ordinary_ternary = decimal_to_ternary(number)
    balanced_ternary = decimal_to_balanced_ternary(number)

    print_screen(
        result_screen(
            "Conversion Result",
            key_value_lines(
                [
                    ("Input Number", number),
                    ("Ordinary Base-3", ordinary_ternary),
                    ("Balanced Base-3", balanced_ternary),
                ]
            ),
        )
    )

    print_screen(explanation_screen("Legend", ["T = -1", "0 = 0", "1 = +1"]))

    display_step_by_step_conversion(number, balanced_ternary)
    display_place_value_table(balanced_ternary)

    print_screen(
        explanation_screen("Verification", verify_conversion(balanced_ternary).splitlines())
    )

    display_round_trip_verification(number, balanced_ternary)

    print_screen(
        explanation_screen(
            "Learning Summary",
            [
                "Balanced ternary uses -1, 0, and +1 as digit values.",
                "The digit T makes it easy to represent negative contributions.",
            ],
        )
    )


def display_reverse_conversion_results(balanced_ternary: str) -> None:
    """Display decimal output and verification for balanced to decimal mode."""
    normalized_value = validate_balanced_ternary(balanced_ternary)
    decimal_value = balanced_ternary_to_decimal(normalized_value)

    print_screen(
        result_screen(
            "Reverse Conversion Result",
            key_value_lines(
                [
                    ("Balanced Base-3", normalized_value),
                    ("Decimal Number", decimal_value),
                ]
            ),
        )
    )

    display_place_value_table(normalized_value)

    print_screen(
        explanation_screen("Verification", verify_conversion(normalized_value).splitlines())
    )

    print_screen(
        explanation_screen(
            "Learning Summary",
            [
                "Each balanced ternary digit is multiplied by a power of 3.",
                "Adding the positive and negative contributions gives the decimal value.",
            ],
        )
    )


def main() -> None:
    """Run the balanced ternary educational module."""
    display_header()
    explain_conversion()
    explain_examples()

    while True:
        choice = get_conversion_mode()

        if choice == "1":
            display_results(get_decimal_input())
        elif choice == "2":
            display_reverse_conversion_results(get_balanced_ternary_input())
        else:
            print_screen(success_message("Returning to the converter menu."))
            break


if __name__ == "__main__":
    main()
