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

        # codificacion 3 puestos diccionario

        result = ""
        for caracter in data.decode():
            if caracter.isalpha():
                posicionesAMover = 3
                if caracter.islower():
                    result += chr((ord(caracter) - ord('a') + posicionesAMover) % 26 + ord('a'))
                elif caracter.isupper():
                    result += chr((ord(caracter) - ord('A') + posicionesAMover) % 26 + ord('A'))
            else:
                result += caracter

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