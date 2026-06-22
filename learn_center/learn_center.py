from converters.decimal_to_ternary import clean_input
from ui.terminal import (
    error_screen,
    explanation_screen,
    menu_screen,
    pause,
    print_screen,
    prompt,
    success_message,
)


LessonSection = tuple[str, list[str]]
Lesson = dict[str, str | list[LessonSection]]


LESSONS: list[Lesson] = [
    {
        "menu_title": "What is Ternary?",
        "title": "What is Ternary?",
        "question": "What is ternary and how does it store numbers?",
        "sections": [
            (
                "Answer",
                [
                    "Ternary is a number system with base 3.",
                    "It uses three digits: 0, 1, and 2.",
                    "Each place is worth a power of 3, just like each",
                    "binary place is worth a power of 2.",
                ],
            ),
            (
                "Worked Example",
                [
                    "The ternary number 102 means:",
                    "",
                    "1 x 9 = 9",
                    "0 x 3 = 0",
                    "2 x 1 = 2",
                    "",
                    "So 102 in ternary equals 11 in decimal.",
                ],
            ),
            (
                "Computer Science Context",
                [
                    "A binary digit is called a bit.",
                    "A ternary digit is called a trit.",
                    "A trit can represent three possible states instead of two.",
                ],
            ),
            (
                "Key Takeaway",
                [
                    "Ternary is another way to encode information.",
                    "It is not strange or magic; it is simply base 3.",
                ],
            ),
        ],
    },
    {
        "menu_title": "Why do computers use Binary?",
        "title": "Why Computers Use Binary",
        "question": "Why do most modern computers use binary?",
        "sections": [
            (
                "Answer",
                [
                    "Modern computers use binary because electronic circuits",
                    "naturally have two stable states:",
                    "",
                    "OFF = 0",
                    "ON  = 1",
                    "",
                    "That makes binary hardware reliable and simple to build.",
                ],
            ),
            (
                "Real-World Example",
                [
                    "A switch, transistor, or logic gate can be treated as",
                    "either low voltage or high voltage.",
                    "Small electrical noise is less likely to confuse the",
                    "computer when only two states must be separated.",
                ],
            ),
            (
                "Common Misconception",
                [
                    "Binary is not used because humans prefer it.",
                    "Humans usually prefer decimal.",
                    "Binary became dominant because it fits digital hardware well.",
                ],
            ),
            (
                "Did You Know?",
                [
                    "Computers can show text, images, music, and video because",
                    "all of that data can be encoded as long patterns of bits.",
                ],
            ),
        ],
    },
    {
        "menu_title": "Why isn't Ternary commonly used?",
        "title": "Why Ternary Is Not Common",
        "question": "If ternary is useful, why do most computers still use binary?",
        "sections": [
            (
                "Answer",
                [
                    "Ternary can be elegant, but computer design is not decided",
                    "by mathematics alone.",
                    "Engineers also care about cost, reliability, manufacturing,",
                    "tools, standards, and compatibility.",
                ],
            ),
            (
                "Hardware Reason",
                [
                    "A ternary circuit needs three clearly separated states.",
                    "For example, it may need low, middle, and high voltage.",
                    "Keeping those states stable is harder than separating two",
                    "states, especially at high speed and tiny chip sizes.",
                ],
            ),
            (
                "Ecosystem Reason",
                [
                    "Binary already has decades of processors, memory chips,",
                    "programming tools, file formats, and operating systems.",
                    "Changing the entire computing ecosystem would be expensive.",
                ],
            ),
            (
                "Key Takeaway",
                [
                    "Ternary is interesting, but binary won because it is simple,",
                    "reliable, cheap to manufacture, and widely standardized.",
                ],
            ),
        ],
    },
    {
        "menu_title": "Balanced Ternary",
        "title": "Balanced Ternary",
        "question": "What makes balanced ternary different from ordinary ternary?",
        "sections": [
            (
                "Definition",
                [
                    "Ordinary ternary uses 0, 1, and 2.",
                    "Balanced ternary uses T, 0, and 1.",
                    "",
                    "T means -1.",
                    "0 means 0.",
                    "1 means +1.",
                ],
            ),
            (
                "Why It Matters",
                [
                    "Balanced ternary can represent positive and negative values",
                    "symmetrically.",
                    "To negate a balanced ternary number, swap 1 and T.",
                    "The digit 0 stays the same.",
                ],
            ),
            (
                "Small Table",
                [
                    "Decimal    Balanced Ternary",
                    "───────    ────────────────",
                    "-2         T1",
                    "-1         T",
                    " 0         0",
                    " 1         1",
                    " 2         1T",
                ],
            ),
            (
                "Did You Know?",
                [
                    "Balanced ternary is often admired because negative numbers",
                    "do not need a separate sign symbol in the same way ordinary",
                    "positional notation does.",
                ],
            ),
        ],
    },
    {
        "menu_title": "Binary vs Ternary",
        "title": "Binary vs Ternary",
        "question": "How are binary and ternary different?",
        "sections": [
            (
                "Comparison",
                [
                    "Binary is base 2 and uses 0 and 1.",
                    "Ternary is base 3 and uses 0, 1, and 2.",
                    "Balanced ternary is also base 3, but uses T, 0, and 1.",
                ],
            ),
            (
                "Small Table",
                [
                    "System             Base    Digits",
                    "──────             ────    ──────",
                    "Binary             2       0, 1",
                    "Ordinary Ternary   3       0, 1, 2",
                    "Balanced Ternary   3       T, 0, 1",
                ],
            ),
            (
                "Computer Science Context",
                [
                    "Binary is easier to implement in circuits.",
                    "Ternary can sometimes use fewer digit positions for the",
                    "same decimal value because base 3 carries more information",
                    "per digit than base 2.",
                ],
            ),
            (
                "Key Takeaway",
                [
                    "Binary is the practical standard.",
                    "Ternary is a useful idea for learning number systems and",
                    "thinking about alternative computer designs.",
                ],
            ),
        ],
    },
    {
        "menu_title": "History of Ternary Computing",
        "title": "History of Ternary Computing",
        "question": "Has ternary computing ever been used in real computers?",
        "sections": [
            (
                "Historical Background",
                [
                    "Yes. Ternary computers have been built.",
                    "One famous example is Setun, a Soviet computer built in",
                    "the late 1950s at Moscow State University.",
                ],
            ),
            (
                "Why Setun Matters",
                [
                    "Setun used balanced ternary logic.",
                    "It showed that ternary computing was not only a theory.",
                    "Engineers could design real machines around three-valued",
                    "logic.",
                ],
            ),
            (
                "Computer Science Context",
                [
                    "The history of computing includes many experiments:",
                    "mechanical computers, analog computers, binary computers,",
                    "ternary computers, and quantum computing research.",
                    "Binary became dominant, but it was not the only idea.",
                ],
            ),
            (
                "Did You Know?",
                [
                    "Donald Knuth, a major computer scientist, has written with",
                    "interest about balanced ternary because of its mathematical",
                    "neatness and symmetry.",
                ],
            ),
        ],
    },
]


