from utils.pg import pg
from random import randint
from classes.CameraGroup import CameraGroup
from classes.Item import Item

class Attack(pg.sprite.Sprite):
    def __init__(self, game, camera_group : CameraGroup, weapon : Item, pos : ()) -> None:
        super().__init__(camera_group)
        self.game = game
        self.camera_group = camera_group
        self.weapon = weapon
        
        self.image = self.weapon.image
        self.rect = self.image.get_rect(topleft = pos)
        
        self.hit = False
        self.lifespan = 300
        self.last = pg.time.get_ticks()
        
        self.random = randint(0,1000)
        pg.sprite.Sprite.__init__(self, self.game.player_sprites)
        
    def update(self) -> None:
        print(f"Here {self.random}")
            
        if self.alive() and not self.hit:
            self.collide()
            
            now = pg.time.get_ticks()
            if now - self.last <= self.lifespan:
                self.last = now
                
            del self
        
    def collide(self) -> None:
        hits = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        if hits:
            for sprite in hits:
                if pg.sprite.collide_mask(self, sprite) and sprite.alive:
                    sprite.reduce_health_points(self.weapon.damage)

            self.hit = True
                