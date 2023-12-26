from utils.pg import pg
from classes.Inventory import Inventory

class Monster:
    def __init__(self, image, name: str, description: str, health_points: int, loot: Inventory):
        self.image = image
        self.name = name
        self.description = description
        self.health_points = health_points
        self.loot = loot
        self.speed = 5
        self.equipped = None
        
    def reduce_health_points(self, enemy, value):
        if self.health_points > 1 and enemy.alive:
            self.health_points -= value
        else:
            enemy.die()