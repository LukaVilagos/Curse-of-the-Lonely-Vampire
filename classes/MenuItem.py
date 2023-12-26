from utils.pg import pg

class MenuItem:
    def __init__(self, game, x: int, y: int, image : pg.image, scale = 1) -> None:
        self.game = game
        witdth = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(witdth * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def draw(self) -> None:
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def click(self) -> None:
        pos = pg.mouse.get_pos()
        return pos[1] in range(self.rect.top,self.rect.bottom) and pos[0] in range(self.rect.left, self.rect.right)