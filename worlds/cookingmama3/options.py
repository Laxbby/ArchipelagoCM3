from __future__ import annotations

from dataclasses import dataclass

from Options import Choice, OptionSet, PerGameCommonOptions, Range, DefaultOnToggle

class GoalOption(OptionSet):
    """
    The goal condition(s) for the game. You may specify multiple, which requires all of them to be met.
    unlocked_recipes: obtain a certain number of recipes from the multiworld. They don't need to be attempted, just obtained
    gold_medals: get a specified number of gold medals on the game's recipes
    cook_for_friend: complete a meal for a specified number of friends in the Let's Cook mode
    special_items: obtain the specified special items (these are the Gardening Mama-exclusive items)
    """
    display_name = "Goal Options"
    default = frozenset({"unlocked_recipes", "gold_medals"})
    valid_keys = frozenset({"unlocked_recipes", "gold_medals", "cook_for_friend", "special_items"})


class NumberRecipesForGoal(Range):
    """
    If a certain number of recipes are required for goal, then this is the amount that is required. There are 81 recipes in the game, including the "Let's Cook" flags for the secret "Let's Match" recipes, and including one unused, but fully functional recipe that has been restored in this randomizer.
    this option does nothing if recipes are not required for goal.
    """
    display_name = "Required Unlocked Recipes"
    range_start = 1
    range_end = 81
    default = 30
    
class GoldMedalsSources(Choice):
    """
    If gold medals are required for goal, then this specifies the minimum difficulty at which medals will count for goal.
    Each recipe contributes, at most, one medal to the goal count, regardless of how many modes it's been completed in.
    this option does nothing if gold medals are not required for goal.
    cook_with_mama: the game's normal "free play" mode; the top-left option in the top menu
    lets_cook: the game's "challenge" mode, accessible by selecting a friend in the "Let's Cook" mode (top-center option) and then pressing "Make". In this mode, you are not given instructions between minigames, and some minigames will lose their guide marks.
    platter_mode: the game's "super challenge" mode, accessible by selecting a friend in the "Let's Cook" section and then pressing on the platter icon at the bottom. Similar to previous, but if you get anything but a "Very Well Done" (aka a gold medal, "even better than mama", etc) on a minigame, you automatically lose the dish. succeeding rewards you with a smiley face on that dish
    """
    display_name = "Minimum Gold Medal Difficulty"
    option_cook_with_mama = 0
    option_lets_cook = 1
    option_platter_mode = 2

    default = 0

class NumberGoldMedals(Range):
    """
    If gold medals are required for goal, then this is the amount that is required. There are 81 recipes in the game, including the secret recipes in the "Let's Match" mode, as well as one unused, but fully functional recipe that has been restored in this randomizer.
    this option does nothing if gold medals are not required for goal.
    """
    display_name = "Required Gold Medals"
    range_start = 1
    range_end = 81
    default = 10

class NumberCookForFriends(Range):
    """
    If cooking for friends is required for goal, then this is the number that is required.
    It doesn't matter whether you cook for them using the "Make" mode or the "Platter" mode, or whether you even get a gold medal; as long as you have successfully finished any meal for them, it counts
    It also doesn't matter which friends you cook for. there are 8 total.
    this option does nothing if feeding friends is not required for goal.
    """
    display_name = "Required Friends to Feed"
    range_start = 1
    range_end = 8
    default = 4

class NumberSpecialItems(Range):
    """
    If special items are required for goal, then this is the number that is required.
    These are items obtained exclusively from connecting to a copy of Gardening Mama in the regular game. They are obtained from the multiworld here.
    there are 4 total. It doesn't matter which ones you get.
    this option does nothing if special items are not required for goal.
    """
    display_name = "Required Special Items"
    range_start = 1
    range_end = 4
    default = 2

class NumberOfRecipes(Range):
    """
    The main focus of this game, and indeed the randomizer, are the recipes. Each recipe gives several checks, and must be obtained from the multiworld before they can be prepared.
    There are 66 recipes in the game, not including the secret "Let's Match" recipes which are handled differently, and including an unused, near-final and fully-functional recipe that has been re-enabled for this randomizer.
    This option determines how many of these recipes you will start with. A larger number means more sphere 1 checks, and potentially a faster goal, if Unlocked Recipes and Gold Medals are required.
    Your starting and unlocked recipes are always random.
    Unfortunately, the game freezes if 0 recipes are unlocked, so at least 1 must be unlocked from the start for now.
    """
    display_name = "Number of Starting Recipes"
    range_start = 1
    range_end = 66
    default = 1

class NumberOfFriends(Range):
    """
    The Friends give checks when you cook for them for the first time, and are a potential goal option.
    There are 8 friends in the game.
    This option determines how many friends you will start with. A larger number means more sphere 1 checks, and potentially a faster goal, if Cooking for Friends is required.
    Your starting and unlocked friends are always random.
    Unfortunately, unlike in real life, the game freezes if 0 friends are unlocked, so at least 1 must be unlocked from the start for now.
    """
    display_name = "Number of Starting Friends"
    range_start = 1
    range_end = 8
    default = 1

