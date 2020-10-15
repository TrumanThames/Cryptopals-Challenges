from functools import reduce
from math import ceil
import single_byte_xor_cypher as sbxc
import copy
import sys
import repeated_xor_cypher as rxc


def sumbits(i0):
    #sums the bits in a numero
    i = i0
    cnt = 0
    while i != 0:
        cnt += i%2
        i = i >> 1
    return cnt

def stringed(byted_thing):
    return "".join([chr(x) for x in byted_thing])

def byted(chrs, istextbytes=False):
    if istextbytes:
        return chrs
    else:
        return [ord(c) for c in chrs]

def hammingD(s1, s2, istextbytes=False):
    h1 = byted(s1, istextbytes)
    h2 = byted(s2, istextbytes)
    sum_xrd = [sumbits(h1[i] ^ h2[i]) for i in range(0,min(len(h1), len(h2)))]
    def f(x,y):
        return x+y
    return reduce(f, sum_xrd, 0)

def blockbreak(text, ksz):
    blocks = [copy.deepcopy([]) for x in range(0,ksz)]
    for i in range(0,len(text)):
        blocks[i%ksz].append(text[i])
    #strocks = []
    #for b in blocks:
    #    strocks.append("".join(b))
    return blocks

def fullFat(kszblck,length,ksz):
    strstr = []
    kblck = {}
    key = []
    #print("len(kszblck) = "+str(len(kszblck)))
    #print("ksz = "+str(ksz))
    #print("len(text) = "+str(length))
    for i in range(0,len(kszblck)):
        kblck[i] = sbxc.singlebyte("".join([hex(x)[2:].zfill(2) for x in kszblck[i]]), True, 0)
        #print("Score = "+str(kblck[i][0]))
        #print("kszblck[i] = "+str(kszblck[i]))
        #print("I actually pass this to singlebyte : "+"".join([hex(x)[2:].zfill(2) for x in kszblck[i]]))
        #print("kblck[i][1] = "+str([int(x) for x in kblck[i][1]]))
    for i in range(0,length):
        strstr.append(kblck[i%ksz][1][int(i/ksz)])
    for i in range(0,len(kszblck)):
        #print(kblck[i][2])
        key.append(kblck[i][2])
    #print(kblck[0])
    return (strstr, key)

def break_it(text, num_kszs=3, istextbytes=False):
    num_kszs = min(num_kszs, int(len(text)/4)-1, 42)
    hammin_keysize = {}
    for i in range(2,44):
        if(len(text) >= i*4):
            hams = hammingD(text[:i], text[i:2*i], istextbytes) + hammingD(text[i:2*i], text[2*i:3*i], istextbytes) + hammingD(text[2*i:3*i], text[3*i:4*i], istextbytes) + hammingD(text[:i], text[2*1:3*i], istextbytes) + hammingD(text[:i], text[3*i:4*i], istextbytes) + hammingD(text[i:2*i], text[3*i:4*i], istextbytes)
            hammin_keysize[i] = hams/(i*6*8)
    so_hammin = sorted(hammin_keysize.items(), key=lambda x:x[1])
    kszs = {}
    kszblcks = {}
    kbs = {}
    #print("so_hammin length : "+str(len(so_hammin)))
    for i in range(0,num_kszs):
        kszs[i] = so_hammin[i][0]
        kszblcks[i] = blockbreak(byted(text, istextbytes), kszs[i])
        kbs[i] = fullFat(kszblcks[i], len(text), kszs[i])
        print("keysize : "+str(kszs[i]))
        print("Key : "+str((kbs[i][1]))+stringed(kbs[i][1]))
        #print("First 100 : " +str(kbs[i][0][:100]))
        print("Full string (actually no, just firs 500 chars) : \n"+stringed(kbs[i][0][:500]))
    return

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
        bytez+=([byt])
        return bytez
    elif(b64[lgth - 1] == '='):
        dubyte = (b64_to_int[b64[lgth-4]]<<10)+(b64_to_int[b64[lgth-3]]<<4)+(b64_to_int[b64[lgth-2]]>>2)
        bytez+=([dubyte >> 8, dubyte & 255])
        return bytez
    return bytez



num_keysizes = 3

if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        num_keysizes = int(sys.argv[1])

"""
str1ng = 'But when a banana breaks it\'s skin,\nthere\'s no rest of us.'
x_str1ng = rxc.xordem(str1ng, 'PaAya')
b_str1ng = list(bytes.fromhex(x_str1ng))
break_it(b_str1ng, num_keysizes, True)


data = open('6.txt', 'r').read().replace('\n','')
b_data = b64_to_bytes(data)
#print(data)
#print(b_data)
break_it(b_data, num_keysizes, True)
"""