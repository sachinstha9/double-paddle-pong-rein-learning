import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
from model import Qnet

device = "cuda" if torch.cuda.is_available() else "cpu"

class Agent:
    def __init__(self, state_size=8, action_size=3):
        self.state_size = state_size
        self.action_size = action_size

        self.model = Qnet().to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.SmoothL1Loss()

        self.epsilon = 1.0  
        self.gamma = 0.9
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1

        self.memory = deque(maxlen=100000)
        self.batch_size = 64

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)

        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train_step(self, state, next_state, done, reward, action, epsilon_update):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0).to(device)

        q = self.model(state)
        target = q.detach().clone()

        with torch.no_grad():
            next_q = self.model(next_state)

        if done:
            target[0][action] = reward
        else:
            target[0][action] = reward + self.gamma * torch.max(next_q).item()

        loss = self.loss_fn(q, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if epsilon_update and self.epsilon >= self.epsilon_min:
            self.epsilon *= self.epsilon_decay 


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states = []
        targets = []

        for state, action, reward, next_state, done in batch:
            state_tensor = torch.tensor(state, dtype=torch.float32).to(device)
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32).to(device)

            q = self.model(state_tensor.unsqueeze(0))
            target = q.detach().clone()

            with torch.no_grad():
                next_q = self.model(next_state_tensor.unsqueeze(0))

            if done:
                target[0][action] = reward
            else:
                target[0][action] = reward + self.gamma * torch.max(next_q).item()

            states.append(state_tensor)
            targets.append(target.squeeze(0))

        states = torch.stack(states).to(device)
        targets = torch.stack(targets).to(device)

        predictions = self.model(states)
        loss = self.loss_fn(predictions, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()