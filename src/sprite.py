import pygame
from math import sqrt, pow

MOVEMENT_SPEED = 2.0

class Sprite:
    image: pygame.Surface
    x: int
    y: int
    width: int
    height: int

    def __init__(self, path: str, x, y, width, height):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self):
        pygame.display.get_surface().blit(self.image, (self.x, self.y))
        return self

    def moveTo(self, x, y):
        self.x = x
        self.y = y
        return self

    def moveBy(self, x, y):
        if sqrt(pow(x, 2) + pow(y, 2)) > MOVEMENT_SPEED:
            a = sqrt(pow(MOVEMENT_SPEED, 2) / 2)
            x = a * -1 if x < 0 else 1
            y = a * -1 if y < 0 else 1
        self.x += x
        self.y += y
        return self
