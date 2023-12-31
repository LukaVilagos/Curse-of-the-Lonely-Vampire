from utils.pg import pg
from enums.Colors import Colors

screen = pg.display.set_mode((1280, 720), pg.SCALED)

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((Colors.BLACK.value))