import pygame
import random

from player import Player
from map import Map
from camera import Camera
from car import Car
SCREEN_W, SCREEN_H = 550, 900
WORLD_W,WORLD_H = SCREEN_W,1450
CAMERA_W,CAMERA_H = SCREEN_W,SCREEN_H


pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()


background = pygame.image.load("exp_bg.png")
chicken = pygame.image.load("chicken.png")
carpng = pygame.image.load("car.png")
carimg = pygame.image.load("car.png")
world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
map = Map(SCREEN_W,WORLD_H).initialize_map()
player = Player(250,WORLD_H - 150,map)

camera = Camera(CAMERA_W,CAMERA_H,WORLD_H)

#obstacles
carRows = [25, 23, 22, 19, 15, 13, 12, 11, 9, 8, 5, 2]
cars = []
cartimer = 0
#map.add_obstacle(24,2)

def spawncars():
    for row in carRows:
        if random.randint(0,2) == 0:
            car = Car(row)
            cars.append(car)

running = True
tile_size = 50
camera.update_camera(pygame.K_w,player.y,screen,world)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.key_pressed(map,event.key)
            camera.update_camera(event.key,player.y,screen,world)

    if cartimer % 30 == 0:
        spawncars()
    cartimer += 1
    camera.update_camera(0,0,screen,world)
    screen.blit(chicken, (player.x, player.y - camera.y))
    map.draw_grid(screen)

    new_cars = []
    for car in cars:
        if car.x > -150:
            new_cars.append(car)
        car.update(map)
        screen.blit(carimg, (car.x, car.y - camera.y))

    cars = new_cars

    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()