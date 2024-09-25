from utils.pg import pg
from classes.Monster import Monster

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos, monster : Monster, scale = 1) -> None:
        self.game = game
        self.monster = monster
        self.health_points = self.monster.health_points
        self.x = pos[0]
        self.y = pos[1]
        self.scale = scale
        witdth = self.monster.image.get_width()
        height = self.monster.image.get_height()
        self.image = pg.transform.scale(self.monster.image, (int(witdth * self.scale), int(height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.x_change = 0
        self.y_change = 0
        self.alive = True
        super().__init__(self.game.enemy_sprites)
        
    def reduce_health_points(self, value : int) -> None:
        self.health_points -= value
        if self.health_points <= 0:
            self.die()
        
    def draw(self) -> None:
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def die(self) -> None:
        self.alive = False
        self.game.enemy_sprites.remove(self)
        del self

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
        
    def move(self) -> None:
        for player in self.game.player_sprite:
            distance_x = player.rect.topleft[0] - self.rect.topleft[0]
            distance_y = player.rect.topleft[1] - self.rect.topleft[1]
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            # Move the enemy toward the player
            if distance != 0:
                self.x_change = self.monster.speed * distance_x / distance
                self.y_change = self.monster.speed * distance_y / distance
        
        # Update position
        self.rect.x += self.x_change
        self.collide_obstacle('x')
        self.rect.y += self.y_change
        self.collide_obstacle('y')
        
    def update(self) -> None:
        self.move()