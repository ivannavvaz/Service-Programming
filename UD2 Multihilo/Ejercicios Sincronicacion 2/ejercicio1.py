import threading
from threading import Semaphore
import time

def lavadoCoche(semaforo):
    print("El " + str(threading.current_thread().name) + " en espera")
    time.sleep(2)
    with semaforo:
        print("Iniciando lavado del coche " + str(threading.current_thread().name))
        time.sleep(5)
    print("El "  + str(threading.current_thread().name) + " ya esta limpio")


if __name__ == "__main__":

    semaforo = Semaphore(1)

    threads = []

    for i in range(1, 21):
        hilo = threading.Thread(name='Coche'+str(i), target=lavadoCoche, args=(semaforo,))
        threads.append(hilo)
        hilo.start()

    for thread in threads:
        thread.join()

    print("El programa de lavado ha finalizado")