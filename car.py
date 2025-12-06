import random
from map import Map

class Car:
    def __init__(self, road):
        self.x = 650
        self.y = road * 50
        self.frame_count = 0
    
    def update(self, map):
        self.frame_count += 1
        if self.frame_count % 4 == 0:
            new_x = self.x - 50
            if not map.check_collision(self.y,new_x):
                map.updatecarpos(self.y, self.x,new_x)
                self.x = new_x
            



    