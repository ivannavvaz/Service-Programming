import multiprocessing, os
import time
import math
import random

mylist = ['+','-','$','&','!','<','>','#','*','/']

def selector(mylist, nveces):

    resultado = os.getpid(), random.choice(mylist), nveces

    if __name__ == "__main__":
        for i in range(nveces):
            print("PADRE", resultado)
    else:
        for i in range(nveces):
            print(resultado)


    print()

        
if __name__ == "__main__":

    multiprocessing.set_start_method("spawn")

    for i in range(3):
        multiprocessing.Process(target=selector, args=(mylist, random.randrange(5, 10))).start()

    selector(mylist, random.randrange(5, 10))

    for i in range(10):
        print("0")
    print()
