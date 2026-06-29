"""Foundations of number systems lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Foundations of Number Systems",
    "title": "Foundations of Number Systems",
    "lessons": [
        {
            "menu_title": "What is a Number System?",
            "title": "What is a Number System?",
            "question": "What does it mean to write a number in a system?",
            "sections": [
                page(
                    "Definition",
                    """
                    A number system is a method for writing quantities using a
                    set of symbols and rules. The symbols are digits. The rules
                    explain how the position of each digit changes its value.

                    The quantity seventeen can be written as 17 in decimal,
                    10001 in binary, or 122 in ternary. The quantity has not
                    changed. Only the representation has changed.
                    """,
                ),
                page(
                    "Place Value",
                    """
                    Most number systems used in computing are positional. That
                    means a digit means different things depending on where it
                    appears.

                    In decimal, 327 means:

                    3 x 100 = 300
                    2 x 10  = 20
                    7 x 1   = 7

                    The same digit 3 would mean thirty in 37, but three hundred
                    in 327. Position gives the digit its weight.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Computers store and process information as physical states.
                    A number system tells us how to interpret those states as
                    values.

                    When you learn binary or ternary, you are not learning
                    strange new numbers. You are learning new encodings for the
                    same quantities you already understand.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    A number is a quantity.
                    A numeral is a written representation of that quantity.
                    A base tells how many digit values are available.
                    Positional notation uses powers of the base as place values.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Decimal Number System",
            "title": "Decimal Number System",
            "question": "Why is decimal familiar, and how does it work?",
            "sections": [
                page(
                    "Definition",
                    """
                    Decimal is base 10. It uses ten digit symbols:

                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9

                    After 9, there is no single digit for the next quantity, so
                    the system carries into the next place and writes 10.
                    """,
                ),
                page(
                    "Powers of Ten",
                    """
                    Decimal place values are powers of 10.

                    10^0 = 1
                    10^1 = 10
                    10^2 = 100
                    10^3 = 1000

                    The number 2048 means:

                    2 x 1000 + 0 x 100 + 4 x 10 + 8 x 1
                    """,
                ),
                page(
                    "Why Humans Use It",
                    """
                    Decimal is common in everyday life partly because humans
                    have used finger counting for a very long time. That is a
                    cultural and historical reason, not a law of mathematics.

                    Computers do not need to use decimal internally. They use
                    the number system that best fits their hardware.
                    """,
                ),
                page(
                    "Comparison",
                    """
                    Decimal is comfortable for people because we practice it
                    constantly. Binary and ternary feel unfamiliar at first
                    because their place values grow by 2 or 3 instead of 10.

                    The core idea is the same: multiply each digit by its place
                    value, then add the results.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Binary Number System",
            "title": "Binary Number System",
            "question": "How can two digits represent every whole number?",
            "sections": [
                page(
                    "Definition",
                    """
                    Binary is base 2. It uses only two digits:

                    0 and 1

                    Each position is worth a power of 2. A binary digit is
                    called a bit, short for binary digit.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Convert binary 10001 to decimal.

                    Place values: 16  8  4  2  1
                    Digits:        1  0  0  0  1

                    1 x 16 = 16
                    0 x 8  = 0
                    0 x 4  = 0
                    0 x 2  = 0
                    1 x 1  = 1

                    10001 in binary equals 17 in decimal.
                    """,
                ),
                page(
                    "Hardware Connection",
                    """
                    Binary matches electronic switching very well. A circuit
                    can treat one voltage range as 0 and another voltage range
                    as 1.

                    Real circuits are not perfect, but two well-separated states
                    are easier to detect reliably than many crowded states.
                    That reliability is a major reason binary dominates modern
                    digital computers.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Binary uses powers of 2.
                    A bit has two possible values.
                    Long binary patterns can encode numbers, text, images,
                    instructions, sound, and many other kinds of data.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Ternary Number System",
            "title": "Ternary Number System",
            "question": "How does ordinary ternary represent values?",
            "sections": [
                page(
                    "Definition",
                    """
                    Ordinary ternary is base 3. It uses three digits:

                    0, 1, and 2

                    A ternary digit is called a trit. Each position is worth a
                    power of 3: 1, 3, 9, 27, 81, and so on.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Convert ternary 122 to decimal.

                    Place values: 9  3  1
                    Digits:       1  2  2

                    1 x 9 = 9
                    2 x 3 = 6
                    2 x 1 = 2

                    9 + 6 + 2 = 17

                    So 122 in ternary equals 17 in decimal.
                    """,
                ),
                page(
                    "Comparison With Binary",
                    """
                    Ternary carries more information per digit than binary
                    because each trit has three possible values instead of two.

                    Decimal 17:

                    Binary  : 10001
                    Ternary : 122

                    The ternary form is shorter here, but shorter notation does
                    not automatically mean easier hardware.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Ternary is useful for studying how bases work because it is
                    close to binary but introduces a third state. It also leads
                    naturally into balanced ternary, where digits can represent
                    negative, zero, and positive values.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Balanced Ternary",
            "title": "Balanced Ternary",
            "question": "What changes when ternary digits are balanced around zero?",
            "sections": [
                page(
                    "Definition",
                    """
                    Balanced ternary is base 3, but its digit values are:

                    T = -1
                    0 = 0
                    1 = +1

                    Many books use a barred 1 for -1. TriCore uses T because it
                    is easy to type in a terminal.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Convert balanced ternary 1T1 to decimal.

                    Place values: 9   3   1
                    Digits:       1   T   1
                    Values:      +1  -1  +1

                    1 x 9  = 9
                    T x 3  = -3
                    1 x 1  = 1

                    9 - 3 + 1 = 7
                    """,
                ),
                page(
                    "Why It Is Special",
                    """
                    Balanced ternary represents positive and negative values
                    symmetrically. To negate a number, swap every 1 with T and
                    every T with 1. Zeros stay zero.

                    Example:

                    1T1 represents 7.
                    T1T represents -7.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ordinary ternary digits are 0, 1, and 2.
                    Balanced ternary digit values are -1, 0, and +1.
                    Balanced ternary can express signs inside the digits rather
                    than by attaching a separate minus sign to the whole number.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Positional Number Systems",
            "title": "Positional Number Systems",
            "question": "How do place values make compact notation possible?",
            "sections": [
                page(
                    "Definition",
                    """
                    In a positional number system, a digit's position determines
                    its weight. The rightmost place is usually the ones place.
                    Moving left multiplies the place value by the base.

                    This lets a small set of digit symbols represent very large
                    quantities.
                    """,
                ),
                page(
                    "Three Bases Side by Side",
                    """
                    Decimal 231:

                    2 x 100 + 3 x 10 + 1 x 1

                    Binary 1011:

                    1 x 8 + 0 x 4 + 1 x 2 + 1 x 1 = 11

                    Ternary 102:

                    1 x 9 + 0 x 3 + 2 x 1 = 11
                    """,
                ),
                page(
                    "Common Mistake",
                    """
                    Students sometimes read 102 in ternary as one hundred two.
                    That phrase belongs to decimal language.

                    In ternary, 102 means one 9, zero 3s, and two 1s. Its
                    decimal value is 11.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Conversion, arithmetic, memory addresses, instruction
                    encodings, and digital logic all rely on place-value
                    thinking. Once positional notation is clear, binary and
                    ternary become much less mysterious.
                    """,
                ),
            ],
        },
    ],
}
