from typing import List

from shared.character import Cyborg
from shared.team import Team

characters = [
    Cyborg
]
teams: List[Team] = [
    Team(name="Blue", color=(0, 0, 255)),
    Team(name="Red", color=(255, 0, 0))
]
players: List = []
sprites = []
