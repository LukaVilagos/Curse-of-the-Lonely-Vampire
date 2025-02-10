from utils.pg import pg
from utils.build_map import build_map
from config.keybinds import *
from classes.CameraGroup import CameraGroup
from classes.Healthbar import Healthbar
from constants.backgrounds import background
from constants.fonts import font
from enums.Colors import Colors

class Play:
    def __init__(self, game, tilemap : list) -> None:
        self.game = game
        self.tilemap = tilemap
        self.player = None
        self.create_tilemap()
        self.camera = CameraGroup(self.game)
        self.healthbar = Healthbar(self.game, self.player)
        
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
        self.camera.draw(self.player)
        self.healthbar.draw()
        if len(self.game.enemy_sprites) < 1:
            background.fill((Colors.BLACK.value))
            self.game.screen.blit(background, (0,0))
            heading = font.render("You Win", True, Colors.WHITE.value)
            headingpos = heading.get_rect(centerx=background.get_width() / 2, y=100)
            self.game.screen.blit(heading, headingpos)
        
    def create_tilemap(self) -> None:
        build_map(self)