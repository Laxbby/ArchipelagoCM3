from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import items, locations, rules
from .regions import create_and_connect_regions
from .options import CookingMama3Options

class CookingMama3World(World):
    """Cooking Mama 3 is a 2009 Nintendo DS game where you prepare a variety of dishes with help from Mama."""
    game = "Cooking Mama 3"

    options_dataclass = CookingMama3Options
    options: CookingMama3Options  # type: ignore

    location_name_to_id = locations.location_name_to_id
    item_name_to_id = items.item_name_to_id
    location_name_groups = locations.location_name_groups
    item_name_groups = items.item_name_groups

    origin_region_name = "Top Menu"

    def create_regions(self) -> None:
        create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.CookingMama3Item:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "goal_option", "number_recipes_for_goal", "gold_medals_sources", "number_gold_medals", "number_cook_for_friends", "excluded_medal_checks","number_special_items", "progressive_recipe_scores", "timer_buffs"
        )


