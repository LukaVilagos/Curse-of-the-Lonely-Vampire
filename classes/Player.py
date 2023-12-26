from utils.pg import pg
from classes.Character import Character
from config.keybinds import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos, character: Character, camera_group : pg.sprite.Sprite, scale = 1):
        super().__init__(camera_group)
        self.game = game
        self.character = character
        
        witdth = self.character.image.get_width()
        height = self.character.image.get_height()
        self.x = pos[0]
        self.y = pos[1]
        self.image = pg.transform.scale(self.character.image, (int(witdth * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.rect.topleft = (self.x,self.y)
        
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        
        self.last = pg.time.get_ticks()
        self.speed = self.character.speed
        
        pg.sprite.Sprite.__init__(self, self.game.active_sprites)
        
    def input(self, enemies):
        keys = pg.key.get_pressed()
        # Create a vector from the key inputs
        move_vec = pg.math.Vector2(keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY], keys[MOVE_DOWN_KEY] - keys[MOVE_UP_KEY])

        # Normalize the vector and scale it by the speed
        if move_vec.x != 0 or move_vec.y != 0:
            move_vec.scale_to_length(self.speed)

        # Update the position and facing direction
        self.x_change += move_vec.x
        self.y_change += move_vec.y
        if move_vec.x > 0:
            self.facing = 'right'
        elif move_vec.x < 0:
            self.facing = 'left'
        elif move_vec.y > 0:
            self.facing = 'down'
        elif move_vec.y < 0:
            self.facing = 'up'

        
        if keys[ATTACK_KEY]:
            now = pg.time.get_ticks()
            if now - self.last >= self.character.equipped.cooldown:
                self.last = now
                self.attack(enemies)
        
            
    def attack(self, enemies : []):
        for enemy in enemies:
            enemy.monster.reduce_health_points(enemy, self.character.equipped.damage)
            
    def collide_obstacle(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.obstacle_sprites, False)
        
        if hits: 
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
  
    def custom_update(self, enemies: []):
        self.input(enemies)
        
        self.rect.x += self.x_change
        self.collide_obstacle("x")
        self.rect.y += self.y_change
        self.collide_obstacle("y")

        self.x_change = 0
        self.y_change = 0
