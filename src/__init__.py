
from importlib import import_module
from typing import Any, Dict, Tuple

_EXPORTS: Dict[str, Tuple[str, str]] = {
    "SCREEN_WIDTH": ("config", "SCREEN_WIDTH"),
    "SCREEN_HEIGHT": ("config", "SCREEN_HEIGHT"),
    "TILE_SIZE": ("config", "TILE_SIZE"),
    "ROOT_DIR": ("config", "ROOT_DIR"),
    "ASSETS_DIR": ("config", "ASSETS_DIR"),
    "IMAGES_DIR": ("config", "IMAGES_DIR"),
    "DATA_DIR": ("config", "DATA_DIR"),

    # database (JSON data)
    "MOVES_DB": ("core.database", "MOVES_DB"),
    "POKEDEX_DB": ("core.database", "POKEDEX_DB"),
    "ITEMS_DB": ("core.database", "ITEMS_DB"),
    "TYPES_DB": ("core.database", "TYPES_DB"),

    # core models
    "Trainer": ("core.models.classes", "Trainer"),
    "Pokemon": ("core.models.classes", "Pokemon"),
    "Move": ("core.models.classes", "Move"),
    "Item": ("core.models.classes", "Item"),

    # world management
    "SceneManager": ("world.manager", "SceneManager"),
    "WorldScene": ("world.scenes", "WorldScene"),
    "PokecenterScene": ("world.scenes", "PokecenterScene"),

    # battle (controller only)
    "BattleController": ("battle.controller", "BattleController"),
    "BattleScene": ("battle.scene", "BattleScene"),
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> Any:
    if name in _EXPORTS:
        rel_module, attr = _EXPORTS[name]
        full_module = f"{__name__}.{rel_module}"
        module = import_module(full_module)
        return getattr(module, attr)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list:
    return sorted(list(globals().keys()) + __all__)
