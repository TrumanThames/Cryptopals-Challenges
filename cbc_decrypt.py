import sys
import pkcs_pad
from brk_rxc import b64_to_bytes
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import functools

def bytes_xor(bytes0, bytes1, blocksize=16):
    i = (int.from_bytes(bytes0, 'big'))^(int.from_bytes(bytes1, 'big'))
    return i.to_bytes(blocksize, 'big')

def bytes_flatten(listbytes, actually=True):
    if actually:
        return functools.reduce(lambda x,y: x+y, listbytes)
    else:
        return listbytes


def encrypt_cbc(text, key, iv=bytes([0]*16), blocksize=16):
    #Assumes iv is length blocksize and that key is a valid length 
    text = pkcs_pad.pad(text, blocksize)
    blcks = int(len(text)/blocksize)
    ciphtext = []
    cipht = iv
    back = openssl.backend
    cipher = Cipher(algorithms.AES(key), modes.ECB(), back)
    for i in range(0,blcks):
        #cipher.__init__(algorithms.AES(key), modes.ECB(), back)
        encryptor = cipher.encryptor()
        xcipht = bytes_xor(cipht, text[i*blocksize:i*blocksize+blocksize])
        #print("cipht: "+str(cipht))
        #print("text[i:i+blcksz]: "+str(text[i*blocksize:i*blocksize+blocksize]))
        #print("xcipht: "+str(xcipht))
        cipht = encryptor.update(xcipht) + encryptor.finalize()
        ciphtext.append(cipht)
    return bytes_flatten(ciphtext)

def decrypt_cbc(ctext, key, iv=bytes([0]*16), blocksize=16):
    blcks = int(len(ctext)/blocksize)
    text = []
    decr = ''
    back = openssl.backend
    cipher = Cipher(algorithms.AES(key), modes.ECB(), back)
    for i in range(0, blcks):
        #cipher.__init__(algorithms.AES(key), modes.ECB(), back)
        decryptor = cipher.decryptor()
        if i == 0:
            cipht = iv
        else:
            cipht = ctext[i*blocksize-blocksize:i*blocksize]
        decr = bytes_xor(cipht, decryptor.update(ctext[i*blocksize:i*blocksize+blocksize]) + decryptor.finalize())
        text.append(decr)
    return bytes_flatten(text)

import random

def test_bytes_xor(n=1000):
    for i in range(0,n):
        x = random.randint(0,2**128)
        y = random.randint(0,2**128)
        bx = x.to_bytes(16,'big')
        by = y.to_bytes(16,'big')
        if(int.from_bytes(bytes_xor(bx,by), 'big') != (y^x)):
           print("AAAAAH")
           print("x = "+str(x)+"   y = "+str(y))
           break
    print("Seems Okay")
    return


if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Need two arguments, the text file to encrypt and the key")
        sys.exit()
    fname = sys.argv[1]
    ctext = open(fname).read().replace("\n",'')
    key = sys.argv[2]
    if((len(key) != 16) and (len(key) != 24) and (len(key) != 32)):
        print("the key must be length 16, 24, or 32")
        sys.exit()
    initv = bytes([0]*16)
    dtext = decrypt_cbc(bytes(b64_to_bytes(ctext)), key.encode(), initv, 16)
    print(dtext)

