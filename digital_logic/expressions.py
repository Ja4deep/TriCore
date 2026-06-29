"""Ternary logic expression parser and evaluator for digital logic lessons."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .logic_gates import evaluate_gate, get_gate
from .validation import validate_expression_text

TOKEN_PATTERN = re.compile(r"\s*([A-Za-z][A-Za-z0-9_]*|[()]|.)")
TERNARY_PRECEDENCE = {
    "MAX": 1,
    "NMAX": 1,
    "MIN": 2,
    "NMIN": 2,
    "SUM": 3,
}
OPERATORS = {"NOT", *TERNARY_PRECEDENCE}


@dataclass(frozen=True, slots=True)
class ExpressionStep:
    """Describe one step in a ternary logic expression evaluation."""

    expression: str
    result: int
    explanation: str


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Structured result from evaluating a ternary logic expression."""

    expression: str
    assignments: dict[str, int]
    result: int
    steps: list[ExpressionStep]


@dataclass(frozen=True, slots=True)
class VariableNode:
    """AST node representing a ternary logic variable."""

    name: str


@dataclass(frozen=True, slots=True)
class UnaryNode:
    """AST node representing a unary ternary logic operation."""

    operator: str
    operand: "ExpressionNode"


@dataclass(frozen=True, slots=True)
class TernaryNode:
    """AST node representing a ternary logic operation."""

    operator: str
    left: "ExpressionNode"
    right: "ExpressionNode"


ExpressionNode = VariableNode | UnaryNode | TernaryNode


def tokenize_expression(expression: str) -> list[str]:
    """Tokenize a ternary logic expression into identifiers and parentheses."""
    normalized_expression = validate_expression_text(expression)
    tokens = []

    for match in TOKEN_PATTERN.finditer(normalized_expression):
        token = match.group(1)
        if token.isspace():
            continue
        if token in {"(", ")"}:
            tokens.append(token)
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
            tokens.append(token.upper())
            continue
        raise ValueError(f"Unexpected token {token!r} in logic expression.")
    if not tokens:
        raise ValueError("Logic expression cannot be empty.")
    return tokens


class ExpressionParser:
    """Recursive-descent parser for ternary logic expressions."""

    def __init__(self, tokens: list[str]) -> None:
        """Store tokens and initialize the parser cursor."""
        self.tokens = tokens
        self.position = 0

    def parse(self) -> ExpressionNode:
        """Parse all tokens into an expression tree."""
        if not self.tokens:
            raise ValueError("Logic expression cannot be empty.")
        expression = self._parse_expression(0)
        if self._peek() is not None:
            raise ValueError(f"Unexpected token {self._peek()!r} after expression.")

        return expression

    def _parse_expression(self, minimum_precedence: int) -> ExpressionNode:
        """Parse a ternary expression using precedence climbing."""
        left = self._parse_unary()

        while True:
            operator = self._peek()

            if operator is None or operator not in TERNARY_PRECEDENCE:
                break

            precedence = TERNARY_PRECEDENCE[operator]

            if precedence < minimum_precedence:
                break

            self._advance()
            right = self._parse_expression(precedence + 1)
            left = TernaryNode(operator, left, right)

        return left

    def _parse_unary(self) -> ExpressionNode:
        """Parse variables, parenthesized expressions, and NOT expressions."""
        token = self._peek()
        if token is None:
            raise ValueError("Expression ended before an operand was found.")

        if token == "NOT":
            self._advance()
            return UnaryNode("NOT", self._parse_unary())

        if token == "(":
            self._advance()
            expression = self._parse_expression(0)
            if self._peek() != ")":
                raise ValueError("Missing closing parenthesis.")
            self._advance()
            return expression

        if token == ")":
            raise ValueError("Unexpected closing parenthesis.")

        if token in OPERATORS:
            raise ValueError(f"Operator {token} is missing a left operand.")

        self._advance()
        return VariableNode(token)

    def _peek(self) -> str | None:
        """Return the current token without consuming it."""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def _advance(self) -> str:
        """Consume and return the current token."""
        token = self.tokens[self.position]
        self.position += 1
        return token


