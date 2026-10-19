from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import  Location
from Options import OptionError

from .constants import (
    FRIENDS_BYTE, 
    RECIPE_BYTE,
    CHALLENGE_BYTE,
    SHOPPING_BYTE,
)

if TYPE_CHECKING:
    from .world import CookingMama3World

ID_COOK_FOR_FRIEND = 65000
ID_RECIPE_COOK_WITH_MAMA = 65008
ID_RECIPE_LETS_COOK = 65500
ID_COOKING_CONTEST_CHALLENGE = 66000
ID_SHOPPING_LOC = 66100
ID_BONUS_LOC = 66120

ALL_MEDAL_TYPES= {
    "gold_medal_cook_with_mama", 
    "gold_medal_lets_cook", 
    "silver_medal_cook_with_mama", 
    "silver_medal_lets_cook", 
    "bronze_medal_cook_with_mama", 
    "bronze_medal_lets_cook", 
    "smiley_face"}

MEDAL = [
    "Gold Medal",
    "Silver Medal",
    "Bronze Medal"
]

LETS_COOK_MEDAL = [
    "Gold Medal",
    "Silver Medal",
    "Bronze Medal",
    "Smiley Face"
]

THRESHOLD = [
    "Easy Score Target",
    "Medium Score Target",
    "Hard Score Target"
]

MEDAL_DIFFICULTY = [
    "Cook With Mama",
    "Let's Cook Make Mode",
    "Let's Cook Platter Mode"
]
RECIPE_TYPE = [
    "Cook With Mama", 
    "Let's Match"
    ]


cook_for_friends_locs = {
    f"Cook for {name}":
        ID_COOK_FOR_FRIEND + index
    for index, name in enumerate(FRIENDS_BYTE)
}

cook_with_mama_locs = {
    f"{RECIPE_TYPE[i]}: {name} - {medal}":
        ID_RECIPE_COOK_WITH_MAMA + index
    for index, (name, medal, i) in enumerate(
        (name, medal, 0 if RECIPE_BYTE[name] == 0 else 1)
        for name in RECIPE_BYTE
        for medal in MEDAL
    )
}

lets_cook_locs = {
    f"Let's Cook: {name} - {medal}":
        ID_RECIPE_LETS_COOK + index
    for index, (name, medal) in enumerate((name, medal)
        for name in RECIPE_BYTE
        for medal in LETS_COOK_MEDAL
    )
}

cooking_contest_locs = {
    f"Cooking Contest: \"{name}\" {threshold}":
        ID_COOKING_CONTEST_CHALLENGE + index
    for index, (name, threshold) in enumerate((name, threshold)
        for name in CHALLENGE_BYTE
        for threshold in THRESHOLD
    )
}

shopping_locs = {
    f"Shopping: {name} - {threshold}":
        ID_SHOPPING_LOC + index
    for index, (name, threshold) in enumerate((name, threshold)
        for name in SHOPPING_BYTE
        for threshold in THRESHOLD
    )
}

BONUS_THRESHOLDS = tuple(range(1, 101))

bonus_locs = {
    f"Complete Bonus {threshold}":
        ID_BONUS_LOC + index
    for index, threshold in enumerate(BONUS_THRESHOLDS)
}

location_name_to_id = {

    **cook_for_friends_locs,
    **cook_with_mama_locs,
    **lets_cook_locs,
    **cooking_contest_locs,
    **shopping_locs,
    **bonus_locs
}

location_id_to_name = {
    location_id: name
    for name, location_id in location_name_to_id.items()
}

location_name_groups = {
    "Cook For Friends": {item for item in cook_for_friends_locs},
    "Cook With Mama Bronze Medals": {item for item in cook_with_mama_locs if "Bronze Medal" in item},
    "Cook With Mama Silver Medals": {item for item in cook_with_mama_locs if "Silver Medal" in item},
    "Cook With Mama Gold Medals": {item for item in cook_with_mama_locs if "Gold Medal" in item},
    "Let's Cook Bronze Medals": {item for item in lets_cook_locs if "Bronze Medal" in item},
    "Let's Cook Silver Medals": {item for item in lets_cook_locs if "Silver Medal" in item},
    "Let's Cook Gold Medals": {item for item in lets_cook_locs if "Gold Medal" in item},
    "Let's Cook Smiley Faces": {item for item in lets_cook_locs if "Smiley Face" in item},
    "Cooking Contest Easy Score Thresholds": {item for item in shopping_locs if "Easy" in item},
    "Cooking Contest Medium Score Thresholds": {item for item in shopping_locs if "Medium" in item},
    "Cooking Contest Hard Score Thresholds": {item for item in shopping_locs if "Hard" in item},
    "Shopping Mode Easy Score Thresholds": {item for item in shopping_locs if "Easy" in item},
    "Shopping Mode Medium Score Thresholds": {item for item in shopping_locs if "Medium" in item},
    "Shopping Mode Hard Score Thresholds": {item for item in shopping_locs if "Hard" in item},
    "Bonus Rewards": {item for item in bonus_locs}
}

