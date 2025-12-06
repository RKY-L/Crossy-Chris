import pygame
import random

from player import Player
from maps import Map
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
carRows = [25]
cartimer = 0

class Game:
    def __init__(self):
        self.map = Map(SCREEN_W,WORLD_H,self).initialize_map()
        self.player = Player(250,WORLD_H - 150,self.map)
        self.camera = Camera(CAMERA_W,CAMERA_H,WORLD_H,self)
        self.cars = []


    def spawncars(self):
        for row in carRows:
            if random.randint(0,2) == 0:
                car = Car(row)
                self.cars.append(car)

    def refresh(self):
        self.__init__()
game = Game()


running = True
tile_size = 50
game.camera.update_camera(pygame.K_w,game.player.y,screen,world)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.refresh()
            else:
                game.player.key_pressed(game.map,event.key)
                game.camera.update_camera(event.key,game.player.y,screen,world)

    if cartimer % 30 == 0:
        game.spawncars()
    cartimer += 1
    game.camera.update_camera(0,0,screen,world)
    screen.blit(chicken, (game.player.x, game.player.y - game.camera.y))
    game.map.draw_grid(screen)

    new_cars = []
    for car in game.cars:
        if car.x > -150:
            new_cars.append(car)
        car.update(game.map)
        screen.blit(carimg, (car.x, car.y - game.camera.y))

    game.cars = new_cars

    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()