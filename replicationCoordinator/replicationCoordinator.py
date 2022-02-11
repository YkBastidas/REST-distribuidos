import json
import os
import socket
import pandas as pd


HOST_REPLICATION_A = "127.0.0.1"
PORT_REPLICATION_A = 65432

HOST_COORDINATOR = "127.0.0.1"
PORT_COORDINATOR = 65433


def getJSONfile():
        root = os.path.dirname(__file__)
        filename = os.path.join(root, "objectsDatabase.json")
        file = open(filename)
        json_data = json.load(file)
        print(json_data)
        return json_data

class ReplicationCoordinator:
    
    
    
    def runServer():
        CHUNK_SIZE = 8 * 1024

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
                            vote = socket_replication.recv(1024)  # RECEIVE COMMIT
                            print("Received", repr(vote))
                            socket_replication.sendall(b"VOTE_REQUEST")
                            vote = socket_replication.recv(
                                1024
                            )  # RECEIVE VOTE_COMMIT OR VOTE_ABORT
                            if vote.decode("utf-8") == "VOTE_COMMIT":
                                socket_replication.sendall(b"GLOBAL_COMMIT")
                                receive = socket_replication.recv(1024)
                            else:
                                socket_replication.sendall(b"GLOBAL_ABORT")
                                receive = socket_replication.recv(1024)
                        print("Received", repr(receive))  # RECEIVE REPLICATION OUTCOME
                        conn.sendall(receive)  # SEND OUTCOME TO APP SERVER
                        socket_replication.sendall(action)
                        vote = socket_replication.recv(1024)  # RECEIVE VOTE
                        print("Received", repr(vote))
                        socket_replication.sendall(b"VOTE_REQUEST")
                        ##abre el json                        
                        with open('objectsDatabase.json', 'rb') as f:
                            ## obtiene un frame de 1024 bit
                            data = f.read(CHUNK_SIZE)
                            while data:
                                ##envia el frame de 1024 bit
                                socket_replication.send(data)
                                ## obtiene un frame de 1024 bit
                                data = f.read(CHUNK_SIZE)                        
                        
                        vote = socket_replication.recv(1024)
                    print("Received", repr(vote))
                    conn.sendall(vote)

    def restoreObjects():
        # TODO: comunicarse via sockets con los servidores de replicacion
        msg = "RESTORE"    

    runServer()
