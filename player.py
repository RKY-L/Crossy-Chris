import pygame

class Player():
    def __init__(self,spawn_x,spawn_y,map_obj):
        self.x = spawn_x
        self.y = spawn_y
        self.width = 50
        self.height = 50
        self.grid_pos = []
        self.map = map_obj

    def move_player(self,map,direction,distance):
        new_x = self.x
        new_y = self.y
        if(direction == "x"):
            if(self.x + distance >= 0 and self.x + distance < self.map.width):
                new_x = self.x + distance
        else:
            if(self.y + distance >= 0 and self.y + distance < self.map.height):
                new_y = self.y + distance
        
        self.y,self.x = map.update_player_pos(self.x, self.y,new_x,new_y)
        
    def key_pressed(self,map,key):
        if key == pygame.K_a:
            self.move_player(map,"x",-50)
        if key == pygame.K_d:
            self.move_player(map,"x",50)
        if key == pygame.K_w:
            self.move_player(map,"y",-50)
        if key == pygame.K_s:
            self.move_player(map,"y",50)

    