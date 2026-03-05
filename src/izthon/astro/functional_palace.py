from __future__ import annotations

from dataclasses import dataclass, field

from . import analyzer
from .palace import Decadal


@dataclass
class FunctionalPalace:
    index: int
    name: str
    is_body_palace: bool
    is_original_palace: bool
    heavenly_stem: str
    earthly_branch: str
    major_stars: list["FunctionalStar"] = field(default_factory=list)
    minor_stars: list["FunctionalStar"] = field(default_factory=list)
    adjective_stars: list["FunctionalStar"] = field(default_factory=list)
    changsheng12: str = ""
    boshi12: str = ""
    jiangqian12: str = ""
    suiqian12: str = ""
    decadal: Decadal | None = None
    ages: list[int] = field(default_factory=list)

    _astrolabe: "FunctionalAstrolabe | None" = None

    def set_astrolabe(self, astrolabe: "FunctionalAstrolabe") -> None:
        self._astrolabe = astrolabe

    def astrolabe(self) -> "FunctionalAstrolabe | None":
        return self._astrolabe

    def contains_stars(self, stars: list[str]) -> bool:
        return analyzer.has_stars(self, stars)

    def excludes_stars(self, stars: list[str]) -> bool:
        return analyzer.not_have_stars(self, stars)

    def contains_any_star(self, stars: list[str]) -> bool:
        return analyzer.has_one_of_stars(self, stars)

    def contains_mutagen(self, mutagen: str) -> bool:
        return analyzer.has_mutagen_in_palace(self, mutagen)

    def lacks_mutagen(self, mutagen: str) -> bool:
        return analyzer.not_have_mutagen_in_palace(self, mutagen)

    def is_empty(self, exclude_stars: list[str] | None = None) -> bool:
        if [s for s in self.major_stars if s.type == "major"]:
            return False

        if exclude_stars and self.contains_any_star(exclude_stars):
            return False

        return True

    def flies_to(self, to: int | str, with_mutagens: str | list[str]) -> bool:
        astrolabe = self.astrolabe()
        if not astrolabe:
            raise ValueError("palace is detached from astrolabe.")
        to_palace = astrolabe.palace(to)

        stars = analyzer.mutagens_to_stars(self.heavenly_stem, with_mutagens)
        if not stars:
            return False
        return to_palace.contains_stars(stars)

    def flies_one_of_to(self, to: int | str, with_mutagens: list[str]) -> bool:
        astrolabe = self.astrolabe()
        if not astrolabe:
            raise ValueError("palace is detached from astrolabe.")
        to_palace = astrolabe.palace(to)

        stars = analyzer.mutagens_to_stars(self.heavenly_stem, with_mutagens)
        if not stars:
            return True
        return to_palace.contains_any_star(stars)

    def not_fly_to(self, to: int | str, with_mutagens: str | list[str]) -> bool:
        astrolabe = self.astrolabe()
        if not astrolabe:
            raise ValueError("palace is detached from astrolabe.")
        to_palace = astrolabe.palace(to)

        stars = analyzer.mutagens_to_stars(self.heavenly_stem, with_mutagens)
        if not stars:
            return True
        return to_palace.excludes_stars(stars)

    def self_mutaged(self, with_mutagens: str | list[str]) -> bool:
        stars = analyzer.mutagens_to_stars(self.heavenly_stem, with_mutagens)
        return self.contains_stars(stars)

    def self_mutaged_one_of(self, with_mutagens: list[str] | None = None) -> bool:
        muts = with_mutagens or ["禄", "权", "科", "忌"]
        stars = analyzer.mutagens_to_stars(self.heavenly_stem, muts)
        return self.contains_any_star(stars)

    def not_self_mutaged(self, with_mutagens: str | list[str] | None = None) -> bool:
        muts = with_mutagens or ["禄", "权", "科", "忌"]
        stars = analyzer.mutagens_to_stars(self.heavenly_stem, muts)
        return self.excludes_stars(stars)

    def mutaged_places(self) -> list["FunctionalPalace | None"]:
        astrolabe = self.astrolabe()
        if not astrolabe:
            raise ValueError("palace is detached from astrolabe.")

        stars = analyzer.mutagens_to_stars(self.heavenly_stem, ["禄", "权", "科", "忌"])
        return [astrolabe.star(star).palace() for star in stars]


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..star.functional_star import FunctionalStar
    from .functional_astrolabe import FunctionalAstrolabe
