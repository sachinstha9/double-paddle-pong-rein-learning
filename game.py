import pygame

pygame.init()

WIDTH = 1600
HEIGHT = 1000

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.paddle_width = 20
        self.paddle_height = 200
        self.paddle_color = WHITE

        self.paddle_position_l = [
            50,
            (HEIGHT / 2) - (self.paddle_height / 2)
        ]
        self.paddle_position_r = [
            WIDTH - 50 - self.paddle_width,
            (HEIGHT / 2) - (self.paddle_height / 2)
        ]

        self.ball_size = 25
        self.ball_position = [
            WIDTH / 2,
            HEIGHT / 2
        ]
        self.ball_color = RED

    def draw(self):
        self.screen.fill((0, 0, 0))

        # left paddle
        pygame.draw.rect(self.screen, self.paddle_color, (
            self.paddle_position_l[0],
            self.paddle_position_l[1],
            self.paddle_width,
            self.paddle_height
        ))

        # right paddle
        pygame.draw.rect(self.screen, self.paddle_color, (
            self.paddle_position_r[0],
            self.paddle_position_r[1],
            self.paddle_width,
            self.paddle_height
        ))

        # ball
        pygame.draw.circle(self.screen, self.ball_color, (
            self.ball_position[0],
            self.ball_position[1]
        ), self.ball_size) 

        pygame.display.update()

g = Game()

while True:
    g.draw()