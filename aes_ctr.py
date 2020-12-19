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
    # b0 and b1 are bytearrays, this function stops when one of 
    #b0 or b1 terminates, which isn't quite what an ideal xor would do
    #but is good 'nough for me
    z = zip(b0,b1)
    x = [y0^y1 for (y0,y1) in z]
    return bytes(x)
## 

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
    if l == 0:
        return b''
    text = [b'0']*l
    ctext = ctext
    for i in range(0,l-1):
        text[i] = decrypt_ctr_n(key, nonce, i, ctext[16*i:16*(i+1)])
    text[l-1] = decrypt_ctr_n(key, nonce, l-1, ctext[16*(l-1):min(16*l, len(ctext))])
    return reduce(lambda x,y:x+y, text)
    
