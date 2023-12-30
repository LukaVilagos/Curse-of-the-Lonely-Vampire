from utils.pg import pg
from classes.Player import Player

class Healthbar(pg.sprite.Sprite):
    def __init__(self, game, player : Player):
        self.game = game
        self.player = player
        self.text = f"{self.player.health_points}/{self.player.character.health_points}"
        pg.draw(self.game.screen, "CC0000", (10, 10, 300 * (self.player.health_points / 100), 60))