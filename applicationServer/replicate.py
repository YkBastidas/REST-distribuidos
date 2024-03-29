from flask_restful import Resource
import socket

HOST_COORDINATOR = "172.26.208.232"
PORT_COORDINATOR = 65433


class Replicate(Resource):
    def post(self, action: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_COORDINATOR, PORT_COORDINATOR))
            s.sendall(bytes("REPLICATE", "utf-8"))  # SEND REPLICATE
            data = s.recv(1024)
            s.sendall(bytes(action, "utf-8"))  # SEND ACTION
            dataA = s.recv(1024)
            print("Received from A", repr(data))
            s.recv(1024)
            print("Received from B", repr(data))
        data = data.decode("utf-8")
        if data == "FAILED REPLICATION":
            return ({"message": f"'{data}'"}, 501)
        else:
            return ({"message": f"'{data}'"}, 200)