class CookingMama3Location(Location):
    game = "Cooking Mama 3"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: location_name_to_id[location_name] for location_name in location_names}

def create_all_locations(world: CookingMama3World)-> None:
    hub = world.get_region("Top Menu")

    excluded_medals = world.options.excluded_medal_checks
    chosen_medals = ALL_MEDAL_TYPES.difference(excluded_medals)
    if len(chosen_medals) == 0:
        #this technically *does* generate, but i do not wanna deal with testing this, man. 
        ##hey fred! gimme a cooking mama ap. hold the cooking minigames!
        ##hold the cooking minigames??? hey jimmy! gimme a cooking mama with nothin!
        ##*nothin*????????
        raise OptionError(f"Cooking Mama 3: {world.player_name} excluded all recipe medals! Please make sure to include at least one category of medals as checks!")
    
    if "bronze_medal_cook_with_mama" in chosen_medals:
        bronze_medal_cook_with_mama_locs = [
        name for name in location_name_to_id
        if  (name.startswith("Cook With Mama: ") or name.startswith("Let's Match: ")) and name.endswith("Bronze Medal")
        ]
        hub.add_locations(get_location_names_with_ids(bronze_medal_cook_with_mama_locs), CookingMama3Location)
    if "silver_medal_cook_with_mama" in chosen_medals:
        silver_medal_cook_with_mama_locs = [
        name for name in location_name_to_id
        if  (name.startswith("Cook With Mama: ") or name.startswith("Let's Match: ")) and name.endswith("Silver Medal")
        ]
        hub.add_locations(get_location_names_with_ids(silver_medal_cook_with_mama_locs), CookingMama3Location)
    if "gold_medal_cook_with_mama" in chosen_medals:
        gold_medal_cook_with_mama_locs = [
        name for name in location_name_to_id
        if  (name.startswith("Cook With Mama: ") or name.startswith("Let's Match: ")) and name.endswith("Gold Medal")
        ]
        hub.add_locations(get_location_names_with_ids(gold_medal_cook_with_mama_locs), CookingMama3Location)

    if "bronze_medal_lets_cook" in chosen_medals:
        bronze_medal_lets_cook_locs = [
        name for name in location_name_to_id
        if  name.startswith("Let's Cook: ") and name.endswith("Bronze Medal")
        ]
        hub.add_locations(get_location_names_with_ids(bronze_medal_lets_cook_locs), CookingMama3Location)
    if "silver_medal_lets_cook" in chosen_medals:
        silver_medal_lets_cook_locs = [
        name for name in location_name_to_id
        if  name.startswith("Let's Cook: ") and name.endswith("Silver Medal")
        ]
        hub.add_locations(get_location_names_with_ids(silver_medal_lets_cook_locs), CookingMama3Location)
    if "gold_medal_lets_cook" in chosen_medals:
        gold_medal_lets_cook_locs = [
        name for name in location_name_to_id
        if  name.startswith("Let's Cook: ") and name.endswith("Gold Medal")
        ]
        hub.add_locations(get_location_names_with_ids(gold_medal_lets_cook_locs), CookingMama3Location)
    if "smiley_face" in chosen_medals:
        smiley_face_lets_cook_locs = [
        name for name in location_name_to_id
        if  name.startswith("Let's Cook: ") and name.endswith("Smiley Face")
        ]
        hub.add_locations(get_location_names_with_ids(smiley_face_lets_cook_locs), CookingMama3Location)


    cook_for_friends_locs = [
        name for name in location_name_to_id
        if  name.startswith("Cook for ")
        ]
    hub.add_locations(get_location_names_with_ids(cook_for_friends_locs), CookingMama3Location)


    cooking_challenge_locs = []
    for ix in range (0, world.options.enable_cooking_challenge_checks):
        threshold = THRESHOLD[ix]
        cooking_challenge_locs += [
            name for name in location_name_to_id
            if  name.startswith("Cooking Contest: ") and name.endswith(threshold)
        ]
    hub.add_locations(get_location_names_with_ids(cooking_challenge_locs), CookingMama3Location)


    lets_shop_locs = []
    for ix in range (0, world.options.enable_shop_mode_checks):
        threshold = THRESHOLD[ix]
        lets_shop_locs += [
            name for name in location_name_to_id
            if  name.startswith("Shopping: ") and name.endswith(threshold)
            ]
    hub.add_locations(get_location_names_with_ids(lets_shop_locs), CookingMama3Location)

    bonuses_locs = []
    for ix in range (0, world.options.number_bonus_checks):
        bonuses_locs += [
            name for name in location_name_to_id
            if  name == (f"Complete Bonus {str(ix + 1)}")
            ]
    hub.add_locations(get_location_names_with_ids(bonuses_locs), CookingMama3Location)



