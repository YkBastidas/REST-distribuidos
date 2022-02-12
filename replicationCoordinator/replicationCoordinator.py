import os
import socket

# from tqdm import tqdm

HOST_REPLICATION_A = "172.26.110.42"
PORT_REPLICATION_A = 65432

HOST_REPLICATION_B = "172.26.110.42"
PORT_REPLICATION_B = 65435

HOST_COORDINATOR = "172.26.208.232"
PORT_COORDINATOR = 65433


class ReplicationCoordinator:
    def runServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_coordinator:
            socket_coordinator.bind((HOST_COORDINATOR, PORT_COORDINATOR))
            socket_coordinator.listen()
            conn, addr = socket_coordinator.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    action_type = conn.recv(1024)  # RECEIVE REPLICATE/RESTORE FROM API
                    print("Received", repr(action_type))
                    if action_type.decode("utf-8") == "REPLICATE":
                        conn.sendall(action_type)
                        action = conn.recv(1024)  # RECEIVE COMMIT/ABORT FROM API
                        print("Received", repr(action))
                        if not action:
                            break

                        with socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM
                        ) as socket_replication:
                            socket_replication.connect(
                                (HOST_REPLICATION_A, PORT_REPLICATION_A)
                            )

                            if action_type.decode("utf-8") == "REPLICATE":
                                socket_replication.sendall(
                                    action
                                )  # SEND ACTION (COMMIT OR ABORT) 1
                                action = socket_replication.recv(
                                    1024
                                )  # RECEIVE COMMIT 2
                                print("Received", repr(action))
                                socket_replication.sendall(
                                    b"VOTE_REQUEST"
                                )  # SEND VOTE_REQUEST 3
                                vote = socket_replication.recv(
                                    1024
                                )  # RECEIVE VOTE_COMMIT OR VOTE_ABORT 4
                                print("Received", repr(vote))
                                if vote.decode("utf-8") == "VOTE_COMMIT":
                                    socket_replication.sendall(
                                        b"GLOBAL_COMMIT"
                                    )  # SEND GLOBAL_COMMIT 5
                                    receive = socket_replication.recv(1024)
                                    print("Received", repr(receive))  # RECEIVE GLOBAL 6
                                    # EMPIEZA EL MANEJO DEL FILE
                                    root = os.path.dirname(__file__)
                                    relative_path = os.path.join(
                                        root,
                                        "..",
                                        "applicationServer",
                                        "objectsDatabase.json",
                                    )
                                    filename = os.path.realpath(relative_path)
                                    file = open(filename, "rb")
                                    file_data = file.read(10240)  # MANEJO DEL FILE
                                    socket_replication.send(
                                        file_data
                                    )  # ENVIO DE DATA 7
                                    file.close()
                                    print("Done Sending!")
                                    receive = socket_replication.recv(
                                        1024
                                    )  # RECEIVE SUCCEED 8
                                else:
                                    socket_replication.sendall(
                                        b"GLOBAL_ABORT"
                                    )  # SEND ABORT 9
                                    receive = socket_replication.recv(
                                        1024
                                    )  # RECEIVE FILED 10
                                socket_replication.close()
                                print(
                                    "Received", repr(receive)
                                )  # RECEIVE REPLICATION OUTCOME
                                conn.sendall(
                                    receive
                                )  # SEND OUTCOME TO APP SERVER (API)

                        with socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM
                        ) as socket_replication:
                            socket_replication.connect(
                                (HOST_REPLICATION_B, PORT_REPLICATION_B)
                            )

                            if action_type.decode("utf-8") == "REPLICATE":
                                socket_replication.sendall(
                                    action
                                )  # SEND ACTION (COMMIT OR ABORT) 1
                                action = socket_replication.recv(
                                    1024
                                )  # RECEIVE COMMIT 2
                                print("Received", repr(action))
                                socket_replication.sendall(
                                    b"VOTE_REQUEST"
                                )  # SEND VOTE_REQUEST 3
                                vote = socket_replication.recv(
                                    1024
                                )  # RECEIVE VOTE_COMMIT OR VOTE_ABORT 4
                                print("Received", repr(vote))
                                if vote.decode("utf-8") == "VOTE_COMMIT":
                                    socket_replication.sendall(
                                        b"GLOBAL_COMMIT"
                                    )  # SEND GLOBAL_COMMIT 5
                                    receive = socket_replication.recv(1024)
                                    print("Received", repr(receive))  # RECEIVE GLOBAL 6
                                    # EMPIEZA EL MANEJO DEL FILE
                                    root = os.path.dirname(__file__)
                                    relative_path = os.path.join(
                                        root,
                                        "..",
                                        "applicationServer",
                                        "objectsDatabase.json",
                                    )
                                    filename = os.path.realpath(relative_path)
                                    file = open(filename, "rb")
                                    file_data = file.read(10240)  # MANEJO DEL FILE
                                    socket_replication.send(
                                        file_data
                                    )  # ENVIO DE DATA 7
                                    file.close()
                                    print("Done Sending!")
                                    receive = socket_replication.recv(
                                        1024
                                    )  # RECEIVE SUCCEED 8
                                else:
                                    socket_replication.sendall(
                                        b"GLOBAL_ABORT"
                                    )  # SEND ABORT 9
                                    receive = socket_replication.recv(
                                        1024
                                    )  # RECEIVE FILED 10
                                socket_replication.close()
                                print(
                                    "Received", repr(receive)
                                )  # RECEIVE REPLICATION OUTCOME
                                conn.sendall(
                                    receive
                                )  # SEND OUTCOME TO APP SERVER (API)

                    else:
                        conn.sendall(action_type)  # SEND TO THE API
                        action = conn.recv(1024)  # RECEIVE A / B FROM API
                        print("Received", repr(action))
                        if not action:
                            break
                        if action.decode("utf-8") == "A":
                            self.restoreObjects(
                                action, HOST_REPLICATION_A, PORT_REPLICATION_A
                            )
                        else:
                            self.restoreObjects(
                                action, HOST_REPLICATION_B, PORT_REPLICATION_B
                            )
                        break

    def restoreObjects(self, server, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_replication:
            socket_replication.connect((host, port))
            socket_replication.sendall(server)  # SEND SERVER
            receive = socket_replication.recv(1024)  # RECEIVE RESTAURAR 12
            print("Received", repr(receive))
            root = os.path.dirname(__file__)
            relative_path = os.path.join(
                root,
                "..",
                "applicationServer",
                "objectsDatabase.json",
            )
            filename = os.path.realpath(relative_path)
            file = open(filename, "wb")
            file_data = socket_replication.recv(10240)  # RECEIVE DATA 13
            file.write(file_data)
            file.close()
            socket_replication.sendall(b"SUCCEED")  #  SEND 14
            rec = socket_replication.recv(1024)
            print("Received", repr(rec))
            socket_replication.close()
            return f"FILE RECEIVED FROM {server}"


server = ReplicationCoordinator()
server.runServer()
