"""Ternary arithmetic lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Ternary Arithmetic",
    "title": "Ternary Arithmetic",
    "lessons": [
        {
            "menu_title": "Ternary Addition",
            "title": "Ternary Addition",
            "question": "How do carries work when the base is 3?",
            "sections": [
                page(
                    "Basic Rule",
                    """
                    Ordinary ternary addition works like decimal addition, but
                    a column can only hold the digits 0, 1, and 2.

                    If a column total reaches 3 or more, write the remainder
                    after division by 3 and carry the quotient to the next
                    column.
                    """,
                ),
                page(
                    "Small Facts",
                    """
                    Ternary single-column addition:

                    0 + 0 = 0
                    1 + 0 = 1
                    1 + 1 = 2
                    2 + 1 = 10 because decimal 3 is ternary 10
                    2 + 2 = 11 because decimal 4 is ternary 11
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Add ternary 122 and 21.

                       122
                    +   21
                    -----

                    Ones: 2 + 1 = 3, write 0 carry 1
                    Threes: 2 + 2 + carry 1 = 5, write 2 carry 1
                    Nines: 1 + carry 1 = 2

                    Result: 220
                    """,
                ),
                page(
                    "Check",
                    """
                    Decimal check:

                    122 ternary = 17 decimal
                    21 ternary  = 7 decimal
                    220 ternary = 24 decimal

                    17 + 7 = 24, so the ternary addition is correct.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Ternary Subtraction",
            "title": "Ternary Subtraction",
            "question": "How do borrows work in base 3?",
            "sections": [
                page(
                    "Basic Rule",
                    """
                    Ternary subtraction uses borrowing just like decimal
                    subtraction. The difference is that one borrow is worth 3
                    in the next lower column, not 10.

                    If the top digit is too small, borrow 1 from the next column
                    and add 3 to the current column.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Subtract ternary 12 from 102.

                       102
                    -   12
                    -----

                    Ones: 2 - 2 = 0
                    Threes: 0 - 1 is not possible, so borrow from the nines.
                    The 1 in the nines place becomes 0.
                    The threes column becomes 3.
                    3 - 1 = 2

                    Result: 20
                    """,
                ),
                page(
                    "Check",
                    """
                    Decimal check:

                    102 ternary = 11 decimal
                    12 ternary  = 5 decimal
                    20 ternary  = 6 decimal

                    11 - 5 = 6, so the result is correct.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Borrowing does not mean adding ten unless the base is ten.
                    In base 3, a borrow adds 3 to the current column.
                    Good subtraction depends on knowing the base of the numeral.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Ternary Multiplication",
            "title": "Ternary Multiplication",
            "question": "How does long multiplication change in ternary?",
            "sections": [
                page(
                    "Basic Rule",
                    """
                    Ternary multiplication uses the same layout as decimal long
                    multiplication. The single-digit facts and carries are in
                    base 3.

                    Important facts:

                    2 x 0 = 0
                    2 x 1 = 2
                    2 x 2 = 11 in ternary
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Multiply ternary 12 by 2.

                    12 ternary means 5 decimal.
                    2 ternary means 2 decimal.

                       12
                    x   2
                    ----

                    Ones: 2 x 2 = 4 decimal = 11 ternary.
                    Write 1, carry 1.

                    Threes: 1 x 2 + carry 1 = 3 decimal = 10 ternary.
                    Write 0, carry 1.

                    Result: 101
                    """,
                ),
                page(
                    "Place Shifts",
                    """
                    When multiplying by a digit in a higher place, shift the
                    partial product left just as you would in decimal.

                    A left shift in ternary multiplies by 3. Appending one zero
                    to 12 gives 120, which is 12 x 3 in value.
                    """,
                ),
                page(
                    "Check",
                    """
                    Decimal check:

                    12 ternary = 5 decimal
                    2 ternary  = 2 decimal
                    101 ternary = 9 + 1 = 10 decimal

                    5 x 2 = 10.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Ternary Division",
            "title": "Ternary Division",
            "question": "How does long division work with ternary digits?",
            "sections": [
                page(
                    "Basic Rule",
                    """
                    Ternary division asks how many times the divisor fits into
                    the current part of the dividend. Each quotient digit must
                    be 0, 1, or 2.

                    The arithmetic is base 3, but the long division idea is the
                    same as in decimal.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Divide ternary 101 by 2.

                    Decimal meaning:
                    101 ternary = 10 decimal
                    2 ternary = 2 decimal

                    10 / 2 = 5 decimal, and 5 decimal is 12 ternary.

                    Quotient: 12
                    Remainder: 0
                    """,
                ),
                page(
                    "Long Division Thinking",
                    """
                    In ternary terms, 2 fits into the leading 1 zero times, so
                    you consider the next digit. It fits into 10 ternary, which
                    is 3 decimal, one time with a remainder of 1.

                    Bring down the final 1 to make 11 ternary, which is 4
                    decimal. The divisor 2 fits two times with remainder 0.
                    Quotient digits are 1 then 2.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary division is not a new kind of division. It is the
                    familiar division process using base-3 digits.

                    Estimation becomes easier if you know the decimal meanings
                    of small ternary values such as 10, 11, 12, and 20.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Carry and Borrow in Base-3",
            "title": "Carry and Borrow in Base-3",
            "question": "Why are carrying and borrowing different in ternary?",
            "sections": [
                page(
                    "The Core Idea",
                    """
                    Carrying and borrowing are place-value actions. Their size
                    depends on the base.

                    In decimal, one carry into the next place is worth 10 of the
                    current place. In ternary, one carry into the next place is
                    worth 3 of the current place.
                    """,
                ),
                page(
                    "Carry Example",
                    """
                    Add one column:

                    2 + 2 = 4 decimal

                    In base 3, 4 decimal is 11 ternary. That means:

                    write 1 in the current column
                    carry 1 to the next column
                    """,
                ),
                page(
                    "Borrow Example",
                    """
                    Subtract one column:

                    0 - 1 is not possible without borrowing.

                    Borrow 1 from the next column. In the current column, that
                    borrowed 1 is worth 3.

                    Now compute 3 - 1 = 2.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Arithmetic circuits must implement these carry and borrow
                    rules physically. Binary adders carry when a column reaches
                    2. Ternary adders carry when a column reaches 3.

                    The base changes both the notation and the circuit design.
                    """,
                ),
            ],
        },
    ],
}
