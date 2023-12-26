from classes.Inventory import Inventory
from classes.Item import Item

def health_point_calc(charcter_class):
    match charcter_class:
        case "Fighter":
            return 10
        case "Wizard":
            return 5
        case "Cleric":
            return 8


class Character:
    def __init__(self, image, name: str, age: int, gender: str, charcter_class: str, inventory: Inventory):
        self.image = image
        self.name = name
        self.age = age
        self.gender = gender
        self.charcter_class = charcter_class
        self.experiance_points = 0
        self.health_points_max = health_point_calc(charcter_class)
        self.health_points = self.health_points_max
        self.speed = 5
        self.inventory = inventory
        self.equipped = False
