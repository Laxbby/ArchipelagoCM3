from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import CookingMama3World


def create_and_connect_regions(world: CookingMama3World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: CookingMama3World) -> None:
    regions = [Region("Top Menu", world.player, world.multiworld),
               Region("Cook With Mama Recipes", world.player, world.multiworld),
               Region("Let's Cook Friends List", world.player, world.multiworld),
               Region("Let's Cook Recipes", world.player, world.multiworld),
               Region("Let's Match", world.player, world.multiworld),
               Region("Bonuses", world.player, world.multiworld),
               ]
    if world.options.enable_shop_mode_checks > 0:
        regions.append(Region("Let's Shop", world.player, world.multiworld))
    if world.options.enable_cooking_challenge_checks > 0:
        regions.append(Region("Cooking Contest", world.player, world.multiworld))

    world.multiworld.regions += regions


def connect_regions(world: CookingMama3World) -> None:
    top_menu = world.get_region("Top Menu")
    cook_with_mama = world.get_region("Cook With Mama Recipes")
    lets_cook_friend = world.get_region("Let's Cook Friends List")
    lets_cook_recipe = world.get_region("Let's Cook Recipes")
    lets_match = world.get_region("Let's Match")
    bonuses = world.get_region("Bonuses")

    top_menu.connect(cook_with_mama, "Cook With Mama Mode", lambda state: state.has_group("Recipes", world.player, count=1))
    top_menu.connect(lets_cook_friend, "Friends List", lambda state: state.has_group("Friends", world.player, count=1))
    lets_cook_friend.connect(lets_cook_recipe, "Let's Cook Mode", lambda state: state.has_group("Recipes", world.player, count=1))
    top_menu.connect(lets_match, "Let's Match Mode", lambda state: state.has_group("Ingredients", world.player, count=2))
    top_menu.connect(bonuses, "Bonus Prize", lambda state: state.has_group("Recipes", world.player, count=1))


    if world.options.enable_shop_mode_checks > 0:
        lets_shop = world.get_region("Let's Shop")
        top_menu.connect(lets_shop, "Let's Shop Mode", lambda state: state.has_group("Shopping", world.player, count=1))

    if world.options.enable_shop_mode_checks > 0:
        cooking_contest = world.get_region("Cooking Contest")
        top_menu.connect(cooking_contest, "Let's Shop Mode", lambda state: state.has_group("Cooking Contests", world.player, count=1))

