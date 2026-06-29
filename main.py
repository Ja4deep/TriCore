from __future__ import annotations

from config import PROJECT_NAME
from logging_config import configure_logging
from arithmetic import add_numbers, divide_numbers, multiply_numbers, subtract_numbers
from arithmetic.explanation import ArithmeticResult, ExplanationStep
from converters.binary_vs_ternary import (
    display_header as show_binary_vs_ternary,
    display_results as show_binary_vs_ternary_results,
    explain_comparison,
)
from converters.balanced_ternary import main as run_balanced_ternary
from converters.decimal_to_ternary import (
    display_header as show_dec_to_ter,
    display_results as show_dec_to_ter_results,
    explain_conversion as explain_dec_to_ter,
    get_decimal_input,
)
from converters.ternary_to_decimal import (
    display_header as show_ter_to_dec,
    display_results as show_ter_to_dec_results,
    explain_conversion as explain_ter_to_dec,
    get_ternary_input,
)
from digital_logic import main as run_digital_logic
from learn_center.learn_center import main as run_learn_center
from logic_circuit_simulator import main as run_circuit_simulator
from ui.terminal import (
    CONTENT_WIDTH,
    error_screen,
    explanation_screen,
    help_screen,
    input_screen,
    menu_screen,
    pause,
    print_screen,
    prompt,
    result_screen,
    success_message,
)


def main_menu() -> str:
    """Display the TriCore main menu and poll choices."""
    print_screen(
        menu_screen(
            f"{PROJECT_NAME} Main Menu",
            [
                ("1", "Number System Converters"),
                ("2", "Arithmetic Engine"),
                ("3", "Learning Center"),
                ("4", "Digital Logic Laboratory"),
                ("5", "Ternary Logic Circuit Simulator"),
                ("6", "Settings"),
                ("7", "Help"),
                ("0", "Exit"),
            ],
        )
    )
    return prompt()


def converter_menu() -> str:
    """Display the converter menu and return the selected option."""
    print_screen(
        menu_screen(
            "Number System Converter",
            [
                ("1", "Decimal to Ordinary Ternary"),
                ("2", "Ordinary Ternary to Decimal"),
                ("3", "Binary vs Ternary"),
                ("4", "Balanced Ternary"),
                ("5", "Back"),
            ],
        )
    )
    return prompt()


def arithmetic_menu() -> str:
    """Display the arithmetic menu and return the selected option."""
    print_screen(
        menu_screen(
            "Arithmetic Engine",
            [
                ("1", "Addition"),
                ("2", "Subtraction"),
                ("3", "Multiplication"),
                ("4", "Division"),
                ("5", "Back"),
            ],
        )
    )
    return prompt()


def get_decimal_number() -> int:
    """Read a decimal integer from the user with validation."""
    return get_decimal_input()


def run_decimal_to_ternary() -> None:
    """Run the decimal-to-ternary converter."""
    show_dec_to_ter()
    explain_dec_to_ter()
    number = get_decimal_number()
    show_dec_to_ter_results(number)
    pause()


def run_ternary_to_decimal() -> None:
    """Run the ternary-to-decimal converter."""
    show_ter_to_dec()
    explain_ter_to_dec()
    ternary = get_ternary_input()
    show_ter_to_dec_results(ternary)
    pause()


def run_binary_vs_ternary() -> None:
    """Run the binary-vs-ternary comparison."""
    show_binary_vs_ternary()
    explain_comparison()
    number = get_decimal_number()
    show_binary_vs_ternary_results(number)
    pause()


def run_converter_menu() -> None:
    """Run the converter submenu."""
    while True:
        choice = converter_menu()

        if choice == "5":
            return
        if choice == "1":
            run_decimal_to_ternary()
        elif choice == "2":
            run_ternary_to_decimal()
        elif choice == "3":
            run_binary_vs_ternary()
        elif choice == "4":
            run_balanced_ternary()
        else:
            print_screen(error_screen("Please enter a number from 1 to 5."))


def read_ternary_operand(label: str) -> str:
    """Read one ternary operand from the student."""
    print_screen(
        input_screen(
            "Input",
            label,
            "Use ordinary ternary digits only: 0, 1, and 2.",
        )
    )
    return prompt(label)


def render_arithmetic_expression(
    left: str,
    right: str,
    operator: str,
    result: ArithmeticResult,
) -> list[str]:
    """Return aligned arithmetic expression lines for a result screen."""
    if operator == "÷":
        return [
            f"Dividend  : {left}",
            f"Divisor   : {right}",
            "─" * CONTENT_WIDTH,
            f"Quotient  : {result.metadata['quotient']}",
            f"Remainder : {result.metadata['remainder']}",
        ]

    width = max(len(left), len(right), len(result.result))
    return [
        left.rjust(width + 3),
        f"{operator}  {right.rjust(width)}",
        "─" * (width + 3),
        result.result.rjust(width + 3),
    ]


