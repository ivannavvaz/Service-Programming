import threading
from math import sqrt
import time

def funcion(numero):
    print("[Hilo " + str(numero) + "]: INICIO")
    time.sleep(3)
    print("[Hilo " + str(numero) + "]: FINAL")

if __name__ == "__main__":

    hilos = []

    for i in range(1, 11):
        hilo = threading.Thread(target=funcion, args=(i,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("FIN DEL PROGRAMA PRINCIPAL")