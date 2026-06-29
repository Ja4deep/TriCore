"""Colorama-backed terminal rendering primitives for TriCore."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from textwrap import wrap

try:
    from colorama import Fore, Style, init
except ImportError:  # pragma: no cover - only used outside the project venv.

    class _NoColor:
        BLACK = ""
        BLUE = ""
        CYAN = ""
        GREEN = ""
        LIGHTWHITE_EX = ""
        RED = ""
        RESET_ALL = ""
        WHITE = ""
        YELLOW = ""

    Fore = Style = _NoColor()  # type: ignore[assignment]

    def init(*_args: object, **_kwargs: object) -> None:
        """Fallback Colorama initializer when Colorama is unavailable."""


init(autoreset=True)


WIDTH = 72
INNER_WIDTH = WIDTH - 2
CONTENT_WIDTH = INNER_WIDTH - 4
TABLE_RULE = "─"

COLOR_TITLE = Fore.CYAN
COLOR_RESULT = Fore.GREEN
COLOR_EXPLANATION = Fore.YELLOW
COLOR_ERROR = Fore.RED
COLOR_NORMAL = Fore.WHITE


def color_text(text: str, color: str = COLOR_NORMAL) -> str:
    """Return text with a Colorama color prefix while keeping plain text readable."""
    return f"{color}{text}{Style.RESET_ALL}"


def _fit_line(text: str, width: int = CONTENT_WIDTH) -> list[str]:
    """Wrap one line to the content width without dropping blank lines."""
    if text == "":
        return [""]

    return wrap(text, width=width, break_long_words=False) or [text[:width]]


def _border(left: str, fill: str, right: str, width: int = INNER_WIDTH) -> str:
    """Return a Unicode box border."""
    return left + (fill * width) + right


def _content_line(text: str = "", *, align: str = "left") -> str:
    """Return a padded box content line."""
    if align == "center":
        padded = text.center(CONTENT_WIDTH)
    elif align == "right":
        padded = text.rjust(CONTENT_WIDTH)
    else:
        padded = text.ljust(CONTENT_WIDTH)

    return f"║  {padded}  ║"


def box(
    title: str,
    lines: Iterable[str] = (),
    *,
    subtitle: str = "",
    color: str = COLOR_NORMAL,
) -> str:
    """Render a bordered section using Unicode box-drawing characters."""
    rendered_lines = [_border("╔", "═", "╗"), _content_line(title, align="center")]

    if subtitle:
        rendered_lines.append(_content_line(subtitle, align="center"))

    rendered_lines.append(_border("╠", "═", "╣"))

    content = list(lines) or [""]
    for line in content:
        for wrapped_line in _fit_line(str(line)):
            rendered_lines.append(_content_line(wrapped_line))

    rendered_lines.append(_border("╚", "═", "╝"))
    return color_text("\n".join(rendered_lines), color)


def menu_screen(
    title: str,
    options: Sequence[tuple[str, str]],
    *,
    subtitle: str = "",
) -> str:
    """Render a consistent menu screen."""
    lines = [f"{key:>2} │ {label}" for key, label in options]
    return box(title, lines, subtitle=subtitle, color=COLOR_TITLE)


def section(title: str, lines: Iterable[str], *, color: str = COLOR_NORMAL) -> str:
    """Render a generic content section."""
    return box(title, lines, color=color)


def input_screen(title: str, prompt_text: str, helper_text: str = "") -> str:
    """Render an input section."""
    lines = [prompt_text]
    if helper_text:
        lines.extend(["", helper_text])

    return box(title, lines, color=COLOR_TITLE)


def result_screen(title: str, lines: Iterable[str]) -> str:
    """Render a result section."""
    return box(title, lines, color=COLOR_RESULT)


def explanation_screen(title: str, lines: Iterable[str]) -> str:
    """Render an explanation section."""
    return box(title, lines, color=COLOR_EXPLANATION)


def error_screen(message: str, *, title: str = "Error") -> str:
    """Render an error section."""
    return box(title, [message], color=COLOR_ERROR)


def success_message(message: str, *, title: str = "Success") -> str:
    """Render a success section."""
    return box(title, [message], color=COLOR_RESULT)


def help_screen(title: str, lines: Iterable[str]) -> str:
    """Render a help section."""
    return box(title, lines, color=COLOR_EXPLANATION)


def print_screen(screen: str) -> None:
    """Print a rendered screen with a leading blank line for readability."""
    print()
    print(screen)
    print()


def prompt(label: str = "Select an option") -> str:
    """Read a user input value with consistent styling."""
    try:
        return input(color_text(f"\n{label}: ", COLOR_NORMAL)).strip()
    except EOFError:
        return "0"


def pause(message: str = "Press Enter to continue") -> None:
    """Pause the interface so students can read the current screen."""
    try:
        input(color_text(f"\n{message}...", COLOR_NORMAL))
    except EOFError:
        print()


def key_value_lines(items: Sequence[tuple[str, object]]) -> list[str]:
    """Return aligned label/value lines for result screens."""
    label_width = max((len(label) for label, _value in items), default=0)
    return [f"{label.ljust(label_width)} : {value}" for label, value in items]


def table_lines(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> list[str]:
    """Return a compact text table that fits inside UI sections."""
    widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows))
        for index, header in enumerate(headers)
    ]
    header_line = "  ".join(
        str(header).ljust(widths[index]) for index, header in enumerate(headers)
    )
    rule = TABLE_RULE * min(CONTENT_WIDTH, len(header_line))
    body = [
        "  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row))
        for row in rows
    ]

    return [header_line, rule, *body]


def message_lines(*lines: str) -> list[str]:
    """Return a reusable list of message lines."""
    return list(lines)


class ReturnToMainMenu(Exception):
    """Signal that a module should return to the TriCore main menu."""

    pass
