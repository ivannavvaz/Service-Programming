import socket
import threading
import time
import hashlib
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


global private_key
global public_key


# Genera la keys privada y publica
def generar_keys():
    key = RSA.generate(2048, randfunc=get_random_bytes) # Genera la clave
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


# Descifrar con la clave privada
def descifrar(private_key, txtcifrado):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    txtplano = cipher_rsa.decrypt(txtcifrado).decode()
    return txtplano


def hilo(c):

    # Enviamos la clave pública al cliente
    c.send(public_key)

    while True:
        # Recibimos el mensaje cifrado
        mensaje_cifrado = c.recv(1024)
        if not mensaje_cifrado:
            break

        # Desciframos el mensaje
        mensaje_descifrado = descifrar(private_key, mensaje_cifrado)
        print('Mensaje descifrado:', mensaje_descifrado)

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

    global private_key
    global public_key
    private_key, public_key = generar_keys()

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