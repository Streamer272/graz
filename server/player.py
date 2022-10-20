import json
import socket
from typing import List, Tuple, Callable, Dict

from shared.find import find
from shared.sprite import Sprite
from shared.team import Team


class Player(Sprite):
    client: socket.socket
    teams: List[Team]
    team: Team
    event_table: Dict[str, Callable]

    def __init__(self, client: socket.socket, teams: List[Team]):
        super(Player, self).__init__()
        self.client = client
        self.teams = teams
        self.team = teams[0]
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
        return self.teams

    def team_set(self, value: str):
        team = find(self.teams, lambda x: x.id == value)
        self.team = team

    def character_get(self):
        # TODO
        pass

    def character_set(self, value: str):
        # TODO
        pass

    def shoot(self, value: Tuple[int, int]):
        # TODO
        pass

    def player_move(self, value: Tuple[int, int]):
        # TODO
        pass

    def player_ability(self, value: Tuple[int, int]):
        # TODO
        pass
