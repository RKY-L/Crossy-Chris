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
car = Car(25)
carimg = pygame.image.load("car.png")
world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
map = Map(SCREEN_W,WORLD_H).initialize_map()
player = Player(250,WORLD_H - 150,map)

camera = Camera(CAMERA_W,CAMERA_H,WORLD_H)

#obstacles
carRows = {25:0, 23:1, 22:0, 19:0, 15:1, 13:0, 12:1, 11:1, 9:0, 8:1, 5:0, 2:1}
cars = []
cartimer = 0
map.add_obstacle(24,2)

def spawncars():
    for row in carRows:
        coin = random.randint(0,3)
        if coin == 1:
            car = Car(row)
            cars.append(car)
            car.direction = carRows[row]
            if car.direction == 0:
                car.x = 650
            else:
                car.x = -100

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

    if cartimer % 720 == 0:
        spawncars()
    cartimer += 30
    camera.update_camera(0,0,screen,world)
    screen.blit(chicken, (player.x, player.y - camera.y))
    map.draw_grid(screen)
    for car in cars:
        car.update(map)
        screen.blit(carimg, (car.x, car.y - camera.y))
        if car.x < -150 or car.x > 650:
            cars.remove(car)


    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()