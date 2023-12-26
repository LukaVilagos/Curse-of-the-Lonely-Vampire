from utils.pg import pg
from classes.Game import Game
from classes.Character import Character
from config.keybinds import *

class Player(pg.sprite.Sprite):
    def __init__(self, game : Game, pos : (), character: Character, camera_group : pg.sprite.Sprite, scale = 1) -> None:
        super().__init__(camera_group)
        self.game = game
        self.character = character
        self.health_points = self.character.health_points
        
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
        
        pg.sprite.Sprite.__init__(self, self.game.player_sprites)
        
    def input(self, enemies : []) -> None:
        keys = pg.key.get_pressed()
        move_vec = pg.math.Vector2(keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY], keys[MOVE_DOWN_KEY] - keys[MOVE_UP_KEY])
        
        if move_vec.x != 0 or move_vec.y != 0:
            move_vec.scale_to_length(self.character.speed)

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
            if now - self.character.equipped.last >= self.character.equipped.cooldown:
                self.last = now
                self.attack(enemies)
        
            
    def attack(self, enemies : []) -> None:
        for enemy in enemies:
            enemy.monster.reduce_health_points(enemy, self.character.equipped.damage)
            
    def reduce_health_points(self, value: int) -> None:
        self.health_points -= value
    
    def die(self) -> None:
        self.game.player_sprites.remove(self)
            
    def collide_obstacle(self, direction : str) -> None:
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
                    
    def collide_enemy(self) -> None:
        hits = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        if hits:
            for sprite in hits:
                self.character.health_points -= sprite.monster.equipped.damage
                if self.character.health_points <= 0:
                    self.die()
                
            match self.facing:
                case "up":
                    self.y_change += self.character.speed * (1 / self.character.weight) * 1000
                case "down":
                    self.y_change -= self.character.speed * (1 / self.character.weight) * 1000
                case "left":
                    self.x_change += self.character.speed * (1 / self.character.weight) * 1000
                case "right":
                    self.x_change -= self.character.speed * (1 / self.character.weight) * 1000
  
    def custom_update(self, enemies: []) -> None:
        self.input(enemies)
        now = pg.time.get_ticks()
        if now - self.character.last >= self.character.endurance:
                self.character.last = now
                self.collide_enemy()
        
        self.rect.x += self.x_change
        self.collide_obstacle("x")
        self.rect.y += self.y_change
        self.collide_obstacle("y")

        self.x_change = 0
        self.y_change = 0
