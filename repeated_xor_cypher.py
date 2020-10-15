import os
import sys

    
def repeatkey(string, key):
    l0 = len(string)
    l1 = len(key)
    return key*(int(l0/l1)+1)

def pad(string):
    l = len(string) + len(string)%2
    return string.zfill(l)

def xordem(string, key):
    ord0 = [ord(c) for c in string]
    ord1 = [ord(c) for c in repeatkey(string, key)]
    xord = [ord0[i] ^ ord1[i] for i in range(0, len(ord0))]
    #for s in xord:
    #    print(s)
    hexd = "".join([hex(s)[2:].zfill(2) for s in xord])
    return pad(hexd)

    

if __name__ == "__main__":
    if(len(sys.argv)) < 3:
        print("Need an arg for string, and another for key")
        sys.exit()
    key = sys.argv[2]
    string = sys.argv[1]
    print(xordem(string, key))
