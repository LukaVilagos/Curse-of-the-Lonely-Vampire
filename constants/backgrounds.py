from utils.pg import pg

screen = pg.display.set_mode((1280,720), pg.SCALED)

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill(('#000000'))