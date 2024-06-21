import random
import socket
import threading
import time

productos = {}

conexiones = {}
precioConexiones = {}
resultadoConexiones = {}
resultados = {}

terminaJuego = False
esperaResultados = False

productoAleatorio = None


def difundirMensaje(c, mensaje):
    for i in conexiones.keys():
        i.send(mensaje.encode())


def difundirMensajeIndibidual(c, mensaje):
    for i in conexiones.keys():
        if i == c:
            i.send(mensaje.encode())


def empezarJuego(c):
    mensaje = c.recv(1024)
    precioConexiones[c] = mensaje.decode()
    calcularResultado(c)


def calcularResultado(c):
    global terminaJuego
    resultadoConexiones[c] = int(productoAleatorio[1] - int(precioConexiones[c]))
    terminaJuego = True


def enviarResultados(c):
    global esperaResultados

    while not esperaResultados:

        if len(resultadoConexiones) == 3:
            difundirMensajeIndibidual(c, "=== Resultados ===")
            time.sleep(0.5)

            if resultadoConexiones[c] < 0:
                difundirMensajeIndibidual(c, "Has perdido, has superado el precio | Precio: " + str(productoAleatorio[1]))
            elif int(resultadoConexiones[c]) == 0:
                difundirMensajeIndibidual(c, "Has ganado + Regalo | Precio: " + str(productoAleatorio[1]))
                print("~ Ha ganado + Regalo: " + conexiones[c])
            elif resultadoConexiones[c] == min(valor for valor in resultadoConexiones.values() if valor >= 0):
                difundirMensajeIndibidual(c, "Has ganado | Precio: " + str(productoAleatorio[1]))
                print("~ Ha ganado: " + conexiones[c])
            else:
                difundirMensajeIndibidual(c, "Has perdido | Precio: " + str(productoAleatorio[1]))

            time.sleep(1)
            esperaResultados = True


def hilo(c, cliente):
    threadName = threading.current_thread().name

    # recibimos nombre que se a asignado el cliente
    nameUser = c.recv(1024)
    nameUser = nameUser.decode()

    nombreRepetido = "1"

    global productoAleatorio

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

    empiezadoJuego = False
    global mensajeEmpezarJuego
    mensajeEmpezarJuego = True

    if len(conexiones) == 3:
        mensajeEmpezarJuego = False
        print("=> Ha empezado el juegos")

    while True:

        if empiezadoJuego == False:
            if len(conexiones) == 3:
                if mensajeEmpezarJuego:
                    mensajeEmpezarJuego = False
                    print("=> Ha empezado el juegos")
                empiezadoJuego = True

                difundirMensajeIndibidual(c,
                                "=====================================================================\n# El juego a comenzado, a continuacion escribe el precio del producto\n# Objeto : " +
                                productoAleatorio[
                                    0] + "\n=====================================================================")
                time.sleep(1)
                empezarJuego(c)

        if not nameUser:
            print('# Desconectado ' + threadName)
            break

        time.sleep(0.5)

        global terminaJuego

        if terminaJuego:
            enviarResultados(c)
            conexiones.clear()

            try:
                mensaje = c.recv(1024)
                mensaje = mensaje.decode()
            except Exception as e:
                None

            if mensaje == 'N':
                c.close()
                break

            else:
                productoAleatorio = random.choice(list(productos.items()))

                conexiones[c] = nameUser

            empiezadoJuego = False
            terminaJuego = False

            global esperaResultados
            esperaResultados = False
            mensajeEmpezarJuego = True

            global precioConexiones
            global  resultadoConexiones
            global resultados

            precioConexiones.clear()
            resultadoConexiones.clear()
            resultados.clear()


def Main():

    archivo_entrada = "productos.txt"

    with open(archivo_entrada, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split(';')

            if len(partes) == 2:
                nombre = partes[0]
                precio = int(partes[1])
                productos[nombre] = precio

    global productoAleatorio
    productoAleatorio = random.choice(list(productos.items()))

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