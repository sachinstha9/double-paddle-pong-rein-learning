import pygame
from agent import Agent
from game import Game

game = Game()
agent = Agent()

EPISODES = 5000

for ep in range(EPISODES):
    state = game.reset()
    done = False

    epsilon_update = True

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

        action = agent.choose_action(state)

        next_state, reward, done = game.step(action)

        agent.train(state, next_state, done, reward, action, epsilon_update)

        state = next_state

        game.update()

        if reward == 10:
            print("##############################################" \
            "##############################################" \
            "##############################################" \
            "##############################################" \
            "##############################################")
            
        else:
            print("----------------------------------------------")

        epsilon_update = False

    print("Episode No: ", ep)