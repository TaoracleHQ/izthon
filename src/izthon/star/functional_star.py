from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from ..i18n import kot

if TYPE_CHECKING:
    from ..astro.functional_astrolabe import FunctionalAstrolabe
    from ..astro.functional_palace import FunctionalPalace
    from ..astro.functional_surrounding_palaces import FunctionalSurroundingPalaces


StarType = Literal["major", "soft", "tough", "lucun", "tianma", "flower", "helper", "adjective"]
Scope = Literal["origin", "decadal", "yearly", "monthly", "daily", "hourly"]


@dataclass
class FunctionalStar:
    name: str
    type: str
    scope: str
    brightness: str | None = None
    mutagen: str | None = None

    _palace: "FunctionalPalace | None" = None
    _astrolabe: "FunctionalAstrolabe | None" = None

    def set_palace(self, palace: "FunctionalPalace") -> None:
        self._palace = palace

    def set_astrolabe(self, astrolabe: "FunctionalAstrolabe") -> None:
        self._astrolabe = astrolabe

    def palace(self) -> "FunctionalPalace | None":
        return self._palace

    def surrounding_palaces(self) -> "FunctionalSurroundingPalaces | None":
        if not self._palace or not self._astrolabe:
            return None
        return self._astrolabe.surrounding_palaces(self._palace.name)

    def opposite_palace(self) -> "FunctionalPalace | None":
        sp = self.surrounding_palaces()
        return sp.opposite if sp else None

    def with_mutagen(self, mutagen: str | list[str]) -> bool:
        if not self.mutagen:
            return False
        if isinstance(mutagen, list):
            return any(kot(mt) == kot(self.mutagen) for mt in mutagen)
        return kot(mutagen) == kot(self.mutagen)

    def with_brightness(self, brightness: str | list[str]) -> bool:
        if not self.brightness:
            return False
        if isinstance(brightness, list):
            return any(kot(b) == kot(self.brightness) for b in brightness)
        return kot(brightness) == kot(self.brightness)
