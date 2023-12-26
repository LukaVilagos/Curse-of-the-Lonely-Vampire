from utils.pg import pg
from constants.backgrounds import background

class Options:
    def __init__(self, game):
        self.game = game
        
    def run_options(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.exit_game()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.pause_game()
                
    def draw_options(self):
        self.game.screen.blit(background, (0,0))