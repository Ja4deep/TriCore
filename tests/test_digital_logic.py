import pytest

import digital_logic
from digital_logic.expressions import (
    evaluate_expression,
    expression_variables,
    parse_expression,
    tokenize_expression,
)
from digital_logic.formatter import gate_reference_lines, simulation_diagram_lines
from digital_logic.logic_gates import evaluate_gate, list_gate_names
from digital_logic.simulator import simulate_gate
from digital_logic.truth_tables import generate_truth_table
from digital_logic.validation import (
    normalize_gate_name,
    validate_ternary_value,
    validate_ternary_values,
    validate_expression_text,
)


@pytest.mark.parametrize(
    ("gate_name", "inputs", "expected"),
    [
        ("NOT", (0,), 2),
        ("NOT", (1,), 1),
        ("NOT", (2,), 0),
        ("MIN", (0, 2), 0),
        ("MIN", (1, 2), 1),
        ("MAX", (0, 2), 2),
        ("MAX", (1, 0), 1),
        ("SUM", (1, 1), 2),
        ("SUM", (2, 1), 0),
        ("SUM", (2, 2), 1),
        ("NMIN", (2, 2), 0),
        ("NMIN", (1, 2), 1),
        ("NMAX", (0, 0), 2),
        ("NMAX", (1, 0), 1),
    ],
)
def test_evaluate_gate_returns_expected_output(
    gate_name: str,
    inputs: tuple[int, ...],
    expected: int,
) -> None:
    assert evaluate_gate(gate_name, inputs) == expected


def test_supported_gate_order_matches_digital_logic_menu() -> None:
    assert list_gate_names() == ["NOT", "MIN", "MAX", "SUM", "NMIN", "NMAX"]


@pytest.mark.parametrize(
    ("gate_name", "expected_rows"),
    [
        ("NOT", [(0, 2), (1, 1), (2, 0)]),
        (
            "MIN",
            [
                (0, 0, 0),
                (0, 1, 0),
                (0, 2, 0),
                (1, 0, 0),
                (1, 1, 1),
                (1, 2, 1),
                (2, 0, 0),
                (2, 1, 1),
                (2, 2, 2),
            ],
        ),
    ],
)
def test_generate_truth_table_returns_all_input_combinations(
    gate_name: str,
    expected_rows: list[tuple[int, ...]],
) -> None:
    headers, rows = generate_truth_table(gate_name)

    assert headers[-1] == "Output"
    assert rows == expected_rows


def test_simulate_gate_returns_output_and_educational_explanation() -> None:
    result = simulate_gate("MIN", (1, 2))

    assert result.output == 1
    assert "lowest input value" in result.explanation
    assert "real hardware" in result.explanation


def test_gate_reference_lines_include_circuit_diagram() -> None:
    lines = gate_reference_lines("MIN")

    assert "Circuit Diagram" in lines
    assert "      [MIN]--- Output" in lines


def test_simulation_diagram_lines_annotate_output() -> None:
    result = simulate_gate("NOT", (0,))

    assert simulation_diagram_lines(result) == [
        "A ---[NOT]--- Output",
        "",
        "Output = 2",
    ]


@pytest.mark.parametrize("value", ["0", " 1 ", "2", "\ufeff1"])
def test_validate_ternary_value_accepts_ternary_text(value: str) -> None:
    assert validate_ternary_value(value) in {0, 1, 2}


@pytest.mark.parametrize("value", ["", "3", "true", "1 0"])
def test_validate_ternary_value_rejects_invalid_text(value: str) -> None:
    with pytest.raises(ValueError):
        validate_ternary_value(value)


def test_validate_ternary_values_checks_expected_count() -> None:
    assert validate_ternary_values(["1", "2"], expected_count=2) == (1, 2)

    with pytest.raises(ValueError):
        validate_ternary_values(["1"], expected_count=2)


def test_normalize_gate_name_accepts_case_insensitive_names() -> None:
    assert normalize_gate_name(" min ") == "MIN"


