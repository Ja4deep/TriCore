def decimal_to_ternary(n):
    """Converts a decimal number to its ternary number"""

    if n == 0:
        return "0"

    digits = []

    while n > 0:
        digits.append(str(n % 3))
        n //= 3

    return "".join(reversed(digits))


# User's input (DECIMAL)
number = int(input("Enter a number: "))

# Converting to binary and ternary
binary = bin(number)[2:]
ternary = decimal_to_ternary(number)

# Display Results
print("\n=== Binary vs Ternary Comparison ===")
print(f"Decimal : {number}")
print(f"Binary  : {binary}")
print(f"Ternary : {ternary}")

print("\nDigit Count:") 
print(f"Binary Digits  : {len(binary)}")
print(f"Ternary Digits : {len(ternary)}")

# Compare digit counts
if len(binary) > len(ternary):
    print("\nTernary uses fewer digits.")
elif len(binary) < len(ternary):
    print("\nBinary uses fewer digits.")
else:
    print("\nBoth use the same number of digits.")
