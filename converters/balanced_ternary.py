import sys

try:
    from converters.decimal_to_ternary import decimal_to_ternary
except ModuleNotFoundError:
    from decimal_to_ternary import decimal_to_ternary


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SEPARATOR = "=" * 40
BALANCED_DIGIT_VALUES = {
    "T": -1,
    "0": 0,
    "1": 1,
}

def display_header() -> None:
    """Display the balanced ternary module title."""
    print(SEPARATOR)
    print("BALANCED TERNARY CONVERTER".center(40))
    print(SEPARATOR)


def clean_input(raw_input_value: str) -> str:
    """Return user input with whitespace and hidden BOM characters removed."""
    return raw_input_value.strip().replace("\ufeff", "").replace("\xef\xbb\xbf", "")


def get_decimal_input() -> int:
    """Ask the user for a decimal integer until the input is valid."""
    while True:
        raw_input_value = clean_input(input("Enter a decimal integer: "))

        try:
            return int(raw_input_value)
        except ValueError:
            print("Invalid input. Please enter a whole number, such as 8 or -11.\n")


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
        try:
            return validate_balanced_ternary(
                input("Enter a balanced ternary number using T, 0, and 1: ")
            )
        except ValueError as error:
            print(f"Invalid input. {error}\n")


def get_conversion_mode() -> str:
    """Ask the user which balanced ternary conversion mode to run."""
    while True:
        print("\nChoose a conversion mode:")
        print("1. Decimal -> Balanced Ternary")
        print("2. Balanced Ternary -> Decimal")
        print("3. Exit")

        choice = clean_input(input("\nEnter your choice: "))

        if choice in {"1", "2", "3"}:
            return choice

        print("Invalid choice. Please enter 1, 2, or 3.")


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
    print("\n" + "-" * 40)
    print("HOW BALANCED TERNARY WORKS")
    print("-" * 40)
    print("Ordinary ternary is base-3 and uses digits 0, 1, and 2.")
    print("Balanced ternary is still base-3, but its digits are T, 0, and 1.")
    print("T represents -1, so each digit can mean -1, 0, or +1.")
    print()
    print("Balanced ternary removes the digit 2 by rewriting it as:")
    print("2 = -1 + 3")
    print()
    print("That is why remainder 2 becomes T with a carry of 1.")
    print("The T supplies -1 in the current place.")
    print("The carry supplies +3 in the next higher place.")
    print()
    print("One advantage is symmetry: positive and negative values use the")
    print("same digit positions, and negation is done by swapping 1 and T.")


def explain_examples() -> None:
    """Print small reference examples for common balanced ternary values."""
    print("\nSmall Examples")
    print("-" * 40)

    for number in [2, 5, 8, 11]:
        balanced_ternary = decimal_to_balanced_ternary(number)
        print(f"{number:>2} -> {balanced_ternary}")


def display_step_by_step_conversion(number: int, balanced_ternary: str) -> None:
    """Display each division step used for decimal to balanced conversion."""
    print("\n" + "-" * 40)
    print("STEP-BY-STEP CONVERSION")
    print("-" * 40)

    if number == 0:
        print("0 is represented as 0 in balanced ternary.")
        return

    working_number = abs(number)

    if number < 0:
        print(f"First convert the magnitude {working_number}.")
        print("Then invert the digits because the original number is negative.")
        print("1 becomes T, T becomes 1, and 0 stays 0.\n")

    for step in get_conversion_steps(working_number):
        current_number = step["number"]
        quotient = step["quotient"]
        remainder = step["remainder"]
        digit = step["digit"]
        carry = step["carry"]
        next_number = step["next_number"]

        print(f"{current_number} / 3 = {quotient} remainder {remainder}")

        if remainder == 2:
            print("remainder 2 -> write T, carry 1 because 2 = -1 + 3")
            print(f"{quotient} + carry = {next_number}")
        else:
            print(f"remainder {remainder} -> write {digit}, carry {carry}")

        print()

    print(f"Balanced Ternary = {balanced_ternary}")


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
    print("\n" + "-" * 40)
    print("PLACE-VALUE TABLE")
    print("-" * 40)
    print(
        f"{'Digit':<8}"
        f"{'Value':>7}"
        f"{'Power':>8}"
        f"{'Place Value':>14}"
        f"{'Contribution':>15}"
    )
    print("-" * 52)

    for digit, digit_value, power, place_value, contribution in build_place_value_rows(
        balanced_ternary
    ):
        formatted_power = f"3{superscript_power(power)}"
        print(
            f"{digit:<8}"
            f"{digit_value:>7}"
            f"{formatted_power:>8}"
            f"{place_value:>14}"
            f"{contribution:>15}"
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
    print("\n" + "-" * 40)
    print("ROUND-TRIP VERIFICATION")
    print("-" * 40)

    converted_decimal = balanced_ternary_to_decimal(balanced_ternary)
    print(f"Balanced -> Decimal : {converted_decimal}")

    if converted_decimal == original_decimal:
        print("[OK] Verification Successful")
    else:
        print("[X] Verification Failed")


def display_results(number: int) -> None:
    """Display decimal, ordinary ternary, balanced ternary, and verification."""
    ordinary_ternary = decimal_to_ternary(number)
    balanced_ternary = decimal_to_balanced_ternary(number)

    print("\n" + "-" * 40)
    print("CONVERSION RESULT")
    print("-" * 40)
    print(f"Input Number    : {number}")
    print(f"Ordinary Base-3 : {ordinary_ternary}")
    print(f"Balanced Base-3 : {balanced_ternary}")

    print("\nLegend")
    print("T = -1")
    print("0 = 0")
    print("1 = +1")

    display_step_by_step_conversion(number, balanced_ternary)
    display_place_value_table(balanced_ternary)

    print("\n" + "-" * 40)
    print(verify_conversion(balanced_ternary))

    display_round_trip_verification(number, balanced_ternary)

    print("\nLearning Summary")
    print("-" * 40)
    print("Balanced ternary uses -1, 0, and +1 as digit values.")
    print("The digit T makes it easy to represent negative contributions.")


def display_reverse_conversion_results(balanced_ternary: str) -> None:
    """Display decimal output and verification for balanced to decimal mode."""
    normalized_value = validate_balanced_ternary(balanced_ternary)
    decimal_value = balanced_ternary_to_decimal(normalized_value)

    print("\n" + "-" * 40)
    print("REVERSE CONVERSION RESULT")
    print("-" * 40)
    print(f"Balanced Base-3 : {normalized_value}")
    print(f"Decimal Number  : {decimal_value}")

    display_place_value_table(normalized_value)

    print("\n" + "-" * 40)
    print(verify_conversion(normalized_value))

    print("\nLearning Summary")
    print("-" * 40)
    print("Each balanced ternary digit is multiplied by a power of 3.")
    print("Adding the positive and negative contributions gives the decimal value.")


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
            print("\nExiting Balanced Ternary Converter.")
            break


if __name__ == "__main__":
    main()
