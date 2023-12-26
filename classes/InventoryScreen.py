from utils.pg import pg
from constants.backgrounds import background
from config.keybinds import *

class InventoryScreen():
    def __init__(self, game):
        self.game = game
        
    def run_inventory(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.exit_game()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.pause_game()
                if event.key == INVENTORY_KEY:
                    self.game.start_game()
                
    def draw_inventory(self):
        self.game.screen.blit(background, (0,0))