import random
from game.map import Map

class Car:
    def __init__(self, road):
        self.x = 0
        self.y = road * 50
        self.frame_count = 0
        self.direction = -1
        self.car_img = None
    
    def update(self, map):
        self.frame_count += 1
        if self.frame_count % 3 == 0:
            self.x = map.updatecarpos(self.x, self.y,self.direction)
            



    