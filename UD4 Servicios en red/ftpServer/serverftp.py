"""
FTP Server
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Crear un autorizador
authorizer = DummyAuthorizer()

# Añadir usuarios, permisos explicados al final del documento
authorizer.add_user("user", "password", ".", perm="elradfmw")
authorizer.add_anonymous("./public", perm="elradfmw")

# Crear el manejador FTP
handler = FTPHandler
handler.authorizer = authorizer

# Crear el servidor FTP, que utiliza el manejador
server = FTPServer(("127.0.0.1", 2121), handler)

# Iniciar el servidor para escuchar, hay otras maneras
server.serve_forever()