import threading
from math import sqrt
import time, random

bloqueo = threading.Lock()

def beber(numeroHilo):

    global jarra
    global lista

    time.sleep(random.randint(1,10)*0.5)
    while jarra >= 1:
        time.sleep(random.randint(1,10)*0.5)
        with bloqueo:
            if jarra >= 1:
                print("Persona" + str(numeroHilo) + " coge la jarra")
                time.sleep(0.1)
                print("Persona" + str(numeroHilo) + " saboreando...")
                jarra -= 1
                lista[numeroHilo-1] += 1
                time.sleep(0.1)
                print("Persona" + str(numeroHilo) + " deja la jarra")
                print("-----------------------")
        time.sleep(0.1)

if __name__ == "__main__":

    jarra = 120

    lista = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    threads = []

    for i in range(1, 11):
        hilo = threading.Thread(target=beber, args=(i,))
        threads.append(hilo)
        hilo.start()

    for thread in threads:
        thread.join()

    for r, i in enumerate(lista) :
        print("Persona" + str(r+1) + " - Jarras bebidas: " + str(i))

    print("Persona que mas a bebido:", lista.index(max(lista))+1)

print("Todas las personas están satisfechas")