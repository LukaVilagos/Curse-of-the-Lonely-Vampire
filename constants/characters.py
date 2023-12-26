from classes.Character import Character
from constants.inventories import VAMPIRE_INVENTORY
from constants.items import BASIC_SWORD
from constants.images import player_img

CHARACTER = Character(player_img, "Bob", 13, "M", "Warrior", VAMPIRE_INVENTORY)
CHARACTER.equipped = BASIC_SWORD