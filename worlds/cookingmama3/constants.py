GAME_NAME = "Cooking Mama 3"

US_HASH = "36406ED5497799060624E09622BC09D7"

SAVED_BONUSES = 0x20B708C

START_OF_TROPHIES= 0x20B708E

SPECIAL_ITEMS = 0x20B7094

CURRENT_SHIRT = 0x20B7096 #3E8-41E
CURRENT_GLASSES = 0x20B709A #41F-428
CURRENT_EARRINGS = 0x20B709C #429-42D
CURRENT_HAT = 0x20B709E #42E-437
CURRENT_HEADGEAR = 0x20B70A0 #438-43C
CURRENT_BONNET = 0x20B70A2 #43D-441
CURRENT_BACKGROUND = 0x20B70A4
START_OF_APPLIANCES = 0x20B70A5

#Clobber Warning: these values seem to be unused in a save file. i cant say for sure, so if issues arise, check here first
MAGIC_NUMBER = 0x20B70B4
PREV_BONUS = 0x20B70C0
TRAP_TIME_START = 0x20B70C1 #reserve 4 bytes
TRAP_TIME_DURATION = 0x20B70C5 #reserve 2 bytes
PREV_TIMER_STATE = 0x20B70C7 
PREV_GAME_MODE = 0x20B70C8
PREV_GAME_MODE2 = 0x20B70C9
##these were originally stored on the server, but i kept getting issues with them not procing or procing too many times on AP.gg servers. worked fine on localhost, not on the real thing
##so now theyre stored in the slack area of the game, and the server keeps a backup just in case
BONUS_COUNT = 0x20B70CA #reserve 2 bytes
WAITING_BONUS_FILLER = 0x20B70CC #reserve 2 bytes
WAITING_TIME_TRAP = 0x20B70CE #reserve 2 bytes
WAITING_BABEL_TRAP = 0x20B70D0 #reserve 2 bytes

#the last safe byte, kept here only to remember
RESERVED_1 = 0x20B70E5
#End Clobber Warning

START_OF_STICKERS = 0x20B70E6
START_OF_ACCESSORY = 0x20B7100 #they go in order of the dress up screen, each bit is an accessory
START_OF_KITCHEN =  0x20B710B

START_OF_FRIENDS = 0x20B711B
START_OF_RECIPES = 0x20B712F
START_OF_CHALLENGE = 0x20B7274
START_OF_SHOPPING = 0x20B8D5C

LANGUAGE_FLAG = 0x20B8D68 
TRAP_DURATION = 0xE10 #about a minute's worth of frames

GAME_MODE = 0x20B8D80
GAME_MODE_2 = 0x20B8D84 #the second gamemode byte moreso tracks what menu you're in, while the first tracks what type of menu to display
CURRENT_RECIPE = 0x20B8D94
CURRENT_STEP = 0x20B8D9C
CURRENT_TOTAL_STEP = 0x20B8D9E
CURRENT_BONUS = 0x20B8DF6
CURRENT_MINIGAME = 0x20B8DD8
BONUS_WATCHER = 0x20B8E38 #this value, along with the one at 3C, seems to only become 30 on the bonus screen, and 31 when obtaining an item. i dont love using this to track bonuses, because i dont actually really understand what its doing... it seems to affect the graphics on the bonus screen when frozen. but, my other memory addresses that determine bonuses dont update in real time, making them very difficult to use for real-time bonus tracking

TIMER_TYPE = 0x20CAAE4
TIMER_STATE = 0x20CAAE8
TARGET_TIMER = 0x20CAAEC
CURRENT_TIMER = 0x20CAAEE
#"current" counts up till it gets to "Target"

CHALLENGE_PAGE = 0x20E4AE4
#determines what page youre on in the cooking contest

GAMEPLAY_TIMER = 0x23FFC3C #32-bit frame counter

SPECIAL_ITEMS_BYTE = {
    "Giant Strawberry": 0b0001,
    "Star Potato": 0b0010,
    "Giant Pumpkin": 0b0100,
    "Golden Apple": 0b1000,
}

#index * 2 = offset
#offset + 1 = if theyve been cooked for
FRIENDS_BYTE = [
    "Papa",
    "Grandpa",
    "Grandma",
    "Chika",
    "Ayaka",
    "Takuya",
    "David",
    "Kate"
]

