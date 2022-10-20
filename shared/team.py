from typing import Tuple

from shared.sprite import Entity


class Team(Entity):
    name: str
    color: Tuple[int, int, int]

    def __init__(self, name: str, color: Tuple[int, int, int]):
        super(Team, self).__init__()
        self.name = name
        self.color = color