class ExcludedMedalChecks(OptionSet):
    """
    You are awarded medals for achieving certain score milestones on a dish. This option allows you to remove the checks for medals in some modes, in-case you know you do not want to be pressured to do them all.
    For now, individual recipes can't be excluded here, so just use "excluded_locations" at the bottom of the file.
    Each of these will remove 81 checks from the pool. Be careful with removing large amounts of checks.
    At least one medal type MUST be included or generation will fail.
    Note that this is NOT exclusive with the goal option. If you have "gold_medals" listed as a goal option, you will have to get some gold medals to goal, even if they don't send out checks!
    gold_medal_cook_with_mama: This is a perfect score on a dish in "Cook With Mama" mode.
    gold_medal_lets_cook: This is a perfect score on a dish in the "Let's Cook" Make mode. You aren't given instructions for the minigames in this mode, and some of the guide lines will be missing, so it is slightly harder than the previous mode.
    silver_medal_cook_with_mama: A silver medal is a score of 73-99.
    silver_medal_lets_cook: A silver medal is a score of 73-99.
    bronze_medal_cook_with_mama: A bronze medal is a score of 50-72.
    bronze_medal_lets_cook: A bronze medal is a score of 50-72.    
    smiley_face: this is a successful attempt on the "Let's Cook" Platter mode. Platter mode requires a perfect score or you'll automatically fail the entire dish.
    """
    display_name = "Excluded Medal Checks"
    default = frozenset({"smiley_face", "gold_medal_lets_cook", "gold_medal_cook_with_mama"})
    valid_keys = frozenset({"gold_medal_cook_with_mama", "gold_medal_lets_cook", "silver_medal_cook_with_mama", "silver_medal_lets_cook", "bronze_medal_cook_with_mama", "bronze_medal_lets_cook", "smiley_face"})


class ProgressiveRecipeScores(DefaultOnToggle):
    """
    If this option is enabled, then getting a score in a more challenging mode will also copy this score to the previous mode scores.
    The order is Cook With Mama < Let's Cook < Let's Cook Platter Mode. Completing a dish in one mode will apply the score to any mode to the left.
    This can help with game pacing, as you can get more checks by just completing a dish once, instead of having to do it twice or even thrice.
    """
    display_name = "Progressive Recipe Scores"


class NumberOfIngredients(Range):
    """
    The top right option in the top menu is the "Let's Match" mode. This is where you unlock special secret recipes that do not show up in the "Cooking with Mama" mode, and must be discovered before they can be played in the "Let's Cook" mode.
    You unlock these recipes by matching 2 out of the 6 ingredients with each other. In this randomizer, these ingredients are scattered in the multiworld and must be found before you can cook any of their respective secret recipes with them.
    Once attempted, they will appear in Let's Cook mode and counts towards your Number Of Recipes for goal.
    This option allows you to select how many ingredients you have at the start. 0 means you must find them all and cannot use the Let's Match mode at first, while 6 means they are all available from the start and all of them can be prepared immediately.
    There are 15 secret recipes total.
    """
    display_name = "Number of Starting Ingredients"
    range_start = 0
    range_end = 6
    default = 0

class EnableShopModeChecks(Choice):
    """
    The center left option in the menu is the titular Shopping mode. It's most similar to a Frogger-style game, where you collect groceries while trying to avoid the other shoppers.
    There are 4 difficulties total, each with a different grocery store map, more difficult minigames, and more items to collect.
    In this randomizer, getting certain scores will send checks. Each game difficulty can send up to 3.
    selecting the Hard setting will force all three difficulty checks into the pool, while each difficulty below it removes one of the higher tiers of checks.
    The hard threshold is based on what I could reasonably accomplish on real hardware after a few tries, and the other difficulties were chosen based on that.
    If you don't want to deal with this at all, you can also just disable them entirely.
    """
    display_name = "Shopping Mode Checks"
    option_disable_entirely = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3

    default = 2

class NumberStartingShopGames(Range):
    """
    There are 4 shop difficulties in total, which are progressively unlocked with a "Progressive Shopping Minigame" check.
    This is the number of difficulties that are unlocked at the start of the randomizer. 0 means you cannot do any of them at the beginning. 4 means they're all unlocked from the start and 0 unlocks will be needed.
    """
    display_name = "Number of Starting Shop Difficulties"
    range_start = 0
    range_end = 4
    default = 0


class EnableCookingChallengeChecks(Choice):
    """
    The top menu has a button in the center called "Cooking Contest". These are basically time trial or time attack minigames, where you try to complete one kitchen task as many times as possible.
    In this randomizer, getting certain scores will send checks. Each challenge can send up to 3.
    selecting the Hard setting will force all three difficulty checks into the pool, while each difficulty below it removes one of the higher checks.
    The scores are wildly different based on the specific minigame, but I set the Hard threshold to be what I could reasonably accomplish on real hardware after a few tries, and the other difficulties were chosen based on that.
    If you don't want to deal with this at all, you can also just disable them entirely.
    easy mode is 20 checks total, medium is 40, hard is 60
    """
    display_name = "Cooking Contest Solo Challenge Checks"
    option_disable_entirely = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3

    default = 2