#index * 4 = offset
#offset + 1 = cook with mama score
#offset + 2 = let's cook score
#offset + 3 = platter mode
#data value of 0 means regular recipe, binary numbers correspond to which ingredients are needed for the secret recipes
RECIPE_BYTE = {
    "Dried Squid": 0,
    "Sardine Escabeche": 0,
    "Eclair": 0,
    "Matcha Green Tea": 0,
    "Affogato": 0,
    "Creme Brulee": 0,
    "Crab Cream Croquette": 0,
    "Turban Cooked in its Shell": 0,
    "Smoked Rainbow Trout": 0,
    "Egg Tofu": 0,
    "Chicken Tulips": 0,
    "Dora-yaki": 0,
    "Strawberry Bavarois": 0,
    "Parfait": 0,
    "Fruit Punch": 0,
    "Fried Egg on Toast": 0,
    "Potato Wedges": 0,
    "Banana Muffins": 0,
    "Trout Sushi": 0,
    "Raw Oysters": 0,
    "Serrano Ham and Melon": 0,
    "Salt-Baked Sea Bream": 0,
    "Tofu Skin": 0,
    "Nagashi Somen Noodles": 0,
    "Mochi with Edamame Paste": 0,
    "Gazpacho": 0,
    "Panini": 0,
    "Lemon Pie": 0,
    "Candy Apples": 0,
    "Cornbread": 0,
    "Eggs Benedict": 0,
    "Chili Con Carne": 0,
    "Samosas": 0,
    "Fortune Cookies": 0,
    "Pumpkin Gnocchi": 0,
    "Vegetable Terrine": 0,
    "Simmered Vegetables": 0,
    "Lasagna": 0,
    "Mapo Tofu": 0,
    "Korean Barbecue": 0,
    "Tortoiseshell Candy": 0,
    "Salt-Roasted Sweetfish": 0,
    "Tofu Pancakes": 0,
    "Baumkuchen": 0,
    "Vongole Bianco": 0,
    "Instant Ramen": 0,
    "Marshmallows": 0,
    "Cheese Risotto": 0,
    "Pickled Radish": 0,
    "Barbecue Skewer": 0,
    "Instant Stir-fried Noodles": 0,
    "Beefsteak": 0,
    "Mama Bread": 0,
    "Fried Shrimp": 0,
    "Cabbage Rolls": 0,
    "Pizza": 0,
    "Soba Noodles": 0,
    "Minestrone": 0,
    "Sushi": 0,
    "Hamburger": 0,
    "Tempura": 0,
    "French Cruller": 0,
    "Shortcake": 0,
    "Octopus Dumplings": 0,
    "Pickles": 0,
    "Tofu Hamburger": 0,
    "Omelette": 0b000011,
    "Beef Bowl": 0b000101,
    "Salisbury Steak": 0b000110,
    "Savory Egg Custard": 0b001010,
    "Chop Suey": 0b001100,
    "Curry": 0b010100,
    "Potato Salad": 0b010010,
    "Stewed Vegetable Rice Bowl": 0b010001,
    "Fish and Chips": 0b011000,
    "Matsutake Mushroom Rice": 0b100001,
    "Mushroom Quiche": 0b100010,
    "Meatloaf": 0b100100,
    "Fish and Mushrooms in Foil": 0b101000,
    "German Mushroom Potatoes": 0b110000,
    "Rice-Stuffed Squid": 0b001001,
}

RECIPE_LIST = list(RECIPE_BYTE)

#these are fabrications since all the ingredients are unlocked from the start in vanilla, but we need to store the unlocked ones somehow in the randomized game
INGREDIENTS_BYTE = {
    "Rice": 0b000001,
    "Egg": 0b000010,
    "Meat": 0b000100,
    "Seafood": 0b001000,
    "Veggies": 0b010000,
    "Mushrooms": 0b100000,
}

#index * 2 = offset
#16-bit. if upper byte is FF, means "unattempted", otherwise its just the score. 
#lists are the thresholds. these are largely arbitrary so lemme know if they feel off, please
#last part of the list is what special items are required. 0 means none, a binary number corresponds to the correct item
CHALLENGE_BYTE = {
"Break an egg!": [4,8,13, 0],
"Chop it finely!": [1,3,5, 0],
"Peel the skin!": [1,2,4, 0],
"Grill it!": [15,25,40, 0],
"Crack the salt!": [2,4,6, 0],
"Use the slicer!": [20,44,63, 0],
"Open the can!": [2,4,6, 0],
"Roll it into a ball!": [8,15,22, 0],
"Pop it out!": [7,15,24, 0],
"Squeeze it!": [4,8,13, 0],
"Catch the toast!": [9,20,30, 0],
"Boil the noodles!": [2,4,7, 0],
"Hang the squid!": [10,25,45, 0],
"Scoop out the noodles!": [2,4,9, 0],
"Pop the marshmallows out!": [25,46,70, 0],
"Clean the shrimp!": [2,4,8, 0],
"Giant Strawberry!": [5,10,14, 0b0001],
"Star Potatoes!": [17,29,45, 0b0010],
"Ghost Pumpkin!": [5,11,17, 0b0100],
"Golden Apple!": [5,9,13, 0b1000]
}

