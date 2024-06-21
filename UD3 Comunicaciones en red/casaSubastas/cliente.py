import socket
import sys
import threading
import time

def elegirArticulo(s):
    print()
    print(s.recv(1024).decode())
    print()
    print(s.recv(1024).decode())

    productoElegido = input("('Exit' para salir) Nombre del articulo: ").lower()
    s.send(productoElegido.encode())

    productoValido = "1"

    while productoValido == "1" and productoElegido != 'Exit':

        productoValido = s.recv(1024).decode()

        if productoValido == "0":
            print("Produto Valido")

            print(s.recv(1024).decode())

            precioPujar = input("Precio a pujar: ")
            s.send(precioPujar.encode())

            time.sleep(1)

            if s.recv(1024).decode() == "1":
                print("Has subido la apuesta")
                s.close()
            else:
                elegirArticulo(s)

        elif productoElegido == "exit":
            s.close()
            break

        else:
            productoElegido = input("('Exit' para salir) Producto no encontrado, Escribe un producto valido: ").lower().strip()
            s.send(productoElegido.encode())


def Main():

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectado al servidor
    s.connect((host, port))
    # Escribir la frase a enviar
    print("-- Casa De Subastas Sothebys --")
    nameUser = input("Escribe un nombre de usuario: ")
    nameUser = nameUser.capitalize()
    s.send(nameUser.encode())

    nombreRepetido = "1"

    while nombreRepetido == "1":

        nombreRepetido = s.recv(1024).decode()

        if nombreRepetido == "0":
            elegirArticulo(s)

        else:
            nameUser = input("Sesion registrada, Escribe un nombre de usuario: ")
            nameUser = nameUser.capitalize()
            s.send(nameUser.encode())


if __name__ == '__main__':
    Main()