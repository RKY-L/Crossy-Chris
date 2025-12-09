import torch
import pygame
import random
from game.crossy_roads import *
import time
from model.model import ANN, QTrainer
from collections import deque
from model.helper import plot
BATCH_SIZE = 100
class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01
        self.actions = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,0]
        self.enviroment = game
        self.memory = deque(maxlen=100000)

        self.num_games = 0

        self.model = ANN(10,256,5)
        self.trainer = QTrainer(self.model, lr = 0.001, gamma = self.gamma)

        self.speed = 5
    
    def get_state(self):
        #[car ahead left, car ahead middle, car ahead right,car behind, car left, car right,row,col,row_car_direction,row_car_speed]
        state = self.enviroment.car_nearme()
        state.append(self.enviroment.map.player_row())
        state.append(self.enviroment.map.player_col())
        row_dir,row_speed = self.enviroment.get_row_info()
        state.append(row_dir)
        state.append(row_speed)
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
        if self.num_games % 10 == 0 and self.num_games > 0:
            self.epsilon= max(self.min_epsilon, self.epsilon_decay * self.epsilon)
        if random.random() < self.epsilon:
            action = random.randint(0,len(self.actions)-1)
        else:
            curr_state = torch.tensor(state,dtype=torch.float)
            prediction = self.model.forward(curr_state)
            print(prediction)
            action = torch.argmax(prediction).item()
        return action

def train():
    pygame.init()
    pygame.display.set_caption("Crossy Chris")
    normal_logo = pygame.image.load("./game/normal_logo.png")
    pygame.display.set_icon(normal_logo)
    clock = pygame.time.Clock()
    running = True
    #randomize_cars()
    game = Crossy_roads()
    agent = Agent(game)
    high_score = 0
    time.sleep(1)
    player_frames =  0

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    while running:
        #RL
        if player_frames % agent.speed == 0:
            state = agent.get_state()
            print(state)
            action = agent.actions[agent.get_action(state)]

        reward,done = game.play(action)
        if reward is None:
            running = False
        if player_frames % agent.speed == 0:
            new_state = agent.get_state()
            agent.train(state, action, reward, new_state, done)

            agent.memorize(state,action,reward,new_state,done)
        
        if done:
            if high_score < game.highscore:
                agent.model.save()
                high_score = game.highscore
            agent.num_games += 1
            agent.batch_train()
            player_frames = 0

            #plotting
            print('Game', agent.num_games, 'Score', game.prev_score, 'Record:', high_score)

            plot_scores.append(game.prev_score)
            total_score += game.prev_score
            mean_score = total_score / agent.num_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


        action = 0
        player_frames += 1
        game.frames_passed += 1
        clock.tick(30)

if __name__ == '__main__':
    #train()
    model = ANN(10,256,5)
    model.load_state_dict(torch.load("./model/model.pth", map_location="cpu"))
    model.eval()
    state = [1 ,1, 1, 0, 0, 0, 26, 5,-1,25]
    curr_state = torch.tensor(state,dtype=torch.float)
    prediction = model.forward(curr_state)
    action = torch.argmax(prediction).item()

    print("Q-values:", prediction)
    print("Predicted action:", action)