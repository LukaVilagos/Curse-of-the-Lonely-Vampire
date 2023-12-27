from utils.pg import pg
from classes.Character import Character
from classes.Attack import Attack
from enums.PlayerFacingDirections import PlyerFacingDirections
from config.keybinds import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos : (), character: Character, camera_group : pg.sprite.Sprite, scale = 1) -> None:
        super().__init__(camera_group)
        self.game = game
        self.camera_group = camera_group
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
        self.facing = PlyerFacingDirections.DOWN.value
        
        self.last = pg.time.get_ticks()
        pg.sprite.Sprite.__init__(self, self.game.player_sprites)
        
    def knock_back(self):
        match self.facing:
            case PlyerFacingDirections.UP.value:
                self.y_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.DOWN.value:
                self.y_change -= self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.LEFT.value:
                self.x_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.RIGHT.value:
                self.x_change -= self.character.speed * (1 / self.character.weight) * 1000
        
    def input(self, enemies : []) -> None:
        keys = pg.key.get_pressed()
        move_vec = pg.math.Vector2(keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY], keys[MOVE_DOWN_KEY] - keys[MOVE_UP_KEY])
        
        if move_vec.x != 0 or move_vec.y != 0:
            move_vec.scale_to_length(self.character.speed)

        self.x_change += move_vec.x
        self.y_change += move_vec.y
        if move_vec.x > 0:
            self.facing = PlyerFacingDirections.RIGHT.value
        elif move_vec.x < 0:
            self.facing = PlyerFacingDirections.LEFT.value
        elif move_vec.y > 0:
            self.facing = PlyerFacingDirections.DOWN.value
        elif move_vec.y < 0:
            self.facing = PlyerFacingDirections.UP.value
        
        if keys[ATTACK_KEY]:
            now = pg.time.get_ticks()
            if now - self.character.equipped.last >= self.character.equipped.cooldown:
                self.character.equipped.last = now
                self.attack(enemies)
        
            
    def attack(self, enemies : []) -> None:
        match self.facing:
            case PlyerFacingDirections.UP.value:
                Attack(self.game, self.camera_group, self.character.equipped, (self.rect.x + 16, self.rect.y - self.game.tile_size + 16))
            case PlyerFacingDirections.DOWN.value:
                Attack(self.game, self.camera_group, self.character.equipped, (self.rect.x + 16, self.rect.y + self.game.tile_size))
            case PlyerFacingDirections.LEFT.value:
                Attack(self.game, self.camera_group, self.character.equipped, (self.rect.x - self.game.tile_size + 16, self.rect.y + 16))
            case PlyerFacingDirections.RIGHT.value:
                Attack(self.game, self.camera_group, self.character.equipped, (self.rect.x + self.game.tile_size + 16, self.rect.y + 16))   
    
    def die(self) -> None:
        self.game.exit_game()
            
    def reduce_health_points(self, value: int) -> None:
        self.health_points -= value
        if self.health_points <= 0:
            self.die()
            
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
                if pg.sprite.collide_mask(self, sprite):
                    self.reduce_health_points(sprite.monster.equipped.damage)
                    self.knock_back()
  
    def custom_update(self, enemies: []) -> None:
        self.input(enemies)
        
        now = pg.time.get_ticks()
        if now - self.last >= self.character.endurance:
            self.last = now
            self.collide_enemy()
        
        self.rect.x += self.x_change
        self.collide_obstacle("x")
        self.rect.y += self.y_change
        self.collide_obstacle("y")

        self.x_change = 0
        self.y_change = 0
