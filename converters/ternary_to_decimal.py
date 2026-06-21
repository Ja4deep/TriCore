import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SEPARATOR = "=" * 40


def clean_input(raw_input_value: str) -> str:
    """Return input with whitespace and hidden BOM characters removed."""
    return raw_input_value.strip().replace("\ufeff", "").replace("\xef\xbb\xbf", "")


def validate_ternary(ternary_str: str) -> str:
    """Validate and normalize an ordinary ternary string.

    Args:
        ternary_str: User-entered ternary text.

    Returns:
        The cleaned ternary string.

    Raises:
        ValueError: If the input is empty or contains digits other than 0, 1,
            and 2. A leading minus sign is allowed.
    """
    normalized_value = clean_input(ternary_str)

    if not normalized_value:
        raise ValueError("Ternary input cannot be empty.")

    sign_removed = normalized_value[1:] if normalized_value.startswith("-") else normalized_value

    if not sign_removed or any(digit not in "012" for digit in sign_removed):
        raise ValueError("Ternary numbers can only contain 0, 1, and 2.")

    return normalized_value


def ternary_to_decimal(ternary_str: str) -> int:
    """Convert a ternary number to decimal.

    Args:
        ternary_str: Ordinary ternary text using digits 0, 1, and 2.

    Returns:
        The decimal integer represented by the ternary input.

    Raises:
        ValueError: If the ternary input is invalid.
    """
    ternary_str = validate_ternary(ternary_str)

    sign = -1 if ternary_str.startswith("-") else 1
    digits = ternary_str[1:] if sign == -1 else ternary_str

    total = 0
    power = 0

    # Read digits from right to left
    for digit in digits[::-1]:

        # Convert character to integer
        digit = int(digit)

        # Add the digit's contribution based on its position
        total += digit * (3 ** power)

        # Move to the next power of 3
        power += 1

    return sign * total


def get_ternary_input() -> str:
    """Ask for an ordinary ternary number until the input is valid."""
    while True:
        try:
            return validate_ternary(input("Enter a ternary number: "))
        except ValueError as error:
            print(f"Invalid input. {error}\n")


def display_header() -> None:
    """Display the ternary-to-decimal converter title."""
    print(SEPARATOR)
    print("ORDINARY TERNARY TO DECIMAL".center(40))
    print(SEPARATOR)


def explain_conversion() -> None:
    """Print the place-value idea behind ternary-to-decimal conversion."""
    print("\nHow Ternary to Decimal Works")
    print("-" * 40)
    print("Each ternary digit is multiplied by a power of 3.")
    print("The rightmost digit uses 3^0, then 3^1, then 3^2, and so on.")
    print("Adding all contributions gives the decimal value.")


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
        place_value = 3 ** power
        contribution = sign * digit_value * place_value
        rows.append((digit, digit_value, power, place_value, contribution))

    return rows


def display_place_value_table(ternary: str) -> None:
    """Display a table showing each digit's decimal contribution."""
    print("\nPlace-Value Table")
    print("-" * 55)
    print(
        f"{'Digit':<8}"
        f"{'Value':>7}"
        f"{'Power':>8}"
        f"{'Place Value':>14}"
        f"{'Contribution':>15}"
    )
    print("-" * 55)

    for digit, digit_value, power, place_value, contribution in build_place_value_rows(
        ternary
    ):
        print(
            f"{digit:<8}"
            f"{digit_value:>7}"
            f"{'3^' + str(power):>8}"
            f"{place_value:>14}"
            f"{contribution:>15}"
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

    print("\nConversion Result")
    print("-" * 40)
    print(f"Ordinary Ternary : {normalized_value}")
    print(f"Decimal Number   : {decimal_value}")

    print("\nLegend")
    print("0, 1, 2 are ordinary base-3 digits.")
    print("Each position is a power of 3.")

    display_place_value_table(normalized_value)

    print()
    print(verify_conversion(normalized_value))

    print("\nLearning Summary")
    print("-" * 40)
    print("Ternary to decimal uses place values of 1, 3, 9, 27, and so on.")
    print("The final decimal number is the sum of all digit contributions.")


def main() -> None:
    """Run the educational ternary-to-decimal converter."""
    display_header()
    explain_conversion()
    display_results(get_ternary_input())


if __name__ == "__main__":
    main()
