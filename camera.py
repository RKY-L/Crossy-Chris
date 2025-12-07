import pygame

class Camera:
    def __init__(self,camera_w,camera_h,world_h,game):
        self.width = camera_w
        self.height = camera_h
        self.world_height = world_h
        self.y = self.world_height - self.height
        self.checkpoint = 0
        self.game = game

    
    def update_camera(self,key,player_y,screen,world):
        if(isinstance(key,list)):
            if key == [1,0,0,0,0]:
                key = pygame.K_w
            elif key == [0,1,0,0,0]:
                key = pygame.K_a
            elif key == [0,0,1,0,0]:
                key = pygame.K_s
            elif key == [0,0,0,1,0]:
                key = pygame.K_d
            elif key == [0,0,0,0,1]:
                key = 0
        if key and (player_y - 50 - self.y) == -50:
            self.game.win()
        if key and (player_y - 50 - self.y) > 800:
            return False
        if key == pygame.K_s:
            if self.checkpoint == 0:
                    self.checkpoint = player_y - 50
        elif key == pygame.K_w and (player_y == self.checkpoint or self.checkpoint == 0):
            self.y = max(0, min(player_y - self.height // 2, self.world_height - self.height))
            self.checkpoint = 0 

        screen.blit(world,(0,0),(0,self.y,self.width,self.height))
        return True