FAQ_ITEMS: list[tuple[str, str]] = [
    (
        "What is ternary computing?",
        "Ternary computing uses three possible digit states instead of two.",
    ),
    (
        "What is a trit?",
        "A trit is a ternary digit, similar to how a bit is a binary digit.",
    ),
    (
        "Is ternary better than binary?",
        "Not always. Ternary is mathematically interesting, but binary is simpler for most hardware.",
    ),
    (
        "Why don't modern computers use ternary?",
        "Binary circuits are cheaper, simpler, reliable, and supported by a huge technology ecosystem.",
    ),
    (
        "What is balanced ternary?",
        "Balanced ternary is base 3 using the digit values -1, 0, and +1.",
    ),
    (
        "Has a ternary computer ever existed?",
        "Yes. Setun, built in the Soviet Union in the late 1950s, is a well-known example.",
    ),
    (
        "Can ternary computers exist today?",
        "Yes, but building them at modern scale is difficult compared with binary systems.",
    ),
]


FUN_FACTS: list[tuple[str, list[str]]] = [
    (
        "The Setun Computer",
        [
            "Setun was a real ternary computer built at Moscow State",
            "University in the late 1950s.",
        ],
    ),
    (
        "Balanced Ternary Digits",
        [
            "Balanced ternary can use T for -1, 0 for 0, and 1 for +1.",
            "This gives the number system a natural symmetry.",
        ],
    ),
    (
        "Donald Knuth",
        [
            "Donald Knuth discussed balanced ternary in computer science",
            "writing because it is elegant and useful for learning.",
        ],
    ),
    (
        "Mathematical Elegance",
        [
            "Base 3 is close to the mathematical constant e, which is one",
            "reason ternary is often discussed in efficiency arguments.",
        ],
    ),
    (
        "Powers of Three",
        [
            "Ternary place values grow as 1, 3, 9, 27, 81, and so on.",
            "Each new place is three times the value of the previous place.",
        ],
    ),
    (
        "Modern Research",
        [
            "Researchers still explore multi-valued logic, memory devices,",
            "and non-binary computing models, even though everyday computers",
            "remain binary.",
        ],
    ),
]


