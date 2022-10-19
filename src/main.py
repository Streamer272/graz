import pygame
from pygame.locals import *

from sprite import MOVEMENT_SPEED
from characters import Cyborg

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Graz")

sprites = []
player = Cyborg(x=100, y=100)
sprites.append(player)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            bullet = player.shoot(event.pos)
            sprites.append(bullet)

    keys = pygame.key.get_pressed()

    if keys[K_q]:
        player.ability()

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
    for sprite in sprites:
        if sprite is None:
            continue

        sprite.update()
        if sprite.destroy:
            sprites.pop(sprites.index(sprite))
            continue
        sprite.show()
    pygame.display.flip()
    clock.tick(60)
