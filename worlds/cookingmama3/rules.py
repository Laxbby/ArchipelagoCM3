from __future__ import annotations

from typing import TYPE_CHECKING

from Options import OptionError
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from .world import CookingMama3World

from .constants import (
    SPECIAL_ITEMS_BYTE, 
    FRIENDS_BYTE, 
    RECIPE_BYTE,
    INGREDIENTS_BYTE,
    CHALLENGE_BYTE,
    SHOPPING_BYTE
)

from .locations import (
MEDAL,
LETS_COOK_MEDAL,
THRESHOLD
)


def set_all_rules(world: CookingMama3World) -> None:
    
    set_recipe_rules(world)
    set_friend_rules(world)
    set_challenge_rules(world)
    set_shopping_rules(world)
    set_bonus_rules(world)
    set_goal(world)

def set_recipe_rules(world: "CookingMama3World") -> None:
        
    #most recipes require just the recipe unlock
    for id, key in enumerate(RECIPE_BYTE):
            for medal in MEDAL:
                #convert the medal in the MEDAL list into a form that can be compared with the options
                medaloption = medal.lower()
                medaloption = medaloption.replace(" ", "_") + "_cook_with_mama"

                if medaloption not in world.options.excluded_medal_checks:
                    #secret recipes are called "Let's Match" checks
                    if RECIPE_BYTE[key] > 0:
                        recipe_loc = world.multiworld.get_location(
                        f"Let's Match: {key} - {medal}",
                            world.player,
                        )
                    else:
                        recipe_loc = world.multiworld.get_location(
                        f"Cook With Mama: {key} - {medal}",
                            world.player,
                        )
                    #if this is a secret recipe, its value in the dict is greater than 0. compare it with the ingredients list to determine which ingredients it needs
                    if RECIPE_BYTE[key] > 0:
                        ingredients = []
                        for id, key2 in enumerate(INGREDIENTS_BYTE):
                            #ingredients that have nothing to do with recipes wont have lined-up bits, so theyll be ignored. if they are involved, there will be just one bit that remains after ANDing them
                            if RECIPE_BYTE[key] & INGREDIENTS_BYTE[key2] > 0:
                                ingredients.append(key2)
                        set_rule(recipe_loc, lambda state, required_ingredients=ingredients: state.has_all(required_ingredients, world.player))
                    #if this is a nonsecret recipe, it just needs its recipe unlock
                    else:
                        recipe_item = f"{key} (Recipe Unlock)"  
                        set_rule(recipe_loc,lambda state, item=recipe_item: state.has(item, world.player))
                     
            for medal in LETS_COOK_MEDAL:
                medaloption = medal.lower()
                medaloption = medaloption.replace(" ", "_")
                if medaloption != "smiley_face": 
                    medaloption = medaloption + "_lets_cook"

                if medaloption not in world.options.excluded_medal_checks:
                    recipe_loc = world.multiworld.get_location(
                    f"Let's Cook: {key} - {medal}",
                        world.player,
                    )
                    #if this is a secret recipe, its value in the dict is greater than 0. compare it with the ingredients list to determine which ingredients it needs
                    if RECIPE_BYTE[key] > 0:
                        required_items = []
                        for id, key2 in enumerate(INGREDIENTS_BYTE):
                            #ingredients that have nothing to do with recipes wont have lined-up bits, so theyll be ignored. if they are involved, there will be just one bit that remains after ANDing them
                            if RECIPE_BYTE[key] & INGREDIENTS_BYTE[key2] > 0:
                                required_items.append(key2)
                        set_rule(recipe_loc, lambda state, required_items=required_items: state.has_all(required_items, world.player))
                    #if this is a nonsecret recipe, it just needs its recipe unlock
                    else:
                        recipe_item = f"{key} (Recipe Unlock)"  
                        set_rule(recipe_loc, lambda state, item=recipe_item: state.has(item, world.player)
)



