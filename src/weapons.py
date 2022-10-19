from enum import Enum
from typing import Callable, Tuple

import pygame.display

from sprite import Sprite, MOVEMENT_SPEED

GUN_OFFSET = (32, 24)


class WeaponType(Enum):
    RANGE = 0
    MELEE = 1


class Bullet(Sprite):
    x1: int
    y1: int
    x2: int
    y2: int
    x_multiplier: int
    y_multiplier: int
    damage: float
    speed: float
    fx: Callable
    fy: Callable

    def __init__(self, damage: float, speed: float, path: str, x: int, y: int, width: int, height: int):
        super(Bullet, self).__init__(path, x, y, width, height)
        self.damage = damage
        self.speed = speed

    def target(self, x, y):
        self.x1 = self.x
        self.y1 = self.y
        self.x2 = x
        self.y2 = y
        self.x_multiplier = 1 if self.x1 < self.x2 else -1
        self.y_multiplier = 1 if self.y1 < self.y2 else -1
        self.fx = lambda x: (self.y2 - self.y1) / (self.x2 - self.x1) * (x - self.x1) + self.y1
        self.fy = lambda y: (y - self.y1) * (self.x2 - self.x1) / (self.y2 - self.y1) + self.x1

    def update(self):
        next_x = self.x + self.speed * MOVEMENT_SPEED * self.x_multiplier
        next_y = self.fx(next_x)
        if abs(next_y - self.y) > self.speed * MOVEMENT_SPEED:
            next_y = self.y + self.speed * MOVEMENT_SPEED * self.y_multiplier
            next_x = self.fy(next_y)

        screen_size = pygame.display.get_window_size()
        if next_x < 0 or next_y < 0 or next_x > screen_size[0] or next_y > screen_size[1]:
            self.destroy = True
            return

        self.move_to(next_x, next_y)


class Weapon(Sprite):
    weapon_type: WeaponType
    damage: float
    fire_cooldown: int
    bullet_speed: float
    last_fired: int

    def __init__(self, weapon_type: WeaponType, damage: float, fire_rate: float, bullet_speed: float, path: str, x: int,
                 y: int, width: int, height: int):
        super(Weapon, self).__init__(path, x, y, width, height)
        self.weapon_type = weapon_type
        self.damage = damage
        self.fire_cooldown = int(1 / fire_rate * 1000)
        self.bullet_speed = bullet_speed
        self.last_fired = -self.fire_cooldown

    def shoot(self, position: Tuple[int, int]):
        now = pygame.time.get_ticks()
        if now - self.last_fired < self.fire_cooldown:
            return
        self.last_fired = now

        bullet = Bullet(self.damage, self.bullet_speed, "bullet.png", self.x, self.y, 4, 4)
        bullet.target(position[0], position[1])
        return bullet


class Gun(Weapon):
    def __init__(self, x: int, y: int):
        super(Gun, self).__init__(WeaponType.RANGE, 5, 1, 2, "gun.png", x, y, 24, 24)
