from enum import Enum

from sprite import Sprite


class WeaponType(Enum):
    RANGE = 0
    MELEE = 1


class Weapon(Sprite):
    weapon_type: WeaponType
    damage: float
    fire_rate: float
    bullet_speed: float

    def __init__(self, weapon_type: WeaponType, damage: float, fire_rate: float, bullet_speed: float, path: str, x: int, y: int, width: int, height: int):
        super(Weapon, self).__init__(path, x, y, width, height)
        self.weapon_type = weapon_type
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed


class Bullet(Sprite):
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    damage: float
    speed: float

    def __init__(self, damage: float, speed: float, path: str, x: int, y: int, width: int, height: int):
        super(Bullet, self).__init__(path, x, y, width, height)
        self.damage = damage
        self.speed = speed

    def target(self, x, y):
        pass


class Gun(Weapon):
    def __init__(self, x, y):
        super(Gun, self).__init__(WeaponType.RANGE, 5, 2/3, 2, "gun.png", x, y, 12, 12)