#for unlocking modes: index = offset
#for the scores: 4 + index * 2 = offset
#scores are largely arbitrary here as well
SHOPPING_BYTE = {
    "Level 1": [300,600,800],
    "Level 2": [500,900,1200],
    "Level 3": [600,1000,1400],
    "Level 4": [800,1500,1800]
}

#list of every goddamn sticker in the game
##these names are all conjecture and may not be super descriptive. i was going for a bit of an Animal Crossing feel with them
##storing these with their specific mem offset plus their respective bit. could probs be done more efficiently but these are kinda a pain in the ass so im ok with taking the easy way out on them
STICKER_FULL = {
   "Frames Sticker Pack": 
        {
         "Empty Frame": [0x0, 0b00000010], #not an item you can ever actually get, but this flag is important for disabling frames after applying them, so they are tracked
         "Wooden Frame": [0x0, 0b00000100],
         "Curtains Frame": [0x0, 0b00001000],
         "Hearts Frame": [0x0, 0b00010000],
         "Bedazzled Frame": [0x0, 0b00100000],
         "Clouds Frame":[0x0, 0b01000000],
         "Flowery Frame":[0x0, 0b10000000],
         "Roses Frame": [0x1, 0b00000001],
         "Striped Frame": [0x1, 0b00000010], 
         "Scrapbook Frame": [0x1, 0b00000100]},
   "Speech Bubble Sticker Pack":
        {"Happy Birthday Speech Bubble":[0x1, 0b00001000], 
         "Happy New Year Speech Bubble": [0x1, 0b00010000], 
         "Merry Christmas Speech Bubble": [0x1, 0b00100000], 
         "Very Good Speech Bubble": [0x1, 0b01000000], 
         "Love & Peace Speech Bubble": [0x1, 0b10000000]},
   "Weather Sticker Pack":
        {"Sunny Weather": [0x2, 0b00000001], 
         "Overcast Weather": [0x2, 0b00000010], 
         "Dark Clouds Weather": [0x2, 0b00000100], 
         "Stormy Weather": [0x2, 0b00001000], 
         "Cloudy Weather": [0x2, 0b00010000]},
   "Eyes Sticker Pack":
        {"Wide Eyes": [0x2, 0b00100000],
         "Angry Eyes": [0x2, 0b01000000], 
         "Dopey Eyes": [0x2, 0b10000000], 
         "Squinting Eyes": [0x3, 0b00000001], 
         "Furious Eyes": [0x3, 0b00000010], 
         "Puppy-dog Eyes": [0x3, 0b00000100], 
         "Heart Eyes": [0x3, 0b00001000], 
         "Wet Eyes": [0x3, 0b00010000],
         "Anime Eyes": [0x3, 0b00100000], 
         "Dizzy Eyes": [0x3, 0b01000000]},
   "Mouths Sticker Pack":
        {"Big Lips": [0x3, 0b10000000], 
         "Wide Grin": [0x4, 0b00000001], 
         "Clenched Teeth": [0x4, 0b00000010], 
         "Vampire Teeth": [0x4, 0b00000100], 
         "Licking Lips": [0x4, 0b00001000], 
         "Dog Nose": [0x4, 0b00010000], 
         "Cat Nose": [0x4, 0b00100000], 
         "Pig Nose": [0x4, 0b01000000], 
         "Shocked Mouth": [0x4, 0b10000000], 
         "Toothy Grin": [0x5, 0b00000001]},
   "Face Accessory Sticker Pack":
        {"Cat Whiskers": [0x5, 0b00000010], 
         "Beard and Mustache": [0x5, 0b00000100], 
         "Classy Mustache": [0x5, 0b00001000], 
         "Swirly Mustache": [0x5, 0b00010000], 
         "Beard": [0x5, 0b00100000]},
   "Head Accessory Sticker Pack":
        {"Cat's Ears": [0x5, 0b01000000], 
         "Devil Horns": [0x5, 0b10000000], 
         "Bunny's Ears": [0x6, 0b00000001], 
         "Oni Horns": [0x6, 0b00000010], 
         "Red Bow": [0x6, 0b00000100], 
         "Ribbons Headband": [0x6, 0b00001000], 
         "Pom-Pom Headband": [0x6, 0b00010000], 
         "Maid's Headband": [0x6, 0b00100000], 
         "Headphones": [0x6, 0b01000000], 
         "Earmuffs": [0x6, 0b10000000]},
   "Friends Sticker Pack":
        {"Happy Mama": [0x7, 0b00000001], 
         "Angry Mama": [0x7, 0b00000010], 
         "Papa": [0x7, 0b00000100], 
         "Grandpa": [0x7, 0b00001000], 
         "Grandma": [0x7, 0b00010000], 
         "Chika": [0x7, 0b00100000], 
         "Ayaka": [0x7, 0b01000000], 
         "Takuya": [0x7, 0b10000000], 
         "David": [0x8, 0b00000001], 
         "Kate": [0x8, 0b00000010]},
   "Sweets Sticker Pack":
        {"Flan": [0x8, 0b00000100], 
         "Ice Cream Scoop": [0x8, 0b00001000], 
         "Birthday Cake": [0x8, 0b00010000], 
         "Sherbet": [0x8, 0b00100000], 
         "Hard Candy": [0x8, 0b01000000], 
         "Lollipop": [0x8, 0b10000000], 
         "Soft Serve": [0x9, 0b00000001], 
         "Cheesecake": [0x9, 0b00000010], 
         "Cruller": [0x9, 0b00000100], 
         "Chocolate": [0x9, 0b00001000]},
   "Drinks Sticker Pack":
        {"Orange Juice": [0x9, 0b00010000], 
         "Wine": [0x9, 0b00100000], 
         "Tropical Drink": [0x9, 0b01000000], 
         "Pawprint Mug": [0x9, 0b10000000], 
         "Cherry Blossom Mug": [0xA, 0b00000001]},
   "Fruits n' Veggies Sticker Pack":
        {"Tomato": [0xA, 0b00000010], 
         "Eggplant": [0xA, 0b00000100], 
         "Potato": [0xA, 0b00001000], 
         "Bell Pepper": [0xA, 0b00010000], 
         "Carrot": [0xA, 0b00100000], 
         "Melon": [0xA, 0b01000000], 
         "Apple": [0xA, 0b10000000], 
         "Orange": [0xB, 0b00000001], 
         "Grape": [0xB, 0b00000010], 
         "Strawberry": [0xB, 0b00000100]},
   "Glasses Sticker Pack":
        {"Business Glasses": [0xB, 0b00001000], 
         "Aviator Shades": [0xB, 0b00010000], 
         "Dizzy Glasses": [0xB, 0b00100000], 
         "Vibrant Mask": [0xB, 0b01000000], 
         "Big Goggles": [0xB, 0b10000000], 
         "Groucho Glasses": [0xC, 0b00000001], 
         "Diving Gear": [0xC, 0b00000010], 
         "Heart Shades": [0xC, 0b00000100], 
         "No-Frames Glasses": [0xC, 0b00001000], 
         "Smart Glasses": [0xC, 0b00010000]},
   "Hats Sticker Pack":
        {"Green Hat": [0xC, 0b00100000], 
         "Top Hat": [0xC, 0b01000000], 
         "Chef's Hat": [0xC, 0b10000000], 
         "Summer Hat": [0xD, 0b00000001], 
         "Wizard Hat": [0xD, 0b00000010], 
         "Fancy Hat": [0xD, 0b00000100], 
         "Cowboy Hat": [0xD, 0b00001000], 
         "Sumo Headband": [0xD, 0b00010000], 
         "Party Hat": [0xD, 0b00100000], 
         "Crown": [0xD, 0b01000000]},
   "Celebration Sticker Pack":
        {"Balloon": [0xD, 0b10000000], 
         "Party Popper": [0xE, 0b00000001], 
         "Party Ball": [0xE, 0b00000010], 
         "Cute Ghost": [0xE, 0b00000100], 
         "Jack O' Lantern": [0xE, 0b00001000], 
         "Gourd": [0xE, 0b00010000], 
         "Pink Present": [0xE, 0b00100000], 
         "Celebratory Candle": [0xE, 0b01000000], 
         "Plain Egg": [0xE, 0b10000000], 
         "Splotchy Egg": [0xF, 0b00000001]},
   "Emoji Sticker Pack":
        {"Happy Face": [0xF, 0b00000010], 
         "Sad Face": [0xF, 0b00000100], 
         "Flushed Face": [0xF, 0b00001000], 
         "Pensive Face": [0xF, 0b00010000], 
         "Angry Face": [0xF, 0b00100000]},
   "Animals Sticker Pack":
        {"Puppy": [0xF, 0b01000000], 
         "Kitty": [0xF, 0b10000000], 
         "Bunny": [0x10, 0b00000001], 
         "Hamster": [0x10, 0b00000010], 
         "Bat": [0x10, 0b00000100], 
         "Frog": [0x10, 0b00001000], 
         "Butterfly": [0x10, 0b00010000], 
         "Bee": [0x10, 0b00100000], 
         "Caterpillar": [0x10, 0b01000000], 
         "Fish": [0x10, 0b10000000]},
   "Festive Sticker Pack":
        {"Christmas Tree": [0x11, 0b00000001], 
         "Snowman": [0x11, 0b00000010], 
         "Santa Hat": [0x11, 0b00000100], 
         "Santa Centerpiece": [0x11, 0b00001000], 
         "Festive Lights": [0x11, 0b00010000]},
   "Garland Sticker Pack":
        {"Flowery Garland": [0x11, 0b00100000], 
         "Colorful Garland": [0x11, 0b01000000], 
         "Starry Garland": [0x11, 0b10000000], 
         "Ribbon Garland": [0x12, 0b00000001], 
         "Beautiful Garland": [0x12, 0b00000010]},
   "Household Items Sticker Pack":
        {"Alarm Clock": [0x12, 0b00000100],
         "Parasol": [0x12, 0b00001000],
         "Lightbulb": [0x12, 0b00010000], 
         "Grandfather Clock": [0x12, 0b00100000], 
         "Thermometer": [0x12, 0b01000000], 
         "Pinwheel": [0x12, 0b10000000], 
         "Uchiwa Fan": [0x13, 0b00000001], 
         "Teru Teru Bozu": [0x13, 0b00000010], 
         "Toothbrush and Cup": [0x13, 0b00000100], 
         "Baby Rattle": [0x13, 0b00001000]},
   "Kitchenware Sticker Pack":
        {"Kitchen Pot": [0x13, 0b00010000], 
         "Blender": [0x13, 0b00100000], 
         "Kettle": [0x13, 0b01000000], 
         "Toaster": [0x13, 0b10000000], 
         "Cutlery": [0x14, 0b00000001]},
   "Emotions Sticker Pack":
        {"Sweatdrops": [0x14, 0b00000010], 
         "Floating Hearts": [0x14, 0b00000100], 
         "Musical Note": [0x14, 0b00001000], 
         "Question Mark": [0x14, 0b00010000], 
         "Exclamation Mark": [0x14, 0b00100000]},
   "Hands Sticker Pack":
        {"Dog Paws": [0x14, 0b01000000], 
         "Cat Paws": [0x14, 0b10000000], 
         "Peace Sign": [0x15, 0b00000001], 
         "Open Hand": [0x15, 0b00000010],
         "Thumbs Up": [0x15, 0b00000100]},
   "Bedazzled Sticker Pack":
        {"Gemstone Heart": [0x15, 0b00001000],
         "Diamond": [0x15, 0b00010000], 
         "Gemstone Crescent": [0x15, 0b00100000], 
         "Gemstone Star": [0x15, 0b01000000], 
         "Assorted Gemstones": [0x15, 0b10000000]},
   "Flowery Sticker Pack":
        {"Tulip": [0x16, 0b00000001], 
         "Rose": [0x16, 0b00000010], 
         "Daisy": [0x16, 0b00000100], 
         "Sunflower": [0x16, 0b00001000], 
         "Pansy": [0x16, 0b00010000], 
         "Sapling": [0x16, 0b00100000], 
         "Flower Bush": [0x16, 0b01000000], 
         "Pink Bouquet": [0x16, 0b10000000], 
         "Colorful Bouquet": [0x17, 0b00000001], 
         "Warm Bouquet": [0x17, 0b00000010]},
   "Neckwear Sticker Pack":
        {"Scarf": [0x17, 0b00000100], 
         "Necklace": [0x17, 0b00001000], 
         "Tie": [0x17, 0b00010000], 
         "Handkerchief": [0x17, 0b00100000], 
         "Bandana": [0x17, 0b01000000]},
   "Toys Sticker Pack":
        {"Wind-up Car": [0x17, 0b10000000], 
         "Dolly": [0x18, 0b00000001], 
         "Toyboat": [0x18, 0b00000010], 
         "Hot Air Balloon": [0x18, 0b00000100], 
         "Teddy Bear": [0x18, 0b00001000]},
   "Crayon Sticker Pack":
        {"Red Crayon": [0x18, 0b00010000], 
         "Blue Crayon": [0x18, 0b00100000], 
         "Yellow Crayon": [0x18, 0b01000000], 
         "Green Crayon": [0x18, 0b10000000], 
         "Pink Crayon": [0x19, 0b00000001]},
}

