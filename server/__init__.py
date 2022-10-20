import socket
from threading import Thread

from server.handler import Handler
from server.variables import teams, players


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("Server started on localhost:5000")

    while True:
        client, _ = server.accept()
        print("Client connected")
        handler = Handler(client)
        Thread(target=handler.handle, daemon=True).start()
        players.append(handler)
