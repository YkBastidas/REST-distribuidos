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
                    action_type = conn.recv(1024)
                    print("Received", repr(action_type))  # RECEIVE REPLICATE/RESTORE
                    conn.sendall(action_type)
                    action = conn.recv(1024)           # VOTE_COMMIT OR VOTE_ABORT
                    print("Received", repr(action))  # RECEIVE ACTION
                    if not action:
                        break

                    with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    ) as socket_replication:
                        socket_replication.connect(
                            (HOST_REPLICATION_A, PORT_REPLICATION_A)
                        )
                        if action_type == 'REPLICATE':

                            socket_replication.sendall(action)    # SEND ACTION (COMMIT OR ABORT)
                            vote = socket_replication.recv(1024)  # RECEIVE VOTE
                            print("Received", repr(vote))
                            socket_replication.sendall(b"VOTE_REQUEST")
                            vote = socket_replication.recv(1024)    # RECEIVE VOTE_COMMIT OR VOTE_ABORT
                            if vote == 'VOTE_COMMIT':
                                socket_replication.sendall(b"GLOBAL_COMMIT")
                                receive = socket_replication.recv(1024)  # RECEIVE REPLICATION CREATED
                                print(receive) 
                            else:
                                socket_replication.sendall(b"GLOBAL_ABORT")
                                receive = socket_replication.recv(1024)  # RECEIVE REPLICATION FAILURE
                                print(receive)
                        #print("Received", repr(vote))
                        #conn.sendall(vote)

    def restoreObjects():
        # TODO: comunicarse via sockets con los servidores de replicacion
        msg = "RESTORE"

    runServer()
