"""
Interactive terminal builder management workspace interface loop routines.
"""

from __future__ import annotations
from collections.abc import Callable

from arithmetic.utils import clean_input
from exceptions import InvalidCircuitError
from ui.terminal import (
    ReturnToMainMenu,
    error_screen,
    input_screen,
    menu_screen,
    pause,
    print_screen,
    prompt,
    success_message,
)
from logic_circuit_simulator.circuit import Circuit
from logic_circuit_simulator.validation import parse_and_validate_slot_index
from digital_logic.logic_gates import list_gate_names

BuilderAction = Callable[[Circuit], None]

WORKSPACE_OPTIONS = [
    ("1", "Add Input Pin"),
    ("2", "Add Logic Gate"),
    ("3", "Add Output Pin"),
    ("4", "Connect Components"),
    ("5", "Reset Workspace"),
    ("0", "Back"),
]


def run_interactive_circuit_builder_workspace(circuit: Circuit) -> None:
    """Interactive loop for modifying, clearing, or wiring logic graph structures."""
    actions: dict[str, BuilderAction] = {
        "1": _add_input_pin,
        "2": _add_logic_gate,
        "3": _add_output_pin,
        "4": _connect_components,
        "5": _reset_workspace,
    }

    while True:
        print_screen(menu_screen("Circuit Builder Workspace", WORKSPACE_OPTIONS))
        user_choice = clean_input(prompt())

        if user_choice == "0":
            return

        try:
            action = actions.get(user_choice)
            if action is None:
                print_screen(error_screen("Invalid choice. Please enter 0-5."))
                pause()
                continue

            action(circuit)

        except (ValueError, IndexError) as err:
            print_screen(error_screen(str(err)))
            pause()
        except (KeyboardInterrupt, ReturnToMainMenu):
            raise
        except EOFError:
            return


def _add_input_pin(circuit: Circuit) -> None:
    """Prompt for and add a primary input pin."""
    node_id = _read_required(
        "Add Input Pin",
        "Enter a unique ID (e.g., A, IN1):",
        "ID",
        "Node ID cannot be empty.",
    )
    label = _read_required(
        "Add Input Pin",
        f"Enter a label for {node_id}:",
        "Label",
        "Label cannot be empty.",
    )
    circuit.add_input(node_id, label)
    _show_success(f"Input '{node_id}' added.")


def _add_logic_gate(circuit: Circuit) -> None:
    """Prompt for and add a supported logic gate."""
    node_id = _read_required(
        "Add Logic Gate",
        "Enter a unique ID (e.g., G1, M_AND):",
        "ID",
        "Node ID cannot be empty.",
    )
    supported = ", ".join(list_gate_names())
    gate_type = _read_required(
        "Add Logic Gate",
        f"Enter gate type ({supported}):",
        "Type",
        "Gate type cannot be empty.",
    ).upper()

    circuit.add_gate(node_id, gate_type)
    _show_success(f"Gate '{node_id}' ({gate_type}) added.")


def _add_output_pin(circuit: Circuit) -> None:
    """Prompt for and add a primary output pin."""
    node_id = _read_required(
        "Add Output Pin",
        "Enter a unique ID (e.g., OUT, Z):",
        "ID",
        "Node ID cannot be empty.",
    )
    label = _read_required(
        "Add Output Pin",
        f"Enter a label for {node_id}:",
        "Label",
        "Label cannot be empty.",
    )
    circuit.add_output(node_id, label)
    _show_success(f"Output '{node_id}' added.")


def _connect_components(circuit: Circuit) -> None:
    """Prompt for and connect two existing circuit components."""
    source_id = _read_required(
        "Connect Components",
        "Enter source node ID:",
        "Source ID",
        "Source ID cannot be empty.",
    )
    target_id = _read_required(
        "Connect Components",
        "Enter target node ID:",
        "Target ID",
        "Target ID cannot be empty.",
    )
    print_screen(
        input_screen(
            "Connect Components",
            "Enter target input slot index (default 0):",
        )
    )
    slot_raw = clean_input(prompt("Slot Index"))
    slot = parse_and_validate_slot_index(slot_raw) if slot_raw else 0

    circuit.connect(source_id, target_id, slot)
    _show_success(f"Connected {source_id} to {target_id} (slot {slot}).")


def _reset_workspace(circuit: Circuit) -> None:
    """Clear the active circuit workspace."""
    circuit.clear()
    _show_success("Workspace reset.")


def _read_required(
    title: str,
    message: str,
    prompt_label: str,
    empty_message: str,
) -> str:
    """Read a non-empty terminal value from the user."""
    print_screen(input_screen(title, message))
    value = clean_input(prompt(prompt_label))
    if not value:
        raise InvalidCircuitError(empty_message)

    return value


def _show_success(message: str) -> None:
    """Display a success message and pause for the user."""
    print_screen(success_message(message))
    pause()
