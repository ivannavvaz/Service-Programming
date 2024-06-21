import socket
import sys
import threading

def enviarMensaje(s, nameUser):
    while True:
        mensaje = input("> ")

        s.send(mensaje.encode())

        if mensaje == "Exit!":
            break

    s.close()


def recibirMensaje(s, nameUser):
    while True:
        mensaje = s.recv(1024)
        mensaje = mensaje.decode()

        if mensaje == "<"+nameUser+"> Exit!":
            break

        print("\n", mensaje, "\n> ", end="")

    s.close()


def Main():
    global exit_flag
    exit_flag = False

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectado al servidor
    s.connect((host, port))
    # Escribir la frase a enviar
    print("Para salir del chat escribe: Exit!")
    nameUser = input("Escribe un nombre de usuario: ")
    nameUser = nameUser.capitalize()
    s.send(nameUser.encode())

    nombreRepetido = "1"

    while nombreRepetido == "1":

        nombreRepetido = s.recv(1024).decode()

        if nombreRepetido == "0":
            h1 = threading.Thread(name=nameUser, target=enviarMensaje, args=(s, nameUser,))
            h1.start()

            h2 = threading.Thread(name=nameUser, target=recibirMensaje, args=(s, nameUser,))
            h2.start()
        else:
            nameUser = input("Nombre de usuario repetido, Escribe un nombre de usuario: ")
            nameUser = nameUser.capitalize()
            s.send(nameUser.encode())


if __name__ == '__main__':
    Main()