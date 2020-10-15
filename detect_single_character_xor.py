import os
import sys
import single_byte_xor_cypher as sbxc
from multiprocessing import Pool

if(len(sys.argv) < 2):
    print("Needs at least one argument, A file that exists, ideally")
    sys.exit()

fname = sys.argv[1]

lines = open(fname).readlines()

if __name__ == '__main__':
    with Pool(6) as p:
        decoded = p.map(sbxc.singlebyte, lines)
    dec0ded = []
    for i in range(0,len(decoded)):
        dec0ded.append((i,decoded[i]))
    so_decoded = sorted(dec0ded, key=lambda x:x[1][0], reverse=True)
    # this array 
    for s in so_decoded:
        print(s)

#for l in lines:
#    print(sbxc.singlebyte(l))
    
