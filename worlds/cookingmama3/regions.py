from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import CookingMama3World


def create_and_connect_regions(world: CookingMama3World) -> None:
    create_all_regions(world)

def create_all_regions(world: CookingMama3World) -> None:
    regions = [Region("Top Menu", world.player, world.multiworld)]

    world.multiworld.regions += regions

