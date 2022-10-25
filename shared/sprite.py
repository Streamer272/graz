from math import sqrt, pow

from shared.entity import Entity

MOVEMENT_SPEED = 2.0


class Sprite(Entity):
    x: int
    y: int
    width: int
    height: int

    def init_sprite(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.init_entity()
        return self

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, x, y, movement_speed=MOVEMENT_SPEED):
        if sqrt(pow(x, 2) + pow(y, 2)) > movement_speed:
            a = sqrt(pow(movement_speed, 2) / 2)
            x = a * (-1.0 if x < 0 else 1.0)
            y = a * (-1.0 if y < 0 else 1.0)
        self.x += x
        self.y += y

    def collides_with(self, other):
        return not any([
            other.x + other.width < self.x,
            other.y + other.height < self.y,
            other.x > self.x + self.width,
            other.y > self.y + self.height
        ])

    def update(self):
        pass
