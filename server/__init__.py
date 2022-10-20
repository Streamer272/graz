import socket
from threading import Thread
from typing import List

from server.handler import Handler
from shared.team import Team


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("Server started on localhost:5000")

    teams: List[Team] = [
        Team(name="Blue", color=(0, 0, 255)),
        Team(name="Red", color=(255, 0, 0))
    ]
    players: List[Handler] = []

    while True:
        client, _ = server.accept()
        print("Client connected")
        handler = Handler(client, teams)
        Thread(target=handler.handle, daemon=True).start()
        players.append(handler)
