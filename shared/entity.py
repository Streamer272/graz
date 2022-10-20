from uuid import uuid4

ID = str


class Entity:
    id: ID

    def __init__(self):
        self.id = uuid4().hex
