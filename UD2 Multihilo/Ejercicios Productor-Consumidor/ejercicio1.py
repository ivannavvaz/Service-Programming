import threading
import time
import queue
import random

def productor(lock):
    while True:
        with lock:
            if q.empty():
                numero = random.randint(1,10)
                q.put(numero)
                print(f"Se produce un {numero}")
        time.sleep(0.3)

def consumidor(lock):
    while True:
        with lock:
            if not q.empty():
                numero = q.get()
                print(f"Se consume un {numero}")
        time.sleep(0.3)

lock = threading.Lock()

q = queue.Queue()

t1 = threading.Thread(target=productor, args=(lock,))
t2 = threading.Thread(target=consumidor, args=(lock,))

t1.start()
t2.start()