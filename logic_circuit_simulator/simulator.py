"""
Core structural controller orchestration module managing menus, tracking runs,
and educational walkthrough loops for the Circuit Simulator.
"""

from __future__ import annotations

from arithmetic.utils import clean_input
from exceptions import TriCoreError
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
from logic_circuit_simulator.circuit import Circuit
from logic_circuit_simulator.builder import run_interactive_circuit_builder_workspace
from logic_circuit_simulator.evaluator import run_circuit_simulation
from logic_circuit_simulator.formatter import (
    generate_static_ascii_layout,
    format_custom_flow_diagram,
)
from logic_circuit_simulator.examples import (
    EXAMPLES_REPOSITORY,
    load_example_into_circuit,
)
from logic_circuit_simulator.lessons import LESSONS_CHAMBER
from logic_circuit_simulator.validation import parse_and_validate_ternary_state


def show_lessons() -> None:
    """Display educational lessons about circuit design."""
    while True:
        options = [
            (str(idx), str(lesson["title"]))
            for idx, lesson in enumerate(LESSONS_CHAMBER, start=1)
        ]
        options.append(("0", "Back"))

        print_screen(menu_screen("Learn Circuit Design", options))
        choice = clean_input(prompt())

        if choice == "0":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(LESSONS_CHAMBER):
            lesson = LESSONS_CHAMBER[int(choice) - 1]
            body_content = [
                "Definition",
                str(lesson["definition"]),
                "",
                "Functional Breakdown",
                *[f"• {line}" for line in lesson["explanation"]],
                "",
                "Hardware Context",
                str(lesson["hardware"]),
            ]

            print_screen(explanation_screen(str(lesson["title"]), body_content))
            pause()
        else:
            print_screen(error_screen("Invalid selection."))
            pause()


def run_simulation(circuit: Circuit) -> None:
    """Run a simulation of the current circuit."""
    try:
        circuit.validate_integrity()
    except (TriCoreError, ValueError) as err:
        print_screen(error_screen(str(err), title="Validation Error"))
        pause()
        return

    runtime_inputs = {}
    for inp_id, inp_node in sorted(circuit.inputs.items()):
        while True:
            try:
                print_screen(
                    input_screen(
                        "Inputs", f"Enter ternary value for {inp_node.label} ({inp_id})"
                    )
                )
                raw_val = prompt("Value")
                val = parse_and_validate_ternary_state(raw_val)
                runtime_inputs[inp_id] = val
                break
            except (TriCoreError, ValueError) as val_err:
                print_screen(error_screen(str(val_err)))

    try:
        payload = run_circuit_simulation(circuit, runtime_inputs)

        res_lines = ["Input States:"]
        for k, v in sorted(payload.input_states.items()):
            res_lines.append(f"  • {circuit.get_node(k).label} ({k}): {v}")

        res_lines.append("\nOutput Results:")
        for k, v in sorted(payload.output_states.items()):
            res_lines.append(f"  • {circuit.get_node(k).label} ({k}): {v}")

        print_screen(result_screen("Simulation Results", res_lines))
        pause()

        for step in payload.execution_trace:
            step_card = [
                f"Step {step.step_number}: {step.label} ({step.node_id})",
                f"Type   : {step.node_type}",
                f"Result : {step.assigned_value}",
                "",
                "Explanation:",
                step.narrative_detail,
            ]
            print_screen(
                explanation_screen(
                    f"Signal Propagation - Step {step.step_number}", step_card
                )
            )
            pause("Press Enter to continue")

        print_screen(success_message("Simulation complete."))
        pause()

    except (TriCoreError, ValueError, IndexError) as err:
        print_screen(error_screen(str(err), title="Simulation Error"))
        pause()


def explore_built_in_example_circuits(circuit: Circuit) -> None:
    """Browse and load pre-configured example circuits."""
    while True:
        options = [(k, card.title) for k, card in sorted(EXAMPLES_REPOSITORY.items())]
        options.append(("0", "Back"))

        print_screen(menu_screen("Example Circuits", options))
        choice = clean_input(prompt())

        if choice == "0":
            return

        if choice in EXAMPLES_REPOSITORY:
            card = EXAMPLES_REPOSITORY[choice]

            card_info = [
                f"Title   : {card.title}",
                f"Purpose : {card.purpose}",
                f"Context : {card.real_world_application}",
                "",
                "Schematic Diagram:",
                *format_custom_flow_diagram(card.diagram_key),
            ]

            print_screen(explanation_screen("Circuit Specification", card_info))

            load_opt = clean_input(prompt("Load this circuit? (y/n)")).lower()
            if load_opt == "y":
                load_example_into_circuit(card, circuit)
                print_screen(success_message(f"Loaded '{card.title}' into workspace."))
                pause()
                return
        else:
            print_screen(error_screen("Invalid choice."))
            pause()


def main() -> None:
    """Main entry point for the Circuit Simulator module."""
    active_circuit = Circuit()

    while True:
        options = [
            ("1", "Circuit Builder"),
            ("2", "View Architecture"),
            ("3", "Run Simulation"),
            ("4", "Example Circuits"),
            ("5", "Learn Circuit Design"),
            ("6", "Reset Workspace"),
            ("0", "Back"),
        ]

        print_screen(menu_screen("Logic Circuit Simulator", options))
        user_choice = clean_input(prompt())

        if user_choice == "0":
            return

        try:
            if user_choice == "1":
                run_interactive_circuit_builder_workspace(active_circuit)
            elif user_choice == "2":
                lines = generate_static_ascii_layout(active_circuit)
                print_screen(explanation_screen("Circuit Architecture", lines))
                pause()
            elif user_choice == "3":
                run_simulation(active_circuit)
            elif user_choice == "4":
                explore_built_in_example_circuits(active_circuit)
            elif user_choice == "5":
                show_lessons()
            elif user_choice == "6":
                active_circuit.clear()
                print_screen(success_message("Workspace reset."))
                pause()
            else:
                print_screen(error_screen("Invalid choice. Please enter 0-6."))
                pause()
        except (KeyboardInterrupt, ReturnToMainMenu):
            print_screen(success_message("Returning to menu."))
            return
        except (TriCoreError, ValueError, IndexError) as err:
            print_screen(error_screen(str(err)))
            pause()
