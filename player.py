import pygame

class Player():
    def __init__(self,spawn_x,spawn_y):
        self.player = pygame.Rect(spawn_x,spawn_y, 50, 50)
        self.grid_pos = []
        self.alive_state = True

    def move_player(self,direction,distance):
        if(direction == "x"):
            if(not (self.player.x + distance < 0) and not (self.player.x + distance > 500)):
                self.player.x += distance
        else:
            if(not (self.player.y + distance > 850)):
                self.player.y += distance
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
    