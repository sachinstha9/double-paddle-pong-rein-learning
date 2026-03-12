import random
import torch
import torch.optim as optim
import torch.nn as nn
from model import Qnet

device = "cuda" if torch.cuda.is_available() else "cpu"

class Agent:
    def __init__(self):
        self.model = Qnet().to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        self.gamma = 0.9

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 2)
        
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)

        with torch.no_grad():
            q = self.model(state).to(device)
        
        return torch.argmax(q).item()
    
    def train(self, state, next_state, done, reward, action, epsilon_update):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0).to(device)

        q = self.model(state).to(device)
        with torch.no_grad():
            next_q = self.model(next_state).to(device)

        target = q.clone().detach()

        if done:
            target[0][action] = reward
        else:
            target[0][action] = reward + self.gamma * torch.max(next_q)

        loss = nn.SmoothL1Loss()(q, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if epsilon_update and self.epsilon >= self.epsilon_min:
            self.epsilon *= self.epsilon_decay 
            print("Epsilon: ", self.epsilon)

