import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import random
import math

pygame.init()

WIDTH = 1600
HEIGHT = 1000

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 5000

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT


        self.paddle_width = 20
        self.paddle_height = 200
        self.paddle_color = WHITE
        self.paddle_y_velocity = 10

        self.paddle_position_l = []
        self.paddle_position_r = []

        self.ball_size = 25

        self.ball_position = []
        self.ball_color = RED
        self.ball_velocity = []

        self.reset()

    def reset(self):
        self.paddle_position_l = [
            50,
            (HEIGHT / 2) - (self.paddle_height / 2)
        ]
        self.paddle_position_r = [
            WIDTH - 50 - self.paddle_width,
            (HEIGHT / 2) - (self.paddle_height / 2)
        ]

        self.ball_position = [
            WIDTH / 2,
            HEIGHT / 2
        ]

        self.ball_velocity = [10, 8]

        return self.get_state()

    def get_state(self):
        dis_b_x_l = max(((self.ball_position[0] - (self.ball_size)) - (self.paddle_position_l[0] + self.paddle_width)) / WIDTH - (self.paddle_position_l[0] + self.paddle_width), 0) 
        dis_b_y_l = (self.ball_position[1] - (self.paddle_position_l[1] + (self.paddle_height / 2)) + HEIGHT) / HEIGHT * 2

        dis_b_w_y_b = (HEIGHT - self.ball_position[1]) / HEIGHT 
        
        h = math.sqrt(self.ball_velocity[0] ** 2 + self.ball_velocity[1] ** 2)
        
        ang_b_y = (math.asin(self.ball_velocity[0] / h) + (math.pi / 2)) / math.pi
        ang_b_x = (math.asin(self.ball_velocity[1] / h) + (math.pi / 2)) / math.pi

        return [
            dis_b_x_l,
            dis_b_y_l,
            dis_b_w_y_b,
            ang_b_y,
            ang_b_x,
            (self.ball_velocity[0] + 10) / 20,
            (self.ball_velocity[1] + 8) / 16,
            (self.paddle_y_velocity + 10) / 20
        ]
    
    def step(self, action):
        if action == 0:
            self.paddle_position_l[1] -= self.paddle_y_velocity
        elif action == 2:
            self.paddle_position_l[1] += self.paddle_y_velocity

        done = False

        reward = 0

        paddle_left = self.paddle_position_l[0]
        paddle_right = self.paddle_position_l[0] + self.paddle_width
        paddle_top = self.paddle_position_l[1]
        paddle_bottom = self.paddle_position_l[1] + self.paddle_height

        ball_left = self.ball_position[0] - self.ball_size
        ball_right = self.ball_position[0] + self.ball_size
        ball_top = self.ball_position[1] - self.ball_size
        ball_bottom = self.ball_position[1] + self.ball_size

        if ball_right >= paddle_left and ball_left <= paddle_right:
            if ball_bottom >= paddle_top and ball_top <= paddle_bottom:
                reward = 10
        
        if self.ball_position[0] + (self.ball_size) < 0:
            reward = -10
            done = True

        if self.paddle_position_l[1] < 0 or self.paddle_position_l[1] + self.paddle_height > HEIGHT:
            reward = -10

        return self.get_state(), reward, done
            
    def draw(self):
        SCREEN.fill((0, 0, 0))

        # left paddle
        pygame.draw.rect(SCREEN, self.paddle_color, (
            self.paddle_position_l[0],
            self.paddle_position_l[1],
            self.paddle_width,
            self.paddle_height
        ))

        # right paddle
        pygame.draw.rect(SCREEN, self.paddle_color, (
            self.paddle_position_r[0],
            self.paddle_position_r[1],
            self.paddle_width,
            self.paddle_height
        ))

        # ball
        pygame.draw.circle(SCREEN, self.ball_color, (
            self.ball_position[0],
            self.ball_position[1]
        ), self.ball_size) 

        CLOCK.tick(FPS)

        pygame.display.update()

    def update(self):
        self.ball_position[0] += self.ball_velocity[0]
        self.ball_position[1] += self.ball_velocity[1]

        if self.ball_position[0] + (self.ball_size) > WIDTH:
            self.ball_position[0] = WIDTH - (self.ball_size)
            self.ball_velocity[0] *= -1
        elif self.ball_position[1] + (self.ball_size) > HEIGHT:
            self.ball_position[1] = HEIGHT - (self.ball_size)
            self.ball_velocity[1] *= -1
        elif self.ball_position[1] - (self.ball_size) <= 0:
            self.ball_position[1] = self.ball_size
            self.ball_velocity[1] *= -1

        paddle_left = self.paddle_position_l[0]
        paddle_right = self.paddle_position_l[0] + self.paddle_width
        paddle_top = self.paddle_position_l[1]
        paddle_bottom = self.paddle_position_l[1] + self.paddle_height

        ball_left = self.ball_position[0] - self.ball_size
        ball_right = self.ball_position[0] + self.ball_size
        ball_top = self.ball_position[1] - self.ball_size
        ball_bottom = self.ball_position[1] + self.ball_size

        if ball_right >= paddle_left and ball_left <= paddle_right:
            if ball_bottom >= paddle_top and ball_top <= paddle_bottom:
                self.ball_velocity[0] *= -1
                self.ball_position[0] = paddle_right + self.ball_size  # avoid sticking


        self.draw()