def test_normalize_gate_name_rejects_unknown_gate() -> None:
    with pytest.raises(ValueError):
        normalize_gate_name("MAYBE")


def test_validate_expression_text_rejects_empty_expression() -> None:
    with pytest.raises(ValueError):
        validate_expression_text("")


def test_tokenize_expression_normalizes_operators_and_variables() -> None:
    assert tokenize_expression("not (a max b)") == ["NOT", "(", "A", "MAX", "B", ")"]


@pytest.mark.parametrize(
    ("expression", "assignments", "expected"),
    [
        ("NOT A", {"A": 0}, 2),
        ("A MIN B", {"A": 1, "B": 2}, 1),
        ("A MAX B", {"A": 0, "B": 2}, 2),
        ("A SUM B", {"A": 1, "B": 1}, 2),
        ("(A MIN B) MAX C", {"A": 1, "B": 0, "C": 2}, 2),
        ("NOT (A MAX B)", {"A": 0, "B": 0}, 2),
    ],
)
def test_evaluate_expression_returns_expected_result(
    expression: str,
    assignments: dict[str, int],
    expected: int,
) -> None:
    result = evaluate_expression(expression, assignments)

    assert result.result == expected
    assert result.steps


def test_expression_precedence_matches_ternary_rules() -> None:
    result = evaluate_expression("A MAX B MIN C", {"A": 0, "B": 2, "C": 1})

    assert result.result == 1  # B MIN C is 1, then A MAX 1 is 1


def test_evaluate_expression_returns_canonical_expression_text() -> None:
    result = evaluate_expression("not (a max b)", {"A": 0, "B": 0})

    assert result.expression == "NOT (A MAX B)"
    assert result.result == 2


def test_expression_variables_returns_sorted_variables() -> None:
    assert expression_variables("(C MIN A) MAX B") == ["A", "B", "C"]


@pytest.mark.parametrize(
    "expression",
    [
        "A MIN",
        "MIN A",
        "(A MAX B",
        "A MAX )",
        "A $ B",
        "",
    ],
)
def test_parse_expression_rejects_invalid_syntax(expression: str) -> None:
    with pytest.raises(ValueError):
        parse_expression(expression)


def test_evaluate_expression_rejects_missing_variable_assignment() -> None:
    with pytest.raises(ValueError):
        evaluate_expression("A MIN B", {"A": 1})


def test_evaluate_expression_rejects_non_ternary_assignment() -> None:
    with pytest.raises(ValueError):
        evaluate_expression("A MIN B", {"A": 1, "B": 3})


def test_evaluate_expression_reports_friendly_assignment_type_error() -> None:
    with pytest.raises(ValueError, match="Variable B must be 0, 1, or 2"):
        evaluate_expression("A MIN B", {"A": 1, "B": "HIGH"})  # type: ignore[dict-item]


def test_evaluate_gate_rejects_invalid_arity_and_ternary_values() -> None:
    with pytest.raises(ValueError):
        evaluate_gate("MIN", (1,))

    with pytest.raises(ValueError):
        evaluate_gate("MAX", (1, 3))


def test_digital_logic_main_back_returns_to_caller(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prompts = iter(["0"])
    messages = []

    monkeypatch.setattr(
        digital_logic, "safe_prompt", lambda _label="Enter your choice": next(prompts)
    )
    monkeypatch.setattr(digital_logic, "print_screen", messages.append)

    digital_logic.main()

    assert any("Returning to the main menu" in message for message in messages)


@pytest.mark.parametrize("submenu_choice", ["1", "2", "3", "4", "5"])
def test_digital_logic_submenu_back_returns_to_main_menu(
    monkeypatch: pytest.MonkeyPatch,
    submenu_choice: str,
) -> None:
    prompts = iter([submenu_choice, "0"])
    messages = []

    monkeypatch.setattr(
        digital_logic, "safe_prompt", lambda _label="Enter your choice": next(prompts)
    )
    monkeypatch.setattr(digital_logic, "print_screen", messages.append)

    digital_logic.main()

    assert any("Returning to the main menu" in message for message in messages)
