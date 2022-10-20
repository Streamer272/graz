from typing import Tuple

from shared.sprite import Entity


class Team(Entity):
    name: str
    color: Tuple[int, int, int]

    def __init__(self, name: str, color: Tuple[int, int, int]):
        self.name = name
        self.color = color
        self.init_entity()
