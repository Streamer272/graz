from typing import Tuple, List
from uuid import uuid4, UUID

import pygame.time

from sprite import Sprite, load_image
from weapons import Weapon, Gun, GUN_OFFSET, Bullet

HEALTH_BAR_OFFSET = (0, -24)


class Character(Sprite):
    id: UUID
    weapon: Weapon
    max_health: int
    health: float
    ability_cooldown: int
    ability_last_used: int
    health_bar: Sprite
    health_bar_bg: Sprite

    def __init__(
            self,
            health: int,
            weapon: Weapon,
            ability_cooldown: int,
            path: str,
            x: int,
            y: int,
            width: int,
            height: int
    ):
        self.id = uuid4()
        super(Character, self).__init__(load_image(path, width, height), x, y)
        self.max_health = health
        self.health = health
        self.weapon = weapon
        self.ability_cooldown = ability_cooldown
        self.ability_last_used = -ability_cooldown
        self.health_bar = Sprite(
            load_image("red.png", int(self.health / self.max_health * 100), 16),
            self.x + HEALTH_BAR_OFFSET[0] - int(self.surface.get_width() / 2),
            self.y + HEALTH_BAR_OFFSET[1]
        )
        self.health_bar_bg = Sprite(load_image("black.png", 100, 16), 10, 10)

    def shoot(self, position: Tuple[int, int]):
        return self.weapon.shoot(position, self.id)

    def take_damage(self, damage: float):
        self.health -= damage
        self.health_bar.surface = load_image("red.png", int(self.health / self.max_health * 100), 16)

    def update(self):
        self.weapon.move_to(self.x + GUN_OFFSET[0], self.y + GUN_OFFSET[1])
        self.health_bar.move_to(
            self.x + HEALTH_BAR_OFFSET[0] - int(self.surface.get_width() / 2),
            self.y + HEALTH_BAR_OFFSET[1]
        )
        self.health_bar_bg.move_to(
            self.x + HEALTH_BAR_OFFSET[0] - int(self.surface.get_width() / 2),
            self.y + HEALTH_BAR_OFFSET[1]
        )

    def ability(self, sprites: List):
        pass

    def show(self):
        super(Character, self).show()
        self.weapon.show()
        self.health_bar_bg.show()
        self.health_bar.show()


class Cyborg(Character):
    def __init__(self, x: int, y: int):
        weapon = Gun(x + GUN_OFFSET[0], y + GUN_OFFSET[1])
        super(Cyborg, self).__init__(30, weapon, 5000, "cyborg.png", x, y, 48, 48)

    def update(self):
        super(Cyborg, self).update()

    def ability(self, sprites: List):
        now = pygame.time.get_ticks()
        if now - self.ability_last_used < self.ability_cooldown:
            return
        self.ability_last_used = now

        mouse_position = pygame.mouse.get_pos()
        bullet = Bullet(
            shot_by=self.id,
            damage=10,
            speed=5,
            surface=load_image("energy-bolt.png", 12, 12),
            x=self.weapon.x,
            y=self.weapon.y,
        )
        bullet.target(mouse_position[0], mouse_position[1])
        sprites.append(bullet)
