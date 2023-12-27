from utils.pg import pg
from utils.build_map import build_map
from config.keybinds import *
from classes.CameraGroup import CameraGroup

class Play:
    def __init__(self, game, tilemap : [], camera : CameraGroup) -> None:
        self.game = game
        self.tilemap = tilemap
        self.camera = camera
        self.player = None
        self.create_tilemap()
        
    def run_play(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.exit_game()
            if event.type == pg.KEYDOWN:
                if event.key == INVENTORY_KEY:
                    self.game.show_inventory()
                if event.key == pg.K_ESCAPE:
                    self.game.pause_game()
                    
    def draw_play(self) -> None:
        self.player.custom_update()
        self.camera.draw(self.player)
        
    def create_tilemap(self) -> None:
        build_map(self)