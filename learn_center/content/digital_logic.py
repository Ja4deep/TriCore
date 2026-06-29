"""Digital logic lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Digital Logic",
    "title": "Digital Logic",
    "lessons": [
        {
            "menu_title": "What is Digital Logic?",
            "title": "What is Digital Logic?",
            "question": "How do circuits process information using discrete signal levels?",
            "sections": [
                page(
                    "Definition",
                    """
                    Digital logic is the study of circuits that operate on a
                    finite set of discrete signal values.

                    Different digital systems choose different signal sets:

                    Binary logic uses two states: 0 and 1.
                    Ordinary ternary logic uses three states: 0, 1, and 2.
                    Balanced ternary logic uses three values: -1, 0, and +1.

                    A signal is not a mathematical digit floating in space. In
                    hardware, it is a physical condition such as a voltage range
                    that the circuit interprets as a digit.
                    """,
                ),
                page(
                    "Why Discrete Values Help",
                    """
                    Real electrical signals are messy. They rise, fall, and pick
                    up noise. Digital systems simplify this by grouping ranges
                    of physical values into symbolic states.

                    A binary circuit usually separates two ranges, such as low
                    and high. A ternary circuit separates three ranges, such as
                    low, middle, and high.

                    In both cases, the circuit is not measuring a perfect
                    mathematical value. It is deciding which allowed range the
                    signal belongs to.
                    """,
                ),
                page(
                    "From Logic to Computation",
                    """
                    Logic gates combine input signals to produce output signals.
                    The same general idea works for binary gates and ternary
                    gates; the difference is the number of states each gate must
                    handle.

                    Many gates connected together can add numbers, compare
                    values, choose instructions, address memory, and control a
                    processor.

                    Computer architecture is built from layers of digital logic.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Digital logic uses a finite set of signal states.
                    Gates are small decision-making circuits.
                    Binary and ternary logic are two implementations of the same
                    broader digital-logic idea.
                    Complex computers are built by organizing many simple logic
                    operations into larger systems.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Logic Gates",
            "title": "Logic Gates",
            "question": "What does a logic gate do?",
            "sections": [
                page(
                    "Definition",
                    """
                    A logic gate is a circuit or model that takes input values
                    and produces an output value according to a rule.

                    The rule depends on the logic system. Binary gates operate
                    on two possible input states. Ternary gates operate on three
                    possible input states.
                    """,
                ),
                page(
                    "Binary and Ternary Examples",
                    """
                    Binary NOT flips one input:

                    NOT 0 = 1
                    NOT 1 = 0

                    A ternary NOT rule must define three cases. TriCore's
                    ternary NOT uses 2 - x:

                    NOT 0 = 2
                    NOT 1 = 1
                    NOT 2 = 0

                    Both are gates. They differ because the signal alphabets are
                    different.
                    """,
                ),
                page(
                    "Why Gates Matter",
                    """
                    Gates are the basic vocabulary of digital circuits. An
                    adder, for example, can be built from gates that combine
                    input digits and carry digits.

                    A processor contains huge numbers of gate-level operations,
                    even when programmers usually see a higher-level language.
                    """,
                ),
                page(
                    "Ternary Connection",
                    """
                    Ternary logic gates also map inputs to outputs, but the
                    inputs may have three possible values. The exact rule must
                    be defined carefully because there are more possible input
                    combinations than in binary logic.

                    You can experiment with these rules in TriCore's Digital
                    Logic Laboratory.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Truth Tables",
            "title": "Truth Tables",
            "question": "How can every input-output case be shown clearly?",
            "sections": [
                page(
                    "Definition",
                    """
                    A truth table lists every possible input combination for a
                    logic operation and shows the output for each combination.

                    It is a complete, compact description of a gate's behavior.
                    Truth tables work for any finite logic system, including
                    binary and ternary logic.
                    """,
                ),
                page(
                    "Binary AND Table",
                    """
                    A  B  A AND B
                    0  0     0
                    0  1     0
                    1  0     0
                    1  1     1

                    The output is 1 only in the final row because both inputs
                    are 1 only in that row.
                    """,
                ),
                page(
                    "Ternary Table Size",
                    """
                    A two-input binary gate has 2 x 2 = 4 input rows.

                    A two-input ternary gate has 3 x 3 = 9 input rows.

                    More signal states mean more cases to define and test. This
                    is one reason ternary logic requires careful design.
                    """,
                ),
                page(
                    "Practical Application",
                    """
                    Truth tables help circuit designers verify that a gate or
                    circuit matches the intended rule. They also help students
                    debug logic because every possible input case is visible.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Binary Logic vs Ternary Logic",
            "title": "Binary Logic vs Ternary Logic",
            "question": "What changes when logic has three values instead of two?",
            "sections": [
                page(
                    "Binary Logic",
                    """
                    Digital logic can use different finite sets of states. The
                    comparison below focuses on the two systems TriCore studies
                    most:

                    Binary logic has two values. They are often described as
                    false and true, low and high, or 0 and 1.

                    With two values, the behavior of common gates is simple and
                    the hardware distinction between states can be wide.
                    """,
                ),
                page(
                    "Ternary Logic",
                    """
                    Ternary logic has three values. Depending on the system,
                    these might be 0, 1, 2 or negative, zero, positive.

                    The middle value can represent a real third state, not just
                    an error. Designers must define exactly what each operation
                    means for all three values.
                    """,
                ),
                page(
                    "Comparison",
                    """
                    Binary two-input gate rows: 4
                    Ternary two-input gate rows: 9

                    Binary three-input gate rows: 8
                    Ternary three-input gate rows: 27

                    Ternary can express more per digit, but the design space
                    grows quickly.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    A ternary computer is not made by simply renaming binary
                    bits. The storage cells, gates, truth tables, arithmetic
                    circuits, and signal rules all need to support three
                    dependable states.

                    The same general computer-science concepts still apply:
                    representation, logic, arithmetic, memory, and control.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Universal Gates",
            "title": "Universal Gates",
            "question": "How can one kind of gate build many kinds of logic?",
            "sections": [
                page(
                    "Definition",
                    """
                    A universal gate is a gate type that can be combined to
                    build any logic operation in a given logic system.

                    In binary logic, NAND is universal. NOR is also universal.
                    In ternary logic, universality depends on the specific
                    three-valued operations chosen.
                    """,
                ),
                page(
                    "NAND Example",
                    """
                    NAND means NOT AND.

                    A  B  A NAND B
                    0  0      1
                    0  1      1
                    1  0      1
                    1  1      0

                    If both NAND inputs are tied together, the gate acts like
                    NOT: A NAND A equals NOT A.
                    """,
                ),
                page(
                    "Why This Matters",
                    """
                    Universal gates simplify manufacturing and theory. If a
                    designer can build a reliable NAND gate, larger circuits can
                    be constructed from repeated NAND combinations.

                    Real chips use many optimized gate structures, but
                    universality is a powerful design concept.
                    """,
                ),
                page(
                    "Ternary Caution",
                    """
                    Universality depends on the exact logic system. Ternary
                    logic has multiple possible definitions for operations such
                    as inversion, minimum, maximum, and implication.

                    A universal set must be proven for the chosen ternary logic,
                    not assumed from the binary case.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Signal Levels in Ternary Logic",
            "title": "Signal Levels in Ternary Logic",
            "question": "What would three logic states mean in real hardware?",
            "sections": [
                page(
                    "Physical Meaning",
                    """
                    A ternary circuit needs three distinguishable signal states.
                    One possible design is low, middle, and high voltage.

                    The exact voltages are engineering choices. What matters is
                    that the circuit can reliably tell the states apart.
                    This is the ternary version of a general digital-design
                    problem: map physical signals onto symbolic values.
                    """,
                ),
                page(
                    "Binary and Ternary Noise Margins",
                    """
                    Noise margin is the tolerance a circuit has before a signal
                    might be read incorrectly.

                    With two states, the distance between low and high can be
                    large. With three states in the same voltage range, the
                    states are closer together, so noise margins can become
                    smaller.
                    """,
                ),
                page(
                    "Balanced Interpretation",
                    """
                    Balanced ternary often maps naturally to negative, zero, and
                    positive ideas. In hardware, that might suggest negative,
                    zero, and positive voltages, though actual implementations
                    can vary.

                    The mathematical digit set and the physical signal design
                    must be connected by a clear encoding rule.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary logic needs three stable, readable states.
                    More states can increase information density.
                    More states can also make circuits harder to build reliably,
                    especially at high speed and small scale.
                    """,
                ),
            ],
        },
    ],
}
