from typing import Callable, Tuple
from uuid import UUID

import pygame.display

from game.gsprite import GSprite, MOVEMENT_SPEED, load_image
from shared.weapon import WeaponType

GUN_OFFSET = (32, 24)


class GBullet(GSprite):
    shot_by: UUID
    x1: int
    y1: int
    x2: int
    y2: int
    x_multiplier: int
    y_multiplier: int
    damage: int
    speed: float
    fx: Callable
    fy: Callable

    def __init__(self, shot_by: UUID, damage: int, speed: float, surface: pygame.Surface, x: int, y: int):
        super(GBullet, self).__init__(surface, x, y)
        self.shot_by = shot_by
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


class GWeapon(GSprite):
    weapon_type: WeaponType
    damage: int
    fire_cooldown: int
    bullet_speed: float
    last_fired: int

    def __init__(
            self,
            weapon_type: WeaponType,
            damage: int,
            fire_rate: float,
            bullet_speed: float,
            surface: pygame.Surface,
            x: int,
            y: int,
    ):
        super(GWeapon, self).__init__(surface, x, y)
        self.weapon_type = weapon_type
        self.damage = damage
        self.fire_cooldown = int(1 / fire_rate * 1000)
        self.bullet_speed = bullet_speed
        self.last_fired = -self.fire_cooldown

    def shoot(self, position: Tuple[int, int], shot_by: UUID):
        return self._shoot(position, shot_by, "bullet.png", 4, 4)

    def _shoot(self, position: Tuple[int, int], shot_by: UUID, surface: pygame.Surface):
        now = pygame.time.get_ticks()
        if now - self.last_fired < self.fire_cooldown:
            return
        self.last_fired = now

        bullet = GBullet(shot_by, self.damage, self.bullet_speed, surface, self.x, self.y)
        bullet.target(position[0], position[1])
        return bullet


class GGun(GWeapon):
    def __init__(self, x: int, y: int):
        super(GGun, self).__init__(
            weapon_type=WeaponType.RANGE,
            damage=5,
            fire_rate=1,
            bullet_speed=3,
            surface=load_image("gun.png", 24, 24),
            x=x,
            y=y,
        )

    def shoot(self, position: Tuple[int, int], shot_by: UUID):
        return self._shoot(position, shot_by, load_image("bullet.png", 4, 4))
