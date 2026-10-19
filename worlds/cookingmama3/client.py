import logging
import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING, Sequence
import asyncio
from random import Random

from .locations import (
ALL_MEDAL_TYPES,
MEDAL_DIFFICULTY,
ID_COOK_FOR_FRIEND,
ID_RECIPE_COOK_WITH_MAMA,
ID_RECIPE_LETS_COOK,
ID_COOKING_CONTEST_CHALLENGE,
ID_SHOPPING_LOC,
ID_BONUS_LOC,
)

from .items import(
ID_SPECIAL_ITEMS,
ID_COLLECTIONS,
ID_SETS,
ID_INDIVIDUAL,
ID_FRIEND,
ID_RECIPE,
ID_INGREDIENT,
ID_CHALLENGE,
ID_SHOPPING,
ID_TIMER,
ID_BONUS,
ID_FILLER,
ID_TRAP,
)

from .constants import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class CookingMama3Client(BizHawkClient):
    game = GAME_NAME
    system = "NDS"
    patch_suffix = ""
    logger = logging.getLogger("Client")
    #a copy of most of the important parts of the sava data is stored in the ap server
    #this accomplishes a few things: first, if the save file is somehow lost, it can be resynced with this
    #second, this allows obtained items to be tracked without storing it somewhere in the save file, which there may not be much room for
    #third, this allows for items that are unlocked in-game to be immediately wiped so as to not ruin the progression
    special_items = []
    accessory_array = [0] * 49
    friend_array = [0] * 16
    recipe_array = [0] * 327
    challenge_array = [255] * 40
    shopping_array = [0] * 12

    #this is a dict that stores data that isnt normally tracked by the game and is ap-exclusive
    extra_data = dict()
    config = dict()

    #goal conditions such as these are calced on connection every time
    gold_medals_awarded = set()
    num_gold_medals = 0
    num_friends_fed = 0

    random: Random = Random()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            if ctx.rom_hash != US_HASH:
                self.logger.warning(f"This is not the correct hash for this game! Make sure that you are using the US Version and that the ROM was dumped correctly.")
                return False
        except bizhawk.RequestFailedError:
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.10
        return True

    #determine how the save file should be handled. overall, checks to see if it needs to be cleared and set up or not
    async def ram_init(self, ctx: "BizHawkClientContext"):
        game_data = await bizhawk.read(ctx.bizhawk_ctx, [
            (MAGIC_NUMBER, 10, "ARM9 System Bus")
        ])
        #if the "magic number" is not detected in the save file, completely prepare the file for archipelagoing
        if ctx.server_seed_name != None:
            if int.from_bytes(bytearray(game_data[0]), "little") != int(ctx.server_seed_name):
                await self.sync_save(ctx)
                return 0
            #otherwise, a less destructive sync is done, which mostly just makes sure that items unlocked in-game dont activate
            else:
                await self.partial_sync_save(ctx)
                return 1

    #this clears up all of the saved data and entirely replaces it with the one stored in the data storage
    #this includes stored in-game scores as well. this is important for initializing a save for the first time, and also allows you to re-obtain scores and unlocks if you lose the save for some reason
    async def sync_save(self, ctx: "BizHawkClientContext") -> None:
        writes: list[tuple[int, Sequence[int], str]] = []
        #clears trophies and resets obtained trophies to 0 so they can be counted and re-rewarded
        writes.append((START_OF_TROPHIES, 0x0.to_bytes(5, "little"), "ARM9 System Bus"))

        self.extra_data["TrophyList"] = []
        special_bits = 0
        for i in self.special_items:
            special_bits |= SPECIAL_ITEMS_BYTE[i]
        writes.append((SPECIAL_ITEMS, special_bits.to_bytes(), "ARM9 System Bus"))

        #resets mama's accessories to default, so that you dont start with random accessories if using a new save
        ##note that if this is done during a reset, the game will overwrite mama's accessories just afterwards anyways, so this will have no effect. but assumedly, on first connect, the game will already be loaded, so the game will not do this and rather save the new clothes to the file! clever!
        writes.append((CURRENT_SHIRT, 0x3E8.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_GLASSES, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_EARRINGS, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_HAT, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_HEADGEAR, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_BONNET, 0x43D.to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((CURRENT_BACKGROUND, 0x0.to_bytes(1, "little"), "ARM9 System Bus"))
        writes.append((START_OF_APPLIANCES, 0x0.to_bytes(11, "little"), "ARM9 System Bus"))

        #things that are stored in the game save file, but are backed up on the server just incase a sync needs to be done
        writes.append((BONUS_COUNT, self.extra_data["NumOfBonusChecks"].to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((WAITING_BONUS_FILLER, self.extra_data["NumOfFillerWaiting"][0].to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((WAITING_TIME_TRAP, self.extra_data["NumOfFillerWaiting"][2].to_bytes(2, "little"), "ARM9 System Bus"))
        writes.append((WAITING_BABEL_TRAP, self.extra_data["NumOfFillerWaiting"][3].to_bytes(2, "little"), "ARM9 System Bus"))

        writes.append((START_OF_STICKERS, bytearray(self.accessory_array), "ARM9 System Bus"))

        writes.append((START_OF_FRIENDS, bytearray(self.friend_array), "ARM9 System Bus"))

        writes.append((START_OF_RECIPES, bytearray(self.recipe_array), "ARM9 System Bus"))

        writes.append((START_OF_SHOPPING, bytearray(self.shopping_array), "ARM9 System Bus"))

        writes.append((START_OF_CHALLENGE, bytearray(self.challenge_array), "ARM9 System Bus"))

        #sets language flag to english, incase the last game was closed while on a Babel Trap
        writes.append((LANGUAGE_FLAG, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))
        writes.append((TRAP_TIME_START, 0x0.to_bytes(4, "little"), "ARM9 System Bus"))
        writes.append((TRAP_TIME_DURATION, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))

        #writes the server's seed to an unused part of the save file. This lets the client know if this save is setup, and/or if its the right save for this slot
        if ctx.server_seed_name != None:
            magic_number = int(ctx.server_seed_name)
            writes.append((MAGIC_NUMBER, magic_number.to_bytes(20, "little"), "ARM9 System Bus"))
        await bizhawk.write(ctx.bizhawk_ctx, writes)
        self.logger.warning(f"game synced!")

    #the game will unlock things on its own for certain milestones. we dont want this, so we go through and clean up extraneous stuff
    #this overall doesn't touch scores. we don't want for new scores to get overwritten, after all. if we truly do want to clear all the scores, then we can use the above method
    async def partial_sync_save(self, ctx: "BizHawkClientContext") -> None:
        writes: list[tuple[int, Sequence[int], str]] = []
        special_bits = 0
        for i in self.special_items:
            special_bits |= SPECIAL_ITEMS_BYTE[i]
        writes.append((SPECIAL_ITEMS, special_bits.to_bytes(), "ARM9 System Bus"))

        writes.append((START_OF_STICKERS, bytearray(self.accessory_array), "ARM9 System Bus"))

        #updates array to only have unlocked AP friends
        for id, item in enumerate(self.extra_data["FriendList"]):
            friend_id = FRIENDS_BYTE.index(item) * 2
            self.friend_array[friend_id] = (id + 1)
        #only affects the bytes that dictate which friends are unlocked. the flag that stores whether theyve been cooked for are not affected
        for id, i in enumerate(self.friend_array):
            if id % 2 == 0:
                writes.append((START_OF_FRIENDS + id, i.to_bytes(), "ARM9 System Bus"))

        #updates the array to only have unlocked AP recipes
        for id, item in enumerate(self.extra_data["RecipeList"]):
            recipe_id = RECIPE_LIST.index(item) * 4
            self.recipe_array[recipe_id] = (id + 1)
        #only affects the bytes that dictate which recipes are unlocked. scores are not affected
        for id, i in enumerate(self.recipe_array):
            if id % 4 == 0:
                writes.append((START_OF_RECIPES + id, i.to_bytes(), "ARM9 System Bus"))

        #only affects the first 4 bytes, which are the ones responsible for unlocking shopping levels. scores are not affected
        for id, i in enumerate(self.shopping_array):
            if id < 4:
                writes.append((START_OF_SHOPPING + id, i.to_bytes(), "ARM9 System Bus"))
        await bizhawk.write(ctx.bizhawk_ctx, writes)

    #The Big One. this is where all of the actual logic for the ap is.
    ##i will admit that it is perhaps a bit too long to be one big ugly method, but i dont wanna bother splitting it up. ill try to comment it to make it neater to read
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.slot is None:
            return
        #was getting key error issues because the client seemingly just didnt make all the dicts. blegh.
        if (str(ctx.slot) + "SavedData") not in ctx.stored_data or (str(ctx.slot) + "ExtraData") not in ctx.stored_data or (str(ctx.slot) + "Options") not in ctx.stored_data:
            await ctx.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": str(ctx.slot) + "SavedData",
                        "default": {
                                    "SpecialItems": [],
                                    "Accessories": [0] * 49,
                                    "Friends": [0] * 16,
                                    "Recipes": [0, 255, 255, 255] * 81,
                                    "Challenges": [255] * 40,
                                    "Shopping": [0] * 12,
                                    
                                    },
                        "want_reply": True,
                        "operations": [{"operation": "default", "value": {
                                                                            "SpecialItems": [],
                                                                            "Accessories": [0] * 49,
                                                                            "Friends": [0] * 16,
                                                                            "Recipes": [0, 255, 255, 255] * 81,
                                                                            "Challenges": [255] * 40,
                                                                            "Shopping": [0] * 12,
                                                                            }}],
                    },
                    {
                        "cmd": "Set",
                        "key": str(ctx.slot) + "ExtraData",
                        "default": {
                                    "ReceivedItems": 0,
                                    "FriendList": [],
                                    "RecipeList": [],
                                    "Ingredients": 0,
                                    "NumOfShops": 0,
                                    "NumOfChallenge": 0,
                                    "NumOfTimerBuffs": 0,
                                    "NumOfBonusBuffs": 0,
                                    "NumOfBonusChecks": 0, 
                                    "NumOfFillerWaiting": [0] * 4, #0. random bonuses, 1. bad fashion trap, 2. timer trap, 3. babel trap
                                    "NumOfFillerDone": [0] * 4, #0. random bonuses, 1. bad fashion trap, 2. timer trap, 3. babel trap
                                    "TrophyList": []

                                    },
                        "want_reply": True,
                        "operations": [{"operation": "default", "value": {
                                                                            "ReceivedItems": 0,
                                                                            "FriendList": [],
                                                                            "RecipeList": [],
                                                                            "NumOfIngredients": 0,
                                                                            "NumOfShops": 0,
                                                                            "NumOfChallenge": 0,
                                                                            "NumOfTimerBuffs": 0,
                                                                            "NumOfBonusBuffs": 0,
                                                                            "NumOfBonusChecks": 0,
                                                                            "NumOfFillerWaiting": [0] * 4, #0. random bonuses, 1. bad fashion trap, 2. timer trap, 3. babel trap
                                                                            "NumOfFillerDone": [0] * 4, #0. random bonuses, 1. bad fashion trap, 2. timer trap, 3. babel trap
                                                                            "TrophyList": []
                                                                            }}],
                    },
                    {
                        "cmd": "Set",
                        "key": str(ctx.slot) + "Options",
                        "default": {
                                    "ExcludedMedalChecks": ctx.slot_data.get("excluded_medal_checks", frozenset({})),
                                    "ProgressiveScore": int(ctx.slot_data.get("progressive_recipe_scores", 1)),
                                    "ChosenGoals": ctx.slot_data.get("goal_option", frozenset({"unlocked_recipes", "gold_medals", "cook_for_friend", "special_items"})),
                                    "TimerBuffs": int(ctx.slot_data.get("timer_buffs", 2)),
                                    "MinimumGoldMedal": int(ctx.slot_data.get("gold_medals_sources", 0)),
                                    "GoalThresholds": 
                                                    {
                                                        "NumOfRecipes": int(ctx.slot_data.get("number_recipes_for_goal", 30)),
                                                        "NumOfMedals": int(ctx.slot_data.get("number_gold_medals", 10)),
                                                        "NumOfFriends": int(ctx.slot_data.get("number_cook_for_friends", 4)),
                                                        "NumOfSpecialItem": int(ctx.slot_data.get("number_special_items", 2)),
                                                    },

                                    },
                        "want_reply": True,
                        "operations": [{"operation": "default", "value": {
                                                                                "ProgressiveScore": int(ctx.slot_data.get("progressive_recipe_scores", 1)),
                                                                                "ChosenGoals": ctx.slot_data.get("goal_option", frozenset({"unlocked_recipes", "gold_medals", "cook_for_friend", "special_items"})),
                                                                                "TimerBuffs": int(ctx.slot_data.get("timer_buffs", 2)),
                                                                                "MinimumGoldMedal": int(ctx.slot_data.get("gold_medals_sources", 0)),
                                                                                "GoalThresholds": 
                                                                                                {
                                                                                                    "NumOfRecipes": int(ctx.slot_data.get("number_recipes_for_goal", 30)),
                                                                                                    "NumOfMedals": int(ctx.slot_data.get("number_gold_medals", 10)),
                                                                                                    "NumOfFriends": int(ctx.slot_data.get("number_cook_for_friends", 4)),
                                                                                                    "NumOfSpecialItem": int(ctx.slot_data.get("number_special_items", 2)),
                                                                                                },
                                                                            }}],
                    },
                ]
            )
            await asyncio.sleep(0.1)
            return
            #client doesnt do anything on first pass
        else:
            #collect data from data storage
            self.special_items = ctx.stored_data[str(ctx.slot) + "SavedData"]["SpecialItems"]
            self.accessory_array = ctx.stored_data[str(ctx.slot) + "SavedData"]["Accessories"]
            self.friend_array = ctx.stored_data[str(ctx.slot) + "SavedData"]["Friends"]
            self.recipe_array = ctx.stored_data[str(ctx.slot) + "SavedData"]["Recipes"]
            self.challenge_array = ctx.stored_data[str(ctx.slot) + "SavedData"]["Challenges"]
            self.shopping_array = ctx.stored_data[str(ctx.slot) + "SavedData"]["Shopping"]
            self.extra_data = ctx.stored_data[str(ctx.slot) + "ExtraData"]
            self.config = ctx.stored_data[str(ctx.slot) + "Options"]

        sync_type = await self.ram_init(ctx)
        #if a destructive sync was done, do not go further
        if sync_type == 0:
            return

        writes: list[tuple[int, Sequence[int], str]] = []
        #long and out of order. would you want to go through the code and change ALL the byte array indices? thought so
        game_data = await bizhawk.read(ctx.bizhawk_ctx, [
            (SPECIAL_ITEMS, 0x1, "ARM9 System Bus"),
            (START_OF_RECIPES, 0x146, "ARM9 System Bus"),
            (TIMER_TYPE, 0x1, "ARM9 System Bus"),
            (CHALLENGE_PAGE, 0x1, "ARM9 System Bus"),
            (SAVED_BONUSES, 0x1, "ARM9 System Bus"),
            (CURRENT_RECIPE, 0x1, "ARM9 System Bus"),
            (START_OF_FRIENDS, 0x10, "ARM9 System Bus"),
            (START_OF_CHALLENGE, 40, "ARM9 System Bus"),
            (START_OF_SHOPPING, 12, "ARM9 System Bus"),
            (CURRENT_BONUS, 0x1, "ARM9 System Bus"),
            (CURRENT_STEP, 0x1, "ARM9 System Bus"),
            (CURRENT_TOTAL_STEP, 0x1, "ARM9 System Bus"),
            (PREV_BONUS, 0x1, "ARM9 System Bus"),
            (BONUS_WATCHER, 0x1, "ARM9 System Bus"),
            (GAMEPLAY_TIMER, 0x4, "ARM9 System Bus"),
            (TRAP_TIME_START, 0x4, "ARM9 System Bus"),
            (TRAP_TIME_DURATION, 0x2, "ARM9 System Bus"),
            (GAME_MODE, 0x1, "ARM9 System Bus"),
            (TIMER_STATE, 0x1, "ARM9 System Bus"),
            (PREV_TIMER_STATE, 0x1, "ARM9 System Bus"),
            (WAITING_BONUS_FILLER, 0x2, "ARM9 System Bus"),
            (TARGET_TIMER, 0x2, "ARM9 System Bus"),
            (CURRENT_TIMER, 0x2, "ARM9 System Bus"),
            (GAME_MODE_2, 0x1, "ARM9 System Bus"),
            (PREV_GAME_MODE2, 0x1, "ARM9 System Bus"),
            (PREV_GAME_MODE, 0x1, "ARM9 System Bus"),
            (START_OF_TROPHIES, 0x5, "ARM9 System Bus"),
            (CURRENT_MINIGAME, 0x2, "ARM9 System Bus"),
            (BONUS_COUNT, 0x2, "ARM9 System Bus"),
            (WAITING_TIME_TRAP, 0x2, "ARM9 System Bus"),
            (WAITING_BABEL_TRAP, 0x2, "ARM9 System Bus"),
        ])

        waiting_bonus_filler = int.from_bytes(bytearray(game_data[20]), "little")
        waiting_time_trap = int.from_bytes(bytearray(game_data[29]), "little")
        waiting_babel_trap = int.from_bytes(bytearray(game_data[30]), "little")
        received_index = self.extra_data["ReceivedItems"]

###RECEIVING ITEMS=================================================================================================

        if received_index < len(ctx.items_received):
            item = ctx.items_received[received_index]
            self.extra_data["ReceivedItems"] += 1

            item_name = ctx.item_names.lookup_in_slot(item.item)
            item_code = item.item

            ##checks for the special items
            if item_code < ID_COLLECTIONS and item_code >= ID_SPECIAL_ITEMS:
                #the bit value for the received item is or'd with whats already there
                if item_name not in self.special_items:
                    self.special_items.append(item_name)
                #nothing is directly written here because its already done by partial_sync_save
                
            ##check for accessories
            elif item_code < ID_SETS and item_code >= ID_COLLECTIONS:
                #theres only 3 collection items, so for them, we just check them individually and fill up all of the necessary bits
                if item_code == ID_COLLECTIONS:
                    for id in range(0, 0x1A):
                        self.accessory_array[id] = 0xFF
                if item_code == ID_COLLECTIONS + 1:
                    for id in range(0x1A, 0x26):
                        #the last byte of the Accessories list overlaps with the appliances list, so for this byte, we OR it so that the other few bits arent set or unset on accident
                        if id == 0x25:
                            self.accessory_array[id] |=  0x03
                        else:
                            self.accessory_array[id] = 0xFF
                if item_code == ID_COLLECTIONS + 2:
                    for id in range(0x25, len(self.accessory_array)):
                        if id == 0x25:
                            self.accessory_array[id] |=  0xFC
                        else:
                            self.accessory_array[id] = 0xFF     
            elif item_code < ID_INDIVIDUAL and item_code >= ID_SETS:
                allbits: dict[int, list[int]] = {} #creates a dict of all offsets that need to be changed, plus their bits
                for item in ALL_ACCESSORY[item_name]:
                    #we go through every single item that exists in this particular set and add their bits and offsets to this dict
                    if ALL_ACCESSORY[item_name][item][0] not in allbits:
                        allbits[ALL_ACCESSORY[item_name][item][0]] = []
                    allbits[ALL_ACCESSORY[item_name][item][0]].append(ALL_ACCESSORY[item_name][item][1])
                for key in allbits:
                    for bit in allbits[key]:
                        if item_name in STICKER_FULL: #if its part of first list, just use the offset
                            self.accessory_array[key] |= bit
                        else: #if not, add 26 to the offset to ensure it lines up with the combined list
                            self.accessory_array[key + 26] |= bit    
            elif item_code < ID_FRIEND and item_code >= ID_INDIVIDUAL:
                for id, key in enumerate(ALL_ACCESSORY): #find the key at that id
                    for item in ALL_ACCESSORY[key]:
                        #somewhat messy way to see if the item name matches an item in the accessory list
                        if item_name == (item  + " (Sticker)") or item_name == (item  + " (Clothing)") or item_name == (item  + " (Kitchenware)"):
                            #like before, if it exists, we add it to the correct offset depending on which list its a part of
                            if item in ALL_STICKER:
                                self.accessory_array[ALL_ACCESSORY[key][item][0]] |= ALL_ACCESSORY[key][item][1]
                            else:
                                self.accessory_array[ALL_ACCESSORY[key][item][0] + 26] |= ALL_ACCESSORY[key][item][1]

            ##friend unlocks
            elif item_code < ID_RECIPE and item_code >= ID_FRIEND:
                id = item_code - ID_FRIEND
                friend_name = FRIENDS_BYTE[id]
                self.extra_data["FriendList"].append(friend_name)
                self.friend_array[id * 2] = len(self.extra_data["FriendList"])
                #like before, things are already written by partial_sync_save so we dont do it here

            ##recipe unlocks
            elif item_code < ID_INGREDIENT and item_code >= ID_RECIPE:
                id = item_code - ID_RECIPE
                recipe_name = RECIPE_LIST[id]
                if recipe_name != None:
                    self.extra_data["RecipeList"].append(recipe_name)
                    self.recipe_array[id * 4] = len(self.extra_data["RecipeList"])

            ##ingredient unlocks for Lets Match mode   
            elif item_code < ID_CHALLENGE and item_code >= ID_INGREDIENT:
                self.extra_data["Ingredients"] |= INGREDIENTS_BYTE[item_name]

            ##unlocks pages of the cooking contest challenges
            elif item_code < ID_SHOPPING and item_code >= ID_CHALLENGE:
                self.extra_data["NumOfChallenge"] += 1
                #not technically necessary, but this changes the lower byte of the score to 0, which makes the challenge have a "NEW" sticker.
                #it does look a bit off because most challenges arent supposed to have this emblem, but it doesnt seem to affect anything, and is a nice easy way to visually denote which challenges are allowed
                for i in range(0, self.extra_data["NumOfChallenge"] * 4):
                    writes.append((START_OF_CHALLENGE + (i * 2), 0x00.to_bytes(1, "little"), "ARM9 System Bus"))
                    
            ##unlocks levels of the shopping minigame
            elif item_code < ID_TIMER and item_code >= ID_SHOPPING:
                self.extra_data["NumOfShops"] += 1
                self.shopping_array[self.extra_data["NumOfShops"] - 1] = 0x01 

            ##progressive timer buffs
            elif item_code < ID_BONUS and item_code >= ID_TIMER:
                self.extra_data["NumOfTimerBuffs"] += 1

            ##progressive bonus buffs
            elif item_code < ID_FILLER and item_code >= ID_BONUS:
                self.extra_data["NumOfBonusBuffs"] += 1

            ##random extra bonuses
            elif item_code < ID_TRAP and item_code >= ID_FILLER:
                waiting_bonus_filler += 1 
                writes.append((WAITING_BONUS_FILLER, waiting_bonus_filler.to_bytes(2, "little"), "ARM9 System Bus"))
            ##traps
            elif item_code < ID_TRAP + 3 and item_code >= ID_TRAP:
                ##checking for each trap. nested for... readability probably
                ##bad fashion
                if item_code == ID_TRAP:
                    self.extra_data["NumOfFillerWaiting"][item_code - ID_TRAP + 1] += 1 
                    #timer and babel traps are primarily stored in the slack area of the save file, because i was having issues with them procing several times if i kept them on the server. It doesnt actually matter if bad fashion traps proc several times though, so im not gonna bother
                ##timer trap
                elif item_code == ID_TRAP + 1:
                    waiting_time_trap += 1
                    writes.append((WAITING_TIME_TRAP, waiting_time_trap.to_bytes(2, "little"), "ARM9 System Bus"))
                elif item_code == ID_TRAP + 2:
                    waiting_babel_trap += 1
                    writes.append((WAITING_BABEL_TRAP, waiting_babel_trap.to_bytes(2, "little"), "ARM9 System Bus"))
            ##if you see this, oops
            else:
                self.logger.warning(f"what the hey is this? {item_name} {item_code}")

###GAME HOUSECLEANING=============================================================
        ##used for various things throughout this part of the code
        current_mode = int.from_bytes(bytearray(game_data[17]), "little")
        timer_state = int.from_bytes(bytearray(game_data[18]), "little")
        timer_type = int.from_bytes(bytearray(game_data[2]), "little")
        prev_timer_state = int.from_bytes(bytearray(game_data[19]), "little")
        current_minigame = int.from_bytes(bytearray(game_data[27]), "little")

        #if Lets Match mode is entered, print the unlocked ingredients in the client. a bit of a compromise since i couldnt figure out how to visually indicate it ingame.
        #mode 3 = lets match (non practice). mode 4 =  let's match (practice)
        current_mode_2 = int.from_bytes(bytearray(game_data[23]), "little")
        prev_mode_2 = int.from_bytes(bytearray(game_data[24]), "little")
        if (prev_mode_2 != 3 and prev_mode_2 != 4) and current_mode_2 == 3:
            ingredients = [name 
            for i, name in enumerate(INGREDIENTS_BYTE) if (self.extra_data["Ingredients"] & INGREDIENTS_BYTE[name]) == INGREDIENTS_BYTE[name]
            ]
            self.logger.warning(f"Currently Unlocked Ingredients: {ingredients}")
        prev_mode_2 = current_mode_2
        writes.append((PREV_GAME_MODE2, prev_mode_2.to_bytes(1, "little"), "ARM9 System Bus"))

        ##Checks if a secret recipe is being prepared, and if so, makes sure that its respective ingredients are unlocked.
        #if the ingredients arent obtained, you get stuck on the first step, and minigames will end instantly.
        current_recipe = int.from_bytes(bytearray(game_data[5]), "little")
        needed_ingredients = 0b000000
        if current_recipe > 0x42: #index for Omelette (first secret recipe)
            for i, key in enumerate(RECIPE_BYTE):
                if i == current_recipe - 1:
                    needed_ingredients = RECIPE_BYTE[key] 
                    break
            #checks if needed ingredients are available, and also makes sure that player is actually in Lets Match mode
            ##the current recipe byte doesnt get cleared until its directly overwritten by something else. so if you tried to do a locked recipe and then immediately went to do a challenge, the game would panic because it thought you were still doing that recipe
            if (self.extra_data["Ingredients"] & needed_ingredients != needed_ingredients) and (current_mode_2 == 3 or current_mode_2 == 4):
                writes.append((CURRENT_STEP, 0x0.to_bytes(1, "little"), "ARM9 System Bus"))
                if prev_timer_state == 0 and timer_state == 1:
                    self.logger.warning(f"You don't have the necessary ingredients for this recipe!")
                    writes.append((TIMER_STATE, 0x2.to_bytes(1, "little"), "ARM9 System Bus"))

        #block challenge mode checks
        challenge_page = int.from_bytes(bytearray(game_data[3]), "little")
        #if the game is in Challenge mode, and the current page of the challenge list is greater than or equal to (0-indexed!) the number of challenges, we must make sure the player does not try a locked challenge
        #page 4 is the page for Special Item challenges which are always unlocked when the special item is obtained
        if current_mode == 0x05 and (challenge_page >= self.extra_data["NumOfChallenge"] and challenge_page != 0x04):
            #nested if for better readability or something. the timer state is usually 0, and becomes 1 when the timer is actively counting. this indicates that a game has been started
            if prev_timer_state == 0 and timer_state == 1:
                self.logger.warning(f"This Challenge has not been unlocked yet!")
                #if this is the case, the timer state is set to 2. this makes the game automatically complete the minigame.
                writes.append((TIMER_STATE, 0x2.to_bytes(1, "little"), "ARM9 System Bus"))
            
        #if there is a bonus buff, then the bonus counter is not allowed to go below the number of buffs
        saved_bonus = int.from_bytes(bytearray(game_data[4]), "little")
        bonus_buff = self.extra_data["NumOfBonusBuffs"]
        if saved_bonus < bonus_buff:
            writes.append((SAVED_BONUSES, bonus_buff.to_bytes(1, "little"), "ARM9 System Bus"))

        #change the timer depending on the buff
        ##this feature is disabled entirely if timer buffs are disabled
        if self.config["TimerBuffs"] > 0:
            timer_buffs = self.extra_data["NumOfTimerBuffs"]
            #if a minigame is in progress
            ##by design, this also affects Challenge mode
            if prev_timer_state == 0 and timer_state == 1:
                #inexplicably, there is one minigame that actually depends on the timer being the correct amount of time. this is the only one in the entire game thats like this, so id rather add a stupid check for it than remove this whole thing outright
                if current_minigame != 0x1e:
                    target_time = int.from_bytes(bytearray(game_data[21]), "little")
                    current_time = int.from_bytes(bytearray(game_data[22]), "little")
                    #purposefully affects the target time, so that it looks seamless in-game
                    ##idea is: each buff adds 10% to the timer, 0 buffs starts at 90% of the original. 
                    target_time = int(target_time + (target_time * (timer_buffs * .10) - (target_time * .10))) 
                    writes.append((TARGET_TIMER, target_time.to_bytes(2, "little"), "ARM9 System Bus"))

        #apply random extra bonuses
        current_step = int.from_bytes(bytearray(game_data[10]), "little")
        current_step_total = int.from_bytes(bytearray(game_data[11]), "little")
        current_bonus = int.from_bytes(bytearray(game_data[9]), "little")
        #we wait until a dish is finished, and then just append the random extra bonuses to the "current recipe bonus" counter
        #somewhat scuffed way to check if a dish is done... see if the current step = number of total steps, which always happens on the results screen. but we make sure they arent both 0, which happens when the game is booted and such
        if current_step == current_step_total and current_step_total > 0 and waiting_bonus_filler > 0:
            #in the EXTREMELY RARE CASE where the player has more than 255 bonuses saved up, the bonuses gets clamped to 255. the bonus counter MIGHT be 2-byte but like, i already dont wanna have to wait through 255 bonuses so we'll just max it at that
            if current_bonus + waiting_bonus_filler > 255:
                waiting_bonus_filler = waiting_bonus_filler - (255 - current_bonus)
                current_bonus = 255
            else:
                current_bonus += waiting_bonus_filler
                waiting_bonus_filler = 0
            ##the number of steps remains after returning to the menu, which means that bonuses obtained between completing one recipe and starting another may be lost. it doesnt seem to hurt anything at this point to just manually set it to 0 ourselves
            writes.append((CURRENT_STEP, 0x0.to_bytes(1, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_BONUS, current_bonus.to_bytes(1, "little"), "ARM9 System Bus"))
            writes.append((WAITING_BONUS_FILLER, waiting_bonus_filler.to_bytes(2, "little"), "ARM9 System Bus"))

        #bad fashion trap
        if self.extra_data["NumOfFillerWaiting"][1] > 0:
            #sets all of the clothing to random values so that mamas outfit is totally randomized
            ##funny thing: all the accessories are in one big table in the files, but these memory values are only intended to hold these arbitrary values that correspond to what type of accessory they are
            ##you can technically set these to any accessory in the table! sometimes it works and sometimes it doesnt. im not gonna bother finding out what works and what doesnt, so we'll only use valid values here
            writes.append((CURRENT_SHIRT, self.random.randint(0x3E8, 0x41E).to_bytes(2, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_GLASSES, self.random.randint(0x41F, 0x428).to_bytes(2, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_EARRINGS, self.random.randint(0x429, 0x42D).to_bytes(2, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_HAT, self.random.randint(0x42E, 0x437).to_bytes(2, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_HEADGEAR, self.random.randint(0x438, 0x43C).to_bytes(2, "little"), "ARM9 System Bus"))
            writes.append((CURRENT_BONNET, self.random.randint(0x43D, 0x441).to_bytes(2, "little"), "ARM9 System Bus"))
            self.extra_data["NumOfFillerWaiting"][1] -= 1

        #timer trap
        if waiting_time_trap > 0:
            #ensures that the game is in a cooking mode
            if current_mode == 0x3 or current_mode == 0x4:
                #if a minigame is in progress
                ##unlike other timer-affecting things, this only checks if a timer is elapsing. this is so that a bad timer trap can occur in the middle of a minigame!
                ##oh and it also checks if the minigame actually utilizes the timer, thats what the latter thing is about
                if timer_state == 1 and timer_type != 0:
                    #once again, 1e is unwinnable if the timer is edited
                    if current_minigame != 0x1e:
                        target_time = int.from_bytes(bytearray(game_data[21]), "little")
                        current_time = int.from_bytes(bytearray(game_data[22]), "little")
                        #purposefully affects the current time, so that the player sees the clock hand jump forwards
                        ##value is arbitrary, lemme know if its too much/too little! the idea is not to make a timer trap instant death, but to just make things harder.
                        ##since they also stack, i went for something smaller instead of something larger
                        current_time = int(current_time + target_time * .20) 
                        writes.append((CURRENT_TIMER, current_time.to_bytes(2, "little"), "ARM9 System Bus"))
                        waiting_time_trap -= 1
                        writes.append((WAITING_TIME_TRAP, waiting_time_trap.to_bytes(2, "little"), "ARM9 System Bus"))


        #babel trap
        current_time = int.from_bytes(bytearray(game_data[14]), "little")
        starting_time = int.from_bytes(bytearray(game_data[15]), "little")
        time_remaining = int.from_bytes(bytearray(game_data[16]), "little")
        if waiting_babel_trap > 0:
            #if a babel trap is already activated, we dont want to change the starting time, since its already started
            if starting_time == 0:
                writes.append((TRAP_TIME_START, current_time.to_bytes(4, "little"), "ARM9 System Bus"))
            #apply a preset amount of frames to the trap timer. this is equal to about a minute
            time_remaining += TRAP_DURATION
            #set language flag to italian
            ##the non-english localizations in the US version of cooking mama are unused and unfinished. most of the language options crash the game at various points, but italian doesnt *seem* to do that. Some strings are localized, but a lot of them also just pull random stuff from the english localization
            ##this is why it isnt called a "Language trap", because it isnt really setting it to another language, its kind of shuffling the text in unexpected ways
            writes.append((LANGUAGE_FLAG, 0x4.to_bytes(1, "little"), "ARM9 System Bus"))
            #in the rare case where the player already has over 65535 frames lined up, it just gets clamped to that. we could technically make this limit as high as we want, but 65535 frames is already like 18 minutes, so i'll call it there
            if time_remaining > 65535:
                time_remaining = 65535
            writes.append((TRAP_TIME_DURATION, time_remaining.to_bytes(2, "little"), "ARM9 System Bus"))
            waiting_babel_trap -= 1
            writes.append((WAITING_BABEL_TRAP, waiting_babel_trap.to_bytes(2, "little"), "ARM9 System Bus"))
        #manage existing babel traps if they exist
        elif time_remaining > 0:
            #if the current frame counter is less than the starting time, this indicates that the game was reset, or that the game was on for so long that the timer has overflowed (which, according to my calculations, will take over 2 years!)
            if current_time < starting_time:
                #in this case we just reset the timer outright, as PUNISHMENT for trying to get out of it by resetting (or for leaving the game on for over 2 years straight)
                starting_time = current_time
                writes.append((LANGUAGE_FLAG, 0x4.to_bytes(1, "little"), "ARM9 System Bus"))
            #time has run out
            elif current_time - starting_time >= time_remaining:
                writes.append((LANGUAGE_FLAG, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))
                writes.append((TRAP_TIME_START, 0x0.to_bytes(4, "little"), "ARM9 System Bus"))
                writes.append((TRAP_TIME_DURATION, 0x0.to_bytes(2, "little"), "ARM9 System Bus"))
            
        
        #store timer state for next time
        prev_timer_state = timer_state
        writes.append((PREV_TIMER_STATE, prev_timer_state.to_bytes(1, "little"), "ARM9 System Bus"))

        #goal tracker
        ##when the options menu is opened, the client will list the current goal conditions, and the progress towards them
        prev_mode = int.from_bytes(bytearray(game_data[25]), "little")
        if prev_mode == 0 and current_mode == 0x0a:
            self.logger.warning(f"GOAL TRACKER:")
            if "unlocked_recipes" in self.config["ChosenGoals"]:
                self.logger.warning(f"Obtained Recipes: {len(self.extra_data["RecipeList"])}/{self.config["GoalThresholds"]["NumOfRecipes"]}")
            if "gold_medals" in self.config["ChosenGoals"]:
                self.logger.warning(f"Number of Gold Medals: {self.num_gold_medals}/{self.config["GoalThresholds"]["NumOfMedals"]}")
            if "cook_for_friend" in self.config["ChosenGoals"]:
                self.logger.warning(f"Number of Fed Friends: {self.num_friends_fed}/{self.config["GoalThresholds"]["NumOfFriends"]}")
            if "special_items" in self.config["ChosenGoals"]:
                self.logger.warning(f"Obtained Special Items: {len(self.special_items)}/{self.config["GoalThresholds"]["NumOfSpecialItem"]}")
            #yes there is already a check for this up there. i want this to print down here. cope
            if "gold_medals" in self.config["ChosenGoals"]:
                self.logger.warning(f"Minimum Gold Medal Difficulty is {MEDAL_DIFFICULTY[self.config["MinimumGoldMedal"]]}")
            if len(self.config["ExcludedMedalChecks"]) > 0:
                chosen_medals = ALL_MEDAL_TYPES.difference(self.config["ExcludedMedalChecks"])
                self.logger.warning(f"These medals have checks: {chosen_medals}")
        prev_mode = current_mode
        writes.append((PREV_GAME_MODE, prev_mode.to_bytes(1, "little"), "ARM9 System Bus"))

###SENDING STUFF=======================================================================================================
        
        ##send bonus checks
        prev_bonus = int.from_bytes(bytearray(game_data[12]), "little")
        bonus_watch = int.from_bytes(bytearray(game_data[13]), "little")
        bonus_count = int.from_bytes(bytearray(game_data[28]), "little")
        print(f"{prev_bonus} and {bonus_watch}")
        #our lovely bonus watcher moves to 30 when a bonus is unlocked, and then to 31. we watch for that and send checks only when that happens
        if prev_bonus == 0x30 and bonus_watch == 0x31:
            #to avoid race condition nonsense, every bonus loc ID up to this point is checked to see if it was sent proper
            for i in range(ID_BONUS_LOC, ID_BONUS_LOC + bonus_count + 1): #must be +1 because range isnt inclusive to the last value!
                if i not in ctx.locations_checked:
                    ctx.locations_checked.add(i)
            bonus_count += 1
        prev_bonus = bonus_watch
        writes.append((PREV_BONUS, prev_bonus.to_bytes(1, "little"), "ARM9 System Bus"))
        writes.append((BONUS_COUNT, bonus_count.to_bytes(2, "little"), "ARM9 System Bus"))

        ##send "cook for friend" checks
        friends_list = bytearray(game_data[6])
        for i, key in enumerate(FRIENDS_BYTE):
            friend_offset = friends_list[i * 2 + 1]
            if friend_offset > 1:
                self.friend_array[i * 2 + 1] = friend_offset
                item_code = ID_COOK_FOR_FRIEND + i
                if item_code not in ctx.locations_checked:
                    self.num_friends_fed += 1
                    ctx.locations_checked.add(item_code)

        ##send recipe medal checks
        recipe_list = bytearray(game_data[1])
        progressive_score = self.config["ProgressiveScore"]
        for i, key in enumerate(RECIPE_BYTE):
            recipe_offset = recipe_list[i * 4 + 1]
            if recipe_offset != 255:
                self.recipe_array[i * 4 + 1] = recipe_offset
                if recipe_offset > 49:
                    #if this is a secret recipe, this means that it has been "discovered". we add it to the list of recipes so itll show up in Let's Cook mode and count for num of recipes goal
                    if RECIPE_BYTE[key] > 0 and key not in self.extra_data["RecipeList"]:
                        self.extra_data["RecipeList"].append(key)
                    item_code = ID_RECIPE_COOK_WITH_MAMA + (i * 3) + 2
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if recipe_offset > 72:
                    item_code = ID_RECIPE_COOK_WITH_MAMA + (i * 3) + 1
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if recipe_offset > 99:
                    item_code = ID_RECIPE_COOK_WITH_MAMA + (i * 3) 
                    if item_code not in ctx.locations_checked:
                        #if this item has already had a gold medal obtained for it, we dont want to add more for other difficulties
                        if self.config["MinimumGoldMedal"] == 0 and key not in self.gold_medals_awarded:
                            self.num_gold_medals += 1
                            self.gold_medals_awarded.add(key)
                        ctx.locations_checked.add(item_code)
            recipe_offset = recipe_list[i * 4 + 2]
            if recipe_offset != 255:
                self.recipe_array[i * 4 + 2] = recipe_offset
                if recipe_offset > 49:
                    item_code = ID_RECIPE_LETS_COOK + (i * 4) + 2
                    if item_code not in ctx.locations_checked:
                        #progressive score copies scores from higher difficulties to lower difficulties
                        ##we make sure it only does this if the lower difficulties are unattempted, or otherwise lower than what we got here. this technically wouldnt affect anything but it would look weird and not feel right
                        if progressive_score and (recipe_list[i * 4 + 1] <= recipe_offset or recipe_list[i * 4 + 1] == 0xFF):
                            writes.append((START_OF_RECIPES + (i * 4) + 1, recipe_offset.to_bytes(1, "little"), "ARM9 System Bus"))
                        ctx.locations_checked.add(item_code)
                if recipe_offset > 72:
                    item_code = ID_RECIPE_LETS_COOK + (i * 4) + 1
                    if item_code not in ctx.locations_checked:
                        if progressive_score and (recipe_list[i * 4 + 1] <= recipe_offset or recipe_list[i * 4 + 1] == 0xFF):
                            writes.append((START_OF_RECIPES + (i * 4) + 1, recipe_offset.to_bytes(1, "little"), "ARM9 System Bus"))
                        ctx.locations_checked.add(item_code)
                if recipe_offset > 99:
                    item_code = ID_RECIPE_LETS_COOK + (i * 4)
                    if item_code not in ctx.locations_checked:
                        if progressive_score and (recipe_list[i * 4 + 1] <= recipe_offset or recipe_list[i * 4 + 1] == 0xFF):
                            writes.append((START_OF_RECIPES + (i * 4) + 1, recipe_offset.to_bytes(1, "little"), "ARM9 System Bus"))
                        if self.config["MinimumGoldMedal"] <= 1 and key not in self.gold_medals_awarded:
                            self.num_gold_medals += 1
                            self.gold_medals_awarded.add(key)
                        ctx.locations_checked.add(item_code)
            recipe_offset = recipe_list[i * 4 + 3]
            if recipe_offset != 255:
                self.recipe_array[i * 4 + 3] = recipe_offset
                if recipe_offset > 99:
                    item_code = ID_RECIPE_LETS_COOK + (i * 4) + 3
                    if item_code not in ctx.locations_checked:
                        #copy score to previous difficulty if option is enabled
                        if progressive_score and (recipe_list[i * 4 + 2] <= recipe_offset or recipe_list[i * 4 + 2] == 0xFF):
                            writes.append((START_OF_RECIPES + (i * 4) + 2, recipe_offset.to_bytes(1, "little"), "ARM9 System Bus"))
                        if self.config["MinimumGoldMedal"] <= 2 and key not in self.gold_medals_awarded:
                            self.num_gold_medals += 1
                            self.gold_medals_awarded.add(key)
                        ctx.locations_checked.add(item_code)

        ##shop score checks
        shopping_list = bytearray(game_data[8])
        #this list contains both the shopping levels that are unlocked *and* the scores. we only care about the scores, so we scoop out the unlocked bytes. we also turn these into 2-byte values here, which is necessary because shopping easily goes over 255 on all difficulties
        shopping_list_clean = [
            int.from_bytes(shopping_list[i:i+2], byteorder="little")
            for i in range(4, len(shopping_list), 2)
        ]
        for i, key in enumerate(SHOPPING_BYTE):
            shopping_offset = shopping_list_clean[i]
            if shopping_offset != 0:
                if shopping_offset >= SHOPPING_BYTE[key][0]:
                    item_code = ID_SHOPPING_LOC + (i * 3)
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if shopping_offset >= SHOPPING_BYTE[key][1]:
                    item_code = ID_SHOPPING_LOC + (i * 3) + 1
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if shopping_offset >= SHOPPING_BYTE[key][2]:
                    item_code = ID_SHOPPING_LOC + (i * 3) + 2
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)

        ##challenge score checks
        challenge_list = bytearray(game_data[7])
        for i, key in enumerate(CHALLENGE_BYTE):
            challenge_offset = challenge_list[i * 2]
            #we're only gonna check the lower byte for challenges because none of the minigames even come close to being reasonable to get over 255 in
            ##if you prove me wrong, please contact me directly so i can swear you out
            if challenge_offset != 255:
                self.challenge_array[i * 2] = challenge_offset
                if challenge_offset >= CHALLENGE_BYTE[key][0]:
                    item_code = ID_COOKING_CONTEST_CHALLENGE + (i * 3)
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if challenge_offset >= CHALLENGE_BYTE[key][1]:
                    item_code = ID_COOKING_CONTEST_CHALLENGE + (i * 3) + 1
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)
                if challenge_offset >= CHALLENGE_BYTE[key][2]:
                    item_code = ID_COOKING_CONTEST_CHALLENGE + (i * 3) + 2
                    if item_code not in ctx.locations_checked:
                        ctx.locations_checked.add(item_code)

###GOAL============================================
        #completion of single goal conditions will enable one of the trophies on the top screen. these generally correspond to the trophy that would be unlocked in the vanilla game for these same reqs, except the vanilla game requires all of them instead of just a fraction
        if "unlocked_recipes" in self.config["ChosenGoals"]:
            #only procs if the trophy hasnt already been obtained
            if len(self.extra_data["RecipeList"]) >= self.config["GoalThresholds"]["NumOfRecipes"] and "Plate Trophy" not in self.extra_data["TrophyList"]:
                #also tracks which trophies have been unlocked so it can be checked against the goal later
                self.extra_data["TrophyList"].append("Plate Trophy")
                #Plate Trophy. unlocked in vanilla for discovering all recipes
                writes.append((START_OF_TROPHIES + 1, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))
        if "gold_medals" in self.config["ChosenGoals"]:
            if self.num_gold_medals >= self.config["GoalThresholds"]["NumOfMedals"] and "Pan Trophy" not in self.extra_data["TrophyList"]:
                self.extra_data["TrophyList"].append("Pan Trophy")
                #Pan trophy. unlocked in vanilla for getting a smiley face on every recipe in Let's Cook mode
                ##obviously the goal doesnt always require smiley faces, but its close enough. there is a trophy for getting all gold medals, but its kinda ill-fitting, and is placed on top of this one. so i prefer using this one
                writes.append((START_OF_TROPHIES + 3, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))
        if "cook_for_friend" in self.config["ChosenGoals"]:
            if self.num_friends_fed >= self.config["GoalThresholds"]["NumOfFriends"] and "Mama's Trophy" not in self.extra_data["TrophyList"]:
                self.extra_data["TrophyList"].append("Mama's Trophy")
                #Mama's Trophy. unlocked in vanilla for making a meal for every friend
                writes.append((START_OF_TROPHIES, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))
        if "special_items" in self.config["ChosenGoals"]:
            if len(self.special_items) >= self.config["GoalThresholds"]["NumOfSpecialItem"] and "Pot Trophy" not in self.extra_data["TrophyList"]:
                self.extra_data["TrophyList"].append("Pot Trophy")
                #Pot trophy. unlocked in vanilla for obtaining all accessories
                ##obviously not close, but you dont get a trophy for special items in vanilla. I REALLY REALLY dont wanna bother making an option for accessories being goal conditions, so this trophy would go unused otherwise
                writes.append((START_OF_TROPHIES + 2, 0x1.to_bytes(1, "little"), "ARM9 System Bus"))

        #the goal!
        ##since the above code only rewards trophies for *enabled* goal conditions, we can simply just count how many trophies have been rewarded for this
        if len(self.extra_data["TrophyList"]) >= len(self.config["ChosenGoals"]) and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

###update checked locations, write things, and update the slot data=========================================
        self.extra_data["NumOfBonusChecks"] = bonus_count
        self.extra_data["NumOfFillerWaiting"][0] = waiting_bonus_filler
        self.extra_data["NumOfFillerWaiting"][2] = waiting_time_trap
        self.extra_data["NumOfFillerWaiting"][3] = waiting_babel_trap
        await ctx.check_locations(ctx.locations_checked)
        await bizhawk.write(ctx.bizhawk_ctx, writes)
        await ctx.send_msgs(
            [
                {  
                    "cmd": "Set",
                    "key": str(ctx.slot) + "SavedData",
                    "want_reply": True,
                    "operations": [{"operation": "update", "value": {"SpecialItems":  self.special_items,
                                                                    "Accessories":  self.accessory_array,
                                                                    "Friends": self.friend_array,
                                                                    "Recipes": self.recipe_array,
                                                                    "Challenges": self.challenge_array,
                                                                    "Shopping": self.shopping_array
                                                                    }}],
                },
                {
                    "cmd": "Set",
                    "key": str(ctx.slot) + "ExtraData",
                    "want_reply": True,
                    "operations": [{"operation": "update", "value": self.extra_data}],
                },
                {
                    "cmd": "Set",
                    "key": str(ctx.slot) + "Options",
                    "want_reply": True,
                    "operations": [{"operation": "update", "value": self.config}],
                },
            ]
        )   
        await asyncio.sleep(0.1)
