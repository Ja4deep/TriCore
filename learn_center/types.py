"""Shared curriculum types for the Learning Center."""

from __future__ import annotations

from textwrap import dedent
from typing import TypedDict

LessonSection = tuple[str, list[str]]


class Lesson(TypedDict):
    """A single Learning Center lesson."""

    menu_title: str
    title: str
    question: str
    sections: list[LessonSection]


class CurriculumSection(TypedDict):
    """A named group of related Learning Center lessons."""

    menu_title: str
    title: str
    lessons: list[Lesson]


def page(heading: str, body: str) -> LessonSection:
    """Return a lesson page from readable multiline source text."""
    return heading, dedent(body).strip("\n").splitlines()
