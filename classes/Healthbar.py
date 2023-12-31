from utils.pg import pg
from classes.Player import Player
from enums.Colors import Colors

class Healthbar(pg.sprite.Sprite):
    def __init__(self, game, player : Player) -> None:
        self.game = game
        self.player = player
        self.text = f"{self.player.health_points}/{self.player.character.health_points}"
    
    def draw(self) -> None:
        pg.draw.rect(self.game.screen, Colors.GRAY.value, (10, 10, 300, 30))
        pg.draw.rect(self.game.screen, Colors.RED.value, (10, 10, 300 * (self.player.health_points / self.player.character.health_points), 30))
        pg.draw.rect(self.game.screen, Colors.GRAY.value, (10, 40, 200, 15))
        pg.draw.rect(self.game.screen, Colors.BLUE.value, (10, 40, 200 * (self.player.stamina / self.player.character.stamina), 15))