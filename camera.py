import pygame

class Camera:
    def __init__(self,camera_w,camera_h,world_h,game):
        self.width = camera_w
        self.height = camera_h
        self.world_height = world_h
        self.y = self.world_height - self.height
        self.checkpoint = 0
        self.game = game

    
    def update_camera(self,key_pressed,player_y,screen,world):
        if key_pressed == pygame.K_s:
            if player_y - 50 - self.y > 800:
                self.game.refresh()
            if self.checkpoint == 0:
                    self.checkpoint = player_y - 50
        elif key_pressed == pygame.K_w and (player_y == self.checkpoint or self.checkpoint == 0):
            self.y = max(0, min(player_y - self.height // 2, self.world_height - self.height))
            self.checkpoint = 0 

        screen.blit(world,(0,0),(0,self.y,self.width,self.height))