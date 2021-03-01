#moving to using pycryptodome from cryptography for this one
from Cryptodome.Hash import SHA1
from ecb_cbc_oracle import gen_bytes
from ctr_bitflippin import xor
import random

K0 = gen_bytes(24)

def macify(mensaje, key = K0):
    hashy = SHA1.new(key + mensaje)
    return hashy.digest()

def sha1(T): return macify(T, b'')

def mac_check(mensaje, mac):
    hashy = SHA1.new(K0 + mensaje)
    if mac != hashy.digest():
        return False
    else:
        return True

T = b'Bananas fortify the soil and strengthen the heart. If you should chance upon a bunch of bananas or a fistful of fingers, you should take care to not uproot the blessed banana tree!!!!!!?'

def test_macify(n=1000, text = T, key = K0):
    H0 = macify(key, text)
    for i in range(0,n):
        rbytes0 = gen_bytes(100)
        mtext = xor(text, rbytes0)
        mHash0 = macify(mtext, key)
        mkey = gen_bytes(24)
        mHash1 = macify(text, mkey)
        mHash2 = macify(mtext, mkey)
        if mHash0 == H0:
            print("000 What da, why are these dang things equal!?!")
            print(key)
            print(text)
            print(key)
            print(mtext)
            return False
        if mHash1 == H0:
            print("111 What da, why are these dang things equal!?!")
            print(key)
            print(text)
            print(mkey)
            print(text)
            return False
        if mHash2 == H0:
            print("222 What da, why are these dang things equal!?!")
            print(key)
            print(text)
            print(mkey)
            print(mtext)
            return False
    print("None of them were equal yay!!")
    return True
