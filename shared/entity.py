from uuid import uuid4

ID = str


class Entity:
    id: ID

    def init_entity(self):
        self.id = uuid4().hex
        return self
