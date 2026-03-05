from __future__ import annotations

from dataclasses import dataclass

from . import analyzer


@dataclass
class FunctionalSurpalaces:
    target: "FunctionalPalace"
    opposite: "FunctionalPalace"
    wealth: "FunctionalPalace"
    career: "FunctionalPalace"

    def contains_stars(self, stars: list[str]) -> bool:
        return analyzer.is_surrounded_by_stars(self, stars)

    def excludes_stars(self, stars: list[str]) -> bool:
        return analyzer.not_surrounded_by_stars(self, stars)

    def contains_any_star(self, stars: list[str]) -> bool:
        return analyzer.is_surrounded_by_one_of_stars(self, stars)

    def contains_mutagen(self, mutagen: str) -> bool:
        return (
            self.target.contains_mutagen(mutagen)
            or self.opposite.contains_mutagen(mutagen)
            or self.wealth.contains_mutagen(mutagen)
            or self.career.contains_mutagen(mutagen)
        )

    def lacks_mutagen(self, mutagen: str) -> bool:
        return not self.contains_mutagen(mutagen)


# Avoid circular imports at runtime; only for type checking / editor hints.
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .functional_palace import FunctionalPalace