def set_friend_rules(world: "CookingMama3World") -> None:
     for friend in FRIENDS_BYTE:
          friend_loc = world.multiworld.get_location(
                                f"Cook for {friend}",
                                world.player,
                              )
          friend_item = f"{friend} (Friend Unlock)"
          set_rule(friend_loc, lambda state, item=friend_item: state.has(item, world.player))


def set_challenge_rules(world: "CookingMama3World") -> None:
    for i, key in enumerate(CHALLENGE_BYTE):
        challenge_loc = None
        for x in range(0, world.options.enable_cooking_challenge_checks):
            threshold = THRESHOLD[x]
            challenge_loc = world.multiworld.get_location(
                                f"Cooking Contest: \"{key}\" {threshold}",
                                world.player,
                              )
            if challenge_loc != None:
                if i >= 16:
                    #4th page only requires the special items
                    for item in SPECIAL_ITEMS_BYTE:
                        if CHALLENGE_BYTE[key][3] == SPECIAL_ITEMS_BYTE[item]:
                            set_rule(challenge_loc, lambda state, item=item: state.has(item, world.player))
                            
                else:
                    required_count = int(i / 4) + 1
                    set_rule(challenge_loc, lambda state, count=required_count: state.has("Progressive Cooking Contest Challenge Page", world.player, count=count))

                    

def set_shopping_rules(world: "CookingMama3World") -> None:
     for ix, shop in enumerate(SHOPPING_BYTE):
          shopping_loc = None
          for x in range(0, world.options.enable_shop_mode_checks):
            threshold = THRESHOLD[x]
            shopping_loc = world.multiworld.get_location(
                                f"Shopping: {shop} - {threshold}",
                                world.player,
                              )
            if shopping_loc != None:
                required_count = ix + 1
                set_rule(shopping_loc, lambda state, count=required_count: state.has("Progressive Shopping Minigame", world.player, count=count))

def set_bonus_rules(world: "CookingMama3World") -> None:
    for x in range(1, world.options.number_bonus_checks + 1):
        bonus_loc = world.multiworld.get_location(
                                f"Complete Bonus {x}",
                                world.player,
                              )
        set_rule(bonus_loc, lambda state, count=x: state.has_group("Recipes", world.player, count=min(count, 65)))

        #for now, simple bonus logic
        #the logic just directly, 1:1 maps bonuses to recipes. it's capped at about 65 to avoid logic issues. 
        #since you could technically get all bonuses with just one recipe, and recipes have varying amounts of easy bonuses to obtain, this is supposed to be a healthy compromise. in testing, it seems that this lets you keep up pretty well while only needing to repeat a recipe once or twice per run, if at all

def set_goal(world: CookingMama3World) -> None:
    goals = world.options.goal_option

    recipes_number = 0
    gold_medal_number = 0
    friend_number = 0
    special_items = 0
    if "unlocked_recipes" in goals:
        recipes_number = world.options.number_recipes_for_goal
    if "gold_medals" in goals:
        gold_medal_number = world.options.number_gold_medals
    if "cook_for_friend" in goals:
            friend_number = world.options.number_cook_for_friends
    if "special_items" in goals:
            special_items = world.options.number_special_items 
    
    if len(set(goals)) == 0:
        raise OptionError(f"Cooking Mama 3: {world.player_name} has no goal conditions!")
    
    if recipes_number <= world.options.number_of_recipes and (recipes_number > 0) and (gold_medal_number + friend_number + special_items == 0):
        #if this is the only goal condition, this can lead to literally instantly goaling
        ##this may be a bit "no fun allowed" but instant goaling seems like it should be avoided
        raise OptionError(f"Cooking Mama 3: {world.player_name} has enough starting recipes to fulfill the goal requirement. This may lead to instant goaling! Please make sure {world.player_name}'s starting recipes is less than the required recipes for goal!")
    

    world.multiworld.completion_condition[world.player] = lambda state: state.has_group("Recipes", world.player, count=max(int(gold_medal_number), int(recipes_number))) and \
                                                                        state.has_group("Friends", world.player, count=int(friend_number)) and \
                                                                        state.has_group("Special Items", world.player, count=int(special_items))
