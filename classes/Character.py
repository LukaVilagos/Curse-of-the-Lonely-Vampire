from classes.Inventory import Inventory
from utils.pg import pg

def health_point_calc(charcter_class : str):
    match charcter_class:
        case "Fighter":
            return 10
        case "Wizard":
            return 5
        case "Cleric":
            return 8


class Character:
    def __init__(self, image : pg.image, name: str, age: int, gender: str, charcter_class: str, inventory: Inventory) -> None:
        self.image = image
        self.name = name
        self.age = age
        self.gender = gender
        self.charcter_class = charcter_class
        self.experiance_points = 0
        self.health_points = health_point_calc(charcter_class)
        self.speed = 5
        self.weight = 100
        self.endurance = 500
        self.inventory = inventory
        self.equipped = False
        self.last = pg.time.get_ticks()
