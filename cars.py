import random
import pygame

listofCars = []

class cars:
    def __init__(self):
        self.x_coord = 0
        self.y_coord = 0
        self.direction = 1 # 1 for right, -1 for left
        self.speed = 2 # 1 is slow. 2 is fast
        self.type = 0 # 0 for car, 1 for truck

def draw_cars(screen,  car):
    global listofCars
    for car in listofCars:
        pygame.draw.rect(screen, (255,0,0),(car.x_coord, car.y_coord, 100, 50))    

def spawn():
    global listofCars
    new_car = cars()
    new_car.y_coord = 2
    new_car.x_coord = 100
    new_car.type = 0
    listofCars.append(new_car)

def updatecar_pos():
    global listofCars
    for car in listofCars:
        if car.direction == 1:
            car.x_coord += 50
        else:
            car.x_coord -= 50

