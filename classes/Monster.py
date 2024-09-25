from utils.pg import pg
from classes.Inventory import Inventory

class Monster:
    def __init__(self, image : pg.image, name: str, description: str, health_points: int, loot: Inventory) -> None:
        self.image = image
        self.name = name
        self.description = description
        self.health_points = health_points
        self.loot = loot
        self.speed = 2
        self.equipped = None