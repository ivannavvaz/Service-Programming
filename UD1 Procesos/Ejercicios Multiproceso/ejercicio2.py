import multiprocessing, os
import time
import math

mylist = [1,4,9,16,25,36,49,64,81,100]

def raices(x):
    if __name__ == "__main__":
        print("PROCESO PADRE "+str(os.getpid()))
    else:
        print("PROCESO HIJO " + str(os.getpid()) + " y PADRE " + str(os.getppid()))
    return int(math.sqrt(x))    

if __name__ == "__main__":

    multiprocessing.set_start_method("spawn")      
    pool = multiprocessing.Pool(4)
    result = pool.map(raices,mylist)
    
    print(result)