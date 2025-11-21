import pygame

class Map:
    def __init__(self,screen_w,screen_h,tile_size = 50):
        self.tile_size = tile_size
        self.grid = []
        self.s_width = screen_w
        self.s_height = screen_h
        self.speed = 1
    
    def initialize_map(self):
        map = []
        row = self.s_width//self.tile_size
        for y in range(0, self.s_height, self.tile_size):
            map.append([0] * row)
        self.grid = map
        return self
    
    def draw_grid(self,screen):
        for x in range(0, self.s_width, self.tile_size):
            pygame.draw.line(screen, (200,200,200), (x,0), (x,self.s_height))
        for y in range(0, self.s_height, self.tile_size):
            pygame.draw.line(screen, (200,200,200), (0,y), (self.s_width,y))
