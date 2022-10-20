import json
import random
import socket
from typing import Tuple, Callable, Dict

from server.variables import characters, sprites, teams
from shared.character import Character, Cyborg
from shared.find import find
from shared.sprite import Sprite


class Handler(Sprite):
    client: socket.socket
    character: Character | None
    event_table: Dict[str, Callable]

    def __init__(self, client: socket.socket):
        super(Handler, self).__init__()
        self.client = client
        self.character = Cyborg(random.choice(teams), 100, 100)
        self.event_table = {
            "team_get": self.team_get,
            "team_set": self.team_set,
            "character_get": self.character_get,
            "character_set": self.character_set,
            "shoot": self.shoot,
            "player_move": self.player_move,
            "player_ability": self.player_ability
        }

    def handle(self):
        while True:
            data = self.client.recv(1024)
            if not data:
                break
            data = json.loads(data)

            function = self.event_table.get(data.event)
            if not function:
                continue
            if data.get("value"):
                result = function(data["value"])
            else:
                result = function()

            if result is None:
                result = {}
            self.client.send(json.dumps(result))

    def team_get(self):
        return teams

    def team_set(self, value: str):
        team = find(teams, lambda x: x.id == value)
        self.character.team = team

    def character_get(self):
        return characters

    def character_set(self, value: str):
        character = find(characters, lambda x: x.id == value)
        self.character = character(self.character.team, self.character.x, self.character.y)

    def shoot(self, value: Tuple[int, int]):
        bullet = self.character.weapon.shoot(value, self.character.team)
        sprites.append(bullet)

    def player_move(self, value: Tuple[int, int]):
        self.character.x = value[0]
        self.character.y = value[1]

    def player_ability(self, value: Tuple[int, int]):
        bullet = self.character.ability(value)
        sprites.append(bullet)
