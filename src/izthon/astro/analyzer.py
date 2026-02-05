from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from ..data import MUTAGEN
from ..i18n import kot
from ..util import fix_earthly_branch_index, fix_index, get_mutagens_by_heavenly_stem

if TYPE_CHECKING:
    from ..star.functional_star import FunctionalStar
    from .functional_astrolabe import FunctionalAstrolabe
    from .functional_palace import FunctionalPalace
    from .functional_surpalaces import FunctionalSurpalaces


def _concat_star_keys(*stars: Iterable["FunctionalStar"]) -> list[str]:
    return [kot(star.name) for star in stars]


def _include_all(all_star_keys: list[str], target_star_names: list[str]) -> bool:
    target_keys = [kot(name) for name in target_star_names]
    return all(key in all_star_keys for key in target_keys)


def _exclude_all(all_star_keys: list[str], target_star_names: list[str]) -> bool:
    target_keys = [kot(name) for name in target_star_names]
    return all(key not in all_star_keys for key in target_keys)


def _include_one_of(all_star_keys: list[str], target_star_names: list[str]) -> bool:
    target_keys = [kot(name) for name in target_star_names]
    return any(key in all_star_keys for key in target_keys)


def _include_mutagen(stars: Iterable["FunctionalStar"], mutagen: str) -> bool:
    mutagen_key = kot(mutagen)
    for star in stars:
        if star.mutagen and kot(star.mutagen) == mutagen_key:
            return True
    return False


def get_surrounded_palaces(astrolabe: "FunctionalAstrolabe", index_or_name: int | str) -> "FunctionalSurpalaces":
    palace = get_palace(astrolabe, index_or_name)
    if palace is None:
        raise ValueError("index_or_name is incorrect.")

    palace_index = fix_earthly_branch_index(palace.earthly_branch)
    opposite = get_palace(astrolabe, fix_index(palace_index + 6))
    career = get_palace(astrolabe, fix_index(palace_index + 4))
    wealth = get_palace(astrolabe, fix_index(palace_index + 8))

    if not opposite or not career or not wealth:
        raise ValueError("index_or_name is incorrect.")

    from .functional_surpalaces import FunctionalSurpalaces

    return FunctionalSurpalaces(target=palace, opposite=opposite, wealth=wealth, career=career)


def get_palace(astrolabe: "FunctionalAstrolabe", index_or_name: int | str) -> "FunctionalPalace | None":
    palace: FunctionalPalace | None = None

    if isinstance(index_or_name, int):
        if index_or_name < 0 or index_or_name > 11:
            raise ValueError("invalid palace index.")
        palace = astrolabe.palaces[index_or_name]
    else:
        name_key = kot(index_or_name)
        for item in astrolabe.palaces:
            if name_key == "originalPalace" and item.is_original_palace:
                palace = item
                break
            if name_key == "bodyPalace" and item.is_body_palace:
                palace = item
                break
            if kot(item.name) == kot(index_or_name):
                palace = item
                break

    if palace:
        palace.set_astrolabe(astrolabe)
    return palace


def has_stars(palace: "FunctionalPalace", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(*palace.major_stars, *palace.minor_stars, *palace.adjective_stars)
    return _include_all(all_keys, stars)


def not_have_stars(palace: "FunctionalPalace", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(*palace.major_stars, *palace.minor_stars, *palace.adjective_stars)
    return _exclude_all(all_keys, stars)


def has_one_of_stars(palace: "FunctionalPalace", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(*palace.major_stars, *palace.minor_stars, *palace.adjective_stars)
    return _include_one_of(all_keys, stars)


def has_mutagen_in_palace(palace: "FunctionalPalace", mutagen: str) -> bool:
    return _include_mutagen([*palace.major_stars, *palace.minor_stars], mutagen)


def not_have_mutagen_in_palace(palace: "FunctionalPalace", mutagen: str) -> bool:
    return not has_mutagen_in_palace(palace, mutagen)


def is_surrounded_by_stars(surpalaces: "FunctionalSurpalaces", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(
        *surpalaces.target.major_stars,
        *surpalaces.target.minor_stars,
        *surpalaces.target.adjective_stars,
        *surpalaces.opposite.major_stars,
        *surpalaces.opposite.minor_stars,
        *surpalaces.opposite.adjective_stars,
        *surpalaces.wealth.major_stars,
        *surpalaces.wealth.minor_stars,
        *surpalaces.wealth.adjective_stars,
        *surpalaces.career.major_stars,
        *surpalaces.career.minor_stars,
        *surpalaces.career.adjective_stars,
    )
    return _include_all(all_keys, stars)


def not_surrounded_by_stars(surpalaces: "FunctionalSurpalaces", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(
        *surpalaces.target.major_stars,
        *surpalaces.target.minor_stars,
        *surpalaces.target.adjective_stars,
        *surpalaces.opposite.major_stars,
        *surpalaces.opposite.minor_stars,
        *surpalaces.opposite.adjective_stars,
        *surpalaces.wealth.major_stars,
        *surpalaces.wealth.minor_stars,
        *surpalaces.wealth.adjective_stars,
        *surpalaces.career.major_stars,
        *surpalaces.career.minor_stars,
        *surpalaces.career.adjective_stars,
    )
    return _exclude_all(all_keys, stars)


def is_surrounded_by_one_of_stars(surpalaces: "FunctionalSurpalaces", stars: list[str]) -> bool:
    all_keys = _concat_star_keys(
        *surpalaces.target.major_stars,
        *surpalaces.target.minor_stars,
        *surpalaces.target.adjective_stars,
        *surpalaces.opposite.major_stars,
        *surpalaces.opposite.minor_stars,
        *surpalaces.opposite.adjective_stars,
        *surpalaces.wealth.major_stars,
        *surpalaces.wealth.minor_stars,
        *surpalaces.wealth.adjective_stars,
        *surpalaces.career.major_stars,
        *surpalaces.career.minor_stars,
        *surpalaces.career.adjective_stars,
    )
    return _include_one_of(all_keys, stars)


def mutagens_to_stars(heavenly_stem: str, mutagens: str | list[str]) -> list[str]:
    muts = mutagens if isinstance(mutagens, list) else [mutagens]
    stars: list[str] = []
    mutagen_stars = get_mutagens_by_heavenly_stem(heavenly_stem)

    for with_mutagen in muts:
        try:
            mutagen_index = MUTAGEN.index(kot(with_mutagen))
        except ValueError:
            continue
        if mutagen_stars[mutagen_index]:
            stars.append(mutagen_stars[mutagen_index])

    return stars
