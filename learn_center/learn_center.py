"""Interactive Learning Center navigation for TriCore."""

from __future__ import annotations

from arithmetic.utils import clean_input
from learn_center.curriculum import CURRICULUM
from learn_center.types import CurriculumSection, Lesson
from ui.terminal import (
    error_screen,
    explanation_screen,
    menu_screen,
    pause,
    print_screen,
    prompt,
    success_message,
)


def display_header() -> None:
    """Display the Learning Center title."""
    print_screen(
        explanation_screen(
            "Learning Center",
            [
                "A guided course in number systems, ternary arithmetic,",
                "digital logic, circuit behavior, and computer architecture.",
            ],
        )
    )


def display_course_menu() -> None:
    """Display the top-level Learning Center course menu."""
    options = [
        (str(index), section["menu_title"])
        for index, section in enumerate(CURRICULUM, start=1)
    ]
    options.append((str(len(CURRICULUM) + 1), "Back"))
    print_screen(menu_screen("Learning Center", options))


def display_section_menu(section: CurriculumSection) -> None:
    """Display one course section's lesson menu."""
    lessons = section["lessons"]
    options = [
        (str(index), lesson["menu_title"])
        for index, lesson in enumerate(lessons, start=1)
    ]
    options.append((str(len(lessons) + 1), "Back"))
    print_screen(menu_screen(section["title"], options))


def get_menu_choice() -> str:
    """Read and clean the user's Learning Center menu choice."""
    return clean_input(prompt())


def display_lesson_frame(title: str, question: str) -> None:
    """Display the opening frame for a lesson."""
    print_screen(explanation_screen(title, ["Guiding question", "", question]))


def display_lesson(lesson: Lesson) -> None:
    """Display one Learning Center lesson as a sequence of pages."""
    display_lesson_frame(lesson["title"], lesson["question"])

    for heading, lines in lesson["sections"]:
        print_screen(explanation_screen(heading, lines))

    print_screen(success_message("Lesson complete."))


def pause_for_reader() -> None:
    """Pause after a lesson or error so the student can read."""
    pause("Press Enter to return")


def run_section(section: CurriculumSection) -> None:
    """Run a section submenu until the student chooses Back."""
    lessons = section["lessons"]
    back_choice = str(len(lessons) + 1)

    while True:
        display_section_menu(section)
        choice = get_menu_choice()

        if choice == back_choice:
            return

        if choice.isdigit() and 1 <= int(choice) <= len(lessons):
            display_lesson(lessons[int(choice) - 1])
            pause_for_reader()
            continue

        print_screen(error_screen(f"Please enter a number from 1 to {back_choice}."))


def main() -> None:
    """Run the interactive Learning Center module."""
    display_header()
    back_choice = str(len(CURRICULUM) + 1)

    while True:
        display_course_menu()
        choice = get_menu_choice()

        if choice == back_choice:
            print_screen(success_message("Returning to the main menu."))
            break

        if choice.isdigit() and 1 <= int(choice) <= len(CURRICULUM):
            run_section(CURRICULUM[int(choice) - 1])
            continue

        print_screen(error_screen(f"Please enter a number from 1 to {back_choice}."))


if __name__ == "__main__":
    main()
