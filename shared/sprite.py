from uuid import uuid4


class Entity:
    id: str

    def __init__(self):
        self.id = uuid4().hex


class Sprite(Entity):
    x: int
    y: int
