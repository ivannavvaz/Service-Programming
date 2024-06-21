import socket
import sys
import threading
import time


def enviarMensaje(s, mensaje):
        s.send(mensaje.encode())


def empiezaJuego(s, nameUser):

    mensaje = s.recv(1024)
    mensaje = mensaje.decode()
    print(mensaje, "\n", end="")

    precio = input("Precio: ")
    enviarMensaje(s, precio)
    print("Esperando ...")

    recibirResultado(s, nameUser)


def recibirResultado(s, nameUser):
    mensaje = s.recv(1024)
    mensaje = mensaje.decode()

    print()
    print(mensaje)

    mensaje = s.recv(1024)
    mensaje = mensaje.decode()
    print(mensaje, "\n", end="")
    volverAJugar(s, nameUser)


def volverAJugar(s, nameUser):
    time.sleep(2)

    print()
    mensaje = input("¿Quieres volver a jugar? (Y/N): ")
    s.send(mensaje.upper().encode())

    if mensaje.upper() == "N":
        time.sleep(1)
        s.close()
    else:
        empiezaJuego(s, nameUser)


def Main():
    global exit_flag
    exit_flag = False

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectado al servidor
    s.connect((host, port))
    # Escribir la frase a enviar
    print("-- Precio Justo --")
    nameUser = input("Escribe un nombre de usuario: ")
    nameUser = nameUser.capitalize()
    s.send(nameUser.encode())

    nombreRepetido = "1"

    while nombreRepetido == "1":

        nombreRepetido = s.recv(1024).decode()

        if nombreRepetido == "0":
            print("Esperando que comience el juego ...")

            h2 = threading.Thread(name=nameUser, target=empiezaJuego, args=(s, nameUser,))
            h2.start()

        else:
            nameUser = input("Nombre de usuario repetido, Escribe un nombre de usuario: ")
            nameUser = nameUser.capitalize()
            s.send(nameUser.encode())


if __name__ == '__main__':
    Main()