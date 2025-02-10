from utils.pg import pg
from constants.backgrounds import background
from enums.Colors import Colors

class CameraGroup:
    def __init__(self, game) -> None:
        self.display_surface = pg.display.get_surface()
        self.game = game

        self.offset = pg.math.Vector2()
        self.camera_borders = {'left': 0.4 * self.game.screen.get_width(), 'right': 0.4 * self.game.screen.get_width(), 'top': 0.4 * self.game.screen.get_height(), 'bottom':  0.4 * self.game.screen.get_height()}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pg.Rect(l,t,w,h)

        self.ground_surf = background
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
        
    def box_target_camera(self,target) -> None:
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
        
    def draw_sprites(self, sprites : pg.sprite.Sprite) -> None:
        for sprite in sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.ground_surf.blit(sprite.image,offset_pos)
  
    def draw(self, player) -> None:
        
        self.box_target_camera(player)
        
        self.ground_surf.fill(Colors.BLACK.value)
        
        self.draw_sprites(self.game.ground_sprites)
        self.draw_sprites(self.game.obstacle_sprites)
        self.draw_sprites(self.game.enemy_sprites)
        self.draw_sprites(self.game.player_sprite)
        self.draw_sprites(self.game.attack_sprites)
        self.draw_sprites(self.game.ui_sprites)
        
        self.display_surface.blit(self.ground_surf,self.ground_rect)
