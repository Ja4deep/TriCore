"""Central configuration constants for TriCore.

Constants in this module are intentionally small and dependency-free so they
can be reused by arithmetic, conversion, digital logic, simulator, and UI code.
"""

from __future__ import annotations

from typing import Final

PROJECT_NAME: Final = "TriCore"
PROJECT_SUBTITLE: Final = "Educational Ternary Computing Lab"

SUPPORTED_BASE: Final = 3
SUPPORTED_BASES: Final = frozenset({SUPPORTED_BASE})

ORDINARY_TERNARY_DIGITS: Final = frozenset({"0", "1", "2"})
BALANCED_TERNARY_DIGITS: Final = frozenset({"T", "0", "1"})
TERNARY_SIGNAL_VALUES: Final = frozenset({0, 1, 2})
TERNARY_SIGNAL_DIGITS: Final = frozenset({"0", "1", "2"})

BOM_CHARACTERS: Final = ("\ufeff", "\xef\xbb\xbf")

DEFAULT_THEME: Final = "terminal"
ENABLE_EXPLANATION_MODE_DEFAULT: Final = False
MAX_DIGITS: Final = 10_000
