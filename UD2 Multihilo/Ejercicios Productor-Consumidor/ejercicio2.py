import threading
import time
import queue
import random

def productor(lock):
    while True:
        with lock:
            elementos = random.randint(1,3)
            print(f"Se producen {elementos} numeros")
            for i in range(elementos):
                numero = random.randint(1,10)
                q.put(numero)
                print(f"Se produce un {numero}")
        time.sleep(1)

def consumidor(lock):
    while True:
        elementos = random.randint(8,12)
        print(f"Se intentan consumir {elementos} numeros")
        while q.qsize() < elementos:
            print("Esperar a que hayan suficientes")
            time.sleep(1)
        with lock:  
            print(f"Se consumen los {elementos} numeros")
            for i in range(elementos):
                numero = q.get()
                print(f"Se consume un {numero}")
        time.sleep(1)

lock = threading.Lock()

q = queue.Queue()

t1 = threading.Thread(target=productor, args=(lock,))
t2 = threading.Thread(target=consumidor, args=(lock,))

t1.start()
t2.start()