import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SEPARATOR = "=" * 40


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


def clean_input(raw_input_value: str) -> str:
    """Return input with whitespace and hidden BOM characters removed."""
    return raw_input_value.strip().replace("\ufeff", "").replace("\xef\xbb\xbf", "")


def get_decimal_input() -> int:
    """Ask for a decimal integer until the input is valid."""
    while True:
        raw_input_value = clean_input(input("Enter a decimal number: "))

        try:
            return int(raw_input_value)
        except ValueError:
            print("Invalid input. Please enter a whole number, such as 8 or -11.\n")


def display_header() -> None:
    """Display the ordinary ternary converter title."""
    print(SEPARATOR)
    print("DECIMAL TO ORDINARY TERNARY".center(40))
    print(SEPARATOR)


def explain_conversion() -> None:
    """Print the idea behind ordinary ternary conversion."""
    print("\nHow Ordinary Ternary Works")
    print("-" * 40)
    print("Ternary is base-3, so every place is a power of 3.")
    print("The allowed digits are 0, 1, and 2.")
    print("Repeated division by 3 gives the digits from right to left.")


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
    print("\nStep-by-Step Conversion")
    print("-" * 40)

    if number < 0:
        print(f"Convert the magnitude {abs(number)} first, then add the minus sign.\n")

    for current_number, quotient, remainder in get_conversion_steps(number):
        print(f"{current_number} / 3 = {quotient} remainder {remainder}")
        print(f"write {remainder}\n")


def ternary_to_decimal_value(ternary: str) -> int:
    """Evaluate an ordinary ternary string as decimal."""
    sign = -1 if ternary.startswith("-") else 1
    digits = ternary.lstrip("-")
    total = 0

    for power, digit in enumerate(reversed(digits)):
        total += int(digit) * (3 ** power)

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
        place_value = 3 ** power
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

    print("\nConversion Result")
    print("-" * 40)
    print(f"Decimal Number   : {number}")
    print(f"Ordinary Ternary : {ternary}")

    display_step_by_step_conversion(number)

    print("\nLegend")
    print("0, 1, 2 are ordinary base-3 digits.")
    print("Each digit is multiplied by a power of 3.")

    print()
    print(verify_conversion(number, ternary))

    print("\nLearning Summary")
    print("-" * 40)
    print("Decimal to ternary uses repeated division by 3.")
    print("The remainders form the ternary answer from right to left.")


def main() -> None:
    """Run the educational ordinary ternary converter."""
    display_header()
    explain_conversion()
    display_results(get_decimal_input())


if __name__ == "__main__":
    main()
