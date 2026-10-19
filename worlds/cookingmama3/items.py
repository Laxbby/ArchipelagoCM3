from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import CookingMama3World

from .constants import (
    SPECIAL_ITEMS_BYTE,
    FRIENDS_BYTE,
    RECIPE_BYTE,
    INGREDIENTS_BYTE,
    STICKER_FULL,
    ACCESSORY_FULL,
    KITCHEN_FULL,
    ALL_STICKER,
    ALL_CLOTHING,
)

ItemData = dict[str, Any]

ID_SPECIAL_ITEMS = 70000
ID_COLLECTIONS = 70004
ID_SETS = 70007
ID_INDIVIDUAL = 70107
ID_FRIEND = 700600
ID_RECIPE = 700608
ID_INGREDIENT = 700700
ID_CHALLENGE = 700706
ID_SHOPPING = 700707
ID_TIMER = 700708
ID_BONUS = 700709
ID_FILLER = 700710
ID_TRAP = 700720


COLLECTION = [
    "Sticker Collection",
    "Clothing Collection",
    "Kitchen Collection"
]

SETS = [
    name
    for collection in (
        STICKER_FULL,
        ACCESSORY_FULL,
        KITCHEN_FULL,
    )
    for name in collection
]

INDIVIDUAL = [
    name
    for collection in (
        STICKER_FULL,
        ACCESSORY_FULL,
        KITCHEN_FULL,
    )
    for subset in collection.values()
    for name in subset
]

TYPES = [
    "Sticker", "Clothing", "Kitchenware"
    ]

###cooking contest challenges###
CHALLENGE = [
    "Progressive Cooking Contest Challenge Page",
]

###shopping###
SHOPPING = [
    "Progressive Shopping Minigame",
]

###misc###
TIMER = [
    "Progressive Minigame Timer",
]

BONUS = [
    "Progressive Bonus Counter",
]

FILLER = [
    "Extra Bonus",
]

TRAP = [
    "Bad Fashion Trap",
    "Less Time Trap",
    "Babel Trap",
]


item_table: dict[str, ItemData] = {
    **{
        name: {
            "id": ID_SPECIAL_ITEMS + index,
            "classification": ItemClassification.progression,
            "category": "Special Items",
        }
        for index, name in enumerate(SPECIAL_ITEMS_BYTE)
    },
    **{
        name: {
            "id": ID_COLLECTIONS + index,
            "classification": ItemClassification.filler,
            "category": "Accessory Collections",
        }
        for index, name in enumerate(COLLECTION)
    },
    **{
        name: {
            "id": ID_SETS + index,
            "classification": ItemClassification.filler,
            "category": "Accessory Sets",
        }
        for index, name in enumerate(SETS)
    }, 
    
    **{
        f"{name} ({TYPES[i]})": {
            "id": ID_INDIVIDUAL + index,
            "classification": ItemClassification.filler,
            "category": "Accessories",
        }
        for index, name in enumerate(INDIVIDUAL)
        for i in (
            0 if name in ALL_STICKER
            else 1 if name in ALL_CLOTHING
            else 2,
        )
    },
    **{
        f"{name} (Friend Unlock)": {
            "id": ID_FRIEND + index,
            "classification": ItemClassification.progression,
            "category": "Friends",
        }
        for index, name in enumerate(FRIENDS_BYTE)
    }, 
    **{
        f"{name} (Recipe Unlock)": {
            "id": ID_RECIPE + index,
            "classification": ItemClassification.progression,
            "category": f"Recipes",
        }
        for index, name in enumerate(RECIPE_BYTE)
        if RECIPE_BYTE[name] == 0
    }, 
    **{
        name: {
            "id": ID_INGREDIENT + index,
            "classification": ItemClassification.progression,
            "category": "Ingredients",
        }
        for index, name in enumerate(INGREDIENTS_BYTE)
    }, 
    **{
        name: {
            "id": ID_CHALLENGE  + index,
            "classification": ItemClassification.progression,
            "category": "Cooking Contests",
        }
        for index, name in enumerate(CHALLENGE)
    }, 
    **{
        name: {
            "id": ID_SHOPPING + index,
            "classification": ItemClassification.progression,
            "category": "Shopping",
        }
        for index, name in enumerate(SHOPPING)
    }, 
    **{
        name: {
            "id": ID_TIMER + index,
            "classification": ItemClassification.useful,
            "category": "Timer Buff",
        }
        for index, name in enumerate(TIMER)
    }, 
    **{
        name: {
            "id": ID_BONUS + index,
            "classification": ItemClassification.useful,
            "category": "Bonus Buff",
        }
        for index, name in enumerate(BONUS)
    }, 
    **{
        name: {
            "id": ID_FILLER + index,
            "classification": ItemClassification.filler,
            "category": "Filler",
        }
        for index, name in enumerate(FILLER)
    }, 
    **{
        name: {
            "id": ID_TRAP + index,
            "classification": ItemClassification.trap,
            "category": "Traps",
        }
        for index, name in enumerate(TRAP)
    }, 
}

