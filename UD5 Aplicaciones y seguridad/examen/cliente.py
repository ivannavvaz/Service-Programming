import socket
import sys

def Main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    user = input("Escribe un usuario: ")
    s.send(user.encode())

    password = input("Escribe una contraseña: ")
    s.send(password.encode())

    print()

    data = s.recv(1024).decode()

    if data == "You can vote":
        data = s.recv(1024).decode()
        print(data)

        vote = input("Escribe el nombre de la película: ")
        s.send(vote.encode())

        data = s.recv(1024).decode()
        print('Result:', data)
    else:
        print('Result:', data)

    # S cierra la conexión
    s.close()


if __name__ == '__main__':
    Main()