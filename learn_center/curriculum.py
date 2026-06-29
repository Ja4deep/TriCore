"""Course outline for the TriCore Learning Center."""

from __future__ import annotations

from learn_center.content.architecture import SECTION as ARCHITECTURE
from learn_center.content.arithmetic import SECTION as ARITHMETIC
from learn_center.content.conversion import SECTION as CONVERSION
from learn_center.content.digital_logic import SECTION as DIGITAL_LOGIC
from learn_center.content.enrichment import enrich_curriculum
from learn_center.content.extras import SECTION as EXTRAS
from learn_center.content.foundations import SECTION as FOUNDATIONS
from learn_center.content.representation import SECTION as REPRESENTATION
from learn_center.content.simulator import SECTION as SIMULATOR
from learn_center.types import CurriculumSection

RAW_CURRICULUM: list[CurriculumSection] = [
    FOUNDATIONS,
    REPRESENTATION,
    CONVERSION,
    ARITHMETIC,
    DIGITAL_LOGIC,
    SIMULATOR,
    ARCHITECTURE,
    EXTRAS,
]


CURRICULUM: list[CurriculumSection] = enrich_curriculum(RAW_CURRICULUM)
