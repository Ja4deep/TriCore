"""Structured explanation objects for arithmetic lessons."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


@dataclass(frozen=True, slots=True)
class ExplanationStep:
    """Describe one educational step in an arithmetic operation.

    Attributes:
        title: Short label such as "Step 1".
        expression: The arithmetic expression for the step.
        explanation: Human-readable explanation of what happened.
    """

    title: str
    expression: str
    explanation: str


@dataclass(frozen=True, slots=True)
class ArithmeticResult:
    """Structured return value for future arithmetic operations.

    Attributes:
        result: Final result as a number-system string.
        carries: Carry values produced during the operation.
        borrows: Borrow values produced during the operation.
        steps: Educational explanation steps.
        metadata: Optional operation-specific details.
    """

    result: str
    carries: list[int] = field(default_factory=list)
    borrows: list[int] = field(default_factory=list)
    steps: list[ExplanationStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def create_step(title: str, expression: str, explanation: str) -> ExplanationStep:
    """Create a single reusable explanation step."""
    return ExplanationStep(
        title=title,
        expression=expression,
        explanation=explanation,
    )


def number_steps(steps: Iterable[tuple[str, str]]) -> list[ExplanationStep]:
    """Create numbered explanation steps from expression/explanation pairs.

    Args:
        steps: Pairs in the form (expression, explanation).

    Returns:
        Numbered explanation steps.
    """
    return [
        create_step(f"Step {index}", expression, explanation)
        for index, (expression, explanation) in enumerate(steps, start=1)
    ]


def render_step(step: ExplanationStep) -> str:
    """Return a terminal-friendly string for one explanation step."""
    lines = [step.title]

    if step.expression:
        lines.append(step.expression)

    if step.explanation:
        lines.append(step.explanation)

    return "\n".join(lines)


def render_steps(steps: Sequence[ExplanationStep], separator: str = "\n\n") -> str:
    """Return terminal-friendly text for a sequence of explanation steps."""
    return separator.join(render_step(step) for step in steps)
