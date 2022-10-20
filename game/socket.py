import json
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    client.connect(("localhost", 5000))


def recieve():
    data = client.recv(1024)
    if not data:
        raise Exception("No data")
    return json.loads(data)


def send(data):
    client.send(json.dumps(data))
