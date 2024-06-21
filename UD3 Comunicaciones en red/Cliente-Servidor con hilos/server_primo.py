import socket
import threading
import time

def hilo(c):
    nombre = threading.current_thread().name
    while True:
        # datos recibidos de un cliente
        data = c.recv(1024)

        if not data:
            print('Adios '+nombre)
            break

        print('Recibido',nombre,':', data.decode())

        # es primo?
        if data.isdigit():
            data = float(data)
            if data < 2:
                result = f"{data} no es un número primo"
            else:
                es_primo = True
                for i in range(2, int(data ** 0.5) + 1):
                    if data % i == 0:
                        es_primo = False
                        break

                if es_primo:
                    result = f"{data} es un número primo"
                else:
                    result = f"{data} no es un número primo"
        else:
            result = "ERROR - No has proporcionado un numero"

        # Enviamos los datos al cliente
        c.send(result.encode('utf-8'))
        time.sleep(0.5)

    c.close() # Cerramos la conexión

def Main():
    host = '192.168.1.173'
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
        cliente = 'cliente'+str(ncliente) # Numeramos los clientes
        print('Conectado',cliente,' :', addr[0], '-', addr[1])
        h = threading.Thread(name=cliente, target=hilo, args=(c,))
        h.start()
        ncliente += 1
        
    s.close()

if __name__ == '__main__':
    Main()