import ch33_diff_hell as dh
from sha1_mac import sha1
from cbc_decrypt import encrypt_cbc, decrypt_cbc





class mal_agent:
    p = None
    g = None
    A = None
    B = None

    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.key = None

    def get_1(self, A):
        self.A = A

    def get_2(self, B):
        self.B = B

    def send_to_(self):
        # sending this to the agents will ensure the sess_key
        # they generate is just 0 = int.to_bytes(0, 16)
        self.key = sha1(int.to_bytes(0, 16, 'big'))[:16]
        return self.p

    def mitm(self, ctext, iv=None):
        youjustgotmitmd = None
        if iv is None:
            iv = ctext[-16:]
        return decrypt_cbc(ctext, self.key, iv)


##  Performing a MITM attack on diffie-hellman using a bogus public key passing
##  (the p as a public key, which is 0 mod p )
if True:#__name__ == '__main__':
    msg = b"A buttered banana's s'more is what you're least likely to get"
    p = 73
    g = 2
    Alice = dh.agent(p, g) # initializing A and B with their public and private keys
    Bob = dh.agent(p, g)
    Mal = mal_agent(p, g)

    Mal.get_1(Alice.give_pubkey())
    Bob.gen_session_key(Mal.send_to_())
    Mal.get_2(Bob.give_pubkey())
    Alice.gen_session_key(Mal.send_to_())
    ctextA = Alice.encrypt_msg(msg)

    ctextAB = Bob.encrypt_msg(ctextA)

    print(Mal.mitm(ctextA))