class NumberCookingChallengeGames(Range):
    """
    In total, there are 20 minigames. 4 of them are unlocked when obtaining the Special Items from Gardening Mama.
    The remaining 16 are unlocked 4-at-a-time, which are unlocked with a "Progressive Cooking Contest Challenge Page" Check.
    This is the number of pages that are unlocked at the start of the randomizer. 4 means that they're unlocked from the start and 0 unlocks will be needed.
    Note that this does not affect the previously-mentioned 4 special minigames, and those must ALWAYS be unlocked with the special Gardening Mama item and will be available as soon as they are.
    """
    display_name = "Number of Starting Cooking Contest Solo Challenge Pages"
    range_start = 0
    range_end = 4
    default = 0


class NumberBonusChecks(Range):
    """
    Completing a minigame for a dish quickly or well enough will land you a "Bonus!". Every 5 will unlock a bonus prize.
    In the randomizer, these have been turned into checks. This option allows you to specify how many bonuses will be turned into checks. Bonuses beyond this point will simply do nothing.
    Note that bonuses are obtainable in the multiworld and there are permanent bonus buffs available in the itempool, so obtaining these may not be as slow as in the vanilla game.
    """
    display_name = "Number of Bonus Checks"
    range_start = 1
    range_end = 100
    default = 50

class BonusBuffs(Range):
    """
    Every 5 Bonuses is a check.
    This option, if enabled, will place permanent bonuses into the pool
    If enabled, you will start with needing 5 bonuses per unlock, but when a "Progressive Bonus Counter" is obtained, you will need one less bonus per unlock.
    If disabled, you'll always need 5.
    """
    display_name = "Number of Permanent Bonuses"

    range_start = 0
    range_end = 4
    default = 4

class TimerBuffs(Range):
    """
    The timer can be modified to give you more time during minigames that use the clock on the top screen.
    This option, if enabled, will place permanent timer bonuses into the pool.
    If enabled, you will start with all minigame timers being 90% of their original length. Each bonus will add 10% back to the timer. More bonuses mean that more multipliers will be added to the pool, and therefore you will end up with a larger timer bonus.
    if disabled, the timer will never be touched and will always be at its vanilla value unless a trap is obtained.
    """
    display_name = "Number of Permanent Timer Increases"

    range_start = 0
    range_end = 6
    default = 2

class FillerComposition(Choice):
    """
    The in-game stickers and accessories exist as filler items. there are over 400 of these, so depending on how much filler exists, they can be condensed into sets. This is handled automatically, but if you would like to force the accessories to be condensed into packs, you may do so here.
    Condensing them will leave more room for random Extra Bonus checks, as well as traps, to be added to the pool.
    if disabled entirely, accessories will all be unlocked at the start and no accessory items will exist in the pool.
    collections are massive mass-unlocks of every accessory in a menu. This adds 3 items: a collection for Diary Stickers, Mama's Accessories, and Kitchen Appliances
    sets are smaller unlocks of accessories based on the item's category. This adds 57 items, including earring sets or emoji sticker sets, as examples.
    individual means that every individual (~400) accessory item is added right to the pool.
    note that, if not enough unfilled locations exist to satisfy the choice given here, it will be ignored and the next-smallest option will be selected.
    """
    display_name = "Condense Accessories into Packs"
    option_disable_entirely = 0
    option_collections = 1
    option_sets = 2
    option_individual = 3

    default = 3

class TrapWeight(Range):
    """
    Out of the remaining unfilled locations, this is the percentage that is converted into traps.
    There are 3 traps:
    Bad Fashion Trap: Mama's outfit and kitchen appliances are scrambled to random options. If you don't have the respective accessories unlocked, you may not be able to change it back for a while.
    Timer Trap: The next played minigame will have a small amount of time removed from the timer.
    Babel Trap: The game's language is set to Italian for some time. The translation in the US version is incomplete, so the names of recipes and recipe steps are scrambled.
    """
    display_name = "Trap Weight"

    range_start = 0
    range_end = 100
    default = 10




@dataclass
class CookingMama3Options(PerGameCommonOptions):

    goal_option: GoalOption
    number_recipes_for_goal: NumberRecipesForGoal
    gold_medals_sources: GoldMedalsSources
    number_gold_medals: NumberGoldMedals
    number_cook_for_friends: NumberCookForFriends
    number_special_items: NumberSpecialItems

    number_of_recipes: NumberOfRecipes
    number_of_friends: NumberOfFriends
    excluded_medal_checks: ExcludedMedalChecks
    progressive_recipe_scores: ProgressiveRecipeScores
    number_of_ingredients: NumberOfIngredients

    enable_shop_mode_checks: EnableShopModeChecks
    number_starting_shop_games: NumberStartingShopGames
    enable_cooking_challenge_checks: EnableCookingChallengeChecks
    number_cooking_challenge_games: NumberCookingChallengeGames
    number_bonus_checks: NumberBonusChecks

    bonus_buffs: BonusBuffs
    timer_buffs: TimerBuffs
    filler_composition: FillerComposition
    trap_weight: TrapWeight