###Accessories and Accessory Packs###
ACCESSORY_FULL = {
   "Apron Clothing Set":
        {"Yellow Apron": [0x0, 0b00000001], 
         "Blue Apron": [0x0, 0b00000010], 
         "Red Apron": [0x0, 0b00000100], 
         "Green Apron": [0x0, 0b00001000], 
         "Black Apron": [0x0, 0b00010000]},
   "Overalls Clothing Set":
        {"Blue Overalls": [0x0, 0b00100000], 
         "Pink Overalls": [0x0, 0b01000000], 
         "Yellow Overalls": [0x0, 0b10000000], 
         "Green Overalls": [0x1, 0b00000001], 
         "Black Overalls": [0x1, 0b00000010]},
   "Blouse Clothing Set":
        {"Yellow Blouse": [0x1, 0b00000100], 
         "Red Blouse": [0x1, 0b00001000], 
         "Black Blouse": [0x1, 0b00010000], 
         "Green Blouse": [0x1, 0b00100000], 
         "Pink Blouse": [0x1, 0b01000000]},
   "Dotted Dress Clothing Set":
        {"Pink Dotted Dress": [0x1, 0b10000000], 
         "Green Dotted Dress": [0x2, 0b00000001], 
         "Yellow Dotted Dress": [0x2, 0b00000010], 
         "Blue Dotted Dress": [0x2, 0b00000100], 
         "Brown Dotted Dress": [0x2, 0b00001000]},
   "Yukata Clothing Set":
        {"Red Yukata": [0x2, 0b00010000], 
         "Blue Yukata": [0x2, 0b00100000], 
         "Yellow Yukata": [0x2, 0b01000000], 
         "Green Yukata": [0x2, 0b10000000], 
         "Navy Yukata": [0x3, 0b00000001]},
   "Country Dress Clothing Set":
        {"Red/Green Country Dress": [0x3, 0b00000010], 
         "Blue/Pink Country Dress": [0x3, 0b00000100], 
         "Green/Blue Country Dress": [0x3, 0b00001000], 
         "Pink/Yellow Country Dress": [0x3, 0b00010000], 
         "Orange/Blue Country Dress": [0x3, 0b00100000]},
   "Fluffy Gown Clothing Set":
        {"Blue Fluffy Gown": [0x3, 0b01000000], 
         "Red Fluffy Gown": [0x3, 0b10000000], 
         "Yellow Fluffy Gown": [0x4, 0b00000001], 
         "Green Fluffy Gown": [0x4, 0b00000010], 
         "Purple Fluffy Gown": [0x4, 0b00000100]},
   "Formal Clothing Set":
        {"Blue/Green Formal Clothing Set": [0x4, 0b00001000], 
         "Red Formal Clothing Set": [0x4, 0b00010000], 
         "Yellow Formal Clothing Set": [0x4, 0b00100000], 
         "Blue Formal Clothing Set": [0x4, 0b01000000], 
         "Purple Clothing Set": [0x4, 0b10000000]},
   "Kimono Clothing Set":
        {"Red Kimono": [0x5, 0b00000001], 
         "Yellow Kimono": [0x5, 0b00000010], 
         "Blue Kimono": [0x5, 0b00000100], 
         "Green Kimono": [0x5, 0b00001000], 
         "Black Kimono": [0x5, 0b00010000]},
   "Maid Outfit Clothing Set":
        {"Black Maid Outfit": [0x5, 0b00100000], 
         "Blue Maid Outfit": [0x5, 0b01000000], 
         "Green Maid Outfit": [0x5, 0b10000000], 
         "Red Maid Outfit": [0x6, 0b00000001], 
         "Yellow Maid Outfit": [0x6, 0b00000010]},
   "Festive Outfit Clothing Set":
        {"Festive Outfit Set": [0x6, 0b01111100]}, #INEXPLICABLY, the outfits from this particular set requires that every previous festive outfit be unlocked. im too tired to deal with this so im just gonna make it a set no matter what
   "Glasses Set": 
        {"No Glasses": [0x6, 0b10000000],
         "Frameless Glasses": [0x7, 0b00000001], 
         "Red Triangular Glasses": [0x7, 0b00000010], 
         "Full Moon Glasses": [0x7, 0b00000100], 
         "Pink Shades": [0x7, 0b00001000], 
         "Yellow Triangular Glasses": [0x7, 0b00010000], 
         "Yellow Shades": [0x7, 0b00100000], 
         "Star Glasses": [0x7, 0b01000000], 
         "Reading Glasses": [0x7, 0b10000000], 
         "Swirly Glasses": [0x8, 0b00000001]},
   "Earrings Set":
        {"No Earrings": [0x8, 0b00000010],
         "Moon Earrings": [0x8, 0b00000100], 
         "Flower Earrings": [0x8, 0b00001000], 
         "Dewdrop Earrings": [0x8, 0b00010000], 
         "Mysterious Earrings": [0x8, 0b00100000]},
   "Hat Set":
        {"No Hat": [0x8, 0b01000000], 
         "Maid Headband": [0x8, 0b10000000], 
         "Cat Ears": [0x9, 0b00000001], 
         "Regal Crown": [0x9, 0b00000010], 
         "Bunny Ears": [0x9, 0b00000100],
         "Chef Hat": [0x9, 0b00001000], 
         "Blue Headband": [0x9, 0b00010000], 
         "Bowtie Headband": [0x9, 0b00100000], 
         "Flower Crown": [0x9, 0b01000000], 
         "Hearts Headband": [0x9, 0b10000000]},
   "Headgear Set":
        {"No Headgear": [0xA, 0b00000001], 
         "Green Bows": [0xA, 0b00000010], 
         "Hibiscus Hairpiece": [0xA, 0b00000100], 
         "Shades on Forehead": [0xA, 0b00001000], 
         "Tiara": [0xA, 0b00010000]},
    "Bandana Set":
        {"Pink Bandana": [0xA, 0b00100000], 
         "Yellow Bandana": [0xA, 0b01000000], 
         "Blue Bandana": [0xA, 0b10000000], 
         "Red Bandana": [0xB, 0b00000001], 
         "Green Bandana": [0xB, 0b00000010]},
}

