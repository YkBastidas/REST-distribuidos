import socket

HOST_REPLICATION_A = "127.0.0.1"
PORT_REPLICATION_A = 65432

HOST_COORDINATOR = "127.0.0.1"
PORT_COORDINATOR = 65433
ThreadCount = 0


class ReplicationCoordinator:
    def runServer():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_coordinator:
            socket_coordinator.bind((HOST_COORDINATOR, PORT_COORDINATOR))
            socket_coordinator.listen()
            conn, addr = socket_coordinator.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    option = conn.recv(1024)
                    print("Received", repr(option))  # RECEIVE OPTION
                    if not option:
                        break

                    with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    ) as socket_replication:
                        socket_replication.connect(
                            (HOST_REPLICATION_A, PORT_REPLICATION_A)
                        )
                        socket_replication.sendall(option)
                        vote = socket_replication.recv(1024)  # RECEIVE VOTE
                        print("Received", repr(vote))
                        socket_replication.sendall(b"VOTE_REQUEST")
                        vote = socket_replication.recv(1024)
                    print("Received", repr(vote))
                    conn.sendall(vote)

    def restoreObjects():
        # TODO: comunicarse via sockets con los servidores de replicacion
        msg = "RESTORE"

    runServer()
