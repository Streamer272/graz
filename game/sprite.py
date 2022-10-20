import pygame
from math import sqrt, pow

from shared import sprite

MOVEMENT_SPEED = 2.0


def load_image(path: str, width: int, height: int):
    image = pygame.image.load(f"./game/images/{path}")
    image = pygame.transform.scale(image, (width, height))
    return image


class Sprite(sprite.Sprite):
    surface: pygame.Surface
    destroy: bool

    def __init__(self, surface: pygame.Surface, x: int, y: int):
        self.surface = surface
        self.x = x
        self.y = y
        self.destroy = False

    def show(self):
        pygame.display.get_surface().blit(self.surface, (self.x, self.y))

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, x, y):
        if sqrt(pow(x, 2) + pow(y, 2)) > MOVEMENT_SPEED:
            a = sqrt(pow(MOVEMENT_SPEED, 2) / 2)
            x = a * (-1.0 if x < 0 else 1.0)
            y = a * (-1.0 if y < 0 else 1.0)
        self.x += x
        self.y += y

    def collides_with(self, other):
        return not any([
            other.x + other.surface.get_width() < self.x,
            other.y + other.surface.get_height() < self.y,
            other.x > self.x + self.surface.get_width(),
            other.y > self.y + self.surface.get_height()
        ])

    def update(self):
        pass
