from util import modexp
from sha1_mac import sha1
import random


class srp:
    N = None
    g = None
    k = None
    I = None
    P = None

    def __init__(self, N, g, k, I, P):
        self.N = N
        self.g = g
        self.k = k
        self.I = I
        self.P = P


class srp_server(srp):
    salt = None
    v = None
    b = None
    B = None
    A = None
    uH = None
    u = None
    S = None
    K = None
    x = None

    def gen_pubkey(self):
        self.salt = str(random.randint(0, self.N - 1)).encode()
        xH = sha1(self.salt+self.P)
        x = int.from_bytes(xH, 'big')
        self.x = int.from_bytes(xH, 'big')  # for debugging
        self.v = modexp(self.g, x, self.N)
        self.b = random.randint(0, self.N - 1)
        self.B = (self.k*self.v + modexp(self.g, self.b, self.N)) % self.N
        return self.salt, self.B

    def set_client_pubkey(self, A):
        bB = int.to_bytes(self.B, (self.B.bit_length()+7)//8, 'big')
        bA = int.to_bytes(A, (A.bit_length()+7)//8, 'big')
        self.A = A
        self.uH = sha1(bA+bB)
        self.u = int.from_bytes(self.uH, 'big')
        self.S = modexp(self.A * modexp(self.v, self.u, self.N), self.b, self.N)
        self.K = sha1(self.S.to_bytes((self.S.bit_length()+7)//8, 'big'))
        return

    def __str__(self):
        return str([('salt',self.salt),('v',self.v),('b',self.b),('B',self.B),
                    ('A',self.A),('uH',self.uH),('u',self.u),('S',self.S),('K',self.K),('x',self.x)])


def client_key(B, k, g, x, a, u, N, debug=False):
    temp = modexp(g, x, N)
    retval = modexp(B -k*temp, a+u*x, N)
    if debug:
        print("Client key is : "+str(retval))
    return retval


def server_key(A, v, u, b, N, debug=False):
    temp = modexp(v, u, N)
    retval = modexp(A*temp, b, N)
    if debug:
        print("Server key is : "+str(retval))
    return retval


def check_keygen(N, g, k, a, b, trials=10, xmax=99999, umax=99999):
    A = modexp(g, a, N)
    for _ in range(1, trials):
        x = random.randint(1, xmax)
        u = random.randint(1, umax)
        v = modexp(g, x, N)
        B = k*v + modexp(g, b, N)
        print(N, g, k, a, A, b, B, x, u, v)
        assert client_key(B, k, g, x, a, u, N, debug=True) == server_key(A, v, u, b, N, debug=True)


class srp_client(srp):
    a = None
    A = None
    B = None
    uH = None
    u = None
    S = None
    K = None
    x = None

    def gen_pubkey(self):
        self.a = random.randint(0, self.N - 1)
        self.A = modexp(self.g, self.a, self.N)
        return self.I, self.A

    def set_server_pubkey(self, salt, B):
        bB = int.to_bytes(B, (B.bit_length()+7)//8, 'big')
        bA = int.to_bytes(self.A, (self.A.bit_length()+7)//8, 'big')
        self.B = B
        self.uH = sha1(bA+bB)
        self.u = int.from_bytes(self.uH, 'big')
        xH = sha1(salt+self.P)
        x = int.from_bytes(xH, 'big')
        self.x = x
        self.S = modexp(self.B - self.k*modexp(self.g, x, self.N), self.a + self.u * x, self.N)
        self.K = sha1(self.S.to_bytes((self.S.bit_length()+7)//8, 'big'))
        return

    def __str__(self):
        return str([('a',self.a),('B',self.B),('A',self.A),('uH',self.uH),
                    ('u',self.u),('S',self.S),('K',self.K),('x',self.x)])


def check_srp(N=662505174548378135863530772829, g=2, k=3,
              I=b"tremaine@clements.pizza", P=b"I'm the hiphopapotamus"):
    Client = srp_client(N, g, k, I, P)
    Server = srp_server(N, g, k, I, P)
    Client.gen_pubkey()
    Server.gen_pubkey()
    Client.set_server_pubkey(Server.salt, Server.B)
    Server.set_client_pubkey(Client.A)
    assert Client.u == Server.u
    assert Client.uH == Server.uH
    assert Client.x == Server.x
    assert modexp(Server.g, Server.x, Server.N) == Server.v
    assert modexp(Client.g, Client.a, Client.N) == Client.A
    assert Client.S == Server.S
    assert Client.K == Server.K
    return True


N, g, k, I, P = 101, 2, 3, b'tremaine', b'clement'

Client = srp_client(N, g, k, I, P)
Server = srp_server(N, g, k, I, P)
Client.gen_pubkey()
Server.gen_pubkey()
Client.set_server_pubkey(Server.salt, Server.B)
Server.set_client_pubkey(Client.A)
