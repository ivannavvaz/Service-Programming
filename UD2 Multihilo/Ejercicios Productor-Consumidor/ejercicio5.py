import threading
import time
import queue
import random

def productor(lock):
    while True:
        with lock:
            if q.qsize() < 31:
                elementos = random.randint(1,10)
                if elementos + q.qsize() > 30:
                    elementos = 30 - q.qsize()
                print(f"{threading.current_thread().name} | Se producen {elementos} numeros | Capacidad {q.qsize()}")
                for i in range(elementos):
                    numero = random.randint(1,10)
                    q.put(numero)
                    print(f"-> Se produce un {numero}")
        time.sleep(random.randint(1,3))

def consumidor(lock):
    while True:
        elementos = random.randint(3,6)
        elementosConsumidos = 0
        while elementosConsumidos != elementos:
            with lock:
                while q.qsize() > 0 and elementosConsumidos != elementos:
                    numero = q.get()
                    print(f"Se consume un {numero}")
                    elementosConsumidos += 1
        print(f"{threading.current_thread().name} # Se han consumen los {elementos} numeros")
        time.sleep(random.randint(1,3))

lock = threading.Lock()

q = queue.Queue()

t1 = threading.Thread(target=productor, args=(lock,), name="Productor 1")
t2 = threading.Thread(target=consumidor, args=(lock,), name="Consumidor 1")
t3 = threading.Thread(target=productor, args=(lock,), name="Productor 2")
t4 = threading.Thread(target=consumidor, args=(lock,), name="Consumidor 2")

t1.start()
t2.start()
t3.start()
t4.start()