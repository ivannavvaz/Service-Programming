import random
import socket
import threading
import time

conexiones = {}
productos = {}
productosUltimaPuja = {}
productosUltimoPujante = {}


def mostrarProductos(c, nameUser):
    c.send("- Elige un articulo -".encode())
    c.send(("Articulos: " + str(list(productos.keys()))).encode())


def validarProducto(c, nameUser):
    productoElegido = c.recv(1024).decode()

    productoValido = "1"

    while productoValido == "1":

        if productoElegido == "exit":
            del conexiones[c]

            c.send("exit".encode())
            break

        elif productoElegido not in productos.keys():
            productoValido = "1"

            c.send(productoValido.encode())
            productoElegido = c.recv(1024).decode()

        else:
            productoValido = "0"

            c.send(productoValido.encode())

    if productoElegido != "exit":
        time.sleep(1)
        c.send((productoElegido + " - Ultima puja: " + str(productosUltimaPuja[productoElegido])).encode())

        validarPrecio(c, productoElegido, nameUser)


def validarPrecio(c, productoElegido, nameUser):
    precio = c.recv(1024).decode()

    if int(precio) > int(productosUltimaPuja[productoElegido]):

        productosUltimaPuja[productoElegido] = int(precio)
        productosUltimoPujante[productoElegido] = nameUser
        print(nameUser + " puja " + precio + " por " + productoElegido)
        c.send("1".encode())
        del conexiones[c]

    else:
        c.send("0".encode())

        time.sleep(1)
        mostrarProductos(c, nameUser)

        time.sleep(1)
        validarProducto(c, nameUser)


def hilo(c, cliente):
    threadName = threading.current_thread().name

    # recibimos nombre que se a asignado el cliente
    nameUser = c.recv(1024)
    nameUser = nameUser.decode()

    global productoAleatorio

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

    time.sleep(1)

    mostrarProductos(c, nameUser)

    time.sleep(1)

    validarProducto(c, nameUser)


def Main():

    archivo_entrada = "productos.txt"

    with open(archivo_entrada, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split(';')

            if len(partes) == 2:
                nombre = partes[0].lower()
                precio = int(partes[1])
                productos[nombre] = precio
                productosUltimaPuja[nombre] = precio

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