import shutil
import time
import os
import multiprocessing
import hashlib

def comprobador(ruta, diccionario_hash_pasado, copia_src):

    for root, dirs, files in os.walk(monitored_directory):
        for file in files:
            file_path = os.path.join(root, file)
            hash_actual = calcular_hash(file_path)
            if hash_actual != diccionario_hash_pasado.get(file_path):
                print(f"File {file_path} has changed.")
                with open('archivo.txt', 'a') as archivo:
                    archivo.write(str(os.getpid()))
                    archivo.write("File" + file_path + "has changed.")
                shutil.rmtree(copia_src)
                shutil.copytree(ruta, copia_src)
                diccionario_hash_pasado[file_path] = hash_actual

    return diccionario_hash_pasado


def calcular_hash(ruta):
    sha256 = hashlib.sha256()
    with open(ruta, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def calcular_hash_inicial(ruta):
    diccionario_hashes = {}

    for root, dirs, files in os.walk(ruta):
        for dir in dirs:
            ruta_fichero = os.path.join(root, dir)
            diccionario_hashes[ruta_fichero] = calcular_hash(ruta_fichero)
        for file in files:
            ruta_fichero = os.path.join(root, file)
            diccionario_hashes[ruta_fichero] = calcular_hash(ruta_fichero)

    return diccionario_hashes


if __name__ == "__main__":

    multiprocessing.set_start_method("spawn")

    #src = "/media/dam/IVAN DAM1/DAM2/Programacion de servicios - Patxi/UD1 Procesos/Ejercicios multiproceso/DropBox1"

    src1 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox1'''
    copia_src1 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox1'''
    src2 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox2'''
    copia_src2 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox2'''
    src3 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox3'''
    copia_src3 = r'''E:\DAM2\Programacion de servicios - Patxi\UD1 Procesos\Ejercicios multiproceso\DropBox3'''


    if not os.path.exists(src1):
        os.mkdir(src1)

    if not os.path.exists(src2):
        os.mkdir(src2)

    if not os.path.exists(src3):
        os.mkdir(src3)

    if not os.path.exists("copia"):
        os.mkdir("copia")


    diccionario_hashes_p1 = calcular_hash_inicial(src1)
    diccionario_hashes_p2 = calcular_hash_inicial(src2)
    diccionario_hashes_p3 = calcular_hash_inicial(src3)


    while True:
        pool = multiprocessing.Pool(3)
        res = pool.starmap(monitor, [(src1, diccionario_hashes_p1, copia_src1), (src1, diccionario_hashes_p2, copia_src2), (src1, diccionario_hashes_p3, copia_src3)])

        diccionario_hashes_p1 = res[0]
        diccionario_hashes_p2 = res[1]
        diccionario_hashes_p3 = res[2]

        pool.close()
        time.sleep(5)
