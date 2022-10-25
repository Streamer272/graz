from typing import Tuple

from shared.entity import ID
from shared.sprite import Entity


class Team(Entity):
    name: str
    color: Tuple[int, int, int]

    def __init__(self, name: str, color: Tuple[int, int, int]):
        self.name = name
        self.color = color
        self.init_entity()

    def set_id(self, id: ID):
        self.id = id
        return self
