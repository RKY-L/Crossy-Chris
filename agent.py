import torch
import pygame
import random
from game.crossy_roads import *
import time
from model.model import ANN, QTrainer
from collections import deque
from model.helper import plot
import os
BATCH_SIZE = 100
MEMORY_SIZE = 100000
class Agent:
    def __init__(self,game):
        #Running into a car = -100 reward
        #Getting hit by a car = -100 reward
        #Standing still for 210 frames = -100 reward
        #Making a new score = +10 reward
        #Touching finish line = +100 Reward
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.9995
        self.min_epsilon = 0.01
        self.actions = [0,pygame.K_w,pygame.K_a,pygame.K_d]
        self.enviroment = game
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.num_games = 0

        self.model = ANN(15,128,64,4)
        self.trainer = QTrainer(self.model, lr = 0.001, gamma = self.gamma)
    
    def get_state(self):
        #[TL,TM,TR,L,R,
        # player_row,player_col,
        # row_type,direction,
        # next_row_type,next_row_direction,
        # next_next_rt, next_next_rd,
        # nnn_rt, nnn_rd]
        state = self.enviroment.whats_nearme()
        state.append(self.enviroment.map.player_row()/28.0)
        state.append(self.enviroment.map.player_col()/10.0)
        row_type,row_dir = self.enviroment.get_row_info()
        state.append(row_type)
        state.append(row_dir)
        row_type,row_dir = self.enviroment.get_row_info(self.enviroment.map.player_pos[1]-1)
        state.append(row_type)
        state.append(row_dir)
        row_type,row_dir = self.enviroment.get_row_info(self.enviroment.map.player_pos[1]-2)
        state.append(row_type)
        state.append(row_dir)
        row_type,row_dir = self.enviroment.get_row_info(self.enviroment.map.player_pos[1]-3)
        state.append(row_type)
        state.append(row_dir)
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

    def get_prediction(self,state):
        if random.random() < self.epsilon:
            prediction = random.randint(0,len(self.actions)-1)
        else:
            curr_state = torch.tensor(state,dtype=torch.float)
            prediction = self.model.forward(curr_state)
            prediction = torch.argmax(prediction).item()
        return prediction

def train():
    pygame.init()
    pygame.display.set_caption("Crossy Chris")
    clock = pygame.time.Clock()
    running = True
    #randomize_cars()
    game = Crossy_roads()

    #Loading Model
    agent = Agent(game)
    if os.path.exists('./model/model.pth'):
        agent.model.load_state_dict(torch.load('./model/model.pth'))

    high_score = 0
    time.sleep(1)
    player_frames =  0
    AItoggle = True
    scores = []
    mean_scores = []
    total_score = 0
    above_halfway = 0
    above_halfway_percent = []
    ma_100 = deque(maxlen=100)
    avg_ma_100 = []
    while running:
        #RL
        if AItoggle == True:
            before_state = agent.get_state()
            prediction = agent.get_prediction(before_state)
            action = agent.actions[prediction]

            rd,AItoggle = game.play(AItoggle, action)
            reward = rd[0]
            done = rd[1]
            if reward is None:
                running = False
            after_state = agent.get_state()
            print(before_state, prediction,reward,done,after_state)
            agent.train(before_state, prediction, reward, after_state, done)
            agent.memorize(before_state,prediction,reward,after_state,done)
            
            if done:
                if high_score < game.highscore or game.prev_score == 26:
                    agent.model.save()
                    high_score = game.highscore
                agent.num_games += 1
                agent.batch_train()
                player_frames = 0
                if game.prev_score > 13:
                    above_halfway += 1
                if agent.num_games % 1 == 0 and agent.num_games > 0:
                    agent.epsilon= max(agent.min_epsilon, agent.epsilon_decay * agent.epsilon)

                #plotting
                scores.append(game.prev_score)
                ma_100.append(game.prev_score)
                total_score += game.prev_score
                mean_scores.append(total_score / agent.num_games)
                above_halfway_percent.append((above_halfway/agent.num_games)*26)
                avg_ma_100.append(sum(ma_100)/len(ma_100))
                plot(scores, mean_scores,above_halfway_percent,avg_ma_100)
        else:
            AItoggle = game.play(AItoggle, None)[1]

        player_frames += 1
        game.frames_passed += 1
        clock.tick(30)

if __name__ == '__main__':
    train()
    '''model = ANN(11,64,32,4)
    model.load_state_dict(torch.load("./model/model.pth", map_location="cpu"))
    model.eval()
    #[TL,TM,TR,L,R,player_row,player_col,row_type,direction,next_row_type,next_row_direction]
    state = [0 ,0, 0, 0, 0, 26, 5,0,-1,1,0]
    curr_state = torch.tensor(state,dtype=torch.float)
    prediction = model.forward(curr_state)
    action = torch.argmax(prediction).item()

    print("Q-values:", prediction)
    print("Predicted action:", action)'''