import socket
import sys
import time

def Main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Conectado al servidor
    s.connect((host,port))
    
    while True:
        data = s.recv(1024)
        print(data.decode('utf-8'))

        # Escribir la frase a enviar
        message = input("Escribe una Opción: ")

        # Enviamos mensaje al servidor
        s.send(message.encode())
        # Recibimos el mensaje del servidor
        data = s.recv(1024)

        # revertir cadena
        if message == "1":
            print(str(data.decode()))

            cadena = input("Cadena: ")
            s.send(cadena.encode())

            cadenaRevertida = s.recv(1024)
            print("Cadena revertida:", cadenaRevertida.decode())

        # numero es primo?
        elif message == "2":
            print(str(data.decode()))

            numero = input("Numero: ")
            s.send(numero.encode())

            respuesta = s.recv(1024)
            print("Es primo?:", respuesta.decode())

        # pertenece a la clase?
        elif message == "3":
            print(str(data.decode()))

            nombre = input("Nombre: ")
            s.send(nombre.encode())

            respuesta = s.recv(1024)
            print("Pertenece a la clase?:", respuesta.decode())

        # puesto de pc?
        elif message == "4":
            print(str(data.decode()))

            pc = input("PC: ")
            s.send(pc.encode())

            respuesta = s.recv(1024)
            print("Puesto de PC:", respuesta.decode())

        # cifrado cesar
        elif message == "5":
            print(str(data.decode()))

            pc = input("Cadena: ")
            s.send(pc.encode())

            respuesta = s.recv(1024)
            print("Cadena cifrada:", respuesta.decode())

        # opcion invalida
        else:
            print("ERROR - Opcion invalida")

        # Preguntamos al cliente si quiere hacer otra petición
        ans = input('\nDesea enviar otro? (s/n) : ')

        if ans == 's':
            continue
        else:
            break

    # S cierra la conexión
    print("Cerrando cliente")
    s.close()

if __name__ == '__main__':
    Main()