from sha1_mac import macify

macify()

def padd(mensaje):
    H0 = macify(mensaje, b'')
    l = len(mensaje)
    m = l%64
    if m < 56:
        add = 56-m-1
    else:
        add = 56-m-1+56
    mtext = mensaje+b'\x80'+b'\x00'*add
    return mtext+int.to_bytes(l, 8, 'big')

h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0

def xordem(b0, b1, b2=0, b3=0):
    #xors a bunch of byte arrays
    i0 = int.from_bytes(b0, 'big')
    i1 = int.from_bytes(b1, 'big')
    i2 = int.from_bytes(b2, 'big')
    i3 = int.from_bytes(b3, 'big')
    xint = i0^i1^i2^i3
    return xint

def lrotate(x, n):
    #left rotates a 32 bit int, assuming big endianess
    return ((x << n) + (x >> (32-n))) & (2**32-1)

def SHA1_YO(text, a=h0, b=h1, c=h2, d=h3, e=h4):
    m1 = len(text)
    mtext = padd(text)
    if (len(mtext)%64) != 0:
        print("The dang padded text needs to be a multiple of 64 bytes")
        return None
    words = [0]*80
    for i in range(len(mtext)/64):
        for j in range(0,16):
            words[j] = mtext[4*j:4*(j+1)]
        for j in range(16,64):
            words[j] = lrotate(xordem(words[j-3], words[j-8], words[j-14], words[j-16]), 1)
        a = 

