import pygame
class Map:
    def __init__(self,world_w,world_h,game):
        self.tile_size = 50
        self.grid = []
        self.width = world_w
        self.height = world_h
        self.player_pos = [0,0]
        self.obstacles = []
        self.game = game
    
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

    def add_obstacle(self, tile_y, tile_x):
        self.grid[tile_y][tile_x] = "T"
        
    def check_collision(self,x,y):
        tile_x = x // 50
        tile_y = y // 50
        if tile_y < len(self.grid) and tile_x < len(self.grid[0]):
            if self.grid[tile_y][tile_x] == "T":
                return "Tree"
            elif self.grid[tile_y][tile_x] == 'x':
                self.game.refresh()
                return "Car"
            elif self.grid[tile_y][tile_x] == "@":
                self.game.refresh()
                return "Player"
        return None

    def update_player_pos(self,x,y,new_x,new_y):
        if not self.check_collision(new_x,new_y):
            new_x_idx = new_x // self.tile_size
            new_y_idx = new_y // self.tile_size
            if self.within_map(new_x_idx,new_y_idx):
                self.grid[self.player_pos[1]][self.player_pos[0]] = ""
                self.player_pos[0] = new_x_idx
                self.player_pos[1] = new_y_idx
                self.grid[self.player_pos[1]][self.player_pos[0]] = "@"
                return new_y,new_x
        return y,x
    
    def updatecarpos(self,x, y,direction):
        front_x = x // self.tile_size
        back_x = front_x - direction

        new_front = front_x + direction
        new_back = new_front - direction
        y_idx = y // self.tile_size
        if not self.check_collision(new_front * self.tile_size,y):
            if y_idx < len(self.grid):
                #front of car
                if 0 <= front_x < len(self.grid[0]):
                    self.grid[y_idx][front_x] = ""
                if 0 <= new_front < len(self.grid[0]):
                    self.grid[y_idx][new_front] = "x"
                #back of car
                if 0 <= back_x < len(self.grid[0]):
                    self.grid[y_idx][back_x] = ""
                if 0 <= new_back < len(self.grid[0]):
                    self.grid[y_idx][new_back] = "x"
            return new_front * self.tile_size
        return x

    def within_map(self,x,y):
        if y < len(self.grid) and x < len(self.grid[0]):
            return True
        return False

    def player_row(self):
        return self.player_pos[1]

    def player_col(self):
        return self.player_pos[0]