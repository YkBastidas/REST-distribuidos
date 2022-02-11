import json
from random import choice
import socket

HOST = "127.0.0.1"
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
                    # data = conn.recv(1024)
                    # print("Received", repr(data))
                    # if not data:
                    # break
                    # conn.sendall(data)
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
                        
                        jsonReceived = conn.makefile()
                        
                        with open('objectsDatabase.json', 'wb') as file:
                            json.dump(jsonReceived, file)
                        conn.sendall(b"SUCCEED REPLICATION")
                    else:
                        conn.sendall(b"FAILED REPLICATION")

    runServer()
