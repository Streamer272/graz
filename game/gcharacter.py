from typing import Tuple

import pygame.time

from game.gsprite import GSprite, load_image, FONT
from game.gweapon import GWeapon, GGun, GBullet
from shared.character import Character
from shared.team import Team
from shared.weapon import GUN_OFFSET

HEALTH_BAR_OFFSET = (0, -24)
ABILITY_COOLDOWN_OFFSET = (0, 58)


class GCharacter(GSprite, Character):
    weapon: GWeapon
    ability_last_used: int
    ability_cooldown_text: GSprite
    health_bar: GSprite
    health_bar_bg: GSprite

    def init_gcharacter(
            self,
            weapon: GWeapon,
            team: Team,
            max_health: int,
            health: int,
            ability_cooldown: int,
            path: str,
            x: int,
            y: int,
            width: int,
            height: int
    ):
        self.ability_last_used = -ability_cooldown
        self.ability_cooldown_text = GSprite().init_gsprite(FONT.render("Ready", True, (0, 0, 0)), 0, 0)
        self.health_bar = GSprite().init_gsprite(load_image("red.png", int(self.health / self.max_health * 100), 16), 0, 0)
        self.health_bar_bg = GSprite().init_gsprite(load_image("black.png", 100, 16), 0, 0)
        self.init_character(weapon, team, max_health, health, ability_cooldown, x, y, width, height)
        self.init_gsprite(load_image(path, width, height), x, y)
        self.weapon = weapon
        return self

    def shoot(self, position: Tuple[int, int]):
        return self.weapon.shoot(position, self.team)

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

        self.weapon.move_to(self.x + GUN_OFFSET[0], self.y + GUN_OFFSET[1])
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

    def ability(self, mouse_position: Tuple[int, int]):
        pass

    def show(self):
        super(GCharacter, self).show()
        self.weapon.show()
        self.health_bar_bg.show()
        self.health_bar.show()
        self.ability_cooldown_text.show()


class GCyborg(GCharacter):
    def __init__(self, team: Team, x: int, y: int):
        self.init_gcharacter(
            weapon=GGun(x + GUN_OFFSET[0], y + GUN_OFFSET[1]),
            team=team,
            max_health=30,
            health=30,
            ability_cooldown=5000,
            path="cyborg.png",
            x=x,
            y=y,
            width=48,
            height=48
        )

    def ability(self, mouse_position: Tuple[int, int]):
        now = pygame.time.get_ticks()
        if now - self.ability_last_used < self.ability_cooldown:
            return
        self.ability_last_used = now

        mouse_position = pygame.mouse.get_pos()
        bullet = GBullet(
            shot_by=self.team,
            damage=10,
            speed=5,
            x1=self.weapon.x,
            y1=self.weapon.y,
            x2=mouse_position[0],
            y2=mouse_position[1],
            surface=load_image("energy-bolt.png", 12, 12)
        )
        return bullet
