import json
import random
import socket
import re
from typing import Tuple, Callable, Dict

from server.variables import characters, sprites, teams, players
from shared.character import Character, Cyborg
from shared.entity import Entity
from shared.find import find
from shared.sprite import MOVEMENT_SPEED


class Handler(Entity):
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
            "refresh": self.refresh,
            "shoot": self.shoot,
            "player_move": self.player_move,
            "player_ability": self.player_ability
        }
        self.init_entity()

    def handle(self):
        self.log("Player connected")
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break
                data = json.loads(data.decode())

                function = self.event_table.get(data["event"])
                if not function:
                    continue
                self.log(f"Calling {function.__name__}")
                if data.get("value"):
                    result = function(data["value"])
                else:
                    result = function()

                if result is not None and result != {}:
                    self.client.send(json.dumps(result).encode())
            except Exception as e:
                self.log(f"Exception occurred: {e} ({type(e)})")
                if isinstance(e, ConnectionError):
                    self.log("Connection lost")
                    self.broadcast("sprite_destroy", self.id)
                    players.pop(players.index(self))
                    break

    def log(self, message):
        print(f"[{self.id}] {message}")

    def broadcast(self, event, value):
        for player in players:
            if player is None:
                continue

            player.log(f"Broadcasting {json.dumps({'event': event, 'value': value})}")
            try:
                player.client.send(json.dumps({
                    "event": event,
                    "value": value
                }).encode())
            except ConnectionError:
                pass

    def get_character_name(self, character: str):
        regex = "(?<=<class 'shared.character.).*(?='>)"
        match = re.search(regex, character)
        return None if match is None else match.group()

    def team_get(self):
        return [{
            "id": it.id,
            "name": it.name,
            "color": it.color
        } for it in teams]

    def team_set(self, value: str):
        team = find(teams, lambda x: x.id == value)
        self.character.team = team

    def character_get(self):
        return [it.__name__ for it in characters]

    def character_set(self, value: str):
        character = find(characters, lambda x: self.get_character_name(str(x)) == value)
        self.character = character(self.character.team, self.character.x, self.character.y)
        self.broadcast("sprite_create", {
            "id": self.id,
            "path": f"{self.get_character_name(str(type(self.character))).lower()}.png",
            "x": self.character.x,
            "y": self.character.y,
            "width": self.character.width,
            "height": self.character.height
        })

    def refresh(self):
        for player in players:
            self.client.send(json.dumps({
                "event": "sprite_create",
                "value": {
                    "id": player.id,
                    "path": f"{self.get_character_name(str(type(player.character))).lower()}.png",
                    "x": player.character.x,
                    "y": player.character.y,
                    "width": player.character.width,
                    "height": player.character.height
                }
            }).encode())

    def shoot(self, value: Tuple[int, int]):
        bullet = self.character.weapon.shoot(value, self.character.team)
        sprites.append(bullet)

    def player_move(self, value: Tuple[int, int]):
        self.log(f"Updated x:y from {self.character.x}:{self.character.y} to {self.character.x + value[0] * MOVEMENT_SPEED}:{self.character.y + value[1] * MOVEMENT_SPEED}")
        self.character.x += value[0] * MOVEMENT_SPEED
        self.character.y += value[1] * MOVEMENT_SPEED
        self.broadcast("sprite_move", {
            "id": self.id,
            "x": self.character.x,
            "y": self.character.y
        })

    def player_ability(self, value: Tuple[int, int]):
        bullet = self.character.ability(value)
        sprites.append(bullet)
