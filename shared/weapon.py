from enum import Enum
from typing import Callable, Tuple

from shared.sprite import Sprite, MOVEMENT_SPEED
from shared.team import Team

GUN_OFFSET = (32, 24)


class WeaponType(Enum):
    RANGE = 1
    MELEE = 2


class Bullet(Sprite):
    shot_by: Team
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

    def init_bullet(
            self,
            shot_by: Team,
            damage: int,
            speed: float,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            width: int,
            height: int
    ):
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

        self.init_sprite(x1, y1, width, height)
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


class Gun(Weapon):
    def __init__(self, x: int, y: int):
        self.init_weapon(
            weapon_type=WeaponType.RANGE,
            damage=5,
            fire_rate=1,
            bullet_speed=3,
            x=x,
            y=y,
            width=24,
            height=24
        )

    def shoot(self, position: Tuple[int, int], shot_by: Team):
        return Bullet().init_bullet(
            shot_by=shot_by,
            damage=self.damage,
            speed=self.bullet_speed,
            x1=self.x,
            y1=self.y,
            x2=position[0],
            y2=position[1],
            width=4,
            height=4
        )
