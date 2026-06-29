"""Beginner-friendly lessons for the Digital Logic Laboratory."""

from __future__ import annotations

from typing import TypedDict

LessonSection = tuple[str, list[str]]


class Lesson(TypedDict):
    """A single Digital Logic Laboratory lesson."""

    menu_title: str
    title: str
    definition: str
    sections: list[LessonSection]


LESSONS: list[Lesson] = [
    {
        "menu_title": "Ternary Signals",
        "title": "Ternary Signals",
        "definition": "A ternary signal has three stable states: LOW, MID, and HIGH.",
        "sections": [
            (
                "Explanation",
                [
                    "Ternary computers use three voltage levels to represent 0, 1, and 2. ",
                    "Some ternary systems use balanced ternary values (-1, 0, +1), while TriCore uses 0, 1, and 2. ",
                    "Using three states increases information density per wire compared to binary.",
                ],
            ),
            (
                "Examples",
                [
                    "A three-way switch.",
                    "A trit in memory can store 0, 1, or 2.",
                ],
            ),
            (
                "Real Hardware Example",
                [
                    "Specialized transistors or multi-threshold CMOS can represent three levels.",
                    "Historical ternary computers like Setun used magnetic cores.",
                ],
            ),
            (
                "Key Concepts",
                [
                    "Trit",
                    "LOW, MID, and HIGH",
                    "Information density",
                ],
            ),
            (
                "Summary",
                ["Ternary signals are the foundation for three-valued logic."],
            ),
        ],
    },
    {
        "menu_title": "Logic Gates",
        "title": "Logic Gates",
        "definition": "A logic gate is a small circuit that applies a ternary rule.",
        "sections": [
            (
                "Explanation",
                [
                    "Gates transform input trits into output trits.",
                    "MIN, MAX, and NOT are basic building blocks.",
                    "NMIN and NMAX are universal gates because they can build all other logic.",
                ],
            ),
            (
                "Examples",
                [
                    "MIN can check whether two conditions are both HIGH.",
                    "SUM can check whether two trits are different (modulo 3).",
                ],
            ),
            (
                "Did You Know?",
                [
                    "NMIN and NMAX are called universal gates.",
                    "A processor could be built from only NMIN gates or only NMAX gates.",
                ],
            ),
            (
                "Key Concepts",
                ["Input", "Output", "Ternary logic rule", "Universal gate"],
            ),
            (
                "Summary",
                ["Large circuits are built from many small gate decisions."],
            ),
        ],
    },
    {
        "menu_title": "Ternary Logic",
        "title": "Ternary Logic",
        "definition": "Ternary logic is math for three-valued signals.",
        "sections": [
            (
                "Explanation",
                [
                    "Ternary logic uses operators such as NOT, MIN, and MAX.",
                    "It lets engineers simplify digital circuits before building them.",
                ],
            ),
            (
                "Examples",
                [
                    "A MIN 2 = A",
                    "A MAX 0 = A",
                    "NOT(2) = 0",
                ],
            ),
            (
                "Real Hardware Example",
                [
                    "Simplifying ternary logic expressions can reduce the number of gates required in a circuit.",
                    "Fewer gates can mean less area, less power, and less delay.",
                ],
            ),
            (
                "Key Concepts",
                ["Identity", "Complement", "De Morgan's laws"],
            ),
            (
                "Summary",
                ["Logic algebra connects symbolic expressions to real hardware."],
            ),
        ],
    },
    {
        "menu_title": "Truth Tables",
        "title": "Truth Tables",
        "definition": "A truth table lists every input pattern and output.",
        "sections": [
            (
                "Explanation",
                [
                    "For n ternary inputs, a complete truth table has 3^n rows.",
                    "Each row shows exactly what the circuit does for one case.",
                ],
            ),
            (
                "Examples",
                [
                    "A two-input MIN gate has nine rows.",
                    "The output is the minimum of the two inputs.",
                ],
            ),
            (
                "Did You Know?",
                [
                    "Hardware designers use truth tables to check circuit behavior.",
                    "They are small, complete specifications for combinational logic.",
                ],
            ),
            (
                "Key Concepts",
                ["Input combination", "Output column", "Exhaustive testing"],
            ),
            (
                "Summary",
                ["Truth tables make circuit behavior explicit and checkable."],
            ),
        ],
    },
    {
        "menu_title": "Combinational Logic",
        "title": "Combinational Logic",
        "definition": "Combinational logic depends only on current inputs.",
        "sections": [
            (
                "Explanation",
                [
                    "A combinational circuit has no memory of previous inputs.",
                    "Adders, multiplexers, and decoders are common examples.",
                ],
            ),
            (
                "Examples",
                [
                    "A half adder uses SUM for the sum and specialized gates for the carry.",
                    "A decoder turns ternary input trits into one selected output line.",
                ],
            ),
            (
                "Real Hardware Example",
                [
                    "The arithmetic logic unit inside a CPU is built from combinational blocks.",
                    "For the same inputs, a combinational block always gives the same output.",
                ],
            ),
            (
                "Key Concepts",
                ["Current inputs", "No stored state", "Adders and decoders"],
            ),
            (
                "Summary",
                ["Combinational circuits calculate immediate results from inputs."],
            ),
        ],
    },
    {
        "menu_title": "Digital Circuits",
        "title": "Digital Circuits",
        "definition": "A digital circuit connects gates to process ternary information.",
        "sections": [
            (
                "Explanation",
                [
                    "Real chips contain billions of transistor-level gates.",
                    "Designers group gates into reusable blocks such as registers and ALUs.",
                ],
            ),
            (
                "Examples",
                [
                    "A register stores trits.",
                    "An ALU performs arithmetic and logic operations.",
                ],
            ),
            (
                "Did You Know?",
                [
                    "A gate is usually built from transistors, not from a separate visible part.",
                    "Modern chips pack these transistor networks into very small areas.",
                ],
            ),
            (
                "Key Concepts",
                ["Transistor", "Gate network", "Register", "ALU"],
            ),
            (
                "Summary",
                [
                    "Digital circuits turn simple ternary logic rules into useful machines."
                ],
            ),
        ],
    },
    {
        "menu_title": "CPU Applications",
        "title": "CPU Applications",
        "definition": "CPUs use logic gates to execute instructions.",
        "sections": [
            (
                "Explanation",
                [
                    "Instruction decoding, arithmetic, comparisons, and branching all use logic.",
                    "The CPU control unit chooses which gate networks should be active.",
                ],
            ),
            (
                "Examples",
                [
                    "SUM appears in addition and parity logic.",
                    "MIN can mask selected trits in an instruction.",
                    "MAX can combine status flags.",
                ],
            ),
            (
                "Real Hardware Example",
                [
                    "A branch instruction may depend on a zero flag.",
                    "Logic gates compute and route that flag so the CPU can choose the next instruction.",
                ],
            ),
            (
                "Key Concepts",
                ["Instruction decoder", "Control signal", "Status flag", "ALU"],
            ),
            (
                "Summary",
                [
                    "Logic gates are the small decisions that make CPU instructions possible."
                ],
            ),
        ],
    },
]


def lesson_count() -> int:
    """Return the number of available digital logic lessons."""
    return len(LESSONS)


def get_lesson(index: int) -> Lesson:
    """Return a lesson by one-based index."""
    if index < 1 or index > len(LESSONS):
        raise ValueError("Lesson index is out of range.")

    return LESSONS[index - 1]
