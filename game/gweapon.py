from typing import Tuple

import pygame.display

from game.gsprite import GSprite, load_image
from shared.team import Team
from shared.weapon import WeaponType, Bullet, Weapon


class GBullet(GSprite, Bullet):
    def __init__(
            self,
            shot_by: Team,
            damage: int,
            speed: float,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            surface: pygame.Surface
    ):
        self.init_bullet(
            shot_by,
            damage,
            speed,
            x1,
            y1,
            x2,
            y2,
            surface.get_width(),
            surface.get_height()
        )
        self.init_gsprite(surface, x1, y1)


class GWeapon(GSprite, Weapon):
    last_fired: int

    def init_gweapon(
            self,
            weapon_type: WeaponType,
            damage: int,
            fire_rate: float,
            bullet_speed: float,
            surface: pygame.Surface,
            x: int,
            y: int,
    ):
        self.init_weapon(weapon_type, damage, fire_rate, bullet_speed, x, y, surface.get_width(), surface.get_height())
        self.init_gsprite(surface, x, y)
        self.last_fired = -self.fire_cooldown
        return self

    def shoot(self, position: Tuple[int, int], shot_by: Team):
        return self._shoot(position, shot_by, load_image("bullet.png", 4, 4))

    def _shoot(self, position: Tuple[int, int], shot_by: Team, surface: pygame.Surface):
        now = pygame.time.get_ticks()
        if now - self.last_fired < self.fire_cooldown:
            return
        self.last_fired = now

        return GBullet(
            shot_by,
            self.damage,
            self.bullet_speed,
            self.x,
            self.y,
            position[0],
            position[1],
            surface
        )


class GGun(GWeapon):
    def __init__(self, x: int, y: int):
        self.init_gweapon(
            weapon_type=WeaponType.RANGE,
            damage=5,
            fire_rate=1,
            bullet_speed=3,
            surface=load_image("gun.png", 24, 24),
            x=x,
            y=y
        )

    def shoot(self, position: Tuple[int, int], shot_by: Team):
        return self._shoot(position, shot_by, load_image("bullet.png", 4, 4))
