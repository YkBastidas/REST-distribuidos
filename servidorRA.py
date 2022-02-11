import socket
import os
import subprocess
import multiprocessing

s = socket.socket()
#IP de la maquina donde se encuentra el servidor
host = '10.0.0.66 '
port = 56789

s.connect((host, port))

while True:
    #RECIBE REPLICAR 1
    data = s.recv(20840).decode()
    print(data)

    if data == 'REPLICAR':

        #ENVIA 2 
        s.send(str.encode(""))

        #RECIVE REQUEST 3
        d = s.recv(20840).decode()
        print(d)

        cmd = input('Confirmacion -> ')

        #ENVIA RESPUESTA DEL VOTO 4
        s.send(str.encode(cmd))
        gCommint = s.recv(20840).decode()
        print(gCommint)
        s.send(str.encode(' '))
        break



    #if data == 'RESTAURAR':

        #file = open("repositorioA/eje.txt", "r")
        #dato = file.read

        #s.send(str.encode('eje.txt'))
        #msg = s.recv(20480).decode()
        #print("[COORDINADOR]:  " + msg)

        """ Sending the file data to the server. """
        #s.send(str.encode(dato))
        #msg = s.recv(20480).decode()
        #print(f"[SERVER]: {msg}")

        """ Closing the file. """
        #file.close()

        """ Closing the connection from the server. """
        #s.close()


    #if len(data) > 0:
        #Popen open terminal y ejecuta el comando (data[])
        #shell=True nos da acceso a los comandos shell
        #cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #output_byte = cmd.stdout.read() + cmd.stderr.read()
        #output_str = str(output_byte,"utf-8")
        #currentWD = os.getcwd() + "> "
        #s.send(str.encode(output_str + currentWD))

        #print(output_str)