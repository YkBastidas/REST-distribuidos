import os
import socket

from tqdm import tqdm

HOST_REPLICATION_A = "172.26.208.232"
PORT_REPLICATION_A = 65432

HOST_REPLICATION_B = "172.26.110.42"
PORT_REPLICATION_B = 65432

HOST_COORDINATOR = "172.26.77.116"
PORT_COORDINATOR = 65433


class ReplicationCoordinator:
    def runServer():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_coordinator:
            socket_coordinator.bind((HOST_COORDINATOR, PORT_COORDINATOR))
            socket_coordinator.listen()
            conn, addr = socket_coordinator.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    action_type = conn.recv(1024)  # RECEIVE REPLICATE/RESTORE
                    print("Received", repr(action_type))
                    conn.sendall(action_type)
                    action = conn.recv(1024)  # RECEIVE COMMIT/ABORT
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
                            )  # SEND ACTION (COMMIT OR ABORT)
                            action = socket_replication.recv(1024)  # RECEIVE COMMIT
                            print("Received", repr(action))
                            socket_replication.sendall(b"VOTE_REQUEST")
                            vote = socket_replication.recv(
                                1024
                            )  # RECEIVE VOTE_COMMIT OR VOTE_ABORT
                            print("Received", repr(vote))
                            if vote.decode("utf-8") == "VOTE_COMMIT":
                                socket_replication.sendall(b"GLOBAL_COMMIT")
                                receive = socket_replication.recv(1024)
                                print("Received", repr(receive))  # RECEIVE GLOBAL
                                root = os.path.dirname(__file__)
                                relative_path = os.path.join(
                                    root,
                                    "..",
                                    "applicationServer",
                                    "objectsDatabase.json",
                                )
                                filename = os.path.realpath(relative_path)
                                file = open(filename, "rb")
                                file_data = file.read(10240)
                                socket_replication.send(file_data)
                                file.close()
                                print("Done Sending!")
                                receive = socket_replication.recv(1024)
                            else:
                                socket_replication.sendall(b"GLOBAL_ABORT")
                                receive = socket_replication.recv(1024)
                            socket_replication.close()
                        print("Received", repr(receive))  # RECEIVE REPLICATION OUTCOME
                        conn.sendall(receive)  # SEND OUTCOME TO APP SERVER

                    with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    ) as socket_replicationB:
                        socket_replicationB.connect(
                            (HOST_REPLICATION_B, PORT_REPLICATION_B)
                        )

                        if action_type.decode("utf-8") == "REPLICATE":
                            socket_replicationB.sendall(
                                action
                            )  # SEND ACTION (COMMIT OR ABORT)
                            action = socket_replicationB.recv(1024)  # RECEIVE COMMIT
                            print("Received", repr(action))
                            socket_replicationB.sendall(b"VOTE_REQUEST")
                            vote = socket_replicationB.recv(
                                1024
                            )  # RECEIVE VOTE_COMMIT OR VOTE_ABORT
                            print("Received", repr(vote))
                            if vote.decode("utf-8") == "VOTE_COMMIT":
                                socket_replicationB.sendall(b"GLOBAL_COMMIT")
                                receive = socket_replicationB.recv(1024)
                                print("Received", repr(receive))  # RECEIVE GLOBAL
                                root = os.path.dirname(__file__)
                                relative_path = os.path.join(
                                    root,
                                    "..",
                                    "applicationServer",
                                    "objectsDatabase.json",
                                )
                                filename = os.path.realpath(relative_path)
                                file = open(filename, "rb")
                                file_data = file.read(10240)
                                socket_replicationB.send(file_data)
                                file.close()
                                print("Done Sending!")
                                receive = socket_replicationB.recv(1024)
                            else:
                                socket_replicationB.sendall(b"GLOBAL_ABORT")
                                receive = socket_replicationB.recv(1024)
                            socket_replicationB.close()
                        print("Received", repr(receive))  # RECEIVE REPLICATION OUTCOME
                        conn.sendall(receive)  # SEND OUTCOME TO APP SERVER

    def restoreObjects():
        # TODO: comunicarse via sockets con los servidores de replicacion
        msg = "RESTORE"

    runServer()
