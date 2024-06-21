import socket

# El cliente debe tener las mismas especificaciones del servidor
host = socket.gethostname()
port = 12345
BUFFER_SIZE = 1024
MESSAGE = 'Hola, mundo!' # Datos que queremos enviar

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
# Convertimos str a bytes
s.send(MESSAGE.encode('utf-8'))
data = s.recv(BUFFER_SIZE)