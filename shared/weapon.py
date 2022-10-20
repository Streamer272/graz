from enum import Enum
from typing import Callable

from shared.entity import ID
from shared.sprite import Sprite, MOVEMENT_SPEED


class WeaponType(Enum):
    RANGE = 1
    MELEE = 2


class Bullet(Sprite):
    shot_by: ID
    damage: int
    speed: float
    x1: int
    y1: int
    x2: int
    y2: int
    x_mul: int
    y_mul: int
    fx: Callable
    fy: Callable

    def init_bullet(self, shot_by: ID, damage: int, speed: float, x1: int, y1: int, x2: int, y2: int):
        self.shot_by = shot_by
        self.damage = damage
        self.speed = speed
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.x_mul = 1 if self.x1 <= self.x2 else -1
        self.y_mul = 1 if self.y1 <= self.y2 else -1

        self.fx = lambda x: (self.y2 - self.y1) / (self.x2 - self.x1) * (x - self.x1) + self.y1
        self.fy = lambda y: (y - self.y1) * (self.x2 - self.x1) / (self.y2 - self.y1) + self.x1
        return self

    def update(self):
        next_x = self.x + self.speed * MOVEMENT_SPEED * self.x_mul
        next_y = self.fx(next_x)
        if abs(next_y - self.y) > self.speed * MOVEMENT_SPEED:
            next_y = self.y + self.speed * MOVEMENT_SPEED * self.y_mul
            next_x = self.fy(next_y)

        self.move_to(next_x, next_y)


class Weapon(Sprite):
    weapon_type: WeaponType
    damage: int
    fire_cooldown: int
    bullet_speed: float

    def init_weapon(self, weapon_type: WeaponType, damage: int, fire_rate: float, bullet_speed: float, x: int, y: int,
                    width: int, height: int):
        self.weapon_type = weapon_type
        self.damage = damage
        self.fire_cooldown = int(1 / fire_rate * 1000)
        self.bullet_speed = bullet_speed
        self.init_sprite(x, y, width, height)
        return self
