from utils.pg import pg
from classes.Game import Game
from classes.CameraGroup import CameraGroup

class Ground(pg.sprite.Sprite):
    def __init__(self, game : Game, pos: (), camera_group : CameraGroup, image : pg.image) -> None:
        super().__init__(camera_group)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.x = pos[0] * self.game.tile_size
        self.y = pos[1] * self.game.tile_size
        self.width, self.height = self.game.tile_size, self.game.tile_size
        pg.sprite.Sprite.__init__(self, self.game.ground_sprites)