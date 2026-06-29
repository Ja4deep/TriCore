"""Extra Learning Center reference lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Extras",
    "title": "Extras",
    "lessons": [
        {
            "menu_title": "Frequently Asked Questions",
            "title": "Frequently Asked Questions",
            "question": "What questions come up most often when learning ternary computing?",
            "sections": [
                page(
                    "Number Systems",
                    """
                    Q: Is ternary a different kind of number?
                    A: No. It is a different way to write quantities.

                    Q: Is 122 in ternary equal to one hundred twenty-two?
                    A: No. 122 in ternary equals 17 in decimal.

                    Q: Why learn bases other than ten?
                    A: Computers use encodings. Learning bases teaches you how
                    representation differs from value.
                    """,
                ),
                page(
                    "Binary and Ternary",
                    """
                    Q: Is ternary better than binary?
                    A: Not automatically. Ternary has interesting mathematical
                    properties, but binary is easier to build reliably at scale.

                    Q: What is a trit?
                    A: A ternary digit, similar to how a bit is a binary digit.
                    """,
                ),
                page(
                    "Balanced Ternary",
                    """
                    Q: What does T mean?
                    A: In TriCore, T means -1 in balanced ternary.

                    Q: Why not use the digit 2?
                    A: Balanced ternary uses -1, 0, and +1 instead of 0, 1, and
                    2. It is still base 3 because the place values are powers of
                    3.
                    """,
                ),
                page(
                    "Computers",
                    """
                    Q: Did ternary computers really exist?
                    A: Yes. Setun, built at Moscow State University in the late
                    1950s, is a well-known balanced ternary example.

                    Q: Do modern computers use ternary?
                    A: General-purpose modern computers are overwhelmingly
                    binary, though non-binary computing remains a research area.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Fun Facts",
            "title": "Fun Facts",
            "question": "What memorable facts help connect the course ideas?",
            "sections": [
                page(
                    "Powers of Three",
                    """
                    Ternary place values grow as:

                    1, 3, 9, 27, 81, 243

                    This growth is why ternary representations can be shorter
                    than binary representations for some values.
                    """,
                ),
                page(
                    "Balanced Negation",
                    """
                    Balanced ternary has a neat negation rule.

                    Swap 1 and T:

                    1T01 becomes T10T

                    That works because every digit value has an opposite digit
                    value, except 0, which is already its own opposite.
                    """,
                ),
                page(
                    "Base 3 and Efficiency",
                    """
                    In mathematical discussions of radix economy, base 3 often
                    appears because it is close to the number e, about 2.718.

                    This is an interesting theoretical observation, not a proof
                    that ternary chips are automatically better than binary
                    chips.
                    """,
                ),
                page(
                    "History",
                    """
                    Setun is remembered because it used balanced ternary in real
                    hardware. It is a useful reminder that computing history was
                    not a straight line from one obvious idea to the present.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Glossary of Terms",
            "title": "Glossary of Terms",
            "question": "What vocabulary should a beginner know?",
            "sections": [
                page(
                    "Number Terms",
                    """
                    Base: The number of digit values available in a positional
                    number system.

                    Digit: One symbol in a numeral.

                    Place value: The weight of a digit's position, such as ones,
                    threes, nines, or sixteens.

                    Numeral: The written form of a number.
                    """,
                ),
                page(
                    "Binary and Ternary Terms",
                    """
                    Bit: A binary digit, either 0 or 1.

                    Trit: A ternary digit.

                    Ordinary ternary: Base 3 using 0, 1, and 2.

                    Balanced ternary: Base 3 using digit values -1, 0, and +1.
                    """,
                ),
                page(
                    "Logic Terms",
                    """
                    Logic gate: A component that maps input signals to an output
                    signal according to a rule.

                    Truth table: A table listing every input combination and the
                    output for each case.

                    Signal: A physical or simulated value interpreted as a logic
                    state.
                    """,
                ),
                page(
                    "Architecture Terms",
                    """
                    Circuit: A connected network of components.

                    Combinational circuit: A circuit whose output depends only
                    on current inputs.

                    Computer architecture: The organization of a computer's
                    processing, memory, instructions, and data paths.
                    """,
                ),
            ],
        },
    ],
}
