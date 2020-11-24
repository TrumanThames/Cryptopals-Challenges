from decrypt_aes_ecb import encrypt, decrypt
from math import ceil
from functools import reduce


def little_end(n):
    # n is an int from 0 to (2**64)-1 (a 64 bit uint or whatever)
    bytez = [0]*8
    for i in range(0,8):
        bytez[i] = (n>>(i*8))%256
    return bytes(bytez)

def bytes_xor(b0, b1):
    # b0 and b1 are same length bytearrays, 
    b0z = [i for i in b0]
    b1z = [i for i in b1]
    x = [i^j for (i,j) in zip(b0z, b1z)]
    return bytes(x)

def encrypt_ctr_n(key, nonce, n, text):
    l = len(text)
    text = text + b'\x00'*(16-l)
    return bytes_xor(encrypt(nonce+little_end(n), key), text)[:l]

def decrypt_ctr_n(key, nonce, n, ctext):
    l = len(ctext)
    ctext = ctext+(b'\x00'*(16-l))
    return bytes_xor(encrypt(nonce+little_end(n), key), ctext)[:l]

def encrypt_ctr(key, nonce, text):
    l = ceil(len(text)/16)
    ctext = [b'0']*l
    for i in range(0,l):
        ctext[i] = encrypt_ctr_n(key, nonce, i, text[16*i:16*(i+1)])
    return reduce(lambda x,y:x+y, ctext)

def decrypt_ctr(key, nonce, ctext):
    l = ceil(len(ctext)/16)
    text = [b'0']*l
    for i in range(0,l):
        text[i] = decrypt_ctr_n(key, nonce, i, ctext[16*i:16*(i+1)])
    return reduce(lambda x,y:x+y, text)
