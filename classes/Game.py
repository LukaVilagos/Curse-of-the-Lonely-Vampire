from utils.pg import pg
from classes.Menu import Menu
from classes.Play import Play
from classes.InventoryScreen import InventoryScreen
from classes.Options import Options

class Game:
    def __init__(self) -> None:
        self.screen_width = 1280
        self.scree_height = 720
        self.fps = 60
        self.tile_size = 64
        self.screen = pg.display.set_mode((self.screen_width, self.scree_height), pg.SCALED)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.menu = True
        self.play = False
        self.inventory = False
        self.options = False
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.obstacle_sprites = pg.sprite.Group()
        self.ground_sprites = pg.sprite.Group()
        
    def events(self, menu : Menu, play : Play, inventory_screen : InventoryScreen, options : Options) -> None:
        if self.menu:
            menu.run_menu()
        elif self.play:
            play.run_play()
        elif self.inventory:
            inventory_screen.run_inventory()
        elif self.options:
            options.run_options()
            
    def update(self):
        self.all_sprites.update()
        
    def draw(self, menu : Menu, play : Play, inventory_screen : InventoryScreen, options : Options) -> None:
        self.clock.tick(self.fps)  
           
        if self.menu:
            menu.draw_menu()
        elif self.play:
            play.draw_play()
        elif self.inventory:
            inventory_screen.draw_inventory()
        elif self.options:
            options.draw_options()
            
        pg.display.update()
        
    def main(self, menu : Menu, play : Play, inventory_screen : InventoryScreen, options : Options)-> None:
        while self.running:
            self.events(menu, play, inventory_screen, options)
            self.update()
            self.draw(menu, play, inventory_screen, options)
                           
    def pause_game(self) -> None:
        self.menu = True
        
    def start_game(self) -> None:
        self.menu = False
        self.play = True
        self.inventory = False
        self.options = False
        
    def show_options(self) -> None:
        self.menu = False
        self.play = False
        self.inventory = False
        self.options = True
        
    def show_inventory(self) -> None:
        self.menu = False
        self.play = False
        self.inventory = True
        self.options = False
        
    def exit_game(self) -> None:
        self.playing = False
        self.running = False