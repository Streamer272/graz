import json
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    client.connect(("localhost", 5000))


def recieve():
    data = client.recv(1024)
    print(f"recevied {data.decode()}")
    if not data:
        raise Exception("No data")
    return json.loads(data.decode())


def send(event: str, value: object | None = None):
    data = {
        "event": event
    }
    if value is not None:
        data["value"] = value
    print(f"sending {data}")
    client.send(json.dumps(data).encode())
