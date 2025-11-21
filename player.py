import pygame

class Player():
    def __init__(self,spawn_x,spawn_y):
        self.player = pygame.Rect(spawn_x,spawn_y, 50, 50)
        self.alive_state = True
    
    def move_left(self):
        self.player.x -= 1
    
    def move_right(self):
        self.player.x += 1
    
    def move_up(self):
        self.player.y -= 1
    
    def move_down(self):
        self.player.y += 1