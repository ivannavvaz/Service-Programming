import socket
import threading
import time
import hashlib


def hilo(c):
    user = c.recv(1024).decode().lower()

    password = c.recv(1024)

    encryptedPassword = hashlib.sha256(password).hexdigest()

    login = False

    with open('passwd.in', 'r') as archivo:
        for linea in archivo:
            parts = linea.strip().split(':')

            readUser = parts[0].strip()
            readPassword = parts[1].strip()

            if user == readUser and encryptedPassword == readPassword:
                c.send('Login Successful'.encode())
                login = True
                break

    if not login:
        c.send('ERROR - Invalid user'.encode())

    c.close()  # Cerramos la conexión


def Main():
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('Habilitamos el socket en el puerto', port)
    s.listen()
    print('Servidor preparado y a la escucha...')
    ncliente = 1

    while True:
        # Acepta conexion del cliente
        c, addr = s.accept()
        cliente = 'cliente' + str(ncliente)  # Numeramos los clientes
        print('Conectado', cliente, ' :', addr[0], '-', addr[1])
        h = threading.Thread(name=cliente, target=hilo, args=(c,))
        h.start()
        ncliente += 1

    s.close()


if __name__ == '__main__':
    Main()