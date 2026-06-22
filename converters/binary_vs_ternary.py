from converters.decimal_to_ternary import decimal_to_ternary, get_decimal_input
from ui.terminal import (
    explanation_screen,
    key_value_lines,
    print_screen,
    result_screen,
    table_lines,
)


def decimal_to_binary(number: int) -> str:
    """Convert a decimal integer to binary without the Python 0b prefix."""
    if number < 0:
        return "-" + bin(-number)[2:]

    return bin(number)[2:]


def compare_binary_and_ternary(number: int) -> tuple[str, str, str]:
    """Return binary, ternary, and a short digit-count comparison message."""
    binary = decimal_to_binary(number)
    ternary = decimal_to_ternary(number)
    binary_digit_count = len(binary.lstrip("-"))
    ternary_digit_count = len(ternary.lstrip("-"))

    if binary_digit_count > ternary_digit_count:
        comparison = "Ternary uses fewer digits."
    elif binary_digit_count < ternary_digit_count:
        comparison = "Binary uses fewer digits."
    else:
        comparison = "Both use the same number of digits."

    return binary, ternary, comparison


def display_header() -> None:
    """Display the binary-vs-ternary comparison title."""
    print_screen(
        explanation_screen(
            "Binary vs Ternary",
            ["Compare how base 2 and base 3 represent the same decimal value."],
        )
    )


def explain_comparison() -> None:
    """Explain why binary and ternary lengths can be compared."""
    print_screen(
        explanation_screen(
            "How the Comparison Works",
            [
                "Binary is base 2, so it uses the digits 0 and 1.",
                "Ternary is base 3, so it uses the digits 0, 1, and 2.",
                "A larger base usually stores the same value using fewer places.",
                "This program compares the number of digits needed in each base.",
            ],
        )
    )


def digit_count_table_lines(binary: str, ternary: str) -> list[str]:
    """Return a table comparing binary and ternary digit counts."""
    return table_lines(
        ["Number System", "Base", "Digits"],
        [
            ("Binary", 2, len(binary.lstrip("-"))),
            ("Ternary", 3, len(ternary.lstrip("-"))),
        ],
    )


def display_digit_count_table(binary: str, ternary: str) -> None:
    """Display a small table comparing binary and ternary digit counts."""
    print_screen(
        explanation_screen("Digit Count Table", digit_count_table_lines(binary, ternary))
    )


def display_results(number: int) -> None:
    """Display binary, ternary, digit counts, and a learning summary."""
    binary, ternary, comparison = compare_binary_and_ternary(number)

    print_screen(
        result_screen(
            "Comparison Result",
            key_value_lines(
                [
                    ("Decimal Number", number),
                    ("Binary", binary),
                    ("Ternary", ternary),
                ]
            ),
        )
    )
    display_digit_count_table(binary, ternary)
    print_screen(
        explanation_screen(
            "Observation",
            [
                comparison,
                "The sign is not counted as a digit because it only shows direction.",
            ],
        )
    )
    print_screen(
        explanation_screen(
            "Learning Summary",
            [
                "Binary and ternary are both positional number systems.",
                "Changing the base changes how many digit positions are needed.",
            ],
        )
    )


def main() -> None:
    """Run the binary vs ternary comparison directly from the terminal."""
    number = get_decimal_input()
    display_header()
    explain_comparison()
    display_results(number)


if __name__ == "__main__":
    main()