def display_header() -> None:
    """Display the Learn Center title."""
    print_screen(
        explanation_screen(
            "Learn Center",
            ["Short lessons for ternary computing and computer architecture."],
        )
    )


def display_lesson_frame(title: str, question: str) -> None:
    """Display the opening frame for a lesson page."""
    print_screen(explanation_screen(title, ["Question", "", question]))


def display_section(heading: str, lines: list[str]) -> None:
    """Display a named lesson section with formatted body lines."""
    print_screen(explanation_screen(heading, lines))


def display_lesson(lesson: Lesson) -> None:
    """Display one Learn Center lesson."""
    title = str(lesson["title"])
    question = str(lesson["question"])
    sections = lesson["sections"]

    display_lesson_frame(title, question)

    for heading, lines in sections:
        display_section(heading, lines)

    print_screen(success_message("Lesson complete."))


def display_faq() -> None:
    """Display frequently asked questions about ternary computing."""
    for index, (question, answer) in enumerate(FAQ_ITEMS, start=1):
        print_screen(explanation_screen(f"FAQ {index}", [question, "", answer]))


def display_fun_facts() -> None:
    """Display interesting facts related to ternary computing."""
    for index, (title, facts) in enumerate(FUN_FACTS, start=1):
        print_screen(explanation_screen(f"Fact {index}: {title}", facts))


def display_menu() -> None:
    """Display the Learn Center submenu."""
    options = [
        (str(index), str(lesson["menu_title"]))
        for index, lesson in enumerate(LESSONS, start=1)
    ]
    options.extend(
        [
            ("7", "Frequently Asked Questions"),
            ("8", "Fun Facts"),
            ("9", "Back"),
        ]
    )
    print_screen(menu_screen("Learn Center", options))


def get_menu_choice() -> str:
    """Read and clean the user's Learn Center menu choice."""
    return clean_input(prompt())


def pause_for_reader() -> None:
    """Pause after a lesson so the user can read before returning."""
    pause("Press Enter to return to the Learn Center menu")


def run_selected_topic(choice: str) -> bool:
    """Run a Learn Center topic.

    Args:
        choice: The user's menu choice.

    Returns:
        True if the Learn Center should continue, otherwise False.
    """
    if choice == "9":
        return False

    if choice in {"1", "2", "3", "4", "5", "6"}:
        display_lesson(LESSONS[int(choice) - 1])
        pause_for_reader()
        return True

    if choice == "7":
        display_faq()
        pause_for_reader()
        return True

    if choice == "8":
        display_fun_facts()
        pause_for_reader()
        return True

    print_screen(error_screen("Please enter a number from 1 to 9."))
    return True


def main() -> None:
    """Run the interactive Learn Center module."""
    display_header()
    while True:
        display_menu()
        choice = get_menu_choice()

        if not run_selected_topic(choice):
            print_screen(success_message("Returning to the main menu."))
            break


if __name__ == "__main__":
    main()
