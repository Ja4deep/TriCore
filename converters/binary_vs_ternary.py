from converters.decimal_to_ternary import decimal_to_ternary, get_decimal_input


SEPARATOR = "=" * 40


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
    print(SEPARATOR)
    print("BINARY VS TERNARY COMPARISON".center(40))
    print(SEPARATOR)


def explain_comparison() -> None:
    """Explain why binary and ternary lengths can be compared."""
    print("\nHow the Comparison Works")
    print("-" * 40)
    print("Binary is base-2, so it uses the digits 0 and 1.")
    print("Ternary is base-3, so it uses the digits 0, 1, and 2.")
    print("A larger base usually stores the same value using fewer places.")
    print("This program compares the number of digits needed in each base.")


def display_digit_count_table(binary: str, ternary: str) -> None:
    """Display a small table comparing binary and ternary digit counts."""
    binary_digit_count = len(binary.lstrip("-"))
    ternary_digit_count = len(ternary.lstrip("-"))

    print("\nDigit Count Table")
    print("-" * 40)
    print(f"{'Number System':<18}{'Base':>6}{'Digits':>10}")
    print("-" * 40)
    print(f"{'Binary':<18}{2:>6}{binary_digit_count:>10}")
    print(f"{'Ternary':<18}{3:>6}{ternary_digit_count:>10}")


def display_results(number: int) -> None:
    """Display binary, ternary, digit counts, and a learning summary."""
    binary, ternary, comparison = compare_binary_and_ternary(number)

    print("\nComparison Result")
    print("-" * 40)
    print(f"Decimal Number : {number}")
    print(f"Binary         : {binary}")
    print(f"Ternary        : {ternary}")

    display_digit_count_table(binary, ternary)

    print("\nObservation")
    print("-" * 40)
    print(comparison)
    print("The sign is not counted as a digit because it only shows direction.")

    print("\nLearning Summary")
    print("-" * 40)
    print("Binary and ternary are both positional number systems.")
    print("Changing the base changes how many digit positions are needed.")


def main() -> None:
    """Run the binary vs ternary comparison directly from the terminal."""
    number = get_decimal_input()
    display_header()
    explain_comparison()
    display_results(number)


if __name__ == "__main__":
    main()
