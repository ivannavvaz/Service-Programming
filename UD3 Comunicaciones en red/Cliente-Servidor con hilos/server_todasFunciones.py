import socket
import threading
import time

def hilo(c, listaClase, diccionarioPC):
    nombre = threading.current_thread().name
    while True:
        opciones = ("Elige una opcion:\n 1) Revertir cadena\n 2) Ver si numero es primo\n 3) Diga si una persona esta en la clase\n 4) Diga el puesto de PC de una persona de clase\n 5) Cifrado cesar")
        c.send(opciones.encode())

        # datos recibidos de un cliente
        try:
            opcion = c.recv(1024)
        except:
            print('Adios '+nombre)
            break

        print('Recibido',nombre,':', opcion.decode())

        # todas las funciones
        if opcion.isdigit():
            opcion = float(opcion)

            # revertir cadena
            if opcion == 1:
                mensaje = ("- Escribe una cadena para revertirla -")
                c.send(mensaje.encode())

                frase = c.recv(1024)

                resultado = frase[::-1].decode('utf-8')

            # numero es primo?
            elif opcion == 2:
                mensaje = ("- Escribe un numero -")
                c.send(mensaje.encode())

                numero = c.recv(1024)

                if numero.isdigit():
                    numero = float(numero)
                    if numero < 2:
                        resultado = f"{numero} no es un número primo"
                    else:
                        es_primo = True
                        for i in range(2, int(numero ** 0.5) + 1):
                            if numero % i == 0:
                                es_primo = False
                                break
                        if es_primo:
                            resultado = f"{numero} es un número primo"
                        else:
                            resultado = f"{numero} no es un número primo"
                else:
                    resultado = "ERROR - No has proporcionado un numero"

            # pertenece a la clase?
            elif opcion == 3:
                mensaje = ("- Escribe un nombre -")
                c.send(mensaje.encode())

                nombre = c.recv(1024)

                if nombre.decode().lower() in listaClase:
                    resultado = f"{nombre.decode()}, pertenece a la clase"
                else:
                    resultado = f"{nombre.decode()}, no pertenece a la clase"

            # puesto de pc?
            elif opcion == 4:
                mensaje = ("- Escribe un numero de PC -")
                c.send(mensaje.encode())

                numeroPC = c.recv(1024)

                if numeroPC.isdigit():
                    if int(numeroPC) not in diccionarioPC:
                        resultado = "ERROR - Puesto no disponible"
                    else:
                        resultado = diccionarioPC.get(int(numeroPC))
                else:
                    resultado = "ERROR - No has proporcionado un numero"

            # cifrado cesar
            elif opcion == 5:
                mensaje = ("- Escribe una cadena para cifrarla -")
                c.send(mensaje.encode())

                cadena = c.recv(1024)

                resultado = ""
                for caracter in cadena.decode():
                    if caracter.isalpha():
                        posicionesAMover = 3
                        if caracter.islower():
                            resultado += chr((ord(caracter) - ord('a') + posicionesAMover) % 26 + ord('a'))
                        elif caracter.isupper():
                            resultado += chr((ord(caracter) - ord('A') + posicionesAMover) % 26 + ord('A'))
                    else:
                        resultado += caracter

            # opcion invalida
            else:
                resultado = "ERROR - Opcion invalida"

        # no se proporciona un numero
        else:
            resultado = "ERROR - No has proporcionado un numero"

        # Enviamos los datos al cliente
        c.send(resultado.encode())
        time.sleep(0.5)

    c.close() # Cerramos la conexión

def Main():
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('Habilitamos el socket en el puerto', port)
    s.listen()
    print('Servidor preparado y a la escucha...')
    ncliente = 1

    listaClase = ["ivan", "yago", "maria", "unai", "marc"]
    diccionarioPC = {1: "ivan", 2: "yago", 3: "maria", 4: "unai", 5: "marc"}

    while True:
        # Acepta conexion del cliente
        c, addr = s.accept()
        cliente = 'cliente'+str(ncliente) # Numeramos los clientes
        print('Conectado',cliente,' :', addr[0], '-', addr[1])
        h = threading.Thread(name=cliente, target=hilo, args=(c, listaClase, diccionarioPC,))
        h.start()
        ncliente += 1
        
    s.close()

if __name__ == '__main__':
    Main()