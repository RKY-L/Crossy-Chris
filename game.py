import pygame
from cars import *
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
chicken = Player(250,850)

tile_size = 50

#11x18 Grid



map = Map(SCREEN_W,SCREEN_H).initialize_map()

spawn()

draw_cars(screen, listofCars)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    
    pygame.draw.rect(screen, (0,255,0), chicken.player)
    pygame.display.update()


    map.draw_grid(screen)
    time_delta = clock.tick(30)
    pygame.display.flip()

    dt = clock.tick(60) / 1000.0

    updatecar_pos()








pygame.quit()