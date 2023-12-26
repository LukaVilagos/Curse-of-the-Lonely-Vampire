from utils.pg import pg
from constants.backgrounds import background

class Options:
    def __init__(self, game) -> None:
        self.game = game
        
    def run_options(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.exit_game()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.pause_game()
                
    def draw_options(self) -> None:
        self.game.screen.blit(background, (0,0))