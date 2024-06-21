import socket
import threading
import time
import hashlib
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


def validarUsuario(c, user, encryptedPassword):
    canVote = False

    with open('academicos.txt', 'r') as archivo:
        for linea in archivo:
            parts = linea.strip().split(':')

            readUser = parts[0].strip()
            readPassword = parts[1].strip()
            doVote = parts[2].strip()

            if user == readUser:
                if encryptedPassword == readPassword:
                    if doVote == "0":
                        canVote = True
                        c.send('You can vote'.encode())
                        print('User', user, 'can vote')
                        break
                    else:
                        c.send(str(user + ' has already voted').encode())
                        print('User', user, 'has already voted')
                        break
                else:
                    c.send('ERROR - Invalid password'.encode())
                    break
        else:
            c.send('ERROR - Invalid user'.encode())

    return canVote


def leerAcademicos():
    academicosArchivo = []
    with open('academicos.txt', 'r') as archivo:
        for linea in archivo:
            parts = linea.strip().split(':')

            readUser = parts[0].strip()
            readPassword = parts[1].strip()
            doVote = parts[2].strip()

            academicosArchivo.append(f"{readUser}:{readPassword}:{doVote}")

    return academicosArchivo


def cambiarAcademicos(user, academicosArchivo):
    for i, linea in enumerate(academicosArchivo):
        readUser, readPassword, readVote = linea.strip().split(':')
        if user == readUser:
            academicosArchivo[i] = f"{readUser}:{readPassword}:{1}\n"
        else:
            academicosArchivo[i] = f"{readUser}:{readPassword}:{readVote}\n"

    escribirAcademicos(academicosArchivo)


def escribirAcademicos(academicosArchivo):
    with open("academicos.txt", 'w') as file:
        file.writelines(academicosArchivo)


def leerPeliculas():
    films = "Películas:\n"

    with open('peliculas.txt', 'r') as archivo:
        for linea in archivo:
            parts = linea.strip().split(':')

            films = films + parts[0] + '\n'

    return films


def cambiarPeliculas(vote):
    pelicularArchivo = {}
    filmFound = False

    with open('peliculas.txt', 'r') as archivo:
        for linea in archivo:
            parts = linea.strip().split(':')

            if vote.lower() == parts[0].lower():
                parts[1] = str(int(parts[1]) + 1)
                pelicularArchivo[parts[0]] = parts[1]
                filmFound = True
            else:
                pelicularArchivo[parts[0]] = parts[1]

    escribirPeliculas(pelicularArchivo)
    return filmFound


def escribirPeliculas(pelicularArchivo):
    with open('peliculas.txt', 'w') as archivo:
        for film, voting in pelicularArchivo.items():
            archivo.write(f"{film}:{voting}\n")


def hilo(c):
    user = c.recv(1024).decode().lower()
    password = c.recv(1024)

    encryptedPassword = hashlib.sha256(password).hexdigest()

    canVote = validarUsuario(c, user, encryptedPassword)

    academicosArchivo = leerAcademicos()

    if canVote:
        films = leerPeliculas()

        c.send(films.encode())

        vote = c.recv(1024).decode()

        lock = threading.Lock()

        with lock:
            filmFound = cambiarPeliculas(vote)

            if filmFound:
                c.send('Voto registrado'.encode())

                cambiarAcademicos(user, academicosArchivo)

                print('User', user, 'Voto registrado')
            else:
                c.send('ERROR - Película no encontrada'.encode())

                print('User', user, 'ERROR - Película no encontrada')

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