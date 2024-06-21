from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

# Genera la keys privada y publica
def generar_keys():
    key = RSA.generate(2048, randfunc=get_random_bytes) # Genera la clave
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Cifrar con la clave pública
def cifrar(public_key, txtplano):
    key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    txtcifrado = cipher_rsa.encrypt(txtplano.encode())
    return txtcifrado

# Descifrar con la clave privada
def descifrar(private_key, txtcifrado):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    txtplano = cipher_rsa.decrypt(txtcifrado).decode()
    return txtplano

if __name__ == "__main__":
    private_key, public_key = generar_keys()
    
    mensaje = "Hola Mundo!"
    mensaje_cifrado = cifrar(public_key, mensaje)
    mensaje_descifrado = descifrar(private_key, mensaje_cifrado)
    
    print("Original message:", mensaje)
    print("Encrypted message:", mensaje_cifrado)
    print("Decrypted message:", mensaje_descifrado)



