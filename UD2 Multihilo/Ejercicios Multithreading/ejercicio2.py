import threading
from math import sqrt
import time
import random

def funcion(numero, entrada):
    primerMensaje = "[Persona " + str(numero) + "]: en cola"
    print(primerMensaje)

    with open('registro.txt', 'a') as file:
        file.write(f'{primerMensaje}\n')
        file.close()

    time.sleep(int(entrada)*1)

    mensajeFinal = "[Persona " + str(numero) + "]: con entrada tipo " + entrada + " ha entrado al espectaculo"
    print(mensajeFinal)

    with open('registro.txt', 'a') as file:
        file.write(f'{mensajeFinal}\n')
        file.close()

if __name__ == "__main__":

    with open('registro.txt', 'w') as file:
        pass

    entradas = ["1", "2", "3", "4"]

    for i in range(1, 11):
        hilo = threading.Thread(target=funcion, args=(i, random.choice(entradas)))
        hilo.start()