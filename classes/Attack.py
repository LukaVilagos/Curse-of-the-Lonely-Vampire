from utils.pg import pg
from classes.Game import Game
from classes.CameraGroup import CameraGroup

class Attack(pg.sprite.Sprite):
    def __init__(self, game : Game, group : CameraGroup, weapon, player, target) -> None:
        super().__init__(group)
        self.weapon = weapon
        self.player = player
        self.target = target
        pg.sprite.Sprite.__init__(self, self.game.player_sprites)