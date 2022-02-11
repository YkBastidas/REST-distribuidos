from flask_restful import Resource
import socket

HOST_COORDINATOR = "127.0.0.1"
PORT_COORDINATOR = 65433


class Restore(Resource):
    def put(self, action: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_COORDINATOR, PORT_COORDINATOR))
            s.sendall(bytes("RESTORE", "utf-8"))
            data = s.recv(1024)
            s.sendall(bytes(action, "utf-8"))
            data = s.recv(1024)
        print("Received", repr(data))
        return data.decode("utf-8"), 200
