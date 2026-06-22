import pytest

from arithmetic.addition import add_many, add_numbers
from arithmetic.borrow import calculate_borrow, create_borrow, normalize_borrows
from arithmetic.carry import calculate_carry, create_carry, normalize_carries
from arithmetic.division import divide_numbers
from arithmetic.multiplication import multiply_numbers
from arithmetic.subtraction import subtract_numbers


def ternary_to_decimal(value: str) -> int:
    """Convert a signed ordinary ternary string to decimal for test assertions."""
    sign = -1 if value.startswith("-") else 1
    digits = value.lstrip("-")
    total = 0

    for digit in digits:
        total = (total * 3) + int(digit)

    return sign * total


def decimal_to_ternary(value: int) -> str:
    """Convert a decimal integer to signed ordinary ternary for test assertions."""
    if value == 0:
        return "0"
    if value < 0:
        return "-" + decimal_to_ternary(-value)

    digits = []
    while value:
        digits.append(str(value % 3))
        value //= 3

    return "".join(reversed(digits))


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("0", "0", "0"),
        ("1", "2", "10"),
        ("2", "2", "11"),
        ("222", "1", "1000"),
        ("102012", "2201", "111220"),
    ],
)
def test_add_numbers_returns_ternary_sum(left: str, right: str, expected: str) -> None:
    result = add_numbers(left, right)

    assert result.result == expected
    assert result.borrows == []


def test_add_numbers_records_carry_chain_and_explanation() -> None:
    result = add_numbers("222", "1", explanation_mode=True)

    assert result.result == "1000"
    assert result.carries == [1, 1, 1]
    assert len(result.metadata["carry_records"]) == 3
    assert any("Carry 1" in step.expression for step in result.steps)


def test_add_many_reuses_addition_for_multiple_operands() -> None:
    result = add_many(["1", "2", "10", "11"])

    assert result.result == "101"


@pytest.mark.parametrize("invalid_value", ["", " 1", "1 ", "03", "-1", "1203"])
def test_add_numbers_rejects_invalid_operands(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        add_numbers(invalid_value, "1")


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("0", "0", "0"),
        ("10", "1", "2"),
        ("1000", "1", "222"),
        ("102012", "2201", "22111"),
        ("1", "2", "-1"),
    ],
)
def test_subtract_numbers_returns_ternary_difference(
    left: str,
    right: str,
    expected: str,
) -> None:
    result = subtract_numbers(left, right)

    assert result.result == expected
    assert ternary_to_decimal(result.result) == (
        ternary_to_decimal(left) - ternary_to_decimal(right)
    )


def test_subtract_numbers_records_borrow_chain_and_explanation() -> None:
    result = subtract_numbers("1000", "1", explanation_mode=True)

    assert result.result == "222"
    assert result.borrows == [1, 1, 1]
    assert len(result.metadata["borrow_records"]) == 3
    assert any("Borrow one trit" in step.expression for step in result.steps)


@pytest.mark.parametrize("invalid_value", ["", " 1", "1 ", "00", "-1", "abc"])
def test_subtract_numbers_rejects_invalid_operands(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        subtract_numbers("1", invalid_value)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("0", "221", "0"),
        ("1", "222", "222"),
        ("12", "10", "120"),
        ("22", "22", "2101"),
        ("1021", "201", "212221"),
    ],
)
def test_multiply_numbers_returns_ternary_product(
    left: str,
    right: str,
    expected: str,
) -> None:
    result = multiply_numbers(left, right)

    assert result.result == expected
    assert ternary_to_decimal(result.result) == (
        ternary_to_decimal(left) * ternary_to_decimal(right)
    )


def test_multiply_numbers_returns_partial_rows_and_explanations() -> None:
    result = multiply_numbers("12", "10", explanation_mode=True)

    assert result.result == "120"
    assert result.metadata["partial_rows"] == ["0", "120"]
    assert any(step.title == "Add Partial Rows" for step in result.steps)


@pytest.mark.parametrize("invalid_value", ["", " 2", "2 ", "012", "-2", "9"])
def test_multiply_numbers_rejects_invalid_operands(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        multiply_numbers(invalid_value, "1")


@pytest.mark.parametrize(
    ("dividend", "divisor", "quotient", "remainder"),
    [
        ("0", "1", "0", "0"),
        ("120", "10", "12", "0"),
        ("1000", "2", "111", "1"),
        ("222", "10", "22", "2"),
        ("102012", "21", "1121", "1"),
    ],
)
def test_divide_numbers_returns_quotient_and_remainder(
    dividend: str,
    divisor: str,
    quotient: str,
    remainder: str,
) -> None:
    result = divide_numbers(dividend, divisor)

    assert result.result == quotient
    assert result.metadata["quotient"] == quotient
    assert result.metadata["remainder"] == remainder
    assert ternary_to_decimal(dividend) == (
        ternary_to_decimal(divisor) * ternary_to_decimal(quotient)
    ) + ternary_to_decimal(remainder)


def test_divide_numbers_returns_long_division_steps() -> None:
    result = divide_numbers("1000", "2", explanation_mode=True)

    assert result.result == "111"
    assert result.metadata["remainder"] == "1"
    assert len(result.metadata["intermediate_rows"]) == 4
    assert any("Bring down" in step.expression for step in result.steps)


def test_divide_numbers_rejects_zero_divisor() -> None:
    with pytest.raises(ValueError):
        divide_numbers("1", "0")


@pytest.mark.parametrize("invalid_value", ["", " 1", "1 ", "01", "-1", "12A"])
def test_divide_numbers_rejects_invalid_operands(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        divide_numbers(invalid_value, "1")


def test_large_number_operations_match_decimal_arithmetic() -> None:
    left = "222222222222222222222222"
    right = "111111111111"

    sum_result = add_numbers(left, right).result
    difference_result = subtract_numbers(left, right).result
    product_result = multiply_numbers("222222222222", "111111").result
    division_result = divide_numbers(left, right)

    assert ternary_to_decimal(sum_result) == ternary_to_decimal(left) + ternary_to_decimal(right)
    assert ternary_to_decimal(difference_result) == ternary_to_decimal(left) - ternary_to_decimal(right)
    assert ternary_to_decimal(product_result) == (
        ternary_to_decimal("222222222222") * ternary_to_decimal("111111")
    )
    assert ternary_to_decimal(left) == (
        ternary_to_decimal(right) * ternary_to_decimal(division_result.result)
    ) + ternary_to_decimal(division_result.metadata["remainder"])


def test_carry_helpers_create_and_normalize_records() -> None:
    written_digit, carry = calculate_carry(4)
    record = create_carry(2, carry, "2 + 2")

    assert written_digit == "1"
    assert carry == 1
    assert normalize_carries([record, 1]) == [record, create_carry(1, 1)]


def test_borrow_helpers_create_and_normalize_records() -> None:
    written_digit, borrow, adjusted_top = calculate_borrow(0, 2, 0)
    record = create_borrow(0, borrow, "0 - 2")

    assert written_digit == "1"
    assert borrow == 1
    assert adjusted_top == 3
    assert normalize_borrows([record, 1]) == [record, create_borrow(1, 1)]


@pytest.mark.parametrize("base", [2, 4, 10])
def test_operations_reject_unsupported_bases(base: int) -> None:
    with pytest.raises(ValueError):
        add_numbers("1", "1", base=base)
