import pygame
import random

from game.player import Player
from game.map import Map
from game.camera import Camera
from game.car import Car
SCREEN_W, SCREEN_H = 550, 900
WORLD_W,WORLD_H = SCREEN_W,1450
CAMERA_W,CAMERA_H = SCREEN_W,SCREEN_H


background = pygame.image.load("./game/exp_bg.png")
chicken = pygame.image.load("./game/chicken.png")
carpng = pygame.image.load("./game/car.png")
car_left_img = pygame.image.load("./game/car.png")
car_right_img = pygame.image.load("./game/rev_car.png")
carRows = {25:(0,25), 23:(1,30), 22:(0,50), 19:(0,30), 15:(1,30), 13:(0,25), 12:(1,50), 11:(1,30), 9:(0,25), 8:(1,50), 5:(0,25), 1:(1,30)}
cartimer = 0

class Crossy_roads:
    def __init__(self,highscore=0):
        self.score = 0
        self.cars = []
        self.highscore = highscore
        self.prev_score = 0
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.world = pygame.transform.scale(background, (SCREEN_W, WORLD_H))
        self.car_timer = 0
        self.frames_passed = 0
        self.player_died = False
        self.refresh()
        
    def refresh(self):
        if(self.highscore < self.score):
            self.highscore = self.score
        self.prev_score = self.score
        self.map = Map(SCREEN_W,WORLD_H,self).initialize_map()
        self.player = Player(250,WORLD_H - 150,self.map)
        self.camera = Camera(CAMERA_W,CAMERA_H,WORLD_H,self)
        self.score = 0
        self.best_y = self.player.y
        self.frames_passed = 0

        self.player_died = False
        self.won = False
        


    def spawncars(self):
        for row in carRows:
            if self.car_timer % carRows[row][1] == 0:
                car = Car(row)
                self.cars.append(car)
                car.direction = carRows[row][0]
                car.car_img = car_left_img if car.direction == 0 else car_right_img
                if car.direction == 0: #spawn right move left
                    car.x = 650
                else: #spawn left move right
                    car.x = -100

    
    def play(self,action = None):
        advanced_foward = False
        cars_infront = self.whats_nearme()[:3]
        prev_pos = self.map.player_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif not action and event.type == pygame.KEYDOWN:
                action = event.key
        if action:
            if self.key_pressed(action) == "New Score":
                advanced_foward = True
        
        #Moving Cars in game
        self.spawncars()
        self.car_timer += 1

        new_cars = []
        for car in self.cars:
            if -150 < car.x < 700:
                new_cars.append(car)
            car.update(self.map)
        self.cars = new_cars
        #==============================================

        self.camera.update_camera(0,0,self.screen,self.world)
        self.screen.blit(chicken, (self.player.x, self.player.y - self.camera.y))

        for car in self.cars:
            self.screen.blit(car.car_img, (car.x, car.y - self.camera.y))
        self.screen.blit(pygame.font.SysFont(None, 100).render(str(self.score), True, (255, 255, 255)), (25, 25))
        self.screen.blit(pygame.font.SysFont(None, 50).render("Highscore: " + str(self.highscore), True, (255, 255, 255)), (10, 850))
        pygame.display.update()
        pygame.display.flip()

        if(self.frames_passed > 210): #Death for standing still too long
            self.player_died = True
        
        return self.reward_function(action,advanced_foward)
    
    def key_pressed(self,key):
        self.player.key_pressed(self.map,key)
        self.camera.update_camera(key,self.player.y,self.screen,self.world)
        if self.player.y < self.best_y:
            self.score += 1
            self.best_y = self.player.y
            self.frames_passed = 0
            return "New Score"
        return "No New Score"
    
    def whats_nearme(self,player_pos = None):
        if player_pos == None:
            player_pos = self.map.player_pos
        positions = [(player_pos[0]-1,player_pos[1]-1), #TL
                     (player_pos[0],player_pos[1]-1), #TM
                     (player_pos[0]+1,player_pos[1]-1), #TR
                     (player_pos[0]-1,player_pos[1]), #Left
                     (player_pos[0]+1,player_pos[1])] #Right
        car_near = []
        for x,y in positions:
            if not self.map.within_map(x,y):
                car_near.append(-1)
            else:
                car_near.append(1 if self.map.grid[y][x] else 0)

        return car_near
    
    def get_row_info(self,row_index=None):
        if row_index == None:
            row_index = self.map.player_pos[1]
        type = 0
        direction = -1
        for car_row in carRows.keys():
            if row_index == car_row:
                type = 1
                direction = carRows[car_row][0]
        return type,direction
    
    def reward_function(self,action,advanced_foward):
        reward = 0
        done = 0

        #Death Or Win Or Alive
        if self.player_died:
            reward -= 100
            done = 1
            self.refresh()
        elif self.won:
            reward += 100
            done = 1
            self.refresh()
        else:
            if advanced_foward:
                max_row = (WORLD_H//50) - 1
                bonus = (max_row - self.map.player_pos[1])
                reward += 10 + bonus
        
            if action == 0: #standing still
                reward -= 0.5
            
            if self.map.player_pos[0] == 0 or self.map.player_pos[0] == 10:
                if reward > 0:
                    reward *= 0.5
                else:
                    reward -= 20

        return reward,done
    
def randomize_cars():
    offsetTiming = [21, 30, 45]
    directions = [0,1]
    for row in carRows:
        direction = random.randint(0,1)
        offset = random.randint(0,2)
        carRows[row] = (directions[direction],offsetTiming[offset])

