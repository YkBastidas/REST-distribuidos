import os
import socket

#from tqdm import tqdm

HOST_REPLICATION_A = "172.26.208.116"
PORT_REPLICATION_A = 65432

HOST_REPLICATION_B = "172.26.110.42"
PORT_REPLICATION_B = 65432

HOST_COORDINATOR = "172.26.77.116"
PORT_COORDINATOR = 65433


def replicate(host, port, action, conn):
    print("entre replicate")
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as socket_replication:
        socket_replication.connect(
            (host, port)
        )           
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
                    print("verifico")
                    if action_type == 'REPLICATE':
                        conn.sendall(action_type)
                        action = conn.recv(1024)  # RECEIVE COMMIT/ABORT
                        print("verifico")
                        print("Received", repr(action))
                        print("verifico")
                        if not action:
                            print("entro en el not")
                            break
                        print("antes de llamar replicate")
                        replicate(HOST_REPLICATION_A,PORT_REPLICATION_A, action, conn)

                    else:
                        conn.sendall(action_type)
                        action = conn.recv(1024)  # RECEIVE A/B
                        print("Received", repr(action))
                        if not action:
                            break                     
 

    def restoreObjects():
        # TODO: comunicarse via sockets con los servidores de replicacion
        msg = "RESTORE"

    runServer()
