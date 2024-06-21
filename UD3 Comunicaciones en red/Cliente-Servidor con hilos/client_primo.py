import socket
import sys


def Main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Conectado al servidor
    s.connect((host,port))
    # Escribir la frase a enviar
    message = input("Escribe un numero: ")
    
    while True:
        # Enviamos mensaje al servidor
        s.send(message.encode())
        # Recibimos el mensaje del servidor
        data = s.recv(1024)
        # El servidor devuelve reverse string
        print('Recibido del servidor :',str(data.decode()))
        # Preguntamos al cliente si quiere hacer otra petición
        ans = input('\nDesea enviar otro? (s/n) : ')

        if ans == 's':
            message = input("Escribe un numero: ")
            continue
        else:
            break

    # S cierra la conexión
    s.close()

if __name__ == '__main__':
    Main()