"""Logic circuit simulator lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Logic Circuit Simulator",
    "title": "Logic Circuit Simulator",
    "lessons": [
        {
            "menu_title": "What is a Logic Circuit?",
            "title": "What is a Logic Circuit?",
            "question": "How do gates become a circuit?",
            "sections": [
                page(
                    "Definition",
                    """
                    A logic circuit is a network of connected logic components.
                    Inputs enter the circuit, gates transform the signals, and
                    outputs report the final values.

                    A circuit can be drawn as a diagram or represented as data
                    inside a simulator.
                    """,
                ),
                page(
                    "Simple Example",
                    """
                    Suppose inputs A and B feed an AND gate.

                    A = 1
                    B = 0

                    AND outputs 1 only if both inputs are 1, so the output is 0.

                    The circuit is small, but it already has inputs, a rule, and
                    an output.
                    """,
                ),
                page(
                    "Why Simulation Helps",
                    """
                    A simulator lets you test circuit behavior before building
                    hardware. It can show intermediate signals and help you find
                    mistakes in connections or gate choices.

                    In education, simulation makes invisible signal flow easier
                    to reason about.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    A circuit is more than a list of gates.
                    Connections determine how signals move.
                    Inputs, gates, and outputs together define behavior.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Signal Propagation",
            "title": "Signal Propagation",
            "question": "How does a value move through a circuit?",
            "sections": [
                page(
                    "Definition",
                    """
                    Signal propagation is the movement of values from inputs
                    through gates toward outputs.

                    In a simulator, propagation happens as an ordered evaluation
                    of connected components. In hardware, propagation takes a
                    small amount of physical time.
                    """,
                ),
                page(
                    "Step Example",
                    """
                    Circuit:

                    A and B feed AND gate G1.
                    G1 and C feed OR gate G2.

                    If A = 1, B = 1, and C = 0:

                    G1 becomes 1 because 1 AND 1 = 1.
                    G2 becomes 1 because 1 OR 0 = 1.
                    """,
                ),
                page(
                    "Why Order Matters",
                    """
                    A gate cannot be evaluated until its needed inputs are
                    available. Simulators often track dependencies so that gates
                    are evaluated after the components that feed them.

                    Badly formed circuits, such as unsupported feedback loops,
                    may not have a simple evaluation order.
                    """,
                ),
                page(
                    "Practical Application",
                    """
                    Propagation explains why real circuits have delay. A large
                    processor must be designed so that signals settle before
                    the next clocked step uses them.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Series vs Parallel Gates",
            "title": "Series vs Parallel Gates",
            "question": "How does circuit shape affect logic behavior?",
            "sections": [
                page(
                    "Series Idea",
                    """
                    In a series-style logic path, the output of one gate feeds
                    another gate. The second gate depends on the first.

                    Example:

                    A and B feed AND.
                    The AND output and C feed OR.
                    """,
                ),
                page(
                    "Parallel Idea",
                    """
                    In a parallel-style logic structure, multiple gates evaluate
                    separate input combinations at the same level.

                    Example:

                    A and B feed one AND gate.
                    C and D feed another AND gate.
                    The two outputs are compared or combined later.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Series paths can create longer delays because a signal must
                    pass through more gate levels. Parallel structures can
                    compute several intermediate results at the same time.

                    Circuit designers care about both correctness and timing.
                    """,
                ),
                page(
                    "Simulator Connection",
                    """
                    When building circuits in TriCore, watch which component
                    feeds which input. A wrong connection can turn a parallel
                    design into a series design or change the final truth table.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Circuit Evaluation",
            "title": "Circuit Evaluation",
            "question": "How does a simulator decide the output of a circuit?",
            "sections": [
                page(
                    "Definition",
                    """
                    Circuit evaluation means computing the output values from
                    the input values and the gate rules.

                    The simulator reads the circuit structure, validates the
                    connections, then evaluates components in an order that
                    respects signal dependencies.
                    """,
                ),
                page(
                    "Evaluation Steps",
                    """
                    A typical evaluation flow is:

                    1. Read input pin values.
                    2. Evaluate gates whose inputs are ready.
                    3. Store each gate output.
                    4. Continue until output pins can be read.
                    5. Report the final output values.
                    """,
                ),
                page(
                    "Worked Example",
                    """
                    Inputs:

                    A = 1
                    B = 0
                    C = 1

                    Gate G1 = A OR B, so G1 = 1.
                    Gate G2 = G1 AND C, so G2 = 1.

                    Output connected to G2 is 1.
                    """,
                ),
                page(
                    "Common Problems",
                    """
                    Missing inputs, invalid signal values, unsupported gate
                    names, and circular dependencies can prevent evaluation.

                    A good simulator reports these problems instead of silently
                    producing a misleading output.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Combinational Circuits",
            "title": "Combinational Circuits",
            "question": "What kind of circuit depends only on current inputs?",
            "sections": [
                page(
                    "Definition",
                    """
                    A combinational circuit is a circuit whose outputs depend
                    only on the current input values.

                    It has no memory of earlier inputs. If the same inputs are
                    applied again, the same outputs should appear again.
                    """,
                ),
                page(
                    "Examples",
                    """
                    Common binary combinational circuits include:

                    adders
                    multiplexers
                    decoders
                    comparators

                    Ternary versions can be designed too, but their truth tables
                    and signal rules must handle three states.
                    """,
                ),
                page(
                    "Contrast With Memory",
                    """
                    A memory circuit, or sequential circuit, can depend on
                    previous state. A latch or flip-flop remembers information.

                    TriCore's beginner circuit simulations focus on
                    combinational behavior because it is easier to inspect and
                    reason about step by step.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Arithmetic units, condition checks, and instruction decode
                    logic often use combinational circuits. They are core
                    building blocks inside CPUs.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Building a Ternary Circuit",
            "title": "Building a Ternary Circuit",
            "question": "What should you decide before simulating ternary logic?",
            "sections": [
                page(
                    "Choose Signal Values",
                    """
                    First decide what the three signal values mean.

                    Ordinary ternary might use 0, 1, and 2.
                    Balanced ternary might use T, 0, and 1.

                    The rest of the circuit must follow that choice
                    consistently.
                    """,
                ),
                page(
                    "Define Gate Rules",
                    """
                    A ternary gate needs a complete rule for every possible
                    input combination.

                    For a two-input gate, that means 9 combinations. For three
                    inputs, that means 27 combinations.

                    A name like AND is not enough unless the ternary version of
                    AND has been defined.
                    """,
                ),
                page(
                    "Test Small Pieces",
                    """
                    Build and test small circuits first.

                    Confirm one gate's truth table.
                    Then connect two gates.
                    Then inspect intermediate outputs before trusting the final
                    result.

                    This mirrors real engineering practice: test components
                    before relying on the full system.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary circuit design requires clear encodings, complete
                    truth tables, and careful testing.

                    Simulation is useful because it exposes signal values and
                    connection mistakes before any hardware exists.
                    """,
                ),
            ],
        },
    ],
}
