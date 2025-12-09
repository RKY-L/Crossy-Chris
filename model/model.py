import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as activeF
import os

class ANN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, value):
        value = activeF.sigmoid(self.layer1(value))
        value = self.layer2(value)
        return value
    
    def save(self, file_name = 'model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
    

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.lossfunct = nn.MSELoss()

    def train_step(self, state, action, reward, new_state, done):
        state = torch.tensor(state, dtype = torch.float)
        new_state = torch.tensor(new_state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.long)
        reward = torch.tensor(reward, dtype = torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            new_state = torch.unsqueeze(new_state, 0)
            action = torch.unsqueeze(action,0)
            reward = torch.unsqueeze(reward,0)
            done = (done, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                #Update Q table from slides. 
                Q_new = reward[idx] + self.gamma * torch.max(self.model(new_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new
        

        self.optimizer.zero_grad()
        loss = self.lossfunct(target, pred)
        loss.backward()
        self.optimizer.step()