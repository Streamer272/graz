from uuid import uuid4, UUID
from typing import Tuple

import pygame.time

from sprite import Sprite
from weapons import Weapon, Gun, GUN_OFFSET


class Character(Sprite):
    id: UUID
    weapon: Weapon
    max_health: int
    health: float
    ability_cooldown: int
    ability_last_used: int

    def __init__(self, health: int, weapon: Weapon, ability_cooldown: int, path: str, x: int, y: int, width: int,
                 height: int):
        self.id = uuid4()
        super(Character, self).__init__(path, x, y, width, height)
        self.max_health = health
        self.health = health
        self.weapon = weapon
        self.ability_cooldown = ability_cooldown
        self.ability_last_used = -ability_cooldown

    def shoot(self, position: Tuple[int, int]):
        return self.weapon.shoot(position, self.id)

    def take_damage(self, damage: float):
        self.health -= damage

    def update(self):
        self.weapon.move_to(self.x + GUN_OFFSET[0], self.y + GUN_OFFSET[1])

    def ability(self):
        pass

    def show(self):
        super(Character, self).show()
        self.weapon.show()


class Cyborg(Character):
    def __init__(self, x: int, y: int):
        weapon = Gun(x + GUN_OFFSET[0], y + GUN_OFFSET[1])
        super(Cyborg, self).__init__(30, weapon, 5000, "cyborg.png", x, y, 48, 48)

    def update(self):
        super(Cyborg, self).update()

    def ability(self):
        now = pygame.time.get_ticks()
        if now - self.ability_last_used < self.ability_cooldown:
            return
        self.ability_last_used = now

        print("USING ABILITY")
        # TODO
