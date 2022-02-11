import os
from random import choice
import socket

HOST = "172.26.110.42"
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
                    action = conn.recv(1024)  # RECEIVE ACTION 1
                    print("Received", repr(action))
                    if(action.decode("UTF-8") == "COMMIT"):
                        conn.sendall(action)  # SEND ACTION 2
                        vote_request = conn.recv(1024)  # RECEIVE VOTE_REQUEST 3
                        print("Received", repr(vote_request))
                        action = action.decode("utf-8")
                        if not action:
                            break
                        else:
                            if action == "COMMIT":
                                conn.sendall(b"VOTE_COMMIT")  # SEND VOTE_COMMIT 4
                            elif action == "ABORT":
                                conn.sendall(b"VOTE_ABORT")  # SEND VOTE_ABORT 4
                            else:
                                choose = choice(["COMMIT", "ABORT"])
                                if choose == "COMMIT":
                                    conn.sendall(b"VOTE_COMMIT")  # SEND VOTE_COMMIT 4
                                else:
                                    conn.sendall(b"VOTE_ABORT")  # SEND VOTE_ABORT 4

                        last = conn.recv(1024)  # RECEIVE GLOBAL 5
                        print("Received", repr(last))
                        if last.decode("utf-8") == "GLOBAL_COMMIT":
                            conn.sendall(last)  # 6
                            # CREA EL FILE
                            root = os.path.dirname(__file__)
                            filename = os.path.join(root, "replicationDatabase.json")
                            file = open(filename, "wb")
                            file_data = conn.recv(10240) # RECIBE LA DATA 7
                            # LLENA EL ARCHIVO
                            file.write(file_data)
                            file.close()
                            print("FILE RECEIVED")
                            conn.sendall(b"SUCCEED REPLICATION")    # SEND SUCCEED 8
                        else:
                            t = conn.recv(1024)     # RECEIVE ABORT 9
                            conn.sendall(b"FAILED REPLICATION") # SEND FAILED 10
                            print("Received", repr(t)) 
                    else:
                        serv = conn.recv(1024)  # RECEIVE A 11
                        conn.sendall(b"RESTAURAR")  #SEND RESTAURAR 12
                        print("Received", repr(serv))
                        root = os.path.dirname(__file__)
                        relative_path = os.path.join(
                            root,
                            "..",
                            "replicationServer",
                            "replicationDatabase.json",
                        )
                        filename = os.path.realpath(relative_path)
                        file = open(filename, "rb")
                        file_data = file.read(10240)
                        conn.send(file_data) # SEND DATA 13
                        file.close()
                        print("Done Sending!")
                        

    runServer()
