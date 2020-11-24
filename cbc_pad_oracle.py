from pkcs7_pad_val import pad_val
from cbc_decrypt import encrypt_cbc, decrypt_cbc
from pkcs_pad import pad
from brk_rxc import b64_to_bytes
import ecb_cbc_oracle
from random import randint
from byte_ecb_decryption import check_block_length
from functools import reduce

def b64_bytes(b64):
    return bytes(b64_to_bytes(b64))

rankey = ecb_cbc_oracle.gen_bytes(16)
iv = ecb_cbc_oracle.gen_bytes(16)

strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

def choose_string(strs):
    return b64_bytes(strs[randint(0,len(strs)-1)])

def encryptOh():
    return (iv, encrypt_cbc(pad(choose_string(strings)), rankey, iv))

def decryptOh(iv0, ctext):
    ptext = decrypt_cbc(ctext, rankey, iv0)
    #print(ptext)
    try:
        pad_val(ptext)
    except:
        return False
    else:
        return True

def xor_blk_with(iv, ctext, bX, whr, blocksize):
    l = int(len(ctext)/blocksize)
    if l == 1:
        iv0 = [i for i in iv]
        iv0[15-whr] = iv0[15-whr] ^ bX
        return (bytes(iv0), ctext)
    else:
        ct0 = ctext[(l-2)*blocksize+15-whr] ^ bX
        ctext0 = ctext[:(l-2)*blocksize+15-whr]+bytes([ct0])+ctext[(l-2)*blocksize+16-whr:]
        return (iv, ctext0)

def sub_byte_wrap(n0, n1):
    return (n0-n1)%256

def add_byte_wrap(n0, n1):
    return (n0+n1)%256

def increment(iv, ctext, whr, blocksize):
    if whr == 0:
        return (iv, ctext)
    l = len(ctext)
    if l > blocksize:
        return (iv, ctext[:l-blocksize-whr]+bytes([i^whr^(whr+1) for i in ctext[l-blocksize-whr:l-blocksize]]) + ctext[l-blocksize:])
    else:
        return (iv[:blocksize-whr]+bytes([i^whr^(whr+1) for i in iv[blocksize-whr:]]), ctext)


def last_block(iv, ctext, padoracle, blocksize):
    l = int(len(ctext)/blocksize)
    if l <= 1:
        las_blok = [i for i in iv]
    else:
        las_blok = [i for i in ctext[(l-1)*blocksize:l*blocksize]]
    las_blok = [0]*16
    boole = False
    for whr in range(0,16):
        #print(boole)
        boole = False
        #print(whr)
        #print("pre increment: ")
        #print(iv, ctext)
        (iv, ctext) = increment(iv, ctext, whr, blocksize)
        #print("post increment: ")
        #print(iv, ctext)
        for bX in range(0,256):
            (ivX, ctextX) = xor_blk_with(iv, ctext, bX, whr, blocksize)
            #print(iv, ivX)
            boole = padoracle(ivX, ctextX)
            if boole:
                #print(bX)
                #print(ivX, ctextX)
                #because the plaintext could've ended in ...020x, and so on
                #actually, maybe this can only happen when whr is 0
                if whr == 0:
                    (ivY, ctextY) = xor_blk_with(ivX, ctextX, 234, whr+1, blocksize)
                    if padoracle(ivY,ctextY):
                        las_blok[15-whr] = bX ^ (whr+1)
                        ctext = ctextX
                        iv = ivX
                    else:
                        boole = False
                else:
                    las_blok[15-whr] = bX ^ (whr+1)
                    ctext = ctextX
                    iv = ivX
            if boole:
                break
    #print(las_blok)
    return bytes(las_blok)

def oracular_crack(iv, ctext, padoracle=decryptOh):
    blocksize = 16
    #len ctext needs to be a multiple of blocksize, or I think bad things happen
    #actually, it may just ignore the last bit after the last full blocksize bit
    l = int(len(ctext)/blocksize)
    stuff = [] # is gonna be the list of decoded bytearrays
    for i in range(0,l):
        lb = last_block(iv, ctext[:(i+1)*blocksize], padoracle, blocksize)
        stuff.append(lb)
    return reduce(lambda x,y:x+y, stuff)
