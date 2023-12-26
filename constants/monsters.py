from classes.Monster import Monster
from constants.inventories import VAMPIRE_INVENTORY
from constants.items import BASIC_SWORD
from constants.images import monster_img
  
VAMPIRE = Monster(monster_img, "Vampire", "It's spooky", 10, VAMPIRE_INVENTORY)
VAMPIRE.equipped = BASIC_SWORD