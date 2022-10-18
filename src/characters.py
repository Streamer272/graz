from sprite import Sprite
from weapons import Weapon


class Character(Sprite):
    weapon: Weapon
    max_health: int
    health: float

    def __init__(self, path: str, x: int, y: int, width: int, height: int):
        super(Character, self).__init__(path, x, y, width, height)


class Cyborg(Character):
    def __init__(self, x: int, y: int):
        super(Cyborg, self).__init__("cyborg.png", x, y, 48, 48)

    def ability(self):
        pass
