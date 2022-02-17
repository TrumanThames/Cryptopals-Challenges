import random
import util
from util import modexp, randbytes
from sha1_mac import sha1
from cbc_decrypt import encrypt_cbc

p = 37
g = 5
a = random.randint(0, p-1)
A = modexp(g, a, p)
b = random.randint(0, p-1)
B = modexp(g, b, p)

s0 = modexp(B, a, p)
s1 = modexp(A, b, p)



class agent:
    p = None
    g = None
    a = None
    A = None
    sess_key = None

    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.a = random.randint(0, p-1)
        self.A = modexp(self.g, self.a, self.p)

    def gen_session_key(self, B):
        self.sess_key = modexp(B, self.a, self.p)

    def give_pubkey(self):
        return self.A

    def give_params(self):
        return self.p, self.g

    def encrypt_msg(self, msg, iv=None):
        # with aes cbc for now, iv should be 16 bytes
        k0 = self.sess_key
        if iv is None:
            iv = randbytes(16, 16)
        key = sha1(k0.to_bytes(16, 'big'))[:16]
        ctext = encrypt_cbc(msg, key, iv=iv)+iv
        return ctext

