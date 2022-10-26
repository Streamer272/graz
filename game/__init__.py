from threading import Thread

import pygame
from pygame.locals import *

from game import socket
from game.gcharacter import GCyborg, GCharacter
from game.gsprite import FONT, GSprite, load_image
from game.gweapon import GBullet
from game.variables import sprites, teams
from shared.find import find
from shared.sprite import Sprite
from shared.team import Team


def main():
    global teams, characters, sprites

    pygame.init()
    socket.connect()
    socket.send("team_get")
    teams_raw = socket.recieve()
    teams = [Team(team["name"], team["color"]).set_id(team["id"]) for team in teams_raw]
    socket.send("character_get")
    characters = socket.recieve()

    screen = pygame.display.set_mode((512, 512), pygame.RESIZABLE)
    pygame.display.set_caption("Graz")

    # TODO: fix
    # player = GCyborg(x=100, y=100)
    # sprites.append(player)
    team: Team | None = None
    character: str | None = None
    select_sprites = []

    for i in range(len(teams)):
        surface = FONT.render(teams[i].name, True, teams[i].color)
        x = (i + 1) * 100
        y = 100
        sprite = Sprite().init_sprite(x, y, surface.get_width(), surface.get_height())
        sprite.select_id = teams[i].id
        select_sprites.append(sprite)
        sprites.append(GSprite().init_gsprite(surface, x, y))

    running = True
    receiving = False
    clock = pygame.time.Clock()

    def handle(data):
        if not data.get("event"):
            return
        value = data.get("value")
        match data["event"]:
            case "sprite_create":
                try:
                    find(sprites, lambda x: x.id == value["id"])
                    return
                except Exception:
                    pass

                sprite = GSprite().init_gsprite(
                    load_image(
                        value["path"],
                        value["width"],
                        value["height"]
                    ),
                    value["x"],
                    value["y"]
                )
                sprite.id = value["id"]
                sprites.append(sprite)
            case "sprite_move":
                sprite = find(sprites, lambda x: x.id == value["id"])
                sprite.move_to(value["x"], value["y"])
            case "sprite_destroy":
                sprite = find(sprites, lambda x: x.id == value["id"])
                sprites.pop(sprites.index(sprite))

    def take_input():
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

        if x == 0 and y == 0:
            return

        socket.send("player_move", (x, y))

    def receive():
        while True:
            data = socket.recieve()
            if not data.get("event"):
                continue
            handle(data)

    while running:
        ready = team is not None and character is not None
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
                    for sprite in select_sprites:
                        if not Sprite().init_sprite(
                                mouse_position[0],
                                mouse_position[1],
                                1, 1
                        ).collides_with(sprite):
                            continue

                        select_sprites = []
                        sprites = []

                        if team is None:
                            team = find(teams, lambda x: x.id == sprite.select_id)
                            socket.send("team_set", team.id)
                            for i in range(len(characters)):
                                surface = FONT.render(characters[i], True, (0, 0, 0))
                                x = (i + 1) * 100
                                y = 100
                                sprite = Sprite().init_sprite(x, y, surface.get_width(), surface.get_height())
                                sprite.select_id = characters[i]
                                select_sprites.append(sprite)
                                sprites.append(GSprite().init_gsprite(surface, x, y))
                        elif character is None:
                            character = find(characters, lambda x: x == sprite.select_id)
                            socket.send("character_set", character)

                        break

        if ready:
            take_input()

            if not receiving:
                Thread(target=receive, daemon=True).start()
                socket.send("refresh")
                receiving = True

        # rendering
        screen.fill((255, 255, 255))
        for sprite in sprites:
            if sprite is None:
                continue

            sprite.update()
            sprite.show()

        pygame.display.flip()
        clock.tick(60)