KITCHEN_FULL = {
    #note that it seems like one wallpaper must be unlocked before clocks and gauges show up
    ##im once again too tired to deal with this, so im making them all one set. in individual accessory mode, youll get one wallpaper as a freebie
   "Top Screen Deco Set":
        {"Blue Tiles Wallpaper": [0xB, 0b00000100], 
         "Carrots Wallpaper": [0xB, 0b00001000], 
         "Stars and Clouds Wallpaper": [0xB, 0b00010000], 
         "Checkered Hearts Wallpaper": [0xB, 0b00100000], 
         "Striped Wallpaper": [0xB, 0b01000000], 
         "Frilly Roses Wallpaper": [0xB, 0b10000000], 
         "Blue Spotlights Wallpaper": [0xC, 0b00000001], 
         "Pink Sparkling Wallpaper": [0xC, 0b00000010], 
         "Daisies Wallpaper": [0xC, 0b00000100], 
         "Nighttime Sparkling Wallpaper": [0xC, 0b00001000], 
         "Garden Window Wallpaper": [0xC, 0b00010000], 
         "Sauna Wallpaper": [0xC, 0b00100000], 
         "Tatami Room Wallpaper": [0xC, 0b01000000], 
         "Cityscape Wallpaper": [0xC, 0b10000000], 
         "Beachside Wallpaper": [0xD, 0b00000001], 
         "Festive Wallpaper": [0xD, 0b00000010],
        "Gingham Clock": [0xD, 0b00000100], 
         "Citrus Clock": [0xD, 0b00001000], 
         "Plate Clock": [0xD, 0b00010000], 
         "Cookie Clock": [0xD, 0b00100000], 
         "Kiwi Clock": [0xD, 0b01000000],
        "Yellow Gauge": [0xD, 0b10000000], 
         "Pink Gauge": [0xE, 0b00000001], 
         "Blue Gauge": [0xE, 0b00000010], 
         "Green Gauge": [0xE, 0b00000100], 
         "Purple Gauge": [0xE, 0b00001000]},
   "Skillet Set":
        {"Yellow Skillet": [0xE, 0b00010000], 
         "Red Skillet": [0xE, 0b00100000], 
         "Blue Skillet": [0xE, 0b01000000], 
         "Green Skillet": [0xE, 0b10000000], 
         "Pink Skillet": [0xF, 0b00000001]},
   "Pot Set":
        {"Yellow Pot": [0xF, 0b00000010], 
         "Red Pot": [0xF, 0b00000100], 
         "Blue Pot": [0xF, 0b00001000], 
         "Green Pot": [0xF, 0b00010000], 
         "Pink Pot": [0xF, 0b00100000]},
   "Knife Set":
        {"Blue Knife": [0xF, 0b01000000], 
         "Red Knife": [0xF, 0b10000000], 
         "Orange Knife": [0x10, 0b00000001], 
         "Yellow Knife": [0x10, 0b00000010], 
         "Green Knife": [0x10, 0b00000100]},
   "Cutting Board Set":
        {"Blue Cutting Board": [0x10, 0b00001000], 
         "Pink Cutting Board": [0x10, 0b00010000], 
         "Yellow Cutting Board": [0x10, 0b00100000], 
         "Green Cutting Board": [0x10, 0b01000000], 
         "Black Cutting Board": [0x10, 0b10000000]},
   "Meat Grinder Set":
        {"Orange Meat Grinder": [0x11, 0b00000001], 
         "Red Meat Grinder": [0x11, 0b00000010], 
         "Blue Meat Grinder": [0x11, 0b00000100], 
         "Yellow Meat Grinder": [0x11, 0b00001000], 
         "Green Meat Grinder": [0x11, 0b00010000]},
   "Veggie Peeler Set":
        {"Blue Veggie Peeler": [0x11, 0b00100000], 
         "Pink Veggie Peeler": [0x11, 0b01000000], 
         "Red Veggie Peeler": [0x11, 0b10000000], 
         "Yellow Veggie Peeler": [0x12, 0b00000001], 
         "Green Veggie Peeler": [0x12, 0b00000010]},
   "Oven Set":
        {"Blue Oven": [0x12, 0b00000100], 
         "Red Oven": [0x12, 0b00001000], 
         "Orange Oven": [0x12, 0b00010000], 
         "Yellow Oven": [0x12, 0b00100000],
         "Green Oven": [0x12, 0b01000000]},
   "Hand Mixer Set":
        {"Blue Hand Mixer": [0x12, 0b10000000], 
         "Red Hand Mixer": [0x13, 0b00000001], 
         "Orange Hand Mixer": [0x13, 0b00000010], 
         "Yellow Hand Mixer": [0x13, 0b00000100], 
         "Green Hand Mixer": [0x13, 0b00001000]},
   "Veggie Slicer Set":
        {"Blue Veggie Slicer": [0x13, 0b00010000], 
         "Red Veggie Slicer": [0x13, 0b00100000], 
         "Orange Veggie Slicer": [0x13, 0b01000000], 
         "Yellow Veggie Slicer": [0x13, 0b10000000], 
         "Green Veggie Slicer": [0x14, 0b00000001]},
   "Blender Set":
        {"Blue Blender": [0x14, 0b00000010], 
         "Red Blender": [0x14, 0b00000100], 
         "Orange Blender": [0x14, 0b00001000], 
         "Yellow Blender": [0x14, 0b00010000], 
         "Green Blender": [0x14, 0b00100000]},
   "Kitchen Counter Set":
        {"Yellow Kitchen Counters": [0x14, 0b01000000], 
         "Pink Kitchen Counters": [0x14, 0b10000000], 
         "Blue Kitchen Counters": [0x15, 0b00000001], 
         "Green Kitchen Counters": [0x15, 0b00000010], 
         "Black Kitchen Counters": [0x15, 0b00000100]},
   "Stove Set": #ngl i dont know what this one is even supposed to be. lemme know if its wrong
        {"Blue Stove": [0x15, 0b00001000], 
         "Pink Stove": [0x15, 0b00010000], 
         "Green Stove": [0x15, 0b00100000], 
         "Orange Stove": [0x15, 0b01000000], 
         "Lime Stove": [0x15, 0b10000000]},
   "Sink Set":
        {"Blue Sink": [0x16, 0b00000001], 
         "Pink Sink": [0x16, 0b00000010], 
         "Yellow Sink": [0x16, 0b00000100], 
         "Green Sink": [0x16, 0b00001000], 
         "Black Sink": [0x16, 0b00010000]},
}

ALL_ACCESSORY = {
    **STICKER_FULL, 
    **ACCESSORY_FULL, 
    **KITCHEN_FULL}

ALL_STICKER = {
    key: value
    for item in STICKER_FULL.values()
    for key, value in item.items()
}

ALL_CLOTHING = {
    key: value
    for item in ACCESSORY_FULL.values()
    for key, value in item.items()
}