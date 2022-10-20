from typing import Tuple

from server.variables import sprites
from shared.sprite import Sprite
from shared.team import Team
from shared.weapon import Gun, Weapon, GUN_OFFSET, Bullet


class Character(Sprite):
    weapon: Weapon
    team: Team
    max_health: int
    health: int
    ability_cooldown: int

    def init_character(
            self,
            weapon: Weapon,
            team: Team,
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

    def ability(self, mouse_position: Tuple[int, int]):
        pass


class Cyborg(Character):
    def __init__(self, team: Team, x: int, y: int):
        self.init_character(
            weapon=Gun(x + GUN_OFFSET[0], y + GUN_OFFSET[1]),
            team=team,
            max_health=30,
            health=30,
            ability_cooldown=5000,
            x=x,
            y=y,
            width=48,
            height=48
        )

    def ability(self, mouse_position: Tuple[int, int]):
        bullet = Bullet().init_bullet(
            shot_by=self.team,
            damage=10,
            speed=5,
            x1=self.weapon.x,
            y1=self.weapon.y,
            x2=mouse_position[0],
            y2=mouse_position[1],
            width=12,
            height=12
        )
        sprites.append(bullet)
