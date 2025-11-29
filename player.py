import pygame

class Player():
    def __init__(self,spawn_x,spawn_y,map_obj):
        self.x = spawn_x
        self.y = spawn_y
        self.width = 50
        self.height = 50
        self.grid_pos = []
        self.alive_state = True
        self.map = map_obj

    def move_player(self,direction,distance):
        if(direction == "x"):
            if(self.x + distance >= 0 and self.x + distance < self.map.width):
                self.x += distance
        else:
            if(self.y + distance >= 0 and self.y + distance < self.map.height):
                self.y += distance
        #detect collision here?
        
    def key_pressed(self,key):
        if key == pygame.K_a:
            self.move_player("x",-50)
        if key == pygame.K_d:
            self.move_player("x",50)
        if key == pygame.K_w:
            self.move_player("y",-50)
        if key == pygame.K_s:
            self.move_player("y",50)
    