import socket

host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024

# Creamos un objeto socket tipo TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5) # Esperamos la conexión del cliente
conn, addr = s.accept() # Establecemos la conexión con el cliente

with conn:
    print('[*] Conexión establecida')
    while True:
        # Recibimos bytes, convertimos en str
        data = conn.recv(BUFFER_SIZE)
        # Verificamos que hemos recibido datos
        if not data:
            break   
        else:
            print('[*] Datos recibidos: {}'.format(data.decode('utf-8')))
            conn.send(data) # Hacemos echo convirtiendo de nuevo a bytes