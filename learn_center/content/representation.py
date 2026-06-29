"""Number representation lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Number Representation",
    "title": "Number Representation",
    "lessons": [
        {
            "menu_title": "Bits vs Trits",
            "title": "Bits vs Trits",
            "question": "How much information can one digit carry?",
            "sections": [
                page(
                    "Definition",
                    """
                    A bit is a binary digit. It can be 0 or 1.

                    A trit is a ternary digit. It can be 0, 1, or 2 in ordinary
                    ternary, or T, 0, or 1 in balanced ternary.

                    The important idea is the number of possible states.
                    """,
                ),
                page(
                    "Counting Patterns",
                    """
                    With n binary bits, the number of possible patterns is 2^n.

                    1 bit  gives 2 patterns
                    2 bits give 4 patterns
                    3 bits give 8 patterns

                    With n ternary trits, the number of possible patterns is 3^n.

                    1 trit  gives 3 patterns
                    2 trits give 9 patterns
                    3 trits give 27 patterns
                    """,
                ),
                page(
                    "Comparison",
                    """
                    Three trits can represent 27 patterns. Four bits can
                    represent 16 patterns, and five bits can represent 32.

                    This is why ternary notation can sometimes use fewer digit
                    positions than binary. But real computer design also depends
                    on voltage levels, noise margins, memory cells, and logic
                    gate design.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Bits belong to base 2.
                    Trits belong to base 3.
                    More states per digit can reduce digit count.
                    Hardware reliability can matter more than notation length.
                    """,
                ),
            ],
        },
        {
            "menu_title": "How Computers Store Numbers",
            "title": "How Computers Store Numbers",
            "question": "What does it mean for a computer to store a number?",
            "sections": [
                page(
                    "Definition",
                    """
                    A computer stores numbers as patterns of physical states.
                    In a typical binary memory cell, one state is interpreted as
                    0 and another state is interpreted as 1.

                    The machine does not store the idea of seventeen. It stores
                    a pattern that a circuit or program interprets as seventeen.
                    """,
                ),
                page(
                    "Fixed Width",
                    """
                    Computers usually reserve a fixed number of digits for a
                    value. An 8-bit unsigned value has 8 positions.

                    Small example:

                    00010001 in binary is 17.

                    The leading zeros do not change the value, but they matter
                    because the storage field has exactly 8 bit positions.
                    """,
                ),
                page(
                    "Interpretation",
                    """
                    The same stored pattern can mean different things depending
                    on the agreed format.

                    01000001 might be the number 65.
                    In a text encoding such as ASCII, it can represent A.

                    Storage is physical. Meaning comes from the representation
                    rule used to read the pattern.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    This idea explains many computing topics: integer overflow,
                    character encodings, image formats, machine instructions,
                    and network packets.

                    The bits or trits are the raw material. The format tells the
                    computer what those states mean.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Signed Number Representation",
            "title": "Signed Number Representation",
            "question": "How can a computer represent negative numbers?",
            "sections": [
                page(
                    "The Problem",
                    """
                    A positional numeral such as 1011 is just a pattern of
                    digits. To represent negative values, a computer needs a
                    rule for interpreting some patterns as less than zero.

                    The rule must also work well with arithmetic circuits.
                    """,
                ),
                page(
                    "Common Binary Method",
                    """
                    Most modern binary computers use two's complement for
                    signed integers.

                    In 8-bit two's complement:

                    00000001 means 1
                    11111111 means -1
                    11111110 means -2

                    This format is popular because addition hardware can handle
                    positive and negative values with the same basic operation.
                    """,
                ),
                page(
                    "Other Ideas",
                    """
                    A system could use a separate sign bit, where one position
                    records positive or negative. That is easy to understand,
                    but it creates two forms of zero and complicates arithmetic.

                    Number representation is judged by both clarity and how well
                    it supports real operations.
                    """,
                ),
                page(
                    "Ternary Connection",
                    """
                    Balanced ternary gives each digit a negative, zero, or
                    positive value. That means sign is built into the digit set.

                    This does not make hardware problems disappear, but it makes
                    the mathematical representation of negative values unusually
                    elegant.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Why Balanced Ternary is Special",
            "title": "Why Balanced Ternary is Special",
            "question": "Why do computer scientists keep returning to balanced ternary?",
            "sections": [
                page(
                    "Symmetry",
                    """
                    Balanced ternary is centered around zero. Its digit values
                    are -1, 0, and +1.

                    That symmetry makes positive and negative quantities feel
                    like mirror images of each other instead of separate cases.
                    """,
                ),
                page(
                    "Negation Example",
                    """
                    To negate a balanced ternary number, swap 1 and T.

                    1T0 means:

                    1 x 9 + T x 3 + 0 x 1 = 9 - 3 = 6

                    T10 means:

                    T x 9 + 1 x 3 + 0 x 1 = -9 + 3 = -6
                    """,
                ),
                page(
                    "Arithmetic Benefit",
                    """
                    Balanced digits can reduce the need for a separate sign
                    convention. They also make rounding and some arithmetic
                    patterns mathematically neat.

                    The tradeoff is that a real machine still needs dependable
                    three-state storage and logic, which is harder than the
                    two-state binary approach used at massive scale.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Balanced ternary is not magic. It is a positional base-3
                    system with digits chosen around zero.

                    It is special because the notation treats positive and
                    negative values symmetrically while staying compact.
                    """,
                ),
            ],
        },
    ],
}
