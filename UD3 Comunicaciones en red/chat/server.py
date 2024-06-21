import socket
import threading
import time

conexiones = {}

def difundirMensaje(c, mensaje):
    for i in conexiones.keys():
            if i != c:
                i.send(mensaje.encode())


def hilo(c, cliente):
    threadName = threading.current_thread().name

    # recibimos nombre que se a asignado el cliente
    nameUser = c.recv(1024)
    nameUser = nameUser.decode()

    nombreRepetido = "1"

    while nombreRepetido == "1":

        if nameUser in conexiones.values():
            nombreRepetido = "1"

            c.send(nombreRepetido.encode())

            nameUser = c.recv(1024)
            nameUser = nameUser.decode()

        else:
            nombreRepetido = "0"
            c.send(nombreRepetido.encode())

    conexiones[c] = nameUser

    mensajeBienvenida = str("# " + str(nameUser) + " Ha entrado al chat")
    difundirMensaje(c, mensajeBienvenida)
    print('#', str(nameUser), "- Ha entrado al chat")

    while True:
        mensaje = "<"+str(nameUser)+"> " + str(c.recv(1024).decode())

        if mensaje == "<" + str(nameUser) + "> Exit!":
            c.send(mensaje.encode())
            conexiones.pop(c)
            break

        print(mensaje)

        difundirMensaje(c, mensaje)

        if not nameUser:
            print('# Desconectado ' + threadName)
            break

        time.sleep(0.5)

    c.close()  # Cerramos la conexión
    mensajeDespedida = str("# "+ str(nameUser)+ " Ha salido del chat")
    difundirMensaje(c, mensajeDespedida)
    print("#", nameUser, " Ha salido del chat")


def Main():
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('Habilitamos el socket en el puerto', port)
    s.listen()
    print('Servidor preparado y a la escucha...')
    print('=========================================')
    ncliente = 1

    while True:
        # Acepta conexion del cliente
        c, addr = s.accept()
        cliente = 'cliente' + str(ncliente)  # Numeramos los clientes
        print('# Conectado', cliente, ':', addr[0], '-', addr[1])
        h = threading.Thread(name=cliente, target=hilo, args=(c, cliente,))
        h.start()
        ncliente += 1

    s.close()


if __name__ == '__main__':
    Main()