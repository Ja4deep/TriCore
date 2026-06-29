"""Project-wide exception hierarchy for TriCore.

The concrete exceptions inherit from ``ValueError`` where earlier public APIs
raised ``ValueError``. This preserves backward compatibility while allowing
callers to catch domain-specific failures.
"""

from __future__ import annotations


class TriCoreError(Exception):
    """Base exception for all TriCore domain errors."""


class TriCoreValueError(TriCoreError, ValueError):
    """Base class for TriCore validation errors compatible with ``ValueError``."""


class InvalidNumberError(TriCoreValueError):
    """Raised when a number string or trit is malformed."""


class InvalidBaseError(TriCoreValueError):
    """Raised when an unsupported numeric base is requested."""


class DivisionByZeroError(TriCoreValueError):
    """Raised when division by zero is attempted."""


class InvalidGateError(TriCoreValueError):
    """Raised when a logic gate name, arity, or signal value is invalid."""


class InvalidCircuitError(TriCoreValueError):
    """Raised when a circuit graph is malformed or incomplete."""


class SimulationError(TriCoreValueError):
    """Raised when a circuit simulation cannot complete."""
