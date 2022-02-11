from fileinput import filename
import socket
import sys
import threading
import time
from queue import Queue
import multiprocessing

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
FORMAT = "utf-8"
queue = Queue()
all_connections = []
all_address = []
request = 'VOTE_REQUEST'
respuestaCommit = 'VOTE_COMMIT'
respuestaAbort = 'VOTE_ABORT'
globalCommit = 'GLOBAL_COMMIT'
globalAbort = 'GLOBAL_ABORT'
cont = 0


# Crear Socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 56789
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Manejo de conexiones desde multiples clientes y se salvan en una lista
# Cerrar conexiones anteriores cuando coordinador.py es reiniciado

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Se ha establecido la conexion :" + address[0])

        except:
            print("Error aceptando conexiones")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 ServidorReplica-A Port
# 1 ServidorReplica-B Port
# turtle> REPLICAR
# 192.168.0.112> dir


def start_turtle():

    while True:

        #Se envia la opcion (REPLICAR, RESTAURAR)
        cmd = input('> ')

        if cmd == 'REPLICAR':
            replica()

        elif cmd == 'RESTAURAR':
            restaura()






#Agregar las conexiones a un array

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)



# Se envia VOTE_REQUEST, espera respuestas para proceder a replicar
def replica():
    results = ''
    cont = 0

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode('REPLICAR'))

            #RECIBE 2
            resp = s.recv(20480).decode()

            #Se envia VOTE_REQUEST
            conn.send(str.encode(request))
            #Espera respuesta
            resp = s.recv(20480).decode
            print('AQUIIII')
            print(resp)

            #Si es VOTE_COMMIT incrementa el contador
            if resp == respuestaCommit:
                cont = cont + 1
            #Si no disminuye el contador a 1
            else:
                cont = cont - 1

        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print(cont)


    #Si contador es 2 ambos SR enviaron VOTE_COMMIT, procede a respaldar
    if cont == 2:
        for i, conn in enumerate(all_connections):
            #Se envia GLOBAL_COMMIT y el archivo a respaldar
            conn.send(str.encode(globalCommit))
            resp = s.recv(20480).decode()
        print('REPLICA FINALIZADA')

    else:
        for i, conn in enumerate(all_connections):
            conn.send(str.encode(globalAbort))
            resp = s.recv(20480).decode()
        print('LA REPLICA NO PUDO SER PROCESADA')



def restaura():

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode('RESTAURAR'))
            filename = s.recv(20480).decode()
            #print("[RECV] Recibiendo el nombre del archivo")
            #file = open(filename, "w")
            #conn.send(str.encode('Nombre del archivo RECIBIDO'))

            """ Receiving the file data from the client. """
            #data = conn.recv(20480).decode(FORMAT)
            #print(f"[RECV] Receiving the file data.")
            #file.write(data)
            #conn.send("File data received".encode(FORMAT))

            """ Closing the file. """
            #file.close()

            """ Closing the connection from the client. """
            #conn.close()
            #print(f"[DISCONNECTED] disconnected.")


        except:
            del all_connections[i]
            del all_address[i]
            continue

       

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()