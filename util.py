import random

#collection of functions that I've used throughout this code


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
    if(i >= 0 and i <= 25):
        int_to_b64[i] = chr(i+65)
        b64_to_int[chr(i+65)] = i
    elif(i >= 26 and i <= 51):
        int_to_b64[i] = chr(i+71)
        b64_to_int[chr(i+71)] = i
    elif(i >= 52 and i <= 61):
        int_to_b64[i] = chr(i-4)
        b64_to_int[chr(i-4)] = i
    elif(i == 62):
        int_to_b64[i] = '+'
        b64_to_int['+'] = i
    elif(i == 63):
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
    x = random.randint(0,2**(8*i))
    return x.to_bytes(i, 'big')

