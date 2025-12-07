import pygame
import random

from player import Player
from map import Map
from camera import Camera
from car import Car
SCREEN_W, SCREEN_H = 550, 900
WORLD_W,WORLD_H = SCREEN_W,1450
CAMERA_W,CAMERA_H = SCREEN_W,SCREEN_H


background = pygame.image.load("exp_bg.png")
chicken = pygame.image.load("chicken.png")
carpng = pygame.image.load("car.png")
car_left_img = pygame.image.load("car.png")
car_right_img = pygame.image.load("rev_car.png")
carRows = {25:-1, 23:1, 22:-1, 19:-1, 15:1, 13:-1, 12:1, 11:1, 9:-1, 8:1, 5:-1, 1:1}
cartimer = 0

class Crossy_roads:
    def __init__(self,highscore=0):
        self.score = 0
        self.cars = []
        self.highscore = highscore
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
        self.car_timer = 0
        self.frames_passed = 0
        self.refresh()
        
    def refresh(self):
        if(self.highscore < self.score):
            self.highscore = self.score
        self.map = Map(SCREEN_W,WORLD_H,self).initialize_map()
        self.player = Player(250,WORLD_H - 150,self.map)
        self.camera = Camera(CAMERA_W,CAMERA_H,WORLD_H,self)
        self.score = 0
        self.best_y = self.player.y

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
    
    def play(self,action = None):
        if not action:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    self.key_pressed(event.key)
        else:
            self.key_pressed(action)

        self.camera.update_camera(0,0,self.screen,self.world)
        self.screen.blit(chicken, (self.player.x, self.player.y - self.camera.y))

        #Moving Cars in game
        if self.car_timer % 30 == 0:
            self.spawncars()
        self.car_timer += 1

        new_cars = []
        for car in self.cars:
            if car.x > -150 or car.x > 650:
                new_cars.append(car)
            car.update(self.map)
            car_img = car_left_img if car.direction == -1 else car_right_img
            self.screen.blit(car_img, (car.x, car.y - self.camera.y))
        self.cars = new_cars

        self.screen.blit(pygame.font.SysFont(None, 100).render(str(self.score), True, (255, 255, 255)), (25, 25))
        self.screen.blit(pygame.font.SysFont(None, 50).render("Highscore: " + str(self.highscore), True, (255, 255, 255)), (10, 850))
        pygame.display.update()
        pygame.display.flip()
        if(self.frames_passed > 210):
            self.refresh()
            self.frames_passed = 0
        return 100
    
    def key_pressed(self,key):
        self.player.key_pressed(self.map,key)
        self.camera.update_camera(key,self.player.y,self.screen,self.world)
        if self.player.y < self.best_y:
            self.score += 1
            self.best_y = self.player.y
    
    def car_nearme(self):
        player_pos = self.map.player_pos
        car_near = [
            True if self.map.within_map(player_pos[0],player_pos[1]-1) and self.map.grid[player_pos[1]-1][player_pos[0]] else False,
            True if self.map.within_map(player_pos[0],player_pos[1]+1) and self.map.grid[player_pos[1]+1][player_pos[0]] else False,
            True if self.map.within_map(player_pos[0]-1,player_pos[1]) and self.map.grid[player_pos[1]][player_pos[0]-1] else False,
            True if self.map.within_map(player_pos[0]+1,player_pos[1]) and self.map.grid[player_pos[1]][player_pos[0]+1] else False,
                    ] #[car ahead,car behind, car left, car right]
        return car_near