def parse_expression(expression: str) -> ExpressionNode:
    """Parse a ternary logic expression into an abstract syntax tree."""
    return ExpressionParser(tokenize_expression(expression)).parse()


def expression_variables(expression: str) -> list[str]:
    """Return sorted variable names used by a ternary logic expression."""
    tree = parse_expression(expression)
    variables: set[str] = set()

    def visit(node: ExpressionNode) -> None:
        if isinstance(node, VariableNode):
            variables.add(node.name)
            return
        if isinstance(node, UnaryNode):
            visit(node.operand)
            return
        visit(node.left)
        visit(node.right)

    visit(tree)
    return sorted(variables)


def render_expression(node: ExpressionNode) -> str:
    """Return a readable expression string for an AST node."""
    if isinstance(node, VariableNode):
        return node.name
    if isinstance(node, UnaryNode):
        operand = render_expression(node.operand)
        if isinstance(node.operand, TernaryNode):
            operand = f"({operand})"
        return f"NOT {operand}"

    left = render_expression(node.left)
    right = render_expression(node.right)
    if isinstance(node.left, TernaryNode):
        left = f"({left})"
    if isinstance(node.right, TernaryNode):
        right = f"({right})"
    return f"{left} {node.operator} {right}"


def evaluate_expression(
    expression: str,
    assignments: dict[str, int],
) -> EvaluationResult:
    """Evaluate a ternary logic expression with step-by-step explanations."""
    normalized_expression = validate_expression_text(expression)
    tree = parse_expression(normalized_expression)
    normalized_assignments = normalize_assignments(assignments)
    steps: list[ExpressionStep] = []

    result = _evaluate_node(tree, normalized_assignments, steps)
    return EvaluationResult(
        expression=render_expression(tree),
        assignments=normalized_assignments,
        result=result,
        steps=steps,
    )


def normalize_assignments(assignments: dict[str, int]) -> dict[str, int]:
    """Return uppercase ternary assignments with friendly validation errors."""
    normalized_assignments: dict[str, int] = {}

    for name, value in assignments.items():
        normalized_name = name.upper()
        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Variable {normalized_name} must be 0, 1, or 2."
            ) from error

        if normalized_value not in {0, 1, 2}:
            raise ValueError(f"Variable {normalized_name} must be 0, 1, or 2.")

        normalized_assignments[normalized_name] = normalized_value

    return normalized_assignments


def _evaluate_node(
    node: ExpressionNode,
    assignments: dict[str, int],
    steps: list[ExpressionStep],
) -> int:
    """Evaluate an AST node and append educational steps."""
    if isinstance(node, VariableNode):
        if node.name not in assignments:
            raise ValueError(f"Missing ternary value for variable {node.name}.")
        value = assignments[node.name]
        if value not in {0, 1, 2}:
            raise ValueError(f"Variable {node.name} must be 0, 1, or 2.")
        steps.append(
            ExpressionStep(
                expression=f"{node.name} = {value}",
                result=value,
                explanation="A variable represents one ternary signal in the circuit.",
            )
        )
        return value

    if isinstance(node, UnaryNode):
        operand_value = _evaluate_node(node.operand, assignments, steps)
        result = evaluate_gate(node.operator, (operand_value,))
        steps.append(
            ExpressionStep(
                expression=f"NOT {operand_value} = {result}",
                result=result,
                explanation=get_gate(node.operator).logic_rule,
            )
        )
        return result

    left_value = _evaluate_node(node.left, assignments, steps)
    right_value = _evaluate_node(node.right, assignments, steps)
    result = evaluate_gate(node.operator, (left_value, right_value))
    steps.append(
        ExpressionStep(
            expression=f"{left_value} {node.operator} {right_value} = {result}",
            result=result,
            explanation=get_gate(node.operator).logic_rule,
        )
    )
    return result
