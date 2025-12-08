import torch
import pygame
import random
from crossy_roads import Crossy_roads
import time
from model import ANN, QTrainer
from collections import deque
BATCH_SIZE = 1000
class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.gamma = 0.9
        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.actions = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,0]
        self.enviroment = game
        self.memory = deque(maxlen=100000)

        self.num_games = 0

        self.model = ANN(8,256,5)
        self.trainer = QTrainer(self.model, lr = 0.001, gamma = self.gamma)
    
    def get_state(self):
        #[car ahead,car behind, car left, car right,row,col]
        state = self.enviroment.car_nearme()
        state.append(self.enviroment.map.player_row())
        state.append(self.enviroment.map.player_col())
        return state
    
    def memorize(self,state,action,reward,new_state,done):
        self.memory.append((state,action,reward,new_state,done))

    def train(self,state,action,reward,new_state,done):
        self.trainer.train_step(state,action,reward,new_state,done)
    
    def batch_train(self):
        if(len(self.memory) > BATCH_SIZE):
            sample = random.sample(self.memory,BATCH_SIZE)
        else:
            sample = self.memory
        
        states,actions,rewards,new_states,dones = zip(*sample)
        self.trainer.train_step(states,actions,rewards,new_states,dones)

    def get_action(self,state):
        if self.num_games % 2 == 0 and self.num_games > 0:
            self.epsilon *= self.epsilon_decay
        if random.random() < self.epsilon:
            return random.randint(0,len(self.actions)-1)
        else:
            curr_state = torch.tensor(state,dtype=torch.float)
            prediction = self.model.forward(curr_state)
            return torch.argmax(prediction).item()

def train():
    pygame.init()
    pygame.display.set_caption("Crossy Chris")
    normal_logo = pygame.image.load("./normal_logo.png")
    pygame.display.set_icon(normal_logo)
    clock = pygame.time.Clock()
    running = True
    game = Crossy_roads()
    agent = Agent(game)
    high_score = 0
    time.sleep(2)
    while running:
        #RL
        state = agent.get_state()
        action = agent.actions[agent.get_action(state)]

        reward,done = game.play(action)
        if reward is None:
            running = False
        
        new_state = agent.get_state()
        agent.train(state, action, reward, new_state, done)

        agent.memorize(state,action,reward,new_state,done)
        
        if done:
            if high_score < game.highscore:
                agent.model.save()
                high_score = game.highscore
            agent.num_games += 1
            agent.batch_train()

        game.frames_passed += 1
        clock.tick(30)

if __name__ == '__main__':
    train()