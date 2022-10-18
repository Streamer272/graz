import pygame
from sprite import Sprite, MOVEMENT_SPEED

from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Graz")

player = Sprite("cyborg.png", 50, 50, 64, 64)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    keys = pygame.key.get_pressed()
    x = 0
    y = 0
    if keys[K_w] or keys[K_UP]:
        y -= 1
    if keys[K_a] or keys[K_LEFT]:
        x -= 1
    if keys[K_s] or keys[K_DOWN]:
        y += 1
    if keys[K_d] or keys[K_RIGHT]:
        x += 1
    if keys[K_LSHIFT]:
        x /= 2
        y /= 2
    player.move_by(x * MOVEMENT_SPEED, y * MOVEMENT_SPEED)

    screen.fill((255, 255, 255))
    player.show()
    pygame.display.flip()
    clock.tick(60)
