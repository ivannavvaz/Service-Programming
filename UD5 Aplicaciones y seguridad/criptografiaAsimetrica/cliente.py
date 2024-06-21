import socket
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


# Cifrar con la clave pública
def cifrar(public_key, txtplano):
    key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    txtcifrado = cipher_rsa.encrypt(txtplano.encode())
    return txtcifrado


def Main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    public_key = s.recv(1024).decode()

    while True:
        mensaje = input('Mensaje: ')
        if mensaje == 'exit':
            break
        mensaje_cifrado = cifrar(public_key, mensaje)
        s.send(mensaje_cifrado)

    # S cierra la conexión
    s.close()


if __name__ == '__main__':
    Main()