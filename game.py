import pygame

from player import Player
from map import Map
from camera import Camera
SCREEN_W, SCREEN_H = 550, 900
WORLD_W,WORLD_H = SCREEN_W,1450
CAMERA_W,CAMERA_H = SCREEN_W,SCREEN_H


pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()


background = pygame.image.load("test_background.jpg")
world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
map = Map(SCREEN_W,WORLD_H).initialize_map()
player = Player(250,WORLD_H - 150,map)
camera = Camera(CAMERA_W,CAMERA_H,WORLD_H)




running = True
tile_size = 50
camera.update_camera(pygame.K_w,player.y,screen,world)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.key_pressed(event.key)
            camera.update_camera(event.key,player.y,screen,world)
            map.update_player_pos(player.x,player.y)


    pygame.draw.rect(screen, (0,255,0), (player.x,player.y - camera.y, player.width, player.height))
    map.draw_grid(screen)

    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()