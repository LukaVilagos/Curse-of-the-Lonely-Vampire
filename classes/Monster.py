from utils.pg import pg
from classes.Inventory import Inventory

class Monster:
    def __init__(self, image : pg.image, name: str, description: str, health_points: int, loot: Inventory, width = 32, height = 64) -> None:
        self.image = image
        self.width = width
        self.height = height
        
        self.name = name
        self.description = description
        self.health_points = health_points
        self.loot = loot
        self.speed = 2
        self.equipped = None
        