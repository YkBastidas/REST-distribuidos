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
                    #data = conn.recv(1024)
                    #print("Received", repr(data))
                    #if not data:
                        #break
                    #conn.sendall(data)

                    
                    data = conn.recv(1024)  # RECEIVE ACTION
                    print("Received", repr(data))
                    if not data:
                        break
                    else:
                        if data == 'COMMIT':
                            conn.sendall(b"VOTE_COMMIT")    # SEND VOTE_COMMIT
                        if data == 'ABORT':
                            conn.sendall(b"VOTE_ABORT")    # SEND VOTE_ABORT
                        else:
                            choose = choice(['COMMIT', 'ABORT'])
                            if choose == 'COMMIT':
                                conn.sendall(b"VOTE_COMMIT")    # SEND VOTE_COMMIT
                            else:
                                conn.sendall(b"VOTE_ABORT")    # SEND VOTE_ABORT
                    
                    last = conn.recv(1024)  # RECEIVE GLOBAL
                    print("Received", repr(last))
                    if last == 'GLOBAL_COMMIT':
                        conn.sendall(b"SUCCEED REPLICATION")
                    else:
                        conn.sendall(b"FAILED REPLICATION")

    runServer()
