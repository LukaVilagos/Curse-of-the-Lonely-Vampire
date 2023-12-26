from classes.Obstacle import Obstacle
from classes.Ground import Ground
from classes.Player import Player
from classes.Enemy import Enemy
from utils.get_sprite_pos import get_sprite_pos
from constants.images import ground_tile, wall_tile, box_tile
from constants.monsters import VAMPIRE
from constants.characters import CHARACTER

def build_map(self) -> None:
    for i, row in enumerate(self.tilemap):
        for j, column in enumerate(row):
            Ground(self.game, get_sprite_pos(j, i, self.game.tile_size), self.camera, ground_tile)
            if column == "W":
                Obstacle(self.game, get_sprite_pos(j ,i, self.game.tile_size), self.camera, wall_tile)
            elif column == "B":
                Obstacle(self.game, (get_sprite_pos(j, i, self.game.tile_size)[0] + 18, get_sprite_pos(j, i, self.game.tile_size)[1] + 6), self.camera, box_tile)
            elif column == 'E':
                self.enemies.append(Enemy(self.game, get_sprite_pos(j,i,self.game.tile_size), VAMPIRE, self.camera, 2))
            elif column == 'P':
                self.player = Player(self.game, get_sprite_pos(j,i,self.game.tile_size), CHARACTER, self.camera)