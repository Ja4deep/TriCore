import pytest

from converters.balanced_ternary import (
    balanced_ternary_to_decimal,
    build_place_value_rows,
    decimal_to_balanced_ternary,
    validate_balanced_ternary,
    verify_conversion,
    verify_round_trip,
)


@pytest.mark.parametrize(
    ("decimal_number", "balanced_ternary"),
    [
        (0, "0"),
        (1, "1"),
        (2, "1T"),
        (5, "1TT"),
        (8, "10T"),
        (11, "11T"),
        (56, "1T01T"),
    ],
)
def test_decimal_to_balanced_ternary_positive_numbers(
    decimal_number: int, balanced_ternary: str
) -> None:
    assert decimal_to_balanced_ternary(decimal_number) == balanced_ternary


@pytest.mark.parametrize(
    ("decimal_number", "balanced_ternary"),
    [
        (-1, "T"),
        (-2, "T1"),
        (-5, "T11"),
        (-8, "T01"),
        (-11, "TT1"),
        (-56, "T10T1"),
    ],
)
def test_decimal_to_balanced_ternary_negative_numbers(
    decimal_number: int, balanced_ternary: str
) -> None:
    assert decimal_to_balanced_ternary(decimal_number) == balanced_ternary


def test_large_integer_round_trip() -> None:
    decimal_number = 987_654_321
    balanced_ternary = decimal_to_balanced_ternary(decimal_number)

    assert set(balanced_ternary) <= {"T", "0", "1"}
    assert balanced_ternary_to_decimal(balanced_ternary) == decimal_number


@pytest.mark.parametrize("invalid_value", ["", "2", "12", "abc", "1-0", "10X"])
def test_invalid_balanced_ternary_strings_are_rejected(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        validate_balanced_ternary(invalid_value)


def test_validate_balanced_ternary_normalizes_lowercase_t() -> None:
    assert validate_balanced_ternary("t01") == "T01"


def test_place_value_rows_for_10t() -> None:
    assert build_place_value_rows("10T") == [
        ("1", 1, 2, 9, 9),
        ("0", 0, 1, 3, 0),
        ("T", -1, 0, 1, -1),
    ]


def test_verification_contains_symbolic_and_evaluated_forms() -> None:
    verification = verify_conversion("10T")

    assert "(1 x 9) = 9" in verification
    assert "(0 x 3) = 0" in verification
    assert "(-1 x 1) = -1" in verification
    assert "9 + 0 - 1 = 8" in verification


def test_round_trip_range_from_negative_1000_to_positive_1000() -> None:
    for decimal_number in range(-1000, 1001):
        balanced_ternary = decimal_to_balanced_ternary(decimal_number)

        assert balanced_ternary_to_decimal(balanced_ternary) == decimal_number
        assert verify_round_trip(decimal_number, balanced_ternary)
