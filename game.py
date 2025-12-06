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
car_left_img = pygame.image.load("car.png")
car_right_img = pygame.image.load("rev_car.png")
world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
carRows = {25:-1, 23:1, 22:-1, 19:-1, 15:1, 13:-1, 12:1, 11:1, 9:-1, 8:1, 5:-1, 1:1}
cartimer = 0

class Game:
    def refresh(self):
        self.highscore = self.score
        self.map = Map(SCREEN_W,WORLD_H,self).initialize_map()
        self.player = Player(250,WORLD_H - 150,self.map)
        self.camera = Camera(CAMERA_W,CAMERA_H,WORLD_H,self)
        self.score = 0
        self.best_y = self.player.y

    def __init__(self,highscore=0):
        self.score = 0
        self.cars = []
        self.highscore = highscore
        self.refresh()

    def spawncars(self):
        for row in carRows:
            if random.randint(0,1) == 1:
                car = Car(row)
                self.cars.append(car)
                car.direction = carRows[row]
                if car.direction == -1:
                    car.x = 650
                else:
                    car.x = -100

    def win(self):
        self.refresh()
game = Game()


running = True
tile_size = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.player.key_pressed(game.map,event.key)
            game.camera.update_camera(event.key,game.player.y,screen,world)
            if game.player.y < game.best_y:
                game.score += 1
                game.best_y = game.player.y

    if cartimer % 30 == 0:
        game.spawncars()
    cartimer += 1
    game.camera.update_camera(0,0,screen,world)
    screen.blit(chicken, (game.player.x, game.player.y - game.camera.y))
    #game.map.draw_grid(screen)

    new_cars = []
    for car in game.cars:
        if car.x > -150 or car.x > 650:
            new_cars.append(car)
        car.update(game.map)
        if car.direction == -1:
            screen.blit(car_left_img, (car.x, car.y - game.camera.y))
        else:
            screen.blit(car_right_img, (car.x, car.y - game.camera.y))
    game.cars = new_cars

    screen.blit(pygame.font.SysFont(None, 100).render(str(game.score), True, (255, 255, 255)), (25, 25))
    screen.blit(pygame.font.SysFont(None, 50).render("Highscore: " + str(game.highscore), True, (255, 255, 255)), (10, 850))
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()