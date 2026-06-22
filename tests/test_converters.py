import pytest

from converters.binary_vs_ternary import compare_binary_and_ternary, decimal_to_binary
from converters.decimal_to_ternary import (
    decimal_to_ternary,
    get_conversion_steps,
    ternary_to_decimal_value,
    verify_conversion as verify_decimal_to_ternary,
)
from converters.ternary_to_decimal import (
    build_place_value_rows,
    ternary_to_decimal,
    validate_ternary,
    verify_conversion as verify_ternary_to_decimal,
)


@pytest.mark.parametrize(
    ("decimal_number", "ternary"),
    [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "10"),
        (10, "101"),
        (26, "222"),
        (-5, "-12"),
    ],
)
def test_decimal_to_ordinary_ternary(decimal_number: int, ternary: str) -> None:
    assert decimal_to_ternary(decimal_number) == ternary


@pytest.mark.parametrize(
    ("ternary", "decimal_number"),
    [
        ("0", 0),
        ("1", 1),
        ("2", 2),
        ("10", 3),
        ("101", 10),
        ("222", 26),
        ("-12", -5),
    ],
)
def test_ordinary_ternary_to_decimal(ternary: str, decimal_number: int) -> None:
    assert ternary_to_decimal(ternary) == decimal_number
    assert ternary_to_decimal_value(ternary) == decimal_number


@pytest.mark.parametrize("invalid_value", ["", "3", "12A", "--1", "-", "1 2"])
def test_validate_ternary_rejects_invalid_values(invalid_value: str) -> None:
    with pytest.raises(ValueError):
        validate_ternary(invalid_value)


def test_decimal_to_ternary_conversion_steps() -> None:
    assert get_conversion_steps(10) == [
        (10, 3, 1),
        (3, 1, 0),
        (1, 0, 1),
    ]


def test_ternary_place_value_rows() -> None:
    assert build_place_value_rows("101") == [
        ("1", 1, 2, 9, 9),
        ("0", 0, 1, 3, 0),
        ("1", 1, 0, 1, 1),
    ]


def test_decimal_to_ternary_verification_reports_success() -> None:
    verification = verify_decimal_to_ternary(10, "101")

    assert "(1 x 9) = 9" in verification
    assert "9 + 0 + 1 = 10" in verification
    assert "[OK] Verification Successful" in verification


def test_ternary_to_decimal_verification_reports_success() -> None:
    verification = verify_ternary_to_decimal("101")

    assert "(1 x 9) = 9" in verification
    assert "9 + 0 + 1 = 10" in verification
    assert "[OK] Verification Successful" in verification


@pytest.mark.parametrize(
    ("decimal_number", "binary"),
    [
        (0, "0"),
        (5, "101"),
        (10, "1010"),
        (-5, "-101"),
    ],
)
def test_decimal_to_binary(decimal_number: int, binary: str) -> None:
    assert decimal_to_binary(decimal_number) == binary


def test_binary_vs_ternary_comparison() -> None:
    binary, ternary, comparison = compare_binary_and_ternary(10)

    assert binary == "1010"
    assert ternary == "101"
    assert comparison == "Ternary uses fewer digits."
