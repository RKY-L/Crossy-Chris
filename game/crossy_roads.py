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
carRows = {25:(-1,25), 23:(1,30), 22:(-1,50), 19:(-1,30), 15:(1,30), 13:(-1,25), 12:(1,50), 11:(1,30), 9:(-1,25), 8:(1,50), 5:(-1,25), 1:(1,30)}
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
                car.car_img = car_left_img if car.direction == -1 else car_right_img
                if car.direction == -1: #spawn right move left
                    car.x = 650
                else: #spawn left move right
                    car.x = -100

    
    def play(self,action = None):
        advanced_foward = False
        cars_infront = self.car_nearme()[:3]
        prev_pos = self.map.player_pos

        #Moving Cars in game
        self.spawncars()
        self.car_timer += 1

        new_cars = []
        for car in self.cars:
            if car.x > -150 or car.x > 650:
                new_cars.append(car)
            car.update(self.map)
        self.cars = new_cars
        #==============================================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif not action and event.type == pygame.KEYDOWN:
                action = event.key
        if action:
            if self.key_pressed(action) == "New Score":
                advanced_foward = True

        self.camera.update_camera(0,0,self.screen,self.world)
        self.screen.blit(chicken, (self.player.x, self.player.y - self.camera.y))


        for car in self.cars:
            self.screen.blit(car.car_img, (car.x, car.y - self.camera.y))
        self.screen.blit(pygame.font.SysFont(None, 100).render(str(self.score), True, (255, 255, 255)), (25, 25))
        self.screen.blit(pygame.font.SysFont(None, 50).render("Highscore: " + str(self.highscore), True, (255, 255, 255)), (10, 850))
        pygame.display.update()
        pygame.display.flip()



        
        return self.reward_function(action,prev_pos,advanced_foward,cars_infront)
    
    def key_pressed(self,key):
        self.player.key_pressed(self.map,key)
        self.camera.update_camera(key,self.player.y,self.screen,self.world)
        if self.player.y < self.best_y:
            self.score += 1
            self.best_y = self.player.y
            self.frames_passed = 0
            return "New Score"
        return "No New Score"
    
    def car_nearme(self,player_pos = None):
        if player_pos == None:
            player_pos = self.map.player_pos
        car_near = [
            1 if self.map.within_map(player_pos[0]-1,player_pos[1]-1) and self.map.grid[player_pos[1]-1][player_pos[0]-1] else 0, #TL
            1 if self.map.within_map(player_pos[0],player_pos[1]-1) and self.map.grid[player_pos[1]-1][player_pos[0]] else 0, #TM
            1 if self.map.within_map(player_pos[0]+1,player_pos[1]-1) and self.map.grid[player_pos[1]-1][player_pos[0]+1] else 0, #TR
            1 if self.map.within_map(player_pos[0]-1,player_pos[1]) and self.map.grid[player_pos[1]][player_pos[0]-1] else 0, #Left
            1 if self.map.within_map(player_pos[0]+1,player_pos[1]) and self.map.grid[player_pos[1]][player_pos[0]+1] else 0, #Right
                    ] 
        return car_near
    def get_row_info(self):
        row = self.map.player_pos[1]
        type = 0
        direction = 0
        speed = 0
        for car_row in carRows.keys():
            if row == car_row:
                type = 1
                direction = carRows[car_row][0]
                speed = carRows[car_row][1]
        return type,direction,speed
    
    def reward_function(self,action,prev_pos,advanced_foward,cars_infront):
        reward = 0
        done = 0
        if(self.frames_passed > 210): #Death for standing still too long
            self.player_died = True
        
        #Cars infront
        prev_cnme = self.car_nearme(prev_pos)
        prev_row = prev_pos[1]
        prev_row_infront = prev_row - 1
        if prev_row_infront in carRows:
            if carRows[prev_row_infront][0] == -1: #Cars moving <-
                if prev_cnme[2] == 1 and action == pygame.K_w:
                    reward -= 1000
                elif cars_infront[2] == 0 and action == pygame.K_w:
                    reward += 10
            elif carRows[prev_row_infront][0] == 1: #Cars moving ->
                if prev_cnme[0] == 1 and action == pygame.K_w:
                    reward -= 1000
                elif cars_infront[0] and action == pygame.K_w:
                    reward += 10

        #cars to the side
        if prev_row in carRows:
            if carRows[prev_row][0] == -1: #Cars moving <-
                if prev_cnme[4] == 1 and action == pygame.K_d or action == 0: #car is on the right
                    print("Car from the right ran me over")
                    reward -= 1000
                else:
                    reward += 10
            elif carRows[prev_row][0] == 1: #Cars moving ->
                if prev_cnme[3] == 1 and action == pygame.K_a or action == 0: #car is on the left
                    print("Car from the left ran me over")
                    reward -= 1000
                else:
                    reward += 10

        #Negative reward for edge of map
        col = self.map.player_pos[0]
        if col < 2 or col > 8:
            reward -= 50

        if advanced_foward:
            reward += self.map.player_pos[1] * 5
        #Death Or Win
        if self.player_died:
            reward -= 100
            done = 1
            self.refresh()

        if self.won:
            reward += 100
            done = 1
            self.refresh()
        
        return reward,done
    
def randomize_cars():
    offsetTiming = [21, 30, 45]
    directions = [-1,1]
    for row in carRows:
        direction = random.randint(0,1)
        offset = random.randint(0,2)
        carRows[row] = (directions[direction],offsetTiming[offset])

