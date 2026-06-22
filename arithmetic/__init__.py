"""Foundation utilities for TriCore arithmetic lessons."""

from .addition import add_many, add_numbers
from .borrow import BorrowRecord, create_borrow, normalize_borrows
from .carry import CarryRecord, create_carry, normalize_carries
from .division import divide_numbers
from .explanation import ArithmeticResult, ExplanationStep, create_step
from .multiplication import multiply_numbers
from .subtraction import subtract_numbers
from .utils import (
    BALANCED_TERNARY_DIGITS,
    ORDINARY_TERNARY_DIGITS,
    align_numbers,
    clean_input,
    compare_magnitudes,
    iter_digits_from_right,
    strip_leading_zeros,
    validate_balanced_ternary,
    validate_digits,
    validate_no_leading_zeros,
    validate_not_empty,
    validate_ordinary_ternary,
    validate_supported_base,
    validate_ternary_operand,
)

__all__ = [
    "ArithmeticResult",
    "BALANCED_TERNARY_DIGITS",
    "BorrowRecord",
    "CarryRecord",
    "ExplanationStep",
    "ORDINARY_TERNARY_DIGITS",
    "add_many",
    "add_numbers",
    "align_numbers",
    "clean_input",
    "compare_magnitudes",
    "create_borrow",
    "create_carry",
    "create_step",
    "divide_numbers",
    "iter_digits_from_right",
    "multiply_numbers",
    "normalize_borrows",
    "normalize_carries",
    "subtract_numbers",
    "strip_leading_zeros",
    "validate_balanced_ternary",
    "validate_digits",
    "validate_no_leading_zeros",
    "validate_not_empty",
    "validate_ordinary_ternary",
    "validate_supported_base",
    "validate_ternary_operand",
]
