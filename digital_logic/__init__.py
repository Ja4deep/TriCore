"""Digital Logic Laboratory integration for TriCore."""

from __future__ import annotations

from arithmetic.utils import clean_input
from ui.terminal import (
    ReturnToMainMenu,
    error_screen,
    explanation_screen,
    input_screen,
    menu_screen,
    pause,
    print_screen,
    prompt,
    result_screen,
    success_message,
)

from .expressions import EvaluationResult, evaluate_expression, expression_variables
from .formatter import (
    gate_reference_lines,
    simulation_diagram_lines,
    simulation_result_lines,
    truth_table_lines,
)
from .logic_gates import get_gate, list_gate_names
from .lessons import LESSONS, get_lesson, lesson_count
from .simulator import simulate_gate
from .truth_tables import explain_truth_table
from .utils import input_labels
from .validation import validate_ternary_value

# Use shared ReturnToMainMenu exception from ui.terminal


def safe_prompt(label: str = "Enter your choice") -> str:
    """Read user input and return to the main menu on Ctrl+C."""
    try:
        return prompt(label)
    except KeyboardInterrupt as error:
        raise ReturnToMainMenu from error
    except EOFError:
        return "0"


def digital_logic_menu() -> str:
    """Display the Digital Logic Laboratory menu and return the selection."""
    print_screen(
        menu_screen(
            "Digital Logic Laboratory",
            [
                ("1", "Logic Gates"),
                ("2", "Truth Tables"),
                ("3", "Gate Simulator"),
                ("4", "Ternary Logic Expression Evaluator"),
                ("5", "Learn Digital Logic"),
                ("0", "Back"),
            ],
        )
    )
    return clean_input(safe_prompt())


def gate_selection_menu(title: str) -> str:
    """Display a gate selection menu and return the selected gate name or Back."""
    options = [
        (str(index), gate_name)
        for index, gate_name in enumerate(list_gate_names(), start=1)
    ]
    options.append(("0", "Back"))
    print_screen(menu_screen(title, options))

    choice = clean_input(safe_prompt())
    if choice == "0":
        return "0"
    if choice.isdigit():
        index = int(choice)
        names = list_gate_names()
        if 1 <= index <= len(names):
            return names[index - 1]

    print_screen(error_screen("Please choose a listed gate number."))
    return ""


def read_gate_inputs(gate_name: str) -> tuple[int, ...] | None:
    """Read ternary inputs for a gate from the student."""
    gate = get_gate(gate_name)
    values: list[int] = []

    for label in input_labels(gate.arity):
        while True:
            print_screen(
                input_screen(
                    "Gate Input",
                    f"Enter ternary value for {label}",
                    "Use 0 for LOW, 1 for MID, or 2 for HIGH.",
                )
            )
            raw_value = safe_prompt(f"{label}")

            try:
                values.append(validate_ternary_value(raw_value, field_name=label))
                break
            except ValueError as error:
                print_screen(error_screen(str(error)))

    return tuple(values)


def run_logic_gates() -> None:
    """Run the educational logic gate reference and simulation area."""
    while True:
        gate_name = gate_selection_menu("Logic Gates")
        if gate_name == "0":
            raise ReturnToMainMenu
        if not gate_name:
            continue

        print_screen(
            explanation_screen(f"{gate_name} Gate", gate_reference_lines(gate_name))
        )
        simulate_choice = clean_input(safe_prompt("Simulate this gate? (y/n)")).lower()
        if simulate_choice == "y":
            run_gate_simulator(gate_name)
        else:
            pause("Press Enter to return to Logic Gates")


def run_truth_tables() -> None:
    """Run the truth table generator menu."""
    while True:
        gate_name = gate_selection_menu("Truth Tables")
        if gate_name == "0":
            raise ReturnToMainMenu
        if not gate_name:
            continue

        print_screen(
            result_screen(f"{gate_name} Truth Table", truth_table_lines(gate_name))
        )
        print_screen(
            explanation_screen("What This Shows", explain_truth_table(gate_name))
        )
        pause("Press Enter to return to Truth Tables")


def run_gate_simulator(selected_gate: str | None = None) -> None:
    """Run the interactive gate simulator."""
    gate_name = selected_gate
    if gate_name is None:
        while True:
            gate_name = gate_selection_menu("Gate Simulator")
            if gate_name == "0":
                raise ReturnToMainMenu
            if gate_name:
                break

    inputs = read_gate_inputs(gate_name)
    if inputs is None:
        return

    try:
        result = simulate_gate(gate_name, inputs)
    except ValueError as error:
        print_screen(error_screen(str(error)))
        pause()
        return

    print_screen(result_screen("Simulation Result", simulation_result_lines(result)))
    print_screen(explanation_screen("Circuit View", simulation_diagram_lines(result)))
    print_screen(
        explanation_screen("Why This Happened", result.explanation.splitlines())
    )
    pause("Press Enter to return")


