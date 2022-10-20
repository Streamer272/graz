import socket
from threading import Thread
from typing import List

from server.player import Player
from shared.team import Team


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 5000))
        server.listen()
        print("Server started on localhost:5000")

        teams: List[Team] = [
            Team(name="Blue", color=(0, 0, 255)),
            Team(name="Red", color=(255, 0, 0))
        ]
        players: List[Player] = []

        while True:
            client, _ = server.accept()
            print("Client connected")
            player = Player(client, teams)
            Thread(target=player.handle, daemon=True).start()
            players.append(player)
