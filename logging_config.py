"""Logging configuration helpers for TriCore applications."""

from __future__ import annotations

import logging
from typing import Final

DEFAULT_LOG_FORMAT: Final = "%(levelname)s:%(name)s:%(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application logging.

    Args:
        level: Logging threshold such as ``logging.INFO`` or ``logging.DEBUG``.
    """

    logging.basicConfig(level=level, format=DEFAULT_LOG_FORMAT)