item_name_groups = {
    "Special Items": {item for item, data in item_table.items() if data["category"] == "Special Items"},
    "Accessory Collections": {item for item, data in item_table.items() if data["category"] == "Accessory Collections"},
    "Accessory Sets": {item for item, data in item_table.items() if data["category"] == "Accessory Sets"},
    "Accessories": {item for item, data in item_table.items() if data["category"] == "Accessories"},
    "Friends": {item for item, data in item_table.items() if data["category"] == "Friends"},
    "Recipes": {item for item, data in item_table.items() if data["category"] == "Recipes"},
    "Ingredients": {item for item, data in item_table.items() if data["category"] == "Ingredients"},
    "Cooking Contests": {item for item, data in item_table.items() if data["category"] == "Cooking Contests"},
    "Shopping": {item for item, data in item_table.items() if data["category"] == "Shopping"},
    "Timer Buff": {item for item, data in item_table.items() if data["category"] == "Timer Buff"},
    "Bonus Buff": {item for item, data in item_table.items() if data["category"] == "Bonus Buff"},
    "Filler": {item for item, data in item_table.items() if data["category"] == "Filler"},
    "Traps": {item for item, data in item_table.items() if data["category"] == "Traps"},
}

class CookingMama3Item(Item):
    game = "Cooking Mama 3"

def create_item_with_correct_classification(world: CookingMama3World, name: str, make_prog: bool = False) -> CookingMama3Item:
    item = item_table[name]

    return CookingMama3Item(name, item["classification"], item["id"], world.player)

def add_items(entries, ap_id_base: int, classification: ItemClassification, category: str) -> None:
    for index, name in enumerate(entries):
        item_table[name] = {
            "id": ap_id_base + index,
            "classification": classification,
            "category": category,
        }

