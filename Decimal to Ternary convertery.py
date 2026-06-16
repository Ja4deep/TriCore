def decimal_to_ternary(n):
    # Handle the special case where the input is 0
    if n == 0:
        return "0"

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


number = int(input("Enter a decimal number: "))
print("Ternary:", decimal_to_ternary(number))
