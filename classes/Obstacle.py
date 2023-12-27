from utils.pg import pg
from classes.CameraGroup import CameraGroup

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, pos : (), camera_group : CameraGroup, image) -> None:
        self.game = game
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.x = pos[0] * self.game.tile_size
        self.y = pos[1] * self.game.tile_size
        self.width, self.height = self.game.tile_size, self.game.tile_size
        super().__init__(camera_group, self.game.obstacle_sprites)