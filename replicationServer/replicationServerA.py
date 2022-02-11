import os
from random import choice
import socket

HOST = "172.26.77.116"
PORT = 65432


class ReplicationServer:
    def runServer():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    action = conn.recv(1024)  # RECEIVE ACTION
                    print("Received", repr(action))
                    
                    conn.sendall(action)  # SEND ACTION
                    vote_request = conn.recv(1024)  # RECEIVE VOTE_REQUEST
                    print("Received", repr(vote_request))
                    action = action.decode("utf-8")
                    if not action:
                        break
                    else:
                        if action == "COMMIT":
                            conn.sendall(b"VOTE_COMMIT")  # SEND VOTE_COMMIT
                        elif action == "ABORT":
                            conn.sendall(b"VOTE_ABORT")  # SEND VOTE_ABORT
                        else:
                            choose = choice(["COMMIT", "ABORT"])
                            if choose == "COMMIT":
                                conn.sendall(b"VOTE_COMMIT")  # SEND VOTE_COMMIT
                            else:
                                conn.sendall(b"VOTE_ABORT")  # SEND VOTE_ABORT

                        last = conn.recv(1024)  # RECEIVE GLOBAL
                        print("Received", repr(last))
                        if last.decode("utf-8") == "GLOBAL_COMMIT":
                            conn.sendall(last)
                            root = os.path.dirname(__file__)
                            filename = os.path.join(root, "replicationDatabase.json")
                            file = open(filename, "wb")
                            file_data = conn.recv(10240)
                            file.write(file_data)
                            file.close()
                            print("FILE RECEIVED")
                            conn.sendall(b"SUCCEED REPLICATION")
                        else:
                            conn.sendall(b"FAILED REPLICATION")
                     

    runServer()
