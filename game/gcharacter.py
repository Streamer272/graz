from typing import Tuple, List
from uuid import uuid4, UUID

import pygame.time

from game.gsprite import GSprite, load_image
from game.gweapon import GWeapon, GGun, GUN_OFFSET, GBullet
from game.variables import weapons
from shared.character import Character
from shared.find import find

pygame.font.init()

HEALTH_BAR_OFFSET = (0, -24)
ABILITY_COOLDOWN_OFFSET = (0, 58)
FONT = pygame.font.SysFont("freeserif", 16)


class GCharacter(GSprite, Character):
    ability_last_used: int
    ability_cooldown_text: GSprite
    health_bar: GSprite
    health_bar_bg: GSprite

    # TODO: make self.weapon type GWeapon
    def init_gcharacter(
            self,
            weapon: GWeapon,
            max_health: int,
            health: int,
            ability_cooldown: int,
            path: str,
            x: int,
            y: int,
            width: int,
            height: int
    ):
        super(GCharacter, self).__init__(load_image(path, width, height), x, y)
        self.ability_last_used = -ability_cooldown
        self.ability_cooldown_text = GSprite().init_gsprite(FONT.render("Ready", True, (0, 0, 0)), 0, 0)
        self.health_bar = GSprite().init_gsprite(load_image("red.png", int(self.health / self.max_health * 100), 16), 0, 0)
        self.health_bar_bg = GSprite().init_gsprite(load_image("black.png", 100, 16), 0, 0)
        self.init_character(weapon.id, max_health, health, ability_cooldown, x, y, width, height)
        return self

    def shoot(self, position: Tuple[int, int]):
        # TODO: change self.id to self.team
        return find(weapons, lambda x: x.id == self.weapon).shoot(position, self.id)

    def take_damage(self, damage: int):
        self.health -= damage
        self.health_bar.surface = load_image("red.png", int(self.health / self.max_health * 100), 16)

    def update(self):
        position_according_to = lambda to: -int(to.surface.get_width() / 2) + int(self.surface.get_width() / 2)
        now = pygame.time.get_ticks()
        new_ability_cooldown = "Ready"
        if now - self.ability_last_used < self.ability_cooldown:
            new_ability_cooldown = f"Ready in {int((self.ability_cooldown - now + self.ability_last_used) / 1000) + 1}"
        self.ability_cooldown_text.surface = FONT.render(new_ability_cooldown, True, (0, 0, 0))

        find(weapons, lambda x: x.id == self.weapon).move_to(self.x + GUN_OFFSET[0], self.y + GUN_OFFSET[1])
        self.ability_cooldown_text.move_to(
            self.x + ABILITY_COOLDOWN_OFFSET[0] + position_according_to(self.ability_cooldown_text),
            self.y + ABILITY_COOLDOWN_OFFSET[1]
        )
        self.health_bar.move_to(
            self.x + HEALTH_BAR_OFFSET[0] + position_according_to(self.health_bar_bg),
            self.y + HEALTH_BAR_OFFSET[1]
        )
        self.health_bar_bg.move_to(
            self.x + HEALTH_BAR_OFFSET[0] + position_according_to(self.health_bar_bg),
            self.y + HEALTH_BAR_OFFSET[1]
        )

    def ability(self, sprites: List):
        pass

    def show(self):
        super(GCharacter, self).show()
        find(weapons, lambda x: x.id == self.weapon).show()
        self.health_bar_bg.show()
        self.health_bar.show()
        self.ability_cooldown_text.show()


class Cyborg(GCharacter):
    def __init__(self, x: int, y: int):
        weapon = GGun(x + GUN_OFFSET[0], y + GUN_OFFSET[1])
        self.init_gcharacter(
            weapon=weapon,
            max_health=30,
            health=30,
            ability_cooldown=5000,
            path="cyborg.png",
            x=x,
            y=y,
            width=48,
            height=48
        )

    def ability(self, sprites: List):
        now = pygame.time.get_ticks()
        if now - self.ability_last_used < self.ability_cooldown:
            return
        self.ability_last_used = now

        mouse_position = pygame.mouse.get_pos()
        bullet = GBullet(
            shot_by=self.id,
            damage=10,
            speed=5,
            surface=load_image("energy-bolt.png", 12, 12),
            x=find(weapons, lambda x: x.id == self.weapon).x,
            y=find(weapons, lambda x: x.id == self.weapon).y,
        )
        bullet.target(mouse_position[0], mouse_position[1])
        sprites.append(bullet)