def run_expression_evaluator() -> None:
    """Run the ternary expression evaluator."""
    expression = _read_logic_expression()
    if expression is None:
        raise ReturnToMainMenu

    variables = _read_expression_variables(expression)
    if variables is None:
        return

    assignments = _read_variable_assignments(variables)
    evaluation = _evaluate_expression_safely(expression, assignments)
    if evaluation is None:
        return

    _render_expression_evaluation(evaluation, assignments)
    pause("Press Enter to return to Digital Logic")


def _read_logic_expression() -> str | None:
    """Read the expression text for the evaluator."""
    print_screen(
        explanation_screen(
            "Logic Expression Evaluator",
            [
                "Examples: NOT A, A MIN B, (A MIN B) MAX C, NOT (A MAX B)",
                "Supported operators: NOT, MIN, MAX, SUM, NMIN, NMAX.",
                "Enter 0 to return to the Digital Logic menu.",
            ],
        )
    )
    expression = clean_input(safe_prompt("Expression"))
    if expression == "0":
        return None

    return expression


def _read_expression_variables(expression: str) -> list[str] | None:
    """Parse variables referenced by an expression."""
    try:
        return expression_variables(expression)
    except ValueError as error:
        print_screen(error_screen(str(error), title="Expression Error"))
        pause()
        return None


def _read_variable_assignments(variables: list[str]) -> dict[str, int]:
    """Read ternary assignments for all expression variables."""
    assignments: dict[str, int] = {}
    for variable in variables:
        while True:
            print_screen(
                input_screen(
                    "Variable Value",
                    f"Enter ternary value for {variable}",
                    "Use 0 for LOW, 1 for MID, or 2 for HIGH.",
                )
            )
            try:
                assignments[variable] = validate_ternary_value(
                    safe_prompt(variable),
                    field_name=variable,
                )
                break
            except ValueError as error:
                print_screen(error_screen(str(error)))

    return assignments


def _evaluate_expression_safely(
    expression: str,
    assignments: dict[str, int],
) -> EvaluationResult | None:
    """Evaluate an expression and render user-friendly validation errors."""
    try:
        return evaluate_expression(expression, assignments)
    except ValueError as error:
        print_screen(error_screen(str(error), title="Expression Error"))
        pause()
        return None


def _render_expression_evaluation(
    evaluation: EvaluationResult,
    assignments: dict[str, int],
) -> None:
    """Render expression output and educational evaluation steps."""
    assignment_lines = [
        f"{name} = {value}" for name, value in sorted(assignments.items())
    ]
    print_screen(
        result_screen(
            "Expression Result",
            [
                f"Expression : {evaluation.expression}",
                *assignment_lines,
                f"Output     : {evaluation.result}",
            ],
        )
    )

    step_lines = []
    for index, step in enumerate(evaluation.steps, start=1):
        step_lines.append(f"Step {index}: {step.expression}")
        step_lines.append(f"Result {step.result} - {step.explanation}")
        step_lines.append("")

    print_screen(explanation_screen("Step-by-Step Evaluation", step_lines))
    print_screen(
        explanation_screen(
            "Computer Context",
            [
                "A ternary logic expression is a circuit written in text form.",
                "Each operator maps to one or more ternary logic gates.",
                "Processors use these gate networks for arithmetic, comparisons, control, and memory operations.",
            ],
        )
    )


def display_lesson(lesson_index: int) -> None:
    """Display one digital logic lesson."""
    lesson = get_lesson(lesson_index)
    print_screen(
        explanation_screen(
            str(lesson["title"]),
            [
                "Definition",
                str(lesson["definition"]),
            ],
        )
    )

    for heading, lines in lesson["sections"]:
        print_screen(explanation_screen(heading, lines))

    print_screen(success_message("Lesson complete."))


def run_lessons() -> None:
    """Run the Learn Digital Logic submenu."""
    while True:
        options = [
            (str(index), str(lesson["menu_title"]))
            for index, lesson in enumerate(LESSONS, start=1)
        ]
        options.append(("0", "Back"))
        print_screen(menu_screen("Learn Digital Logic", options))

        choice = clean_input(safe_prompt())
        if choice == "0":
            raise ReturnToMainMenu
        if choice.isdigit() and 1 <= int(choice) <= lesson_count():
            display_lesson(int(choice))
            pause("Press Enter to return to Learn Digital Logic")
            continue

        print_screen(error_screen(f"Please enter a number from 0 to {lesson_count()}."))


def main() -> None:
    """Run the Digital Logic Laboratory module."""
    while True:
        try:
            choice = digital_logic_menu()
            if choice == "0":
                print_screen(success_message("Returning to the main menu."))
                return
            if choice == "1":
                run_logic_gates()
            elif choice == "2":
                run_truth_tables()
            elif choice == "3":
                run_gate_simulator()
            elif choice == "4":
                run_expression_evaluator()
            elif choice == "5":
                run_lessons()
            else:
                print_screen(error_screen("Please enter a number from 0 to 5."))
        except (KeyboardInterrupt, ReturnToMainMenu):
            print_screen(success_message("Returning to the main menu."))
            return


__all__ = [
    "evaluate_expression",
    "expression_variables",
    "main",
    "simulate_gate",
]
