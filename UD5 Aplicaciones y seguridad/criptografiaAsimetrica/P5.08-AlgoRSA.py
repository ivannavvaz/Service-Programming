import random
import math

def MCD(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def es_primo(num):
  for i in range(2, int(num / 2)):
    if (num % i) == 0:
      return False
  return True

def gen_primo(bits):
    while True:
        num = random.getrandbits(bits)
        if es_primo(num):
            return num

def generar_keys(bits):
    p = gen_primo(bits)
    q = gen_primo(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(1, phi)
        if MCD(e, phi) == 1:
            break
    d = mod_inverse(e, phi)
    return ((d, n), (e, n))

def cifrar(pk, txtplano):
    e, n = pk
    txtcifrado = [pow(ord(char), e, n) for char in txtplano]
    return txtcifrado

def descifrar(pk, txtcifrado):
    d, n = pk
    txtplano = [chr(pow(char, d, n)) for char in txtcifrado]
    return ''.join(txtplano)

if __name__ == "__main__":
    bits = 16
    private_key, public_key = generar_keys(bits)
    mensaje = "Hola Mundo!"
    mensaje_cifrado = cifrar(public_key, mensaje)
    mensaje_descifrado = descifrar(private_key, mensaje_cifrado)
    
    print("Original message:", mensaje)
    print("Encrypted message:", mensaje_cifrado)
    print("Decrypted message:", mensaje_descifrado)