def render_carry_or_borrow_lines(result: ArithmeticResult) -> list[str]:
    """Return carry, borrow, and intermediate-row lines for arithmetic output."""
    lines = []

    carry_records = result.metadata.get("carry_records", [])
    borrow_records = result.metadata.get("borrow_records", [])
    partial_rows = result.metadata.get("partial_rows", [])
    intermediate_rows = result.metadata.get("intermediate_rows", [])

    if carry_records:
        lines.extend(["", "Carry Information"])
        for record in carry_records:
            lines.append(f"Column {record.position + 1}: carry {record.value}")

    if borrow_records:
        lines.extend(["", "Borrow Information"])
        for record in borrow_records:
            lines.append(f"Column {record.position + 1}: borrow {record.value}")

    if partial_rows:
        lines.extend(["", "Partial Rows"])
        lines.extend(str(row) for row in partial_rows)

    if intermediate_rows:
        lines.extend(["", "Long Division Rows"])
        for row in intermediate_rows:
            lines.append(
                f"{row['current']} ÷ step -> q {row['quotient_digit']}, "
                f"product {row['product']}, rem {row['remainder']}"
            )

    return lines


def render_explanation_steps(steps: list[ExplanationStep]) -> None:
    """Render explanation steps inside bordered sections."""
    for step in steps:
        lines = []
        if step.expression:
            lines.extend(step.expression.splitlines())
        if step.explanation:
            lines.extend(["", *step.explanation.splitlines()])

        print_screen(explanation_screen(step.title, lines))


def run_arithmetic_operation(name: str, operator: str) -> None:
    """Run one arithmetic operation from validated student input."""
    left = read_ternary_operand("First ternary number")
    right = read_ternary_operand("Second ternary number")

    operations = {
        "+": add_numbers,
        "-": subtract_numbers,
        "×": multiply_numbers,
        "÷": divide_numbers,
    }

    try:
        result = operations[operator](left, right, explanation_mode=True)
    except ValueError as error:
        print_screen(error_screen(str(error)))
        pause()
        return

    result_lines = render_arithmetic_expression(left, right, operator, result)
    result_lines.extend(render_carry_or_borrow_lines(result))

    print_screen(result_screen(name, result_lines))
    render_explanation_steps(result.steps)
    pause()


def run_arithmetic_menu() -> None:
    """Run the arithmetic engine submenu."""
    while True:
        choice = arithmetic_menu()

        if choice == "5":
            return
        if choice == "1":
            run_arithmetic_operation("Addition Result", "+")
        elif choice == "2":
            run_arithmetic_operation("Subtraction Result", "-")
        elif choice == "3":
            run_arithmetic_operation("Multiplication Result", "×")
        elif choice == "4":
            run_arithmetic_operation("Division Result", "÷")
        else:
            print_screen(error_screen("Please enter a number from 1 to 5."))


def show_settings() -> None:
    """Display current terminal UI settings."""
    print_screen(
        help_screen(
            "Settings",
            [
                "Color mode uses Colorama when the terminal supports it.",
                "Titles are cyan, results are green, explanations are yellow, and errors are red.",
                "The text remains readable when colors are disabled.",
            ],
        )
    )
    pause()


def show_help() -> None:
    """Display TriCore help content."""
    print_screen(
        help_screen(
            "Help",
            [
                "TriCore teaches number systems and computer architecture concepts.",
                "",
                "Use Number System Converter to study decimal, ternary, binary comparison, and balanced ternary.",
                "Use Arithmetic Engine to solve ordinary ternary arithmetic step by step.",
                "Use Learn Center for short conceptual lessons and historical context.",
                "Use Digital Logic Laboratory to explore ternary gates, truth tables, and ternary logic expressions.",
                "",
                "Future modules can reuse this interface for ternary ALU simulation and ternary CPU architecture studies.",
            ],
        )
    )
    pause()


def main() -> None:
    """Main entry point for TriCore."""
    configure_logging()

    while True:
        choice = main_menu()

        if choice == "0":
            print_screen(success_message("Exiting TriCore. Goodbye!"))
            break

        elif choice == "1":
            run_converter_menu()

        elif choice == "2":
            run_arithmetic_menu()

        elif choice == "3":
            run_learn_center()

        elif choice == "4":
            run_digital_logic()

        elif choice == "5":
            run_circuit_simulator()

        elif choice == "6":
            show_settings()

        elif choice == "7":
            show_help()

        else:
            print_screen(
                error_screen(
                    "Selected option is outside the valid range. Please choose a number between 0 and 7."
                )
            )


if __name__ == "__main__":
    main()
