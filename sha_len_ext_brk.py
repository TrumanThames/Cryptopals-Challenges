from sha1_mac import sha1
from random import randint


def padd(mensaje):
    #performs the sha1 padding, return value should be 0mod64 bytes long and other stuff
    #other stuff being having a '1' bit immediately after the message followed by zeros
    #until the last 64bits which are the length of the original message in bits as a big endian integer
    #H0 = macify(mensaje, b'')
    l = len(mensaje)
    m = l%64
    if m < 56:
        add = 56-m-1
    else:
        add = 56-m-1+64
    mtext = mensaje+b'\x80'+b'\x00'*add
    return mtext+int.to_bytes(l*8, 8, 'big')


h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0


def xordem(b0, b1, b2=b'', b3=b''):
    #xors a bunch of byte arrays
    #thinking about it, for different length bytestrings, endianess is kinda weird
    #and probably does not work like you'd want
    l = max(len(b0), len(b1), len(b2), len(b3))
    i0 = int.from_bytes(b0, 'big')
    i1 = int.from_bytes(b1, 'big')
    i2 = int.from_bytes(b2, 'big')
    i3 = int.from_bytes(b3, 'big')
    xint = i0^i1^i2^i3
    return xint.to_bytes(l, 'big')


def lrot1(x):
    # these are redundant different implementations of rotations
    # I was checking to make sure I had done it correctly
    return ((x<<1) + ((x&(2**31)) == 2**31)) & (2**32 - 1)


def lrotn(x, n):
    for i in range(0,n):
        x = lrot1(x)
    return x


def lrotate(x, n):
    #left rotates a 32 bit int, assuming big endianess
    #does not modify x or n.  Needs 0 <= n <= 32
    #x = x & (2**32 - 1)
    return ((x << n) + (x >> (32-n))) & (2**32 - 1)


def rrot1(x):
    return ((x >> 1) | ((x%2) << 31)) & (2**32 - 1)


def rrotn(x, n):
    for i in range(0,n):
        x = rrot1(x)
    return x


def blrotate(b, n):
    #left rotates a 32bit (4byte) bytestring
    return lrotn(int.from_bytes(b, 'big'), n).to_bytes(4, 'big')


def SHA1_YO(text, a1=h0, b1=h1, c1=h2, d1=h3, e1=h4):
    # this should hash the text variable (a bytestring) with sha1 initial registers a,b,c,d,e
    m1 = len(text)
    mtext = padd(text)
    if (len(mtext)%64) != 0:
        print("The dang padded text needs to be a multiple of 64 bytes")
        return None
    words = [0]*80
    for i in range(0, int(len(mtext)/64)):
        a = a1
        b = b1
        c = c1
        d = d1
        e = e1
        for j in range(0,16):
            words[j] = int.from_bytes(mtext[4*j+i*64:4*(j+1)+i*64], 'big')
        for j in range(16,80):
            words[j] = lrotn(words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16], 1)
        for j in range(0,80):
            if j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = (lrotn(a, 5) + f + e + k + words[j]) & (2**32 - 1)
            e = d
            d = c
            c = lrotn(b, 30)
            b = a
            a = temp
        a1 = (a1 + a) & (2**32 - 1)
        b1 = (b1 + b) & (2**32 - 1)
        c1 = (c1 + c) & (2**32 - 1)
        d1 = (d1 + d) & (2**32 - 1)
        e1 = (e1 + e) & (2**32 - 1)
    abcde = ((a1 << 128) | (b1 << 96) | (c1 << 64) | (d1 << 32) | e1) & (2**160 - 1)
    return abcde.to_bytes(20, 'big')


def test_rotatos(n=1233):
    for i in range(0,n):
        x = randint(0,2**32-1)
        for j in range(0,33):
            if lrotate(x,j) != lrotn(x,j):
                print("What the HECK!!!!! "+str((x,j)))
                return 1
            if rrotn(lrotate(x,j), j) != x:
                print("Oh GOSH!!  "+str(x,j))
                return 1
            if rrotn(lrotn(x,j),j) != x:
                print("OH NOOOOOOOOOO!?!?!?1    "+str(x,j))
                return 1
    return 0
