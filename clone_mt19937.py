import mt19937
from math import ceil
from random import randint
from copy import deepcopy
import sys


(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253

lower_mask = (1 << r) - 1
upper_mask = (2**(w) - 1) & (~ lower_mask)

def untemp_help(a, b, lr, y1, w, deb=False):
    #supposed to be a general step untemperer for whatever choices of mersenne twister
    #backsolve for y0 in y1 = y0 ^ ((y0 {<< or >>} a) & b)
    # where y0 and y1 are w bit integers
    # lr is a bool, if lr then its a leftshift if not its a rightshift
    if a >= w:
        return y1
    mask = 2**a - 1
    y1 = y1 & (2**w - 1)
    y0 = 0
    loops = ceil(w/a)
    y0blocks = [0]*loops
    if (not lr):
        y0blocks[0] = y1 >> (w-a)
        if deb: print(y0blocks[0])
        y0 += y0blocks[0] << (w-a)
        for i in range(1,loops-1):
            y0blocks[i] = ((y1 >> (w-(i+1)*a)) ^ (y0blocks[i-1] & (b >> (w-(i+1)*a)))) & mask
            if deb : print(y0blocks[i])
            y0 += y0blocks[i] << (w-(i+1)*a)
        y0blocks[loops-1] = (((y1 << (a*loops - w)) ^ (y0blocks[loops-2] & (b << (a*loops - w)))) >> (a*loops - w)) & (2**(w-a*(loops-1))-1)
        if deb : print(y0blocks[loops-1])
        y0 += y0blocks[loops-1]
    else:
        y0blocks[0] = y1 & mask
        if deb : print(y0blocks[0])
        y0 += y0blocks[0]
        for i in range(1, loops):
            y0blocks[i] = ((y1 >> (i*a)) ^ (y0blocks[i-1] & (b >> (i*a)))) & mask
            if deb : print(y0blocks[i])
            y0 += y0blocks[i] << (i*a)
    return y0

def untemper(y):
    y = untemp_help(l, 0xFFFFFFFF, False, y, 32)
    y = untemp_help(t, c, True, y, 32)
    y = untemp_help(s, b, True, y, 32)
    y = untemp_help(u, d, False, y, 32)
    return y

def temper(y):
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    return (2**w - 1) & y

def test_untmp_hlp(n=111):
    for i in range(0,n):
        fell = False
        aran = randint(1,29)
        bran = randint(0,2**32-1)
        yran = randint(0,2**32-1)
        xran = randint(0,2**32-1)
        unrxran = untemp_help(aran, bran, False, xran, 32)
        unlxran = untemp_help(aran, bran, True, xran, 32)
        reunrxran = unrxran ^ ((unrxran >> aran)&bran)
        reunlxran = unlxran ^ ((unlxran << aran)&bran)
        rtempy = yran ^ ((yran >> aran) & bran)
        unrtempy = untemp_help(aran, bran, False, rtempy, 32)
        reunrtempy = unrtempy ^ ((unrtempy >> aran)&bran)
        ltempy = yran ^ ((yran << aran) & bran)
        unltempy = untemp_help(aran, bran, True, ltempy, 32)
        reunltempy = unltempy ^ ((unltempy << aran)&bran)
        if not (yran == unrtempy and rtempy == reunrtempy):
            print("untemp help failed for params: "+str((aran,bran,False,rtempy,32)))
            print("yran is: "+str(yran))
            fell = True
        if not (yran == unltempy and ltempy == reunltempy):
            print("untemp help failed for params: "+str((aran,bran,True,rtempy,32)))
            print("yran is: "+str(yran))
            fell = True
        if not (xran == reunrxran):
            print("untemp help failed for params: "+str((aran,bran,False,xran,32)))
            print("unrxran is: "+str(unrxran))
            fell = True
        if not (xran == reunlxran):
            print("untemp help failed for params: "+str((aran,bran,True,xran,32)))
            print("unlxran is: "+str(unlxran))
            fell = True
        if fell: return
    return

def m_twist(M): #Seems to freakin be correct, so there
    mM = M
    for i in range(0,n):
        x = (mM[i] & upper_mask) + (mM[(i+1) % n] & lower_mask)
        xA = x >> 1
        if (x % 2) == 1: #lowest bit of x is 1
            xA = xA ^ a
        mM[i] = mM[(i + m) % n] ^ xA
    return mM



def extract(M,i):
    if i >= n:
        if i > n:
            print("Error: Generator was never seeded")
            return None
        print("Err: index out of range, retwist and reindex mayhaps?")
        return None
    y = M[i]
    return temper(y)

def test_temp_untemp(n=9):
    for i in range(0,n):
        x = randint(0,2**32-1)
        y = randint(0,2**32-1)

def clone_mt(extrct):
    #for the return value to be the state
    #extrct must be a mt19937 at the start of it's cycle
    stuff = [0]*n
    for i in range(0,n):
        outs = extrct()
        stuff[i] = untemper(outs)
    return m_twist(stuff)

