import torch
import pygame
import random

BATCH_SIZE = 1000
class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.reward = 0
        self.gamma = 0
        self.epsilon = 1
        self.epsilon_decay = 0
        self.actions = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,0]
        self.enviroment = game
        self.memory = []
        self.iterations = 0

        self.model = None
        self.trainer = None
    
    def get_state(self):
        #[car ahead,car behind, car left, car right,row,col]
        state = self.enviroment.car_nearme()
        state.append(self.enviroment.map.player_row())
        state.append(self.enviroment.map.player_col())
        return state
    
    def memorize(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def train(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    
    def batch_train(self):
        if(len(self.memory) > BATCH_SIZE):
            sample = random.sample(self.memory,BATCH_SIZE)
        else:
            sample = self.memory
        
        states,actions,rewards,next_states,dones = zip(*sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def get_action(self):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            #pick best
            pass