import sys
from utils.pg import pg
from constants.stages import STAGE_1
from classes.Game import Game
from classes.Menu import Menu
from classes.Play import Play
from classes.InventoryScreen import InventoryScreen
from classes.Options import Options

def main():
    game = Game()
    menu = Menu(game)
    play = Play(game, STAGE_1)
    inventory_screen = InventoryScreen(game)
    options = Options(game)

    while game.running:
        game.main(menu, play, inventory_screen, options)

    pg.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()