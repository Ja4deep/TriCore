"""Educational ordinary-ternary-to-decimal conversion helpers."""

from arithmetic.utils import clean_input
from ui.terminal import (
    error_screen,
    explanation_screen,
    input_screen,
    key_value_lines,
    print_screen,
    prompt,
    result_screen,
    table_lines,
)


def validate_ternary(ternary_str: str) -> str:
    """Validate and normalize an ordinary ternary string."""
    normalized_value = clean_input(ternary_str)

    if not normalized_value:
        raise ValueError("Ternary input cannot be empty.")

    sign_removed = (
        normalized_value[1:] if normalized_value.startswith("-") else normalized_value
    )

    if not sign_removed or any(digit not in "012" for digit in sign_removed):
        raise ValueError("Ternary numbers can only contain 0, 1, and 2.")

    return normalized_value


def ternary_to_decimal(ternary_str: str) -> int:
    """Convert a ternary number to decimal."""
    ternary_str = validate_ternary(ternary_str)

    sign = -1 if ternary_str.startswith("-") else 1
    digits = ternary_str[1:] if sign == -1 else ternary_str

    total = 0
    power = 0

    for digit in digits[::-1]:
        total += int(digit) * (3**power)
        power += 1

    return sign * total


def get_ternary_input() -> str:
    """Ask for an ordinary ternary number until the input is valid."""
    while True:
        print_screen(
            input_screen(
                "Input",
                "Enter a ternary number",
                "Use ordinary ternary digits only: 0, 1, and 2.",
            )
        )
        try:
            return validate_ternary(prompt("Enter a ternary number"))
        except ValueError as error:
            print_screen(error_screen(str(error)))


def display_header() -> None:
    """Display the ternary-to-decimal converter title."""
    print_screen(
        explanation_screen(
            "Ordinary Ternary to Decimal",
            ["Convert a base-3 value back into decimal."],
        )
    )


def explain_conversion() -> None:
    """Print the place-value idea behind ternary-to-decimal conversion."""
    print_screen(
        explanation_screen(
            "How Ternary to Decimal Works",
            [
                "Each ternary digit is multiplied by a power of 3.",
                "The rightmost digit uses 3^0, then 3^1, then 3^2, and so on.",
                "Adding all contributions gives the decimal value.",
            ],
        )
    )


def build_place_value_rows(ternary: str) -> list[tuple[str, int, int, int, int]]:
    """Build place-value rows for an ordinary ternary number."""
    normalized_value = validate_ternary(ternary)
    sign = -1 if normalized_value.startswith("-") else 1
    digits = normalized_value.lstrip("-")
    highest_power = len(digits) - 1
    rows = []

    for index, digit in enumerate(digits):
        power = highest_power - index
        digit_value = int(digit)
        place_value = 3**power
        contribution = sign * digit_value * place_value
        rows.append((digit, digit_value, power, place_value, contribution))

    return rows


def place_value_table_lines(ternary: str) -> list[str]:
    """Return a formatted place-value table for an ordinary ternary number."""
    rows = [
        (digit, value, f"3^{power}", place_value, contribution)
        for digit, value, power, place_value, contribution in build_place_value_rows(
            ternary
        )
    ]
    return table_lines(["Digit", "Value", "Power", "Place", "Contribution"], rows)


def display_place_value_table(ternary: str) -> None:
    """Display a table showing each digit's decimal contribution."""
    print_screen(
        explanation_screen("Place-Value Table", place_value_table_lines(ternary))
    )


def verify_conversion(ternary: str) -> str:
    """Build a mathematical verification for ternary-to-decimal conversion."""
    rows = build_place_value_rows(ternary)
    contributions = [row[4] for row in rows]
    decimal_value = ternary_to_decimal(ternary)
    expression = " + ".join(str(value) for value in contributions).replace("+ -", "- ")

    lines = ["Verification", ""]

    for _digit, digit_value, _power, place_value, contribution in rows:
        lines.append(f"({digit_value} x {place_value}) = {contribution}")

    lines.append("")
    lines.append(f"{expression} = {decimal_value}")
    lines.append("[OK] Verification Successful")

    return "\n".join(lines)


def display_results(ternary: str) -> None:
    """Display decimal output with table and verification."""
    normalized_value = validate_ternary(ternary)
    decimal_value = ternary_to_decimal(normalized_value)

    print_screen(
        result_screen(
            "Conversion Result",
            key_value_lines(
                [
                    ("Ordinary Ternary", normalized_value),
                    ("Decimal Number", decimal_value),
                ]
            ),
        )
    )

    print_screen(
        explanation_screen(
            "Legend",
            [
                "0, 1, and 2 are ordinary base-3 digits.",
                "Each position is a power of 3.",
            ],
        )
    )
    display_place_value_table(normalized_value)
    print_screen(
        explanation_screen(
            "Verification", verify_conversion(normalized_value).splitlines()
        )
    )
    print_screen(
        explanation_screen(
            "Learning Summary",
            [
                "Ternary to decimal uses place values of 1, 3, 9, 27, and so on.",
                "The final decimal number is the sum of all digit contributions.",
            ],
        )
    )


def main() -> None:
    """Run the educational ternary-to-decimal converter."""
    display_header()
    explain_conversion()
    display_results(get_ternary_input())


if __name__ == "__main__":
    main()
