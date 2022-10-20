from shared.entity import ID
from shared.sprite import Sprite


class Character(Sprite):
    weapon: ID
    team: ID
    max_health: int
    health: int
    ability_cooldown: int

    def init_character(
            self,
            weapon: ID,
            team: ID,
            max_health: int,
            health: int,
            ability_cooldown: int,
            x: int,
            y: int,
            width: int,
            height: int
    ):
        self.weapon = weapon
        self.team = team
        self.max_health = max_health
        self.health = health
        self.ability_cooldown = ability_cooldown
        self.init_sprite(x, y, width, height)
        return self
