import random

#collection of functions that I've used throughout this code


def mexp(a, b, p, precomp):
    if b in precomp:
        return precomp[b]
    else:
        r0 = mexp(a, b//2, p, precomp)  # For some godforsaken reason int(b/2) is not the same as b//2
        # for giganto numbers, which makes the thing wrong for the cases that you cannot easily check
        precomp[b//2] = r0
        r1 = mexp(a, (b+1)//2, p, precomp)
        precomp[(b+1)//2] = r1
        return (r0*r1) % p


def modexp(a, b, p, debug=False):
    # a**b mod p = a**(b/2) * a**(b/2) mod p
    # where a, b, and p are integers and p is prime
    a = a % p
    b = b % (p-1) # Fermat's little theorem
    if a == 0:
        return 0
    if a == 1:
        return 1
    precomp = {0: 1, 1: a}
    retval = mexp(a, b, p, precomp)
    if debug:
        print(precomp)
    return retval


def sumbits(i0):
    #sums the bits in a numero
    i = i0
    cnt = 0
    while i != 0:
        cnt += i%2
        i = i >> 1
    return cnt


int_to_b64 = {}
b64_to_int = {}
for i in range(0,64):
    if 0 <= i <= 25:
        int_to_b64[i] = chr(i+65)
        b64_to_int[chr(i+65)] = i
    elif 26 <= i <= 51:
        int_to_b64[i] = chr(i+71)
        b64_to_int[chr(i+71)] = i
    elif 52 <= i <= 61:
        int_to_b64[i] = chr(i-4)
        b64_to_int[chr(i-4)] = i
    elif i == 62:
        int_to_b64[i] = '+'
        b64_to_int['+'] = i
    elif i == 63:
        int_to_b64[i] = '/'
        b64_to_int['/'] = i
#print(b64_to_int)


def b64_to_bytes(b64):
    if(len(b64)%4 != 0):
        lgth = len(b64) + 4 - len(b64)%4
        b64 = b64.ljust(lgth, '=')
    lgth = len(b64)
    bytez = []
    for i in range(0,int(lgth/4) - 1):
        #print([b64[4*i:4*i+4]])
        tripbyte = (b64_to_int[b64[4*i+3]] << 0) + (b64_to_int[b64[4*i+2]] << 6) + (b64_to_int[b64[4*i+1]] << 12) + (b64_to_int[b64[4*i+0]] << 18)
        #print(tripbyte)
        bytez+=([(tripbyte >> 16)&255, (tripbyte >> 8)&255, (tripbyte)&255 ])
    if(b64[lgth - 4] == '='):
        print("This should be impossible 2!!!")
        return bytez
    elif(b64[lgth - 3] == '='):
        print("This should be impossible!!!")
        return bytez
    elif(b64[lgth - 2] == '='):
        byt = (b64_to_int[b64[lgth-4]] << 2) + (b64_to_int[b64[lgth-3]] >> 4)
        bytez += ([byt])
        return bytez
    elif(b64[lgth - 1] == '='):
        dubyte = (b64_to_int[b64[lgth-4]]<<10)+(b64_to_int[b64[lgth-3]]<<4)+(b64_to_int[b64[lgth-2]]>>2)
        bytez += ([dubyte >> 8, dubyte & 255])
        return bytez
    return bytez


def gen_bytes(size=16):
    i = random.randint(0,2**(size*8))
    return i.to_bytes(size, 'big')


def randbytes(low=5, hi=11):
    i = random.randint(low, hi)
    x = random.randint(0,2**(8*i)-1)
    return x.to_bytes(i, 'big')


def encode_hex_to_b64(HcharA, HcharB, HcharC):
    bin_str = str(bin(int("".join(['f',HcharA,HcharB,HcharC]), 16)))
    blen = len(bin_str)
    t1 = bin_str[blen-6:blen]
    t0 = bin_str[blen-12:blen-6]
    it0 = int(t0, 2)
    it1 = int(t1, 2)
    if(it0 >= 0 and it0 <= 25):
        b64_0 = chr(it0+65)
    elif(it0 >= 26 and it0 <= 51):
        b64_0 = chr(it0+71)
    elif(it0 >= 52 and it0 <= 61):
        b64_0 = chr(it0-4)
    elif(it0 == 62):
        b64_0 = '+'
    elif(it0 == 63):
        b64_0 = '/'
    if(it1 >= 0 and it1 <= 25):
        b64_1 = chr(it1+65)
    elif(it1 >= 26 and it1 <= 51):
        b64_1 = chr(it1+71)
    elif(it1 >= 52 and it1 <= 61):
        b64_1 = chr(it1-4)
    elif(it1 == 62):
        b64_1 = '+'
    elif(it1 == 63):
        b64_1 = '/'
    return [b64_0 , b64_1]