import threading
from math import sqrt
import time, random

bloqueo = threading.Lock()

def beber(numeroHilo):

    global jarra

    contador = 0

    time.sleep(random.randint(1,10)*0.5)
    while jarra >= 1:
        time.sleep(random.randint(1,10)*0.5)    
        with bloqueo:
            if jarra >= 1:
                print("Persona" + str(numeroHilo) + " coge la jarra")
                time.sleep(0.1)
                print("Persona" + str(numeroHilo) + " saboreando...")
                jarra -= 1
                contador += 1
                time.sleep(0.1)
                print("Persona" + str(numeroHilo) + " deja la jarra")
                print("-----------------------")
        time.sleep(0.1)

    time.sleep(1)

    print("Persona" + str(numeroHilo) + " - Jarras bebidas: " + str(contador))

if __name__ == "__main__":

    jarra = 100

    threads = []

    for i in range(1, 11):
        hilo = threading.Thread(target=beber, args=(i,))
        threads.append(hilo)
        hilo.start()

    for thread in threads:
        thread.join()

print("Ya no queda cerveza")