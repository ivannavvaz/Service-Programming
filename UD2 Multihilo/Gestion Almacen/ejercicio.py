import threading
import time
import queue
import random
from threading import Lock, Thread

# Variables globales
productosOperarios = 0
productosCamiones = 0
dineroOperarios = {}

def operario(lock):
    jornada = 480
    global productosOperarios
    global dineroOperarios

    while jornada > 0:
        if jornada < 5:
            tiempoViaje = random.randint(1,jornada)
        else:
            tiempoViaje = random.randint(5,11)
        
        lock.acquire()
        if q.qsize() >= 3:
            q.get()
            q.get()
            q.get()
            print(f"El {threading.current_thread().name} ha sacado 3 productos")
            lock.release()
            jornada = jornada - tiempoViaje
            productosOperarios = productosOperarios + 3
            dineroOperarios[threading.current_thread().name] += 3
            time.sleep(tiempoViaje/10)
        else:
            print(f"El {threading.current_thread().name} está esperando")
            lock.release()
            jornada = jornada - 2
            time.sleep(0.2)
        

def camion(semaforo, lock):
    productosTransportados = random.randint(10,21)
    descargado = False
    global productosCamiones

    with semaforo: # Solo pueden descargar de 3 en 3
        while not descargado:

            lock.acquire()
            if q.qsize() + productosTransportados <= 100:
                descargado = True
                for _ in range(productosTransportados):
                    q.put("*")
                print(f"# El {threading.current_thread().name} ha metido {productosTransportados} en el almacen")
                productosCamiones = productosCamiones + productosTransportados
                lock.release()
                time.sleep(1)
            else:
                lock.release()
                time.sleep(0.5)


NUM_MUELLES = 3

lock = threading.Lock()
semaforo = threading.Semaphore(NUM_MUELLES)

threads = []

q = queue.Queue()
for i in range(1,101):
    q.put("*")

o1 = threading.Thread(target=operario, args=(lock,), name="Operario 1")
o2 = threading.Thread(target=operario, args=(lock,), name="Operario 2")
o3 = threading.Thread(target=operario, args=(lock,), name="Operario 3")
o4 = threading.Thread(target=operario, args=(lock,), name="Operario 4")
o5 = threading.Thread(target=operario, args=(lock,), name="Operario 5")

dineroOperarios['Operario 1'] = 0
dineroOperarios['Operario 2'] = 0
dineroOperarios['Operario 3'] = 0
dineroOperarios['Operario 4'] = 0
dineroOperarios['Operario 5'] = 0

o1.start()
o2.start()
o3.start()
o4.start()
o5.start()

for i in range(1, 51):
    hilo = threading.Thread(target=camion, args=(semaforo, lock,), name=f"Camion {i}")
    threads.append(hilo)
    hilo.start()
    time.sleep(0.5)

for i in threads:
    i.join()

o1.join()
o2.join()
o3.join()
o4.join()
o5.join()

print("==============================================")
print(f"En el almacen queda un total de {q.qsize()} productos")
print(f"Los operarios han sacado {productosOperarios} productos")
print(f"Los camiones han metido {productosCamiones} productos")
print("==============================================")
for clave, valor in dineroOperarios.items():
    print(f'El {clave} gana {valor} euros')
print("==============================================")
