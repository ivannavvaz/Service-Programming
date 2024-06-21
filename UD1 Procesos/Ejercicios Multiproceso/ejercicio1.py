import multiprocessing, os
from math import sqrt
import time

def tarea():
    print('Duerme 0.5 segundos')
    time.sleep(0.5)
    print('Fin del descanso')


def calculadora_suma_raiz_cuadrada():
    mylist = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    suma = 0
    for i in mylist:
        suma = suma + sqrt(i)

    if __name__ == "__main__":
        print("Proceso PADRE: " + str(os.getpid()), suma)
    else:
        print("Proceso HIJO: " + str(os.getpid()) + " | PADRE: " + str(os.getppid()))


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    p1 = multiprocessing.Process(target=calculadora_suma_raiz_cuadrada)
    p1.start()
    p1.join()

    calculadora_suma_raiz_cuadrada()


