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
                    data = conn.recv(1024)
                    print("Received", repr(data))
                    if not data:
                        break
                    conn.sendall(data)

    runServer()
