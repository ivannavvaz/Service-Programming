import threading
from math import sqrt
import time

bloqueo = threading.Lock()

def beber(numeroHilo):
    time.sleep(0.5)
    with bloqueo:
        print("Persona" + str(numeroHilo) + " coge la jarra")
        time.sleep(0.5)
        print("Persona" + str(numeroHilo) + " saboreando...")
        time.sleep(0.5)
        print("Persona" + str(numeroHilo) + " deja la jarra")
        print("-----------------------")

if __name__ == "__main__":

    threads = []

    for i in range(1, 11):
        hilo = threading.Thread(target=beber, args=(i,))
        threads.append(hilo)
        hilo.start()

    for thread in threads:
        thread.join()

print("Todas las personas están satisfechas")