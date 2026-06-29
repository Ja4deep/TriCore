"""Number system conversion lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Number System Conversion",
    "title": "Number System Conversion",
    "lessons": [
        {
            "menu_title": "Decimal to/from Binary",
            "title": "Decimal to/from Binary",
            "question": "How do decimal and binary forms describe the same value?",
            "sections": [
                page(
                    "Binary to Decimal",
                    """
                    To convert binary to decimal, multiply each bit by its
                    place value and add the results.

                    Binary 10110:

                    Place values: 16  8  4  2  1
                    Bits:          1  0  1  1  0

                    16 + 0 + 4 + 2 + 0 = 22
                    """,
                ),
                page(
                    "Decimal to Binary",
                    """
                    To convert decimal to binary, repeatedly divide by 2 and
                    record the remainders.

                    Convert 22:

                    22 / 2 = 11 remainder 0
                    11 / 2 = 5  remainder 1
                    5  / 2 = 2  remainder 1
                    2  / 2 = 1  remainder 0
                    1  / 2 = 0  remainder 1

                    Read remainders upward: 10110.
                    """,
                ),
                page(
                    "Why It Works",
                    """
                    Each division by 2 peels off the next lowest binary digit.
                    The remainder tells whether the current value has a 1 or 0
                    in that place.

                    Reading upward restores the digits from highest place value
                    to lowest place value.
                    """,
                ),
                page(
                    "Practical Application",
                    """
                    Binary conversion appears in debugging, memory inspection,
                    bit masks, instruction encodings, and network protocols.
                    Even when tools do the conversion, understanding the method
                    helps you see what the machine is storing.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Decimal to/from Ternary",
            "title": "Decimal to/from Ternary",
            "question": "How do decimal and ordinary ternary convert into each other?",
            "sections": [
                page(
                    "Ternary to Decimal",
                    """
                    Ternary uses powers of 3.

                    Convert ternary 2012:

                    Place values: 27  9  3  1
                    Digits:        2  0  1  2

                    2 x 27 = 54
                    0 x 9  = 0
                    1 x 3  = 3
                    2 x 1  = 2

                    Total: 59
                    """,
                ),
                page(
                    "Decimal to Ternary",
                    """
                    To convert decimal to ternary, divide by 3 and record
                    remainders.

                    Convert 59:

                    59 / 3 = 19 remainder 2
                    19 / 3 = 6  remainder 1
                    6  / 3 = 2  remainder 0
                    2  / 3 = 0  remainder 2

                    Read upward: 2012.
                    """,
                ),
                page(
                    "Comparison",
                    """
                    The conversion method is the same as binary conversion. The
                    base changes from 2 to 3, so the allowed remainders become
                    0, 1, and 2.

                    Decimal 17 becomes 10001 in binary but 122 in ternary.
                    Both notations point to the same quantity.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary place values are 1, 3, 9, 27, and so on.
                    Dividing by 3 finds ternary digits from right to left.
                    Expanding by place values converts ternary back to decimal.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Binary to/from Ternary",
            "title": "Binary to/from Ternary",
            "question": "Should binary and ternary be converted directly?",
            "sections": [
                page(
                    "Reliable Method",
                    """
                    The simplest reliable method is to use decimal as a bridge:

                    binary to decimal to ternary
                    ternary to decimal to binary

                    This avoids mistakes because each step uses familiar place
                    value rules.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Convert binary 10001 to ternary.

                    First convert binary to decimal:

                    1 x 16 + 0 x 8 + 0 x 4 + 0 x 2 + 1 x 1 = 17

                    Now convert decimal 17 to ternary:

                    17 / 3 = 5 remainder 2
                    5  / 3 = 1 remainder 2
                    1  / 3 = 0 remainder 1

                    Read upward: 122.
                    """,
                ),
                page(
                    "Why Direct Grouping Is Different",
                    """
                    Binary and octal or hexadecimal convert neatly by grouping
                    bits because 8 and 16 are powers of 2.

                    Ternary is base 3, and 3 is not a power of 2. There is no
                    simple fixed-size bit grouping that perfectly maps to one
                    ternary digit.
                    """,
                ),
                page(
                    "Practical Advice",
                    """
                    For hand conversion, use decimal as the bridge unless a
                    problem gives a special algorithm.

                    For programs, convert the value mathematically rather than
                    trying to rewrite digit strings by visual pattern alone.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Balanced Ternary Conversion",
            "title": "Balanced Ternary Conversion",
            "question": "How do we convert values when a digit can be negative?",
            "sections": [
                page(
                    "Reading Balanced Ternary",
                    """
                    Reading balanced ternary is straightforward: multiply each
                    digit value by its place value.

                    T = -1, 0 = 0, 1 = +1

                    Balanced ternary 1T0T:

                    1 x 27 + T x 9 + 0 x 3 + T x 1
                    27 - 9 + 0 - 1 = 17
                    """,
                ),
                page(
                    "Writing Balanced Ternary",
                    """
                    One conversion method repeatedly divides by 3, but adjusts
                    remainder 2 into -1 with a carry.

                    Convert decimal 17:

                    17 / 3 = 5 remainder 2
                    Write T and carry 1 because 2 is the same as -1 plus 3.

                    5 + 1 = 6
                    6 / 3 = 2 remainder 0
                    2 / 3 = 0 remainder 2
                    Write T and carry 1.

                    Final carry is 1, so the result is 1T0T.
                    """,
                ),
                page(
                    "Check the Result",
                    """
                    Verify 1T0T:

                    Place values: 27  9  3  1
                    Digits:        1  T  0  T

                    27 - 9 + 0 - 1 = 17

                    Verification is important because the carry adjustment feels
                    unusual until you have practiced it.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Balanced ternary uses the same powers of 3 as ordinary
                    ternary.
                    Digit T contributes a negative place value.
                    Remainder 2 can be handled as T with a carry into the next
                    higher place.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Common Conversion Mistakes",
            "title": "Common Conversion Mistakes",
            "question": "What errors should students watch for when changing bases?",
            "sections": [
                page(
                    "Mistake 1: Reading Digits as Decimal",
                    """
                    The ternary numeral 102 is not one hundred two. It is:

                    1 x 9 + 0 x 3 + 2 x 1 = 11

                    Say "one-zero-two in base three" if that helps you avoid
                    decimal habits.
                    """,
                ),
                page(
                    "Mistake 2: Reversing Remainders",
                    """
                    In repeated division, the first remainder is the rightmost
                    digit. The last remainder is the leftmost digit.

                    Decimal 17 to ternary:

                    17 / 3 gives remainder 2
                    5  / 3 gives remainder 2
                    1  / 3 gives remainder 1

                    The answer is 122, not 221.
                    """,
                ),
                page(
                    "Mistake 3: Invalid Digits",
                    """
                    Each base has a limited digit set.

                    Binary allows only 0 and 1.
                    Ordinary ternary allows only 0, 1, and 2.
                    Balanced ternary in TriCore allows T, 0, and 1.

                    A numeral such as 102 is invalid in binary because binary
                    has no digit 2.
                    """,
                ),
                page(
                    "How to Check Yourself",
                    """
                    Convert your answer back to decimal. If the value matches
                    the original number, your conversion is probably correct.

                    Also check the largest place value. A valid representation
                    should not start with unnecessary leading zeros unless a
                    fixed-width storage format requires them.
                    """,
                ),
            ],
        },
    ],
}
