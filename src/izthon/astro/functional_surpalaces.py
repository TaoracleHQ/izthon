from __future__ import annotations

from dataclasses import dataclass

from . import analyzer


@dataclass
class FunctionalSurpalaces:
    target: "FunctionalPalace"
    opposite: "FunctionalPalace"
    wealth: "FunctionalPalace"
    career: "FunctionalPalace"

    def have(self, stars: list[str]) -> bool:
        return analyzer.is_surrounded_by_stars(self, stars)

    def not_have(self, stars: list[str]) -> bool:
        return analyzer.not_surrounded_by_stars(self, stars)

    def have_one_of(self, stars: list[str]) -> bool:
        return analyzer.is_surrounded_by_one_of_stars(self, stars)

    def have_mutagen(self, mutagen: str) -> bool:
        return (
            self.target.has_mutagen(mutagen)
            or self.opposite.has_mutagen(mutagen)
            or self.wealth.has_mutagen(mutagen)
            or self.career.has_mutagen(mutagen)
        )

    def not_have_mutagen(self, mutagen: str) -> bool:
        return not self.have_mutagen(mutagen)


# Avoid circular imports at runtime; only for type checking / editor hints.
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .functional_palace import FunctionalPalace
