import pygame

class Map:
    def __init__(self,world_w,world_h,tile_size = 50):
        self.tile_size = tile_size
        self.grid = []
        self.width = world_w
        self.height = world_h
        self.player_pos = [0,0]
        self.obstacles = []
    
    def initialize_map(self):
        map = []
        row = self.width//self.tile_size
        for y in range(0, self.height, self.tile_size):
            map.append([""] * row)
        self.grid = map
        return self
    
    def draw_grid(self,screen):
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(screen, (200,200,200), (x,0), (x,self.height))
        for y in range(0, self.height, self.tile_size):
            pygame.draw.line(screen, (200,200,200), (0,y), (self.width,y))

    def update_player_pos(self,x,y):
        self.grid[self.player_pos[1]][self.player_pos[0]] = ""
        self.player_pos[0] = (x//50)
        self.player_pos[1] = (y//50)
        self.grid[self.player_pos[1]][self.player_pos[0]] = "@"

    def add_obstacle(self, tile_y, tile_x):
        self.grid[tile_y][tile_x] = "T"
        
    def check_collision(self, y, x):
        tile_x = x // 50
        tile_y = y // 50
        if self.grid[tile_y][tile_x] == "T":
            return "Tree"
        elif self.grid[tile_y][tile_x] == 'x':
            return "Car"
        elif self.grid[tile_y][tile_x] == "@":
            return "Player"
        return None
