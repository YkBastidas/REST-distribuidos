from flask_restful import Resource
import socket

HOST_COORDINATOR = "172.26.208.232"
PORT_COORDINATOR = 65433


class Restore(Resource):
    def put(self, action: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_COORDINATOR, PORT_COORDINATOR))
            s.sendall(bytes("RESTORE", "utf-8"))  # SEND RESTORE
            data = s.recv(1024)
            s.sendall(bytes(action, "utf-8"))  # SEND ACTION
            data = s.recv(1024)
        print("Received", repr(data))
        data = data.decode("utf-8")
        if data == "FAILED REPLICATION":
            return ({"message": f"'{data}'"}, 501)
        else:
            return ({"message": f"'{data}'"}, 200)
