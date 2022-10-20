from shared.entity import ID
from shared.sprite import Sprite


class Character(Sprite):
    weapon: ID
    max_health: int
    health: int
    ability_cooldown: int

    def __init__(self, weapon: ID, max_health: int, health: int, ability_cooldown: int):
        super(Character, self).__init__()
        self.weapon = weapon
        self.max_health = max_health
        self.health = health
        self.ability_cooldown = ability_cooldown
