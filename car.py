import random
from map import Map

class Car:
    def __init__(self, road):
        self.direction = 0
        self.x = 0
        self.y = road * 50
        self.frame_count = 0
    
    def update(self, map):
        """Move the car by 50 pixels every 2 frames along the X axis."""
        self.frame_count += 1
        if self.frame_count % 4 == 0  and self.direction == 0:
            new_x = self.x - 50
            map.updatecarpos(self.y, self.x,new_x)
            self.x = new_x
        elif self.frame_count % 4 == 0 and self.direction == 1:
            new_x = self.x  + 50
            map.updatecarpos(self.y, self.x,new_x)
            self.x = new_x
            



    