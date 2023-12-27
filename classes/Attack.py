from utils.pg import pg
from random import randint
from classes.CameraGroup import CameraGroup
from classes.Item import Item

class Attack(pg.sprite.Sprite):
    def __init__(self, game, camera_group : CameraGroup, weapon : Item, pos : ()) -> None:
        self.game = game
        self.camera_group = camera_group
        self.weapon = weapon
        
        self.image = self.weapon.image
        self.rect = self.image.get_rect(topleft = pos)
        
        self.hit = False
        self.lifespan = 100
        self.last = pg.time.get_ticks()
        super().__init__(camera_group, self.game.player_sprites)
        
    def update(self) -> None:
        #if sprite is visible
        if self.alive():
            #makes sure each attack can only hit once
            if not self.hit:
                self.collide()
            
            #deletes sprite after some time so that the attack is no longer visible
            now = pg.time.get_ticks()
            if now - self.last >= self.lifespan:
                self.kill()
        # if it isn't delete it  (WHY DOESN'T IT F**KING DELETE IT)     
        else: 
            del self
        
    def collide(self) -> None:
        hits = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        if hits:
            for sprite in hits:
                if pg.sprite.collide_mask(self, sprite) and sprite.alive:
                    sprite.reduce_health_points(self.weapon.damage)

            self.hit = True
                