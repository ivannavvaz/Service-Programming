import ftplib
import sys

# Servidor externo gratuito para pruebas
#FTP_HOST = "ftpServer.dlptest.com"
#FTP_USER = "dlpuser"
#FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu" # este password puede cambiar

FTP_HOST = "127.0.0.1"
FTP_PORT = 2121

#FTP_USER = "user"
#FTP_PASS = "password" # este password puede cambiar

#FTP_USER = "anonymous"
#FTP_PASS = "" # este password puede cambiar

# Crear una instancia del cliente FTP
ftp = ftplib.FTP()

def listCallBack(line):
    print(line)

def listarDirectorio():
    try:
        print()
        lista = ftp.retrlines("LIST", listCallBack)
        print('-------------------')
        print(lista)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()

def mostratRuta():
    try:
        print()
        ruta_actual = ftp.pwd()
        print(f"Ruta actual: {ruta_actual}")
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()

def crearDirectorio(nombreDirectorio):
    try:
        print()
        ftp.mkd(nombreDirectorio)
        print("Directiorio creado: " + nombreDirectorio)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()

def subirFichero(nombreFichero):
    try:
        print()
        with open(nombreFichero, "rb") as file:
            ftp.storbinary(f"STOR {nombreFichero}", file)
            print("Fichero descargado: " + nombreFichero)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()
    except Exception as e:
        print(f"Se ha producido una excepción: {e}")
        print()

def descargarFichero(nombreFichero):
    try:
        print()
        with open(nombreFichero, 'wb') as local_file:
            ftp.retrbinary(f"RETR {nombreFichero}", local_file.write)
        print("Fichero descargado: " + nombreFichero)
        print()
    except ftplib.error_perm as e:
        print("Fichero no exite")
        print('-------------------')
        lista = ftp.retrlines("LIST", listCallBack)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()
    except Exception as e:
        print(f"Se ha producido una excepción: {e}")
        print()


def borrarFichero(nombreFichero):
    try:
        print()
        ftp.delete(nombreFichero)
        print("Fichero borrado: " + nombreFichero)
        print()
    except ftplib.error_perm as e:
        print("Fichero no exite")
        print('-------------------')
        lista = ftp.retrlines("LIST", listCallBack)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()


def cambiarDirectorio(nombreDirectorio):
    try:
        print()
        ftp.cwd(nombreDirectorio)
        ruta_actual = ftp.pwd()
        print(f"Ruta actual: {ruta_actual}")
        print()
    except ftplib.error_perm as e:
        print("Directorio no exite")
        print('-------------------')
        lista = ftp.retrlines("LIST", listCallBack)
        print()
    except ftplib.all_errors as e:
        print(str(e))
        print()

def listarOpciones():
    print()
    print("## Opciones")
    print("l - Listar directorios")
    print("p - Mostrar ruta")
    print("d <nombreDirectorio> - Crear directorio")
    print("f <nombreArchivo> - Subir fichero")
    print("g <nombreArchivo> - Descargar archivo")
    print("r <nombreArchivo> - Borrar fichero")
    print("c <nombreDirectorio> - Cambiar directorio")
    print("quit - Cerrar conexion")
    print()


def contar_palabras(cadena):
    palabras = cadena.split()
    cantidad_palabras = len(palabras)
    return cantidad_palabras


def run():
    FTP_USER = ""
    FTP_PASS = ""
    error = False

    print("1 Conectarse como usuario")
    print("2 Conectarse como anonimo")
    opcion = input("Opcion: ")

    if opcion == "1":
        FTP_USER = input("Usuario: ")
        FTP_PASS = input("Contraseña: ")

    elif opcion == "2":
        FTP_USER = "anonymous"
        FTP_PASS = ""

    else:
        error = True

    if error == False:
        try:
            # Conexion a FTP
            # ftpServer = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USER, FTP_PASS)
            ftp.encoding = "utf-8"
            print(ftp.getwelcome())
            print()

            conexionAbierta = True

            while conexionAbierta:
                opcion = input("ftpServer> ")
                opcion = opcion.lower()

                if opcion == "l":
                   listarDirectorio()

                elif opcion == "p":
                    mostratRuta()

                elif contar_palabras(opcion) == 2:

                    if opcion.split()[0] == "d":
                        crearDirectorio(opcion.split()[1])

                    elif opcion.split()[0] == "f":
                        subirFichero(opcion.split()[1])

                    elif opcion.split()[0] == "g":
                        descargarFichero(opcion.split()[1])

                    elif opcion.split()[0] == "r":
                        borrarFichero(opcion.split()[1])

                    elif opcion.split()[0] == "c":
                        cambiarDirectorio(opcion.split()[1])

                elif opcion == "quit":
                    ftp.close()
                    conexionAbierta = False

                elif opcion == "help":
                    listarOpciones()

                else:
                    print()
                    print("Opcion Incorrecta")
                    print()

        except ftplib.all_errors as e:
            print(str(e))

        except Exception as e:
            print()
            print(f"Se ha producido una excepción: {e}")
            print()
    else:
        print("ERROR - Opcion incorrecta")

if __name__ == "__main__":
    run()