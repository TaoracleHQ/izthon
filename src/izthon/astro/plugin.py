from __future__ import annotations

from collections.abc import Callable, Iterable
from types import MethodType
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:  # pragma: no cover
    from .functional_astrolabe import FunctionalAstrolabe


Plugin: TypeAlias = Callable[..., object | None]

_PLUGINS: list[Plugin] = []


def load_plugin(plugin: Plugin) -> None:
    _PLUGINS.append(plugin)


def load_plugins(plugins: Iterable[Plugin]) -> None:
    _PLUGINS.extend(plugins)


def get_plugins() -> tuple[Plugin, ...]:
    return tuple(_PLUGINS)


def reset_plugins() -> None:
    _PLUGINS.clear()


def apply_plugin(astrolabe: FunctionalAstrolabe, plugin: Plugin) -> object | None:
    if hasattr(plugin, "__get__"):
        bound_plugin = MethodType(plugin, astrolabe)
        return bound_plugin()
    return plugin(astrolabe)
