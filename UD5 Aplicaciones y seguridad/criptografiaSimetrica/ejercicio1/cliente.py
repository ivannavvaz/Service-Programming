import socket
import sys


def Main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Escribir un usuario
    message = input("User: ")
    s.send(message.encode())

    # Escribir contraseña
    message = input("Password: ")
    s.send(message.encode())

    data = s.recv(1024).decode()
    print('Result:', data)

    # S cierra la conexión
    s.close()


if __name__ == '__main__':
    Main()