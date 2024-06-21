import socket
import threading
import time

def hilo(c, diccionarioPC):
    nombre = threading.current_thread().name
    while True:
        # datos recibidos de un cliente
        data = c.recv(1024)

        if not data:
            print('Adios '+nombre)
            break

        print('Recibido',nombre,':', data.decode())

        # puesto del PC

        if data.isdigit():
            if int(data) not in diccionarioPC:
                result = "ERROR - Puesto no disponible"
            else:
                result = diccionarioPC.get(int(data))
        else:
            result = "ERROR - No has proporcionado un numero"

        # Enviamos los datos al cliente
        c.send(result.encode('utf-8'))
        time.sleep(0.5)

    c.close() # Cerramos la conexión

def Main():
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('Habilitamos el socket en el puerto', port)
    s.listen()
    print('Servidor preparado y a la escucha...')
    ncliente = 1

    diccionarioPC = {1:"ivan", 2:"yago", 3:"maria", 4:"unai", 5:"marc"}

    while True:
        # Acepta conexion del cliente
        c, addr = s.accept()
        cliente = 'cliente'+str(ncliente) # Numeramos los clientes
        print('Conectado',cliente,' :', addr[0], '-', addr[1])
        h = threading.Thread(name=cliente, target=hilo, args=(c, diccionarioPC,))
        h.start()
        ncliente += 1
        
    s.close()

if __name__ == '__main__':
    Main()