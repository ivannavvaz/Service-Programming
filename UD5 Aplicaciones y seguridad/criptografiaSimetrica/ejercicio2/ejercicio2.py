import time

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv, set_key
import sys, os


def code(key, text):
    try:
        cipher_suite = Fernet(key)

        cipher_text = cipher_suite.encrypt(text.encode())

        plain_text = cipher_suite.decrypt(cipher_text)

        print("# Mensaje cifrado con exito")
        print("Texto cifrado:", cipher_text)
        print("Texto descifrado:", plain_text.decode())
    except Exception as e:
        print(f"Error al cifrar el texto: {e}")


def decode(key, text):
    try:
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(text.encode())

        print("# Mensaje descifrado con exito")
        print("Texto descifrado:", plain_text.decode())
        print("Texto cifrado:", text)
    except InvalidToken as e:
        print(f"Error al descifrar el token - Invalid token")
    except Exception as e:
        print(f"Error al descifrar el texto: {e}")


def Main():
    load_dotenv()

    clave_cifrado = os.getenv('KEY')

    if not clave_cifrado:
        print("No existe clave de cifrado, creando una...")
        key = Fernet.generate_key()
        set_key('.env', 'KEY', str(key.decode()))
        clave_cifrado = key

    argumentos = sys.argv

    if len(argumentos) == 3:
        if argumentos[1] == "-e":
            code(clave_cifrado, argumentos[2])
        elif argumentos[1] == "-d":
            decode(clave_cifrado, argumentos[2])
        else:
            print("Argumento no válido - (-e | -d) String")
    else:
        print("No se han proporcionado dos argumentos - (-e | -d) String")


if __name__ == '__main__':
    Main()