def create_all_items(world: CookingMama3World):

    itempool: list[Item] = []
    guaranteed_items = [
        name for name, item in item_table.items()
        if item["category"] in ("Special Items")
    ]
    for i in guaranteed_items:
        itempool.append(world.create_item(f"{i}"))

    recipe_items = [
        name for name, item in item_table.items()
        if item["category"] == "Recipes"
    ]
    for i in range(0, world.options.number_of_recipes):
        starting_recipe = world.random.choice(recipe_items)
        world.push_precollected(world.create_item(f"{starting_recipe}"))
        recipe_items.remove(starting_recipe)
    for i in recipe_items:
        itempool.append(world.create_item(f"{i}"))

    friends_items = [
        name for name, item in item_table.items()
        if item["category"] == "Friends"
    ]
    for i in range(0, world.options.number_of_friends):
        starting_friend = world.random.choice(friends_items)
        world.push_precollected(world.create_item(f"{starting_friend}"))
        friends_items.remove(starting_friend)
    for i in friends_items:
        itempool.append(world.create_item(f"{i}"))

    ingredients_items = [
        name for name, item in item_table.items()
        if item["category"] == "Ingredients"
    ]
    for i in range(0, world.options.number_of_ingredients):
        starting_ingredient= world.random.choice(ingredients_items)
        world.push_precollected(world.create_item(f"{starting_ingredient}"))
        ingredients_items.remove(starting_ingredient)
    for i in ingredients_items:
        itempool.append(world.create_item(f"{i}"))

    if world.options.enable_cooking_challenge_checks > 0:
        for i in range(0, world.options.number_cooking_challenge_games):
            world.push_precollected(world.create_item(f"Progressive Cooking Contest Challenge Page"))
        for i in range(0, 4 - world.options.number_cooking_challenge_games):
            itempool.append(world.create_item(f"Progressive Cooking Contest Challenge Page"))

    if world.options.enable_shop_mode_checks > 0:
        for i in range(0, world.options.number_starting_shop_games):
            world.push_precollected(world.create_item(f"Progressive Shopping Minigame"))
        for i in range(0, 4 - world.options.number_starting_shop_games):
            itempool.append(world.create_item(f"Progressive Shopping Minigame"))

    for i in range(0, world.options.timer_buffs):
        itempool.append(world.create_item(f"Progressive Minigame Timer"))

    for i in range(0, world.options.bonus_buffs):
        itempool.append(world.create_item(f"Progressive Bonus Counter"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    accessories_items = []
    if needed_number_of_filler_items < len(COLLECTION) or world.options.filler_composition == 0:
        print(f"Cooking Mama 3: {world.player_name}'s world will include all accessories from the start")
        for i in COLLECTION:
            world.push_precollected(world.create_item(f"{i}"))
    elif needed_number_of_filler_items < len(SETS) or world.options.filler_composition == 1:
        print(f"Cooking Mama 3: {world.player_name}'s world will pack accessories into collections")
        accessories_items = [
            name for name, item in item_table.items()
            if item["category"] == "Accessory Collections"
        ]
    elif needed_number_of_filler_items < len(INDIVIDUAL) or world.options.filler_composition == 2:
        print(f"Cooking Mama 3: {world.player_name}'s world will pack accessories into sets")
        accessories_items = [
            name for name, item in item_table.items()
            if item["category"] == "Accessory Sets"
        ]
    else:
        print(f"Cooking Mama 3: {world.player_name}'s world will include individual accessory items")
        accessories_items = [
            name for name, item in item_table.items()
            if item["category"] == "Accessories"
        ]
        #these are bits that enable the, uh, ability to remove accessories. the plan was to include them as items because i thought it was funny, but it felt too awkward (if you unlocked an accessory and put it on and didnt have this unlocked, you *couldnt take it back off*) so im just gonna unlock these particular bits from the start
        #since i already had them coded as items, its easier to just push them as precollected, rather than have the client code set their bits
        world.push_precollected(world.create_item(f"Empty Frame (Sticker)"))
        world.push_precollected(world.create_item(f"No Glasses (Clothing)"))
        world.push_precollected(world.create_item(f"No Earrings (Clothing)"))
        world.push_precollected(world.create_item(f"No Hat (Clothing)"))
        world.push_precollected(world.create_item(f"No Headgear (Clothing)"))
        #weirdly, for the gauge (and perhaps clock?) customizations, one wallpaper must be unlocked to access them. bit bummed about this, but ill just unlock this one background from the start for now
        world.push_precollected(world.create_item(f"Blue Tiles Wallpaper (Kitchenware)"))
        
        accessories_items.remove("Empty Frame (Sticker)")
        accessories_items.remove("No Glasses (Clothing)")
        accessories_items.remove("No Earrings (Clothing)")
        accessories_items.remove("No Hat (Clothing)")
        accessories_items.remove("No Headgear (Clothing)")
        accessories_items.remove("Blue Tiles Wallpaper (Kitchenware)")
        
    for i in accessories_items:
        itempool.append(world.create_item(f"{i}"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    needed_number_of_traps = int(needed_number_of_filler_items*(world.options.trap_weight/100))
    needed_number_of_filler_items -= needed_number_of_traps
    itempool += [world.create_item(world.random.choice(TRAP)) for _ in range(needed_number_of_traps)]
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool



item_name_to_id = {
    name: data["id"]
    for name, data in item_table.items()
}

item_id_to_name = {
    data["id"]: name
    for name, data in item_table.items()
}


def get_random_filler_item_name(world: CookingMama3World) -> str:
        return world.random.choice(FILLER)
