import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 800

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Game:
    def __init__(self, side="left"):
        self.width = WIDTH
        self.height = HEIGHT
        self.side = side

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.paddle_width = 20
        self.paddle_height = 150
        self.paddle_position = [
            50 if self.side == "left" else WIDTH - 50 - self.paddle_width ,
            HEIGHT - (self.paddle_height / 2)
        ]
        self.paddle_color = WHITE

        self.ball_size = 20
        self.ball_position = [
            WIDTH / 2,
            HEIGHT / 2
        ]
        self.ball_color = RED