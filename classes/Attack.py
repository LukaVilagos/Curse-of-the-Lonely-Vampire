from utils.pg import pg
from random import randint

class Attack(pg.sprite.Sprite):
    def __init__(self, game, camera_group, weapon, pos) -> None:
        super().__init__(camera_group)
        self.game = game
        self.camera_group = camera_group
        self.weapon = weapon
        self.image = self.weapon.image
        self.rect = self.image.get_rect(topleft = pos)
        self.random = randint(0,1000)
        pg.sprite.Sprite.__init__(self, self.game.player_sprites)
        
    def update(self) -> None:
        print(f"Here {self.random}")
        if self.alive():
            self.collide()
            self.kill()
            del self
        
    def collide(self) -> None:
        hits = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        if hits:
            for sprite in hits:
                sprite.reduce_health_points(self.weapon.damage)