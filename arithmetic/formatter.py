"""Reusable terminal formatting helpers for arithmetic lessons."""

from __future__ import annotations

from typing import Iterable, Sequence


DEFAULT_WIDTH = 40


def separator(width: int = DEFAULT_WIDTH, character: str = "─") -> str:
    """Return a horizontal separator line."""
    if width < 1:
        raise ValueError("Width must be at least 1.")
    if len(character) != 1:
        raise ValueError("Separator character must be a single character.")

    return character * width


def centered_title(title: str, width: int = DEFAULT_WIDTH) -> str:
    """Return a title centered within the requested width."""
    return title.center(width)


def title_block(
    title: str,
    subtitle: str = "",
    *,
    width: int = DEFAULT_WIDTH,
    character: str = "═",
) -> str:
    """Return a reusable title block with optional subtitle."""
    lines = [separator(width, character), centered_title(title, width)]

    if subtitle:
        lines.append(centered_title(subtitle, width))

    lines.append(separator(width, character))
    return "\n".join(lines)


def blank_lines(count: int = 1) -> str:
    """Return a reusable block of blank lines."""
    if count < 0:
        raise ValueError("Blank line count cannot be negative.")

    return "\n" * count


def indent(text: str, spaces: int = 4) -> str:
    """Indent every non-empty line in text by the requested number of spaces."""
    if spaces < 0:
        raise ValueError("Indent spaces cannot be negative.")

    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def align_arithmetic_expression(
    top: str,
    bottom: str,
    operator: str,
    result: str | None = None,
    *,
    padding: int = 1,
) -> str:
    """Return a vertically aligned arithmetic expression.

    Args:
        top: The top operand.
        bottom: The bottom operand.
        operator: The operation symbol.
        result: Optional result line.
        padding: Spaces between the operator and bottom operand.
    """
    if not operator:
        raise ValueError("Operator cannot be empty.")
    if padding < 0:
        raise ValueError("Padding cannot be negative.")

    operator_prefix = operator + (" " * padding)
    operand_width = max(len(top), len(bottom), len(result or ""))
    line_width = len(operator_prefix) + operand_width

    lines = [
        (" " * len(operator_prefix)) + top.rjust(operand_width),
        operator_prefix + bottom.rjust(operand_width),
        separator(line_width, "─"),
    ]

    if result is not None:
        lines.append((" " * len(operator_prefix)) + result.rjust(operand_width))

    return "\n".join(lines)


def box_output(
    lines: Iterable[str],
    *,
    title: str = "",
    width: int | None = None,
    padding: int = 1,
) -> str:
    """Return text wrapped in a Unicode box."""
    content_lines = [str(line) for line in lines]
    if title:
        content_lines.insert(0, title)

    content_width = max((len(line) for line in content_lines), default=0)
    inner_width = max(width or 0, content_width + (padding * 2))
    border = "╔" + separator(inner_width, "═") + "╗"
    bottom_border = "╚" + separator(inner_width, "═") + "╝"
    padded_lines = []

    for line in content_lines:
        padded = (" " * padding) + line
        padded_lines.append("║" + padded.ljust(inner_width) + "║")

    return "\n".join([border, *padded_lines, bottom_border])


def render_menu(
    title: str,
    options: Sequence[tuple[str, str]],
    *,
    prompt: str = "",
    width: int = DEFAULT_WIDTH,
) -> str:
    """Return reusable menu text without printing it directly."""
    lines = [title, separator(width, "─")]

    for key, label in options:
        lines.append(f"{key}. {label}")

    if prompt:
        lines.extend(["", prompt])

    return "\n".join(lines)


def join_sections(sections: Sequence[str], spacing: int = 1) -> str:
    """Join non-empty sections with reusable vertical spacing."""
    if spacing < 0:
        raise ValueError("Spacing cannot be negative.")

    separator_text = "\n" * (spacing + 1)
    return separator_text.join(section for section in sections if section)
