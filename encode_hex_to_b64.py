import os
import sys



def encod(HcharA, HcharB, HcharC):
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
    

if len(sys.argv) < 2:
    print('Not enough arguments specified')
    sys.exit()

hex_str = sys.argv[1]

bin_str = bin(int(hex_str, 16))

hex_len = len(hex_str)

i = 0

base64list = []
if (hex_len%3 == 2):
    HcharA = '0'
    HcharB = hex_str[0]
    HcharC = hex_str[1]
    i += 2
    base64list += encod(HcharA,HcharB,HcharC)
elif (hex_len%3 == 1):
    HcharA = '0'
    HcharB = '0'
    HcharC = hex_str[0]
    i += 1
    base64list += encod(HcharA,HcharB,HcharC)

while(i < hex_len):
    HcharA = hex_str[i]
    HcharB = hex_str[i+1]
    HcharC = hex_str[i+2]
    base64list += encod(HcharA,HcharB,HcharC)
    i+=3

print("".join(base64list))
