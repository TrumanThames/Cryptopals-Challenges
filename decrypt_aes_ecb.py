import os
import sys
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from brk_rxc import b64_to_bytes
import nacl



def decrypt(text, key):
    padder = padding.PKCS7(128).padder()
    padded_text = padder.update(text) + padder.finalize()
    boole = False
    #print(dir(cryptography))
    #print(dir(cryptography.hazmat))
    #print(dir(cryptography.hazmat.backends))
    """
    while(not boole):
        try:
            back = cryptography.hazmat.backends.openssl.backend
            boole = True
        except:
            print("Exception Exception!!")
    """
    back = openssl.backend
    cipher = Cipher(algorithms.AES(key), modes.ECB(), back)
    decryptor = cipher.decryptor()
    return decryptor.update(padded_text) + decryptor.finalize()


if(__name__ == '__main__'):
    if(len(sys.argv) < 3):
        print("need two arguments, the file of the text to decrypt and the key")
    key = sys.argv[2]
    keyi = [ord(c) for c in key]
    keyb = bytes(keyi)
    fname = sys.argv[1]
    file0 = open(fname).read().replace("\n",'')
    print(decrypt(bytes(b64_to_bytes(file0)), keyb))
