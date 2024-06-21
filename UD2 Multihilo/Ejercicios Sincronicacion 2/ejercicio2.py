import threading
from threading import Condition
import time, random

def reservarAsiento(cond):

    time.sleep(random.randint(1,5))
    reservado = False

    while butacas.__contains__("") and reservado == False:

        asientoReservar = random.randint(0,4)
        #print("INTENTANDO RESERVAR " + str(threading.current_thread().name))

        with cond:   
            if "" not in butacas:
                    break  
                
            cond.wait()
            #print(asientoReservar)

            if butacas[asientoReservar] == "":
                time.sleep(1)
                butacas[asientoReservar] = str(threading.current_thread().name)
                time.sleep(1)
                print(str(threading.current_thread().name) + " ha reservado el asiento " + str(asientoReservar))
                reservado = True
                #print(butacas)
            else:
                print(str(threading.current_thread().name) + " NO puede reservar el asiento " + str(asientoReservar))
                time.sleep(2)
                
            cond.notify()
            
if __name__ == "__main__":

    nombre = ["Ivan", "Unai", "Yago", "Maria", "Marc", "Patxi"]

    butacas = ["","","","",""]

    threads = []

    cond = threading.Condition()

    for i in range(1, 7):
        hilo = threading.Thread(name=nombre[i-1], target=reservarAsiento, args=(cond,))
        threads.append(hilo)
        hilo.start()

    time.sleep(5)

    with cond:
        cond.notify()

    for thread in threads:
        thread.join()

    print("===============================")
    print("Reservadad:", butacas)

    sin_asiento = set(nombre) - set(butacas)
    if sin_asiento:
            print(f"{', '.join(sin_asiento)} no tienen asiento.")

    