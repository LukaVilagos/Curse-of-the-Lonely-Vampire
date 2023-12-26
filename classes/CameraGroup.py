from utils.pg import pg
from constants.images import tree_img
from constants.backgrounds import background

class CameraGroup(pg.sprite.Group):
    def __init__(self, game, tilemap):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.game = game
        self.tilemap = tilemap

        self.offset = pg.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': 0.4 * self.game.screen.get_width(), 'right': 0.4 * self.game.screen.get_width(), 'top': 0.4 * self.game.screen.get_height(), 'bottom':  0.4 * self.game.screen.get_height()}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pg.Rect(l,t,w,h)

        self.ground_surf = background
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        self.zoom_scale = 1
        self.internal_surf_size = (len(max(tilemap, key=len)) * self.game.tile_size, len(tilemap) * self.game.tile_size)
        self.internal_surf = pg.Surface(self.internal_surf_size, pg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pg.math.Vector2(self.internal_surf_size)
        self.internal_offset = pg.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
        
    def box_target_camera(self,target):
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
        
    def draw_sprites(self, sprites):
        for sprite in sprites:
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image,offset_pos)
  
    def custom_draw(self, player):
        
        self.box_target_camera(player)
        
        self.internal_surf.fill('#000000')

        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf,ground_offset)
        
        self.draw_sprites(self.game.ground_sprites)
        self.draw_sprites(sorted(self.game.obstacle_sprites,key = lambda sprite: sprite.rect.centery))
        self.draw_sprites(sorted(self.game.active_sprites,key = lambda sprite: sprite.rect.centery))

        scaled_surf = pg.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        self.display_surface.blit(scaled_surf,scaled_rect)
