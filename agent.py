import torch
import pygame
import random

class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.reward = 0
        self.gamme = 0
        self.epsilon = 1
        self.epsilon_decay = 0
        self.actions = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]
        self.state = 25
        self.enviroment = game
        self.memory = []
        self.iterations = 0
    
    def get_state(self):
        self.state = self.enviroment.get_row()
    
    def store(self,state,action,reward):
        self.memory.append((state,action,reward))
    
    def get_action(self):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            #pick best
            pass