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
    x1: int
    y1: int
    x2: int
    y2: int
    damage: float
    speed: float

    def __init__(self, damage: float, speed: float, path: str, x: int, y: int, width: int, height: int):
        super(Bullet, self).__init__(path, x, y, width, height)
        self.damage = damage
        self.speed = speed

    def target(self, x, y):
        self.x1 = self.x
        self.y1 = self.y
        self.x2 = x
        self.y2 = y
        slope = (self.y2 - self.y1) / (self.x2 - self.x1)
        return lambda x: slope * (x - self.x1) + self.y1


class Gun(Weapon):
    def __init__(self, x, y):
        super(Gun, self).__init__(WeaponType.RANGE, 5, 2/3, 2, "gun.png", x, y, 12, 12)
