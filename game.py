import pygame

from player import Player
from map import Map

pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
SCREEN_W, SCREEN_H = 550, 900
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

screen.fill((255, 255, 255))
clock = pygame.time.Clock()

running = True
chicken = Player(250,700)

tile_size = 50



map = Map(SCREEN_W,SCREEN_H).initialize_map()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            chicken.key_pressed(event.key)
    
    map.update_player_pos(chicken.player.x,chicken.player.y)
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,255,0), chicken.player)
    map.draw_grid(screen)
    pygame.display.update()
    time_delta = clock.tick(30)
    pygame.display.flip()


pygame.quit()