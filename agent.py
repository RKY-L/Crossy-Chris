import torch
import pygame
import random
from crossy_roads import Crossy_roads


BATCH_SIZE = 1000
class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.reward = 0
        self.gamma = 0.9
        self.epsilon = 1
        self.epsilon_decay = 100
        self.actions = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,0]
        self.enviroment = game
        self.memory = []

        self.num_games = 0

        self.model = None
        self.trainer = None
    
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
        if self.num_games % self.epsilon_decay:
            self.epsilon -= 0.1
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            curr_state = torch.tensor(state,dtype=torch.float)
            prediction = self.model.predict(curr_state)
            return torch.argmax(prediction)


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
    while running:
        #RL
        state = agent.get_state()
        action = agent.get_action(state)

        reward = game.play(action)
        done = 0
        if not reward:
            running = False
        elif reward == 0:
            done = 1
            reward = -100
        
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

train()