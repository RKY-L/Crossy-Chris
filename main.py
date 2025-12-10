import pygame
from game.crossy_roads import *
from agent import *

pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./game/normal_logo.png")
pygame.display.set_icon(normal_logo)
clock = pygame.time.Clock()
running = True
game = Crossy_roads()

#Loading Model
agent = Agent(game)
if os.path.exists('./model/model.pth'):
    agent.model.load_state_dict(torch.load('./model/model.pth'))
agent.epsilon = 0.01
AItoggle = False

high_score = 0
time.sleep(1)
player_frames =  0
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
        
        if done:
            agent.num_games += 1
            player_frames = 0
            if game.prev_score > 13:
                above_halfway += 1

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

pygame.quit()