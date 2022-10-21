import pygame
from pygame.locals import *

from game.gsprite import MOVEMENT_SPEED, FONT, GSprite
from game.gcharacter import GCyborg, GCharacter
from game.gweapon import GBullet
from game.variables import sprites, teams
from game import socket
from shared.find import find
from shared.sprite import Sprite
from shared.team import Team


def main():
    global teams, characters, sprites

    pygame.init()
    socket.connect()
    socket.send("team_get")
    teams = socket.recieve()
    socket.send("character_get")
    characters = socket.recieve()

    screen = pygame.display.set_mode((512, 512), pygame.RESIZABLE)
    pygame.display.set_caption("Graz")

    # TODO: fix
    # player = GCyborg(x=100, y=100)
    # sprites.append(player)
    team: Team | None = None
    character: GCharacter | None = None
    select_sprites = []

    for i in range(len(teams)):
        surface = FONT.render(teams[i]["name"], True, teams[i]["color"])
        x = (i + 1) * 100
        y = 100
        select_sprite = Sprite().init_sprite(x, y, surface.get_width(), surface.get_height())
        select_sprite.select_id = teams[i]["id"]
        select_sprites.append(select_sprite)
        sprites.append(GSprite().init_gsprite(surface, x, y))

    running = True
    clock = pygame.time.Clock()

    while running:
        print(f"team {team}")
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_position = event.pos

                if len(select_sprites) == 0:
                    # bullet = player.shoot(event.pos)
                    # if bullet is not None:
                    #     sprites.append(bullet)
                    pass

                else:
                    for select_sprite in select_sprites:
                        if not Sprite().init_sprite(
                                mouse_position[0],
                                mouse_position[1],
                                1, 1
                        ).collides_with(select_sprite):
                            continue

                        if team is None:
                            team = find(teams, lambda x: x["id"] == select_sprite.select_id)
                        elif character is None:
                            character = find(characters, lambda x: x["id"] == select_sprite.select_id)
                        sprites = []
                        select_sprites = []
                        break

        keys = pygame.key.get_pressed()

        if keys[K_q]:
            # bullet = player.ability(pygame.mouse.get_pos())
            # sprites.append(bullet)
            pass

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
        # player.move_by(x * MOVEMENT_SPEED, y * MOVEMENT_SPEED)

        screen.fill((255, 255, 255))
        for select_sprite in sprites:
            if select_sprite is None:
                continue

            select_sprite.update()
            if select_sprite.destroy:
                sprites.pop(sprites.index(select_sprite))
                continue

        for i in range(len(sprites)):
            if sprites[i] is None:
                continue

            for j in range(i + 1, len(sprites)):
                if i == j or sprites[j] is None:
                    continue
                if not sprites[i].collides_with(sprites[j]):
                    continue

                bullet: GBullet | None = None
                character: GCharacter | None = None
                if isinstance(sprites[i], GBullet):
                    bullet = sprites[i]
                elif isinstance(sprites[i], GCharacter):
                    character = sprites[i]
                if isinstance(sprites[j], GBullet):
                    bullet = sprites[j]
                elif isinstance(sprites[j], GCharacter):
                    character = sprites[j]
                if bullet is None or character is None:
                    continue

                if bullet.shot_by == character.id:
                    continue

                bullet.destroy = True
                character.take_damage(bullet.damage)

        for select_sprite in sprites:
            if select_sprite is None:
                continue

            select_sprite.show()
        pygame.display.flip()
        clock.tick(60)
