import pygame
from agent import Agent
from game import Game
import torch

game = Game()
agent = Agent()

EPISODES = 20000

for ep in range(EPISODES):
    state = game.reset()
    done = False

    epsilon_update = True
    hit = 0

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

        action = agent.choose_action(state)

        next_state, reward, done = game.step(action)

        agent.remember(state, action, reward, next_state, done)

        agent.train_step(state, next_state, done, reward, action, epsilon_update)

        if reward == 10:
            hit += 1
            print("Hitted")

        state = next_state

        game.update()

        epsilon_update = False
    agent.replay() 

    print("Episode No: ", ep)
    print("Hit: ", hit)
    print("\n")

torch.save(agent.model.state_dict(), "pong_model.pth")