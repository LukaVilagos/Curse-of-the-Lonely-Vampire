from utils.pg import pg
from classes.Monster import Monster
from constants.images import exit_button_img

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos: (), monster : Monster, camera_group,scale = 1):
        super().__init__(camera_group)
        self.game = game
        self.monster = monster
        self.x = pos[0]
        self.y = pos[1]
        self.scale = scale
        witdth = self.monster.image.get_width()
        height = self.monster.image.get_height()
        self.image = pg.transform.scale(self.monster.image, (int(witdth * self.scale), int(height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.velX = 0
        self.velY = 0
        self.alive = True
        pg.sprite.Sprite.__init__(self, self.game.enemy_sprites)
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def die(self):
        self.alive = False
        witdth = exit_button_img.get_width()
        height = exit_button_img.get_height()
        self.image = pg.transform.scale(exit_button_img, (int(witdth * self.scale), int(height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)