from utils.pg import pg
from classes.Character import Character
from classes.Attack import Attack
from classes.Effect import Effect, EffectTypes
from enums.PlayerFacingDirections import PlyerFacingDirections
from config.keybinds import *
from constants.effects import SlowEffect

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos, character: Character, scale = 1) -> None:
        self.game = game
        self.character = character
        self.health_points = self.character.health_points
        self.speed = self.character.speed
        self.stamina = self.character.stamina
        
        self.dodge_speed = 0
        self.dodge_speed_max = 50
        self.dodging = False
        self.invincible = False
        
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

        self.enemy_collision_last = pg.time.get_ticks()
        self.player_movement_last = pg.time.get_ticks()
        self.player_dodge_last = pg.time.get_ticks()
        self.stamina_last = pg.time.get_ticks()

        self.effects = []
        
        super().__init__(self.game.player_sprite)

    def refill_stamina(self) -> None:
        now = pg.time.get_ticks()
        if now - self.stamina_last >= 1000 and self.stamina < 100:
            self.stamina += 1

    def knock_back(self) -> None:
        match self.facing.normalize():
            case PlyerFacingDirections.UP.value:
                self.y_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.DOWN.value:
                self.y_change -= self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.LEFT.value:
                self.x_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.RIGHT.value:
                self.x_change -= self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.UPLEFT.value:
                self.y_change += self.character.speed * (1 / self.character.weight) * 1000
                self.x_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.UPRIGHT.value:
                self.y_change += self.character.speed * (1 / self.character.weight) * 1000
                self.x_change -= self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.DOWNLEFT.value:
                self.y_change -= self.character.speed * (1 / self.character.weight) * 1000
                self.x_change += self.character.speed * (1 / self.character.weight) * 1000
            case PlyerFacingDirections.DOWNRIGHT.value:
                self.y_change -= self.character.speed * (1 / self.character.weight) * 1000
                self.x_change -= self.character.speed * (1 / self.character.weight) * 1000
                
    def dodge(self) -> None:
        now = pg.time.get_ticks()
        if self.stamina >= 20 and now - self.player_dodge_last >= 500:
            self.dodging = True
            self.invincible = True
            self.dodge_speed = 0
            self.player_dodge_last = now
            self.stamina -= 20
            self.stamina_last = pg.time.get_ticks()
               
    def is_dodging(self) -> None:
        if self.dodging:
            if self.dodge_speed < self.dodge_speed_max:
                self.dodge_speed += (1 / self.character.weight) * 1000

                match self.facing.normalize():
                    case PlyerFacingDirections.UP.value:
                        self.y_change -= self.dodge_speed
                    case PlyerFacingDirections.DOWN.value:
                        self.y_change += self.dodge_speed
                    case PlyerFacingDirections.LEFT.value:
                        self.x_change -= self.dodge_speed
                    case PlyerFacingDirections.RIGHT.value:
                        self.x_change += self.dodge_speed
                    case PlyerFacingDirections.UPLEFT.value:
                        self.y_change -= self.dodge_speed
                        self.x_change -= self.dodge_speed
                    case PlyerFacingDirections.UPRIGHT.value:
                        self.y_change -= self.dodge_speed
                        self.x_change += self.dodge_speed
                    case PlyerFacingDirections.DOWNLEFT.value:
                        self.y_change += self.dodge_speed
                        self.x_change -= self.dodge_speed
                    case PlyerFacingDirections.DOWNRIGHT.value:
                        self.y_change += self.dodge_speed
                        self.x_change += self.dodge_speed

                self.update_position_with_collision(self.x_change, "x")
                self.update_position_with_collision(self.y_change, "y")

            if self.dodge_speed >= self.dodge_speed_max:
                self.dodging = False 
                self.invincible = False
     
    def sneak(self) -> None:
        self.speed /= 2
        if self.stamina <= self.character.stamina:
            self.stamina += 0.5
        
    def sprint(self) -> None:
        if self.stamina > 0:
            self.speed *= 1.5
            self.stamina -= 1
            self.stamina_last = pg.time.get_ticks()
    
    def input(self):
        keys = pg.key.get_pressed()
        self.movement(keys)
        self.attack_input(keys)

    def movement(self, keys):
        now = pg.time.get_ticks()
               
        if keys[SNEAK_KEY]:
            self.sneak()
        elif keys[SPRINT_KEY]:
            self.sprint()
            
        if keys[DODGE_KEY]:
            self.dodge()
            
        move_vec = pg.math.Vector2(keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY], keys[MOVE_DOWN_KEY] - keys[MOVE_UP_KEY])
        # Check if the player is changing direction
        if move_vec.x != 0 or move_vec.y != 0:
            # If the player is already moving in the same direction, scale the vector to the speed
            if move_vec.x == self.facing.x and move_vec.y == self.facing.y:
                move_vec.scale_to_length(self.speed)
            elif (move_vec.x == 1 or move_vec.x == -1) and (move_vec.y == 1 or move_vec.y == -1):
                self.facing = move_vec
                move_vec.scale_to_length(self.speed) 
            # Otherwise, set the vector to zero and decrease the delay
            else:
                self.facing = move_vec.normalize()
                move_vec.scale_to_length(0)
                
                self.player_movement_last = now

        self.x_change += move_vec.x
        self.y_change += move_vec.y
        self.speed = self.character.speed
            
    def attack_input(self, keys):
        if keys[ATTACK_KEY]:
            self.attack()
            
    def attack(self) -> None:
        now = pg.time.get_ticks()
        if now - self.character.equipped.last >= self.character.equipped.cooldown and self.stamina >= 20:
            self.character.equipped.last = now
            
            match self.facing.normalize():
                case PlyerFacingDirections.UP.value:
                    Attack(self.game, self.character.equipped, (self.rect.x + 16, self.rect.y - self.game.tile_size + 16))
                case PlyerFacingDirections.DOWN.value:
                    Attack(self.game, self.character.equipped, (self.rect.x + 16, self.rect.y + self.game.tile_size))
                case PlyerFacingDirections.LEFT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x - self.game.tile_size + 16, self.rect.y + 16))
                case PlyerFacingDirections.RIGHT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x + self.game.tile_size + 16, self.rect.y + 16))  
                case PlyerFacingDirections.UPLEFT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x - self.game.tile_size + 16, self.rect.y - self.game.tile_size + 16)) 
                case PlyerFacingDirections.UPRIGHT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x + self.game.tile_size + 16, self.rect.y - self.game.tile_size + 16)) 
                case PlyerFacingDirections.DOWNLEFT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x - self.game.tile_size + 16, self.rect.y + self.game.tile_size + 16)) 
                case PlyerFacingDirections.DOWNRIGHT.value:
                    Attack(self.game, self.character.equipped, (self.rect.x + self.game.tile_size + 16, self.rect.y + self.game.tile_size + 16)) 
       
            self.stamina -= 20
            self.stamina_last = pg.time.get_ticks()
        
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

    def update_position_with_collision(self, change, axis):
        if axis == "x":
            self.rect.x += change
            self.collide_obstacle("x")
        elif axis == "y":
            self.rect.y += change
            self.collide_obstacle("y")
                    
    def collide_enemy(self) -> None:
        now = pg.time.get_ticks()

        if now - self.enemy_collision_last >= self.character.endurance:
            hits = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
            if hits and not self.invincible:
                for sprite in hits:
                    if pg.sprite.collide_mask(self, sprite):
                        self.reduce_health_points(sprite.monster.equipped.damage)
                        self.knock_back()
                        
                        if not any(effect.type == EffectTypes.SLOW for effect in self.effects):
                            slow_effect = SlowEffect()
                            self.effects.append(slow_effect)
                        
                        self.enemy_collision_last = now

    def apply_effects(self):
        for effect in self.effects:
            if effect.duration <= 0:
                self.effects.remove(effect)
            
            effect.apply(self)

    def reduce_effects_duration(self):
        for effect in self.effects:
            effect.duration -= 1
  
    def update(self) -> None:
        self.input()
        self.is_dodging()
        
        self.refill_stamina()
        self.collide_enemy()

        self.apply_effects()
        self.reduce_effects_duration()
        
        if not self.dodging:
            self.update_position_with_collision(self.x_change, "x")
            self.update_position_with_collision(self.y_change, "y")

        self.x_change = 0
        self.y_change = 0
