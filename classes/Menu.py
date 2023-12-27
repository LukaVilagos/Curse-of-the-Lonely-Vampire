from utils.pg import pg
from constants.backgrounds import background
from constants.fonts import font
from enums.Colors import Colors
from classes.MenuItem import MenuItem
from constants.images import start_button_img, options_button_img, exit_button_img
from utils.center_image import center_image_vertically

class Menu:
    def __init__(self, game) -> None:
        self.game = game
        self.start_button = MenuItem(game, center_image_vertically(start_button_img, 1.2), 200, start_button_img, 1.2)
        self.options_button = MenuItem(game ,center_image_vertically(options_button_img, 1), 350, options_button_img)
        self.exit_button = MenuItem(game, center_image_vertically(exit_button_img, 1), 500, exit_button_img)

    def run_menu(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.exit_game()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.exit_game()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.start_button.click():
                    self.game.start_game()
                if self.options_button.click(): 
                    self.game.show_options()
                if self.exit_button.click(): 
                    self.game.exit_game()

    def draw_menu(self) -> None:
        self.game.screen.blit(background, (0,0))
        heading = font.render("Curse of the Lonely Vampire", True, Colors.WHITE.value)
        headingpos = heading.get_rect(centerx=background.get_width() / 2, y=100)
        self.game.screen.blit(heading, headingpos)
        
        self.start_button.draw()
        self.options_button.draw()
        self.exit_button.draw()
        
        pg.display.update()