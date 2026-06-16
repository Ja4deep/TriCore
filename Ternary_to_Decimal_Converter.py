def ternary_to_decimal(ternary_str):
    """
    Convert a ternary (base 3) number to decimal (base 10).
    """

    total = 0
    power = 0

    # Read digits from right to left
    for digit in ternary_str[::-1]:

        # Convert character to integer
        digit = int(digit)

        # Add the digit's contribution based on its position
        total += digit * (3 ** power)

        # Move to the next power of 3
        power += 1

    return total


ternary = input("Enter a ternary number: ")
print("Decimal:", ternary_to_decimal(ternary))